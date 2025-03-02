# Axiom
Hasura presales demo kit for showcasing DDN and PromptQL capabilities across various industry verticals.

## Prerequisites
Before getting started, ensure you have the following installed:
- [DDN CLI](https://hasura.io/docs/3.0/reference/cli/installation/)
- Git LFS (`brew install git-lfs` on macOS)
- Docker and Docker Compose
- Node.js (for utility scripts)
- Ansible (for infrastructure management)

## Overview
Axiom provides a comprehensive platform for deploying and testing Hasura industry demos. It serves as:
- A library of industry-specific demo profiles for quick deployment
- A testing ground for showcasing Hasura features with real-world examples
- A centralized toolkit for demo deployment and management

| Directory | Purpose |
|-----------|---------|
| `hasura` | Contains all DDN configurations including supergraph, subgraph, and connector metadata for industry demo profiles |
| `infra` | Ansible playbooks for managing demo servers and infrastructure automation |
| `scripts` | Utility tools for demo management, deployment, and maintenance |
| `.data` | Seed data and Docker configurations for local demonstrations |

## Demo Profiles

Axiom includes the following demo profiles:

- **Telco**: Telecommunications industry capabilities
- **AML**: Anti-Money Laundering compliance and risk management
- **Healthcare**: Patient operations and medical reference data
- **Starter**: Basic example for getting started

### Telco Demo
Demonstrates telecommunications industry capabilities with features for:
- Customer management and billing
- Network operations and monitoring
- Service provisioning and activation
- User authentication and authorization

#### Quick Start
1. Clone the repository:
```bash
git clone git@github.com:hasura/axiom.git
```

2. Set up environment:
```bash
cp hasura/.env.telco.template hasura/.env.telco
cp .data/.env.template .data/telco/.env
```

3. Launch the demo:
```bash
cd hasura
ddn run build -- telco
ddn run demo -- telco
```

### Anti-Money Laundering (AML) Demo
Comprehensive compliance and risk management solution with detailed examples and workflows available in [hasura/docs/aml-demo-guide.md](hasura/docs/aml-demo-guide.md).

#### Features
- Customer Risk Management (real-time scoring, KYC validation)
- Sanctions Screening (global database integration, automated flagging)
- Transaction Monitoring (ML-based detection, pattern recognition)
- Compliance Operations (SAR management, account freezing)

#### Quick Start
1. Clone the repository:
```bash
git clone git@github.com:hasura/axiom.git
```

2. Set up environment:
```bash
cp hasura/.env.aml.template hasura/.env.aml
cp .data/.env.template .data/aml/.env
```

3. Launch the demo:
```bash
cd hasura
ddn run build -- aml
ddn run demo -- aml
```

### Healthcare Demo
A comprehensive healthcare operations platform demonstrating patient management, clinical workflows, and medical reference data integration.

#### Features
- Patient Operations Management
- Operator Scheduling and Availability
- Case Management and Prioritization
- Medical Reference Data Integration
- Emergency Slot Management

#### Quick Start
1. Clone the repository:
```bash
git clone git@github.com:hasura/axiom.git
```

2. Set up environment:
```bash
cp hasura/.env.healthcare.template hasura/.env.healthcare
cp .data/.env.template .data/healthcare/.env
```

3. Launch the demo:
```bash
cd hasura
ddn run build -- healthcare
ddn run demo -- healthcare
```

## Command Documentation
The `ddn run` commands in `hasura/.hasura/context.yaml` now use a context parameter to dynamically work with any demo profile. This approach makes it easier to add new profiles without creating profile-specific commands.

| **Command**              | **Description**                                                                                                   |
|--------------------------|-------------------------------------------------------------------------------------------------------------------|
| `ddn run build -- <context>`            | Builds the DDN supergraph for the specified context (e.g., telco, aml, foobar)|
| `ddn run docker-start -- <context>`     | Starts the containers for the specified context's data sources locally|
| `ddn run demo -- <context>`             | Builds the supergraph and starts the containers for the specified context|
| `ddn run docker-stop`                   | Stops and removes all Docker containers and volumes related to Axiom|

For example, to work with the telco demo:
```bash
ddn run build -- telco
ddn run docker-start -- telco
ddn run demo -- telco
```

To work with a new context (e.g., media):
```bash
ddn run build -- media
ddn run docker-start -- media
ddn run demo -- media
```


## Deployment

### Deploying new metadata

Any metadata change that has been tested locally and against CI/CD in a pull request may be rolled out in a couple of seconds with the [deploy script](./scripts/deploy/). 

The deploy script will run a JWT deployment and a No-Auth deployment before applying No-Auth as the project API.

Full documentation may be found in the deploy [README](./scripts/deploy/README.md)

```
# Run the deploy script
./scripts/deploy/deploy.mjs --context axiom-dev --profile telco
```

### Deploying new connectors
New connectors should be deployed after connector configuration/schema is updated.

The simplest way to deploy new connectors is to run a new supergraph build in each region. It's important to ensure that the connector regions match the regions you're deploying.

```
# Deploy new connectors
node ./scripts/deploy/deploy.mjs --context axiom-dev --profile telco --rebuild-connectors
```

> [!IMPORTANT]  
> Hasura Note: Following a connector update, it's important to update all the `.env.cloud.*` file details in Confluence. These are not stored in the repo for obvious reasons.

## Connectors

### Deleting connectors
Sometimes the number of connectors in cloud will surpass the max (100) and it will be required to clear out old connectors.

A handy script has been created to quickly and easily delete older connectors from cloud

> [!CAUTION]
> This is a destructive command and will prevent your cloud supergraph from working correctly. Use with caution!

```
# Delete the 20 oldest connector builds from the default environment in .hasura/context.yaml
./scripts/connector-delete.sh axiom-dev 20
```