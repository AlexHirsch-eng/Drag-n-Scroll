# Скрипт для создания демо-данных курса через API
# Запусти: .\create-demo-course.ps1

$API_BASE = "https://drag-n-scroll.onrender.com/api"
$SECRET_KEY = "drag-n-scroll-demo-2026"

Write-Host "🚀 Creating demo course data..." -ForegroundColor Cyan
Write-Host ""

try {
    $body = @{
        secret_key = $SECRET_KEY
    } | ConvertTo-Json

    $response = Invoke-RestMethod `
        -Uri "$API_BASE/learning/create-demo-data/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop

    if ($response.message -eq "Demo course already exists") {
        Write-Host "✅ Demo course already exists!" -ForegroundColor Green
        Write-Host "Course: $($response.course.title)" -ForegroundColor White
        Write-Host ""
        Write-Host "No need to create again. Refresh your frontend page." -ForegroundColor Yellow
    } else {
        Write-Host "✅ SUCCESS!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Course created: $($response.course.title)" -ForegroundColor White
        Write-Host "Day: $($response.day.title)" -ForegroundColor White
        Write-Host "Words created: $($response.words_created)" -ForegroundColor White
        Write-Host ""
        Write-Host "Words:" -ForegroundColor Cyan
        foreach ($word in $response.words) {
            Write-Host "  - $($word.hanzi) ($($word.pinyin))" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "🎉 Demo course is ready!" -ForegroundColor Green
        Write-Host "Refresh your frontend page to see the changes." -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "1. Backend is still deploying (wait 5-10 minutes after git push)" -ForegroundColor White
    Write-Host "2. Check if backend is accessible: https://drag-n-scroll.onrender.com/api/health/" -ForegroundColor White
    Write-Host ""
    Write-Host "Try again in a few minutes." -ForegroundColor Yellow
}

Write-Host ""
