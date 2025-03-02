#!/bin/bash

# Verify context parameter
if [ -z "$1" ]; then
  echo "Error: Context parameter is required"
  echo "Usage: ddn run demo -- <context>"
  echo "Example: ddn run demo -- telco"
  exit 1
fi

CONTEXT=$1

# Get environment file
ENV_FILE=$(ddn context get localEnvFile --context $CONTEXT --out json | jq -r .localEnvFile)

if [ -z "$ENV_FILE" ]; then
  echo "Error: Context '$CONTEXT' not found"
  echo "Available contexts: $(ddn context get-context --out json | jq -r '.contexts[]' | tr '\n' ' ')"
  exit 1
fi

# Build the supergraph and start docker first
../scripts/ddn-run/build.sh "$CONTEXT"
../scripts/ddn-run/docker-start.sh "$CONTEXT"

# Set up PAT and run docker compose with appropriate files
HASURA_DDN_PAT=$(ddn auth print-pat)
docker compose -f compose-$CONTEXT.yaml --env-file "../hasura/$ENV_FILE" up --build --pull always -d