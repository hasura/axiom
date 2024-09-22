Axiom
=

Deploying new connectors
-

The simplest way to deploy new connectors is to run a new supergraph build in each region. It's important to ensure that the connector regions match the regions you're deploying to so this process takes all that into account.

This full rebuild deployment will run a 'build up' of the supergraph before running the standard metadata deploy for JWT/NoAuth

```
# Run the deploy script
./scripts/deploy/deploy.mjs

# Set the region (default points to axiom-test)
# ? Select a context region to set: default
# A complete rebuild will redeploy connectors. Do not use this if you have only altered metadata/hml files
# ? Do you want to perform a complete rebuild? yes

```

> [!IMPORTANT]  
> Following a connector update, it's important to update all the `.env` file details in Monday.com with the new locations/bearer tokens etc. These are not stored in the repo.

Deploying new metadata
-

Any metadata change that you've tested locally and against `axiom-test` can be rolled out in a couple of seconds with the deploy script. The deploy script will run a JWT deployment and a No-Auth deployment before applying No-Auth as the project API.

```
# Run the deploy script
./scripts/deploy/deploy.mjs

# ? Select a context region to set: default
# ? Do you want to perform a complete rebuild? no

```

Supported regions
-

The most up-to-date list is in `.hasura/context.yaml` and mirrored in the deploy script. We're currently deployed with axiom supergraphs in:
- au
- eu
- sg
- us-east
- us-west