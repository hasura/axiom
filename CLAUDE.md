# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Core DDN Operations
- `ddn run dataset-up -- <demo>` - Start backend data services for a demo (e.g., `ddn run dataset-up -- telco`)
- `ddn run docker-start` - Start the DDN + PromptQL demo environment
- `ddn run dataset-down -- <demo>` - Stop backend data services for a demo
- `ddn supergraph build create` - Quick deploy metadata changes to cloud
- `ddn supergraph build create --description "$(git config user.name): $(git log -1 --pretty=format:'%h %s')"` - Deploy with commit traceability

### Demo Management
- `ddn run jwt-gen` - Generate JWT tokens for demo authentication (from within demo directory)
- `./scripts/connector-delete.sh <project> <count>` - Remove old connectors to stay under limits
- `./scripts/connector-keepalive.sh` - Keep connectors warm (prevents cold starts)

### Prerequisites Setup
Before running demos, ensure you have:
- DDN CLI installed
- Git LFS (`brew install git-lfs`)
- Docker and Docker Compose
- Node.js and jq (`brew install jq`)

## Architecture Overview

### Repository Structure
This is the Axiom PromptQL Industry Demo Toolkit - a collection of industry-specific demos showcasing DDN 3.0 and PromptQL capabilities.

**Top-level directories:**
- `demos/` - Industry-specific demo configurations (telco, aml, healthcare, cpg, gtm, diligence, supplychain)
- `scripts/` - Utility tools for deployment, JWT generation, and maintenance
- `infra/` - Ansible playbooks for infrastructure management
- `hasura/` - Hasura engine build artifacts

### Demo Architecture Pattern
Each demo follows a consistent structure:
- `hasura.yaml` - DDN project configuration
- `supergraph.yaml` - Defines subgraphs composition
- `compose.yaml` - Docker services orchestration
- `globals/` - Global configurations (auth, GraphQL, PromptQL settings)
- Domain-specific subgraphs (e.g., `customer/`, `network/`, `support/` for telco)

### Subgraph Structure
Each subgraph contains:
- `connector/` - Data connector implementations (TypeScript functions, configuration JSONs)
- `metadata/` - DDN metadata files (.hml format) defining data models and relationships
- `subgraph.yaml` - Subgraph definition

### Authentication Modes
All demos support:
- **NoAuth** (default) - No authentication required
- **JWT** - Requires `X-Hasura-Auth-Mode: jwt` header and `Authorization: Bearer <token>`

Default JWT tokens include:
- `x-hasura-role: customer`
- `x-hasura-user-id: 7`

## Working with Demos

### Starting a Demo
```bash
cd demos/<demo-name>
cp .data/.env.template .data/<demo-name>/.env  # Configure environment
ddn run dataset-up -- <demo-name>              # Start data services
ddn run docker-start                           # Start DDN environment
```

### Demo-Specific Features
- **Telco**: Customer management, network operations, support systems
- **AML**: Anti-money laundering compliance and risk management
- **Healthcare**: Patient operations, scheduling, medical reference data
- **CPG**: Consumer packaged goods retail operations and execution
- **GTM**: Go-to-market sales and marketing operations
- **Diligence**: Financial due diligence and valuation operations
- **Supply Chain**: End-to-end supply chain management

### PromptQL Configuration
Each demo includes `promptql-config.hml` with:
- Industry-specific system instructions
- Custom query interpretation rules
- Technical requirements (SQL/Python protocols)
- Output formatting requirements

### Connector Types
- **TypeScript Functions** - Custom business logic (in `functions.ts` files)
- **Database Connectors** - PostgreSQL, MongoDB, ClickHouse integrations
- **External API Connectors** - Stripe, Salesforce, etc.

## Important Notes

- Each demo runs independently with its own data services and DDN configuration
- Environment files (`.env`) contain demo-specific database connections and API keys
- Connector deployments are limited to 100 per project - use cleanup scripts regularly
- All TypeScript connectors use Node.js with standard npm package management
- HML files (.hml) define DDN metadata - these are the core configuration files for data models and relationships