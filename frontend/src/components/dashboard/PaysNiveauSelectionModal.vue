<template>
  <Modal
    :is-open="modelValue"
    title="Changer de classe"
    subtitle="Ton pays, ta classe et ton type de compte : tout le contenu s’adapte."
    :icon="AcademicCapIcon"
    :can-close="!saving"
    size="medium"
    @close="closeModal"
  >
    <p v-if="selectionRestricted" class="om-alert om-alert--info config-lock">
      <LockClosedIcon aria-hidden="true" />
      <span><strong>Classes de ton abonnement :</strong> {{ restrictedLabels }}. Contacte l’équipe OptiTAB pour en ajouter d’autres.</span>
    </p>

    <!-- 1. Pays -->
    <section class="config-step">
      <h3 class="config-step__title"><span>1</span> Pays</h3>
      <p v-if="loadingPays" class="config-empty" role="status">Chargement des pays…</p>
      <p v-else-if="paysDisponibles.length === 0" class="config-empty">Aucun pays disponible pour le moment.</p>
      <div v-else class="config-grid">
        <SelectionCard
          v-for="pays in paysDisponibles"
          :key="pays.id"
          :item="pays"
          type="pays"
          :is-selected="selectedPaysId === pays.id"
          :is-current="userPays?.id === pays.id"
          @select="selectPays"
          @hover="prefetchNiveaux"
        />
      </div>
    </section>

    <!-- 2. Classe -->
    <section v-if="selectedPaysId" class="config-step">
      <h3 class="config-step__title"><span>2</span> Classe</h3>
      <p v-if="loadingNiveaux" class="config-empty">Chargement des classes…</p>
      <p v-else-if="!filteredNiveaux || filteredNiveaux.length === 0" class="config-empty">Aucune classe disponible pour ce pays.</p>
      <div v-else class="config-grid">
        <SelectionCard
          v-for="niveau in filteredNiveaux"
          :key="niveau.id"
          :item="niveau"
          type="niveau"
          :is-selected="selectedNiveauId === niveau.id"
          :is-current="userNiveau?.id === niveau.id"
          @select="selectNiveau"
        />
      </div>
    </section>

    <!-- 3. Type de compte -->
    <section class="config-step">
      <h3 class="config-step__title"><span>3</span> Type de compte</h3>
      <div class="config-roles" role="group" aria-label="Type de compte">
        <button type="button" :class="['config-role', { active: selectedRole === 'student' }]" :aria-pressed="selectedRole === 'student'" @click="selectRole('student')">Élève</button>
        <button type="button" :class="['config-role', { active: selectedRole === 'parent' }]" :aria-pressed="selectedRole === 'parent'" @click="selectRole('parent')">Parent</button>
      </div>
    </section>

    <template #footer>
      <button type="button" class="om-btn om-btn--ghost" :disabled="saving" @click="closeModal">Annuler</button>
      <button type="button" class="om-btn om-btn--primary" :disabled="!canSave || saving" @click="saveConfiguration">
        {{ saving ? 'Enregistrement…' : 'Enregistrer' }}
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { computed } from 'vue'
import { AcademicCapIcon, LockClosedIcon } from '@heroicons/vue/24/outline'
import Modal from '@/components/common/Modal.vue'
import { useUserStore } from '@/stores/user'
import SelectionCard from '@/components/common/SelectionCard.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  paysList: {
    type: Array,
    default: () => []
  },
  filteredNiveaux: {
    type: Array,
    default: () => []
  },
  loadingNiveaux: {
    type: Boolean,
    default: false
  },
  loadingPays: {
    type: Boolean,
    default: false
  },
  selectedPaysId: {
    type: Number,
    default: null
  },
  selectedNiveauId: {
    type: Number,
    default: null
  },
  userPays: {
    type: Object,
    default: null
  },
  userNiveau: {
    type: Object,
    default: null
  },
  currentStep: {
    type: String,
    default: 'pays'
  },
  canSave: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  },
  selectedRole: {
    type: String,
    default: 'student'
  },
  selectionRestricted: {
    type: Boolean,
    default: false
  },
  restrictedLevels: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'select-pays', 'select-niveau', 'select-role', 'save', 'prefetch-niveaux'])

// Store utilisateur pour vérifier les permissions admin
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const closeModal = () => {
  emit('update:modelValue', false)
}

const selectPays = (pays) => {
  emit('select-pays', pays)
}

const selectNiveau = (niveau) => {
  emit('select-niveau', niveau)
}

const saveConfiguration = () => {
  emit('save')
}

// Masquer les pays sans aucun niveau (sauf le pays actuel de l'utilisateur)
const paysDisponibles = computed(() =>
  (props.paysList || []).filter(pays => pays.nombre_niveaux !== 0 || props.userPays?.id === pays.id)
)

const restrictedLevels = computed(() => props.restrictedLevels || [])
const selectionRestricted = computed(() => props.selectionRestricted && restrictedLevels.value.length > 0)
const restrictedLabels = computed(() => {
  if (!restrictedLevels.value.length) return 'actuel'
  return restrictedLevels.value.map(level => level.label).join(', ')
})

const prefetchNiveaux = (pays) => {
  emit('prefetch-niveaux', pays?.id || pays)
}

const selectedRole = computed(() => props.selectedRole)
const selectRole = (role) => emit('select-role', role)

</script>

<style scoped>
/* Éléments communs (.om-btn, .om-alert) : components/common/Modal.vue */
.config-lock {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 20px;
}

.config-lock svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-top: 1px;
}

.config-step + .config-step {
  margin-top: 24px;
}

.config-step__title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 12px;
  color: var(--om-ink);
  font-size: 16px;
  font-weight: 700;
}

.config-step__title span {
  display: inline-grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--om-navy-50);
  color: var(--om-navy);
  font-size: 13px;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
}

.config-empty {
  margin: 0;
  color: var(--om-muted);
}

.config-roles {
  display: inline-flex;
  gap: 4px;
  padding: 4px;
  border-radius: 999px;
  background: var(--om-bg-soft);
}

.config-role {
  min-height: 42px;
  padding: 0 22px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: var(--om-ink-soft);
  font: 600 15px/1 var(--om-font);
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
}

.config-role.active {
  background: #fff;
  color: var(--om-navy);
  box-shadow: 0 2px 8px rgba(16, 32, 79, 0.12);
}

.config-role:focus-visible {
  outline: 2px solid var(--om-navy);
  outline-offset: 2px;
}
</style>
