#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Enable error handling to catch errors in functions and subshells
set -o errexit
set -o pipefail
set -o nounset

# Log function for consistent logging
log() {
    local msg="$1"
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $msg"
}

# Error handling function
handle_error() {
    log "Error on line $1"
    exit 1
}
trap 'handle_error $LINENO' ERR

# Define paths and filenames
JWT_FILE="jwtauth.hml"
NOAUTH_FILE="noauth.hml"
DEST_DIR="../../globals"
DEST_FILE="auth-config.hml"

# Define allowed context values
ALLOWED_CONTEXTS=("default" "au" "eu" "us-east" "us-west")

# Set context to 'default' if not provided as an argument
CONTEXT="${1:-default}"

# Validate the context value
if [[ ! " ${ALLOWED_CONTEXTS[*]} " =~ " ${CONTEXT} " ]]; then
    log "Invalid context: $CONTEXT. Allowed values are: ${ALLOWED_CONTEXTS[*]}."
    exit 1
fi

# Function to move a file and run the command
run_command_with_tag() {
    local src_file="$1"
    local tag="$2"

    # Check if source file exists
    if [[ ! -f "$src_file" ]]; then
        log "Source file $src_file does not exist. Exiting."
        exit 1
    fi

    # Move the source file to the destination with the name auth-config.hml
    log "Moving $src_file to $DEST_DIR/$DEST_FILE"
    cp "$src_file" "$DEST_DIR/$DEST_FILE"

    # Get the latest git commit short hash and message
    local git_log
    git_log=$(git --no-pager log -1 --pretty=format:"%h [$tag] %s")

    # Run the supergraph build command with the appropriate tag
    local build_version
    build_version=$(ddn supergraph build create --no-build-connectors -d "$git_log" -c "$CONTEXT" --out json | jq -r '.build_version')

    log "Running supergraph build apply with build version $build_version"
    ddn supergraph build apply "$build_version" -c "$CONTEXT"
}

# Run the command for JWT
run_command_with_tag "$JWT_FILE" "JWT"

# Run the command for NoAuth
run_command_with_tag "$NOAUTH_FILE" "NoAuth"

log "Script completed successfully."

