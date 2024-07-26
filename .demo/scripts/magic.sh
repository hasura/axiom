#!/bin/bash

SUBGRAPH=my_subgraph
CONNECTOR=my_mongo
UPPER_SUBGRAPH=$(echo "${SUBGRAPH}" | tr '[a-z]' '[A-Z]')
UPPER_CONNECTOR=$(echo "${CONNECTOR}" | tr '[a-z]' '[A-Z]')

echo "${UPPER_SUBGRAPH}_${UPPER_CONNECTOR}_READ_URL=http://local.hasura.dev:8082
${UPPER_SUBGRAPH}_${UPPER_CONNECTOR}_WRITE_URL=http://local.hasura.dev:8082"

ddn connector init $CONNECTOR --subgraph $SUBGRAPH --hub-connector hasura/mongodb

echo '\nMONGODB_DATABASE_URI="mongodb+srv://sedemo:0indQrBgrjxDYE6H@sedemocluster.zcxlgsy.mongodb.net/sample_analytics"' >> ./$SUBGRAPH/connector/$CONNECTOR/.env.local

ddn connector introspect --connector $SUBGRAPH/connector/$CONNECTOR/connector.yaml

ddn connector-link add $CONNECTOR

cp $CONNECTOR-docker-compose.hasura.yaml ./docker-compose.hasura.yaml

cp 8082-docker-compose.$CONNECTOR.yaml ./$SUBGRAPH/connector/$CONNECTOR/

echo "${UPPER_SUBGRAPH}_${UPPER_CONNECTOR}_READ_URL=http://local.hasura.dev:8082
${UPPER_SUBGRAPH}_${UPPER_CONNECTOR}_WRITE_URL=http://local.hasura.dev:8082" >>./$SUBGRAPH/.env.$SUBGRAPH

HASURA_DDN_PAT=$(ddn auth print-pat) docker compose -f docker-compose.hasura.yaml watch &

#ddn connector-link update $CONNECTOR --subgraph $SUBGRAPH --add-all-resources

ddn model add --connector-link $CONNECTOR --name transactions

ddn supergraph build local --output-dir ./engine
