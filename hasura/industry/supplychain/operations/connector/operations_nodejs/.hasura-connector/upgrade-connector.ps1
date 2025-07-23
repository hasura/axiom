param(
    [Parameter(Mandatory=$true)]
    [string]$connector_path,

    [Parameter(Mandatory=$true)]
    [string]$target_connector_version,

    [Parameter(Mandatory=$false)]
    [string[]]$npm_flags = @()
)

if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
  Write-Host "npm could not be found. Is Node.js installed?"
  exit 1
}

Push-Location $connector_path -ErrorAction Stop
try {
    try {
        $packageJson = Get-Content 'package.json' -Raw | ConvertFrom-Json
        $existing_connector_version = $packageJson.dependencies.'@hasura/ndc-lambda-sdk'
    } catch {
        Write-Host "Unable to read the @hasura/ndc-lambda-sdk version from your package.json"
        Write-Host "Please manually upgrade the @hasura/ndc-lambda-sdk package in your package.json to version $target_connector_version"
        exit 1
    }

    if (-not $existing_connector_version) {
        # This is very strange, their package.json must have the SDK installed but doesn't
        # We'll roll with it and just install the package
        Write-Host "Missing the @hasura/ndc-lambda-sdk package in your package.json. Installing version $target_connector_version"
    } else {
        Write-Host "Upgrading @hasura/ndc-lambda-sdk package from version $existing_connector_version to version $target_connector_version"
    }

    try {
        & npm install "@hasura/ndc-lambda-sdk@$target_connector_version" --save-exact --no-update-notifier @npm_flags
        $exit_status = $LASTEXITCODE
    } catch {
        $exit_status = 1
    }

    if ($exit_status -ne 0) {
        Write-Host "Failed to upgrade @hasura/ndc-lambda-sdk package to version $target_connector_version"
        Write-Host "Please manually upgrade the @hasura/ndc-lambda-sdk package in your package.json to version $target_connector_version"
        exit 1
    }

    Write-Host "Successfully upgraded @hasura/ndc-lambda-sdk package to version $target_connector_version"
} finally {
    Pop-Location
}
