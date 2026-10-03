param(
    [string]$Repo = 'Faheem-Ahmad911/EV-Predictions-System',
    [string]$GhPath = 'gh',
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$policy = @{
    required_status_checks = @{
        strict = $true
        contexts = @('Branch policy', 'Lint and tests', 'Data checks and smoke train')
    }
    enforce_admins = $true
    required_pull_request_reviews = @{
        required_approving_review_count = 1
        dismiss_stale_reviews = $true
        require_last_push_approval = $true
    }
    restrictions = $null
    allow_force_pushes = $false
    allow_deletions = $false
    required_conversation_resolution = $true
}
if (-not $Apply) {
    Write-Output 'Preview only. A repository administrator must run with -Apply.'
    $policy | ConvertTo-Json -Depth 10
    exit 0
}
$isAdmin = & $GhPath api "repos/$Repo" --jq '.permissions.admin'
if ($LASTEXITCODE -ne 0 -or $isAdmin -ne 'true') {
    throw 'The signed-in GitHub account needs repository admin permission to protect branches.'
}
$policyFile = New-TemporaryFile
try {
    [System.IO.File]::WriteAllText($policyFile.FullName, ($policy | ConvertTo-Json -Depth 10))
    foreach ($branchName in @('dev', 'staging', 'main')) {
        & $GhPath api --method PUT "repos/$Repo/branches/$branchName/protection" --input $policyFile.FullName --silent
        if ($LASTEXITCODE -ne 0) { throw "Could not protect $branchName; inspect GitHub's error." }
        Write-Output "Protected $branchName with one approval, required checks, and no force pushes."
    }
} finally {
    Remove-Item -LiteralPath $policyFile.FullName
}
