# Axiom Hasura Installation Guide

Axiom provides a centralised platform for deploying and testing a variety of Hasura industry demos. It serves as:
- A library of demo profiles for quick deployment.
- A testing ground for showcasing new Hasura features with real-world examples.

---

## Existing Demo Profiles
* starter
* telco
* finserv

### How to Use
To utilise an existing demo profile, run the commands specified in `.hasura/context.yaml`. These commands are abstracted into `ddn run` scripts for simplicity:
- **`build-telco`**: Builds metadata for the telco demo.
- **`docker-start-telco`**: Sets up the telco demo's Docker environment.
- **`demo-telco`**: Executes `docker-start-telco` and launches Hasura locally.

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

1. Create a new project in DDN cloud and context in `.hasura/context.yaml`:

```bash
ddn project create axiom-$PROFILE
ddn context create-context axiom-$PROFILE
ddn context set localEnvFile .env.$PROFILE
ddn context set cloudEnvFile .env.cloud.$PROFILE
ddn context set project axiom-$PROFILE
```

### Step 2: Copy Subgraphs
1. Copy subgraphs 

Copy any subgraph directories from the source repository into `industry/$PROFILE`.

2. Create subgraphs on DDN:

Add subgraphs to the DDN project, optionally adding the shared `auth` and `support` subgraphs.

   ```bash
   ddn project subgraph create globals
   ddn project subgraph create <your subgraph>
   # Optionally add shared axiom subgraphs
   ddn project subgraph create auth
   ddn project subgraph create support
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
1. Seed environment files:
```bash
touch .env.$PROFILE
touch .env.cloud.$PROFILE
```

2. Create an .env template for example configuration

```bash
touch .env.$PROFILE.template
git add -f .env.$PROFILE.template
```

3. Copy environment files from your own supergraph to populate environments in this repository

Remember to include a JWT_SECRET in your `.env` files to allow for JWT builds to proceed. Use the following one-liner to generate a JWT_SECRET

```bash
openssl rand -base64 32
```

> [!WARNING]
> Do not commit any database credentials to the pull request and ensure that the template file that gets force committed uses dummy data

### Step 5: Connectors

1. Add region configurations to connectors

Update `connector.yaml` in industry/$PROFILE/$SUBGRAPH/connector:


```yaml
   regionConfiguration:
     - mode: ReadWrite
       region: gcp-us-west2
```

This can be achieved automatically with `yq`
```
yq eval '.definition.regionConfiguration = [{"mode": "ReadWrite", "region": "gcp-us-west2"}]' -i industry/$PROFILE/$SUBGRAPH/connector/$CONNECTOR/connector.yaml
```

---

## [_Optional_] Set up local data

Local docker-based configuration may be used to run demo profiles without cloud dependencies. This is demonstrated within the `telco` profile with a docker compose and database seeds in `.data/telco`.

All below commands should be executed from the root directory of this repository.

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

1. Update `hasura/.hasura/context.yaml`

Add a DDN run script for starting the Docker environment. Replace `$PROFILE` with your profile name

> [!NOTE]
> Use `.data/starter/compose.yaml` for reference.

```yaml
docker-start-$PROFILE:
   bash: export DATASET=$PROFILE; docker compose -f ../.data/$PROFILE/compose.yaml --env-file ../.data/$PROFILE/.env up --build --pull always -d
   powershell: $Env:DATASET = "$PROFILE"; docker compose -f ../.data/$PROFILE/compose.yaml --env-file ../.data/$PROFILE/.env up --build --pull always -d
```

This can be achieved automatically with `yq`
```
yq eval ".definition.scripts[\"docker-start-$PROFILE\"] = {\"bash\": \"export DATASET=\$PROFILE; docker compose -f ../.data/\$PROFILE/compose.yaml --env-file ../.data/\$PROFILE/.env up --build --pull always -d\", \"powershell\": \"\$Env:DATASET = \\\"\$PROFILE\\\"; docker compose -f ../.data/\$PROFILE/compose.yaml --env-file ../.data/\$PROFILE/.env up --build --pull always -d\"}" -i hasura/.hasura/context.yaml
```

### Step 3: Docker Compose
1. Create a profile-specific Docker Compose file
```bash
cp hasura/compose.yaml hasura/compose-$PROFILE.yaml
```

> [!IMPORTANT]
> Do not commit changes to the base `hasura/compose.yaml`.

### Step 4: Add remaining scripts to `hasura/.hasura/context.yaml` 
1. Build script:
```yaml
build-$PROFILE:
   bash: ddn supergraph build local --supergraph supergraph-config/$PROFILE$/2-supergraph.yaml
   powershell: ddn supergraph build local  --supergraph supergraph-config/$PROFILE$/2-supergraph.yaml
```

This can be achieved automatically with `yq`
```
yq eval ".definition.scripts[\"build-$PROFILE\"] = {\"bash\": \"ddn supergraph build local --env-file .env.$PROFILE --env-file .env --supergraph supergraph-config/$PROFILE/2-supergraph.yaml\", \"powershell\": \"ddn supergraph build local --env-file .env.$PROFILE --env-file .env --supergraph supergraph-config/$PROFILE/2-supergraph.yaml\"}" -i hasura/.hasura/context.yaml
```

2. Demo script:
```yaml
demo-$PROFILE:
   bash: ddn run docker-start-$PROFILE; HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f compose-$PROFILE$.yaml --env-file .env.$PROFILE$ up --build --pull always -d
   powershell: $Env:HASURA_DDN_PAT = ddn auth print-pat; docker compose -f compose-$PROFILE.yaml --env-file .env.$PROFILE up --build --pull always -d
```

This can be achieved automatically with `yq`
```
yq eval ".definition.scripts[\"demo-$PROFILE\"] = {\"bash\": \" ddn run docker-start-$PROFILE; HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f compose-$PROFILE.yaml --env-file .env.$PROFILE up --build --pull always -d\", \"powershell\": \"$Env:HASURA_DDN_PAT = ddn auth print-pat; docker compose -f compose-$PROFILE.yaml --env-file .env.$PROFILE up --build --pull always -d\"}" -i hasura/.hasura/context.yaml
```

---

## Testing and Deployment

1. **Test the Build:**
```bash
ddn run build-$PROFILE
```

2. **Start the Demo:**
```bash
ddn run demo-$PROFILE
```

3. **Cloud Deployment:**
- Ensure data sources are internet-accessible.
- Update `.env.cloud.$PROFILE` with the relevant URLs.
- Run the deploy script:
```bash
./scripts/deploy/deploy.mjs --context axiom-$PROFILE --profile $PROFILE --log-level  DEBUG --full-metadata-build --override
```
---

## Notes
- **Shared Datasets:** `auth` and `support` are optional and can be omitted.
- **Auto Deployments:** Ensure changes to Ansible playbooks and `.data` are committed to the `main` branch to allow them to be automatically deployed.