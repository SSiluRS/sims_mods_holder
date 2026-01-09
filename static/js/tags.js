const { createApp } = Vue;

createApp({
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
                const response = await axios.get('/api/tags');
                this.tags = response.data.tags.map(tag => ({
                    ...tag,
                    editName: tag.name // поле для редактирования
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
                const response = await axios.post('/add_tag', { tag_name: this.newTagName });
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
                const response = await axios.post(`/edit_tag/${tag.id}`, { tag_name: tag.editName });
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
                const response = await axios.post(`/delete_tag/${tag.id}`);
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
        // Инициализация блесток из внешнего файла
        if (typeof initSparkles === 'function') initSparkles('sparkleCanvas');
    }
}).mount('#app');