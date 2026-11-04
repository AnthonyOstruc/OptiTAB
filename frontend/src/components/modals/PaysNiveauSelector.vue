<template>
  <Modal
    :is-open="isOpen"
    :can-close="false"
    :title="currentStep === 4 ? 'C’est prêt !' : 'Bienvenue sur OptiTAB'"
    :eyebrow="currentStep < 4 ? `Étape ${numeroAffiche} sur ${etapesAffichees.length}` : ''"
    :subtitle="getStepSubtitle()"
    :icon="currentStep === 4 ? CheckCircleIcon : SparklesIcon"
    size="medium"
  >
    <div class="pn">
      <!-- Progression -->
      <ol v-if="currentStep < 4" class="pn-steps" aria-label="Progression">
        <li v-for="(etape, i) in etapesAffichees" :key="etape.nom" :class="{ 'is-done': currentStep > etape.n, 'is-current': currentStep === etape.n }">
          <span class="pn-steps__dot">
            <CheckIcon v-if="currentStep > etape.n" aria-hidden="true" />
            <template v-else>{{ i + 1 }}</template>
          </span>
          {{ etape.nom }}
        </li>
      </ol>

      <!-- Étape 1 : élève ou parent -->
      <div v-if="currentStep === 1" class="pn-step">
        <p class="pn-question">Tu es…</p>
        <div class="pn-grid pn-grid--2">
          <button
            v-for="role in ROLES"
            :key="role.cle"
            type="button"
            :class="['pn-card', { selected: selectedRole === role.cle }]"
            :aria-pressed="selectedRole === role.cle"
            @click="selectRole(role.cle)"
          >
            <span class="pn-card__icon"><component :is="role.icone" aria-hidden="true" /></span>
            <span class="pn-card__text">
              <strong>{{ role.titre }}</strong>
              <small>{{ role.texte }}</small>
            </span>
            <CheckCircleSolid v-if="selectedRole === role.cle" class="pn-card__check" aria-hidden="true" />
          </button>
        </div>
        <div class="pn-actions">
          <span></span>
          <button type="button" class="om-btn om-btn--primary" :disabled="!selectedRole || (loadingPays && currentStep === 1)" @click="nextStep">
            Continuer
            <ArrowRightIcon aria-hidden="true" />
          </button>
        </div>
      </div>

      <!-- Étape 2 : pays -->
      <div v-if="currentStep === 2" class="pn-step">
        <p class="pn-question">Dans quel pays es-tu scolarisé ?</p>
        <p v-if="loadingPays" class="pn-etat">Chargement des pays…</p>
        <div v-else-if="errorPays" class="pn-etat">
          <p class="om-alert om-alert--error">Impossible de charger les pays.</p>
          <button type="button" class="om-btn om-btn--ghost" @click="loadPays">Réessayer</button>
        </div>
        <div v-else class="pn-grid pn-grid--2">
          <button
            v-for="pays in paysAvecCours"
            :key="pays.id"
            type="button"
            :class="['pn-card', { selected: selectedPaysId === pays.id }]"
            :aria-pressed="selectedPaysId === pays.id"
            @click="selectPays(pays)"
          >
            <span class="pn-card__flag" aria-hidden="true">{{ pays.drapeau_emoji }}</span>
            <span class="pn-card__text">
              <strong>{{ pays.nom }}</strong>
              <small>{{ pays.nombre_niveaux || 0 }} classes disponibles</small>
            </span>
            <CheckCircleSolid v-if="selectedPaysId === pays.id" class="pn-card__check" aria-hidden="true" />
          </button>
        </div>
        <div class="pn-actions">
          <button type="button" class="om-btn om-btn--ghost" @click="previousStep">
            <ArrowLeftIcon aria-hidden="true" />
            Retour
          </button>
          <button type="button" class="om-btn om-btn--primary" :disabled="!selectedPaysId || loadingNiveaux" @click="nextStep">
            {{ loadingNiveaux ? 'Chargement…' : 'Continuer' }}
            <ArrowRightIcon v-if="!loadingNiveaux" aria-hidden="true" />
          </button>
        </div>
      </div>

      <!-- Étape 3 : classe -->
      <div v-if="currentStep === 3" class="pn-step">
        <p class="pn-question">En quelle classe{{ selectedPays?.nom ? ` (${selectedPays.nom})` : '' }} ?</p>
        <p v-if="loadingNiveaux" class="pn-etat">Chargement des classes…</p>
        <p v-else-if="niveaux.length === 0" class="pn-etat">Aucune classe disponible pour ce pays.</p>
        <div v-else class="pn-grid pn-grid--classes">
          <button
            v-for="niveau in niveaux"
            :key="niveau.id"
            type="button"
            :class="['pn-classe', { selected: selectedNiveauId === niveau.id }]"
            :aria-pressed="selectedNiveauId === niveau.id"
            @click="selectNiveau(niveau)"
          >
            {{ niveau.nom_local || niveau.nom }}
          </button>
        </div>
        <div class="pn-actions">
          <button type="button" class="om-btn om-btn--ghost" @click="previousStep">
            <ArrowLeftIcon aria-hidden="true" />
            Retour
          </button>
          <button type="button" class="om-btn om-btn--primary" :disabled="!selectedNiveauId || saving" @click="saveConfiguration">
            {{ saving ? 'Enregistrement…' : 'Terminer' }}
          </button>
        </div>
      </div>

      <!-- Étape 4 : confirmation -->
      <div v-if="currentStep === 4" class="pn-step">
        <dl class="pn-summary">
          <div><dt>Profil</dt><dd>{{ selectedRole === 'student' ? 'Élève' : 'Parent' }}</dd></div>
          <div><dt>Pays</dt><dd>{{ selectedPays?.nom }}</dd></div>
          <div><dt>Classe</dt><dd>{{ selectedNiveau?.nom_local || selectedNiveau?.nom }}</dd></div>
        </dl>
        <p class="pn-redirect">Tu vas être redirigé vers ton espace…</p>
      </div>
    </div>
  </Modal>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from '@/composables/useToast'
import Modal from '@/components/common/Modal.vue'
import { AcademicCapIcon, ArrowLeftIcon, ArrowRightIcon, CheckCircleIcon, CheckIcon, SparklesIcon, UsersIcon } from '@heroicons/vue/24/outline'
import { CheckCircleIcon as CheckCircleSolid } from '@heroicons/vue/24/solid'
import { getPaysActifs, getPaysNiveaux } from '@/api/pays.js'
import { updateUserPaysNiveau, updateUserRole } from '@/api/users.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['configuration-complete', 'close'])

const ROLES = [
  { cle: 'student', titre: 'Élève', texte: 'J’apprends et je m’entraîne sur OptiTAB', icone: AcademicCapIcon },
  { cle: 'parent', titre: 'Parent', texte: 'Je suis la progression de mon enfant', icone: UsersIcon }
]

const userStore = useUserStore()
const { showToast } = useToast()

// États réactifs
const currentStep = ref(1)
const selectedRole = ref(null)
const paysDisponibles = ref([])
const niveaux = ref([])
const selectedPaysId = ref(null)
const selectedNiveauId = ref(null)
const loadingPays = ref(false)
const loadingNiveaux = ref(false)
const errorPays = ref(false)
const saving = ref(false)

// Seuls les pays qui ont des classes (donc des cours) sont proposés. S'il n'y en
// a qu'un, l'étape « Pays » est sautée : il est choisi d'office.
const paysAvecCours = computed(() => paysDisponibles.value.filter((p) => Number(p.nombre_niveaux) > 0))
const paysUnique = computed(() => (paysAvecCours.value.length === 1 ? paysAvecCours.value[0] : null))
const etapesAffichees = computed(() => [
  { n: 1, nom: 'Profil' },
  ...(paysUnique.value ? [] : [{ n: 2, nom: 'Pays' }]),
  { n: 3, nom: 'Classe' }
])
const numeroAffiche = computed(() => Math.max(1, etapesAffichees.value.findIndex((e) => e.n === currentStep.value) + 1))

const selectedPays = computed(() => 
  paysDisponibles.value.find(p => p.id === selectedPaysId.value)
)

const selectedNiveau = computed(() => 
  niveaux.value.find(n => n.id === selectedNiveauId.value)
)

// Méthodes
const getStepSubtitle = () => {
  switch (currentStep.value) {
    case 1: return `${paysUnique.value ? 'Deux' : 'Trois'} questions rapides pour te proposer les bons cours et exercices.`
    case 2: return 'Les programmes suivent le système scolaire de ton pays.'
    case 3: return 'Tu pourras changer de classe plus tard depuis ton compte.'
    case 4: return 'Ton espace est prêt.'
    default: return ''
  }
}

const loadPays = async () => {
  try {
    loadingPays.value = true
    errorPays.value = false
    
    const response = await getPaysActifs()
    paysDisponibles.value = response.data || response
    
  } catch (error) {
    console.error('Erreur lors du chargement des pays:', error)
    errorPays.value = true
    showToast('Erreur lors du chargement des pays', 'error')
  } finally {
    loadingPays.value = false
  }
}

const loadNiveauxPourPays = async (paysId) => {
  if (!paysId) {
    niveaux.value = []
    return
  }

  try {
    loadingNiveaux.value = true
    const response = await getPaysNiveaux(paysId)
    niveaux.value = response.data || response
  } catch (error) {
    console.error('Erreur lors du chargement des niveaux:', error)
    niveaux.value = []
    showToast('Erreur lors du chargement des niveaux', 'error')
  } finally {
    loadingNiveaux.value = false
  }
}

const selectPays = (pays) => {
  selectedPaysId.value = pays.id
  selectedNiveauId.value = null
}

const selectNiveau = (niveau) => {
  selectedNiveauId.value = niveau.id
}

const selectRole = (role) => {
  selectedRole.value = role
}

const nextStep = async () => {
  if (currentStep.value === 1 && selectedRole.value) {
    if (paysDisponibles.value.length === 0) await loadPays()
    if (paysUnique.value) {
      selectPays(paysUnique.value)
      currentStep.value = 3
      loadNiveauxPourPays(paysUnique.value.id)
      return
    }
    currentStep.value = 2
  } else if (currentStep.value === 2 && selectedPaysId.value) {
    currentStep.value = 3
    loadNiveauxPourPays(selectedPaysId.value)
  }
}

const previousStep = () => {
  if (currentStep.value === 2) {
    currentStep.value = 1
  } else if (currentStep.value === 3) {
    currentStep.value = paysUnique.value ? 1 : 2
    niveaux.value = []
    selectedNiveauId.value = null
  }
}

const saveConfiguration = async () => {
  if (!selectedRole.value || !selectedPaysId.value || !selectedNiveauId.value) return
  
  try {
    saving.value = true
    
    // Sauvegarder le rôle (élève/parent)
    await updateUserRole(selectedRole.value)
    
    // Sauvegarder pays et niveau
    await updateUserPaysNiveau(selectedPaysId.value, selectedNiveauId.value)
    
    // Mettre à jour le store utilisateur
    await userStore.fetchUser()
    
    // Passer à l'étape de confirmation
    currentStep.value = 4
    
    showToast('Configuration enregistrée avec succès !', 'success')
    
    // Attendre un peu puis émettre la fin
    setTimeout(() => {
      emit('configuration-complete')
    }, 2000)
    
  } catch (error) {
    console.error('Erreur lors de la sauvegarde:', error)
    showToast('Erreur lors de l\'enregistrement de la configuration', 'error')
  } finally {
    saving.value = false
  }
}

// Watchers
watch(() => props.isOpen, (isOpen) => {
  if (isOpen && paysDisponibles.value.length === 0) {
    loadPays()
  }
})

watch(selectedPaysId, (newPaysId) => {
  if (newPaysId && currentStep.value === 3) {
    loadNiveauxPourPays(newPaysId)
  }
})

// Lifecycle
onMounted(() => {
  if (props.isOpen) {
    loadPays()
  }
})
</script>

<style scoped>
/* Éléments communs (.om-btn, .om-alert) : components/common/Modal.vue */
.pn-steps {
  display: flex;
  gap: 8px;
  margin: -4px 0 24px;
  padding: 0;
  list-style: none;
}

.pn-steps li {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 12px;
  background: var(--om-bg-soft);
  color: var(--om-muted);
  font-size: 13.5px;
  font-weight: 600;
}

.pn-steps li.is-current {
  background: var(--om-navy-50);
  color: var(--om-navy);
}

.pn-steps li.is-done {
  color: var(--om-green-700);
}

.pn-steps__dot {
  display: inline-grid;
  flex-shrink: 0;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #fff;
  font-size: 12.5px;
}

.pn-steps li.is-current .pn-steps__dot {
  background: var(--om-navy);
  color: #fff;
}

.pn-steps li.is-done .pn-steps__dot {
  background: var(--om-green-700);
  color: #fff;
}

.pn-steps__dot svg {
  width: 14px;
  height: 14px;
}

.pn-question {
  margin: 0 0 14px;
  color: var(--om-ink);
  font-size: 17px;
  font-weight: 700;
}

.pn-grid {
  display: grid;
  gap: 12px;
}

.pn-grid--2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.pn-grid--classes {
  grid-template-columns: repeat(auto-fill, minmax(118px, 1fr));
  gap: 8px;
}

.pn-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border: 1.5px solid var(--om-line);
  border-radius: 16px;
  background: #fff;
  color: var(--om-ink);
  font-family: var(--om-font);
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

.pn-card:hover {
  border-color: var(--om-navy-100);
  box-shadow: 0 6px 18px rgba(16, 32, 79, 0.08);
}

.pn-card.selected {
  border-color: var(--om-navy);
  background: var(--om-navy-50);
}

.pn-card:focus-visible,
.pn-classe:focus-visible {
  outline: 2px solid var(--om-navy);
  outline-offset: 2px;
}

.pn-card__icon {
  display: inline-grid;
  flex-shrink: 0;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--om-navy-50);
  color: var(--om-navy);
}

.pn-card.selected .pn-card__icon {
  background: #fff;
}

.pn-card__icon svg {
  width: 24px;
  height: 24px;
}

.pn-card__flag {
  font-size: 30px;
  line-height: 1;
}

.pn-card__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.pn-card__text strong {
  font-size: 16px;
}

.pn-card__text small {
  color: var(--om-muted);
  font-size: 13.5px;
  line-height: 1.4;
}

.pn-card__check {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 22px;
  height: 22px;
  color: var(--om-navy);
}

.pn-classe {
  min-height: 48px;
  padding: 0 10px;
  border: 1.5px solid var(--om-line);
  border-radius: 12px;
  background: #fff;
  color: var(--om-ink);
  font: 600 15px/1.2 var(--om-font);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, color 0.2s;
}

.pn-classe:hover {
  border-color: var(--om-navy);
}

.pn-classe.selected {
  border-color: var(--om-navy);
  background: var(--om-navy);
  color: #fff;
}

.pn-etat {
  margin: 8px 0;
  color: var(--om-muted);
}

.pn-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 26px;
}

.pn-summary {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 16px 18px;
  border-radius: 16px;
  background: var(--om-bg-soft);
}

.pn-summary div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.pn-summary dt {
  color: var(--om-muted);
}

.pn-summary dd {
  margin: 0;
  color: var(--om-ink);
  font-weight: 700;
}

.pn-redirect {
  margin: 16px 0 0;
  color: var(--om-muted);
  font-size: 14px;
  text-align: center;
}

@media (max-width: 520px) {
  .pn-grid--2 {
    grid-template-columns: 1fr;
  }

  .pn-steps li {
    justify-content: center;
    font-size: 0;
  }

  .pn-steps__dot {
    font-size: 12.5px;
  }

  .pn-actions .om-btn {
    flex: 1;
  }
}
</style>
