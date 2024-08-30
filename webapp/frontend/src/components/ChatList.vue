<template>
  <div class="chat-list p-3">
    <div class="list-group">
      <a 
        v-for="user in users"
        :key="user.id"
        href="#"
        class="list-group-item list-group-item-action"
        :class="{ active: activeChat === user.id }"
        @click.prevent="selectChat(user.id)"
      >
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">{{ user.username }}</h5>
          <small>Última mensagem</small> <!-- Substitua "Última mensagem" por um valor dinâmico, se necessário -->
        </div>
        <p class="mb-1">Mensagem de exemplo</p> <!-- Substitua "Mensagem de exemplo" por um valor dinâmico, se necessário -->
      </a>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  props: ['activeChat'],
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/users/');
        this.users = response.data;
      } catch (error) {
        console.error('Erro ao buscar usuários:', error);
      }
    },
    selectChat(userId) {
      this.$emit('selectChat', userId);
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.chat-list {
  width: 25%;
  border-right: 1px solid #ddd;
  padding: 10px;
}
.chat-list .list-group-item {
  cursor: pointer;
}
.chat-list .list-group-item.active {
  background-color: #f0f0f0;
}
</style>

