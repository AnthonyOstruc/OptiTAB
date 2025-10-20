<template>
  <div class="chatgpt-container">
    <!-- Header -->
    <div class="chat-header">
      <div class="header-info">
        <div class="ai-avatar">
          <span class="avatar-icon">🤖</span>
        </div>
        <div class="header-text">
          <h3>Assistant IA OptiTAB</h3>
          <span class="status">
            <span class="status-dot" :class="{ online: !isLoading }"></span>
            {{ isLoading ? 'En train d\'écrire...' : 'En ligne' }}
          </span>
        </div>
      </div>
      <div class="header-actions">
        <button @click="clearChat" class="clear-btn" title="Nouvelle conversation">
          🗑️
        </button>
      </div>
    </div>

    <!-- Messages Area -->
    <div class="messages-container" ref="messagesContainer">
      <!-- Message de bienvenue -->
      <div v-if="messages.length === 0" class="welcome-message">
        <div class="welcome-content">
          <h4>👋 Bonjour ! Je suis votre assistant pédagogique IA</h4>
          <p>Je peux vous aider avec vos questions de mathématiques en me basant sur les exercices et cours disponibles dans OptiTAB.</p>

          <!-- Message de connexion si pas authentifié -->
          <div v-if="!getAuthToken()" class="auth-warning">
            <p>⚠️ <strong>Connexion requise :</strong> Connectez-vous pour utiliser l'assistant IA</p>
          </div>

          <div class="suggestions">
            <p>Essayez de me demander :</p>
            <div class="suggestion-tags">
              <span @click="sendSuggestion('Explique-moi les dérivées')" class="tag">Explique-moi les dérivées</span>
              <span @click="sendSuggestion('Donne-moi un exercice sur les intégrales')" class="tag">Exercice sur les intégrales</span>
              <span @click="sendSuggestion('Comment résoudre une équation du second degré')" class="tag">Équation du second degré</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Messages -->
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-wrapper"
        :class="{ 'user-message': message.role === 'user', 'ai-message': message.role === 'assistant' }"
      >
        <div class="message-avatar">
          <span v-if="message.role === 'user'" class="avatar-icon user">👤</span>
          <span v-else class="avatar-icon ai">🤖</span>
        </div>
        <div class="message-content">
          <div class="message-bubble">
            <div v-if="message.role === 'user'" class="message-text">
              {{ message.content }}
            </div>
            <div v-else class="message-text" v-html="formatMessage(message.content)"></div>
            <div v-if="message.role === 'assistant' && message.tokens" class="message-meta">
              <span class="tokens-info">{{ message.tokens }} tokens utilisés</span>
            </div>
          </div>
          <div v-if="message.role === 'assistant'" class="message-time">
            {{ formatTime(message.timestamp) }}
          </div>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="isLoading" class="message-wrapper ai-message">
        <div class="message-avatar">
          <span class="avatar-icon ai">🤖</span>
        </div>
        <div class="message-content">
          <div class="message-bubble typing">
            <div class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="input-container">
      <div class="input-wrapper">
        <textarea
          v-model="currentMessage"
          @keydown.enter.exact.prevent="simpleSend"
          @keydown.enter.shift.exact="addNewLine"
          placeholder="Posez votre question sur les mathématiques... (Enter pour envoyer)"
          class="message-input"
          :disabled="isLoading"
          rows="1"
          ref="messageInput"
        ></textarea>
        <button
          @click="simpleSend"
          class="send-btn"
          :disabled="!currentMessage.trim() || isLoading"
          :class="{ active: currentMessage.trim() }"
          title="Envoyer le message"
        >
          <span v-if="isLoading" class="loading-spinner">⏳</span>
          <span v-else>📤</span>
        </button>
      </div>

    </div>

    <!-- Error Toast -->
    <div v-if="error" class="error-toast">
      <span class="error-icon">⚠️</span>
      <span>{{ error }}</span>
      <button @click="error = null" class="error-close">✕</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AIAssistant',
  props: {
    autoFocus: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentMessage: '',
      selectedModel: 'gpt-3.5-turbo',
      messages: [],
      isLoading: false,
      error: null,
      conversationId: null
    }
  },
  watch: {
    currentMessage: {
      handler() {
        this.$nextTick(() => {
          this.autoResizeTextarea()
        })
      }
    }
  },
  async mounted() {
    await this.loadConversationHistory()

    if (this.autoFocus && this.$refs.messageInput) {
      this.$nextTick(() => {
        this.$refs.messageInput.focus()
      })
    }
  },
  methods: {
    async sendMessage(event) {
      console.log('Send button clicked', event) // Debug log

      if (!this.currentMessage.trim() || this.isLoading) {
        console.log('Cannot send: empty message or loading', {
          message: this.currentMessage.trim(),
          isLoading: this.isLoading
        })
        return
      }

      console.log('Sending message:', this.currentMessage.trim())

      const userMessage = {
        role: 'user',
        content: this.currentMessage.trim(),
        timestamp: new Date()
      }

      // Ajouter le message utilisateur
      this.messages.push(userMessage)
      const messageToSend = this.currentMessage.trim()
      this.currentMessage = ''

      // Scroll to bottom
      this.$nextTick(() => {
        this.scrollToBottom()
      })

      // Envoyer à l'IA
      await this.sendToAI(messageToSend)
    },

    async sendSuggestion(suggestion) {
      this.currentMessage = suggestion
      await this.sendMessage()
    },

    async sendToAI(message) {
      this.isLoading = true
      this.error = null

      try {
        const response = await axios.post('/api/ai/ask/', {
          message: message,
          model: this.selectedModel
        }, {
          headers: {
            'Authorization': `Bearer ${this.getAuthToken()}`
          }
        })

        const aiMessage = {
          role: 'assistant',
          content: response.data.ai_response,
          timestamp: new Date(),
          tokens: response.data.tokens_used
        }

        this.messages.push(aiMessage)

        // Scroll to bottom après la réponse
        this.$nextTick(() => {
          this.scrollToBottom()
        })

      } catch (error) {
        console.error('Erreur IA:', error)
        this.error = error.response?.data?.error ||
                     error.response?.data?.message ||
                     'Erreur lors de la requête IA'

        // Ajouter un message d'erreur dans le chat
        const errorMessage = {
          role: 'assistant',
          content: 'Désolé, une erreur s\'est produite. Veuillez réessayer.',
          timestamp: new Date(),
          isError: true
        }
        this.messages.push(errorMessage)
      } finally {
        this.isLoading = false
      }
    },

    async loadConversationHistory() {
      try {
        const token = this.getAuthToken()
        console.log('Token d\'authentification:', token ? 'Présent' : 'Absent')

        if (!token) {
          console.warn('Pas de token d\'authentification, historique non chargé')
          console.log('Vérifiez que vous êtes connecté à l\'application')
          console.log('Le token devrait être dans localStorage sous la clé "access_token"')
          return
        }

        const response = await axios.get('/api/ai/history/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })

        // Debug log
        console.log('Historique chargé:', response.data)
        console.log('Status HTTP:', response.status)

        // Convertir l'historique en format de messages
        this.messages = []

        // Vérifier que response.data est un tableau
        if (Array.isArray(response.data)) {
          console.log(`Chargement de ${response.data.length} conversations`)
          response.data.forEach((conv, index) => {
            console.log(`Conversation ${index}:`, conv)
            this.messages.push({
              role: 'user',
              content: conv.message,
              timestamp: new Date(conv.created_at)
            })
            this.messages.push({
              role: 'assistant',
              content: conv.ai_response,
              timestamp: new Date(conv.created_at),
              tokens: conv.tokens_used
            })
          })
        } else if (response.data && typeof response.data === 'object') {
          // Si c'est un objet paginé ou autre structure
          console.warn('Structure de réponse inattendue:', response.data)
          if (response.data.results && Array.isArray(response.data.results)) {
            response.data.results.forEach(conv => {
              this.messages.push({
                role: 'user',
                content: conv.message,
                timestamp: new Date(conv.created_at)
              })
              this.messages.push({
                role: 'assistant',
                content: conv.ai_response,
                timestamp: new Date(conv.created_at),
                tokens: conv.tokens_used
              })
            })
          }
        } else {
          console.warn('Aucune donnée d\'historique ou format incorrect:', response.data)
        }

        console.log(`Total messages chargés: ${this.messages.length}`)

        this.$nextTick(() => {
          this.scrollToBottom()
        })
      } catch (error) {
        console.error('Erreur chargement historique:', error)

        // Gestion spécifique des erreurs
        if (error.response) {
          console.error('Erreur HTTP:', error.response.status, error.response.data)
          if (error.response.status === 401) {
            console.warn('Utilisateur non authentifié')
          } else if (error.response.status === 403) {
            console.warn('Accès interdit')
          }
        } else if (error.request) {
          console.error('Erreur réseau:', error.request)
        } else {
          console.error('Erreur inconnue:', error.message)
        }

        // En cas d'erreur, on continue sans historique
        this.messages = []
      }
    },


    clearChat() {
      this.messages = []
      this.conversationId = null
    },

    addNewLine() {
      this.currentMessage += '\n'
    },

    scrollToBottom() {
      if (this.$refs.messagesContainer) {
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight
      }
    },

    autoResizeTextarea() {
      const textarea = this.$refs.messageInput
      if (textarea) {
        textarea.style.height = 'auto'
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
      }
    },

    formatMessage(content) {
      // Convertir les retours à la ligne en HTML
      return content.replace(/\n/g, '<br>')
    },

    formatTime(date) {
      return date.toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getAuthToken() {
      // Utiliser la même clé que le reste de l'application
      return localStorage.getItem('access_token') || ''
    }
  }
}
</script>

<style scoped>
.chatgpt-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* Header */
.chat-header {
  background: white;
  border-bottom: 1px solid #e9ecef;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.avatar-icon {
  font-size: 18px;
}

.header-text h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6c757d;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #dc3545;
  transition: background 0.3s;
}

.status-dot.online {
  background: #28a745;
}

.clear-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #6c757d;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #f8f9fa;
  color: #495057;
}

/* Messages Area */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scroll-behavior: smooth;
}

.welcome-message {
  align-self: center;
  max-width: 600px;
  margin: 40px 0;
}

.welcome-content {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.welcome-content h4 {
  margin: 0 0 12px 0;
  color: #2c3e50;
  font-size: 18px;
}

.welcome-content p {
  margin: 0 0 20px 0;
  color: #6c757d;
  line-height: 1.5;
}

.auth-warning {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 12px 16px;
  margin: 0 0 20px 0;
}

.auth-warning p {
  margin: 0;
  color: #856404;
  font-weight: 500;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.tag {
  background: #e9ecef;
  color: #495057;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.tag:hover {
  background: #007bff;
  color: white;
  transform: translateY(-1px);
}

/* Messages */
.message-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar-icon.user {
  background: linear-gradient(135deg, #007bff, #0056b3);
}

.avatar-icon.ai {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.message-content {
  flex: 1;
  max-width: calc(100% - 52px);
}

.message-bubble {
  background: white;
  padding: 12px 16px;
  border-radius: 18px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
}

.user-message .message-bubble {
  background: #007bff;
  color: white;
  margin-left: auto;
  max-width: 70%;
}

.ai-message .message-bubble {
  background: white;
  color: #2c3e50;
  margin-right: auto;
  max-width: 80%;
}

.message-text {
  line-height: 1.5;
  word-wrap: break-word;
}

.message-meta {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tokens-info {
  font-size: 11px;
  color: #6c757d;
  font-style: italic;
}

.message-time {
  font-size: 11px;
  color: #6c757d;
  margin-top: 4px;
  text-align: right;
}

/* Typing Indicator */
.typing .typing-dots {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing .typing-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #6c757d;
  animation: typing 1.4s infinite ease-in-out;
}

.typing .typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing .typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* Input Area */
.input-container {
  background: white;
  border-top: 1px solid #e9ecef;
  padding: 16px 20px;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  margin-bottom: 12px;
}

.message-input {
  flex: 1;
  border: 1px solid #dee2e6;
  border-radius: 24px;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.4;
  resize: none;
  outline: none;
  transition: border-color 0.2s;
  max-height: 120px;
  overflow-y: auto;
}

.message-input:focus {
  border-color: #007bff;
}

.message-input::placeholder {
  color: #6c757d;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: #e9ecef;
  color: #6c757d;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.send-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.send-btn.active {
  background: #007bff;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}


/* Error Toast */
.error-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #dc3545;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 1000;
  max-width: 300px;
}

.error-close {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
  margin-left: 8px;
}

/* Responsive */
@media (max-width: 768px) {
  .chatgpt-container {
    border-radius: 0;
  }

  .chat-header {
    padding: 12px 16px;
  }

  .messages-container {
    padding: 16px;
  }

  .input-container {
    padding: 12px 16px;
  }

  .message-bubble {
    padding: 10px 14px;
  }

  .welcome-content {
    padding: 24px 20px;
  }

  .suggestion-tags {
    flex-direction: column;
    align-items: center;
  }

  .tag {
    text-align: center;
  }
}
</style>
