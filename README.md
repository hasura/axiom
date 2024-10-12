# Axiom
Hasura presales demo kit

## Quickstart


To get started, first copy template files into the correct locations:

```
cp .hasura/context.yaml.template .hasura/context.yaml
cp .env.template .env
cp .env.local.template .env.local
```

Next, create a build using these environment files:

```
# Create a basic supergraph
ddn run build-local-s1
```

Finally, set up the demo databases and start your supergraph:

```
# Initiate the demo databases and connect to them
ddn run docker-start-local
```

## Command Documentation
Each of the `ddn run` commands in `.hasura/context.yaml` corresponds to both a different way to build your supergraph and which source databases to use

| **Command**              | **Database Location** | **Description**                                                                                                   |
|--------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| `docker-start`           | Any             | Overrides standard message with customer `axiom` instructions|
| `docker-stop`            | Any             | Stops and removes all Docker containers and volumes related to the current setup|
| `build-local-s1`         | Local           | Builds a basic supergraph with one data domain and one data source|
| `build-local-s2`         | Local           | Builds a supergraph with one data domain, multiple data sources and global functions|
| `build-local-s3`         | Local           | Builds a full/complex supergraph with multiple data domains and data sources|
| `build-local-s4`         | Local           | Builds a complex supergraph and adds mutations|
| `docker-start-local`     | Local           | Initiates the telco demo datasources locally and starts the local Hasura DDN containers|
| `demo-telco`             | Telco           | Starts the containers for the telco demo data sources locally|
| `demo-healthcare`        | Healthcare      | Not yet implemented|
| `demo-banking`           | Banking         | Not yet implemented|


## Hasura Team Documentation

### Hasura Commands
| **Command**              | **Database Location** | **Description**                                                                                                   |
|--------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| `build-local-au-dbs`        | AU              | Hasura only: Builds the supergraph locally using the Australian database sources|
| `build-local-eu-dbs`        | EU              | Hasura only: Builds the supergraph locally using the European database sources|
| `build-local-sg-dbs`        | SG              | Hasura only: Builds the supergraph locally using the Singapore database sources|
| `build-local-us-east-dbs`   | US-East         | Hasura only: Builds the supergraph locally using the US-East database sources|
| `build-local-us-west-dbs`   | US-West         | Hasura only: Builds the supergraph locally using the US-West database sources|
| `docker-start-au`        | AU              | Hasura only: Starts DDN locally with Australian database sources|
| `docker-start-eu`        | EU              | Hasura only: Starts DDN locally with European database sources|
| `docker-start-sg`        | SG              | Hasura only: Starts DDN locally with Singapore database sources|
| `docker-start-us-east`   | US-East         | Hasura only: Starts DDN locally with US-East database sources|
| `docker-start-us-west`   | US-West         | Hasura only: Starts DDN locally with US-West database sources|


## Connectors

### Deleting connectors
Sometimes the number of connectors in cloud will surpass the max (100) and it will be required to clear out old connectors.

A handy script has been created to quickly and easily delete older connectors from cloud

> [!CAUTION]
> This is a destructive command and will prevent your cloud supergraph from working correctly. Use with caution!

```
# Delete the 20 oldest connector builds from the default environment in .hasura/context.yaml
./scripts/connector-delete.sh default 20
```

### Deploying new connectors

The simplest way to deploy new connectors is to run a new supergraph build in each region. It's important to ensure that the connector regions match the regions you're deploying to so this process takes all that into account.

This full rebuild deployment will run a 'build up' of 4 progressively more complex supergraph before running the standard metadata deploy for JWT/NoAuth

```
# Run the deploy script
./scripts/deploy/deploy.mjs

# Set the region (default points to axiom-test)
# ? Select a context region to set: default
# A complete rebuild will redeploy connectors. Do not use this if you have only altered metadata/hml files
# ? Do you want to perform a complete rebuild? yes

```

> [!IMPORTANT]  
> Hasura Note: Following a connector update, it's important to update all the `.env.cloud.*` file details in Monday.com with the new locations/bearer tokens etc. These are not stored in the repo for obvious reasons.

### Deploying new metadata

Any metadata change that you've tested locally and against `axiom-test` can be rolled out in a couple of seconds with the deploy script. The deploy script will run a JWT deployment and a No-Auth deployment before applying No-Auth as the project API.

```
# Run the deploy script
./scripts/deploy/deploy.mjs

# ? Select a context region to set: default
# ? Do you want to perform a complete rebuild? no

```

## Supported regions

The most up-to-date list is in `.hasura/context.yaml` and mirrored in the deploy script. We're currently deployed with axiom supergraphs in:
- Australia
- Europe
- Singapore
- US East
- US West