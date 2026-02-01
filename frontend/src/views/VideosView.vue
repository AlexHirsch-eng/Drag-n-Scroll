<template>
  <div class="videos-view">
    <!-- Loading State -->
    <div v-if="loading && videos.length === 0" class="loading-state">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading videos...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && videos.length === 0" class="empty-state">
      <div class="empty-icon">📹</div>
      <h3 class="empty-title">No Videos Yet</h3>
      <p class="empty-text">Be the first to create a video!</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3 class="error-title">Oops!</h3>
      <p class="error-text">{{ error }}</p>
      <button @click="loadVideos()" class="retry-btn">Retry</button>
    </div>

    <!-- TikTok-style Video Feed -->
    <div v-else class="video-feed" @wheel="handleWheel" @touchstart="handleTouchStart" @touchend="handleTouchEnd">
      <div
        v-for="(video, index) in videos"
        :key="video.id"
        class="video-container"
        :class="{ active: currentVideoIndex === index }"
      >
        <!-- Video Player - Keep video element always in DOM -->
        <div class="video-player">
          <video
            :ref="(el) => { if(el) videoPlayers[index] = el as HTMLVideoElement }"
            :src="video.url"
            :poster="video.thumbnail"
            loop
            playsinline
            @click="togglePlay"
            @ended="onVideoEnded"
            @timeupdate="onTimeUpdate"
            class="video-element"
            :class="{ 'video-hidden': currentVideoIndex !== index }"
            @error="onVideoError"
          ></video>

          <!-- Play/Pause Overlay - Only show for current video -->
          <div v-if="!isPlaying && currentVideoIndex === index" class="play-overlay">
            <div class="play-icon">▶</div>
          </div>

          <!-- Progress Bar - Only show for current video -->
          <div v-if="currentVideoIndex === index" class="progress-bar-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- Video Info Overlay -->
        <div class="video-info" v-if="currentVideoIndex === index">
          <!-- Top Bar -->
          <div class="top-bar">
            <button @click="goBack" class="back-btn">←</button>
            <h3 class="section-title">VIDEOS</h3>
            <div class="top-bar-actions">
              <button
                @click="translationLanguage = translationLanguage === 'ru' ? 'en' : 'ru'"
                class="lang-btn"
                title="Switch translation language"
              >
                {{ translationLanguage === 'ru' ? '🇷🇺 RU' : '🇬🇧 EN' }}
              </button>
              <button
                v-if="authStore.user?.is_staff"
                @click="importVideos"
                class="import-btn"
                :disabled="isImporting"
              >
                {{ isImporting ? '⏳' : '📥' }}
              </button>
              <button @click="toggleSearch" class="search-btn">🔍</button>
            </div>
          </div>

          <!-- Search Bar -->
          <div v-if="searchVisible" class="search-bar">
            <input
              v-model="searchQuery"
              @keyup.enter="performSearch"
              type="text"
              placeholder="Search videos by hashtags..."
              class="search-input"
            />
            <button @click="performSearch" class="search-submit-btn">Search</button>
          </div>

          <!-- Right Side Actions -->
          <div class="side-actions">
            <!-- Like -->
            <button @click="toggleLike(video)" class="action-btn">
              <div class="action-icon">{{ video.is_liked ? '❤️' : '🤍' }}</div>
              <div class="action-count">{{ formatCount(video.likes_count) }}</div>
            </button>

            <!-- Comment -->
            <button @click="openComments(video)" class="action-btn">
              <div class="action-icon">💬</div>
              <div class="action-count">{{ formatCount(video.comments_count) }}</div>
            </button>

            <!-- Share -->
            <button @click="shareVideo(video)" class="action-btn">
              <div class="action-icon">↪️</div>
              <div class="action-count">Share</div>
            </button>

            <!-- Save -->
            <button @click="toggleSave(video)" class="action-btn">
              <div class="action-icon">{{ video.is_saved ? '🔖' : '📑' }}</div>
              <div class="action-count">{{ video.is_saved ? 'Saved' : 'Save' }}</div>
            </button>
          </div>

          <!-- Bottom Info -->
          <div class="bottom-info">
            <!-- User Info -->
            <div class="user-info">
              <div class="avatar" @click="goToUserProfile(video.creator.id)">{{ video.creator.username[0].toUpperCase() }}</div>
              <div class="user-details">
                <div class="username" @click="goToUserProfile(video.creator.id)">@{{ video.creator.username }}</div>
                <button
                  v-if="!video.creator.is_following"
                  @click.stop="followUser(video.creator.id)"
                  class="follow-btn"
                >
                  Follow
                </button>
                <button
                  v-else
                  @click.stop="unfollowUser(video.creator.id)"
                  class="following-btn"
                >
                  Following
                </button>
              </div>
            </div>

            <!-- Description -->
            <div class="video-description">
              <p class="description-text">{{ video.description }}</p>
              <div class="video-tags">
                <span v-for="tag in video.tags" :key="tag" class="tag">#{{ tag }}</span>
              </div>
            </div>

            <!-- Lesson Info -->
            <div v-if="video.lesson" class="lesson-info">
              <div class="lesson-badge">📚 LESSON {{ video.lesson.lesson_number }}</div>
              <div class="lesson-title">{{ video.lesson.title }}</div>
              <div class="lesson-words">
                <span v-for="word in video.lesson.words" :key="word" class="lesson-word">
                  {{ word }}
                </span>
              </div>
            </div>

            <!-- Music Info -->
            <div class="music-info">
              <div class="music-icon">🎵</div>
              <div class="music-text">
                <div class="music-title">{{ video.music_title || 'Original Sound' }}</div>
                <div class="music-artist">@{{ video.creator.username }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Comments Modal -->
    <div v-if="showCommentsModal" class="comments-modal" @click="closeComments">
      <div class="comments-content" @click.stop>
        <div class="comments-header">
          <h3>{{ commentsCount }} Comments</h3>
          <button @click="closeComments" class="close-btn">✕</button>
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment">
            <div class="comment-avatar">{{ comment.user.username[0].toUpperCase() }}</div>
            <div class="comment-content">
              <div class="comment-user">@{{ comment.user.username }}</div>
              <div class="comment-text">{{ comment.text }}</div>

              <!-- Translation -->
              <div v-if="comment.translation_ru || comment.translation_en" class="comment-translation">
                <div class="translation-header">Перевод:</div>
                <div class="translation-text">
                  {{ translationLanguage === 'ru' ? comment.translation_ru : comment.translation_en }}
                </div>
              </div>

              <div class="comment-actions">
                <button @click="likeComment(comment.id)" class="comment-action">
                  ❤️ {{ comment.likes_count }}
                </button>
                <button
                  v-if="isChinese(comment.text) && !comment.translation_ru && !comment.translation_en"
                  @click="translateComment(comment.id)"
                  class="comment-action translate-action"
                  :disabled="translatingComments.has(comment.id)"
                >
                  {{ translatingComments.has(comment.id) ? '⏳' : '🌐' }} Translate
                </button>
                <button @click="toggleReply(comment.id)" class="comment-action">
                  Reply
                </button>
              </div>
              <!-- Reply Input -->
              <div v-if="replyingTo === comment.id" class="reply-input">
                <input
                  v-model="replyText"
                  @keyup.enter="postReply(comment.id)"
                  type="text"
                  placeholder="Write a reply..."
                  class="reply-field"
                />
                <div class="reply-actions">
                  <button @click="postReply(comment.id)" class="send-reply-btn" :disabled="!replyText.trim()">
                    Reply
                  </button>
                  <button @click="cancelReply" class="cancel-reply-btn">Cancel</button>
                </div>
              </div>
            </div>
            <div class="comment-time">{{ formatTime(comment.created_at) }}</div>
          </div>
        </div>

        <div class="comment-input">
          <input
            v-model="newComment"
            @keyup.enter="postComment"
            type="text"
            placeholder="Add a comment..."
            class="comment-field"
            :disabled="postingComment"
          />
          <button @click="postComment" class="send-btn" :disabled="!newComment.trim() || postingComment">
            {{ postingComment ? 'Sending...' : 'Send' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Category Filter -->
    <div class="category-filter">
      <button
        v-for="category in categories"
        :key="category.id"
        @click="selectCategory(category.id)"
        class="category-btn"
        :class="{ active: selectedCategory === category.id }"
      >
        {{ category.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { videoAPI, Video } from '@/api/video'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// State
const currentVideoIndex = ref(0)
const isImporting = ref(false)
const isPlaying = ref(false)
const progress = ref(0)
const videos = ref<Video[]>([])
const showCommentsModal = ref(false)
const comments = ref<any[]>([])
const newComment = ref('')
const commentsCount = ref(0)
const postingComment = ref(false)
const replyingTo = ref<number | null>(null)
const replyText = ref('')
const searchVisible = ref(false)
const translationLanguage = ref<'ru' | 'en'>('ru')  // Default to Russian
const translatingComments = ref<Set<number>>(new Set())  // Track which comments are being translated
const searchQuery = ref('')
const selectedCategory = ref('all')
const videoPlayer = ref<HTMLVideoElement | null>(null)
const videoPlayers = ref<(HTMLVideoElement | null)[]>([])
const currentVideoId = ref<number | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

// Categories
const categories = ref([
  { id: 'all', name: '🔥 For You' }
])

// Load categories on mount
onMounted(async () => {
  console.log('=== VideosView mounted ===')
  await loadCategories()
  await loadVideos()

  // Wait for DOM to update with video elements
  await nextTick()

  console.log('After nextTick - Video players registered:', videoPlayers.value.filter(p => p !== null).length)

  // Check if a specific video should be opened
  const videoId = route.query.video as string
  if (videoId) {
    const targetIndex = videos.value.findIndex(v => v.id === parseInt(videoId))
    if (targetIndex !== -1) {
      currentVideoIndex.value = targetIndex
    }
  }

  // Wait another tick for video elements to be ready
  await nextTick()
  playCurrentVideo()
})

async function loadCategories() {
  try {
    const categoriesData = await videoAPI.getCategories()
    categories.value = [
      { id: 'all', name: '🔥 For You' },
      ...categoriesData.map((cat: any) => ({
        id: cat.id.toString(),
        name: `${cat.icon || '📹'} ${cat.name}`
      }))
    ]
  } catch (err) {
    console.error('Error loading categories:', err)
    // Keep default categories if loading fails
  }
}

async function loadVideos(page = 1) {
  try {
    loading.value = true
    error.value = null

    console.log('=== loadVideos called ===')
    console.log('Page:', page, 'Category:', selectedCategory.value)

    let response
    if (selectedCategory.value === 'all') {
      response = await videoAPI.getFeed(page, 50)  // Increased from 20 to 50
    } else if (selectedCategory.value === 'trending') {
      response = { videos: await videoAPI.getTrending(), page: 1, has_more: false, total: 0 }
    } else {
      response = { videos: await videoAPI.getVideosByCategory(parseInt(selectedCategory.value)), page: 1, has_more: false, total: 0 }
    }

    console.log('API Response - Loaded videos:', response.videos.length, 'Total:', response.total)
    console.log('Video IDs:', response.videos.map((v, i) => `${i}: ID=${v.id}, Creator=${v.creator.username}`))

    if (page === 1) {
      videos.value = response.videos
    } else {
      videos.value.push(...response.videos)
    }

    // Set video URLs to use backend media
    videos.value = videos.value.map(video => ({
      ...video,
      url: video.video_file,
      thumbnail: video.thumbnail || ''
    }))

    console.log('After mapping - videos.value length:', videos.value.length)
    console.log('Videos in array:', videos.value.map((v, i) => `${i}: ${v.id} - ${v.url ? 'has URL' : 'NO URL'}`))
  } catch (err: any) {
    console.error('Error loading videos:', err)
    error.value = err.message || 'Failed to load videos. Please try again.'
    videos.value = []
  } finally {
    loading.value = false
  }
}

onUnmounted(() => {
  // Pause all videos
  videoPlayers.value.forEach(player => {
    if (player && typeof player.pause === 'function') {
      player.pause()
    }
  })
})

onBeforeUnmount(() => {
  // Pause ALL videos when leaving the page
  videoPlayers.value.forEach(player => {
    if (player) {
      player.pause()
      player.src = '' // Clear source to stop loading
    }
  })
})

// Watch videos array changes
watch(videos, (newVideos) => {
  console.log('=== Videos array updated ===')
  console.log('Number of videos:', newVideos.length)
  console.log('Video IDs:', newVideos.map((v, i) => `${i}: ${v.id}`))
}, { deep: true })

// Watch video index changes
watch(currentVideoIndex, async (newIndex, oldIndex) => {
  console.log(`Video index changed from ${oldIndex} to ${newIndex}`)
  console.log('Total video players registered:', videoPlayers.value.filter(p => p !== null).length)
  if (videos.value[newIndex]) {
    currentVideoId.value = videos.value[newIndex].id
    console.log('Current video:', videos.value[newIndex]?.description?.substring(0, 30))
  }
  playCurrentVideo()
})

function playCurrentVideo() {
  console.log('=== playCurrentVideo called ===')
  console.log('Playing video index:', currentVideoIndex.value, 'Total videos:', videos.value.length)
  console.log('Video players array length:', videoPlayers.value.length)
  console.log('Non-null players:', videoPlayers.value.map((p, i) => `${i}:${p ? '✓' : '✗'}`).join(', '))

  // Pause all videos first
  videoPlayers.value.forEach((player, index) => {
    if (player && typeof player.pause === 'function') {
      if (index !== currentVideoIndex.value) {
        console.log(`Pausing video at index ${index}`)
        player.pause()
        player.currentTime = 0
      }
    }
  })

  // Small delay to ensure DOM is updated
  setTimeout(() => {
    const currentPlayer = videoPlayers.value[currentVideoIndex.value]
    console.log('Current player:', currentPlayer ? 'found' : 'NOT FOUND')
    if (currentPlayer && typeof currentPlayer.play === 'function') {
      console.log('Playing video:', videos.value[currentVideoIndex.value]?.description?.substring(0, 30))
      console.log('Video src:', currentPlayer.src)

      // Play with volume to check if it works
      currentPlayer.volume = 0.5
      currentPlayer.play().then(() => {
        isPlaying.value = true
        videoPlayer.value = currentPlayer
        console.log('✓ Video started successfully')
      }).catch(err => {
        console.error('✗ Error playing video:', err)
        isPlaying.value = false
      })
    } else {
      console.warn('✗ No video player found for index:', currentVideoIndex.value)
    }
  }, 100)
}

function togglePlay() {
  if (!videoPlayer.value || typeof videoPlayer.value.pause !== 'function') return

  if (isPlaying.value) {
    videoPlayer.value.pause()
  } else {
    videoPlayer.value.play()
  }
  isPlaying.value = !isPlaying.value
}

function onTimeUpdate(event: Event) {
  const video = event.target as HTMLVideoElement
  progress.value = (video.currentTime / video.duration) * 100
}

function onVideoEnded() {
  // Auto-play next video
  if (currentVideoIndex.value < videos.value.length - 1) {
    currentVideoIndex.value++
  } else {
    // Loop back to start
    currentVideoIndex.value = 0
  }
}

function onVideoError(event: Event) {
  console.error('Video loading error:', event)
  const video = event.target as HTMLVideoElement
  if (video.error) {
    console.error('Video error code:', video.error.code)
  }
}

function handleWheel(event: WheelEvent) {
  event.preventDefault()
  if (event.deltaY > 0 && currentVideoIndex.value < videos.value.length - 1) {
    currentVideoIndex.value++
  } else if (event.deltaY < 0 && currentVideoIndex.value > 0) {
    currentVideoIndex.value--
  }
}

let touchStartY = 0
function handleTouchStart(event: TouchEvent) {
  touchStartY = event.touches[0].clientY
}

function handleTouchEnd(event: TouchEvent) {
  const touchEndY = event.changedTouches[0].clientY
  const diff = touchStartY - touchEndY

  if (Math.abs(diff) > 50) {
    if (diff > 0 && currentVideoIndex.value < videos.value.length - 1) {
      currentVideoIndex.value++
    } else if (diff < 0 && currentVideoIndex.value > 0) {
      currentVideoIndex.value--
    }
  }
}

async function toggleLike(video: Video) {
  try {
    const response = await videoAPI.likeVideo(video.id)
    video.is_liked = response.is_liked
    video.likes_count = response.likes_count
  } catch (error) {
    console.error('Error liking video:', error)
  }
}

async function toggleSave(video: Video) {
  try {
    const response = await videoAPI.bookmarkVideo(video.id)
    video.is_saved = response.is_saved
  } catch (error) {
    console.error('Error saving video:', error)
  }
}

async function openComments(video: Video) {
  try {
    currentVideoId.value = video.id
    const commentsData = await videoAPI.getComments(video.id)
    comments.value = commentsData
    commentsCount.value = video.comments_count
    showCommentsModal.value = true
  } catch (error) {
    console.error('Error loading comments:', error)
  }
}

function closeComments() {
  showCommentsModal.value = false
  currentVideoId.value = null
  replyingTo.value = null
  replyText.value = ''
}

async function postComment() {
  if (!newComment.value.trim() || !currentVideoId.value || postingComment.value) return

  try {
    postingComment.value = true
    const updatedComments = await videoAPI.createComment(
      currentVideoId.value,
      newComment.value
    )
    comments.value = updatedComments
    commentsCount.value++
    newComment.value = ''

    // Update comment count in the video list
    const video = videos.value.find(v => v.id === currentVideoId.value)
    if (video) {
      video.comments_count = commentsCount.value
    }
  } catch (error) {
    console.error('Error posting comment:', error)
    alert('Failed to post comment. Please try again.')
  } finally {
    postingComment.value = false
  }
}

async function likeComment(commentId: number) {
  try {
    const response = await videoAPI.likeComment(commentId)
    const comment = comments.value.find(c => c.id === commentId)
    if (comment) {
      comment.is_liked = response.is_liked
      comment.likes_count = response.likes_count
    }
  } catch (error) {
    console.error('Error liking comment:', error)
  }
}

async function translateComment(commentId: number) {
  if (translatingComments.value.has(commentId)) return

  try {
    translatingComments.value.add(commentId)
    const updatedComment = await videoAPI.translateComment(commentId, translationLanguage.value)

    // Update the comment in the list
    const index = comments.value.findIndex(c => c.id === commentId)
    if (index !== -1) {
      comments.value[index] = updatedComment
    }
  } catch (error: any) {
    console.error('Error translating comment:', error)
    alert(`Ошибка перевода: ${error.response?.data?.error || error.message || 'Неизвестная ошибка'}`)
  } finally {
    translatingComments.value.delete(commentId)
  }
}

function isChinese(text: string): boolean {
  // Check for Chinese characters
  const chineseRegex = /[\u4e00-\u9fff]/
  return chineseRegex.test(text)
}

function toggleReply(commentId: number) {
  if (replyingTo.value === commentId) {
    replyingTo.value = null
    replyText.value = ''
  } else {
    replyingTo.value = commentId
    replyText.value = ''
  }
}

function cancelReply() {
  replyingTo.value = null
  replyText.value = ''
}

async function postReply(parentCommentId: number) {
  if (!replyText.value.trim() || !currentVideoId.value) return

  try {
    await videoAPI.createComment(
      currentVideoId.value,
      replyText.value,
      parentCommentId
    )
    // Refresh comments
    const updatedComments = await videoAPI.getComments(currentVideoId.value)
    comments.value = updatedComments
    commentsCount.value++
    replyText.value = ''
    replyingTo.value = null

    // Update comment count in the video list
    const video = videos.value.find(v => v.id === currentVideoId.value)
    if (video) {
      video.comments_count = commentsCount.value
    }
  } catch (error) {
    console.error('Error posting reply:', error)
    alert('Failed to post reply. Please try again.')
  }
}

async function shareVideo(video: Video) {
  try {
    await videoAPI.shareVideo(video.id, 'web')

    if (navigator.share) {
      await navigator.share({
        title: video.description,
        text: `Check out this Chinese learning video!`,
        url: window.location.href
      })
    } else {
      await navigator.clipboard.writeText(window.location.href)
      alert('Link copied to clipboard!')
    }
  } catch (error) {
    console.error('Error sharing video:', error)
  }
}

async function followUser(userId: number) {
  try {
    const response = await videoAPI.followUser(userId)
    const video = videos.value[currentVideoIndex.value]
    if (video) {
      video.creator.is_following = response.is_following
    }
  } catch (error) {
    console.error('Error following user:', error)
  }
}

async function unfollowUser(userId: number) {
  try {
    const response = await videoAPI.followUser(userId)
    const video = videos.value[currentVideoIndex.value]
    if (video) {
      video.creator.is_following = response.is_following
    }
  } catch (error) {
    console.error('Error unfollowing user:', error)
  }
}

async function selectCategory(categoryId: string) {
  console.log('=== Category selected ===', categoryId)
  selectedCategory.value = categoryId
  currentVideoIndex.value = 0
  await loadVideos(1)
  await nextTick()
  playCurrentVideo()
}

async function importVideos() {
  if (isImporting.value) return

  try {
    isImporting.value = true
    const result = await videoAPI.importVideosFromFolder()

    // Show import results
    alert(
      `Импорт завершен!\n\n` +
      `Всего найдено: ${result.total}\n` +
      `Импортировано: ${result.imported}\n` +
      `Пропущено: ${result.skipped}\n` +
      `Ошибок: ${result.errors}`
    )

    // Reload videos to show newly imported ones
    await loadVideos(1)
  } catch (error: any) {
    console.error('Error importing videos:', error)
    alert(
      `Ошибка при импорте: ${error.response?.data?.error || error.message || 'Неизвестная ошибка'}`
    )
  } finally {
    isImporting.value = false
  }
}

function formatCount(count: number): string {
  if (count >= 1000000) return (count / 1000000).toFixed(1) + 'M'
  if (count >= 1000) return (count / 1000).toFixed(1) + 'K'
  return count.toString()
}

function formatTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diff < 60) return 'now'
  if (diff < 3600) return Math.floor(diff / 60) + 'm'
  if (diff < 86400) return Math.floor(diff / 3600) + 'h'
  return Math.floor(diff / 86400) + 'd'
}

function goBack() {
  router.push('/')
}

function toggleSearch() {
  searchVisible.value = !searchVisible.value
  if (!searchVisible.value) {
    searchQuery.value = ''
  }
}

async function performSearch() {
  if (!searchQuery.value.trim()) {
    await loadVideos()
    return
  }

  try {
    loading.value = true
    error.value = null

    console.log('=== Performing search ===', searchQuery.value)

    // Search by hashtag
    const results = await videoAPI.getVideosByHashtag(searchQuery.value.trim())
    videos.value = results.map(video => ({
      ...video,
      url: video.video_file,
      thumbnail: video.thumbnail || ''
    }))

    console.log('Search results:', videos.value.length, 'videos')

    currentVideoIndex.value = 0
    await nextTick()
    playCurrentVideo()
  } catch (err: any) {
    console.error('Error searching videos:', err)
    error.value = err.message || 'Failed to search videos. Please try again.'
  } finally {
    loading.value = false
  }
}

function goToUserProfile(userId: number) {
  router.push(`/profile/${userId}`)
}
</script>

<style scoped>
.videos-view {
  height: 100vh;
  background: #000;
  position: relative;
  overflow: hidden;
}

.video-feed {
  height: 100%;
  position: relative;
}

.video-container {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  transition: opacity 0.3s;
}

.video-container.active {
  opacity: 1;
  z-index: 1;
}

.video-player {
  height: 100%;
  width: 100%;
  position: relative;
}

.video-element {
  height: 100%;
  width: 100%;
  object-fit: cover;
  background: #000;
}

.video-hidden {
  position: absolute;
  top: -9999px;
  left: -9999px;
  visibility: hidden;
  pointer-events: none;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
}

.play-icon {
  font-size: 4rem;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.progress-bar-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
  z-index: 10;
}

.progress-bar {
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  transition: width 0.1s linear;
}

.progress-fill {
  height: 100%;
  background: var(--color-accent-cyan, #00e5ff);
}

.video-info {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 5;
}

.top-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), transparent);
}

.back-btn,
.search-btn,
.import-btn,
.lang-btn {
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  pointer-events: all;
  transition: all 0.3s;
}

.back-btn:hover,
.search-btn:hover,
.import-btn:hover {
  background: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.import-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.top-bar-actions {
  display: flex;
  gap: 0.5rem;
}

.section-title {
  color: white;
  font-size: 1.2rem;
  font-weight: 700;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
}

.search-bar {
  position: absolute;
  top: 60px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  padding: 0 1rem;
  width: 90%;
  max-width: 500px;
  z-index: 15;
  pointer-events: all;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  color: white;
  font-size: 0.9rem;
  outline: none;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  border-color: var(--color-accent-cyan, #00e5ff);
}

.search-submit-btn {
  padding: 0.75rem 1.5rem;
  background: var(--color-accent-cyan, #00e5ff);
  border: none;
  border-radius: 25px;
  color: #000;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
}

.search-submit-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
}

.side-actions {
  position: absolute;
  right: 10px;
  bottom: 200px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  pointer-events: all;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.3s;
}

.action-btn:hover {
  transform: scale(1.2);
}

.action-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.5));
}

.action-count {
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.bottom-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 60px;
  padding: 1rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
  pointer-events: all;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00e5ff, #7c4dff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s;
  pointer-events: all;
}

.avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
}

.user-details {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.username {
  font-weight: 600;
  font-size: 0.95rem;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  transition: all 0.3s;
  pointer-events: all;
}

.username:hover {
  color: #00e5ff;
  text-decoration: underline;
  text-shadow: 0 0 10px rgba(0, 229, 255, 0.8);
}

.follow-btn {
  padding: 0.4rem 1rem;
  background: var(--color-accent-cyan, #00e5ff);
  border: none;
  border-radius: 4px;
  color: #000;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
}

.follow-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
}

.following-btn {
  padding: 0.4rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  color: white;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s;
}

.video-description {
  margin-bottom: 1rem;
}

.description-text {
  font-size: 0.95rem;
  line-height: 1.4;
  margin-bottom: 0.5rem;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.video-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  color: #00e5ff;
  font-size: 0.9rem;
  font-weight: 600;
}

.lesson-info {
  background: rgba(0, 229, 255, 0.2);
  border: 1px solid rgba(0, 229, 255, 0.4);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 1rem;
}

.lesson-badge {
  color: #00e5ff;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 0.25rem;
}

.lesson-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.lesson-words {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.lesson-word {
  background: rgba(0, 0, 0, 0.3);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #00e5ff;
}

.music-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.music-icon {
  font-size: 1.5rem;
}

.music-text {
  flex: 1;
}

.music-title {
  font-size: 0.9rem;
  font-weight: 600;
}

.music-artist {
  font-size: 0.8rem;
  opacity: 0.8;
}

.category-filter {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  display: flex;
  gap: 0.5rem;
  padding: 0 1rem;
  overflow-x: auto;
  z-index: 10;
  scrollbar-width: none;
}

.category-filter::-webkit-scrollbar {
  display: none;
}

.category-btn {
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  color: white;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s;
  pointer-events: all;
}

.category-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.category-btn.active {
  background: var(--color-accent-cyan, #00e5ff);
  border-color: #00e5ff;
  color: #000;
}

/* Comments Modal */
.comments-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.comments-content {
  background: #1a1a1a;
  border-radius: 20px 20px 0 0;
  width: 100%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.comments-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comments-header h3 {
  color: white;
  margin: 0;
  font-size: 1.1rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}

.comments-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.comment {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.comment-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00e5ff, #7c4dff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-user {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.comment-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.95rem;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.comment-actions {
  display: flex;
  gap: 1rem;
}

.comment-action {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  cursor: pointer;
  transition: color 0.3s;
}

.comment-action:hover {
  color: white;
}

.translate-action {
  color: #00e5ff !important;
}

.translate-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.comment-translation {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 229, 255, 0.1);
  border-left: 2px solid #00e5ff;
  border-radius: 4px;
}

.translation-header {
  color: #00e5ff;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.translation-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  line-height: 1.4;
}

.reply-input {
  margin-top: 0.75rem;
}

.reply-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  color: white;
  font-size: 0.85rem;
  outline: none;
}

.reply-field::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.reply-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.send-reply-btn {
  padding: 0.4rem 1rem;
  background: var(--color-accent-cyan, #00e5ff);
  border: none;
  border-radius: 15px;
  color: #000;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.send-reply-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
}

.send-reply-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-reply-btn {
  padding: 0.4rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 15px;
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-reply-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.comment-time {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.75rem;
  align-self: flex-start;
}

.comment-input {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  gap: 0.75rem;
}

.comment-field {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: white;
  font-size: 0.95rem;
  outline: none;
}

.comment-field::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.comment-field:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background: var(--color-accent-cyan, #00e5ff);
  border: none;
  border-radius: 20px;
  color: #000;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading State */
.loading-state {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--color-accent-cyan, #00e5ff);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: white;
  margin-top: 1rem;
  font-size: 1rem;
}

/* Empty State */
.empty-state {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #000;
  color: white;
  text-align: center;
  padding: 2rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.empty-text {
  font-size: 1rem;
  opacity: 0.7;
}

/* Error State */
.error-state {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #000;
  color: white;
  text-align: center;
  padding: 2rem;
}

.error-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.error-text {
  font-size: 1rem;
  opacity: 0.7;
  margin-bottom: 1.5rem;
}

.retry-btn {
  padding: 0.75rem 2rem;
  background: var(--color-accent-cyan, #00e5ff);
  border: none;
  border-radius: 25px;
  color: #000;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.retry-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
}
</style>
