# Автоматическое пересоздание демо-курса после деплоя
# Скрипт проверяет готовность backend и пересоздает курс

param(
    [int]$MaxWaitSeconds = 600,  # Максимальное время ожидания (10 минут)
    [int]$CheckInterval = 10      # Проверять каждые 10 секунд
)

$API_BASE = "https://drag-n-scroll.onrender.com/api"
$SECRET_KEY = "drag-n-scroll-demo-2026"

Write-Host "🔄 Ожидание деплоя backend..." -ForegroundColor Cyan
Write-Host "Максимальное время ожидания: $($MaxWaitSeconds) секунд" -ForegroundColor White
Write-Host ""

$elapsed = 0
while ($elapsed -lt $MaxWaitSeconds) {
    try {
        # Проверяем здоровье backend
        Write-Host "⏳ Проверка здоровья backend... ($elapsed сек)" -ForegroundColor Yellow
        $health = Invoke-RestMethod -Uri "$API_BASE/health/" -Method GET -TimeoutSec 5

        if ($health.status -eq "healthy") {
            Write-Host "✅ Backend готов!" -ForegroundColor Green
            Write-Host ""

            # Пересоздаем курс
            Write-Host "📤 Пересоздание демо-курса..." -ForegroundColor Cyan

            $body = @{
                secret_key = $SECRET_KEY
                force = $true
            } | ConvertTo-Json

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
            return
        }
    } catch {
        # Backend еще не готов
        Write-Host "⏸️  Еще не готово, ждем..." -ForegroundColor Yellow
    }

    Start-Sleep -Seconds $CheckInterval
    $elapsed += $CheckInterval
}

Write-Host ""
Write-Host "❌ Превышено время ожидания" -ForegroundColor Red
Write-Host "Проверь статус деплоя: https://dashboard.render.com" -ForegroundColor Yellow
Write-Host "Или запусти скрипт снова позже." -ForegroundColor Yellow
Write-Host ""
