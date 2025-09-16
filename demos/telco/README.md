# 📱 Telco Demo

Telecommunications operations with customer management, network monitoring, and service provisioning.

## 🚀 Quick Start

```bash
git clone git@github.com:hasura/axiom.git
cd axiom
cp .data/.env.template .data/telco/.env
cd demos/telco
ddn run dataset-up
ddn supergraph build local
ddn run docker-start
```

## ✨ Actions

- **Search Operations** - Search with Gemini, Perplexity, and Brave Search
- **Subscription Management** - Create subscriptions, activate and deactivate devices
- **Document Processing** - Generate document embeddings for search
- **Customer Operations** - Billing, preferences, account management

## 📊 Data

- **Customers** - Profiles, subscriptions, billing, preferences
- **Devices** - Phone models, activation status, IoT devices
- **Services** - Plans, features, usage metrics, family plans
- **Network** - Coverage, performance, outages, spectrum
- **Support** - Tickets, interactions, document search
- **Communications** - Calls, texts, data usage, CDRs
