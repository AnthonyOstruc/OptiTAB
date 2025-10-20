<template>
  <div class="pays-niveaux-display">
    <!-- Affichage groupé par pays -->
    <div v-if="groupedNiveaux.length > 0" class="pays-groups">
      <div 
        v-for="group in groupedNiveaux" 
        :key="group.pays.id"
        class="pays-group"
      >
        <div class="pays-header">
          <span class="pays-flag">{{ group.pays.drapeau_emoji }}</span>
          <span class="pays-name">{{ group.pays.nom }}</span>
        </div>
        <div class="niveaux-list">
          <span 
            v-for="niveau in group.niveaux" 
            :key="niveau.id"
            class="niveau-badge-small"
            :style="{ backgroundColor: niveau.couleur || '#6366f1' }"
          >
            {{ niveau.nom }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- Fallback : affichage simple si les données de pays ne sont pas disponibles -->
    <div v-else-if="niveaux && niveaux.length > 0" class="simple-niveaux">
      <span 
        v-for="niveau in niveaux" 
        :key="niveau.id"
        class="niveau-badge-small"
        :style="{ backgroundColor: niveau.couleur || '#6366f1' }"
      >
        {{ niveau.nom }}
      </span>
    </div>
    
    <!-- Aucun niveau -->
    <span v-else class="no-niveaux">
      {{ noNiveauxText }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  niveaux: {
    type: Array,
    default: () => []
  },
  noNiveauxText: {
    type: String,
    default: 'Aucun niveau'
  }
})

// Grouper les niveaux par pays (robuste aux différentes formes de données)
const groupedNiveaux = computed(() => {
  if (!props.niveaux || props.niveaux.length === 0) return []

  const groups = {}

  props.niveaux.forEach((niveau) => {
    const paysObj = typeof niveau.pays === 'object' && niveau.pays !== null ? niveau.pays : null
    const paysId = paysObj?.id ?? niveau.pays_id ?? niveau.pays ?? 'unknown'
    const paysNom = niveau.pays_nom ?? paysObj?.nom ?? `Pays ${paysId}`
    const paysEmoji = niveau.pays_drapeau ?? paysObj?.drapeau_emoji ?? '🏳️'

    const key = String(paysId)
    if (!groups[key]) {
      groups[key] = {
        pays: { id: paysId, nom: paysNom, drapeau_emoji: paysEmoji },
        niveaux: []
      }
    }

    groups[key].niveaux.push(niveau)
  })

  return Object.values(groups)
})
</script>

<style scoped>
.pays-niveaux-display {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pays-groups {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.simple-niveaux {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.pays-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.pays-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
}

.pays-flag {
  font-size: 1rem;
}

.pays-name {
  color: #1f2937;
}

.niveaux-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-left: 1.5rem;
}

.niveau-badge-small {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 0.65rem;
  font-weight: 500;
  text-align: center;
  min-width: 40px;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.no-niveaux {
  color: #6b7280;
  font-style: italic;
  font-size: 0.9rem;
  padding: 0.5rem;
  text-align: center;
  background: #f9fafb;
  border-radius: 4px;
}

/* Version compacte pour les petits espaces */
.pays-niveaux-display.compact .pays-group {
  flex-direction: row;
  align-items: center;
  padding: 0.25rem 0.5rem;
}

.pays-niveaux-display.compact .niveaux-list {
  margin-left: 0.5rem;
}

@media (max-width: 768px) {
  .pays-group {
    flex-direction: column;
  }
  
  .niveaux-list {
    margin-left: 0;
  }
}
</style>
