#!/usr/bin/env bash
set -eu -o pipefail

script_dir=$(pwd)

./check-reqs.sh

cd $HASURA_PLUGIN_CONNECTOR_CONTEXT_PATH
watch_script=$(node "$script_dir/read-package-script.js" "watch")
PATH="$PATH:$(pwd)/node_modules/.bin" exec $watch_script
