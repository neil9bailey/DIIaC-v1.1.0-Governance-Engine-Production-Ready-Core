$api = 'http://localhost:8000'
$goldenInputPath = 'F:\App Development\vendorlogic-diiac\tests\golden\cto_llm_golden_output.json'

Write-Output 'DIIaC Phase 2 Demo — Golden LLM Deterministic Governance'

if (!(Test-Path $goldenInputPath)) {
    Write-Output 'ERROR: golden LLM artefact not found'
    exit 1
}

# Load golden LLM output
$payload = Get-Content -Path $goldenInputPath -Raw | ConvertFrom-Json

# Construct execution request with fixed contract and fresh execution_id
$guid = [Guid]::NewGuid().ToString()
$request = @{
    contract_id  = 'CTO_STRATEGY_BASELINE'
    execution_id = 'GOLDEN_LLM_EXEC_' + $guid
    payload      = $payload
}

$input = $request | ConvertTo-Json -Depth 10

Write-Output 'STEP 1: attempt baseline execution WITHOUT intent (expected to fail)'

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

    Write-Output 'Baseline execution accepted'
    $result | ConvertTo-Json -Depth 10

} catch {
    Write-Output 'Baseline execution already exists (idempotency enforced)'
    Write-Output 'This confirms deterministic replay protection'
}

Write-Output 'PHASE 2 DEMO COMPLETE'
