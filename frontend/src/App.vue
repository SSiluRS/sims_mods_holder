<template>
  <div class="app-container">
    <div class="main-content">
      <router-view></router-view>
    </div>
    <footer class="app-footer">
      <p>Sims Mods Holder v{{ version }} <span v-if="environment">({{ environment }})</span></p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const version = ref('...');
const environment = ref('');

onMounted(async () => {
  try {
    const response = await axios.get('/api/version');
    version.value = response.data.version;
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