Set-Location "F:\App Development\vendorlogic-diiac"

$timestamp   = Get-Date -Format "yyyyMMdd-HHmm"
$backupName  = "vendorlogic-diiac_BACKUP_step4_container_baseline_$timestamp"
$destination = "..\$backupName.zip"

# Ledger file path
$ledgerPath = "backup-ledger.jsonl"

# Build include list by filtering out excluded paths
$items = Get-ChildItem -Recurse -File | Where-Object {
    $_.FullName -notmatch "\\.git\\" -and
    $_.FullName -notmatch "node_modules" -and
    $_.FullName -notmatch "\\.venv\\" -and
    $_.FullName -notmatch "artefacts\\step4-cto-strategy\\output" -and
    $_.FullName -notmatch "ledger\\ledger.jsonl"
}

try {
    Compress-Archive -Path $items.FullName -DestinationPath $destination -ErrorAction Stop

    # Compute SHA256 hash of the backup
    $hash = Get-FileHash -Path $destination -Algorithm SHA256

    # Build ledger entry
    $entry = [PSCustomObject]@{
        timestamp     = $timestamp
        backup_file   = $destination
        file_count    = $items.Count
        sha256        = $hash.Hash
        status        = "success"
    }

    # Append to ledger
    $entry | ConvertTo-Json -Compress | Add-Content $ledgerPath

    Write-Host "Backup created: $destination"
    Write-Host "Ledger updated: $ledgerPath"
}
catch {
    # Log failure
    $entry = [PSCustomObject]@{
        timestamp     = $timestamp
        backup_file   = $destination
        file_count    = $items.Count
        sha256        = $null
        status        = "failure"
        error         = $_.Exception.Message
    }

    $entry | ConvertTo-Json -Compress | Add-Content $ledgerPath

    Write-Host "Backup failed. See ledger for details."
}