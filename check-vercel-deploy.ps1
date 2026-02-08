#!/usr/bin/env pwsh
# Script to check if Vercel deployment is complete and ready

$ErrorActionPreference = "Continue"

Write-Host "`n=== Vercel Deployment Checker ===" -ForegroundColor Cyan
Write-Host "Waiting for new deployment...`n" -ForegroundColor Yellow

# Expected new build hash (will be different from old one)
$OldBuild = "index-BVZ62spy.js"
$MaxAttempts = 30
$Attempt = 0

while ($Attempt -lt $MaxAttempts) {
    $Attempt++
    Write-Host "Attempt $Attempt/$MaxAttempts..." -ForegroundColor Gray

    try {
        $response = Invoke-WebRequest -Uri "https://drag-n-scroll.vercel.app" -UseBasicParsing -TimeoutSec 10
        $content = $response.Content

        # Extract current build hash
        if ($content -match 'index-([A-Za-z0-9]+)\.js') {
            $CurrentBuild = $matches[0]
            $BuildHash = $matches[1]

            if ($CurrentBuild -ne $OldBuild) {
                Write-Host "`n✓ NEW BUILD DETECTED: $CurrentBuild" -ForegroundColor Green
                Write-Host "Deployment is complete!`n" -ForegroundColor Green

                # Test health endpoint
                Write-Host "Testing backend connection..." -ForegroundColor Cyan
                try {
                    $healthResponse = Invoke-WebRequest -Uri "https://drag-n-scroll.onrender.com/api/health/" -UseBasicParsing -TimeoutSec 10
                    Write-Host "✓ Backend is healthy: $($healthResponse.StatusCode)" -ForegroundColor Green
                } catch {
                    Write-Host "⚠ Backend health check failed: $_" -ForegroundColor Yellow
                }

                Write-Host "`n=== READY TO TEST ===" -ForegroundColor Green
                Write-Host "1. Open browser in INCOGNITO mode" -ForegroundColor White
                Write-Host "2. Go to: https://drag-n-scroll.vercel.app" -ForegroundColor White
                Write-Host "3. Test registration and login`n" -ForegroundColor White

                exit 0
            } else {
                Write-Host "  Still old build: $CurrentBuild" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "  Error checking: $_" -ForegroundColor Red
    }

    Start-Sleep -Seconds 10
}

Write-Host "`n✗ Timeout: Deployment not complete after $MaxAttempts attempts" -ForegroundColor Red
Write-Host "Please check Vercel dashboard manually: https://vercel.com/dashboard`n" -ForegroundColor Yellow
exit 1
