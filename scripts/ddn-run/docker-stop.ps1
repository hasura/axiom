# Stop all compose services from compose files in root directory
$ComposeFiles = Get-ChildItem -Path "../hasura" -Filter "compose*.yaml" -File
foreach ($file in $ComposeFiles) {
    Write-Host "Stopping services in $($file.FullName)"
    docker compose -f $file.FullName down -v
}

# Stop all compose services from .data directory
$DataComposeFiles = Get-ChildItem -Path "../.data" -Recurse -Filter "compose.yaml" -File
foreach ($file in $DataComposeFiles) {
    Write-Host "Stopping services in $($file.FullName)"
    docker compose -f $file.FullName down -v
}
