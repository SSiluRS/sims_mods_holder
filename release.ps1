param(
    [Parameter(Mandatory=$true, HelpMessage="Version to release (e.g. 1.0.0)")]
    [string]$Version
)

# Validate version format (X.Y.Z)
if ($Version -notmatch "^\d+\.\d+\.\d+$") {
    Write-Error "Error: Version must be in format X.Y.Z (e.g. 1.0.0)"
    exit 1
}

$Tag = "v$Version"

# Check if tag exists locally
$existingTag = git tag -l $Tag
if ($existingTag) {
    Write-Error "Error: Tag $Tag already exists locally."
    exit 1
}

# Confirmation
$Confirmation = Read-Host "About to create tag $Tag and push to origin. Continue? (y/n)"
if ($Confirmation -ne 'y') {
    Write-Host "Cancelled."
    exit 0
}

# Create tag
Write-Host "Creating tag $Tag..."
git tag -a $Tag -m "Release $Version"

if ($LASTEXITCODE -eq 0) {
    # Push tag
    Write-Host "Pushing tag $Tag to remote..."
    git push origin $Tag
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS! GitHub Actions should start building for $Tag soon."
        Write-Host "Check status: https://github.com/SSiluRS/sims_mods_holder/actions"
    } else {
        Write-Error "Error pushing tag."
    }
} else {
    Write-Error "Error creating tag."
}