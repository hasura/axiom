# 💚 Axiom: PromptQL Industry Demo Toolkit

## AI Demonstration with PromptQL

![PromptQL](https://img.shields.io/badge/PromptQL-DDN%203.0-b6fc34)
![License](https://img.shields.io/badge/license-MIT-green)

## 🧰 Prerequisites

The following dependencies are required for running the demos:

- [DDN CLI](https://hasura.io/docs/3.0/reference/cli/installation/) - The command line interface
- Git LFS (`brew install git-lfs` on macOS) - Required for handling large files
- Docker and Docker Compose - Necessary for running local environments
- Node.js - Needed for utility scripts
- jq - Required for utility scripts (`brew install jq`)

**Optional:**

- Ansible - Only needed for internal presales team infrastructure management

## 🏁 Quick Start

```bash
# Cloning the repository
git clone git@github.com:hasura/axiom.git

# Make sure your'e inside root
cd axiom

# Copy env vars to your demo data generator
cp .data/.env.template .data/<demo>/.env

cd demos/<demo>

# Start the backend data services for the demo
ddn run dataset-up

# Build supergraph locally
ddn supergraph build local

# Running a demo (PromptQL + DDN)
ddn run docker-start

# Open a new terminal window and Run the PromptQL playground in CHROME browser.
ddn console --local

# PromptQL Playground should open in a new window. If it doesn't work, try with Chrome browser.
```
## 🔍 Overview

Axiom brings PromptQL's capabilities to life through industry-specific demos:

- 🏭 **Ready-to-run industry demos** - Real-world industry use cases with minimal setup
- 🧪 **Feature testing playground** - New DDN & PromptQL features demonstrated in an example project
- 🛠️ **Extensible toolkit** - Easy to add new demos and customisations

| Directory    | What's Inside                                                      | Why It's Awesome                                      |
| ------------ | ------------------------------------------------------------------ | ----------------------------------------------------- |
| 📁 `demos`   | DDN configurations, supergraphs, subgraphs, and connector metadata | The heart of each demo - where DDN metadata resides   |
| 📁 `scripts` | Utility tools and helper scripts                                   | Makes deployment and management simple                |
| 📁 `.data`   | Seed data and Docker configurations                                | Pre-configured data to make demos work out of the box |
| 📁 `infra`   | Ansible playbooks (optional)                                       | For internal presales team infrastructure management  |

## 🌟 Demo Profiles

Axiom comes prebuilt with industry demos. Each demo has its own detailed README with features, datasets, and quickstart instructions:

### 📱 [Telco](demos/telco/README.md)

Telecommunications solutions with customer management, network operations, and service provisioning.

### 💰 [AML (Anti-Money Laundering)](demos/aml/README.md)

Compliance and risk management with real-time monitoring and automated flagging.

### 🏥 [Healthcare](demos/healthcare/README.md)

Patient operations platform with scheduling, case management, and medical reference data.

### 🛒 [CPG (Consumer Packaged Goods)](demos/cpg/README.md)

Retail operations and execution platform for CPG companies with product management, inventory allocation, and promotional planning.

### 📊 [GTM (Go-to-Market)](demos/gtm/README.md)

Sales and marketing operations platform with opportunity management, campaign execution, and revenue forecasting.

### 🔍 [Due Diligence](demos/diligence/README.md)

Financial due diligence platform with valuation operations, financial analysis, and ERP data integration.

### 👟 [SCO (Supply Chain Operations)](demos/supplychain/README.md)

End-to-end supply chain management platform with manufacturing, logistics, and e-commerce integration.

## 🌟 Deployment & Management

Demos may be pushed to PromptQL Cloud with standard [DDN CLI](https://promptql.io/docs/reference/cli/installation/) tooling.

### Deploying Metadata Changes

Changes are released in seconds with DDN CLI.

```bash
cd demos/<demo>

# quick deploy (no message)
ddn supergraph build create

# better: include name and commit summary for traceability
# e.g. Adam Malone: c196a1e CI: Modify cpg (#189)
ddn supergraph build create --description "$(git config user.name): $(git log -1 --pretty=format:'%h %s')"

```

The script handles both JWT and No-Auth deployments automatically, making deployment easier.

### Managing Connectors

#### Cleaning Up Old Connectors

The [connector cleanup tool](./scripts/connector-delete.sh) helps maintain a tidy cloud environment

> [!CAUTION] >

**Caution advised:** This operation removes connectors from the cloud supergraph.

```bash
# Removing the 20 oldest connector builds
./scripts/connector-delete.sh telco-dev 20
```

## 🔐 Authentication

All demos support multiple authentication modes configured in their `auth-config.hml`

Demos should be configured to allow data access for a non-privileged customer role with a predefined id for simplicity.

### NoAuth Mode (Default)

- No headers required
- Default admin role access

### JWT Mode

JWT mode can be achieved both in PromptQL and DDN by setting the following headers:

- `X-Hasura-Auth-Mode: jwt`
- `Authorization: Bearer <token>`

### Token generation

Default functionality creates a token with the following grants:

- x-hasura-role: customer
- x-hasura-user-id: 7

```bash
cd demos/<demo-name>
ddn run jwt-gen
```

For advanced token generation options, see the [JWT documentation](scripts/jwt/README.md).
