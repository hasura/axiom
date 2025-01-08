// This script reads from the package.json file in the current working directory
// and prints out the text in the "scripts.<name>" entry. This is used to bypass
// npm, which does not handle signals correctly, and execute the command directly

const fs = require("node:fs");
const process = require("node:process");
const path = require("node:path");

const cwd = process.cwd();
const packageJsonPath = path.join(cwd, "./package.json");

if (process.argv.length < 3) {
  console.error("Error: Pass the name of script command you want to read as the first command line arg.");
  console.error("Usage: node read-package-script.js <name>");
  process.exit(1);
}
const desiredScript = process.argv[2];

try {
  const packageJsonText = fs.readFileSync(packageJsonPath);
  const packageJson = JSON.parse(packageJsonText);
  const script = packageJson.scripts[desiredScript];
  if (script === undefined) {
    console.error(`Error: script ${desiredScript} not found in ${packageJsonPath}`)
  }
  console.log(script);
} catch (e) {
  console.error(`Error reading ${packageJsonPath}: ${e}`);
}
