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
    // It looks counter inttuitive to default --no-interaction to true but it's correct (see below)
    .option(
        '-n, --no-interaction',
        'Deploy without interactive questions',
        true
    )
    .option(
        '-g, --gcp-region <gcpRegion>',
        'Deploy connectors to a specific GCP region',
        'gcp-us-west2'
    )
    .option(
        '-c, --context <context>',
        'Deploy specific context from .hasura/context.yaml',
        null
    )
    .requiredOption(
        '-p, --profile <profile>',
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
    .option(
        '-q, --quiet',
        'Silence all logging except for errors.',
    )
    .option(
        '-a, --apply-build',
        'Automatically apply the build once it is deployed',
        false
    )
    .parse(process.argv);

// Load command options
const options = program.opts();
const logLevel = options.logLevel.toUpperCase();
const override = options.override;
const dryRun = options.dryRun;
// Counter-intuitive, but --no-interaction is actually changed to options.interaction (nfi why)
// So we reverse it and call the variable something reasonable. This is why --no-interaction
// defaults to true above as (interaction = true) = (no-interaction = false)... at least in my mind
const noInteraction = !options.interaction;
const rebuildConnectors = options.rebuildConnectors;
const gcpRegion = options.gcpRegion;
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

log('magentaBright', `Resolved repository root: ${root}`);

if (!fs.existsSync(root)) {
    throw new Error(`Error: Directory ${root} does not exist.`);
}

// Change the working directory to hasura subdirectory so ddn can find .hasura/context.yaml
const workingDir = join(root);
process.chdir(workingDir);

log('magentaBright', `Changed working directory to: ${process.cwd()}`);

if (!fs.existsSync('.hasura/context.yaml')) {
    console.error(
        chalk.whiteBright.bgRed(
            'Error: .hasura/context.yaml not found in the current working directory.'
        )
    );
    process.exit(1);
}

// Validate region
const availableRegions = [
    'gcp-australia-southeast1',
    'gcp-europe-west1',
    'gcp-asia-southeast1',
    'gcp-us-east4',
    'gcp-us-west2',
];

if (!availableRegions.includes(gcpRegion)) {
    console.error(
        chalk.whiteBright.bgRed(
            `Error: GCP Region ${gcpRegion} not in supported list: ${availableRegions.join(', ')}.`
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
log('magentaBright', `Resolved supergraph config: ${supergraphConfig}`);

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

log('magentaBright', `Log level set to: ${logLevel}`);
log('magentaBright', `Override flag is ${override ? 'enabled' : 'disabled'}`);
log('magentaBright', `Dry run mode is ${dryRun ? 'enabled' : 'disabled'}`);
log('magentaBright', `Connectors ${rebuildConnectors ? 'will' : "won't"} be rebuilt`);
log('magentaBright', `Connector region is set to: ${gcpRegion}`);
log('magentaBright', (`Context: ${context}`));
log('magentaBright', `Full metadata build is: ${fullMetadataBuild ? 'enabled' : 'disabled'}`);
log('magentaBright', `No interaction mode is: ${noInteraction ? 'enabled' : 'disabled'}`);
log('magentaBright', `Automatically apply build is set to: ${options.applyBuild ? 'enabled' : 'disabled'}`);

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
                log('green', `Successfully updated region to ${region} in ${filePath}`);
            } else {
                log('yellow', `[Dry Run] Would update region to ${region} in ${filePath}`);
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
    log('magentaBright', `Converting 'connector.yaml' files to ${connectorRegion}.`);

    const yamlFiles = findConnectorYamlFiles(root);
    yamlFiles.forEach((file) => updateRegionInFile(file, connectorRegion));

    log('magentaBright', `All 'connector.yaml' files have been updated to use the region ${connectorRegion}.`);
}

// Run the command that the deploy script defines
function runCommandWithOutput(command, context = '') {
    return new Promise((resolve, reject) => {
        log('magentaBright', `Executing command: ${command}`);

        if (dryRun) {
            log('yellow', `[Dry Run] Would execute command: ${command}`);
            return resolve();
        }

        const parsedCommand = shellQuote.parse(command);
        const [cmd, ...args] = parsedCommand;
        const childProcess = spawn(cmd, args);

        let output = '';

        childProcess.stdout.on('data', (data) => {
            const message = data.toString();
            output += message;
            log('magentaBright', `[${context}] => ${message.trim()}`);
        });

        childProcess.stderr.on('data', (data) => {
            const message = data.toString();
            log('cyanBright', `[${context}] => ${message.trim()}`);
        });

        childProcess.on('close', (code) => {
            if (code === 0) {
                log('green', `Command completed successfully: ${command}`);
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
async function applyBuild(context, buildInfo) {
    if (options.applyBuild !== true) {
        log('yellow', `Not automatically applying build`);
        return;
    }

    if (!dryRun) {
        const buildVersion = buildInfo.build_version;
        const command = `ddn supergraph build apply ${buildVersion} -c ${context}`;

        log('magentaBright', `Applying build version: ${buildVersion}`);
        runCommandWithOutput(command, context);
        log('green', `Build version ${buildVersion} applied successfully.`);
    } else {
        log('yellow', `[Dry Run] Would apply build`);
    }
}

// Deploy supergraph
async function runCommandWithTag(
    context,
    srcFile,
    tag,
    supergraph,
    rebuildConnectors = true
) {
    const DEST_DIR = join(root, '/globals');
    const DEST_FILE = 'auth-config.hml';

    if (!fs.existsSync(srcFile)) {
        throw new Error(`Error: Source file ${srcFile} does not exist.`);
    }

    // Copy the auth file to the correct location
    if (!dryRun) {
        fs.copyFileSync(srcFile, join(DEST_DIR, DEST_FILE));
        log('green', `Copied ${srcFile} to ${DEST_DIR}/${DEST_FILE}`);
    } else {
        log('yellow', `[Dry Run] Would copy ${srcFile} to ${DEST_DIR}/${DEST_FILE}`);
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
    let command = `ddn supergraph build create -d "${gitLogDescription}" -c "${context}" --out json --log-level "${logLevel}" --supergraph "${supergraph}"`;
    if (!rebuildConnectors) {
        command += ' --no-build-connectors';
    }

    if (!dryRun) {
        log('magentaBright', `[${context}] => Executing command: ${command}`);
        const output = await runCommandWithOutput(command, context);
        const buildInfo = JSON.parse(output);

        if (options.quiet) {
            // I'm not super happy with this as a way to allow CI/CD to work
            // The github action looks for output that it redirects to a file
            // From here it gets the build IDs, console IDs etc.
            // Ideally we should log specific output to an untracked log file
            // and handle that in this deploy script or something but that's
            // a TODO for the future
            // Can't wait for it to bite me in the butt
            console.log(output);
        }

        log('green', `[${context}] => Deployment completed successfully for ${tag}`);
        log('green', `Build URL: ${buildInfo.build_url}`);
        log('green', `Console URL: ${buildInfo.console_url}`);

        return buildInfo;

    } else {
        log('yellow', `[Dry Run] Would execute command: ${command}`);
    }
}

// Pushes incremental release of metadata
async function pushMetadataRelease(supergraph, context, rebuildConnectors) {
    log('magentaBright', `[${context}] => Starting an incremental release of metadata.`);

    let buildInfo = {};
    // Deploy with JWT file to demo authz
    buildInfo = await runCommandWithTag(
        context,
        jwtFile,
        'JWT',
        supergraph,
        rebuildConnectors
    );

    // Deploy with NoAuth file to allow instant access
    buildInfo = await runCommandWithTag(
        context,
        noauthFile,
        'NoAuth',
        supergraph,
        rebuildConnectors
    );

    log('green', `[${context}] => Incremental release completed successfully.`);
    return buildInfo;
}

// Rebuild function that does not use --no-build-connectors
async function rebuildSupergraph(supergraphs, context, rebuildConnectors) {
    log('magentaBright', `[${context}] => Starting a complete rebuild of all supergraphs.`);

    let index = 1;

    for (const supergraph of supergraphs) {
        await runCommandWithTag(
            context,
            noauthFile,
            `NoAuth S-${index}`,
            supergraph,
            rebuildConnectors
        );
        index++;
    }

    log('green', `[${context}] => Rebuild completed successfully.`);
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
            throw new Error(`Error: You must be on the 'main' branch to deploy.`);
        }

        // Check for uncommitted changes
        const status = await git.status();
        if (status.files.length > 0) {
            throw new Error(`Error: Uncommitted changes detected. Please commit or stash changes before running this script.`);
        }
    } else {
        log('yellow', 'Override flag enabled: Skipping branch and uncommitted changes checks.');
    }

    let context = options.context || null;
    let rebuildConnectors = options.rebuildConnectors || null;
    let fullMetadataBuild = options.fullMetadataBuild || null;

    if (!noInteraction && context === null) {
        let doc = yaml.parse(fs.readFileSync('.hasura/context.yaml', 'utf8'));
        if (!doc.definition || !doc.definition.contexts) {
            throw new Error(`Error: .hasura/context.yaml has no contexts.`);
        }
        context = (
            await inquirer.prompt([
                {
                    type: 'list',
                    name: 'context',
                    message: 'Select a context to set:',
                    choices: Object.keys(doc.definition.contexts),
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

    // switch connectors to the right region
    convertConnectorRegion(gcpRegion);

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

    let buildInfo = {};
    buildInfo = await pushMetadataRelease(fullyBuiltSupergraph, context, rebuildConnectors);

    // Apply the build using the extracted build_version
    applyBuild(context, buildInfo);

    // Revert connectors to the default
    convertConnectorRegion('gcp-us-west2');

    log('green',`[${context}] => Deployment completed successfully.`);
}

async function log(colour, message) {
    if (options.quiet) {
        return;
    }
    if (chalk[colour]) {
        console.log(chalk[colour](message));
    } else {
        console.log(chalk.white(`Invalid colour '${colour}'. ${message}`));
    }
}

main().catch((error) => {
    console.error(
        chalk.whiteBright.bgRed(`Unexpected error: ${error.message}`)
    );
    process.exit(1);
});
