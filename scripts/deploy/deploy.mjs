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
    .option(
        '-n, --no-interaction',
        'Deploy without interactive questions',
        true
    )
    .option(
        '-c, --context <context>',
        'Deploy specific context from .hasura/context.yaml',
        'default'
    )
    .requiredOption(
        '-p --profile <profile>',
        'Deploy from demo config in supergraph-config/<profile>',
    )
    .option(
        '-r, --rebuild-connectors',
        'Rebuild all connectors as a result of changing connector configuration (warning: slow)',
        false
    )
    .option(
        '-f, --full-metadata-build',
        'Perform a full rebuild of metadata to build up functionality on DDN',
        false
    )
    .option(
        '-x, --override-description <description>',
        'Override the automatically generated deployment description',
    )
    .parse(process.argv);

// Load command options
const options = program.opts();
const logLevel = options.logLevel.toUpperCase();
const override = options.override;
const dryRun = options.dryRun;
const noInteraction = !options.interaction;
const rebuildConnectors = options.rebuildConnectors;
const context = options.context;
const profile = options.profile;
const fullMetadataBuild = options.fullMetadataBuild;

// Locate the script to allow it to be used from anywhere
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const script_dir = __dirname;
const jwtFile = join(script_dir, 'jwtauth.hml');
const noauthFile = join(script_dir, 'noauth.hml');
const root = resolve(__dirname, '../../hasura/');

console.log(chalk.magentaBright('Resolved repository root:', root));

if (!fs.existsSync(root)) {
    console.error(
        chalk.whiteBright.bgRed(`Error: Directory ${root} does not exist.`)
    );
    process.exit(1);
}

// Change the working directory to hasura subdirectory so ddn can find .hasura/context.yaml
const workingDir = join(root);
process.chdir(workingDir);

console.log(chalk.magentaBright('Changed working directory to:', process.cwd()));

if (!fs.existsSync('.hasura/context.yaml')) {
    console.error(
        chalk.whiteBright.bgRed(
            'Error: .hasura/context.yaml not found in the current working directory.'
        )
    );
    process.exit(1);
}

// Validate profile
const profilePath = resolve(root, 'supergraph-config', profile);
if (!fs.existsSync(profilePath)) {
    console.error(
        chalk.whiteBright.bgRed(
            `Invalid profile: ${profile}. Profile directory does not exist within ${root}/supergraph-config`
        )
    );
    process.exit(1);
}

const supergraphConfig = resolve(root, 'supergraph-config', profile);
console.log(chalk.magentaBright('Resolved supergraph config:', supergraphConfig));

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
console.log(
    chalk.magentaBright(
        `Connectors ${rebuildConnectors ? 'will' : "won't"} be rebuilt`
    )
);
console.log(chalk.magentaBright(`Context: ${context}`));
console.log(
    chalk.magentaBright(
        `Full metadata build is: ${fullMetadataBuild ? 'enabled' : 'disabled'}`
    )
);
console.log(
    chalk.magentaBright(
        `No interaction mode is: ${noInteraction ? 'enabled' : 'disabled'}`
    )
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

// Helper function to convert each connector to the right region
function convertConnectorRegion(connectorRegion) {
    console.log(
        chalk.magentaBright(
            `Converting 'connector.yaml' files to ${connectorRegion}.`
        )
    );

    const yamlFiles = findConnectorYamlFiles(root);
    yamlFiles.forEach((file) => updateRegionInFile(file, connectorRegion));

    console.log(
        chalk.magentaBright(
            `All 'connector.yaml' files have been updated to use the region ${connectorRegion}.`
        )
    );
}

// Run the command that the deploy script defines
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
async function applyBuild(region, buildVersion) {
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
    rebuildConnectors = true
) {
    const DEST_DIR = join(root, '/globals');
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

    // Construct the description, either from the git log or via a user generated override
    let gitLogDescription = options.overrideDescription || null;

    if (gitLogDescription === null) {
        // Get git log description for the command to use as the supergraph build description
        gitLogDescription = execSync(
            `git log -1 --pretty=format:"%h [${tag}] %s"`
        )
            .toString()
            .trim();
    }

    // Construct the ddn supergraph build command
    let command = `ddn supergraph build create -d "${gitLogDescription}" -c "${region}" --out json --log-level "${logLevel}" --supergraph "${supergraph}"`;
    if (!rebuildConnectors) {
        command += ' --no-build-connectors';
    }

    if (!dryRun) {
        console.log(
            chalk.magentaBright(`[${region}] => Executing command: ${command}`)
        );
        const output = await runCommandWithOutput(command, region);
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

// Pushes incremental release of metadata
async function pushMetadataRelease(supergraph, contextRegion, rebuildConnectors) {
    console.log(
        chalk.magentaBright(
            `[${contextRegion}] => Starting an incremental release of metadata.`
        )
    );

    // Deploy with JWT file to demo authz
    await runCommandWithTag(
        contextRegion,
        jwtFile,
        'JWT',
        supergraph,
        rebuildConnectors
    );

    // Deploy with NoAuth file to allow instant access
    await runCommandWithTag(
        contextRegion,
        noauthFile,
        'NoAuth',
        supergraph,
        rebuildConnectors
    );

    console.log(
        chalk.green(
            `[${contextRegion}] => Incremental release completed successfully.`
        )
    );
}

// Rebuild function that does not use --no-build-connectors
async function rebuildSupergraph(supergraphs, contextRegion, rebuildConnectors) {
    console.log(
        chalk.magentaBright(
            `[${contextRegion}] => Starting a complete rebuild of all supergraphs.`
        )
    );

    let index = 1;

    for (const supergraph of supergraphs) {
        await runCommandWithTag(
            contextRegion,
            noauthFile,
            `NoAuth S-${index}`,
            supergraph,
            rebuildConnectors
        );
        index++;
    }

    console.log(
        chalk.green(`[${contextRegion}] => Rebuild completed successfully.`)
    );
}

// Load all supergraphs from the relevant industry profile in supergraph-config
// Order them numerically and return them so they can be built
function getSupergraphs() {
    let files = fs.readdirSync(supergraphConfig);
    files = files
        .filter(file => file.endsWith('.yaml'))
        .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));

    const supergraphs = files.map(file => join(supergraphConfig, file));

    return supergraphs;

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

    let context = options.context || null;
    let rebuildConnectors = options.rebuildConnectors || null;
    let fullMetadataBuild = options.fullMetadataBuild || null;

    if (!noInteraction && context === null) {
        context = (
            await inquirer.prompt([
                {
                    type: 'list',
                    name: 'context',
                    message: 'Select a context to set:',
                    choices: Object.keys(regionMapping),
                },
            ])
        ).context;
    }

    if (!noInteraction && fullMetadataBuild === null) {
        fullMetadataBuild = (
            await inquirer.prompt([
                {
                    type: 'confirm',
                    name: 'fullMetadataBuild',
                    message:
                        'Do you want to perform a full metadata rebuild? (warning slow)',
                    default: false,
                },
            ])
        ).fullMetadataBuild;
    }

    if (!noInteraction && rebuildConnectors === null) {
        rebuildConnectors = (
            await inquirer.prompt([
                {
                    type: 'confirm',
                    name: 'rebuildConnectors',
                    message:
                        'Do you want to perform a full connector rebuild? (warning even slower)',
                    default: false,
                },
            ])
        ).rebuildConnectors;
    }

    // Map the selected context region to the GCP region ID
    const connectorRegion = regionMapping[context] || regionMapping['default'];

    // switch connectors to the right region
    convertConnectorRegion(connectorRegion);

    // Split up all intermediate supergraphs from the final one and
    // build each intermediate supergraph with rebuildSupergraph if
    // --full-metadata-build is selected
    // If --full-metadata-build is not selected or if there is only a single
    // supergraph, only build that with pushMetadataRelease
    const supergraphs = getSupergraphs();

    if (supergraphs.length === 0) {
        throw new Error("No supergraphs found!");
    }
    const intermediarySupergraphs = supergraphs.slice(0, -1);
    const fullyBuiltSupergraph = supergraphs[supergraphs.length - 1];

    if (fullMetadataBuild && intermediarySupergraphs.length > 0) {
        await rebuildSupergraph(intermediarySupergraphs, context, rebuildConnectors);
    }

    await pushMetadataRelease(fullyBuiltSupergraph, context, rebuildConnectors);

    // Revert connectors to the default
    convertConnectorRegion(regionMapping['default']);

    console.log(
        chalk.green(`[${context}] => Deployment completed successfully.`)
    );
}

main().catch((error) => {
    console.error(
        chalk.whiteBright.bgRed(`Unexpected error: ${error.message}`)
    );
    process.exit(1);
});
