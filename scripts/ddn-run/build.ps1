# Verify context parameter
if (-not $args[0]) {
    Write-Host "Error: Context parameter is required"
    Write-Host "Usage: ddn run build -- <context>"
    Write-Host "Example: ddn run build -- telco"
    exit 1
}

$CONTEXT = $args[0]

# Get Supergraph path
$SUPERGRAPH_PATH = ddn context get supergraph --context $CONTEXT --out json | ConvertFrom-Json | Select-Object -ExpandProperty supergraph

if (-not $SUPERGRAPH_PATH) {
    Write-Host "Error: Context '$CONTEXT' not found"
    $contexts = ddn context get-context --out json | ConvertFrom-Json | Select-Object -ExpandProperty contexts -ErrorAction SilentlyContinue
    Write-Host "Available contexts: $contexts"
    exit 1
}

Write-Host $SUPERGRAPH_PATH
ddn supergraph build local --context $CONTEXT
