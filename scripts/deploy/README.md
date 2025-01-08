# Axiom Deploy

The deploy script automates the deployment process for supergraphs within a specified Hasura project. It provides flexibility through various CLI options to customise deployment, rebuild connectors, and manage metadata.

## Features

- Supports incremental and full metadata builds.
- Automates configuration file updates.
- Interactive or non-interactive deployment modes.
- Dry-run mode for safe simulations.

## Installation

1. Clone the repository.
2. Run `npm install` to install dependencies.

## Usage

Run the script using:
```bash
node deploy.mjs [options]
```

### Options

| Option                       | Description                                                                 | Default          |
|------------------------------|-----------------------------------------------------------------------------|------------------|
| `-p, --profile <profile>`    | Deploy from a demo config in `supergraph-config/<profile>`. **Required**.  | N/A              |
| `-c, --context <context>`    | Deploy specific context from `.hasura/context.yaml`.                       | `default`        |
| `-l, --log-level <level>`    | Set the log level (FATAL, ERROR, WARN, INFO, DEBUG).                        | `FATAL`          |
| `-o, --override`             | Override branch and uncommitted changes checks.                            | `false`          |
| `-d, --dry-run`              | Simulate the deployment without executing commands.                        | `false`          |
| `-n, --no-interaction`       | Deploy without interactive questions.                                      | `true`           |
| `-r, --rebuild-connectors`   | Rebuild all connectors (slow).                                             | `false`          |
| `-f, --full-metadata-build`  | Perform a full rebuild of metadata.                                        | `false`          |
| `-x, --override-description` | Override the generated deployment description.                             | N/A              |
| `-q, --quiet`                | Silence all logging except for errors.                                     | `false`          |
| `-a, --apply`                | Automatically apply the build once deployed.                               | `false`          |

## Example Commands

1. **Deploy with the telco profile axiom-test project**:
   ```bash
   node deploy.mjs -p telco -c axiom-test
   ```

1. **Deploy and apply builds**:
   ```bash
   node deploy.mjs -p telco -c axiom-test -a
   ```

2. **Dry run deployment**:
   ```bash
   node deploy.mjs -p telco -c axiom-test -d
   ```

3. **Full metadata rebuild without interaction**:
   ```bash
   node deploy.mjs -p telco -c axiom-test -f -n
   ```

4. **Full metadata rebuild AND rebuild all connectors**:
   ```bash
   node deploy.mjs -p telco -c axiom-test -f -r
   ```

5. **CI/CD Implementation**:

   ```bash
    deploy.mjs \
    --context axiom-test \
    --profile telco \
    --override-description "${calculatedSha} [PR-${{ github.event.pull_request.number }}: ${{ github.event.pull_request.title }}] Test build for commit $GITHUB_SHA" \
    --rebuild-connectors \
    --override \
    --log-level FATAL \
    --quiet \
    --no-interaction
    ```
