# Verify context parameter
if (-not $args[0]) {
    Write-Host "Error: Dataset parameter is required"
    Write-Host "Usage: ddn run dataset-up -- <dataset>"
    Write-Host "Example: ddn run dataset-up -- telco"
    exit 1
}

$DATASET = $args[0]
$DataDir = "../../.data/$DATASET"

# Verify that the context data directory exists
if (-not (Test-Path -Path $DataDir -PathType Container)) {
    Write-Host "Error: Data directory for context '$DATASET' not found at '$DataDir'"
    
    $AvailableDirs = Get-ChildItem -Path "../../.data" -Directory | ForEach-Object { $_.Name }
    Write-Host "Available data directories: $AvailableDirs"
    exit 1
}

# Set dataset environment variable
$env:DATASET = $DATASET

# Start docker containers
docker compose -f "$DataDir/compose.yaml" --env-file "$DataDir/.env" up --build --pull always -d
