Axiom
=

Deploying new connectors
-

The simplest way to deploy new connectors is to run a new supergraph build in each region. It's important to ensure that the connector regions match the regions you're deploying to so this process takes a couple of steps

```
# Change region accordingly
node scripts/region-switcher/region-switcher.mjs

# Change context accordingly
ddn context set-current-context $REGION

# Build the supergraph
git_log=$(git --no-pager log -1 --pretty=format:"%h [NDC] %s")
ddn supergraph build create -d $git_log
```

> [!IMPORTANT]  
> Following a connector update, it's important to update all the `.env` file details in Monday.com with the new locations/bearer tokens etc. These are not stored in the repo.

Deploying new metadata
-

This one is a lot easier. Any metadata change that you've tested locally and against `axiom-test` can be rolled out in a couple of seconds with the deploy script. The deploy script will run a JWT deployment and a No-Auth deployment before applying No-Auth as the project API.

```
./scripts/deploy/deploy.sh $REGION
```

Supported regions
-

The most up-to-date list is in `.hasura/context.yaml` and mirrored in the deploy script. We're currently deployed with axiom supergraphs in:
- au
- eu
- us-east
- us-west