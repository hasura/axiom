#!/usr/bin/env node

import fs from 'fs';

import { dirname, resolve, join } from 'path';
import yaml from 'yaml';
import chalk from 'chalk';
import inquirer from 'inquirer';
import simpleGit from 'simple-git';
import { fileURLToPath } from 'url';
import { spawn, execSync } from 'child_process';
import shellQuote from 'shell-quote';
import { Command } from 'commander';

const git = simpleGit();

// Initialize commander
const program = new Command();

program
    .option(
        '-l, --log-level <level>',
        'Set the log level (FATAL, ERROR, WARN, INFO, DEBUG)',
        'FATAL'
    )
    .option(
        '-o, --override',
        'Override branch and uncommitted changes checks',
        false
    )
    .option(
        '-d, --dry-run',
        'Simulate the deployment without executing commands',
        false
    )
    .parse(process.argv);

const options = program.opts();
const logLevel = options.logLevel.toUpperCase();
const override = options.override;
const dryRun = options.dryRun;

// Validate log level
const allowedLogLevels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'];
if (!allowedLogLevels.includes(logLevel)) {
    console.error(
        chalk.whiteBright.bgRed(
            `Invalid log level: ${logLevel}. Allowed values are: ${allowedLogLevels.join(
                ', '
            )}`
        )
    );
    process.exit(1);
}

console.log(chalk.magentaBright(`Log level set to: ${logLevel}`));
console.log(
    chalk.magentaBright(`Override flag is ${override ? 'enabled' : 'disabled'}`)
);
console.log(
    chalk.magentaBright(`Dry run mode is ${dryRun ? 'enabled' : 'disabled'}`)
);

// Mapping context regions to GCP region IDs
const regionMapping = {
    au: 'gcp-australia-southeast1',
    eu: 'gcp-europe-west1',
    sg: 'gcp-asia-southeast1',
    'us-east': 'gcp-us-east4',
    'us-west': 'gcp-us-west2',
    default: 'gcp-us-west2', // Default axiom-test to us-west
};

// Locate the script to allow it to be used from anywhere
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const root = resolve(__dirname, '../../');
console.log(chalk.magentaBright('Resolved repository root:', root));

if (!fs.existsSync(root)) {
    console.error(
        chalk.whiteBright.bgRed(`Error: Directory ${root} does not exist.`)
    );
    process.exit(1);
}

// Update the region in connector files
function updateRegionInFile(filePath, region) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        let doc = yaml.parse(content);

        if (
            doc.definition &&
            Array.isArray(doc.definition.regionConfiguration)
        ) {
            doc.definition.regionConfiguration.forEach((regionConfig) => {
                regionConfig.region = region;
            });

            const newYaml = yaml.stringify(doc);
            if (!dryRun) {
                fs.writeFileSync(filePath, newYaml, 'utf8');
                console.log(
                    chalk.green(
                        `Successfully updated region to ${region} in ${filePath}`
                    )
                );
            } else {
                console.log(
                    chalk.yellow(
                        `[Dry Run] Would update region to ${region} in ${filePath}`
                    )
                );
            }
        } else {
            console.warn(
                chalk.yellow(
                    `Warning: No valid region configuration found in ${filePath}.`
                )
            );
        }
    } catch (error) {
        console.error(
            chalk.whiteBright.bgRed(
                `Failed to update region in ${filePath}: ${error.message}`
            )
        );
    }
}

// Find all `connector.yaml` files in the supergraph
function findConnectorYamlFiles(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach((file) => {
        const filePath = join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat && stat.isDirectory()) {
            results = results.concat(findConnectorYamlFiles(filePath));
        } else if (file === 'connector.yaml') {
            results.push(filePath);
        }
    });
    return results;
}

function runCommandWithOutput(command, region = '') {
    return new Promise((resolve, reject) => {
        console.log(chalk.magentaBright(`Executing command: ${command}`));

        if (dryRun) {
            console.log(
                chalk.yellow(`[Dry Run] Would execute command: ${command}`)
            );
            return resolve();
        }

        const parsedCommand = shellQuote.parse(command);
        const [cmd, ...args] = parsedCommand;
        const childProcess = spawn(cmd, args);

        let output = '';

        childProcess.stdout.on('data', (data) => {
            const message = data.toString();
            output += message;
            console.log(
                chalk.magentaBright(`[${region}] => ${message.trim()}`)
            );
        });

        childProcess.stderr.on('data', (data) => {
            const message = data.toString();
            console.log(chalk.cyanBright(`[${region}] => ${message.trim()}`));
        });

        childProcess.on('close', (code) => {
            if (code === 0) {
                console.log(
                    chalk.green(`Command completed successfully: ${command}`)
                );
                resolve(output);
            } else {
                console.error(
                    chalk.whiteBright.bgRed(
                        `Command failed with exit code ${code}: ${command}`
                    )
                );
                reject(new Error(`Command failed with exit code ${code}`));
            }
        });
    });
}
// Apply the build using the build version
function applyBuild(region, buildVersion) {
    const command = `ddn supergraph build apply ${buildVersion} -c ${region}`;

    if (!dryRun) {
        console.log(
            chalk.magentaBright(`Applying build version: ${buildVersion}`)
        );
        runCommandWithOutput(command, region);
        console.log(
            chalk.green(`Build version ${buildVersion} applied successfully.`)
        );
    } else {
        console.log(
            chalk.yellow(`[Dry Run] Would apply build version: ${buildVersion}`)
        );
    }
}

// Deploy supergraph
async function runCommandWithTag(
    region,
    srcFile,
    tag,
    supergraph,
    noBuildConnectors = true
) {
    const DEST_DIR = join(__dirname, '../../globals');
    const DEST_FILE = 'auth-config.hml';

    if (!fs.existsSync(srcFile)) {
        console.error(
            chalk.whiteBright.bgRed(
                `Error: Source file ${srcFile} does not exist.`
            )
        );
        process.exit(1);
    }

    // Copy the auth file to the correct location
    if (!dryRun) {
        fs.copyFileSync(srcFile, join(DEST_DIR, DEST_FILE));
        console.log(
            chalk.green(`Copied ${srcFile} to ${DEST_DIR}/${DEST_FILE}`)
        );
    } else {
        console.log(
            chalk.yellow(
                `[Dry Run] Would copy ${srcFile} to ${DEST_DIR}/${DEST_FILE}`
            )
        );
    }

    // Get git log description for the command to use as the supergraph build description
    const gitLogDescription = execSync(
        `git log -1 --pretty=format:"%h [${tag}] %s"`
    )
        .toString()
        .trim();

    // Construct the ddn supergraph build command
    let command = `ddn supergraph build create -d "${gitLogDescription}" -c "${region}" --out json --log-level "${logLevel}" --supergraph "${supergraph}"`;
    if (noBuildConnectors) {
        command += ' --no-build-connectors';
    }

    if (!dryRun) {
        console.log(
            chalk.magentaBright(`[${region}] => Executing command: ${command}`)
        );
        const output = await runCommandWithOutput(command, region);
        // const output = execSync(command, { stdio: 'pipe' }).toString();
        const buildInfo = JSON.parse(output);

        console.log(
            chalk.green(
                `[${region}] => Deployment completed successfully for ${tag}`
            )
        );
        console.log(chalk.green(`Build URL: ${buildInfo.build_url}`));

        // Apply the build using the extracted build_version
        applyBuild(region, buildInfo.build_version);
    } else {
        console.log(
            chalk.yellow(`[Dry Run] Would execute command: ${command}`)
        );
    }
}

// Rebuild function that does not use --no-build-connectors
async function rebuildSupergraph(contextRegion) {
    console.log(
        chalk.magentaBright(
            `[${contextRegion}] => Starting a complete rebuild of all supergraphs and connectors.`
        )
    );

    const NOAUTH_FILE = join(__dirname, 'noauth.hml');
    let index = 1;

    const supergraphs = [
        `${root}/supergraph-project-queries.yaml`,
        `${root}/supergraph-domain.yaml`,
        `${root}/supergraph.yaml`,
        `${root}/supergraph-with-mutations.yaml`,
    ];

    for (const supergraph of supergraphs) {
        await runCommandWithTag(
            contextRegion,
            NOAUTH_FILE,
            `NoAuth RB-${index}`,
            supergraph,
            false
        );
        index++;
    }

    console.log(
        chalk.green(`[${contextRegion}] => Rebuild completed successfully.`)
    );
}

async function main() {
    if (!override) {
        // Check if on the main branch
        const currentBranch = await git.revparse(['--abbrev-ref', 'HEAD']);
        if (currentBranch !== 'main') {
            console.error(
                chalk.whiteBright.bgRed(
                    `Error: You must be on the 'main' branch to deploy.`
                )
            );
            process.exit(1);
        }

        // Check for uncommitted changes
        const status = await git.status();
        if (status.files.length > 0) {
            console.error(
                chalk.whiteBright.bgRed(
                    'Error: Uncommitted changes detected. Please commit or stash changes before running this script.'
                )
            );
            process.exit(1);
        }
    } else {
        console.log(
            chalk.yellow(
                'Override flag enabled: Skipping branch and uncommitted changes checks.'
            )
        );
    }

    const { contextRegion, rebuild } = await inquirer.prompt([
        {
            type: 'list',
            name: 'contextRegion',
            message: 'Select a context region to set:',
            choices: Object.keys(regionMapping),
        },
        {
            type: 'confirm',
            name: 'rebuild',
            message: 'Do you want to perform a complete rebuild?',
            default: false,
        },
    ]);

    // Map the selected context region to the GCP region ID
    const connectorRegion = regionMapping[contextRegion];

    // Update all `connector.yaml` files with the selected region
    const yamlFiles = findConnectorYamlFiles(root);
    yamlFiles.forEach((file) => updateRegionInFile(file, connectorRegion));
    console.log(
        chalk.magentaBright(
            `All 'connector.yaml' files have been updated to use the region ${connectorRegion}.`
        )
    );

    const SCRIPT_DIR = __dirname;
    const JWT_FILE = join(SCRIPT_DIR, 'jwtauth.hml');
    const NOAUTH_FILE = join(SCRIPT_DIR, 'noauth.hml');

    if (rebuild) {
        await rebuildSupergraph(contextRegion);
    }

    await runCommandWithTag(
        contextRegion,
        JWT_FILE,
        'JWT',
        `${root}/supergraph-with-mutations.yaml`,
        true
    ); // Deploy with JWT file
    await runCommandWithTag(
        contextRegion,
        NOAUTH_FILE,
        'NoAuth',
        `${root}/supergraph-with-mutations.yaml`,
        true
    ); // Deploy with NoAuth file

    const defaultRegion = regionMapping['default'];
    console.log(
        chalk.magentaBright(
            `Reverting 'connector.yaml' files to ${defaultRegion}.`
        )
    );
    yamlFiles.forEach((file) => updateRegionInFile(file, defaultRegion));

    console.log(
        chalk.green(`[${contextRegion}] => Deployment completed successfully.`)
    );
}

main().catch((error) => {
    console.error(
        chalk.whiteBright.bgRed(`Unexpected error: ${error.message}`)
    );
    process.exit(1);
});
