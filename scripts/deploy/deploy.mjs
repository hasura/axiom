#!/usr/bin/env node

import fs from 'fs';
import { dirname, resolve, join } from 'path';
import yaml from 'yaml';
import chalk from 'chalk';
import inquirer from 'inquirer';
import simpleGit from 'simple-git';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import shellQuote from 'shell-quote';
import { Command } from 'commander';

const CONFIG = {
    logLevels: ['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG']
};

class DeploymentManager {
    constructor() {
        this.git = simpleGit();
        this.program = new Command()
            .option('-l, --log-level <level>', 'Set log level', 'FATAL')
            .option('-o, --override', 'Override checks', false)
            .option('-d, --dry-run', 'Simulate deployment', false)
            .option('-n, --no-interaction', 'Non-interactive mode', true)
            .option('-c, --context <context>', 'Deploy context', null)
            .option('-p, --profile <profile>', 'Config profile', null)
            .option('-r, --rebuild-connectors', 'Rebuild connectors', false)
            .option('-f, --full-metadata-build', 'Full metadata rebuild', false)
            .option('-x, --override-description <desc>', 'Override description')
            .option('-q, --quiet', 'Quiet mode')
            .option('-a, --apply-build', 'Auto-apply build', false)
            .option('-j, --json-output <file>', 'Output build info to JSON file')
            .parse(process.argv);

        const __dirname = dirname(fileURLToPath(import.meta.url));
        this.paths = {
            root: resolve(__dirname, '../../hasura/'),
        };
        this.options = this.program.opts();
        // This line is counter-intuitive but required.
        this.options.noInteraction = !this.options.interaction;
    }

    log(level, msg) {
        if (!this.options.quiet) {
            console.log(chalk[level] ? chalk[level](msg) : chalk.white(msg));
        }
    }

    async execCommand(command, context) {
        this.log('magentaBright', `Executing: ${command}`);
        if (this.options.dryRun) {
            this.log('yellow', `[Dry Run] Would execute: ${command}`);
            return '';
        }

        return new Promise((resolve, reject) => {
            const [cmd, ...args] = shellQuote.parse(command);
            const proc = spawn(cmd, args);
            let output = '';

            proc.stdout.on('data', data => {
                output += data;
                this.log('magentaBright', `[${context}] => ${data.toString().trim()}`);
            });

            proc.stderr.on('data', data => {
                this.log('cyanBright', `[${context}] => ${data.toString().trim()}`);
            });

            proc.on('close', code => {
                code === 0 ? resolve(output) : reject(new Error(`Failed with code ${code}`));
            });
        });
    }

    async deploy(context, tag, supergraph, rebuild) {

        const desc = this.options.overrideDescription ||
            (await this.git.raw(['log', '-1', '--pretty=format:"%h [' + tag + '] %s"'])).trim();

        const cmd = `ddn supergraph build create -d ${desc} -c ${context} --out json --log-level ${this.options.logLevel} --supergraph ${supergraph}${rebuild ? '' : ' --no-build-connectors'}`;

        if (!this.options.dryRun) {
            const output = await this.execCommand(cmd, context);
            const buildInfo = JSON.parse(output);
            this.options.quiet && console.log(output);
            if (this.options.jsonOutput) {
                try {
                    fs.writeFileSync(this.options.jsonOutput, output);
                } catch (err) {
                    console.error(`Failed to write to JSON output file: ${err.message}`);
                }
            }
            return buildInfo;
        }
    }

    async getDeploymentParams() {
        const profiles = fs.readdirSync(join(this.paths.root, 'supergraph-config'))
            .filter(f => fs.statSync(join(this.paths.root, 'supergraph-config', f)).isDirectory())
            .map(name => ({ name, path: join(this.paths.root, 'supergraph-config', name) }));

        const contextYaml = yaml.parse(fs.readFileSync('.hasura/context.yaml', 'utf8'));

        let profile;
        if (this.options.profile) {
            profile = profiles.find(p => p.name === this.options.profile);
        } else if (!this.options.noInteraction) {
            const answer = await inquirer.prompt([{
                type: 'list',
                name: 'profile',
                message: 'Select profile:',
                choices: profiles.map(p => p.name)
            }]);
            profile = profiles.find(p => p.name === answer.profile);
        }

        const params = {
            profile,
            context: this.options.context || (this.options.noInteraction ? null :
                (await inquirer.prompt([{
                    type: 'list', name: 'context', message: 'Select context:',
                    choices: Object.keys(contextYaml.definition.contexts)
                }])).context),

                fullMetadataBuild: this.options.fullMetadataBuild ||
                (!this.options.noInteraction &&
                    (await inquirer.prompt([{
                        type: 'confirm',
                        name: 'fullMetadataBuild',
                        message: 'Perform full metadata rebuild?',
                        default: false
                    }])).fullMetadataBuild) || false,

                rebuildConnectors: this.options.rebuildConnectors ||
                (!this.options.noInteraction &&
                    (await inquirer.prompt([{
                        type: 'confirm',
                        name: 'rebuildConnectors',
                        message: 'Rebuild all connectors?',
                        default: false
                    }])).rebuildConnectors) || false
        };

        this.log(
            'magenta',
            `Deploying: ${params.profile.name} to ${params.context}` +
            `${params.rebuildConnectors ? ' [Connector rebuild]' : ''}` +
            `${params.fullMetadataBuild ? ' [Full metadata build]' : ''}`
        );
        if (!params.profile || !params.context) {
            throw new Error('Missing required parameters in non-interactive mode');
        }

        return { ...params, contextYaml };
    }

    async main() {
        try {
            if (!fs.existsSync(this.paths.root)) throw new Error(`Missing directory: ${this.paths.root}`);
            process.chdir(this.paths.root);
            if (!fs.existsSync('.hasura/context.yaml')) throw new Error('Missing context.yaml');
            if (!CONFIG.logLevels.includes(this.options.logLevel.toUpperCase())) {
                throw new Error(`Invalid log level: ${this.options.logLevel}`);
            }

            if (!this.options.override) {
                const branch = await this.git.revparse(['--abbrev-ref', 'HEAD']);
                if (branch !== 'main') throw new Error('Must be on main branch');

                const status = await this.git.status();
                if (status.files.length > 0) throw new Error('Uncommitted changes detected');
            }

            const { profile, context, fullMetadataBuild, rebuildConnectors, contextYaml } =
                await this.getDeploymentParams();

            const supergraphs = fs.readdirSync(profile.path)
                .filter(f => f.endsWith('.yaml'))
                .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }))
                .map(f => join(profile.path, f));

            if (supergraphs.length === 0) throw new Error('No supergraphs found');

            let buildInfo = {};

            if (fullMetadataBuild && supergraphs.length > 2) {
                for (let i = 0; i < supergraphs.length - 2; i++) {
                    await this.deploy(context, `NoAuth S-${i + 1}`,
                        supergraphs[i], rebuildConnectors);
                }
            }

            if (supergraphs.length >= 2) {
                buildInfo = await this.deploy(context, 'JWT',
                    supergraphs[supergraphs.length - 2], rebuildConnectors);
            }
            buildInfo = await this.deploy(context, 'NoAuth',
                supergraphs[supergraphs.length - 1], rebuildConnectors);


            if (this.options.applyBuild && !this.options.dryRun && buildInfo.build_version) {
                await this.execCommand(
                    `ddn supergraph build apply ${buildInfo.build_version} -c ${context}`,
                    context
                );
            }

            this.log('inverse', 'Deployment completed successfully');
        } catch (error) {
            console.error(chalk.whiteBright.bgRed(`Error: ${error.message}`));
            process.exit(1);
        }
    }
}

new DeploymentManager().main();