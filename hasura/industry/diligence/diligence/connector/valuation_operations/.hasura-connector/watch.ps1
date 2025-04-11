$ErrorActionPreference = "Stop"

$scriptDir = Get-Location

& ./check-reqs.ps1

Push-Location $env:HASURA_PLUGIN_CONNECTOR_CONTEXT_PATH
try {
  $watchScript = & node "$PSScriptRoot\read-package-script.js" "watch"
  if ($LASTEXITCODE -ne 0) {
    exit 1
  }
  $env:PATH = "$($env:PATH);$($env:HASURA_PLUGIN_CONNECTOR_CONTEXT_PATH)\node_modules\.bin"
  Invoke-Expression "& $watchScript"
} finally {
  Pop-Location
}
