<template>
    <div>
    <header>
        <h1>
            <img src="/header.png" alt="📁" width="60" style="vertical-align: middle; margin-right: 10px;">
            Мои моды для Sims 4
        </h1>
        <canvas id="sparkleCanvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;"></canvas>
        <div class="header-actions">
            <router-link to="/tags" class="header-tag-btn">🏷️ Управление тегами</router-link>
            <div class="header-form-wrapper">
                <form @submit.prevent="addMod" class="header-form">
                    <input type="url" v-model="newModUrl" 
                        placeholder="https://sims-market.ru/mod/..." required>
                    <button type="submit" :disabled="loading">+ Добавить мод</button>
                </form>
            </div>
        </div>
    </header>

    <!-- Отображение активного фильтра -->
    <div class="filter-indicator" v-if="activeFilters.length > 0">
        <span class="filter-text">Фильтр:
            <span v-for="(tag, index) in activeFilterTags" :key="tag.id">
                {{ tag.name }}<span v-if="index < activeFilterTags.length - 1">, </span>
            </span>
        </span>
        <button @click="clearFilters" class="filter-clear-btn">×</button>
    </div>

    <!-- Flash-сообщения -->
    <div class="flash-container" v-if="flashMessage">
        <div :class="'flash-' + flashType">{{ flashMessage }}</div>
    </div>

    <main class="cards-container">
        <div class="card" v-for="mod in filteredMods" :key="mod.id">
            <!-- Кнопка "три точки" в правом верхнем углу -->
            <div class="card-actions">
                <div class="dropdown">
                    <button class="dropdown-btn" @click.stop="toggleDropdown(mod.id)">⋮</button>
                    <div class="dropdown-content" :class="{ show: activeDropdown === mod.id }">
                        <!-- Открыть на Sims-Market -->
                        <a :href="mod.url" target="_blank" class="dropdown-item">
                            🌐 Открыть на Sims-Market
                        </a>
                        <!-- Ссылка для скачивания -->
                        <a href="#" class="dropdown-item" 
                           @click.prevent="downloadMod(mod.download_url)">
                            ⬇️ Скачать ZIP
                        </a>
                        <!-- Кнопка удаления -->
                        <a href="#" class="dropdown-item delete-btn" 
                           @click.prevent="deleteMod(mod)">
                            🗑 Удалить мод
                        </a>
                    </div>
                </div>
            </div>
            
            <img :src="mod.image" :alt="mod.title" 
                 onerror="this.src='https://via.placeholder.com/250x150?text=No+Image'">
            
            <div class="card-content">
                <!-- Верхняя часть (заголовок) -->
                <div class="content-top">
                    <h2>{{ mod.title }}</h2>                       
                </div>
                
                <!-- Нижняя часть (ссылки и кнопки) -->
                <div class="content-bottom">
                    <!-- Теги и плюсик в одной строке -->
                    <div class="assigned-tags">
                        <div class="assigned-tag-container" v-for="tag in mod.tags" :key="tag.id">
                            <span class="assigned-tag" @click="toggleFilter(tag.id)" :class="{ 'active-filter-tag': activeFilters.includes(tag.id) }">
                                {{ tag.name }}
                                <span class="assigned-tag-delete" @click.stop="removeTagFromMod(mod, tag)">×</span>
                            </span>
                        </div>
                        
                        <!-- Плюсик в стиле тега -->
                        <button class="tag-plus-btn" @click.stop="toggleTagDropdown(mod.id)">+</button>
                        <div class="tag-dropdown" :class="{ show: activeTagDropdown === mod.id }">
                            <button type="button" class="tag-item" 
                                    v-for="tag in availableTags(mod)" :key="tag.id"
                                    @click="addTagToMod(mod, tag)">
                                {{ tag.name }}
                            </button>
                        </div>
                    </div>                    
                </div>
            </div>
        </div>
        
        <p class="empty" v-if="filteredMods.length === 0 && mods.length > 0">
                Нет модов с выбранными тегами. 
                <a href="#" @click.prevent="clearFilters">Показать все</a>
        </p>
        <p class="empty" v-if="mods.length === 0 && !loading">
                Нет добавленных модов. Добавьте первый!
        </p>
    </main>
    </div>
</template>

<script>
import axios from 'axios';
import { initSparkles } from '../utils/sparkles';

export default {
    data() {
        return {
            mods: [],
            allTags: [],
            newModUrl: '',
            activeFilters: [],
            activeDropdown: null,
            activeTagDropdown: null,
            flashMessage: '',
            flashType: 'success',
            loading: false
        }
    },
    computed: {
        filteredMods() {
            if (this.activeFilters.length === 0) {
                return this.mods;
            }
            return this.mods.filter(mod => {
                const modTagIds = mod.tags.map(t => t.id);
                return this.activeFilters.every(filterId => modTagIds.includes(filterId));
            });
        },
        activeFilterTags() {
            return this.allTags.filter(tag => this.activeFilters.includes(tag.id));
        }
    },
    methods: {
        async fetchData() {
            try {
                const response = await axios.get('/api/data');
                this.mods = response.data.mods;
                this.allTags = response.data.tags;
            } catch (error) {
                this.showFlash('Ошибка загрузки данных', 'danger');
            }
        },
        async addMod() {
            if (!this.newModUrl) return;
            this.loading = true;
            try {
                const response = await axios.post('/api/mods', { mod_url: this.newModUrl });
                if (response.data.success) {
                    this.showFlash(response.data.message, 'success');
                    this.newModUrl = '';
                    await this.fetchData();
                } else {
                    this.showFlash(response.data.message, 'danger');
                }
            } catch (error) {
                this.showFlash('Ошибка при добавлении мода', 'danger');
            } finally {
                this.loading = false;
            }
        },
        async deleteMod(mod) {
            if (!confirm(`Удалить мод "${mod.title}"?`)) return;
            try {
                const response = await axios.delete(`/api/mods/${mod.id}`);
                if (response.data.success) {
                    this.showFlash(response.data.message, 'success');
                    this.mods = this.mods.filter(m => m.id !== mod.id);
                } else {
                    this.showFlash(response.data.message, 'danger');
                }
            } catch (error) {
                this.showFlash('Ошибка при удалении', 'danger');
            }
        },
        async addTagToMod(mod, tag) {
            try {
                const response = await axios.post(`/api/mods/${mod.id}/tags/${tag.id}`);
                if (response.data.success) {
                    mod.tags.push({ id: tag.id, name: tag.name });
                    this.showFlash(response.data.message, 'success');
                    this.activeTagDropdown = null;
                }
            } catch (error) {
                this.showFlash('Ошибка при добавлении тега', 'danger');
            }
        },
        async removeTagFromMod(mod, tag) {
            if (!confirm('Удалить тег из этого мода?')) return;
            try {
                const response = await axios.delete(`/api/mods/${mod.id}/tags/${tag.id}`);
                if (response.data.success) {
                    mod.tags = mod.tags.filter(t => t.id !== tag.id);
                    this.showFlash(response.data.message, 'success');
                }
            } catch (error) {
                this.showFlash('Ошибка при удалении тега', 'danger');
            }
        },
        toggleFilter(tagId) {
            if (this.activeFilters.includes(tagId)) {
                this.activeFilters = this.activeFilters.filter(id => id !== tagId);
            } else {
                this.activeFilters.push(tagId);
            }
        },
        clearFilters() {
            this.activeFilters = [];
        },
        toggleDropdown(modId) {
            this.activeDropdown = this.activeDropdown === modId ? null : modId;
            this.activeTagDropdown = null;
        },
        toggleTagDropdown(modId) {
            this.activeTagDropdown = this.activeTagDropdown === modId ? null : modId;
            this.activeDropdown = null;
        },
        availableTags(mod) {
            const modTagIds = mod.tags.map(t => t.id);
            return this.allTags.filter(t => !modTagIds.includes(t.id));
        },
        downloadMod(url) {
            if (!url) {
                alert('Ссылка для скачивания отсутствует');
                return;
            }
            window.open(url, '_blank');
        },
        showFlash(message, type) {
            this.flashMessage = message;
            this.flashType = type;
            setTimeout(() => {
                this.flashMessage = '';
            }, 3000);
        }
    },
    mounted() {
        this.fetchData();
        initSparkles('sparkleCanvas');
        
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown') && !e.target.closest('.tag-dropdown') && !e.target.closest('.tag-plus-btn')) {
                this.activeDropdown = null;
                this.activeTagDropdown = null;
            }
        });
    }
}
</script>