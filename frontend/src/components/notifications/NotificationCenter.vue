<template>
  <div class="notification-center">
    <!-- Bouton de notification avec badge -->
    <button 
      class="notification-trigger"
      :class="{ 'has-notifications': hasUnread }"
      @click="togglePanel"
      aria-label="Notifications"
      title="Notifications"
    >
      <BellIcon class="notification-icon" />
      <span 
        v-if="unreadCount > 0" 
        class="notification-badge"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <!-- Panel des notifications -->
    <Transition name="notification-panel">
      <div 
        v-if="isOpen" 
        class="notification-panel"
        @click.stop
      >
        <!-- Header du panel -->
        <div class="notification-header">
          <h3 class="notification-title">Notifications</h3>
          <div class="notification-actions">
            <button 
              v-if="hasUnread"
              @click="markAllAsRead"
              class="btn-mark-all-read"
              title="Tout marquer comme lu"
            >
              ✓ Tout lire
            </button>
            <button 
              @click="handleClearAll"
              class="btn-clear-all"
              title="Effacer tout"
            >
              🗑️
            </button>
            <button 
              @click="closePanel"
              class="btn-close"
              title="Fermer"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Liste des notifications -->
        <div class="notification-list">
          <TransitionGroup name="notification-item" tag="div">
            <div 
              v-for="notification in notifications"
              :key="notification.id"
              class="notification-item"
              :class="[
                `type-${notification.type}`,
                { 'unread': !notification.read }
              ]"
              @click="handleNotificationClick(notification)"
            >
              <!-- Icône selon le type -->
              <div class="notification-item-icon">
                <span class="icon">{{ getNotificationIcon(notification.type) }}</span>
              </div>

              <!-- Contenu -->
              <div class="notification-item-content">
                <h4 class="notification-item-title">{{ notification.title }}</h4>
                <p class="notification-item-message">{{ notification.message }}</p>
                <time class="notification-item-time">
                  {{ formatTime(notification.timestamp) }}
                </time>
              </div>

              <!-- Indicateur non lu -->
              <div v-if="!notification.read" class="unread-indicator"></div>

              <!-- Bouton fermer -->
              <button 
                @click.stop="handleRemove(notification.id)"
                class="btn-remove-notification"
                title="Supprimer"
              >
                ✕
              </button>
            </div>
          </TransitionGroup>

          <!-- Message vide -->
          <div v-if="notifications.length === 0" class="notification-empty">
            <div class="empty-icon">🔔</div>
            <p class="empty-message">Aucune notification</p>
            <p class="empty-subtitle">Vous recevrez des notifications pour vos progrès !</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Overlay pour fermer -->
    <div 
      v-if="isOpen" 
      class="notification-overlay"
      @click="closePanel"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { BellIcon } from '@heroicons/vue/24/outline'
import { useNotificationStore } from '@/stores/notifications'
import { deleteNotification, deleteAllNotifications } from '@/api/users'

const notificationStore = useNotificationStore()

// État local
const isOpen = ref(false)

// Computed depuis le store
const notifications = computed(() => notificationStore.notifications)
const unreadCount = computed(() => notificationStore.unreadCount)
const hasUnread = computed(() => notificationStore.hasUnread)

// Méthodes du panel
function togglePanel() {
  isOpen.value = !isOpen.value
}

function openPanel() {
  isOpen.value = true
}

function closePanel() {
  isOpen.value = false
}

// Actions du store
const { markAsRead, markAllAsRead, removeNotification, clearAll, loadFromServer } = notificationStore

// Gestion des clics sur les notifications
async function handleNotificationClick(notification) {
  if (!notification.read) {
    try {
      await markAsRead(notification.id)
    } catch (error) {
      console.warn('⚠️ Erreur lors du marquage de la notification:', error)
    }
  }
  
  // Actions spécifiques selon le type
  switch (notification.type) {
    case 'level_up':
      // Optionnel: naviguer vers le profil/dashboard
      break
    case 'exercise_unlocked':
      // Optionnel: naviguer vers l'exercice
      break
    case 'xp_gained':
      // Optionnel: naviguer vers les stats
      break
  }
}

async function handleRemove(id) {
  removeNotification(id)
  try {
    await deleteNotification(id)
  } catch (_) {}
}

async function handleClearAll() {
  clearAll()
  try {
    await deleteAllNotifications()
  } catch (_) {}
}

// Utilitaires
function getNotificationIcon(type) {
  const icons = {
    xp_gained: '⭐',
    level_up: '🏆', 
    exercise_unlocked: '🔓',
    chapter_completed: '✅',
    achievement: '🏅',
    daily_streak: '🔥'
  }
  return icons[type] || '🔔'
}

function formatTime(timestamp) {
  const now = new Date()
  const time = new Date(timestamp)
  const diffMs = now - time
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMins < 1) return 'À l\'instant'
  if (diffMins < 60) return `Il y a ${diffMins}min`
  if (diffHours < 24) return `Il y a ${diffHours}h`
  if (diffDays < 7) return `Il y a ${diffDays}j`
  
  return time.toLocaleDateString('fr-FR', { 
    day: 'numeric', 
    month: 'short' 
  })
}

// Fermer avec Escape
function handleKeyDown(event) {
  if (event.key === 'Escape' && isOpen.value) {
    closePanel()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
  try { loadFromServer() } catch (_) {}
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
/* Bouton de déclenchement */
.notification-trigger {
  position: relative;
  background: none;
  border: none;
  font-size: 1.35rem;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s ease;
  padding: 0.5rem;
  border-radius: 8px;
}

.notification-trigger:hover {
  color: #2563eb;
  background: #f1f5f9;
  transform: translateY(-1px);
}

.notification-trigger.has-notifications {
  color: #2563eb;
  animation: pulse-notification 2s infinite;
}

.notification-icon {
  width: 1.7rem;
  height: 1.7rem;
}

/* Badge de notifications */
.notification-badge {
  position: absolute;
  top: 0.2rem;
  right: 0.2rem;
  background: #ef4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.1rem 0.35rem;
  border-radius: 10px;
  min-width: 1rem;
  height: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* Panel des notifications */
.notification-panel {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  width: 380px;
  max-height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
  z-index: 1000;
  overflow: hidden;
}

/* Header du panel */
.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  background: #fafafa;
}

.notification-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.notification-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-mark-all-read,
.btn-clear-all,
.btn-close {
  background: none;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #6b7280;
}

.btn-mark-all-read:hover {
  background: #e0f2fe;
  color: #0369a1;
}

.btn-clear-all:hover {
  background: #fef2f2;
  color: #dc2626;
}

.btn-close:hover {
  background: #f3f4f6;
  color: #374151;
}

/* Liste des notifications */
.notification-list {
  max-height: 400px;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.notification-list::-webkit-scrollbar {
  width: 4px;
}

.notification-list::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

/* Items de notification */
.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f9fafb;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.notification-item:hover {
  background: #f8fafc;
}

.notification-item.unread {
  background: #f0f9ff;
  border-left: 3px solid #2563eb;
}

.notification-item-icon {
  flex-shrink: 0;
  margin-right: 0.75rem;
  margin-top: 0.1rem;
}

.notification-item-icon .icon {
  font-size: 1.2rem;
  display: block;
}

.notification-item-content {
  flex: 1;
  min-width: 0;
}

.notification-item-title {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.3;
}

.notification-item-message {
  margin: 0 0 0.4rem 0;
  font-size: 0.85rem;
  color: #4b5563;
  line-height: 1.4;
}

.notification-item-time {
  font-size: 0.75rem;
  color: #9ca3af;
}

.unread-indicator {
  position: absolute;
  top: 0.5rem;
  right: 2.5rem;
  width: 8px;
  height: 8px;
  background: #2563eb;
  border-radius: 50%;
}

.btn-remove-notification {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  margin-left: 0.5rem;
  opacity: 0;
}

.notification-item:hover .btn-remove-notification {
  opacity: 1;
}

.btn-remove-notification:hover {
  background: #fef2f2;
  color: #dc2626;
}

/* Types de notifications */
.notification-item.type-xp_gained .notification-item-icon .icon {
  color: #f59e0b;
}

.notification-item.type-level_up .notification-item-icon .icon {
  color: #8b5cf6;
}

.notification-item.type-exercise_unlocked .notification-item-icon .icon {
  color: #10b981;
}

.notification-item.type-chapter_completed .notification-item-icon .icon {
  color: #06b6d4;
}

.notification-item.type-achievement .notification-item-icon .icon {
  color: #f59e0b;
}

.notification-item.type-daily_streak .notification-item-icon .icon {
  color: #ef4444;
}

/* État vide */
.notification-empty {
  text-align: center;
  padding: 2rem 1rem;
  color: #9ca3af;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.empty-message {
  margin: 0 0 0.25rem 0;
  font-weight: 500;
  color: #6b7280;
}

.empty-subtitle {
  margin: 0;
  font-size: 0.85rem;
  color: #9ca3af;
}

/* Overlay */
.notification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 999;
  background: transparent;
}

/* Animations */
@keyframes pulse-notification {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Transitions du panel */
.notification-panel-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.notification-panel-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.notification-panel-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.notification-panel-leave-to {
  opacity: 0;
  transform: translateY(-5px) scale(0.98);
}

/* Transitions des items */
.notification-item-enter-active {
  transition: all 0.4s ease;
}

.notification-item-leave-active {
  transition: all 0.3s ease;
}

.notification-item-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.notification-item-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.notification-item-move {
  transition: transform 0.3s ease;
}

/* Responsive */
@media (max-width: 480px) {
  .notification-panel {
    width: calc(100vw - 2rem);
    right: 1rem;
    left: 1rem;
  }
}
</style>
