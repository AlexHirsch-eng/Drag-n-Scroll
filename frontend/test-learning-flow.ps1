# Скрипт для проверки всех шагов обучения
# Сначала создай демо-данные: .\create-demo-course.ps1 -force
# Затем залогинься и получи токен, и запусти этот скрипт

param(
    [Parameter(Mandatory=$true)]
    [string]$Token
)

$API_BASE = "https://drag-n-scroll.onrender.com/api"

Write-Host "🧪 Testing Learning Flow..." -ForegroundColor Cyan
Write-Host ""

$headers = @{
    'Authorization' = "Bearer $Token"
    'Content-Type' = 'application/json'
}

try {
    # 1. Get main screen
    Write-Host "1️⃣  Testing /learning/main-screen/..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$API_BASE/learning/main-screen/" -Headers $headers -Method GET
    Write-Host "   ✅ Main screen loaded" -ForegroundColor Green
    Write-Host "   Course: $($response.current_course_day.title)" -ForegroundColor White
    Write-Host ""

    # 2. Start session
    Write-Host "2️⃣  Testing POST /learning/start/..." -ForegroundColor Yellow
    $body = @{
        course_day_id = $response.current_course_day.id
        session_type = 'A'
    } | ConvertTo-Json

    $session = Invoke-RestMethod -Uri "$API_BASE/learning/start/" -Headers $headers -Method POST -Body $body
    Write-Host "   ✅ Session started: ID $($session.session.id)" -ForegroundColor Green
    Write-Host "   Current step: $($session.session.current_step)" -ForegroundColor White
    Write-Host ""

    # 3. Get step 1 data
    Write-Host "3️⃣  Testing GET /learning/step/$($session.session.id)/..." -ForegroundColor Yellow
    $step1 = Invoke-RestMethod -Uri "$API_BASE/learning/step/$($session.session.id)/" -Headers $headers -Method GET
    Write-Host "   ✅ Step 1 loaded: $($step1.step_type)" -ForegroundColor Green
    Write-Host "   Cards: $($step1.data.total_cards)" -ForegroundColor White
    Write-Host ""

    # 4. Test submit step 1 (first card)
    if ($step1.data.total_cards -gt 0) {
        Write-Host "4️⃣  Testing POST /learning/submit/step-1/..." -ForegroundColor Yellow
        $firstCard = $step1.data.cards[0]
        $submitBody = @{
            session_id = $session.session.id
            card_id = $firstCard.id
            selected_option_id = $firstCard.options[0].word_id
            time_spent_seconds = 5
            current_card_index = 0
            total_shown_cards = $step1.data.total_cards
        } | ConvertTo-Json

        $result = Invoke-RestMethod -Uri "$API_BASE/learning/submit/step-1/" -Headers $headers -Method POST -Body $submitBody
        Write-Host "   ✅ Step 1 submitted" -ForegroundColor Green
        Write-Host "   Correct: $($result.is_correct)" -ForegroundColor White
        Write-Host "   XP earned: $($result.xp_earned)" -ForegroundColor White
        Write-Host ""
    }

    # 5. Get step 2 data (should be available after step 1 completes)
    # Note: This only works if step 1 was completed (all cards answered)
    Write-Host "5️⃣  Testing other steps..." -ForegroundColor Yellow
    Write-Host "   ℹ️  Complete step 1 first to test step 2" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "✅ Basic tests passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next:" -ForegroundColor Yellow
    Write-Host "1. Complete all cards in Step 1 (SRS Review)" -ForegroundColor White
    Write-Host "2. Step 2 (New Words) will unlock" -ForegroundColor White
    Write-Host "3. Then Step 3 (Grammar)" -ForegroundColor White
    Write-Host "4. Then Step 4 (Dialogue)" -ForegroundColor White
    Write-Host "5. Then Step 5 (Word Arrangement)" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "1. Demo course is created (.\\create-demo-course.ps1 -force)" -ForegroundColor White
    Write-Host "2. You are logged in and token is valid" -ForegroundColor White
    Write-Host "3. Backend is deployed (check https://drag-n-scroll.onrender.com/api/health/)" -ForegroundColor White
}

Write-Host ""
