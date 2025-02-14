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

// Constants
const AVAILABLE_REGIONS = [
    'gcp-australia-southeast1',
    'gcp-europe-west1',
    'gcp-asia-southeast1',
    'gcp-us-east4',
    'gcp-us-west2',
];

const LOG_LEVELS = ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'];
const DEFAULT_REGION = 'gcp-us-west2';

class DeploymentManager {
    constructor() {
        this.git = simpleGit();
        this.program = this.setupCommander();
        this.options = this.program.opts();
        this.setupPaths();
    }

    setupCommander() {
        const program = new Command();
        program
            .option('-l, --log-level <level>', 'Set the log level', 'FATAL')
            .option('-o, --override', 'Override branch and uncommitted changes checks', false)
            .option('-d, --dry-run', 'Simulate the deployment without executing commands', false)
            .option('-n, --no-interaction', 'Deploy without interactive questions', true)
            .option('-g, --gcp-region <gcpRegion>', 'Deploy connectors to a specific GCP region', DEFAULT_REGION)
            .option('-c, --context <context>', 'Deploy specific context from .hasura/context.yaml', null)
            .requiredOption('-p, --profile <profile>', 'Deploy from demo config in supergraph-config/<profile>')
            .option('-r, --rebuild-connectors', 'Rebuild all connectors', false)
            .option('-f, --full-metadata-build', 'Perform a full rebuild of metadata', false)
            .option('-x, --override-description <description>', 'Override the deployment description')
            .option('-q, --quiet', 'Silence all logging except for errors.')
            .option('-a, --apply-build', 'Automatically apply the build once deployed', false)
            .parse(process.argv);
        
        return program;
    }

    setupPaths() {
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = dirname(__filename);
        this.scriptDir = __dirname;
        this.jwtFile = join(this.scriptDir, 'jwtauth.hml');
        this.noauthFile = join(this.scriptDir, 'noauth.hml');
        this.root = resolve(__dirname, '../../hasura/');
        this.supergraphConfig = resolve(this.root, 'supergraph-config', this.options.profile);
    }

    log(colour, message) {
        if (this.options.quiet) return;
        if (chalk[colour]) {
            console.log(chalk[colour](message));
        } else {
            console.log(chalk.white(`Invalid colour '${colour}'. ${message}`));
        }
    }

    validateSetup() {
        if (!fs.existsSync(this.root)) {
            throw new Error(`Directory ${this.root} does not exist.`);
        }

        process.chdir(this.root);
        
        if (!fs.existsSync('.hasura/context.yaml')) {
            throw new Error('Error: .hasura/context.yaml not found.');
        }

        if (!AVAILABLE_REGIONS.includes(this.options.gcpRegion)) {
            throw new Error(`GCP Region ${this.options.gcpRegion} not supported. Available: ${AVAILABLE_REGIONS.join(', ')}`);
        }

        if (!fs.existsSync(this.supergraphConfig)) {
            throw new Error(`Invalid profile: ${this.options.profile}. Directory doesn't exist.`);
        }

        if (!LOG_LEVELS.includes(this.options.logLevel.toUpperCase())) {
            throw new Error(`Invalid log level: ${this.options.logLevel}. Allowed: ${LOG_LEVELS.join(', ')}`);
        }
    }

    async runCommand(command, context = '') {
        this.log('magentaBright', `Executing command: ${command}`);

        if (this.options.dryRun) {
            this.log('yellow', `[Dry Run] Would execute: ${command}`);
            return '';
        }

        return new Promise((resolve, reject) => {
            const [cmd, ...args] = shellQuote.parse(command);
            const childProcess = spawn(cmd, args);
            let output = '';

            childProcess.stdout.on('data', (data) => {
                const message = data.toString();
                output += message;
                this.log('magentaBright', `[${context}] => ${message.trim()}`);
            });

            childProcess.stderr.on('data', (data) => {
                this.log('cyanBright', `[${context}] => ${data.toString().trim()}`);
            });

            childProcess.on('close', (code) => {
                if (code === 0) {
                    this.log('green', `Command completed: ${command}`);
                    resolve(output);
                } else {
                    reject(new Error(`Command failed with code ${code}`));
                }
            });
        });
    }

    async handleConnectorRegions(region) {
        const yamlFiles = this.findConnectorYamlFiles(this.root);
        for (const file of yamlFiles) {
            await this.updateRegionInFile(file, region);
        }
    }

    findConnectorYamlFiles(dir) {
        const results = [];
        const list = fs.readdirSync(dir);
        
        for (const file of list) {
            const filePath = join(dir, file);
            const stat = fs.statSync(filePath);
            
            if (stat.isDirectory()) {
                results.push(...this.findConnectorYamlFiles(filePath));
            } else if (file === 'connector.yaml') {
                results.push(filePath);
            }
        }
        
        return results;
    }

    async updateRegionInFile(filePath, region) {
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const doc = yaml.parse(content);

            if (!doc.definition?.regionConfiguration) {
                this.log('yellow', `Warning: No region configuration in ${filePath}`);
                return;
            }

            doc.definition.regionConfiguration.forEach(config => {
                config.region = region;
            });

            if (!this.options.dryRun) {
                fs.writeFileSync(filePath, yaml.stringify(doc), 'utf8');
                this.log('green', `Updated region to ${region} in ${filePath}`);
            }
        } catch (error) {
            throw new Error(`Failed to update region in ${filePath}: ${error.message}`);
        }
    }

    async deploySupergraph(context, srcFile, tag, supergraph, rebuildConnectors) {
        const destDir = join(this.root, '/globals');
        const destFile = 'auth-config.hml';

        if (!fs.existsSync(srcFile)) {
            throw new Error(`Source file ${srcFile} does not exist.`);
        }

        if (!this.options.dryRun) {
            fs.copyFileSync(srcFile, join(destDir, destFile));
        }

        const description = this.options.overrideDescription || 
            execSync(`git log -1 --pretty=format:"%h [${tag}] %s"`).toString().trim();

        let command = `ddn supergraph build create -d "${description}" -c "${context}" --out json --log-level "${this.options.logLevel}" --supergraph "${supergraph}"`;
        
        if (!rebuildConnectors) {
            command += ' --no-build-connectors';
        }

        if (!this.options.dryRun) {
            const output = await this.runCommand(command, context);
            const buildInfo = JSON.parse(output);

            if (this.options.quiet) {
                console.log(output);
            }

            return buildInfo;
        }
    }

    async performDeployment() {
        const contextYaml = yaml.parse(fs.readFileSync('.hasura/context.yaml', 'utf8'));
        const context = await this.getContext(contextYaml);
        const fullMetadataBuild = await this.getFullMetadataBuild();
        const rebuildConnectors = await this.getRebuildConnectors();

        await this.handleConnectorRegions(this.options.gcpRegion);

        const supergraphs = this.getSupergraphs();
        if (supergraphs.length === 0) {
            throw new Error("No supergraphs found!");
        }

        const intermediarySupergraphs = supergraphs.slice(0, -1);
        const finalSupergraph = supergraphs[supergraphs.length - 1];

        if (fullMetadataBuild && intermediarySupergraphs.length > 0) {
            await this.rebuildSupergraph(intermediarySupergraphs, context, rebuildConnectors);
        }

        const fullContext = { ...contextYaml.definition.contexts[context], context };
        const buildInfo = await this.deployFinalSupergraph(finalSupergraph, fullContext, rebuildConnectors);

        if (this.options.applyBuild) {
            await this.applyBuild(context, buildInfo);
        }

        await this.handleConnectorRegions(DEFAULT_REGION);
    }

    async getContext(contextYaml) {
        if (this.options.context) return this.options.context;
        
        if (this.options.noInteraction) {
            throw new Error('Context required in non-interactive mode');
        }

        if (!contextYaml.definition?.contexts) {
            throw new Error('No contexts defined in .hasura/context.yaml');
        }

        const response = await inquirer.prompt([{
            type: 'list',
            name: 'context',
            message: 'Select a context:',
            choices: Object.keys(contextYaml.definition.contexts)
        }]);

        return response.context;
    }

    async getFullMetadataBuild() {
        if (this.options.fullMetadataBuild !== null) return this.options.fullMetadataBuild;
        
        if (this.options.noInteraction) return false;

        const response = await inquirer.prompt([{
            type: 'confirm',
            name: 'fullMetadataBuild',
            message: 'Perform a full metadata rebuild? (warning: slow)',
            default: false
        }]);

        return response.fullMetadataBuild;
    }

    async getRebuildConnectors() {
        if (this.options.rebuildConnectors !== null) return this.options.rebuildConnectors;
        
        if (this.options.noInteraction) return false;

        const response = await inquirer.prompt([{
            type: 'confirm',
            name: 'rebuildConnectors',
            message: 'Perform a full connector rebuild? (warning: very slow)',
            default: false
        }]);

        return response.rebuildConnectors;
    }

    getSupergraphs() {
        return fs.readdirSync(this.supergraphConfig)
            .filter(file => file.endsWith('.yaml'))
            .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
            .map(file => join(this.supergraphConfig, file));
    }

    async deployFinalSupergraph(supergraph, fullContext, rebuildConnectors) {
        this.log('magentaBright', `[${fullContext.context}] => Starting an incremental release of metadata.`);
        
        if (this.options.dryRun) {
            return {};
        }

        let buildInfo = {};
        
        // Only deploy JWT build if there's a JWT in the cloud env file
        if (fullContext.cloudEnvFile && 
            fs.readFileSync(`.hasura/${fullContext.cloudEnvFile}`, 'utf8').includes('JWT_SECRET=')) {
            buildInfo = await this.deploySupergraph(
                fullContext.context,
                this.jwtFile,
                'JWT',
                supergraph,
                rebuildConnectors
            );
        }

        // Deploy with NoAuth file to allow instant access
        buildInfo = await this.deploySupergraph(
            fullContext.context,
            this.noauthFile,
            'NoAuth',
            supergraph,
            rebuildConnectors
        );

        this.log('green', `[${fullContext.context}] => Incremental release completed successfully.`);
        return buildInfo;
    }

    async rebuildSupergraph(supergraphs, context, rebuildConnectors) {
        this.log('magentaBright', `[${context}] => Starting a complete rebuild of all supergraphs.`);

        for (let i = 0; i < supergraphs.length; i++) {
            await this.deploySupergraph(
                context,
                this.noauthFile,
                `NoAuth S-${i + 1}`,
                supergraphs[i],
                rebuildConnectors
            );
        }

        this.log('green', `[${context}] => Rebuild completed successfully.`);
    }

    async applyBuild(context, buildInfo) {
        if (!this.options.applyBuild) {
            this.log('yellow', 'Not automatically applying build');
            return;
        }

        if (!this.options.dryRun) {
            const buildVersion = buildInfo.build_version;
            const command = `ddn supergraph build apply ${buildVersion} -c ${context}`;

            this.log('magentaBright', `Applying build version: ${buildVersion}`);
            await this.runCommand(command, context);
            this.log('green', `Build version ${buildVersion} applied successfully.`);
        } else {
            this.log('yellow', '[Dry Run] Would apply build');
        }
    }

    async main() {
        try {
            this.validateSetup();
            
            if (!this.options.override) {
                const currentBranch = await this.git.revparse(['--abbrev-ref', 'HEAD']);
                if (currentBranch !== 'main') {
                    throw new Error('Must be on main branch to deploy.');
                }

                const status = await this.git.status();
                if (status.files.length > 0) {
                    throw new Error('Uncommitted changes detected.');
                }
            }

            await this.performDeployment();
            
            this.log('green', 'Deployment completed successfully.');
        } catch (error) {
            console.error(chalk.whiteBright.bgRed(`Error: ${error.message}`));
            process.exit(1);
        }
    }
}

// Run the deployment
new DeploymentManager().main();