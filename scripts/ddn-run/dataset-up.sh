#!/bin/bash

# Verify context parameter
if [ -z "$1" ]; then
  echo "Error: Dataset parameter is required"
  echo "Usage: ddn run dataset-up -- <dataset>"
  echo "Example: ddn run dataset-up -- telco"
  exit 1
fi

DATASET=$1

# Verify that the context data directory exists
if [ ! -d "../../.data/$DATASET" ]; then
  echo "Error: Data directory for context '$DATASET' not found at '../../.data/$DATASET'"
  echo "Available data directories: $(find ../../.data -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | tr '\n' ' ')"
  exit 1
fi

# Set dataset environment variable
export DATASET=$DATASET

# Start docker containers
docker compose -f ../../.data/$DATASET/compose.yaml --env-file ../../.data/$DATASET/.env up --build --pull always -d