#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: Dataset parameter is required"
  echo "Usage: ddn run dataset-down -- <dataset>"
  echo "Example: ddn run dataset-down -- telco"
  exit 1
fi

# Stop compose services in .data/<dataset> directory
DATASET_DIR="../../.data/$1"
if [ -d "$DATASET_DIR" ]; then
  echo "Stopping services in $DATASET_DIR"
  docker compose -f "$DATASET_DIR/compose.yaml" down -v
else
  echo "Warning: Dataset directory $DATASET_DIR does not exist"
fi