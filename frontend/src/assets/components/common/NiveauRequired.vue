<template>
  <div class="niveau-required">
    <div class="blocked-content">
      <div class="blocked-icon">🔒</div>
      <h2>Niveau requis</h2>
      <p>Vous devez sélectionner votre niveau scolaire pour accéder à cette section.</p>
      <button @click="goToDashboard" class="btn-primary">
        Choisir mon niveau
      </button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'NiveauRequired',
  setup() {
    const router = useRouter()
    
    const goToDashboard = () => {
      router.push({ name: 'Dashboard' })
    }
    
    return {
      goToDashboard
    }
  }
}
</script>

<style scoped>
.niveau-required {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 2rem;
}

.blocked-content {
  text-align: center;
  max-width: 400px;
  background: white;
  border-radius: 16px;
  padding: 3rem 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 2px solid #e5e7eb;
}

.blocked-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.blocked-content h2 {
  margin: 0 0 1rem 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
}

.blocked-content p {
  margin: 0 0 2rem 0;
  color: #6b7280;
  line-height: 1.6;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}
</style> 