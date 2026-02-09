# Скрипт для создания демо-данных курса через API
# Запусти: .\create-demo-course.ps1
# Используй -force для перезаписи: .\create-demo-course.ps1 -force

param([switch]$force)

$API_BASE = "https://drag-n-scroll.onrender.com/api"
$SECRET_KEY = "drag-n-scroll-demo-2026"

Write-Host "🚀 Creating demo course data..." -ForegroundColor Cyan
if ($force) {
    Write-Host "⚠️  FORCE MODE: Will overwrite existing course!" -ForegroundColor Yellow
}
Write-Host ""

try {
    $body = @{
        secret_key = $SECRET_KEY
        force = $force.IsPresent
    } | ConvertTo-Json

    $response = Invoke-RestMethod `
        -Uri "$API_BASE/learning/create-demo-data/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop

    if ($response.message -eq "Demo course already exists") {
        Write-Host "ℹ️  Demo course already exists!" -ForegroundColor Yellow
        Write-Host "Course: $($response.course.title)" -ForegroundColor White
        Write-Host ""
        Write-Host "To overwrite, run: .\create-demo-course.ps1 -force" -ForegroundColor Cyan
    } else {
        Write-Host "✅ SUCCESS!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Course created: $($response.course.title)" -ForegroundColor White
        Write-Host "Day: $($response.day.title)" -ForegroundColor White
        Write-Host "Words created: $($response.words_created)" -ForegroundColor White
        Write-Host "Grammar tasks: $($response.grammar_tasks)" -ForegroundColor White
        Write-Host "Dialogues: $($response.dialogues)" -ForegroundColor White
        Write-Host "Exercises: $($response.exercises)" -ForegroundColor White
        Write-Host ""
        Write-Host "Words:" -ForegroundColor Cyan
        foreach ($word in $response.words) {
            Write-Host "  - $($word.hanzi) ($($word.pinyin))" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "🎉 Demo course is ready!" -ForegroundColor Green
        Write-Host "All 5 steps now have data for testing!" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Refresh your frontend page" -ForegroundColor White
        Write-Host "2. Click 'Начать обучение' to test the session" -ForegroundColor White
        Write-Host "3. Complete all 5 steps: SRS, Words, Grammar, Dialogue, Arrangement" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "1. Backend is still deploying (wait 5-10 minutes after git push)" -ForegroundColor White
    Write-Host "2. Check backend health: https://drag-n-scroll.onrender.com/api/health/" -ForegroundColor White
    Write-Host ""
    Write-Host "Try again in a few minutes." -ForegroundColor Yellow
}

Write-Host ""
