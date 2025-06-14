# 💚 Axiom: PromptQL Industry Demo Toolkit

**AI Demonstration with PromptQL**

![PromptQL](https://img.shields.io/badge/PromptQL-DDN%203.0-b6fc34)
![License](https://img.shields.io/badge/license-MIT-green)

## 🧰 Prerequisites
The following dependencies are required for running the demos:
- [DDN CLI](https://hasura.io/docs/3.0/reference/cli/installation/) - The command line interface
- Git LFS (`brew install git-lfs` on macOS) - Required for handling large files
- Docker and Docker Compose - Necessary for running local environments
- Node.js - Needed for utility scripts
- jq - Required for utility scripts

**Optional:**
- Ansible - Only needed for internal presales team infrastructure management

## 🏁 Quick Start

```bash
# Cloning the repository
git clone git@github.com:hasura/axiom.git

cd axiom/hasura

# Init is only required once for each demo profile
ddn run init -- telco

# Running a demo (telco, aml, healthcare)
ddn run demo -- telco
```

## 🔍 Overview
Axiom brings PromptQL's capabilities to life through industry-specific demos:
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

### 🛒 CPG (Consumer Packaged Goods)
Retail operations and execution platform for CPG companies with product management, inventory allocation, and promotional planning.

### 📊 GTM (Go-to-Market)
Sales and marketing operations platform with opportunity management, campaign execution, and revenue forecasting.

### 🔍 Due Diligence
Financial due diligence platform with valuation operations, financial analysis, and ERP data integration.

### 👶 Starter
A simplified example to act as a starter kit for new demo use cases.

### 👟 SCO (Supply Chain Operations)
End-to-end supply chain management platform with manufacturing, logistics, and e-commerce integration.

## 📱 Telco Demo in Action

### Features
- **Customer 360° View** - Customer management, billing, and preferences
- **Network Operations Center** - Real-time monitoring, performance analytics, and outage management
- **Service Activation** - Device activation/deactivation, subscription management, and service provisioning
- **Identity Management** - Authentication, authorisation, and user profiles
- **Support Services** - Document search, vector embeddings, and AI-powered assistance
- **Search Capabilities** - Integration with Brave Search, Gemini, and Perplexity

### Quick Start
```bash
cd hasura

# Setting up the environment
ddn run init -- telco

# Launching the demo
ddn run demo -- telco
```

## 💰 AML Demo in Action

### Features
- **Risk Scoring** - Real-time customer risk assessment and KYC validation
- **Sanctions Screening** - Automated sanctions flagging
- **Smart Monitoring** - AI detection of suspicious patterns
- **Compliance Workflows** - SAR management, account freezing, and transaction holds
- **Account Operations** - Account management and financial transfers

### Quick Start
```bash
cd hasura

# Setting up the environment
ddn run init -- aml

# Launching the demo
ddn run demo -- aml
```

## 🏥 Healthcare Demo in Action

### Features
- **Patient Ops** - Patient management and care coordination
- **Smart Scheduling** - Operator scheduling and availability management
- **Case Prioritisation** - Case management with urgency and risk tracking
- **Medical Reference** - Drug and procedure reference data
- **Emergency Response** - Emergency slot management system
- **Insurance Integration** - Insurance plan management and verification
- **Operator Management** - Operator availability adjustment and scheduling

### Quick Start
```bash
cd hasura

# Setting up the environment
ddn run init -- healthcare

# Launching the demo
ddn run demo -- healthcare
```

## 🛒 CPG Demo in Action

### Features
- **Product Management** - Comprehensive product catalog and category management
- **Retail Operations** - Inventory tracking, assortment planning, and availability monitoring
- **Promotional Planning** - Campaign creation, discount management, and promotional effectiveness
- **Market Analytics** - Sales tracking, market share analysis, and competitive intelligence
- **Retail Execution** - Store-level merchandising, pricing updates, and inventory allocation
- **Supply Chain Visibility** - Supply chain event tracking and management
- **Retail Actions** - Inventory allocation, promotion creation, and product pricing updates

### Quick Start
```bash
cd hasura

# Setting up the environment
ddn run init -- cpg

# Launching the demo
ddn run demo -- cpg
```

## 🔍 Due Diligence Demo in Action

### Features
- **Financial Analysis** - Comprehensive financial statement analysis and validation
- **Valuation Operations** - Scenario modeling and adjustment calculations
- **Inconsistency Detection** - Automated flagging of financial inconsistencies
- **ERP Integration** - Complete access to enterprise resource planning data
- **Finding Management** - Creation and tracking of due diligence findings
- **Budget Planning** - Budget vs. actual analysis and capital expenditure tracking
- **Business Unit Management** - Department, region, and business unit organization

### Quick Start
```bash
cd hasura

# Setting up the environment
ddn run init -- diligence

# Launching the demo
ddn run demo -- diligence
```

## 📊 GTM Demo in Action

### Features
- **Sales Operations** - Opportunity management, forecasting, and pipeline analytics
- **Marketing Automation** - Campaign management, lead nurturing, and sequence creation
- **Revenue Intelligence** - Call analytics, opportunity insights, and revenue forecasting
- **Account Management** - Customer 360° view with integrated contact and account data
- **Sales Enablement** - Content management, call transcriptions, and action items
- **MEDDPICC Framework** - Methodology for qualifying and managing complex sales opportunities
- **Sequence Management** - Lead sequence creation and contact assignment
- **Call Intelligence** - Call participants, topics, and action item tracking

### Quick Start
```bash
cd hasura

# Setting up the environment
ddn run init -- gtm

# Launching the demo
ddn run demo -- gtm
```

## 📦 Available Datasets

Each demo profile comes with pre-configured datasets to make demos work out of the box:

### 📱 Telco
- **Customer Data**: User profiles, subscriptions, billing information, preferences
- **Device Data**: Phone models, activation status, upgrade eligibility, IoT devices
- **Service Data**: Plans, features, usage metrics, VoIP services, family plans
- **Support Data**: Customer interactions, feedback, service tickets, document search
- **Network Data**: Coverage areas, performance metrics, outages, spectrum licenses
- **Communication Data**: Calls, texts, data usage, CDR (Call Detail Records)
- **Authentication Data**: User authentication and authorization
- **Search Services**: Integration with Brave Search, Gemini, and Perplexity

### 💰 AML (Anti-Money Laundering)
- **Transaction Data**: Financial transactions with timestamps and amounts
- **Customer Profiles**: Risk scores, KYC information, account details
- **Sanctions Lists**: Flagged entities and individuals
- **Alert Data**: Suspicious activity reports (SARs) and investigation status
- **Compliance Data**: Transaction holds, account freezes, financial transfers

### 🏥 Healthcare
- **Patient Records**: Demographics, medical history, insurance information
- **Provider Data**: Doctors, specialists, availability schedules, operator management
- **Appointment Data**: Scheduling, cancellations, no-shows, emergency slots
- **Medical Reference**: Medications, procedures, diagnostic codes, drug packaging
- **Case Management**: Case urgency, risk assessment, reassignment, review flagging
- **Insurance Data**: Insurance plans and coverage information

### 🛒 CPG (Consumer Packaged Goods)
- **Product Data**: Comprehensive product catalog with categories and attributes
- **Inventory Data**: Stock levels, availability, warehouse locations, inventory transactions
- **Sales Data**: Transactions, pricing history, promotional effectiveness
- **Market Data**: Competitor products, market shares, demand forecasts
- **Retail Data**: Retailers, channels, brands, assortment planning
- **Supply Chain Data**: Supply chain events, shipping information
- **Promotional Data**: Promotions, campaign effectiveness, discount strategies

### 📊 GTM (Go-to-Market)
- **Account Data**: Customer accounts, contacts, relationships, user roles
- **Opportunity Data**: Sales pipeline, forecasts, win/loss analysis, MEDDPICC scoring
- **Campaign Data**: Marketing campaigns, lead sequences, engagement metrics, campaign members
- **Call Data**: Transcriptions, action items, topics discussed, call participants
- **Product Data**: Product catalog, opportunity line items, contracts
- **Sequence Data**: Lead sequences, sequence steps, contact assignment

### 🔍 Due Diligence
- **Financial Data**: Statements, general ledger, cash flow, financial statement items
- **Operational Data**: Business units, departments, regions, debt instruments
- **Sales Data**: Orders, customers, products, suppliers, purchase orders
- **Planning Data**: Budget plans, capital expenditures, marketing campaigns, budget vs. actual
- **Inventory Data**: Inventory movements, inventory tracking
- **Valuation Data**: Adjustment scenarios, financial inconsistency flagging

### 👟 SCO (Supply Chain Operations)
- **Manufacturing Data**: Bill of materials, production orders, factories, raw materials
- **Logistics Data**: Warehouses, shipments, inventory movements
- **Supplier Data**: Suppliers, raw materials, supplier materials
- **Product Data**: Shoes, product specifications, pricing
- **E-commerce Data**: Customer orders and fulfillment
- **Operations Data**: Loyalty rewards and shipment requests

### 👶 Starter
- **Basic Data**: Simple customer dataset for demonstration purposes

## �️ Command Reference

| **Command** | **What it Does** | **When to Use It** |
|-------------|------------------|-------------------|
| `ddn run init -- <context>` | 🛠️ Initializes the DDN environment | Run this once before using other commands or when setting up a new demo |
| `ddn run build -- <context>` | 🏗️ Builds the DDN supergraph | When you've made metadata changes |
| `ddn run docker-start -- <context>` | 🐳 Starts the Docker containers | When you need the data sources |
| `ddn run demo -- <context>` | ✨ Does build, docker-start, and starts PromptQL | The all-in-one command to get started |
| `ddn run docker-stop` | 🛑 Stops all containers | When you're done or need to switch demos |

```
> [!TIP]
> The `ddn run init` & `ddn run demo` commands provide the fastest path to a running demo.


## 🌟 Deployment & Management

Demos may be pushed to PromptQL Cloud with simple/configurable deployment tools

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

## 🔌 Integration Capabilities

Axiom demonstrates PromptQL's powerful integration capabilities across various systems:

### Database Integrations
- **PostgreSQL**: Used in multiple demos for relational data storage
- **MongoDB**: Used in Telco and SCO demos for document storage
- **ClickHouse**: Used in Telco for high-performance analytics

### API Integrations
- **Stripe**: Payment processing in the Telco demo
- **Search Services**: Integration with Brave Search, Gemini, and Perplexity

### AI & Vector Search
- **Document Embeddings**: Vector search capabilities in the Telco support module
- **PromptQL**: AI-powered operations across multiple demos

### Event-Driven Architecture
- **Kafka**: Event streaming in the Telco network module

## 🧩 Architecture Patterns

Axiom showcases several architectural patterns that can be applied to real-world applications:

### Microservices
Each industry demo is composed of multiple subgraphs that can be deployed and scaled independently.

### Federated Data Graph
The supergraph configuration demonstrates how to create a unified API across disparate data sources.

### Hybrid Transactional/Analytical Processing (HTAP)
The Telco demo shows how to combine transactional systems (PostgreSQL) with analytical systems (ClickHouse).

### Event-Driven Architecture
The Kafka integration demonstrates how to build event-driven systems with PromptQL.

### AI-Enhanced Applications
Vector search and PromptQL integrations show how to enhance applications with AI capabilities.
