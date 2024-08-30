<template>
    <div class="chat-container">
      <div class="user-list">
        <div
          v-for="user in users"
          :key="user.id"
          @click="selectUser(user)"
          :class="{ active: selectedUser && selectedUser.id === user.id }"
        >
          {{ user.username }}
        </div>
      </div>
      <div class="chat-messages">
        <div v-for="message in messages" :key="message.id" class="chat-message">
          <div :class="message.user_id === userId ? 'message-outgoing' : 'message-incoming'">
            <div class="message-content">{{ message.message }}</div>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" type="text" placeholder="Digite sua mensagem..." @keyup.enter="sendMessage" />
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    data() {
      return {
        userId: null, // Este ID deve ser recuperado do estado do usuário logado
        users: [],
        selectedUser: null,
        messages: [],
        newMessage: '',
        socket: null,
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
      selectUser(user) {
        this.selectedUser = user;
        this.fetchConversations(user.id);
      },
      async fetchConversations(userId) {
        try {
          const response = await axios.get(`/users/${userId}/conversations/`);
          this.messages = response.data;
        } catch (error) {
          console.error('Erro ao buscar conversas:', error);
        }
      },
      connectWebSocket() {
        this.socket = new WebSocket(`ws://127.0.0.1:8002/ws/${this.userId}`);
  
        this.socket.onmessage = (event) => {
          const message = JSON.parse(event.data);
          this.messages.push(message);
        };
  
        this.socket.onclose = () => {
          console.log('WebSocket fechado.');
        };
      },
      sendMessage() {
        if (this.newMessage.trim() !== '') {
          const message = {
            user_id: this.userId,
            message: this.newMessage,
          };
          this.socket.send(JSON.stringify(message));
          this.newMessage = '';
        }
      },
    },
    mounted() {
      this.fetchUsers();
      this.connectWebSocket();
    },
  };
  </script>
  
  <style scoped>
  /* Seus estilos aqui */
  </style>
  