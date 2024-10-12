#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Enable debug mode if needed for troubleshooting.
# set -x

# Function to print usage information
usage() {
  echo "Usage: $0 [configuration_name] [number_of_deletes|all]"
  echo "  configuration_name: Optional. The configuration name to use (default is 'default')."
  echo "  number_of_deletes: Number of oldest connector builds to delete, or 'all' to delete all."
  exit 1
}

# Check for required dependencies
if ! command -v jq &>/dev/null; then
  echo "Error: 'jq' is required but not installed. Please install 'jq' and try again."
  exit 1
fi

# Get the configuration name or use 'default' if not provided.
config_name="${1:-default}"

# Get the number of connectors to delete or "all" to delete everything.
delete_count="${2}"

# Check if the delete_count is provided.
if [[ -z "$delete_count" ]]; then
  echo "Error: You must specify the number of connector builds to delete or use 'all'."
  usage
fi

# Validate the delete_count argument.
if [[ "$delete_count" != "all" && ! "$delete_count" =~ ^[0-9]+$ ]]; then
  echo "Error: Please provide a positive integer for the number of connector builds to delete or use 'all'."
  usage
fi

# Get all connector build IDs, sorted by creation time (oldest last).
connector_ids=$(ddn connector build get -c "$config_name" --out json | jq -r '.[].connectorBuildID')

# Check if there are any connector IDs to delete.
if [[ -z "$connector_ids" ]]; then
  echo "No connector builds found for configuration '$config_name'."
  exit 0
fi

# Select connector IDs to delete based on the delete_count.
if [[ "$delete_count" == "all" ]]; then
  echo "Deleting all connector builds for configuration '$config_name'..."
  selected_ids="$connector_ids"
else
  # Use 'tail' to get the specified number of oldest IDs.
  selected_ids=$(echo "$connector_ids" | tail -n "$delete_count")
fi

# Loop through each selected ID and delete it.
for id in $selected_ids; do
  echo "Deleting connector build ID: $id"
  ddn connector build delete "$id" &
done

# Wait for all background jobs to complete.
wait
echo "Selected connector builds have been deleted successfully."

