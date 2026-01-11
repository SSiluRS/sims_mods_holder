<template>
  <div class="app-container">
    <div class="main-content">
      <router-view></router-view>
    </div>
    <footer class="app-footer">
      <p>Sims Mods Holder {{ displayVersion }}</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const version = ref('...');
const environment = ref('');

const displayVersion = computed(() => {
  if (version.value === '...') return '...';
  if (version.value === 'unknown') return 'v.unknown';
  
  const vPrefix = version.value === 'latest' ? '' : 'v';
  const envSuffix = environment.value ? ` (${environment.value})` : '';
  
  return `${vPrefix}${version.value}${envSuffix}`;
});

onMounted(async () => {
  try {
    const response = await axios.get('/api/version');
    version.value = response.data.version;
    // Доверяем бэкенду: если он говорит production, скрываем плашку.
    // Если говорит что-то другое (development, testing) - показываем.
    environment.value = response.data.environment !== 'production' ? response.data.environment : '';
  } catch (e) {
    version.value = 'unknown';
  }
});
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
}

.app-footer {
  text-align: center;
  padding: 10px;
  font-size: 0.8rem;
  color: #666;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
}
</style>