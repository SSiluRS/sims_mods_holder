<template>
    <div>
    <header>
        <h1>🏷️ Управление тегами</h1>
        <canvas id="sparkleCanvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;"></canvas>
        <router-link to="/" class="back-link">← Вернуться к модам</router-link>
    </header>

    <main class="container">
        <!-- Форма добавления тега -->
        <div class="tag-form">
            <h2>Добавить новый тег</h2>
            <form @submit.prevent="addTag">
                <div class="form-group">
                    <input type="text" v-model="newTagName" placeholder="Название тега (минимум 2 символа)" 
                           required maxlength="50">
                </div>
                <button type="submit" class="tag-btn tag-btn-add">+ Добавить тег</button>
            </form>
        </div>

        <!-- Список тегов -->
        <div class="tags-list">
            <h2>Существующие теги ({{ tags.length }})</h2>
            
            <div class="flash-container" v-if="flashMessage">
                <div :class="'flash-' + flashType">{{ flashMessage }}</div>
            </div>
            
            <div v-if="tags.length > 0">
                <table class="tags-table">
                    <thead>
                        <tr>
                            <th>Название</th>
                            <th>Действия</th>
                            <th>Дата создания</th>
                            <th>Удаление</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="tag in tags" :key="tag.id">
                            <td>
                                <span class="tag-link">{{ tag.name }}</span>
                            </td>
                            <td>
                                <form @submit.prevent="editTag(tag)" class="edit-form" style="display:flex; gap:5px;">
                                    <input type="text" v-model="tag.editName" 
                                        class="tag-input" maxlength="50">
                                    <button type="submit" class="tag-btn tag-btn-save">💾</button>
                                </form>
                            </td>
                            <td>{{ tag.created_at || 'N/A' }}</td>
                            <td>
                                <button @click="deleteTag(tag)" class="tag-btn tag-btn-delete">🗑️</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p class="empty">Нет созданных тегов. Добавьте первый!</p>
            </div>
        </div>
    </main>
    </div>
</template>

<script>
import api from '../utils/api';
import { initSparkles } from '../utils/sparkles';

export default {
    data() {
        return {
            tags: [],
            newTagName: '',
            flashMessage: '',
            flashType: 'success'
        }
    },
    methods: {
        async fetchTags() {
            try {
                const response = await api.get('/api/tags');
                this.tags = response.data.tags.map(tag => ({
                    ...tag,
                    editName: tag.name 
                }));
            } catch (error) {
                this.showFlash('Ошибка загрузки тегов', 'danger');
            }
        },
        async addTag() {
            if (this.newTagName.length < 2) {
                alert('Название тега должно содержать минимум 2 символа');
                return;
            }
            try {
                const response = await api.post('/api/tags', { tag_name: this.newTagName });
                if (response.data.success) {
                    this.showFlash(response.data.message, 'success');
                    this.newTagName = '';
                    await this.fetchTags();
                } else {
                    this.showFlash(response.data.message, 'danger');
                }
            } catch (error) {
                this.showFlash('Ошибка при добавлении', 'danger');
            }
        },
        async editTag(tag) {
            if (tag.editName.length < 2) {
                alert('Название тега должно содержать минимум 2 символа');
                return;
            }
            try {
                const response = await api.put(`/api/tags/${tag.id}`, { tag_name: tag.editName });
                if (response.data.success) {
                    tag.name = tag.editName;
                    this.showFlash(response.data.message, 'success');
                } else {
                    this.showFlash(response.data.message, 'danger');
                }
            } catch (error) {
                this.showFlash('Ошибка при редактировании', 'danger');
            }
        },
        async deleteTag(tag) {
            if (!confirm(`Удалить тег "${tag.name}"? Все связанные моды потеряют этот тег.`)) return;
            try {
                const response = await api.delete(`/api/tags/${tag.id}`);
                if (response.data.success) {
                    this.tags = this.tags.filter(t => t.id !== tag.id);
                    this.showFlash(response.data.message, 'success');
                } else {
                    this.showFlash(response.data.message, 'danger');
                }
            } catch (error) {
                this.showFlash('Ошибка при удалении', 'danger');
            }
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
        this.fetchTags();
        initSparkles('sparkleCanvas');
    }
}
</script>