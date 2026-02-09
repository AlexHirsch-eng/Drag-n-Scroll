# Пересоздание демо-курса с полными данными для всех шагов
# УДАЛИТ старый курс и создаст новый с:
# - Step 1: SRS Review (10 cards)
# - Step 2: New Words (5 слов)
# - Step 3: Grammar (задачи для Session A и B)
# - Step 4: Dialogue (диалоги для Session A и B)
# - Step 5: Word Arrangement (упражнения для Session A и B)

Write-Host "🔄 Пересоздание демо-курса..." -ForegroundColor Cyan
Write-Host "⚠️  Старый курс будет УДАЛЕН!" -ForegroundColor Red
Write-Host ""

$API_BASE = "https://drag-n-scroll.onrender.com/api"
$SECRET_KEY = "drag-n-scroll-demo-2026"

try {
    $body = @{
        secret_key = $SECRET_KEY
        force = $true
    } | ConvertTo-Json

    Write-Host "📤 Отправка запроса..." -ForegroundColor Yellow
    $response = Invoke-RestMethod `
        -Uri "$API_BASE/learning/create-demo-data/" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body `
        -ErrorAction Stop

    Write-Host ""
    Write-Host "✅ УСПЕХ!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Создано:" -ForegroundColor Cyan
    Write-Host "  Курс: $($response.course.title)" -ForegroundColor White
    Write-Host "  День: $($response.day.day_number) - $($response.day.title)" -ForegroundColor White
    Write-Host "  Слов: $($response.words_created)" -ForegroundColor White
    Write-Host "  Грамматика: $($response.grammar_tasks) задачи" -ForegroundColor White
    Write-Host "  Диалоги: $($response.dialogues)" -ForegroundColor White
    Write-Host "  Упражнения: $($response.exercises)" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Слова:" -ForegroundColor Cyan
    foreach ($word in $response.words) {
        Write-Host "  • $($word.hanzi) - $($word.pinyin)" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "🎯 Теперь ВСЕ 5 шагов имеют данные!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔄 Обнови фронтенд страницу (Ctrl+Shift+R)" -ForegroundColor Yellow
    Write-Host "🚀 Затем нажми 'Начать обучение' для тестирования" -ForegroundColor Yellow
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "❌ Ошибка: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Подробности: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Возможные причины:" -ForegroundColor Yellow
    Write-Host "1. Backend еще deploy'ится (подожди 2-3 минуты)" -ForegroundColor White
    Write-Host "2. Проверь здоровье backend: https://drag-n-scroll.onrender.com/api/health/" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
