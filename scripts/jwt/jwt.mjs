import jwt from 'jsonwebtoken';
import { program } from 'commander';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

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
  .parse(process.argv);

// Extract values from command line options or use default values
const options = program.opts();
const roles = options.roles ? options.roles.split(',') : ['customer'];
const userId = options.userId ? options.userId : '7';

// Determine which .env file to load
const envFilePath = options.env
  ? path.resolve(process.cwd(), options.env)
  : path.resolve(__dirname, '../../.env');

loadEnvFile(envFilePath);

// Get the key from command line option, environment variable, or use a default value
const key = options.key || process.env.JWT_SECRET || 'default-secret-key';

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