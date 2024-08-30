<template>
  <div class="chat-window">
    <div class="message-container" id="message-container">
      <div
        v-for="message in localMessages"
        :key="message.id"
        class="d-flex mb-3"
        :class="{
          'justify-content-end': message.type === 'sent',
          'justify-content-start': message.type === 'received'
        }"
      >
        <div
          class="message-bubble"
          :class="{
            'bg-primary text-white': message.type === 'sent',
            'bg-light': message.type === 'received',
            'font-weight-bold': !isTabActive && message.type === 'received' && message.isNew
          }"
        >
          <p class="mb-1">{{ message.text }}</p>
          <small class="text-muted">{{ message.time }}</small>
        </div>
      </div>
    </div>
    <div class="chat-input">
      <div class="input-group">
        <input
          type="text"
          class="form-control"
          placeholder="Digite uma mensagem..."
          v-model="newMessage"
          @keyup.enter="sendMessage"
        />
        <button class="btn btn-primary" type="button" @click="sendMessage">Enviar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    userId: Number,
    selectedUser: Object,
    messages: {
      type: Array,
      default: () => [], // Garante que messages seja um array
    },
  },
  data() {
    return {
      newMessage: '',
      localMessages: [],
      isTabActive: true,
      socket: null,
    };
  },
  watch: {
    messages: {
      immediate: true,
      handler(newMessages) {
        if (Array.isArray(newMessages)) {
          this.localMessages = [...newMessages].map(msg => ({ ...msg, isNew: true }));
          if (!this.isTabActive) {
            this.updateTitleNotification();
          }
        } else {
          console.error('O valor de messages não é um array.');
        }
      },
    },
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() === '') return;

      const message = {
        user_id: this.userId,
        text: this.newMessage,
        type: 'sent',
        time: 'Agora',
      };

      this.localMessages.push(message);
      this.newMessage = '';

      // Simulando envio de mensagem via WebSocket
      if (this.socket) {
        this.socket.send(JSON.stringify(message));
      }

      this.$nextTick(() => {
        const container = document.getElementById('message-container');
        container.scrollTop = container.scrollHeight;
      });
    },
    updateTitleNotification() {
      document.title = '🔔 Nova mensagem!';
    },
    resetTitleNotification() {
      document.title = 'Chat App';
    },
    handleVisibilityChange() {
      this.isTabActive = !document.hidden;
      if (this.isTabActive) {
        this.resetTitleNotification();
        this.markMessagesAsRead();
      }
    },
    markMessagesAsRead() {
      this.localMessages.forEach(message => {
        if (message.type === 'received') {
          message.isNew = false;
        }
      });
    },
    connectWebSocket() {
      if (this.socket) {
        this.socket.close();
      }
      this.socket = new WebSocket(`ws://127.0.0.1:8002/ws/${this.userId}`);

      this.socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        this.localMessages.push(message);
      };

      this.socket.onclose = () => {
        console.log('WebSocket fechado.');
      };
    },
  },
  created() {
    document.addEventListener('visibilitychange', this.handleVisibilityChange);
    this.connectWebSocket();
  },
  beforeUnmount() {
    document.removeEventListener('visibilitychange', this.handleVisibilityChange);
    if (this.socket) {
      this.socket.close();
    }
  },
};
</script>

<style scoped>
.chat-window {
  width: 70%;
  display: flex;
  flex-direction: column;
}

.message-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f1f1f1;
}

.message-bubble {
  max-width: 70%;
  padding: 10px;
  border-radius: 15px;
  position: relative;
  word-wrap: break-word;
}

.chat-input {
  border-top: 1px solid #ddd;
  padding: 10px;
}

.font-weight-bold {
  font-weight: bold;
}

/* Estilos para balões de mensagem com "triângulos" */
.message-bubble::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  border-style: solid;
}

/* Triângulo para mensagens enviadas (balões à direita) */
.bg-primary.text-white::after {
  border-width: 8px 0 8px 10px;
  border-color: transparent transparent transparent #007bff;
  right: -10px;
  top: 10px;
}

/* Triângulo para mensagens recebidas (balões à esquerda) */
.bg-light::after {
  border-width: 8px 10px 8px 0;
  border-color: transparent #f8f9fa transparent transparent;
  left: -10px;
  top: 10px;
}
</style>
