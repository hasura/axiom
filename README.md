Axiom
=

Demo instructions
-
Everything related to the demo itself and content/data used within it is in the `.demo` directory.

Recreating this project
-
ddn create project --no-dir

ddn context set project <project-name>

PROJECT=\<project name here\>

ddn project subgraph create support --project $PROJECT
ddn project subgraph create customer --project $PROJECT
ddn project subgraph create auth --project $PROJECT
ddn project subgraph create network --project $PROJECT

// Add your db credentials for postgres, clickhouse, mongo.
// NB you might have to encode your password per https://github.com/hasura/v3-docs/blob/fcca076d30feb5b5fc527eb568bba88a67072dfa/docs/connectors/postgresql/index.mdx#L141

for i in `find . -type f -name connector.cloud.yaml`; do echo $i; ddn connector build create --connector $i; done

// Replace the build URLs in .env.cloud.subgraph

ddn supergraph build create --supergraph ./supergraph.cloud.yaml


Adding new commands
-
SUBGRAPH=\<subgraph here\>
ddn add connector-manifest tsconnector --type cloud --hub-connector hasura/nodejs --project $PROJECT --subgraph $SUBGRAPH

ddn update data-connector-link my_ts --subgraph $SUBGRAPH

ddn add command --data-connector-link my_ts --name hello --subgraph $SUBGRAPH


