/**
 * Скрипт для создания демо-данных курса через API
 * Run: node create-demo-course.js
 */

const API_BASE = 'https://drag-n-scroll.onrender.com/api';
const SECRET_KEY = 'drag-n-scroll-demo-2026';

async function createDemoCourse() {
  console.log('🚀 Creating demo course data...\n');

  try {
    const response = await fetch(`${API_BASE}/learning/create-demo-data/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        secret_key: SECRET_KEY
      })
    });

    const data = await response.json();

    if (response.ok) {
      console.log('✅ SUCCESS!\n');
      console.log('Course created:', data.course.title);
      console.log('Day:', data.day.title);
      console.log('Words created:', data.words_created);
      console.log('\nWords:');
      data.words.forEach(word => {
        console.log(`  - ${word.hanzi} (${word.pinyin})`);
      });
      console.log('\n🎉 Demo course is ready!');
      console.log('Refresh your frontend page to see the changes.\n');
    } else if (response.status === 401) {
      console.log('❌ Unauthorized: Invalid secret key');
    } else if (data.message && data.message.includes('already exists')) {
      console.log('✅ Demo course already exists!');
      console.log('Course:', data.course.title);
      console.log('\nNo need to create again. Refresh your frontend page.\n');
    } else {
      console.log('❌ Error:', data.error || 'Unknown error');
    }
  } catch (error) {
    console.error('❌ Request failed:', error.message);
    console.log('\nMake sure backend is deployed and accessible.');
    console.log('If backend was just updated, wait 2-3 minutes for deployment to complete.\n');
  }
}

createDemoCourse();
