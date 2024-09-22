#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
set -o errexit
set -o pipefail
set -o nounset

# Determine the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# Initialize flags
OVERRIDE=false
REBUILD=false
CONTEXT="default"
LOGLEVEL="FATAL"

# Define paths and filenames relative to the script's directory
JWT_FILE="$SCRIPT_DIR/jwtauth.hml"
NOAUTH_FILE="$SCRIPT_DIR/noauth.hml"
DEST_DIR="$SCRIPT_DIR/../../globals"
DEST_FILE="auth-config.hml"

# Define allowed context values
ALLOWED_CONTEXTS=("default" "au" "eu" "us-east" "us-west" "sg")
ALLOWED_LOGLEVEL=("DEBUG" "WARN" "INFO" "ERROR" "FATAL")

# Validate the context value
if [[ ! " ${ALLOWED_CONTEXTS[*]} " =~ " ${CONTEXT} " ]]; then
    log "Invalid context: $CONTEXT. Allowed values are: ${ALLOWED_CONTEXTS[*]}."
    exit 1
fi

# Validate the log level
if [[ ! " ${ALLOWED_LOGLEVEL[*]} " =~ " ${LOGLEVEL} " ]]; then
    log "Invalid log level: $LOGLEVEL. Allowed values are: ${ALLOWED_LOGLEVEL[*]}."
    exit 1
fi

# Process arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --override)
            OVERRIDE=true
            log "Override flag detected. Branch and uncommitted changes checks will be bypassed."
            shift
            ;;
        --rebuild)
            REBUILD=true
            log "Rebuild flag detected. A complete rebuild will be performed."
            shift
            ;;
        *)
            # Handle positional parameters for context and log level
            if [[ " ${ALLOWED_CONTEXTS[*]} " =~ " $1 " ]]; then
                CONTEXT="$1"
                log "Context set to $CONTEXT"
            elif [[ " ${ALLOWED_LOGLEVEL[*]} " =~ " $1 " ]]; then
                LOGLEVEL="$1"
                log "Log level set to $LOGLEVEL"
            else
                log "Unknown option: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if the script is running on the 'main' branch
check_branch() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)

    if [[ "$current_branch" != "main" && "$OVERRIDE" == false ]]; then
        log "This script must be run on the 'main' branch. Current branch is '$current_branch'."
        exit 1
    fi

    log "Running on the 'main' branch or override flag is enabled."
}

# Check for uncommitted changes
check_uncommitted_changes() {
    if [[ -n "$(git status --porcelain)" && "$OVERRIDE" == false ]]; then
        log "Uncommitted changes detected. Please commit or stash your changes before running this script."
        exit 1
    else
        log "No uncommitted changes detected or override flag is enabled. Proceeding with script execution."
    fi
}

# Function to apply the build version
apply_build() {
    local build_version="$1"
    log "Applying supergraph build version $build_version"
    ddn supergraph build apply "$build_version" -c "$CONTEXT" --log-level "$LOGLEVEL"
}

# Function to move a file and run the command
run_command_with_tag() {
    local src_file="$1"
    local tag="$2"
    local supergraph="$3"
    local skip_no_build_connectors="${4:-false}"

    if [[ ! -f "$src_file" ]]; then
        log "Source file $src_file does not exist. Exiting."
        exit 1
    fi

    log "Copying $src_file to $DEST_DIR/$DEST_FILE"
    cp "$src_file" "$DEST_DIR/$DEST_FILE"

    local git_log
    git_log=$(git --no-pager log -1 --pretty=format:"%h [$tag] %s")

    # Determine whether to include --no-build-connectors or not
    local build_command="ddn supergraph build create -d \"$git_log\" -c \"$CONTEXT\" --out json --log-level \"$LOGLEVEL\" --supergraph \"$supergraph\""
    [[ "$skip_no_build_connectors" == false ]] && build_command+=" --no-build-connectors"

    local build_version
    build_version=$(eval "$build_command" | jq -r '.build_version')

    log "Build version $build_version created from $supergraph with $src_file"
    apply_build "$build_version"
}

# New rebuild function reusing run_command_with_tag
rebuild_supergraph() {
    log "Starting a complete rebuild of all supergraphs, including NoAuth."

    # Build each supergraph in the specified order
    local index=1
    for supergraph in "./supergraph-project.yaml" "./supergraph-domain.yaml" "./supergraph.yaml"; do
        run_command_with_tag "$NOAUTH_FILE" "NoAuth RB-$index" $supergraph true
        index=$((index + 1))
    done

    log "Rebuild completed successfully."
}

# Call the function to check the branch
check_branch

# Call the function to check for uncommitted changes
check_uncommitted_changes

# If the rebuild flag is set, perform the rebuild
if [[ "$REBUILD" == true ]]; then
    rebuild_supergraph
    exit 0
fi

# Run the command for JWT
run_command_with_tag "$JWT_FILE" "JWT" "./supergraph.yaml"

# Run the command for NoAuth
run_command_with_tag "$NOAUTH_FILE" "NoAuth" "./supergraph.yaml"

log "Script completed successfully."
