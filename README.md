Axiom
=

Demo instructions
-
Everything related to the demo itself and content/data used within it is in the `.demo` directory.

Recreating this project
-
ddn create project --no-dir

PROJECT=\<project name here\>

ddn create subgraph support --project $PROJECT
ddn create subgraph customer --project $PROJECT
ddn create subgraph auth --project $PROJECT
ddn create subgraph network --project $PROJECT

ddn build supergraph-manifest --project $PROJECT


Adding new commands
-
SUBGRAPH=\<subgraph here\>
ddn add connector-manifest tsconnector --type cloud --hub-connector hasura/nodejs --project $PROJECT --subgraph $SUBGRAPH

ddn update data-connector-link my_ts --subgraph $SUBGRAPH

ddn add command --data-connector-link my_ts --name hello --subgraph $SUBGRAPH


## Additional commands
for i in `find . -type f -name connector.cloud.yaml`; do echo $i; ddn connector build create --connector $i; done


 ddn project subgraph create globals
 ddn supergraph build create --supergraph ./supergraph.cloud.yam