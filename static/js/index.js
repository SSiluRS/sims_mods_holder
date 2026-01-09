const { createApp } = Vue;

createApp({
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
                const response = await axios.post('/add', { mod_url: this.newModUrl });
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
                const response = await axios.post(`/delete/${mod.id}`);
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
                const response = await axios.post(`/mod/${mod.id}/add_tag/${tag.id}`);
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
                const response = await axios.post(`/mod/${mod.id}/remove_tag/${tag.id}`);
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
        // Инициализация блесток из внешнего файла
        if (typeof initSparkles === 'function') initSparkles('sparkleCanvas');
        
        // Close dropdowns on click outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown') && !e.target.closest('.tag-dropdown') && !e.target.closest('.tag-plus-btn')) {
                this.activeDropdown = null;
                this.activeTagDropdown = null;
            }
        });
    }
}).mount('#app');