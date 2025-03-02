# 💚 Axiom: Hasura Industry Demo Toolkit

**API and AI Demonstration with Hasura DDN and PromptQL**

![Hasura DDN](https://img.shields.io/badge/Hasura-DDN%203.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🏁 Quick Start

```bash
# Cloning the repository
git clone git@github.com:hasura/axiom.git

# Running a demo (telco, aml, healthcare)
cd hasura
ddn run demo -- telco
```

## 🧰 Prerequisites
The following dependencies are required for running the demos:
- [DDN CLI](https://hasura.io/docs/3.0/reference/cli/installation/) - The Hasura command line interface
- Git LFS (`brew install git-lfs` on macOS) - Required for handling large files
- Docker and Docker Compose - Necessary for running local environments
- Node.js - Needed for utility scripts

**Optional:**
- Ansible - Only needed for internal presales team infrastructure management

## 🔍 Overview
Axiom brings Hasura's capabilities to life through industry-specific demos:
- 🏭 **Ready-to-run industry demos** - Real-world industry use cases with minimal setup
- 🧪 **Feature testing playground** - New DDN & PromptQL features demonstrated in an example project
- 🛠️ **Extensible toolkit** - Easy to add new demos and customisations

| Directory | What's Inside | Why It's Awesome |
|-----------|---------------|------------------|
| 📁 `hasura` | DDN configurations, supergraphs, subgraphs, and connector metadata | The heart of each demo - where DDN metadata resides |
| 📁 `scripts` | Utility tools and helper scripts | Makes deployment and management simple |
| 📁 `.data` | Seed data and Docker configurations | Pre-configured data to make demos work out of the box |
| 📁 `infra` | Ansible playbooks (optional) | For internal presales team infrastructure management |

## 🌟 Demo Profiles

Axiom comes prebuilt with industry demos:

### 📱 Telco
Telecommunications solutions with customer management, network operations, and service provisioning.

### 💰 AML (Anti-Money Laundering)
Compliance and risk management with real-time monitoring and automated flagging.

### 🏥 Healthcare
Patient operations platform with scheduling, case management, and medical reference data.

### 👶 Starter
A simplified example to act as a starter kit for new demo use cases.

## 📱 Telco Demo in Action

### Features
- **Customer 360° View** - Customer management and billing
- **Network Operations Center** - Real-time monitoring and analytics
- **Service Activation** - Provisioning and activation workflows
- **Identity Management** - Authentication and authorisation

### Quick Start
```bash
# Setting up the environment
cp hasura/.env.telco.template hasura/.env.telco
cp .data/.env.template .data/telco/.env

# Launching the demo
cd hasura
ddn run demo -- telco
```

## 💰 AML Demo in Action

### Features
- **Risk Scoring** - Real-time customer risk assessment and KYC validation
- **Sanctions Screening** - Automated sanctions flagging
- **Smart Monitoring** - AI detection of suspicious patterns
- **Compliance Workflows** - SAR management and account freezing

### Quick Start
```bash
# Setting up the environment
cp hasura/.env.aml.template hasura/.env.aml
cp .data/.env.template .data/aml/.env

# Launching the demo
cd hasura
ddn run demo -- aml
```

## 🏥 Healthcare Demo in Action

### Features
- **Patient Ops** - Patient management and care coordination
- **Smart Scheduling** - Operator scheduling and availability management
- **Case Prioritisation** - Case management with urgency tracking
- **Medical Reference** - Drug and procedure reference data
- **Emergency Response** - Emergency slot management system

### Quick Start
```bash
# Setting up the environment
cp hasura/.env.healthcare.template hasura/.env.healthcare
cp .data/.env.template .data/healthcare/.env

# Launching the demo
cd hasura
ddn run demo -- healthcare
```

## 🛠️ Command Reference

| **Command** | **What it Does** | **When to Use It** |
|-------------|------------------|-------------------|
| `ddn run build -- <context>` | 🏗️ Builds the DDN supergraph | When you've made metadata changes |
| `ddn run docker-start -- <context>` | 🐳 Starts the Docker containers | When you need the data sources |
| `ddn run demo -- <context>` | ✨ Does both build & docker-start | The all-in-one command to get started |
| `ddn run docker-stop` | 🛑 Stops all containers | When you're done or need to switch demos |

### Examples

**Working with the Telco demo:**
```bash
# Complete setup with a single command
ddn run demo -- telco

# Step-by-step alternative approach
ddn run build -- telco
ddn run docker-start -- telco
```

**Creating your own demo:**
```bash
# Running a custom context (e.g., retail)
ddn run demo -- retail
```
> [!TIP]
> The `ddn run demo` command provides the fastest path to a running demo.


## 🌟 Deployment & Management

Demos may be pushed to Hasura Cloud with simple/configurable deployment tools

### Deploying Metadata Changes

Changes are released in seconds with _deploy_. Full documentation in the [deploy README](./scripts/deploy/README.md).

```bash
# Deploying changes to the cloud
./scripts/deploy/deploy.mjs --context telco-dev --profile telco
```

The script handles both JWT and No-Auth deployments automatically, making deployment easier.

### Managing Connectors

#### Deploying New Connectors

After updating connector configuration or schema, the [deploy script](./scripts/deploy/README.md) should be used with the `--rebuild-connectors` flag:

```bash
# Deploying updated connectors
node ./scripts/deploy/deploy.mjs --context telco-dev --profile telco --rebuild-connectors
```

#### Cleaning Up Old Connectors

The [connector cleanup tool](./scripts/connector-delete.sh) helps maintain a tidy cloud environment:

```bash
# Removing the 20 oldest connector builds
./scripts/connector-delete.sh telco-dev 20
```

> [!CAUTION]
> **Caution advised:** This operation removes connectors from the cloud supergraph.

## 🎉 Building Custom Demos

The [hasura/README.md](hasura/README.md) provides detailed instructions on adding new industry demos to the toolkit.