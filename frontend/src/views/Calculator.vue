<template>
  <DashboardLayout @subject-changed="handleSubjectChange">
    <section class="calc">
      <h2 class="title"><CalculatorIcon class="title-icon"/> Outil de Calcul Scientifique</h2>

      <!-- Sous-header avec onglets d'opérations -->
      <div class="operations-tabs">
        <button 
          v-for="operation in operations" 
          :key="operation.id"
          :class="['operation-tab', { active: selectedOperation === operation.id }]"
          @click="selectOperation(operation.id)"
          :title="operation.description"
        >
          <component :is="operation.icon" class="operation-icon" />
          <span class="operation-label">{{ operation.name }}</span>
        </button>
      </div>

      <div class="display" ref="preview" style="margin:1.2rem auto 1.5rem auto;"></div>
      <div class="expr-row">
        <div class="expr-box">
          <!-- Champs de bornes pour les intégrales -->
          <div v-if="selectedOperation === 'integral'" class="bounds-container">
            <div class="bounds-row">
              <div class="bound-input">
                <label for="lower-bound">Borne inférieure :</label>
                <input 
                  id="lower-bound"
                  v-model="lowerBound" 
                  type="text" 
                  placeholder="0 ou -∞"
                  class="bound-field"
                />
              </div>
              <div class="bound-input">
                <label for="upper-bound">Borne supérieure :</label>
                <input 
                  id="upper-bound"
                  v-model="upperBound" 
                  type="text" 
                  placeholder="1 ou +∞"
                  class="bound-field"
                />
              </div>
            </div>
            <div class="integral-type">
              <label class="integral-type-label">
                <input 
                  type="checkbox" 
                  v-model="isDefiniteIntegral"
                  @change="toggleIntegralType"
                />
                Intégrale définie
              </label>
            </div>
          </div>

          <!-- Champs pour les limites -->
          <div v-if="selectedOperation === 'limit'" class="bounds-container">
            <div class="bounds-row">
              <div class="bound-input">
                <label for="limit-point">Point limite :</label>
                <input 
                  id="limit-point"
                  v-model="limitPoint" 
                  type="text" 
                  placeholder="0, 1, +∞, -∞..."
                  class="bound-field"
                />
              </div>
              <div class="bound-input">
                <label for="limit-direction">Direction :</label>
                <select 
                  id="limit-direction"
                  v-model="limitDirection" 
                  class="bound-field"
                >
                  <option value="">Bilatérale</option>
                  <option value="left">À gauche (−)</option>
                  <option value="right">À droite (+)</option>
                </select>
              </div>
            </div>
            <div class="limit-help">
              <small class="help-text">
                Exemples : 0, 1, -2, +∞, -∞. Laissez vide pour +∞ par défaut.
              </small>
            </div>
          </div>

          <!-- Contrôles pour le graphique -->
          <div v-if="selectedOperation === 'graph'" class="bounds-container">
            <div class="graph-controls">
              <h4 class="controls-title">Paramètres du graphique</h4>
              <div class="bounds-row">
                <div class="bound-input">
                  <label for="x-min">X min :</label>
                  <input 
                    id="x-min"
                    v-model.number="xMin" 
                    type="number" 
                    class="bound-field"
                  />
                </div>
                <div class="bound-input">
                  <label for="x-max">X max :</label>
                  <input 
                    id="x-max"
                    v-model.number="xMax" 
                    type="number" 
                    class="bound-field"
                  />
                </div>
              </div>
              <div class="bounds-row">
                <div class="bound-input">
                  <label for="y-min">Y min :</label>
                  <input 
                    id="y-min"
                    v-model.number="yMin" 
                    type="number" 
                    class="bound-field"
                  />
                </div>
                <div class="bound-input">
                  <label for="y-max">Y max :</label>
                  <input 
                    id="y-max"
                    v-model.number="yMax" 
                    type="number" 
                    class="bound-field"
                  />
                </div>
              </div>
              <div class="graph-functions-list">
                <h5 class="functions-title">Fonctions tracées :</h5>
                <div v-if="graphFunctions.length === 0" class="no-functions">
                  Aucune fonction tracée. Saisissez une fonction et cliquez sur "Tracer".
                </div>
                <div v-for="(func, index) in graphFunctions" :key="index" class="function-item">
                  <span class="function-color" :style="{ backgroundColor: func.color }"></span>
                  <span class="function-expression" :ref="el => functionExpressionRefs[index] = el"></span>
                  <button @click="removeFunction(index)" class="remove-function-btn">×</button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="input-container">
            <math-field
              ref="mf"
              id="expr"
              class="math-input expr-input"
              virtual-keyboard-mode="off"
              @focus="isFocused = true"
              @blur="isFocused = false"
              @input="onInput"
              @keydown="handleKeyDown"
            ></math-field>
            <span
              v-if="!isFocused && !expressionValue"
              class="math-placeholder"
            >
              {{ getPlaceholderText() }}
            </span>
            <button class="vk-btn" @click="toggleCustomKeyboard" title="Afficher le clavier scientifique">
              <Cog6ToothIcon class="vk-icon" />
            </button>
          </div>
          <div class="keyboard-container">
            <button 
              class="calculate-btn" 
              @click="selectedOperation === 'graph' ? plotFunction() : calculate()" 
              :disabled="isCalculating"
              :title="isCalculating ? 'Calcul en cours...' : (selectedOperation === 'graph' ? 'Tracer la fonction' : `Calculer ${currentOperationName}`)"
            >
              <svg v-if="!isCalculating" class="calculate-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4"/>
                <path d="M21 12c-1 0-2-1-2-2s1-2 2-2 2 1 2 2-1 2-2 2z"/>
                <path d="M3 12c1 0 2-1 2-2s-1-2-2-2-2 1-2 2 1 2 2 2z"/>
                <path d="M12 3c0 1-1 2-2 2s-2-1-2-2 1-2 2-2 2 1 2 2z"/>
                <path d="M12 21c0-1 1-2 2-2s2 1 2 2-1 2-2 2-2-1-2-2z"/>
              </svg>
              <svg v-else class="calculate-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6"/>
                <path d="M1 12h6m6 0h6"/>
              </svg>
              {{ isCalculating ? 'Calcul...' : (selectedOperation === 'graph' ? 'Tracer' : 'Calculer') }}
            </button>
            
            <!-- Clavier scientifique personnalisé -->
            <div v-if="showCustomKeyboard" class="custom-keyboard">
              <!-- Onglets -->
              <div class="keyboard-tabs">
                <button 
                  class="tab-btn" 
                  :class="{ active: activeTab === 'algebra' }"
                  @click="activeTab = 'algebra'"
                >
                  Algèbre
                </button>
                <button 
                  class="tab-btn" 
                  :class="{ active: activeTab === 'trigonometry' }"
                  @click="activeTab = 'trigonometry'"
                >
                  Trigonométrie
                </button>
                <button 
                  class="tab-btn" 
                  :class="{ active: activeTab === 'exponential' }"
                  @click="activeTab = 'exponential'"
                >
                  Exponentielle
                </button>
                <button 
                  class="tab-btn" 
                  :class="{ active: activeTab === 'special' }"
                  @click="activeTab = 'special'"
                >
                  Spéciaux
                </button>
              </div>
              
              <div class="keyboard-content">
                <!-- Onglet Algèbre -->
                <div v-if="activeTab === 'algebra'" class="keyboard-section">
                  <div class="keyboard-grid">
                    <button 
                      v-for="tool in algebraTools" 
                      :key="tool.insert"
                      class="keyboard-btn"
                      @click="insert(tool.insert)"
                      :title="tool.label || tool.insert"
                    >
                      <img v-if="tool.slot" :src="`/scientificIcons/${tool.slot}.svg`" :alt="tool.slot" class="keyboard-icon" />
                      <span v-else>{{ tool.label }}</span>
                    </button>
                  </div>
                </div>
                
                <!-- Onglet Trigonométrie -->
                <div v-if="activeTab === 'trigonometry'" class="keyboard-section">
                  <div class="keyboard-grid">
                    <button 
                      v-for="tool in trigonometryTools" 
                      :key="tool.insert"
                      class="keyboard-btn"
                      @click="insert(tool.insert)"
                      :title="tool.label"
                    >
                      {{ tool.label }}
                    </button>
                  </div>
                </div>
                
                <!-- Onglet Exponentielle -->
                <div v-if="activeTab === 'exponential'" class="keyboard-section">
                  <div class="keyboard-grid">
                    <button 
                      v-for="tool in exponentialTools" 
                      :key="tool.insert"
                      class="keyboard-btn"
                      @click="insert(tool.insert)"
                      :title="tool.label"
                    >
                      {{ tool.label }}
                    </button>
                  </div>
                </div>
                
                <!-- Onglet Spéciaux -->
                <div v-if="activeTab === 'special'" class="keyboard-section">
                  <div class="keyboard-grid">
                    <button 
                      v-for="tool in specialFunctions" 
                      :key="tool.insert"
                      class="keyboard-btn"
                      @click="insert(tool.insert)"
                      :title="tool.label"
                    >
                      {{ tool.label }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> <!-- Fermeture de expr-box -->

      <div v-if="steps.length" class="deriv-steps">
        <h3 class="steps-title">{{ getStepsTitle() }}</h3>
        <ul class="steps-list">
          <li v-for="(step, i) in steps" :key="i">
            <div v-if="step.text" class="step-text">
              <span class="step-num">Étape {{ i + 1 }} :</span>
              <span :ref="el => textRefs[i] = el"></span>
            </div>
            <div v-if="step.formula" class="step-formula" :ref="el => formulaRefs[i] = el"></div>
          </li>
        </ul>
        <div v-if="steps.length" class="final-result">
          <span class="final-label">Résultat final :</span>
          <span ref="finalResultRef"></span>
        </div>
      </div>

      <!-- Conteneur du graphique -->
      <div v-if="selectedOperation === 'graph'" class="graph-section">
        <div class="graph-header">
          <h3 class="graph-title">Graphique Interactif</h3>
          <div class="graph-actions">
            <button @click="clearGraph" class="clear-graph-btn">Effacer tout</button>
            <button @click="resetZoom" class="reset-zoom-btn">Réinitialiser zoom</button>
          </div>
        </div>
        <div ref="graphContainer" class="graph-container"></div>
      </div>
    </section>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { deriveExpr, integrateExpr, expandExpr, factorExpr, limitExpr } from '@/api'
import { 
  CalculatorIcon, 
  Cog6ToothIcon,
  ArrowTrendingUpIcon,
  Square3Stack3DIcon,
  MinusIcon,
  PlusIcon,
  CubeIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import { normalizeAccents, fixAccentSpacing, cleanText, renderInlineMath } from '@/utils/textCleaner'
import Plotly from 'plotly.js-dist-min'

import { useSubjectsStore } from '@/stores/subjects/index'

// Store pour les matières
const subjectsStore = useSubjectsStore()

const preview = ref(null)
const mf = ref(null)
const isFocused = ref(false)
const expressionValue = ref('')
const steps = ref([])
const textRefs = [];
const formulaRefs = []
const finalResultRef = ref(null)
const originalExpressionRef = ref(null)
const resultData = ref(null)
const functionExpressionRefs = ref([])
const showSteps = ref(false)
const showCustomKeyboard = ref(false)
const activeTab = ref('algebra')
const isCalculating = ref(false)
const selectedOperation = ref('derivative')

// Variables pour les intégrales
const lowerBound = ref('')
const upperBound = ref('')
const isDefiniteIntegral = ref(false)

// Variables pour les limites
const limitPoint = ref('')
const limitDirection = ref('')

// Variables pour le graphique
const graphContainer = ref(null)
const xMin = ref(-10)
const xMax = ref(10)
const yMin = ref(-10)
const yMax = ref(10)
const graphFunctions = ref([])
const currentGraphColor = ref('#3b82f6')

// Configuration des opérations disponibles
const operations = [
  {
    id: 'derivative',
    name: 'Dérivée',
    icon: ArrowTrendingUpIcon,
    description: 'Calculer la dérivée d\'une fonction'
  },
  {
    id: 'integral',
    name: 'Intégrale',
    icon: Square3Stack3DIcon,
    description: 'Calculer l\'intégrale d\'une fonction'
  },
  {
    id: 'limit',
    name: 'Limite',
    icon: MinusIcon,
    description: 'Calculer la limite d\'une fonction'
  },
  {
    id: 'expand',
    name: 'Développement',
    icon: PlusIcon,
    description: 'Développer une expression'
  },
  {
    id: 'factor',
    name: 'Factorisation',
    icon: CubeIcon,
    description: 'Factoriser une expression'
  },
  {
    id: 'graph',
    name: 'Graphique',
    icon: ChartBarIcon,
    description: 'Tracer le graphique d\'une fonction'
  }
]

// Références réactives depuis le store
const selectedSubject = subjectsStore.selectedSubject
const subjects = subjectsStore.subjects

// Outils pour le clavier personnalisé
const algebraTools = [
  { label: '', slot: 'fraction', insert: '\\frac' },
  { label: '', slot: 'sqrt', insert: '\\sqrt{}' },
  { label: '', slot: 'nsqrt', insert: '\\sqrt[n]{}' },
  { label: '', slot: 'exposant', insert: '^\\square' },
  { label: 'ln', insert: '\\ln(' },
  { label: '', slot: 'exp', insert: '\\exp(' }
]

const trigonometryTools = [
  { label: 'sin', insert: '\\sin(' },
  { label: 'cos', insert: '\\cos(' },
  { label: 'tan', insert: '\\tan(' },
  { label: 'csc', insert: '\\csc(' },
  { label: 'sec', insert: '\\sec(' },
  { label: 'cot', insert: '\\cot(' },
  { label: 'arcsin', insert: '\\arcsin(' },
  { label: 'arccos', insert: '\\arccos(' },
  { label: 'arctan', insert: '\\arctan(' }
]

const exponentialTools = [
  { label: 'exp', insert: '\\exp(' },
  { label: 'ln', insert: '\\ln(' },
  { label: 'log', insert: '\\log(' },
  { label: 'log₁₀', insert: '\\log_{10}(' },
  { label: 'log₂', insert: '\\log_{2}(' },
  { label: 'e^x', insert: 'e^{' },
  { label: '10^x', insert: '10^{' },
  { label: '2^x', insert: '2^{' }
]

const specialFunctions = [
  { label: '|x|', insert: '\\left|' },
  { label: '√', insert: '\\sqrt{' },
  { label: '∛', insert: '\\sqrt[3]{' },
  { label: 'ⁿ√', insert: '\\sqrt[n]{' },
  { label: 'π', insert: '\\pi' },
  { label: 'e', insert: 'e' },
  { label: 'sinh', insert: '\\sinh(' },
  { label: 'cosh', insert: '\\cosh(' },
  { label: 'tanh', insert: '\\tanh(' }
]



// Fonctions utilitaires
function getCurrentSubject() {
  return subjects.find(s => s.id === selectedSubject.value) || subjects[0]
}

// Gestionnaire de changement de matière depuis le header
function handleSubjectChange(subjectId) {
  subjectsStore.setSubject(subjectId)
}

// Sélectionner une opération
function selectOperation(operationId) {
  selectedOperation.value = operationId
  // Réinitialiser les champs quand on change d'opération
  if (operationId !== 'integral') {
    lowerBound.value = ''
    upperBound.value = ''
    isDefiniteIntegral.value = false
  }
  if (operationId !== 'limit') {
    limitPoint.value = ''
    limitDirection.value = ''
  }
  // Initialiser le graphique si on sélectionne l'onglet graphique
  if (operationId === 'graph') {
    initializeGraph()
  }
}

// Basculer le type d'intégrale
function toggleIntegralType() {
  if (!isDefiniteIntegral.value) {
    lowerBound.value = ''
    upperBound.value = ''
  }
}

// Obtenir le texte du placeholder selon l'opération
function getPlaceholderText() {
  switch (selectedOperation.value) {
    case 'integral':
      return isDefiniteIntegral.value ? 'Fonction à intégrer (ex: x^2)' : 'Fonction à intégrer (ex: x^2)'
    case 'derivative':
      return 'Fonction à dériver (ex: (x+1)^2)'
    case 'limit':
      return 'Fonction pour la limite (ex: x^2)'
    case 'expand':
      return 'Expression à développer (ex: (x+1)^2)'
    case 'factor':
      return 'Expression à factoriser (ex: x^2-1)'
    case 'graph':
      return 'Fonction à tracer (ex: x^2, sin(x), ln(x))'
    default:
      return 'Expression (ex: (x+1)^2)'
  }
}

// Obtenir le titre des étapes selon l'opération
function getStepsTitle() {
  switch (selectedOperation.value) {
    case 'integral':
      return 'Étapes de l\'intégration :'
    case 'derivative':
      return 'Étapes de la dérivation :'
    case 'limit':
      return 'Étapes du calcul de limite :'
    case 'expand':
      return 'Étapes du développement :'
    case 'factor':
      return 'Étapes de la factorisation :'
    default:
      return 'Étapes du calcul :'
  }
}

// Obtenir l'opération actuelle
function getCurrentOperation() {
  return operations.find(op => op.id === selectedOperation.value) || operations[0]
}

// Computed pour obtenir le nom de l'opération actuelle
const currentOperationName = computed(() => {
  const operation = getCurrentOperation()
  return operation ? operation.name.toLowerCase() : 'dérivée'
})

// Fonctions pour les mathématiques
function integrate() {
  // TODO: Implémenter l'intégration
  console.log('Intégration à implémenter')
}

function solve() {
  // TODO: Implémenter la résolution d'équations
  console.log('Résolution d\'équations à implémenter')
}

// Fonctions pour la physique
function calculateVelocity() {
  // TODO: Implémenter le calcul de vitesse
  console.log('Calcul de vitesse à implémenter')
}

function calculateAcceleration() {
  // TODO: Implémenter le calcul d'accélération
  console.log('Calcul d\'accélération à implémenter')
}

function calculateForce() {
  // TODO: Implémenter le calcul de force
  console.log('Calcul de force à implémenter')
}

function calculateResistance() {
  // TODO: Implémenter le calcul de résistance
  console.log('Calcul de résistance à implémenter')
}

function calculatePower() {
  // TODO: Implémenter le calcul de puissance
  console.log('Calcul de puissance à implémenter')
}

function calculateCurrent() {
  // TODO: Implémenter le calcul d'intensité
  console.log('Calcul d\'intensité à implémenter')
}

function calculateFrequency() {
  // TODO: Implémenter le calcul de fréquence
  console.log('Calcul de fréquence à implémenter')
}

function calculateWavelength() {
  // TODO: Implémenter le calcul de longueur d'onde
  console.log('Calcul de longueur d\'onde à implémenter')
}

// Fonctions pour la chimie
function balanceEquation() {
  // TODO: Implémenter l'équilibrage d'équations
  console.log('Équilibrage d\'équations à implémenter')
}

function calculateMoles() {
  // TODO: Implémenter le calcul de moles
  console.log('Calcul de moles à implémenter')
}

function calculateConcentration() {
  // TODO: Implémenter le calcul de concentration
  console.log('Calcul de concentration à implémenter')
}

function calculateDilution() {
  // TODO: Implémenter le calcul de dilution
  console.log('Calcul de dilution à implémenter')
}

function calculatePH() {
  // TODO: Implémenter le calcul de pH
  console.log('Calcul de pH à implémenter')
}

onMounted(async () => {
  await nextTick()
  if (mf.value) {
    mf.value.virtualKeyboardMode = 'off'
  }
  
  // Gestionnaire de clic à l'extérieur pour fermer le clavier
  document.addEventListener('click', handleClickOutside)
})

// Nettoyer l'écouteur d'événement
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Fonction pour gérer le clic à l'extérieur
function handleClickOutside(event) {
  const keyboardContainer = document.querySelector('.keyboard-container')
  const keyboard = document.querySelector('.custom-keyboard')
  
  if (showCustomKeyboard.value && keyboardContainer && !keyboardContainer.contains(event.target)) {
    showCustomKeyboard.value = false
  }
}

function onInput() {
  if (mf.value) {
    expressionValue.value = mf.value.value
    update()
  }
}

function handleKeyDown(event) {
  if (event.key === 'Enter') {
    event.preventDefault()
    calculate()
  }
}

function insert(val) {
  if (!mf.value) return;

  const field = mf.value;

  if (typeof val === 'object' && val.type === 'clear') {
    field.value = '';
    field.focus();
    return;
  }

  if (typeof val === 'object' && val.type === 'equals') {
    // à compléter si besoin
    return;
  }

  if (typeof val === 'string') {
    if (val === '^\\square') {
      field.executeCommand('insert', '^{}');
      field.executeCommand('moveToPreviousPlaceholder');
      field.executeCommand('insert', '\\placeholder{☐}');
      field.executeCommand('moveToNextPlaceholder'); 
    } else if (val === '\\sqrt[n]{}') {
      field.executeCommand('insert', '\\sqrt[{}]{}');
      field.executeCommand('moveToPreviousPlaceholder');
      field.executeCommand('moveToPreviousPlaceholder');
      field.executeCommand('insert', '\\placeholder{☐}');
      field.executeCommand('moveToNextPlaceholder');
      field.executeCommand('moveToNextPlaceholder');
      field.executeCommand('insert', '\\placeholder{☐}');
      field.executeCommand('moveToPreviousPlaceholder');
    } else if (val === '\\sqrt{}') {
      field.executeCommand('insert', '\\sqrt{}');
      field.executeCommand('moveToPreviousPlaceholder');
      field.executeCommand('insert', '\\placeholder{☐}');
      field.executeCommand('moveToNextPlaceholder');
    } else {
      field.executeCommand('insert', val);
    }
    field.focus();
  }
}

function update() {
  if (preview.value) {
    preview.value.innerHTML = ''
  }
}

async function calculate() {
      if (!mf.value?.value || !mf.value.value.trim()) {
      // Afficher un message d'erreur si aucune fonction n'est saisie
      if (preview.value) {
        preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Veuillez saisir une fonction à calculer</span>`
      }
      return
    }
  
  try {
    isCalculating.value = true
    
    // Afficher un indicateur de chargement
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#3b82f6;font-size:0.9rem;'>Calcul en cours...</span>`
    }
    
    const payload = { latex: mf.value.value }
    
    // Appeler la fonction appropriée selon l'opération sélectionnée
    let data
    switch (selectedOperation.value) {
      case 'derivative':
        data = (await deriveExpr(payload)).data
        break
      case 'integral':
        // Préparer les données pour l'intégrale
        const integralPayload = { ...payload }
        if (isDefiniteIntegral.value && lowerBound.value && upperBound.value) {
          integralPayload.lower_bound = lowerBound.value
          integralPayload.upper_bound = upperBound.value
        }
        data = (await integrateExpr(integralPayload)).data
        break
      case 'limit':
        // Préparer les données pour la limite
        const limitPayload = { ...payload }
        if (limitPoint.value) {
          limitPayload.limit_point = limitPoint.value
        }
        if (limitDirection.value) {
          limitPayload.direction = limitDirection.value
        }
        data = (await limitExpr(limitPayload)).data
        break
      case 'expand':
        data = (await expandExpr(payload)).data
        break
      case 'factor':
        data = (await factorExpr(payload)).data
        break
      default:
        data = (await deriveExpr(payload)).data
    }
    katex.render(data.result_latex, preview.value, { throwOnError: false, displayMode: true })
    steps.value = Array.isArray(data.steps) ? data.steps : []
    await nextTick()
    steps.value.forEach((step, i) => {
      if (step.formula && formulaRefs[i]) {
        try {
          katex.render(step.formula.replace(/\$/g, ''), formulaRefs[i], { throwOnError: false, displayMode: true })
        } catch (e) {
          formulaRefs[i].innerText = step.formula
        }
      }
      if (step.text && textRefs[i]) {
        // Enlève le point final si présent et normalise les caractères accentués
        let cleanText = step.text.trim().replace(/\.$/, '')
        // Applique une correction supplémentaire pour les caractères accentués
        cleanText = fixAccentSpacing(cleanText)
        renderInlineMath(cleanText, textRefs[i])
      }
    })
    // Affiche le résultat final en bas
    if (finalResultRef.value && data.result_latex) {
      try {
        katex.render(data.result_latex, finalResultRef.value, { throwOnError: false, displayMode: true })
      } catch (e) {
        finalResultRef.value.innerText = data.result_latex
      }
    }
  } catch (e) {
    let msg = e?.response?.data?.detail || e.message || 'Erreur inconnue'
    resultData.value = null
    steps.value = []
    showSteps.value = false
    // Afficher l'erreur dans une zone dédiée
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#ef4444'>Erreur : ${msg}</span>`
    }
  } finally {
    isCalculating.value = false
  }
}

function toggleCustomKeyboard() {
  showCustomKeyboard.value = !showCustomKeyboard.value
}

// Fonctions pour le graphique
async function plotFunction() {
  if (!mf.value?.value || !mf.value.value.trim()) {
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Veuillez saisir une fonction à tracer</span>`
    }
    return
  }

  try {
    const expression = mf.value.value
    const color = getNextColor()
    
    // Ajouter la fonction à la liste
    graphFunctions.value.push({
      expression: expression,
      color: color,
      latex: expression
    })

    // Tracer toutes les fonctions
    plotAllFunctions()
    
    // Rendre les expressions en LaTeX
    await nextTick()
    renderFunctionExpressions()
    
    // Effacer le champ de saisie
    mf.value.value = ''
    expressionValue.value = ''
    
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#10b981;font-size:0.9rem;'>Fonction ajoutée au graphique</span>`
    }
  } catch (error) {
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Erreur : ${error.message}</span>`
    }
  }
}

function plotAllFunctions() {
  if (!graphContainer.value || graphFunctions.value.length === 0) return

  const traces = []
  
  graphFunctions.value.forEach((func, index) => {
    try {
      const { x, y } = generateFunctionData(func.latex)
      
      traces.push({
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        name: func.expression,
        line: {
          color: func.color,
          width: 2
        }
      })
    } catch (error) {
      console.error(`Erreur lors du tracé de la fonction ${func.expression}:`, error)
    }
  })

  const layout = {
    title: {
      text: 'Graphique des fonctions',
      font: { size: 18, color: '#1e3a8a' }
    },
    xaxis: {
      title: 'x',
      range: [xMin.value, xMax.value],
      gridcolor: '#e5e7eb',
      zerolinecolor: '#374151',
      zerolinewidth: 2,
      fixedrange: true
    },
    yaxis: {
      title: 'f(x)',
      range: [yMin.value, yMax.value],
      gridcolor: '#e5e7eb',
      zerolinecolor: '#374151',
      zerolinewidth: 2,
      fixedrange: true
    },
    plot_bgcolor: '#f8fafc',
    paper_bgcolor: 'white',
    margin: { t: 50, r: 50, b: 50, l: 50 },
    hovermode: 'closest'
  }

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    scrollZoom: false,
    staticPlot: false,
    editable: false,
    modeBarButtonsToRemove: [
      'zoomIn2d','zoomOut2d','autoScale2d','zoom2d',
      'pan2d','select2d','lasso2d','resetScale2d'
    ]
  }

  Plotly.newPlot(graphContainer.value, traces, layout, config)
    .then(() => {
      // Rerendre les expressions après le tracé
      nextTick(() => renderFunctionExpressions())
    })
    .catch((err) => {
      console.error('Erreur Plotly (plotAllFunctions):', err)
      if (preview.value) {
        preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Erreur d'affichage du graphique</span>`
      }
    })
}

function generateFunctionData(latexExpression) {
  // Convertir l'expression LaTeX en JavaScript
  let jsExpression = convertLatexToJS(latexExpression)
  
  console.log('Expression LaTeX:', latexExpression)
  console.log('Expression JS convertie:', jsExpression)
  
  const x = []
  const y = []
  const numPoints = 500 // Réduire pour de meilleures performances
  const step = (xMax.value - xMin.value) / numPoints
  
  for (let i = 0; i <= numPoints; i++) {
    const xi = xMin.value + i * step
    
    const yi = evaluateFunction(jsExpression, xi)
    
    // Vérifier que la valeur est valide
    if (!isNaN(yi) && isFinite(yi)) {
      // Filtrage plus permissif pour voir toute la courbe
      const yLimit = Math.max(Math.abs(yMax.value), Math.abs(yMin.value)) * 5
      
      if (Math.abs(yi) <= yLimit) {
        x.push(xi)
        y.push(yi)
      }
    }
    // Si yi est NaN, on ignore simplement ce point
  }
  
  console.log(`Points générés: ${x.length}`)
  if (x.length > 0) {
    console.log('Premiers points:', x.slice(0, 5), y.slice(0, 5))
    console.log('Derniers points:', x.slice(-5), y.slice(-5))
  } else {
    console.warn('⚠️ Aucun point valide généré pour:', latexExpression)
  }
  
  return { x, y }
}

function convertLatexToJS(latex) {
  let js = String(latex || '')
  
  // 0) Normaliser certains tokens LaTeX
  js = js.replace(/\\left/g, '')
  js = js.replace(/\\right/g, '')
  
  // 1) Fractions avant tout (pour préserver la priorité)
  js = js.replace(/\\frac{([^}]*)}{([^}]*)}/g, '(($1)/($2))')
  
  // 2) Racines (carrée et n-ième)
  js = js.replace(/\\sqrt\[([^\]]+)\]{([^}]+)}/g, 'Math.pow($2, 1/($1))')
  js = js.replace(/\\sqrt{([^}]+)}/g, 'Math.sqrt($1)')
  
  // 3) Constantes
  js = js.replace(/\\pi\b/g, 'Math.PI')
  js = js.replace(/\\e\b/g, 'Math.E')
  
  // 4) Exponentielles / Logs
  js = js.replace(/\\exp\(([^)]+)\)/g, 'Math.exp($1)')
  js = js.replace(/\\ln\(([^)]+)\)/g, 'Math.log($1)')
  js = js.replace(/\\log\(([^)]+)\)/g, 'Math.log10($1)')
  // log base b : \log_{b}(x)
  js = js.replace(/\\log_\{([^}]+)\}\(([^)]+)\)/g, '(Math.log($2)/Math.log($1))')
  
  // 5) Trigonométrie (avec puissances éventuelles)
  // sin^2(x) -> Math.pow(Math.sin(x),2)
  const trigAll = ['sin','cos','tan','sinh','cosh','tanh','arcsin','arccos','arctan']
  for (const fn of trigAll) {
    const target = fn.startsWith('arc') ? 'a' + fn.slice(3) : fn
    // D'abord gérer les puissances
    const powRegex = new RegExp('\\\\' + fn + '\\^\\{([^}]+)\\}\\(([^)]+)\\)', 'g')
    js = js.replace(powRegex, 'Math.pow(Math.' + target + '($2),$1)')
    // Puis les appels simples
    const callRegex = new RegExp('\\\\' + fn + '\\(([^)]+)\\)', 'g')
    js = js.replace(callRegex, 'Math.' + target + '($1)')
  }
  
  // Fonctions réciproques: sec, csc, cot
  js = js.replace(/\\sec\(([^)]+)\)/g, '(1/Math.cos($1))')
  js = js.replace(/\\csc\(([^)]+)\)/g, '(1/Math.sin($1))')
  js = js.replace(/\\cot\(([^)]+)\)/g, '(1/Math.tan($1))')
  
  // Gestion spéciale pour les fonctions sans parenthèses (sin x -> sin(x))
  js = js.replace(/\\sin\s+([a-zA-Z0-9]+)/g, 'Math.sin($1)')
  js = js.replace(/\\cos\s+([a-zA-Z0-9]+)/g, 'Math.cos($1)')
  js = js.replace(/\\tan\s+([a-zA-Z0-9]+)/g, 'Math.tan($1)')
  js = js.replace(/\\ln\s+([a-zA-Z0-9]+)/g, 'Math.log($1)')
  js = js.replace(/\\log\s+([a-zA-Z0-9]+)/g, 'Math.log10($1)')
  js = js.replace(/\\exp\s+([a-zA-Z0-9]+)/g, 'Math.exp($1)')
  
  // 6) Valeur absolue (|x| ou \left|x\right|)
  js = js.replace(/\\\|([^|]+)\\\|/g, 'Math.abs($1)')
  js = js.replace(/Math\.abs\(([^)]+)\)\)/g, 'Math.abs($1))')
  
  // 7) Puissances génériques
  js = js.replace(/\^\{([^}]+)\}/g, '**($1)')
  js = js.replace(/\^([a-zA-Z0-9]+)/g, '**$1')
  
  // 8) Remplacer e isolé par Math.E (attention à ne pas toucher exp/ etc.)
  js = js.replace(/\be\b/g, 'Math.E')
  
  // 9) Multiplication implicite sûre (évite d'altérer Math.sin(…))
  // a) )(
  js = js.replace(/\)\s*\(/g, ')*(')
  // b) nombre ou x suivi de (
  js = js.replace(/(\d|x)\s*\(/g, '$1*(')
  // c) ) suivi de x ou d'une fonction Math.
  js = js.replace(/\)\s*(x|Math\.)/g, ')*$1')
  // d) nombre ou x suivi de Math.
  js = js.replace(/(\d|x)\s*(Math\.)/g, '$1*$2')
  // e) nombre et variable accolés (2x, x2)
  js = js.replace(/(\d)(x)/g, '$1*$2')
  js = js.replace(/(x)(\d)/g, '$1*$2')
  
  return js
}

function evaluateFunction(expression, x) {
  // Remplacer x par la valeur avec parenthèses pour gérer les nombres négatifs
  let expr = expression.replace(/x/g, `(${x})`)
  
  // Nettoyer l'expression pour éviter les erreurs
  expr = expr.replace(/\s+/g, '')
  
  // Évaluation sécurisée
  try {
    const result = Function('"use strict"; return (' + expr + ')')()
    
    // Vérifier que le résultat est valide
    if (typeof result === 'number' && isFinite(result) && !isNaN(result)) {
      return result
    } else {
      return NaN
    }
  } catch (error) {
    console.warn(`Erreur d'évaluation pour x=${x}:`, error.message)
    return NaN
  }
}

function getNextColor() {
  const colors = [
    '#3b82f6', '#ef4444', '#10b981', '#f59e0b', 
    '#8b5cf6', '#06b6d4', '#f97316', '#84cc16',
    '#ec4899', '#6366f1', '#14b8a6', '#f43f5e'
  ]
  return colors[graphFunctions.value.length % colors.length]
}

function removeFunction(index) {
  graphFunctions.value.splice(index, 1)
  if (graphFunctions.value.length > 0) {
    plotAllFunctions()
    // Rerendre les expressions après suppression
    nextTick(() => renderFunctionExpressions())
  } else {
    clearGraph()
  }
}

function renderFunctionExpressions() {
  graphFunctions.value.forEach((func, index) => {
    if (functionExpressionRefs.value[index]) {
      try {
        katex.render(func.expression, functionExpressionRefs.value[index], { 
          throwOnError: false, 
          displayMode: false,
          fontSize: '1rem'
        })
      } catch (error) {
        // En cas d'erreur, afficher le texte brut
        functionExpressionRefs.value[index].innerText = func.expression
      }
    }
  })
}

function clearGraph() {
  graphFunctions.value = []
  if (graphContainer.value) {
    Plotly.purge(graphContainer.value)
  }
  if (preview.value) {
    preview.value.innerHTML = ''
  }
}

function resetZoom() {
  if (graphContainer.value && graphFunctions.value.length > 0) {
    Plotly.relayout(graphContainer.value, {
      'xaxis.range': [xMin.value, xMax.value],
      'yaxis.range': [yMin.value, yMax.value]
    })
  }
}

// Initialiser le graphique quand l'onglet graphique est sélectionné
function initializeGraph() {
  if (selectedOperation.value === 'graph') {
    nextTick(() => {
      if (graphContainer.value) {
        clearGraph()
        // Dessiner une grille vide
        const layout = {
          title: {
            text: 'Graphique des fonctions',
            font: { size: 18, color: '#1e3a8a' }
          },
          xaxis: {
            title: 'x',
            range: [xMin.value, xMax.value],
            gridcolor: '#e5e7eb',
            zerolinecolor: '#374151',
            zerolinewidth: 2,
            fixedrange: true
          },
          yaxis: {
            title: 'f(x)',
            range: [yMin.value, yMax.value],
            gridcolor: '#e5e7eb',
            zerolinecolor: '#374151',
            zerolinewidth: 2,
            fixedrange: true
          },
          plot_bgcolor: '#f8fafc',
          paper_bgcolor: 'white',
          margin: { t: 50, r: 50, b: 50, l: 50 },
          hovermode: 'closest'
        }

        const config = {
          responsive: true,
          displayModeBar: true,
          displaylogo: false,
          scrollZoom: false,
          staticPlot: false,
          editable: false,
          modeBarButtonsToRemove: [
            'zoomIn2d','zoomOut2d','autoScale2d','zoom2d',
            'pan2d','select2d','lasso2d','resetScale2d'
          ]
        }

        Plotly.newPlot(graphContainer.value, [], layout, config)
          .then(() => {})
          .catch((err) => {
            console.error('Erreur Plotly (initializeGraph):', err)
            if (preview.value) {
              preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Erreur d'initialisation du graphique</span>`
            }
          })
      }
    })
  }
}
</script>

<style scoped>
.calc {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 2rem;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 2rem;
  text-align: center;
  justify-content: center;
}

.title-icon {
  width: 2rem;
  height: 2rem;
}

/* Onglets d'opérations */
.operations-tabs {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.operation-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  color: #374151;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
  justify-content: center;
}

.operation-tab:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.operation-tab.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
}

.operation-tab:active {
  transform: translateY(0);
}

.operation-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.operation-label {
  font-size: 0.9rem;
}





/* Styles existants pour la calculatrice */
.expr-row {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

/* Styles pour les champs de bornes des intégrales */
.bounds-container {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
}

.bounds-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.bound-input {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.bound-input label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.bound-field {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
  transition: border-color 0.2s ease;
}

.bound-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.integral-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.integral-type-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
}

.integral-type-label input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  accent-color: #3b82f6;
}

/* Styles pour les limites */
.limit-help {
  margin-top: 0.5rem;
  text-align: center;
}

.help-text {
  color: #6b7280;
  font-style: italic;
}

.expr-box {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.input-container {
  position: relative;
  width: 100%;
}

.math-input {
  width: 100%;
  min-height: 60px;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  font-size: 1.1rem;
  background: white;
  transition: border-color 0.2s ease;
}

.math-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.math-placeholder {
  position: absolute;
  top: 50%;
  left: 1rem;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
  font-size: 1.1rem;
}

.vk-btn {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calculate-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.calculate-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.calculate-btn:active {
  transform: translateY(0);
}

.calculate-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.calculate-icon {
  width: 18px;
  height: 18px;
}

.vk-btn:hover {
  background: #f3f4f6;
}

.vk-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #6b7280;
}

.svg-dark {
  filter: invert(0.4);
}

/* Étapes de dérivation */
.deriv-steps {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
}

.steps-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 1rem;
}

.steps-list,
.steps-list li {
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

.steps-list li {
  margin-bottom: 1rem !important;
  padding: 1rem !important;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.step-text {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.2em;
  margin-bottom: 0.5rem;
}

.step-num {
  font-weight: bold;
  color: #3b82f6;
  margin-right: 0.5rem;
}

.step-text span.katex {
  font-size: 1.13em;
  vertical-align: middle;
  color: #193e8e;
}

.step-formula {
  margin-top: 0.5rem;
  text-align: center;
}

.final-result {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #dbeafe;
  border-radius: 0.5rem;
  border: 1px solid #93c5fd;
  text-align: center;
}

.final-label {
  font-weight: bold;
  color: #1e3a8a;
  margin-right: 0.5rem;
}

/* Conteneur du clavier */
.keyboard-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
}

/* Clavier scientifique personnalisé */
.custom-keyboard {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 400px;
  max-width: 600px;
  transform-origin: top right;
  animation: keyboardExpand 0.3s ease-out;
}

/* Onglets du clavier */
.keyboard-tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
  border-radius: 10px 10px 0 0;
}

.tab-btn {
  flex: 1;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  font-size: 0.9rem;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 2px solid transparent;
}

.tab-btn:hover {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: white;
}

@keyframes keyboardExpand {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.keyboard-content {
  padding: 1.5rem;
}

.keyboard-section {
  min-height: 200px;
}

.keyboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 0.75rem;
  max-width: 600px;
  margin: 0 auto;
}

.keyboard-btn {
  padding: 0.75rem 0.5rem;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50px;
}

.keyboard-btn:hover {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
}

.keyboard-btn:active {
  transform: translateY(0);
}

.keyboard-icon {
  width: 24px;
  height: 24px;
  filter: invert(0.4);
}

.keyboard-btn:hover .keyboard-icon {
  filter: invert(1);
}

/* Responsive */
@media (max-width: 768px) {
  .calc {
    padding: 1rem;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
  
  .subject-filters {
    flex-direction: column;
    align-items: center;
  }
  
  .subject-btn {
    width: 100%;
    max-width: 200px;
  }
  
  .custom-keyboard {
    max-height: 70vh;
  }
  
  .keyboard-grid {
    grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
    gap: 0.5rem;
  }
  
  .keyboard-btn {
    padding: 0.6rem 0.4rem;
    font-size: 0.85rem;
    min-height: 45px;
  }
  
  /* Responsive pour les champs de bornes */
  .bounds-row {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .bound-input {
    width: 100%;
  }
}

/* Styles pour le graphique */
.graph-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.graph-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e3a8a;
  margin: 0;
}

.graph-actions {
  display: flex;
  gap: 0.5rem;
}

.clear-graph-btn,
.reset-zoom-btn {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-graph-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.reset-zoom-btn:hover {
  background: #f0f9ff;
  border-color: #bfdbfe;
  color: #2563eb;
}

.graph-container {
  width: 100%;
  height: 500px;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: white;
}

/* Styles pour les contrôles du graphique */
.graph-controls {
  padding: 0;
}

.controls-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
}

.graph-functions-list {
  margin-top: 1rem;
  padding: 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.functions-title {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.75rem 0;
}

.no-functions {
  color: #6b7280;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}

.function-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
}

.function-item:last-child {
  margin-bottom: 0;
}

.function-color {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 1px #e5e7eb;
  flex-shrink: 0;
}

.function-expression {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #374151;
}

.remove-function-btn {
  width: 1.5rem;
  height: 1.5rem;
  border: none;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.remove-function-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

/* Responsive pour le graphique */
@media (max-width: 768px) {
  .graph-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .graph-actions {
    width: 100%;
    justify-content: stretch;
  }
  
  .clear-graph-btn,
  .reset-zoom-btn {
    flex: 1;
  }
  
  .graph-container {
    height: 400px;
  }
  
  .bounds-row {
    grid-template-columns: 1fr 1fr;
  }
}
</style> 