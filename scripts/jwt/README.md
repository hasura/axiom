# JWT Generator

A command-line tool to generate JWT tokens with Hasura-specific claims.

## Installation

Ensure you have Node.js installed, then install dependencies:

```
npm install
```

## Usage

Generate a JWT token by running:

```
node jwt.mjs
```

### Usage as `ddn run` command

From the base hasura folder, call `ddn run jwt-gen` for a default token for user `7` as role `customer`. Pass `-u` to change user and `-r` to change role. Example:

```
ddn run jwt-gen -- -u 8 -r editor
```

### Options

- `-u, --userId <userId>`: User ID (default: `7`).
- `-r, --roles <roles>`: Comma-separated list of roles (default: `customer`).
- `-k, --key <key>`: JWT secret key (can be set via `.env` file).
- `-e, --env <path>`: Path to `.env` file containing `JWT_SECRET`.
- `-c, --context <context>`: Context to auto-find `.env` file defined in `.hasura/context.yaml`.

## Example

Using an alternate context from `.hasura/context.yaml`

```
node jwt.mjs -u 8 -r admin,editor -c axiom-test
```

Using a custom `.env` file:

```
node jwt.mjs -u 123 -r admin,editor -e ../../.env
```

Passing a key to the script

```
node jwt.mjs -u 123 -r admin,editor -k "qG7zP4cZK9B5vN5fjYcLr1Jq3RZqP+R/B5fXzP3aLqY="

# Alternate method
JWT_SECRET=qG7zP4cZK9B5vN5fjYcLr1Jq3RZqP+R/B5fXzP3aLqY= node jwt.mjs -u 123 -r admin,editor
```

## Output

The generated JWT token is printed to the console along with its decoded content.

## License

MIT
