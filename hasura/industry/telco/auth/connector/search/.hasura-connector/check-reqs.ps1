$ErrorActionPreference = "Stop"

$minimumNodeVersion = 20

if (-not (Get-Command "node" -ErrorAction SilentlyContinue)) {
  Write-Host "node could not be found. Please install NodeJS v$minimumNodeVersion+."
  exit 1
}

$nodeVersion = & node --version
if ($nodeVersion -match "^v(\d+)\.") {
  $majorVersion = $Matches[1]
  if ($majorVersion -lt $minimumNodeVersion) {
    Write-Host "Detected Node.js version $nodeVersion on the PATH. The minimum required version is v$minimumNodeVersion."
    exit 1
  }
}

Push-Location $env:HASURA_PLUGIN_CONNECTOR_CONTEXT_PATH
try {
  if ((Test-Path "./node_modules") -eq $false) {
    Write-Host "node_modules not found, please ensure you have run 'npm install'."
    exit 1
  }
} finally {
  Pop-Location
}
