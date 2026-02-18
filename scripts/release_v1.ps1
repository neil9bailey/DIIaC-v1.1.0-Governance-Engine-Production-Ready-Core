Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$VERSION = "v1.0.0"
$BRANCH = "main"

Write-Host "Releasing Meta Prompt Generator $VERSION" -ForegroundColor Cyan

if (!(Test-Path ".git")) {
    Write-Error "Not a git repository"
    exit 1
}

$currentBranch = git branch --show-current
if ($currentBranch -ne $BRANCH) {
    Write-Error "Must be on branch $BRANCH (current: $currentBranch)"
    exit 1
}

$status = git status --porcelain
if ($status.Length -ne 0) {
    Write-Error "Working tree not clean. Commit changes first."
    exit 1
}

if (git tag --list $VERSION) {
    Write-Error "Tag $VERSION already exists"
    exit 1
}

Write-Host "Creating tag $VERSION" -ForegroundColor Yellow
git tag -a $VERSION -m "Meta Prompt Generator $VERSION"

Write-Host "Pushing branch $BRANCH" -ForegroundColor Yellow
git push origin $BRANCH

Write-Host "Pushing tag $VERSION" -ForegroundColor Yellow
git push origin $VERSION

Write-Host "Release $VERSION published successfully" -ForegroundColor Green
