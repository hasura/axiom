# Verify dataset parameter
if (-not $args[0]) {
    Write-Host "Error: Dataset parameter is required"
    Write-Host "Usage: ddn run dataset-down -- <dataset>"
    Write-Host "Example: ddn run dataset-down -- telco"
    exit 1
}

$DATASET = $args[0]
$DatasetDir = "../../.data/$DATASET"

# Stop compose services in .data/<dataset> directory
if (Test-Path -Path $DatasetDir -PathType Container) {
    Write-Host "Stopping services in $DatasetDir"
    docker compose -f "$DatasetDir/compose.yaml" down -v
} else {
    Write-Host "Warning: Dataset directory $DatasetDir does not exist"
}
