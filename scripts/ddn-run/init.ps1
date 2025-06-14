param(
    [Parameter(Mandatory=$true)]
    [string]$Context
)

$SupergraphPath = (ddn context get supergraph --context $Context --out json | ConvertFrom-Json).supergraph

if ([string]::IsNullOrEmpty($SupergraphPath)) {
    Write-Error "Error: Context '$Context' not found"
    $AvailableContexts = (ddn context get-context --out json | ConvertFrom-Json).contexts -join ", "
    Write-Host "Available contexts: $AvailableContexts"
    exit 1
}

$HasuraLocalEnvFile = "../hasura/.env.$Context"
$HasuraCloudEnvFile = "../hasura/.env.cloud.$Context"
$DataEnvFile = "../.data/$Context/.env"

# Copy .env templates if they do not exist
if (-not (Test-Path $DataEnvFile)) {
    Write-Host "Creating environment file: $DataEnvFile"
    Copy-Item "../.data/.env.template" -Destination $DataEnvFile
} else {
    Write-Host "Environment file already exists: $DataEnvFile"
}

if (-not (Test-Path $HasuraLocalEnvFile)) {
    Write-Host "Creating local environment file: $HasuraLocalEnvFile"
    Copy-Item "../hasura/.env.$Context.template" -Destination $HasuraLocalEnvFile
} else {
    Write-Host "Environment file already exists: $HasuraLocalEnvFile"
}

if (-not (Test-Path $HasuraCloudEnvFile)) {
    Write-Host "Creating cloud environment file: $HasuraCloudEnvFile"
    Copy-Item "../hasura/.env.$Context.template" -Destination $HasuraCloudEnvFile
} else {
    Write-Host "Hasura cloud environment file already exists: $HasuraCloudEnvFile"
}

Write-Host "Generating PromptQL secret key for context: $Context"
ddn auth generate-promptql-secret-key --context $Context

Write-Host "Initialization for context '$Context' completed successfully"