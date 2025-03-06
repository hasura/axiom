#!/bin/bash

# Verify context parameter
if [ -z "$1" ]; then
  echo "Error: Context parameter is required"
  echo "Usage: ddn run init -- <context>"
  echo "Example: ddn run init -- telco"
  exit 1
fi

CONTEXT=$1

SUPERGRAPH_PATH=$(ddn context get supergraph --context $CONTEXT --out json | jq -r .supergraph)

if [ -z "$SUPERGRAPH_PATH" ]; then
    echo "Error: Context '$CONTEXT' not found"
    echo "Available contexts: $(ddn context get-context --out json | jq -r '.contexts[]' | tr '\n' ' ')"
    exit 1
fi

HASURA_LOCAL_ENV_FILE="../hasura/.env.$CONTEXT"
HASURA_CLOUD_ENV_FILE="../hasura/.env.cloud.$CONTEXT"
DATA_ENV_FILE="../.data/$CONTEXT/.env"

# Copy .env templates if they do not exist
if [ ! -f "$DATA_ENV_FILE" ]; then
    echo "Creating environment file: $DATA_ENV_FILE"
    cp "../.data/.env.template" "$DATA_ENV_FILE"
else
    echo "Environment file already exists: $DATA_ENV_FILE"
fi

if [ ! -f "$HASURA_LOCAL_ENV_FILE" ]; then
    echo "Creating Hasura local environment file: $HASURA_LOCAL_ENV_FILE"
    cp "../hasura/.env.$CONTEXT.template" "$HASURA_LOCAL_ENV_FILE"
else
    echo "Hasura environment file already exists: $HASURA_LOCAL_ENV_FILE"
fi

if [ ! -f "$HASURA_CLOUD_ENV_FILE" ]; then
    echo "Creating Hasura cloud environment file: $HASURA_CLOUD_ENV_FILE"
    cp "../hasura/.env.$CONTEXT.template" "$HASURA_CLOUD_ENV_FILE"
else
    echo "Hasura cloud environment file already exists: $HASURA_CLOUD_ENV_FILE"
fi

echo "Generating PromptQL secret key for context: $CONTEXT"
ddn auth generate-promptql-secret-key --context $CONTEXT

echo "Initialization for context '$CONTEXT' completed successfully"