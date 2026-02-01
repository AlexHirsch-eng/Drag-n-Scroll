<template>
  <div v-if="authStore.isLoading || !authStore.isInitialized" class="loading-screen">
    <div class="loader"></div>
  </div>
  <router-view v-else />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  // Initialize auth from localStorage
  await authStore.initializeAuth()
})
</script>

<style scoped>
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loader {
  width: 50px;
  height: 50px;
  border: 3px solid var(--color-accent-primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
