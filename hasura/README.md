# Axiom Hasura Demo Development Guide

Axiom provides a centralized platform for deploying and testing a variety of Hasura industry demos. This guide will help you understand how to use existing demos and create new ones.

## 🌟 Existing Demo Profiles

* starter - Basic example for new demo development
* telco - Telecommunications industry demo
* aml - Anti-Money Laundering compliance demo
* healthcare - Patient operations and medical reference demo
* cpg - Consumer Packaged Goods retail operations demo
* gtm - Go-to-Market sales and marketing operations demo

## 🚀 Using Existing Demos

To utilize an existing demo profile, run the following `ddn run` commands:

- **`init`**: Initialize the environment for a specific demo (only needed once per profile).
  ```bash
  ddn run init -- <profile>
  # Example: ddn run init -- telco
  ```

- **`build`**: Build metadata for a specific demo context.
  ```bash
  ddn run build -- <profile>
  # Example: ddn run build -- telco
  ```

- **`docker-start`**: Set up the demo's Docker environment.
  ```bash
  ddn run docker-start -- <profile>
  # Example: ddn run docker-start -- telco
  ```

- **`demo`**: Execute both build and docker-start, then launch Hasura locally.
  ```bash
  ddn run demo -- <profile>
  # Example: ddn run demo -- telco
  ```

- **`docker-stop`**: Stop all running Docker containers.
  ```bash
  ddn run docker-stop
  ```

## 🏗️ Creating a New Demo Profile

This section provides a comprehensive guide for creating a new industry demo profile. Each demo requires specific files and configurations in multiple directories.

### Required Components Overview

A complete demo profile requires:

1. **In the `.data` directory**: Docker configuration and seed data
2. **In the `hasura` directory**:
   - Environment files
   - Compose configuration
   - Supergraph configuration
   - Industry-specific subgraphs and metadata

### Step 1: Set Up Your Profile Name

```bash
# Set the profile variable for reuse
PROFILE=<your_profile_name>
echo $PROFILE

# Change directory into hasura
cd hasura
```

### Step 2: Create Required Directory Structure

```bash
# Create industry directory
mkdir -p industry/$PROFILE

# Create supergraph config directory
mkdir -p supergraph-config/$PROFILE

# Create data directory
mkdir -p ../.data/$PROFILE
```

### Step 3: Set Up Data Directory (`.data/$PROFILE`)

The `.data` directory contains Docker configurations and seed data for local development.

```bash
# Create the data directory structure
mkdir -p ../.data/$PROFILE/postgres

# Copy the starter compose.yaml as a template
cp ../.data/starter/compose.yaml ../.data/$PROFILE/compose.yaml

# Copy environment template and customize it
cp ../.data/.env.template ../.data/$PROFILE/.env
sed "s/CONTAINER_PREFIX=axiomdata/CONTAINER_PREFIX=axiom${PROFILE}/g" ../.data/$PROFILE/.env > ../.data/$PROFILE/.env.tmp && mv ../.data/$PROFILE/.env.tmp ../.data/$PROFILE/.env
```

**Required files in `.data/$PROFILE`:**

<<<<<<< Updated upstream
Remember to include a JWT_SECRET configuration in your `.env` files to allow for builds to proceed:

```bash
echo 'JWT_SECRET="hptj8supNeslwet7nhGGr5Uu5MombVVjDmcGMOyrWa8"' > .env.$PROFILE.template
```
=======
1. **`compose.yaml`**: Docker Compose configuration defining:
   - Database containers (PostgreSQL, MongoDB, etc.)
   - Redis for caching
   - Caching plugin configuration
   - Any other services needed for your demo

2. **`postgres/`**: Directory containing SQL initialization scripts that will run when the container starts
   - SQL files should be named with numerical prefixes (e.g., `1-schema.sql`, `2-data.sql`)
   - These scripts create tables and populate them with seed data

3. **`.env`**: Environment variables for Docker Compose
   - Contains passwords and configuration for containers
   - Should include `CONTAINER_PREFIX` to identify your demo's containers

### Step 4: Set Up Hasura Directory Components

#### 4.1: Create Environment Files

```bash
# Create environment files
touch .env.$PROFILE.template .env.$PROFILE .env.cloud.$PROFILE

# Add basic configuration to template
cat > .env.$PROFILE.template << EOF
JWT_SECRET="hptj8supNeslwet7nhGGr5Uu5MombVVjDmcGMOyrWa8"
CACHING_PLUGIN_PRE_PARSE_URL="http://local.hasura.dev:8787/pre-parse"
CACHING_PLUGIN_PRE_RESPONSE_URL="http://local.hasura.dev:8787/pre-response"
CACHING_PLUGIN_REDIS_URL="redis://local.hasura.dev:6379"
CACHING_PLUGIN_SECRET="zZkhKqFjqXR4g5MZCsJUZCnhCcoPyZ"
>>>>>>> Stashed changes

# Add your connector environment variables here
${PROFILE^^}_MYPOSTGRES_READ_URL="postgres://postgres:hbGciOiJIUzI1NiIsInR5cCI6IkpX@local.hasura.dev:5432/postgres"
${PROFILE^^}_MYPOSTGRES_WRITE_URL="postgres://postgres:hbGciOiJIUzI1NiIsInR5cCI6IkpX@local.hasura.dev:5432/postgres"
${PROFILE^^}_MYPOSTGRES_AUTHORIZATION_HEADER="Bearer example-token"
EOF

# Copy template to actual env file
cp .env.$PROFILE.template .env.$PROFILE

# Add git tracking for template only
git add -f .env.$PROFILE.template
```

#### 4.2: Create Docker Compose Configuration

```bash
# Create profile-specific Docker Compose file
cp compose.yaml compose-$PROFILE.yaml
```

#### 4.3: Set Up Industry Directory Structure

```bash
# Create a basic subgraph directory structure
mkdir -p industry/$PROFILE/example/{connector/mypostgres,metadata}

# Create a basic subgraph.yaml
cat > industry/$PROFILE/example/subgraph.yaml << EOF
kind: Subgraph
version: v2
definition:
  name: example
  generator:
    rootPath: .
    namingConvention: graphql
  includePaths:
    - metadata
  envMapping:
    ${PROFILE^^}_MYPOSTGRES_AUTHORIZATION_HEADER:
      fromEnv: ${PROFILE^^}_MYPOSTGRES_AUTHORIZATION_HEADER
    ${PROFILE^^}_MYPOSTGRES_READ_URL:
      fromEnv: ${PROFILE^^}_MYPOSTGRES_READ_URL
    ${PROFILE^^}_MYPOSTGRES_WRITE_URL:
      fromEnv: ${PROFILE^^}_MYPOSTGRES_WRITE_URL
  connectors:
    - path: connector/mypostgres/connector.yaml
      connectorLinkName: mypostgres
EOF

# Create a placeholder for metadata
touch industry/$PROFILE/example/metadata/.keep
```

#### 4.4: Create Supergraph Configuration

```bash
# Create supergraph configuration
cat > supergraph-config/$PROFILE/1-supergraph.yaml << EOF
kind: Supergraph
version: v2
definition:
  subgraphs:
    - ../../globals/subgraph-jwt.yaml
    - ../../industry/$PROFILE/example/subgraph.yaml
EOF
```

### Step 5: Develop Your Demo Content

1. **Create connector configuration** in `industry/$PROFILE/example/connector/mypostgres/connector.yaml`
2. **Add metadata files** in `industry/$PROFILE/example/metadata/` (HML files defining models, relationships, etc.)
3. **Create SQL seed data** in `.data/$PROFILE/postgres/` to populate your database
4. **Update environment variables** in `.env.$PROFILE` with actual connection details

### Step 6: Test Your Demo

```bash
# Test the build
ddn run build -- $PROFILE

# Start the demo
ddn run demo -- $PROFILE
```

### Step 7: Prepare for Deployment

For cloud deployment:

1. Update `.env.cloud.$PROFILE` with internet-accessible data source URLs
2. Deploy using the deploy script:

```bash
../scripts/deploy/deploy.mjs --context $PROFILE --profile $PROFILE --log-level DEBUG --full-metadata-build --override
```

## 📋 Demo Profile Checklist

Ensure your demo profile includes:

### In `.data/$PROFILE/`:
- [ ] `compose.yaml` - Docker Compose configuration
- [ ] `.env` - Environment variables for Docker
- [ ] `postgres/` (or other database) - SQL initialization scripts

### In `hasura/`:
- [ ] `.env.$PROFILE.template` - Template environment file (safe to commit)
- [ ] `.env.$PROFILE` - Local environment file (do not commit)
- [ ] `.env.cloud.$PROFILE` - Cloud environment file
- [ ] `compose-$PROFILE.yaml` - Profile-specific Docker Compose

### In `hasura/industry/$PROFILE/`:
- [ ] Subgraph directories with:
  - [ ] `subgraph.yaml` - Subgraph configuration
  - [ ] `connector/` - Connector configurations
  - [ ] `metadata/` - HML metadata files

### In `hasura/supergraph-config/$PROFILE/`:
- [ ] `1-supergraph.yaml` - Primary supergraph configuration
- [ ] Additional supergraph files if needed

## 📚 Additional Resources

- [DDN Documentation](https://hasura.io/docs/3.0/)
- [Deployment Guide](../scripts/deploy/README.md)
- [Connector Development Guide](https://hasura.io/docs/3.0/data-connectors/build/overview/)