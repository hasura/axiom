#!/bin/bash

# Verify context parameter
if [ -z "$1" ]; then
  echo "Error: Context parameter is required"
  echo "Usage: ddn run build -- <context>"
  echo "Example: ddn run build -- telco"
  exit 1
fi

CONTEXT=$1

SUPERGRAPH_PATH=$(ddn context get supergraph --context $CONTEXT --out json | jq -r .supergraph)

if [ -z "$SUPERGRAPH_PATH" ]; then
    echo "Error: Context '$CONTEXT' not found"
    echo "Available contexts: $(ddn context get-context --out json | jq -r '.contexts[]' | tr '\n' ' ')"
    exit 1
fi

echo $SUPERGRAPH_PATH
ddn supergraph build local --context $CONTEXT
