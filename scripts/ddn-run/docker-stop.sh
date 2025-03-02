#!/bin/bash

# Stop all compose services from compose files in root directory
for file in ../hasura/compose*.yaml; do
  if [ -f "$file" ]; then
    echo "Stopping services in $file"
    docker compose -f "$file" down -v
  fi
done

# Stop all compose services from .data directory
find ../.data -type f -name "compose.yaml" | while read file; do
  echo "Stopping services in $file"
  docker compose -f "$file" down -v
done