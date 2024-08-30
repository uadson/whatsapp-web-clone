<template>
  <div id="app" class="app-container">
    <ChatList :selectedUser="selectedUser" @select-user="handleUserSelect" />
    <ChatWindow :selectedUser="selectedUser" :userId="userId" />
  </div>
</template>

<script>
import ChatList from './components/ChatList.vue';
import ChatWindow from './components/ChatWindow.vue';

export default {
  components: {
    ChatList,
    ChatWindow,
  },
  data() {
    return {
      selectedUser: null,
      userId: 1, // ID do usuário logado, por exemplo, do estado global ou de autenticação
    };
  },
  methods: {
    handleUserSelect(user) {
      this.selectedUser = user;
    },
  },
};
</script>

<style>
.app-container {
  display: flex;
  height: 100vh;
}
</style>
