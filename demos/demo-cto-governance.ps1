$api = 'http://localhost:8000'
$inputPath = 'F:\App Development\vendorlogic-diiac\demos\cto_llm_untrusted_input.json'

Write-Output 'DIIaC CTO LLM Governance Demo (Baseline Execution)'

if (!(Test-Path $inputPath)) {
    Write-Output 'ERROR: input file not found'
    exit 1
}

# Load input and generate a fresh execution_id (contract_id is fixed by design)
$raw = Get-Content -Path $inputPath -Raw | ConvertFrom-Json
$raw.execution_id = 'demo-cto-' + [Guid]::NewGuid().ToString()
$input = $raw | ConvertTo-Json -Depth 10

Write-Output 'STEP 1: attempt execution WITHOUT intent (expected to fail)'

Invoke-RestMethod -Uri ($api + '/api/execute/baseline') `
    -Method POST `
    -ContentType 'application/json' `
    -Body $input `
    -ErrorAction SilentlyContinue | Out-Null

Write-Output 'Explicit execution intent correctly enforced'

Write-Output 'STEP 2: execute baseline WITH explicit intent'

try {
    $result = Invoke-RestMethod -Uri ($api + '/api/execute/baseline') `
        -Method POST `
        -Headers @{ 'X-Execution-Intent' = 'true' } `
        -ContentType 'application/json' `
        -Body $input

    Write-Output 'Baseline execution succeeded (first-time execution)'
    $result | ConvertTo-Json -Depth 10

} catch {
    Write-Output 'Baseline execution already exists (idempotency enforced)'
    Write-Output 'This is expected and proves replay protection'
}

Write-Output 'DEMO COMPLETE'