#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Log function for better readability and maintenance
log() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') - $*"
}

# Error handler to capture any issues and exit gracefully
error_exit() {
  log "ERROR: $1"
  exit 1
}

# Validate that DATASET is set
[ -z "$DATASET" ] && error_exit "DATASET environment variable is not set."

# Define paths relative to the script's location
COMMON_DIR="$SCRIPT_DIR/common"
BUILD_DIR="$SCRIPT_DIR/build"
DATASET_DIR="$SCRIPT_DIR/$DATASET"

# Ensure build directories exist
log "Ensuring build directories exist..."
mkdir -p "$BUILD_DIR/postgres" "$BUILD_DIR/mongodb" || error_exit "Failed to create build directories."

# Function to copy files from source to destination
copy_files() {
  local src=$1
  local dest=$2
  local label=$3

  if [ -d "$src" ]; then
    log "Copying $label files from $src to $dest..."
    cp -R "$src"/* "$dest" || error_exit "Failed to copy files from $src to $dest."
  else
    log "WARNING: Directory $src not found. Skipping $label files."
  fi
}

# Copy global scripts into build directory
log "Processing global scripts..."
copy_files "$COMMON_DIR/postgres" "$BUILD_DIR/postgres" "Postgres"
copy_files "$COMMON_DIR/mongodb" "$BUILD_DIR/mongodb" "MongoDB"

# Copy dataset-specific scripts into build directory
log "Processing dataset ($DATASET) scripts..."
copy_files "$DATASET_DIR/postgres" "$BUILD_DIR/postgres" "Postgres"
copy_files "$DATASET_DIR/mongodb" "$BUILD_DIR/mongodb" "MongoDB"

log "File copying completed successfully."