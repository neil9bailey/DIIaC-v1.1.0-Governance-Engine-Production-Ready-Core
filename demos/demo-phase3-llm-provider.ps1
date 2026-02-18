Write-Output 'DIIaC Phase 3.1 Demo — LLM Provider Interface (Mock)'

$python = 'python'

# Set PYTHONPATH to Backend so `app.*` resolves correctly
$env:PYTHONPATH = 'F:\App Development\vendorlogic-diiac\Backend'

$tempScriptPath = 'F:\App Development\vendorlogic-diiac\demos\_phase3_llm_test.py'

# Write a temporary Python script to disk
@"
from app.llm_providers.llm_service import generate_from_llm

result = generate_from_llm(
    prompt="CTO cloud strategy placeholder",
    provider_name="mock",
    parameters={"temperature": 0},
    trusted=False,
)

print(result)
"@ | Out-File -FilePath $tempScriptPath -Encoding ASCII

Write-Output 'Invoking mock LLM provider via Python...'

& $python $tempScriptPath

Write-Output 'PHASE 3.1 DEMO COMPLETE'
