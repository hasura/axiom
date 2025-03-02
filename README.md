# 💚 Axiom: Hasura Industry Demo Toolkit

**Demonstrate API and AI with Hasura DDN and PromptQL**

![Hasura DDN](https://img.shields.io/badge/Hasura-DDN%203.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🏁 Quick Start

```bash
# Clone the repo
git clone git@github.com:hasura/axiom.git

# Choose a demo (telco, aml, healthcare)
cd hasura
ddn run demo -- telco
```

## 🧰 Prerequisites
Before diving in, you'll need:
- [DDN CLI](https://hasura.io/docs/3.0/reference/cli/installation/) - The Hasura command line interface
- Git LFS (`brew install git-lfs` on macOS) - For handling large files
- Docker and Docker Compose - For running local environments
- Node.js - For utility scripts

**Optional:**
- Ansible - Only needed for internal presales team infrastructure management

## 🔍 Overview
Axiom brings Hasura's capabilities to life through industry-specific demos:
- 🏭 **Ready-to-run industry demos** - Showcase real-world applications with minimal setup
- 🧪 **Feature testing playground** - See how new Hasura features work in realistic scenarios
- 🛠️ **Extensible toolkit** - Easily add your own demos and customizations

| Directory | What's Inside | Why It's Awesome |
|-----------|---------------|------------------|
| 📁 `hasura` | DDN configurations, supergraphs, subgraphs, and connector metadata | The heart of each demo - where DDN metadata resides |
| 📁 `scripts` | Utility tools and helper scripts | Makes deployment and management a breeze |
| 📁 `.data` | Seed data and Docker configurations | Pre-configured data to make demos work out of the box |
| 📁 `infra` | Ansible playbooks (optional) | For internal presales team infrastructure management |

## 🌟 Demo Profiles

Axiom comes loaded with exciting industry demos:

### 📱 Telco
Cutting-edge telecommunications solutions with customer management, network operations, and service provisioning.

### 💰 AML (Anti-Money Laundering)
Sophisticated compliance and risk management with real-time monitoring and automated flagging.

### 🏥 Healthcare
Comprehensive patient operations platform with scheduling, case management, and medical reference data.

### 👶 Starter
Perfect for beginners - a simplified example to help you get up and running quickly.

## 📱 Telco Demo in Action

### Features
- **Customer 360° View** - Customer management and billing
- **Network Operations Center** - Real-time monitoring and analytics
- **Service Activation** - Provisioning and activation workflows
- **Identity Management** - Authentication and authorization

### Quick Start
```bash
# Set up the environment
cp hasura/.env.telco.template hasura/.env.telco
cp .data/.env.template .data/telco/.env

# Launch the demo
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
# Set up the environment
cp hasura/.env.aml.template hasura/.env.aml
cp .data/.env.template .data/aml/.env

# Launch the demo
cd hasura
ddn run demo -- aml
```

## 🏥 Healthcare Demo in Action

### Features
- **Patient Ops** - Patient management and care coordination
- **Smart Scheduling** - Operator scheduling and availability management
- **Case Prioritization** - Case management with urgency tracking
- **Medical Reference** - Drug and procedure reference data
- **Emergency Response** - Emergency slot management system

### Quick Start
```bash
# Set up the environment
cp hasura/.env.healthcare.template hasura/.env.healthcare
cp .data/.env.template .data/healthcare/.env

# Launch the demo
cd hasura
ddn run demo -- healthcare
```

Discover how GraphQL can transform healthcare data management!

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
# One command does it all!
ddn run demo -- telco

# Or step by step if you prefer
ddn run build -- telco
ddn run docker-start -- telco
```

**Creating your own demo:**
```bash
# After setting up your new context (e.g., retail)
ddn run demo -- retail
```
> [!TIP]
> Use `ddn run demo` for the fastest path to a running demo!


## 🌟 Deployment & Management

Take your demos to the cloud with our streamlined deployment tools!

### Deploying Metadata Changes

Roll out your changes in seconds with our powerful deploy script! Full documentation in the [deploy README](./scripts/deploy/README.md).

```bash
# Deploy your changes to the cloud
./scripts/deploy/deploy.mjs --context telco-dev --profile telco
```

The script handles both JWT and No-Auth deployments automatically, making your life easier.

### Managing Connectors

#### Deploying New Connectors

After updating connector configuration or schema, use the [deploy script](./scripts/deploy/README.md) with the `--rebuild-connectors` flag:

```bash
# Deploy your updated connectors
node ./scripts/deploy/deploy.mjs --context telco-dev --profile telco --rebuild-connectors
```

> **Important:** Remember to update the `.env.cloud.*` file details in Confluence after connector updates!

#### Cleaning Up Old Connectors

Keep your cloud environment tidy with our [connector cleanup tool](./scripts/connector-delete.sh):

```bash
# Remove the 20 oldest connector builds
./scripts/connector-delete.sh telco-dev 20
```

> [!CAUTION]
> **Use with caution!** This will remove connectors from your cloud supergraph.

## 🎉 Ready to Build Your Own Demo?

Check out the [hasura/README.md](hasura/README.md) for detailed instructions on adding your own industry demo!