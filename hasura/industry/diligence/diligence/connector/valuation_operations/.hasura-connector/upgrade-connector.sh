#!/usr/bin/env bash
set -eu -o pipefail

connector_path="${1:-}"
target_connector_version="${2:-}"
npm_flags="${3:-}"

if [ -z "$connector_path" ]; then
  echo "Error: connector path must be passed as the first argument"
  exit 1
fi

if [ -z "$target_connector_version" ]; then
  echo "Error: target connector version must be passed as the second argument"
  exit 1
fi

if ! command -v npm &> /dev/null
then
  echo "npm could not be found on the PATH. Is Node.js installed?"
  exit 1
fi

if ! command -v jq &> /dev/null
then
  echo "jq could not be found on the PATH. Is jq installed?"
  exit 1
fi

cd "$connector_path"

set +e
existing_connector_version=$(jq '.dependencies["@hasura/ndc-lambda-sdk"]' -r package.json)
exit_status=$?
if [ $exit_status -ne 0 ]; then
  echo "Unable to read the @hasura/ndc-lambda-sdk version from your package.json"
  echo "Please manually upgrade the @hasura/ndc-lambda-sdk package in your package.json to version $target_connector_version"
  exit 1
fi

if [ $existing_connector_version = "null" ]; then
  # This is very strange, their package.json must have the SDK installed but doesn't
  # We'll roll with it and just install the package
  echo "Missing the @hasura/ndc-lambda-sdk package in your package.json. Installing version $target_connector_version"
else
  echo "Upgrading @hasura/ndc-lambda-sdk package from version $existing_connector_version to version $target_connector_version"
fi

npm install "@hasura/ndc-lambda-sdk@$target_connector_version" --save-exact --no-update-notifier $npm_flags
exit_status=$?
set -e

if [ $exit_status -ne 0 ]; then
  echo "Failed to upgrade @hasura/ndc-lambda-sdk package to version $target_connector_version"
  echo "Please manually upgrade the @hasura/ndc-lambda-sdk package in your package.json to version $target_connector_version"
  exit 1
fi

echo "Successfully upgraded @hasura/ndc-lambda-sdk package to version $target_connector_version"
