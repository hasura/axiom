#!/bin/bash

# Verify context parameter
if [ -z "$1" ]; then
  echo "Error: Context parameter is required"
  echo "Usage: ddn run docker-start -- <context>"
  echo "Example: ddn run docker-start -- telco"
  exit 1
fi

CONTEXT=$1

# Verify that the context data directory exists
if [ ! -d "../.data/$CONTEXT" ]; then
  echo "Error: Data directory for context '$CONTEXT' not found at '../.data/$CONTEXT'"
  echo "Available data directories: $(find ../.data -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | tr '\n' ' ')"
  exit 1
fi

# Set dataset environment variable
export DATASET=$CONTEXT

# Start docker containers
docker compose -f ../.data/$CONTEXT/compose.yaml --env-file ../.data/$CONTEXT/.env up --build --pull always -d