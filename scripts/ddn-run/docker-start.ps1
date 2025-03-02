# Verify context parameter
if (-not $args[0]) {
    Write-Host "Error: Context parameter is required"
    Write-Host "Usage: ddn run docker-start -- <context>"
    Write-Host "Example: ddn run docker-start -- telco"
    exit 1
}

$CONTEXT = $args[0]
$DataDir = "../.data/$CONTEXT"

# Verify that the context data directory exists
if (-not (Test-Path -Path $DataDir -PathType Container)) {
    Write-Host "Error: Data directory for context '$CONTEXT' not found at '$DataDir'"
    
    $AvailableDirs = Get-ChildItem -Path "../.data" -Directory | ForEach-Object { $_.Name }
    Write-Host "Available data directories: $AvailableDirs"
    exit 1
}

# Set dataset environment variable
$env:DATASET = $CONTEXT

# Start docker containers
docker compose -f "$DataDir/compose.yaml" --env-file "$DataDir/.env" up --build --pull always -d
