# Axiom Hasura Installation Guide

Axiom provides a centralised platform for deploying and testing a variety of Hasura industry demos. It serves as:
- A library of demo profiles for quick deployment.
- A testing ground for showcasing new Hasura features with real-world examples.

---

## Existing Demo Profiles

### How to Use
To utilise an existing demo profile, run the commands specified in `.hasura/context.yaml`. These commands are abstracted into `ddn run` scripts for simplicity:
- **`build-telco`**: Builds metadata for the telco demo.
- **`docker-start-telco`**: Sets up the telco demo's Docker environment.
- **`demo-telco`**: Executes `docker-start-telco` and launches Hasura locally.

### Deploying to the Cloud
**TODO**: Add instructions for deploying demo profiles to the cloud using the deploy script.

---

## Creating a New Demo Profile

New profiles can be added with minimal effort, enabling streamlined testing and cloud deployment. Follow these steps:

### Step 1: Naming Your Profile
Decide on a name for your profile. This name (e.g., `telco`, `starter`) will be referenced throughout the repo.

### Step 2: Initial Setup
Use the starter profile to get bootstrapped sooner with existing/common data sets. BYO `compose.yaml` and `.env` is also viable but the location must be in `.data/$PROFILE`

Run the following commands to set up your profile.

```bash
# Set the $PROFILE variable for reuse
PROFILE=<your_profile_name>
echo $PROFILE

# Create the directory structure
mkdir -p .data/$PROFILE

# Add the starter compose.yaml
cp .data/starter/compose.yaml .data/$PROFILE/compose.yaml

# Add starter dataset or your own
cp -r .data/starter/postgres .data/$PROFILE/

# Copy and customise the environment file
cp .data/.env.template .data/$PROFILE/.env
sed "s/CONTAINER_PREFIX=axiomdata/CONTAINER_PREFIX=axiom${PROFILE}/g" .data/$PROFILE/.env > .data/$PROFILE/.env.tmp && mv .data/$PROFILE/.env.tmp .data/$PROFILE/.env
```

### Step 3: Local Docker Setup
1. Navigate to the Hasura directory:
   ```bash
   cd hasura
   ```

2. Update `.hasura/context.yaml`:
   Add a script for starting the Docker environment. Replace `$PROFILE` with your profile name:

   ```yaml
   docker-start-$PROFILE:
     bash: export DATASET=$PROFILE; ../.data/initdb-prepare.sh; docker compose -f ../.data/$PROFILE/compose.yaml --env-file ../.data/$PROFILE/.env up --build --pull always -d
     powershell: $Env:DATASET = "$PROFILE"; docker compose -f ../.data/$PROFILE/compose.yaml --env-file ../.data/$PROFILE/.env up --build --pull always -d
   ```

   This can be achieved automatically with `yq`
   ```
   yq eval ".definition.scripts[\"docker-start-$PROFILE\"] = {\"bash\": \"export DATASET=\$PROFILE; ../.data/initdb-prepare.sh; docker compose -f ../.data/\$PROFILE/compose.yaml --env-file ../.data/\$PROFILE/.env up --build --pull always -d\", \"powershell\": \"\$Env:DATASET = \\\"\$PROFILE\\\"; docker compose -f ../.data/\$PROFILE/compose.yaml --env-file ../.data/\$PROFILE/.env up --build --pull always -d\"}" -i .hasura/context.yaml
   ```

---

### Step 4: Creating the Demo Project

1. Create a new project and context:
   ```bash
   ddn project create axiom-$PROFILE
   ddn context create-context axiom-$PROFILE
   ddn context set localEnvFile .env.$PROFILE
   ddn context set cloudEnvFile .env.cloud.$PROFILE
   ddn context set project axiom-$PROFILE
   ```

2. Set up a supergraph directory:
   ```bash
   mkdir -p supergraph-config/$PROFILE
   ```

3. Add a starter supergraph configuration:
```bash
cat <<EOF > supergraph-config/$PROFILE/1-supergraph.yaml
kind: Supergraph
version: v2
definition:
  subgraphs:
    - ../../globals/subgraph-basic.yaml
EOF
```

---

### Step 5: Adding Subgraphs
1. Create subgraphs:
   ```bash
   SUBGRAPH=<your_subgraph_name>
   ddn project subgraph create auth
   ddn project subgraph create support
   ddn project subgraph create globals
   ddn project subgraph create $SUBGRAPH
   ```

2. Initialise and link subgraphs:
   ```bash
   ddn subgraph init $SUBGRAPH --dir industry/$PROFILE/$SUBGRAPH
   ddn subgraph add --subgraph ./industry/$PROFILE/$SUBGRAPH/subgraph.yaml --target-supergraph ./supergraph-config/$PROFILE/1-supergraph.yaml
   ```

---

### Step 6: Environment and Connectors
1. Seed environment files:
   ```bash
   cp .env.local .env.$PROFILE
   cp .env.local .env.cloud.$PROFILE
   ```

2. Define connectors:
   ```bash
   CONNECTOR=<your_connector_name>
   ddn connector init $CONNECTOR -i --subgraph industry/$PROFILE/$SUBGRAPH/subgraph.yaml
   ddn connector introspect $CONNECTOR --subgraph industry/$PROFILE/$SUBGRAPH/subgraph.yaml
   ddn model add $CONNECTOR "*" --subgraph industry/$PROFILE/$SUBGRAPH/subgraph.yaml
   ```

3. Add region configurations:
   Update `connector.yaml` in industry/$PROFILE/$SUBGRAPH/connector:
   ```yaml
   regionConfiguration:
     - mode: ReadWrite
       region: gcp-us-west2
   ```

   This can be achieved automatically with `yq`
   ```
   yq eval '.definition.regionConfiguration = [{"mode": "ReadWrite", "region": "gcp-us-west2"}]' -i industry/testing/commercial/connector/myconnector/connector.yaml
   ```

---

### Step 7: Docker Compose
Create a profile-specific Docker Compose file:
```bash
cp compose.yaml compose-$PROFILE.yaml
```
**Note:** Do not commit changes to the base `compose.yaml`.

---

### Step 8: Add remaining scripts to `.hasura/context.yaml`
1. Build script:
   ```yaml
   build-$PROFILE:
     bash: ddn supergraph build local --env-file .env.$PROFILE --env-file .env --supergraph supergraph-config/$PROFILE/1-supergraph.yaml
   ```

   This can be achieved automatically with `yq`
   ```
   yq eval ".definition.scripts[\"build-$PROFILE\"] = {\"bash\": \"ddn supergraph build local --env-file .env.$PROFILE --env-file .env --supergraph supergraph-config/$PROFILE/1-supergraph.yaml\"}" -i .hasura/context.yaml
   ```

2. Demo script:
   ```yaml
   demo-$PROFILE:
     bash: ddn run docker-start-$PROFILE; HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f compose-$PROFILE.yaml --env-file .env.$PROFILE --env-file .env up --build --pull always -d
   ```

   This can be achieved automatically with `yq`
   ```
   yq eval ".definition.scripts[\"demo-$PROFILE\"] = {\"bash\": \"ddn run docker-start-$PROFILE; HASURA_DDN_PAT=\$(ddn auth print-pat) docker compose -f compose-$PROFILE.yaml --env-file .env.$PROFILE --env-file .env up --build --pull always -d\"}" -i .hasura/context.yaml
   ```

---

### Testing and Deployment

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
     ./scripts/deploy/deploy.mjs --context axiom-$PROFILE -p $PROFILE -l DEBUG
     ```

---

## Notes
- **Shared Datasets:** `auth` and `support` are optional and can be omitted.
- **Ansible Deployments:** Ensure changes are committed to the `main` branch for cloud deployments.

**TODO:** Add detailed instructions for deploying demo profiles to the cloud.
