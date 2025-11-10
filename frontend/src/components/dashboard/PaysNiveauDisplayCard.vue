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
  width: 100%;
}

.config-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.config-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: #111827;
}

.config-info p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.btn-configure {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-configure:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.icon {
  width: 1rem;
  height: 1rem;
}

.current-config {
  display: grid;
  grid-template-columns: auto 2px auto 2px auto;
  align-items: center;
  gap: 1.25rem;
  background: #f9fafb;
  border-radius: 10px;
  padding: 1.25rem;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.config-value {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #111827;
  font-size: 0.9375rem;
}

.flag {
  font-size: 1.375rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.niveau-badge {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  padding: 0.375rem 0.875rem;
  border-radius: 1.25rem;
  font-size: 0.8125rem;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(99, 102, 241, 0.3);
}

.role-badge {
  background: #e0e7ff;
  color: #4338ca;
  padding: 0.375rem 0.75rem;
  border-radius: 0.875rem;
  font-size: 0.8125rem;
  font-weight: 600;
}

.role-badge.parent {
  background: #fed7aa;
  color: #9a3412;
}

.config-divider {
  width: 1px;
  height: 2.5rem;
  background: #d1d5db;
  border-radius: 1px;
}

@media (max-width: 768px) {
  .config-header {
    margin-bottom: 1rem;
  }

  .config-info h3 {
    font-size: 1.0625rem;
  }

  .config-info p {
    font-size: 0.8125rem;
  }

  .btn-configure {
    padding: 0.5625rem 0.9375rem;
    font-size: 0.8125rem;
  }

  .current-config {
    grid-template-columns: 1fr;
    gap: 0.875rem;
    padding: 1.125rem;
  }
  
  .config-divider {
    display: none;
  }

  .config-label {
    font-size: 0.65rem;
  }

  .config-value {
    font-size: 0.875rem;
  }

  .flag {
    font-size: 1.25rem;
  }

  .niveau-badge,
  .role-badge {
    font-size: 0.8rem;
    padding: 0.35rem 0.8125rem;
  }
}

@media (max-width: 640px) {
  .config-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.875rem;
    margin-bottom: 0.875rem;
  }

  .config-info h3 {
    font-size: 1rem;
  }

  .config-info p {
    font-size: 0.8rem;
  }

  .btn-configure {
    width: 100%;
    justify-content: center;
    padding: 0.625rem 1rem;
    font-size: 0.8125rem;
  }

  .current-config {
    gap: 0.75rem;
    padding: 1rem;
    border-radius: 9px;
  }

  .config-item {
    gap: 0.4rem;
  }

  .config-label {
    font-size: 0.625rem;
  }

  .config-value {
    font-size: 0.8125rem;
  }

  .flag {
    font-size: 1.125rem;
  }

  .niveau-badge {
    font-size: 0.75rem;
    padding: 0.3125rem 0.75rem;
  }

  .role-badge {
    font-size: 0.75rem;
    padding: 0.3125rem 0.6875rem;
  }
}

@media (max-width: 480px) {
  .config-header {
    gap: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .config-info h3 {
    font-size: 0.9375rem;
  }

  .config-info p {
    font-size: 0.75rem;
  }

  .btn-configure {
    padding: 0.5625rem 0.9375rem;
    font-size: 0.8rem;
    gap: 0.4rem;
  }

  .icon {
    width: 0.9375rem;
    height: 0.9375rem;
  }

  .current-config {
    gap: 0.625rem;
    padding: 0.9375rem;
    border-radius: 8px;
  }

  .config-label {
    font-size: 0.6rem;
  }

  .config-value {
    font-size: 0.8rem;
    gap: 0.4rem;
  }

  .flag {
    font-size: 1.0625rem;
  }

  .niveau-badge {
    font-size: 0.7rem;
    padding: 0.3rem 0.6875rem;
    border-radius: 1rem;
  }

  .role-badge {
    font-size: 0.7rem;
    padding: 0.3rem 0.625rem;
    border-radius: 0.75rem;
  }
}

@media (max-width: 380px) {
  .config-header {
    gap: 0.625rem;
  }

  .config-info h3 {
    font-size: 0.875rem;
  }

  .config-info p {
    font-size: 0.7rem;
  }

  .btn-configure {
    padding: 0.5rem 0.875rem;
    font-size: 0.75rem;
  }

  .current-config {
    padding: 0.875rem;
  }

  .config-label {
    font-size: 0.5625rem;
  }

  .config-value {
    font-size: 0.75rem;
  }

  .flag {
    font-size: 1rem;
  }

  .niveau-badge,
  .role-badge {
    font-size: 0.6875rem;
    padding: 0.25rem 0.625rem;
  }
}
</style>
