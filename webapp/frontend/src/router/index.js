import { createRouter, createWebHistory } from 'vue-router';
import ChatComponent from '../components/ChatComponent.vue';
import LoginComponent from '../components/LoginComponent.vue';
import RegisterComponent from '../components/RegisterComponent.vue';

const routes = [
  { path: '/', component: LoginComponent },
  { path: '/register', component: RegisterComponent },
  { path: '/chat', component: ChatComponent },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
