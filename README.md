# Axiom
Hasura presales demo kit

## Quickstart (Telco)

To get started, first copy template files into the correct locations:

```
cp hasura/.env.template.telco hasura/.env.telco
cp .data/.env.template .data/.env
cd hasura
ddn run demo-telco
```

## Command Documentation
Each of the `ddn run` commands in `hasura/.hasura/context.yaml` corresponds to both a different way to build your supergraph and which source databases to use

| **Command**              | **Database Location** | **Description**                                                                                                   |
|--------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| `docker-start-telco`     | Telco           | Starts the containers for the telco demo data sources locally|
| `docker-stop`            | Any             | Stops and removes all Docker containers and volumes related to the current setup|
| `demo-telco`             | Telco           | Starts the containers for the telco demo data sources locally|


## Deployment

### Deploying new metadata

Any metadata change that has been tested locally and against CI/CD in a pull request may be rolled out in a couple of seconds with the [deploy script](./scripts/deploy/). 

The deploy script will run a JWT deployment and a No-Auth deployment before applying No-Auth as the project API.

Full documentation may be found in the deploy [README](./scripts/deploy/README.md)

```
# Run the deploy script
node ./scripts/deploy/deploy.mjs --context axiom-dev --profile telco --no-build-connectors
```

### Deploying new connectors
New connectors should be deployed after connector configuration/schema is updated.

The simplest way to deploy new connectors is to run a new supergraph build in each region. It's important to ensure that the connector regions match the regions you're deploying.

```
# Deploy new connectors
node ./scripts/deploy/deploy.mjs --context axiom-dev --profile telco --gcp-region gcp-us-west2
```

> [!IMPORTANT]  
> Hasura Note: Following a connector update, it's important to update all the `.env.cloud.*` file details in Confluence. These are not stored in the repo for obvious reasons.

## Connectors

### Deleting connectors
Sometimes the number of connectors in cloud will surpass the max (100) and it will be required to clear out old connectors.

A handy script has been created to quickly and easily delete older connectors from cloud

> [!CAUTION]
> This is a destructive command and will prevent your cloud supergraph from working correctly. Use with caution!

```
# Delete the 20 oldest connector builds from the default environment in .hasura/context.yaml
./scripts/connector-delete.sh axiom-dev 20
```