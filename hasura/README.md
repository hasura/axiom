# Axiom Hasura Installation Guide

Axiom provides a centralised platform for deploying and testing a variety of Hasura industry demos. It serves as:
- A library of demo profiles for quick deployment.
- A testing ground for showcasing new Hasura features with real-world examples.

---

## Existing Demo Profiles
* starter
* telco
* aml
* healthcare

### How to Use
To utilize an existing demo profile, run the following `ddn run` commands. These commands automatically use the scripts in the background:

- **`build`**: Builds metadata for a specific demo context.
  ```bash
  ddn run build -- <context>
  # Example: ddn run build -- telco
  ```

- **`docker-start`**: Sets up the demo's Docker environment.
  ```bash
  ddn run docker-start -- <context>
  # Example: ddn run docker-start -- telco
  ```

- **`demo`**: Executes both build and docker-start, then launches Hasura locally.
  ```bash
  ddn run demo -- <context>
  # Example: ddn run demo -- telco
  ```

- **`docker-stop`**: Stops all running Docker containers.
  ```bash
  ddn run docker-stop
  ```

### Deploying to the Cloud
For deployment instructions, see [scripts/deploy/README.md](../scripts/deploy/README.md).

---

## Adding a New Demo Profile

New profiles can be added with minimal effort, enabling streamlined testing and cloud deployment. 

The simplest way to initialise a new industry demo profile within `axiom` is to create and configure supergraph, subgraph(s), and metadata elsewhere before merging it with the following instructions.

Creating a new supergraph from scratch is beyond the scope of this documentation and the [DDN quickstart](https://hasura.io/docs/3.0/getting-started/quickstart/) should be followed

### Step 1: Name Your Profile
Decide on a name for your profile. This name (e.g., `telco`, `starter`) will be referenced throughout the repo.

```bash
# Set the $PROFILE variable for reuse
PROFILE=<your_profile_name>
echo $PROFILE

# Change directory into hasura supergraph directory
cd hasura
```

### Step 2: Create the Demo Project

1. Create a new project in DDN cloud:

```bash
ddn project create $PROFILE
```

2. Add a new context using `ddn context set` commands:

```bash
# Create a new context with the profile name
ddn context set project $PROFILE
ddn context set supergraph ../supergraph-config/$PROFILE/1-supergraph.yaml
ddn context set localEnvFile ../.env.$PROFILE
ddn context set cloudEnvFile ../.env.cloud.$PROFILE
```

### Step 2: Copy Subgraphs
1. Copy subgraphs 

Copy any subgraph directories from the source repository into `industry/$PROFILE`.

2. Create subgraphs on DDN:

Add subgraphs to the DDN project.

   ```bash
   ddn project subgraph create globals
   ddn project subgraph create <your subgraph>
   ```

### Step 3: Copy Supergraph
1. Set up a supergraph directory:
```bash
mkdir -p supergraph-config/$PROFILE
```

2. Copy `supergraph.yaml`

Copy the `supergraph.yaml` from the source supergraph into `supergraph-config/$PROFILE/1-supergraph.yaml`.

Adjust the paths within `1-supergraph.yaml` to reference the right location for subgraphs within `industry/$PROFILE`.

> [!NOTE]
> Add any additional `supergraph.yaml` files you have may be added to the same directory and the [deploy script](../scripts/deploy/) will automatically build them in order.

### Step 4: Environment Files

1. Create an .env template for example configuration

```bash
touch .env.$PROFILE.template
git add -f .env.$PROFILE.template
```

2. Copy environment files from your own supergraph to populate environments in this repository

Remember to include a JWT_SECRET and caching plugin configuration in your `.env` files to allow for builds to proceed:

```bash
echo 'JWT_SECRET="hptj8supNeslwet7nhGGr5Uu5MombVVjDmcGMOyrWa8"
CACHING_PLUGIN_PRE_PARSE_URL="http://local.hasura.dev:8787/pre-parse"
CACHING_PLUGIN_PRE_RESPONSE_URL="http://local.hasura.dev:8787/pre-response"
CACHING_PLUGIN_REDIS_URL="redis://local.hasura.dev:6379"
CACHING_PLUGIN_SECRET="zZkhKqFjqXR4g5MZCsJUZCnhCcoPyZ"' > .env.$PROFILE.template
```

_Optional_ Use the following one-liner to generate a JWT_SECRET

```bash
openssl rand -base64 32
```

3. Seed environment files:
```bash
cp .env.$PROFILE.template .env.$PROFILE
touch .env.$PROFILE.template .env.cloud.$PROFILE
```

> [!WARNING]
> Do not commit any database credentials to the pull request and ensure that the template file that gets force committed uses dummy data

---

## [_Optional_] Set up local data

Local docker-based configuration may be used to run demo profiles without cloud dependencies. This is demonstrated within the `telco` profile with a docker compose and database seeds in `.data/telco`.

> [!TIP]
> All below commands should be executed from the root directory of this repository.

### Step 1: Initial Setup
Use the starter profile to get bootstrapped sooner with existing/common data sets.

Custom `compose.yaml` and `.env` may be used. Their location must be in `.data/$PROFILE`.

1. Set up the data structure of the profile

Run the following commands to set up your profile.

```bash
# Create the directory structure
mkdir -p .data/$PROFILE

# [Optional] Add the starter compose.yaml
cp .data/starter/compose.yaml .data/$PROFILE/compose.yaml

# [Optional] Add starter postgres dataset
cp -r .data/starter/postgres .data/$PROFILE/

# Copy and customise the environment file to show the name of your profile in docker
cp .data/.env.template .data/$PROFILE/.env
sed "s/CONTAINER_PREFIX=axiomdata/CONTAINER_PREFIX=axiom${PROFILE}/g" .data/$PROFILE/.env > .data/$PROFILE/.env.tmp && mv .data/$PROFILE/.env.tmp .data/$PROFILE/.env
```

2. Customise `.data/$PROFILE/compose.yaml`

Make any further adjustments to the profile's `compose.yaml` as appropriate to use different containers, data sources and seed data.

### Step 2: Local Docker Setup

No changes to `hasura/.hasura/context.yaml` are needed as ddn run uses a context parameter. The Docker environment will be started using:

```bash
ddn run docker-start -- $PROFILE
```

This command will:
1. Verify the context exists
2. Check that the data directory exists at `.data/$PROFILE`
3. Set the DATASET environment variable
4. Start the Docker containers using the compose file at `.data/$PROFILE/compose.yaml`

### Step 3: Docker Compose
1. Create a profile-specific Docker Compose file
```bash
cp hasura/compose.yaml hasura/compose-$PROFILE.yaml
```

> [!IMPORTANT]
> Do not commit changes to the base `hasura/compose.yaml`.

---

## Testing and Deployment

1. **Test the Build:**
```bash
ddn run build -- $PROFILE
```

2. **Start the Demo:**
```bash
ddn run demo -- $PROFILE
```

3. **Cloud Deployment:**
- Ensure data sources are internet-accessible.
- Update `.env.cloud.$PROFILE` with the relevant URLs.
- Run the deploy script:
```bash
./scripts/deploy/deploy.mjs --context $PROFILE --profile $PROFILE --log-level DEBUG --full-metadata-build --override
```
---

## Notes
- **Auto Deployments:** Ensure changes to Ansible playbooks and `.data` are committed to the `main` branch to allow them to be automatically deployed.