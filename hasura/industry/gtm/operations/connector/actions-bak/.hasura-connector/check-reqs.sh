#!/usr/bin/env bash
set -eu -o pipefail

minimum_node_version="20"

if ! command -v node &> /dev/null
then
  echo "node could not be found on the PATH. Please install Node.js v$minimum_node_version+."
  exit 1
fi

node_version=$(node --version)
if [[ "$node_version" =~ ^v([[:digit:]]+)\. ]]; then
  major_version="${BASH_REMATCH[1]}"
  if [[ $major_version -lt $minimum_node_version ]]; then
    echo "Detected Node.js version $node_version on the PATH. The minimum required version is v$minimum_node_version."
    exit 1
  fi
else
  echo "no match"
fi

cd $HASURA_PLUGIN_CONNECTOR_CONTEXT_PATH

if [ ! -d "node_modules" ]
then
  echo "node_modules directory not found, please ensure you have run 'npm install'."
  exit 1
fi
