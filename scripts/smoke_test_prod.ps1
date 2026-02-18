Write-Host "Meta Prompt Generator - Production Smoke Test"

$baseUrl = "http://localhost:8000"

function Assert-Ok {
    param (
        [Parameter(Mandatory=$true)] $Response,
        [Parameter(Mandatory=$true)] [string] $Name
    )

    if ($Response.StatusCode -ne 200) {
        Write-Error "$Name failed with status $($Response.StatusCode)"
        exit 1
    }

    Write-Host "$Name OK"
}

# Roles endpoint
$roles = Invoke-WebRequest `
    -Uri "$baseUrl/roles" `
    -Method GET `
    -UseBasicParsing

Assert-Ok -Response $roles -Name "Roles endpoint"

# Schemas endpoint
$schemas = Invoke-WebRequest `
    -Uri "$baseUrl/schemas" `
    -Method GET `
    -UseBasicParsing

Assert-Ok -Response $schemas -Name "Schemas endpoint"

# Generate endpoint
$body = @{
    role   = "Enterprise Architect"
    task   = "Design a target state architecture"
    schema = "EA_SOLUTION"
} | ConvertTo-Json -Depth 5

$generate = Invoke-WebRequest `
    -Uri "$baseUrl/generate" `
    -Method POST `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body $body `
    -UseBasicParsing

Assert-Ok -Response $generate -Name "Generate endpoint"

Write-Host "Production smoke test PASSED"
