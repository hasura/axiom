#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import yaml from 'yaml';
import chalk from 'chalk';
import inquirer from 'inquirer';

// Get the current directory of the script
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// List of available regions
const availableRegions = [
    "gcp-asia-south1",
    "gcp-asia-southeast1",
    "gcp-australia-southeast1",
    "gcp-europe-west1",
    "gcp-southamerica-east1",
    "gcp-us-east4",
    "gcp-us-west2"
];

// Hardcoded directory path
const directory = path.resolve(__dirname, '../../');

// Check if the directory exists
if (!fs.existsSync(directory)) {
    console.error(chalk.red(`Error: Directory ${directory} does not exist.`));
    process.exit(1);
}

// Function to update the region in a YAML file
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

// Recursively find `connector.yaml` files in the directory
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

// Interactive region selection
inquirer.prompt([
    {
        type: 'list',
        name: 'region',
        message: 'Select a region to set:',
        choices: availableRegions
    }
]).then(answers => {
    const region = answers.region;
    const yamlFiles = findConnectorYamlFiles(directory);
    yamlFiles.forEach(file => updateRegionInFile(file, region));

    console.log(chalk.blue('All `connector.yaml` files have been processed.'));
}).catch(error => {
    console.error(chalk.red(`Error: ${error.message}`));
    process.exit(1);
});
