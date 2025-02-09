#!/usr/bin/env node

import jwt from 'jsonwebtoken';
import { program } from 'commander';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import yaml from 'js-yaml';

// Polyfill for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Function to load environment variables from a .env file
function loadEnvFile(envFilePath) {
  if (fs.existsSync(envFilePath)) {
    dotenv.config({ path: envFilePath });
  } else {
    console.error(`Env file not found: ${envFilePath}`);
    process.exit(1);
  }
}

// Parse command line options
program
  .option('-r, --roles <roles>', 'Comma-separated list of roles')
  .option('-u, --userId <userId>', 'User ID')
  .option('-k, --key <key>', 'JWT key')
  .option('-e, --env <env>', 'Path to .env file')
  .option('-c, --context <context>', 'Context from .hasura/context.yaml')
  .parse(process.argv);

// Extract values from command line options or use default values
const options = program.opts();
const roles = options.roles ? options.roles.split(',') : ['customer'];
const userId = options.userId ? options.userId : '7';
const context = options.context || 'axiom-dev';

const contextDir = path.resolve(__dirname, '../../hasura/.hasura');
const contextData = yaml.load(fs.readFileSync(`${contextDir}/context.yaml`, 'utf8'));

if (!contextData.definition.contexts[context]) {
  console.error(`Error: Context '${context}' does not exist in ${contextDir}/context.yaml.`);
  process.exit(1);
}
if (!contextData.definition.contexts[context].localEnvFile) {
  console.error(`Error: localEnvFile key not found in context '${context}' in ${contextDir}/context.yaml.`);
  process.exit(1);
}
const contextEnv = path.resolve(__dirname, contextDir, contextData.definition.contexts[context].localEnvFile);

// Determine which .env file to load
const envFilePath = options.env
  ? path.resolve(process.cwd(), options.env)
  : path.resolve(contextEnv);

loadEnvFile(envFilePath);

// Get the key from command line option, environment variable, or use a default value
const key = options.key || process.env.JWT_SECRET;

if (!key) {
  console.error('Error: No JWT secret provided. Please pass a key with the --key option, --env with the path to an env file or set the JWT_SECRET environment variable.');
  process.exit(1);
}

const claims = {
  "x-hasura-allowed-roles": roles,
  "x-hasura-default-role": roles[0],
  "x-hasura-role": roles[0],
  "x-hasura-user-id": userId
};

// Generate a new JWT token with the private key
const token = jwt.sign(
  { "iss": "holotel-next-auth", 'claims.jwt.hasura.io': claims },
  key,
  { algorithm: 'HS256', expiresIn: '1y' }
);

console.log(`Token: ${token}`);
const decoded = jwt.verify(token, key);
console.log(decoded);
