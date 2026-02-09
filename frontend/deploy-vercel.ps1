# Deploy frontend to Vercel
Write-Host "=== Deploying to Vercel ===" -ForegroundColor Cyan
Write-Host ""

# Check directory
if (-not (Test-Path "package.json")) {
    Write-Host "ERROR: Not in frontend directory" -ForegroundColor Red
    exit 1
}

Write-Host "OK: Found package.json" -ForegroundColor Green
Write-Host ""

# Check login
Write-Host "Checking Vercel login..." -ForegroundColor Cyan
npx vercel whoami >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in. Opening browser..." -ForegroundColor Yellow
    npx vercel login
} else {
    Write-Host "OK: Already logged in" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Deploying ===" -ForegroundColor Cyan
npx vercel --prod --yes

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Deployment complete" -ForegroundColor Green
    Write-Host "URL: https://drag-n-scroll.vercel.app" -ForegroundColor White
    Write-Host ""
    Write-Host "Next:" -ForegroundColor Cyan
    Write-Host "1. Open browser in INCOGNITO mode" -ForegroundColor White
    Write-Host "2. Go to https://drag-n-scroll.vercel.app" -ForegroundColor White
    Write-Host "3. Test the app" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "FAILED: Check errors above" -ForegroundColor Red
    exit 1
}
