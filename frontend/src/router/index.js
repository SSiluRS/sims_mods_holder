import { createRouter, createWebHistory } from 'vue-router'
import ModsView from '../components/ModsView.vue'
import TagsView from '../components/TagsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ModsView
    },
    {
      path: '/tags',
      name: 'tags',
      component: TagsView
    }
  ]
})

export default router