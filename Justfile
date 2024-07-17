start-ddn:
    HASURA_DDN_PAT=$(ddn auth print-pat) sudo docker compose up --build --watch
start-connector-nodejs:
    cd ./customer/connector/nodejs && npx dotenv -e .env.local -- npm run watch
start-connector-ts:
    cd ./support/connector/tsconnector && npx dotenv -e .env.local -- npm run watch
build-local:
    ddn supergraph build local \
    --output-dir ./engine \
    --supergraph ./supergraph.local.yaml \
    --subgraph-env-file auth:./auth/.env.local.auth \
    --subgraph-env-file customer:./customer/.env.local.customer \
    --subgraph-env-file network:./network/.env.local.network \
    --subgraph-env-file support:./support/.env.local.support

start-dbs:
    docker-compose -f ./.demo/docker-compose.yml up -d