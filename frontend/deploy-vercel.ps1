#!/usr/bin/env pwsh
# Script to deploy frontend to Vercel with correct environment variables

Write-Host "=== Deploying Drag'n'Scroll Frontend to Vercel ===" -ForegroundColor Cyan
Write-Host ""

# Check if in frontend directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Error: Please run this script from the frontend directory" -ForegroundColor Red
    Write-Host "   Run: cd frontend" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Found package.json" -ForegroundColor Green
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "Checking Vercel CLI..." -ForegroundColor Cyan
$vercelVersion = npx vercel --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Vercel CLI $vercelVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host ""
Write-Host "=== IMPORTANT ===" -ForegroundColor Yellow
Write-Host "You will need to login to Vercel if not already logged in" -ForegroundColor White
Write-Host ""

# Login to Vercel
Write-Host "Checking Vercel login status..." -ForegroundColor Cyan
npx vercel whoami >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Not logged in. Opening browser for login..." -ForegroundColor Yellow
    npx vercel login
} else {
    Write-Host "✓ Already logged in to Vercel" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Deploying to Production ===" -ForegroundColor Cyan
Write-Host ""

# Deploy to production
Write-Host "Running: npx vercel --prod --yes" -ForegroundColor White
npx vercel --prod --yes

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== ✅ DEPLOYMENT SUCCESSFUL ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your app is now live at: https://drag-n-scroll.vercel.app" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Open browser in INCOGNITO mode" -ForegroundColor White
    Write-Host "2. Go to: https://drag-n-scroll.vercel.app" -ForegroundColor White
    Write-Host "3. Test registration and login" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=== ❌ DEPLOYMENT FAILED ===" -ForegroundColor Red
    Write-Host "Please check the errors above and try again" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
