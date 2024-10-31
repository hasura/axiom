'use strict';

const readline = require('readline');

// Function to securely encode the password
function encodePassword(password) {
  if (typeof password !== 'string' || password.trim() === '') {
    throw new Error("Password cannot be empty or non-string.");
  }
  return encodeURIComponent(password);
}

// Secure prompt function for password entry
function promptForPassword() {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: true,
    });

    rl.question('Enter password: ', (input) => {
      rl.close();
      resolve(input);
    });

    // Mask the password input
    rl.stdoutMuted = true;
    rl._writeToOutput = function _writeToOutput() {
      rl.output.write('*');
    };
  });
}

// Main function to prompt and encode password
async function main() {
  try {
    const userPassword = await promptForPassword();
    const encodedPassword = encodePassword(userPassword);
    console.log(`\nEncoded password: ${encodedPassword}`);
  } catch (error) {
    console.error("An error occurred:", error.message);
    process.exit(1);
  }
}

// Execute main function
main();

