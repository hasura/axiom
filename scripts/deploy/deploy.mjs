#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import yaml from 'yaml';
import chalk from 'chalk';
import inquirer from 'inquirer';
import simpleGit from 'simple-git';
import { execSync } from 'child_process';
import { Command } from 'commander';

const git = simpleGit();

// Initialize commander
const program = new Command();

program
    .option('-l, --log-level <level>', 'Set the log level (FATAL, ERROR, WARN, INFO, DEBUG)', 'FATAL')
    .option('-o, --override', 'Override branch and uncommitted changes checks', false)
    .parse(process.argv);

const options = program.opts();
const logLevel = options.logLevel.toUpperCase();
const override = options.override;

// Validate log level
const allowedLogLevels = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'];
if (!allowedLogLevels.includes(logLevel)) {
    console.error(chalk.red(`Invalid log level: ${logLevel}. Allowed values are: ${allowedLogLevels.join(', ')}`));
    process.exit(1);
}

console.log(chalk.blue(`Log level set to: ${logLevel}`));
console.log(chalk.blue(`Override flag is ${override ? 'enabled' : 'disabled'}`));

// Get the current directory of the script
const __filename = path.basename(import.meta.url);
const __dirname = path.dirname(__filename);

// Mapping context regions to GCP region IDs
const regionMapping = {
    "au": "gcp-australia-southeast1",
    "eu": "gcp-europe-west1",
    "sg": "gcp-asia-southeast1",
    "us-east": "gcp-us-east4",
    "us-west": "gcp-us-west2",
    "default": "gcp-us-west2" // Default axiom-test to us-west
};

// Define root so we can reference files in the same manner
const root = path.resolve(__dirname, '../../');

if (!fs.existsSync(root)) {
    console.error(chalk.red(`Error: Directory ${root} does not exist.`));
    process.exit(1);
}

// Update the region in connector files
function updateRegionInFile(filePath, region) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        let doc = yaml.parse(content);

        if (doc.definition && Array.isArray(doc.definition.regionConfiguration)) {
            doc.definition.regionConfiguration.forEach((regionConfig) => {
                regionConfig.region = region;
            });

            const newYaml = yaml.stringify(doc);
            fs.writeFileSync(filePath, newYaml, 'utf8');
            console.log(chalk.green(`Successfully updated region in ${filePath}`));
        } else {
            console.warn(chalk.yellow(`Warning: No valid region configuration found in ${filePath}.`));
        }
    } catch (error) {
        console.error(chalk.red(`Failed to update region in ${filePath}: ${error.message}`));
    }
}

// Find all `connector.yaml` files in the supergraph
function findConnectorYamlFiles(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach((file) => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat && stat.isDirectory()) {
            results = results.concat(findConnectorYamlFiles(filePath));
        } else if (file === 'connector.yaml') {
            results.push(filePath);
        }
    });
    return results;
}

// Deploy supergraph
function runCommandWithTag(region, srcFile, tag, supergraph, noBuildConnectors = true) {
    const DEST_DIR = path.join(__dirname, '../../globals');
    const DEST_FILE = 'auth-config.hml';

    if (!fs.existsSync(srcFile)) {
        console.error(chalk.red(`Error: Source file ${srcFile} does not exist.`));
        process.exit(1);
    }

    // Copy the auth file to the correct location
    fs.copyFileSync(srcFile, path.join(DEST_DIR, DEST_FILE));
    console.log(chalk.green(`Copied ${srcFile} to ${DEST_DIR}/${DEST_FILE}`));

    // Get git log description for the command to use as the supergrah build description
    const gitLogDescription = execSync(`git log -1 --pretty=format:"%h [${tag}] %s"`).toString().trim();

    // Construct the ddn supergraph build command
    let command = `ddn supergraph build create -d "${gitLogDescription}" -c "${region}" --out json --log-level "${logLevel}" --supergraph "${supergraph}"`;
    if (noBuildConnectors) {
        command += ' --no-build-connectors';
    }

    console.log(chalk.blue(`Executing command: ${command}`));
    execSync(command, { stdio: 'inherit' });
    console.log(chalk.green(`Successfully executed deployment for ${tag}`));
}

// Rebuild function that does not use --no-build-connectors
async function rebuildSupergraph(contextRegion) {
    console.log(chalk.blue('Starting a complete rebuild of all supergraphs and connectors.'));

    const NOAUTH_FILE = path.join(__dirname, 'noauth.hml');
    let index = 1;

    const supergraphs = [
        `${root}/supergraph-project-queries.yaml`,
        `${root}/supergraph-project.yaml`,
        `${root}/supergraph-domain.yaml`,
        `${root}/supergraph.yaml`
    ];

    for (const supergraph of supergraphs) {
        runCommandWithTag(contextRegion, NOAUTH_FILE, `NoAuth RB-${index}`, supergraph, false);
        index++;
    }

    console.log(chalk.green('Rebuild completed successfully.'));
}

async function main() {
    if (!override) {
        // Check if on the main branch
        const currentBranch = await git.revparse(['--abbrev-ref', 'HEAD']);
        if (currentBranch !== 'main') {
            console.error(chalk.red(`Error: You must be on the 'main' branch to deploy.`));
            process.exit(1);
        }

        // Check for uncommitted changes
        const status = await git.status();
        if (status.files.length > 0) {
            console.error(chalk.red('Error: Uncommitted changes detected. Please commit or stash changes before running this script.'));
            process.exit(1);
        }
    } else {
        console.log(chalk.yellow('Override flag enabled: Skipping branch and uncommitted changes checks.'));
    }

    const { contextRegion, rebuild } = await inquirer.prompt([
        {
            type: 'list',
            name: 'contextRegion',
            message: 'Select a context region to set:',
            choices: Object.keys(regionMapping)
        },
        {
            type: 'confirm',
            name: 'rebuild',
            message: 'Do you want to perform a complete rebuild?',
            default: false
        }
    ]);

    // Map the selected context region to the GCP region ID
    const connectorRegion = regionMapping[contextRegion];

    // Update all `connector.yaml` files with the selected region
    const yamlFiles = findConnectorYamlFiles(root);
    yamlFiles.forEach(file => updateRegionInFile(file, connectorRegion));
    console.log(chalk.blue(`All 'connector.yaml' files have been updated to use the region ${connectorRegion}.`));

    const SCRIPT_DIR = __dirname;
    const JWT_FILE = path.join(SCRIPT_DIR, 'jwtauth.hml');
    const NOAUTH_FILE = path.join(SCRIPT_DIR, 'noauth.hml');

    if (rebuild) {
        await rebuildSupergraph(contextRegion);
    }

    runCommandWithTag(contextRegion, JWT_FILE, 'JWT', `${root}/supergraph.yaml`, true);  // Deploy with JWT file
    runCommandWithTag(contextRegion, NOAUTH_FILE, 'NoAuth', `${root}/supergraph.yaml`, true);  // Deploy with NoAuth file

    console.log(chalk.green('Deployment process completed successfully.'));
}

main().catch(error => {
    console.error(chalk.red(`Unexpected error: ${error.message}`));
    process.exit(1);
});
