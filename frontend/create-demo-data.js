// Script to create demo course data via API
// Run with: node create-demo-data.js

const API_BASE = 'https://drag-n-scroll.onrender.com/api';

async function createDemoData() {
  // Login as admin/test user
  const loginResponse = await fetch(`${API_BASE}/auth/jwt/create/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'testuser2026',
      password: 'TestPass123!'
    })
  });

  if (!loginResponse.ok) {
    console.error('❌ Login failed. Please create testuser2026 first.');
    return;
  }

  const { access } = await loginResponse.json();
  console.log('✅ Logged in successfully');

  // Create course via admin API or create directly
  // Note: This requires an admin endpoint to be implemented
  console.log('⚠️  Course creation requires admin access.');
  console.log('Please use Render Shell instead: python manage.py create_demo_course');
}

createDemoData();
