<template>
  <div class="config-card">
    <div class="config-header">
      <div class="config-info">
        <h3>Configuration</h3>
        <p>Votre pays et niveau scolaire</p>
      </div>
      <button @click="$emit('edit')" class="btn-configure">
        <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Modifier
      </button>
    </div>
    
    <div class="current-config">
      <div class="config-item">
        <div class="config-label">Pays</div>
        <div class="config-value">
          <span class="flag">{{ userPays?.drapeau_emoji }}</span>
          <span>{{ userPays?.nom }}</span>
        </div>
      </div>
      <div class="config-divider"></div>
      <div class="config-item">
        <div class="config-label">Niveau</div>
        <div class="config-value">
          <div class="niveau-badge">
            {{ userNiveau?.nom }}
          </div>
        </div>
      </div>
      <div class="config-divider"></div>
      <div class="config-item">
        <div class="config-label">Rôle</div>
        <div class="config-value">
          <div class="role-badge" :class="userRole === 'parent' ? 'parent' : 'student'">
            {{ userRole === 'parent' ? 'Parent' : 'Élève' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  userPays: {
    type: Object,
    default: null
  },
  userNiveau: {
    type: Object,
    default: null
  },
  userRole: {
    type: String,
    default: 'student'
  }
})

defineEmits(['edit'])
</script>

<style scoped>
.config-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.config-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.config-info h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.config-info p {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.btn-configure {
  background: #f9fafb;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-configure:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.icon {
  width: 16px;
  height: 16px;
}

.current-config {
  display: flex;
  align-items: center;
  gap: 24px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
}

.config-item {
  flex: 1;
  background: #f8fafc;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #e2e8f0;
}

.config-label {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.config-value {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1e293b;
  font-size: 15px;
}

.flag {
  font-size: 22px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.niveau-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.role-badge {
  background: #eef2ff;
  color: #1e293b;
  padding: 6px 12px;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 600;
}
.role-badge.parent {
  background: #fff7ed;
  color: #9a3412;
}

.config-divider {
  width: 2px;
  height: 40px;
  background: linear-gradient(to bottom, #e2e8f0, #cbd5e1, #e2e8f0);
  border-radius: 1px;
}

@media (max-width: 768px) {
  .current-config {
    flex-direction: column;
    gap: 16px;
  }
  
  .config-divider {
    width: 100%;
    height: 1px;
  }
}
</style>
