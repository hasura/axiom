# Axiom Scripts

## Demo Scripts
These scripts are used as part of regular demo operations.

### JWT
The [JWT script](./jwt/) loads secrets from `.env` files automatically to generate tokens.

These tokens may be used to demonstrate RBAC/ABAC on secure builds.

### Connector Keepalive
Loaded onto the cron server to ping each demo instance and keep connectors/lambdas from spinning down.

This [script](./connector-keepalive.sh) ensures that demos are responsive and queries do run into cold starts.

## Deployment + Maintenance

### Deploy
The most comprehensive script, [deploy](./deploy/) allows deployment of any demo profile to any project with a large array of configurable options

### Connector Delete
A soft limit of 100 connectors exists on DDN and this [script](./connector-delete.sh) deletes older connectors to make room for new deployments

## Other

### Encode Password
Database passwords with special characters sometimes need to have those passwords encoded within the `.env` files. This [script](./encode-password.js) provides a simple method for password encoding.

## Deprecated

### Region Switcher
Previously, GCP regions were switched manually prior to deployment. Now, the deploy script manages this on the fly and this [script](./region-switcher/) is no longer required.