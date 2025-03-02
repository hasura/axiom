# Verify context parameter
if (-not $args[0]) {
    Write-Host "Error: Context parameter is required"
    Write-Host "Usage: ddn run demo -- <context>"
    Write-Host "Example: ddn run demo -- telco"
    exit 1
}

$CONTEXT = $args[0]

# Get environment file
$ENV_FILE = ddn context get localEnvFile --context $CONTEXT --out json | ConvertFrom-Json | Select-Object -ExpandProperty localEnvFile

if (-not $ENV_FILE) {
    Write-Host "Error: Context '$CONTEXT' not found"
    $contexts = ddn context get-context --out json | ConvertFrom-Json | Select-Object -ExpandProperty contexts -ErrorAction SilentlyContinue
    Write-Host "Available contexts: $contexts"
    exit 1
}

# Build the supergraph and start docker first
& "../scripts/ddn-run/build.ps1" $CONTEXT
& "../scripts/ddn-run/docker-start.ps1" $CONTEXT

# Set up PAT and run docker compose with appropriate files
$HASURA_DDN_PAT = ddn auth print-pat
docker compose -f "compose-$CONTEXT.yaml" --env-file "../hasura/$ENV_FILE" up --build --pull always -d
