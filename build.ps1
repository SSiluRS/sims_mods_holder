param (
    [string]$Version = "latest"
)

$BackendImage = "sims-mods-backend:$Version"
$FrontendImage = "sims-mods-frontend:$Version"

Write-Host "Building Backend Image: $BackendImage..." -ForegroundColor Cyan
docker build -t $BackendImage -f Dockerfile .

Write-Host "Building Frontend Image: $FrontendImage..." -ForegroundColor Cyan
docker build -t $FrontendImage -f frontend/Dockerfile ./frontend

Write-Host "`nBuild complete!" -ForegroundColor Green
Write-Host "Images created:"
Write-Host " - $BackendImage"
Write-Host " - $FrontendImage"
