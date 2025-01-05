
# Axiom Hasura Install
Axiom provides a library of different demo profiles that can be used (and deployed) with ease. The aim of Axiom is allow multiple different Hasura industry demos to be used from one place.

Axiom also provides a testing ground for new Hasura features and will include recently released features as a means of providing a real world example.


## Existing demo profiles
### Usage
To use an existing demo profile, use the commands that exist within the `.hasura/context.yaml` file. By abstracting the commands that Hasura uses into `ddn run` commands, it's far easier to spin up and test industry demos:

* build-telco: builds the metadata that powers the telco demo
* docker-start-telco: creates the docker ecosystem for the telco demo
* demo-telco: runs docker-start-telco and then spins up Hasura locally


### Deploying an existing demo profile to the cloud
TODO: Add directions for how to use the deploy script


## Setting up a new demo profile
New demo profiles can be incorporated with a limited number of steps. Doing this will allow the deployment scripts (and CI/CD) to hook into the demo profile and make testing/rollout to cloud more simple.

### Instructions
First decide on a name for your profile. This will be important as it'll be a key to use throughout this repo e.g. the telco demo is called 'telco' and the stub/example demo is called 'starter'.

#### Set up profile and add default data
```
# Set your $PROFILE so all future commands work
PROFILE=<your profile name here>
echo $PROFILE

# Create a new directory in .data for your demo profile
mkdir -p .data/$PROFILE

# Copy the starter compose.yaml in (or create your own docker compose)
cp .data/starter/compose.yaml .data/$PROFILE/compose.yaml

# Copy the starter dataset in. Alternatively, use your own that are referenced in your .data/$PROFILE/compose.yaml
cp -r .data/starter/postgres .data/$PROFILE/

# Copy the environment variable template and alter/add any additional variables you have in your compose.yaml that should not be committed.
cp .data/.env.template .data/$PROFILE/.env`

# Use this one-liner to rename the containers if needed
sed "s/CONTAINER_PREFIX=axiomdata/CONTAINER_PREFIX=axiom${PROFILE}/g" .data/$PROFILE/.env > .data/$PROFILE/.env.tmp && mv .data/$PROFILE/.env.tmp .data/$PROFILE/.env
```

#### Run docker for local datasets
Navigate into the hasura directory and create the new profile:

`cd hasura`

Add this to the scripts section in your `.hasura/context.yaml` making sure you **manually** replace `$PROFILE` with the name of your profile:
```
docker-start-$PROFILE:
      bash: export DATASET=$PROFILE; ../.data/initdb-prepare.sh; docker compose -f ../.data/$PROFILE/compose.yaml --env-file ../.data/$PROFILE/.env up --build --pull always -d
      powershell: $Env:DATASET = "$PROFILE"; docker compose -f ../.data/$PROFILE/compose.yaml --env-file ../.data/$PROFILE/.env up --build --pull always -d
```

N.B. the initdb-prepare.sh will automatically combine common datasets (auth and support). This can be removed if you don't plan on using those.



#### Create the project for your demo profile
```
ddn project create axiom-$PROFILE
ddn context create-context axiom-$PROFILE
ddn context set localEnvFile .env.$PROFILE
ddn context set cloudEnvFile .env.cloud.$PROFILE
ddn context set project axiom-$PROFILE
```

#### Create your local supergraph

```
# Create a supergraph directory
mkdir -p supergraph-config/$PROFILE

# Copy your supergraph in to supergraph-config/$PROFILE/1-supergraph.yaml. Optional: use the following as a starter

cat <<EOF > supergraph-config/$PROFILE/1-supergraph.yaml
kind: Supergraph
version: v2
definition:
  subgraphs:
    - ../../globals/subgraph-basic.yaml
EOF
```

#### Set up profile subgraph(s)
Init a new subgraph for your profile
```
SUBGRAPH=commercial

# Create any subgraphs on the cloud project.
# auth and support may be omitted if shared subgraphs are not being used
ddn project subgraph create auth
ddn project subgraph create support
ddn project subgraph create globals
ddn project subgraph create $SUBGRAPH
```

Initialise the structure for your custom subgraphs in the repo
```
ddn subgraph init $SUBGRAPH --dir industry/$PROFILE/$SUBGRAPH
```

Add your subgraphs to the local supergraph
```
ddn subgraph add --subgraph ./industry/$PROFILE/$SUBGRAPH/subgraph.yaml --target-supergraph ./supergraph-config/$PROFILE/1-supergraph.yaml
ddn subgraph add --subgraph ./auth/subgraph.yaml --target-supergraph ./supergraph-config/$PROFILE/1-supergraph.yaml
ddn subgraph add --subgraph ./support/subgraph.yaml --target-supergraph ./supergraph-config/$PROFILE/1-supergraph.yaml
```

#### Seed environment files
```
cp .env.local .env.$PROFILE
cp .env.local .env.cloud.$PROFILE
```

#### Add your connectors
```
# Define your connector name
CONNECTOR=myconnector

# Run through connector logic
ddn connector init $CONNECTOR -i --subgraph industry/$PROFILE/$SUBGRAPH/subgraph.yaml
ddn connector introspect $CONNECTOR --subgraph industry/$PROFILE/$SUBGRAPH/subgraph.yaml
ddn model add $CONNECTOR "*" --subgraph industry/$PROFILE/$SUBGRAPH/subgraph.yaml
```

Add the region config to `industry/$PROFILE/$SUBGRAPH/connector/$CONNECTOR/connector.yaml`
```
  regionConfiguration:
    - mode: ReadWrite
      region: gcp-us-west2
```


#### Create a profile compose
```
cp compose.yaml compose-$PROFILE.yaml
```

N.B. Don't commit anything to the original compose.yaml


#### DDN Scripts
Create easy start scripts in `.hasura/context.yaml` for the following. Remember to **manually** change the `$PROFILE` for your profile name.

* build-$PROFILE
```
build-$PROFILE:
      bash: ddn supergraph build local --env-file .env.$PROFILE --env-file .env --supergraph supergraph-config/$PROFILE/1-supergraph.yaml
      powershell: ddn supergraph build local --env-file .env.$PROFILE --env-file .env --supergraph supergraph-config/$PROFILE/1-supergraph.yaml
```

* demo-$PROFILE
```
demo-$PROFILE:
      bash: ddn run docker-start-$PROFILE; HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f compose-$PROFILE.yaml --env-file .env.$PROFILE --env-file .env up --build --pull always -d
      powershell: $Env:HASURA_DDN_PAT = ddn auth print-pat; docker compose -f compose-$PROFILE.yaml --env-file .env.local --env-file .env up --build --pull always -d
```

### Test the build
Once the ddn scripts have been added in to `.hasura/context.yaml` test the build

```
ddn run build-$PROFILE
```

### Start the demo

```
ddn run demo-$PROFILE
```

### Deploying to the cloud
In order to deploy to cloud, it is mandatory for the data sources to be available on the open internet.

This can either be achieved by using cloud services, or by using the resources within the `infra` directory of this repo.

N.B. As Ansible deploys the main branch of the repo to servers, ensure the working demo profile above is committed before deploying with Ansible.

Once your data sources are available over the internet, update `.env.cloud.$PROFILE` with the internet-accessible database URLs.


TODO: Detailed instructions for running the deploy script

`./scripts/deploy/deploy.mjs --context axiom-$PROFILE -p $PROFILE -l DEBUG`