<template>
  <component :is="layoutComponent" v-on="layoutListeners">
    <section class="calc">
      <h2 class="title"><CalculatorIcon class="title-icon"/> Outil de Calcul Scientifique</h2>

      <!-- Système d'onglets pour le graphique -->
      <div v-if="selectedOperation === 'graph'" class="graph-tabs-wrapper">
        <div class="graph-tabs-container top-tabs">
          <div class="graph-tabs">
            <button 
              class="graph-tab" 
              :class="{ active: activeGraphTab === 'functions' }"
              @click="activeGraphTab = 'functions'"
            >
              📈 Fonctions
            </button>
            <button 
              class="graph-tab" 
              :class="{ active: activeGraphTab === 'axes' }"
              @click="activeGraphTab = 'axes'"
            >
              ⚙️ Axes
            </button>
            <button 
              class="graph-tab" 
              :class="{ active: activeGraphTab === 'asymptotes' }"
              @click="activeGraphTab = 'asymptotes'"
            >
              📐 Asymptotes
            </button>
            <button 
              class="graph-tab" 
              :class="{ active: activeGraphTab === 'analysis' }"
              @click="activeGraphTab = 'analysis'"
            >
              🔍 Analyse
            </button>
            <button 
              class="graph-tab" 
              :class="{ active: activeGraphTab === 'calculus' }"
              @click="activeGraphTab = 'calculus'"
            >
              📊 Calcul
            </button>
            <button 
              class="graph-tab" 
              :class="{ active: activeGraphTab === 'shapes' }"
              @click="activeGraphTab = 'shapes'"
            >
              🟢 Formes
            </button>
          </div>
        </div>
        
        <!-- Contenu des onglets directement sous les onglets -->
        <div class="graph-tab-content-top">
            <!-- Onglet Fonctions tracées -->
            <div v-show="activeGraphTab === 'functions'" class="tab-panel">
              <h4 class="panel-title">Fonctions tracées</h4>
              <div v-if="graphFunctions.length === 0" class="no-content">
                Aucune fonction tracée. Saisissez une fonction et cliquez sur "Tracer".
              </div>
              <div v-else class="functions-list">
                <div v-for="(func, index) in graphFunctions" :key="index" class="function-item">
                  <span class="function-color" :style="{ backgroundColor: func.color }"></span>
                  <span class="function-expression" :ref="el => functionExpressionRefs[index] = el"></span>
                  <button @click="removeFunction(index)" class="remove-function-btn">×</button>
                </div>
              </div>
            </div>
            
            <!-- Onglet Axes et fenêtre -->
            <div v-show="activeGraphTab === 'axes'" class="tab-panel">
              <h4 class="panel-title">Axes et fenêtre</h4>
              <div class="display-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showGrid" />
                  Afficher la grille
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showAxes" />
                  Afficher les axes
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showTicks" />
                  Afficher les graduations
                </label>
              </div>
              <div class="bounds-row">
                <div class="bound-input">
                  <label for="x-min">X min :</label>
                  <input id="x-min" v-model.number="xMin" type="number" class="bound-field" />
                </div>
                <div class="bound-input">
                  <label for="x-max">X max :</label>
                  <input id="x-max" v-model.number="xMax" type="number" class="bound-field" />
                </div>
              </div>
              <div class="bounds-row">
                <div class="bound-input">
                  <label for="y-min">Y min :</label>
                  <input id="y-min" v-model.number="yMin" type="number" class="bound-field" />
                </div>
                <div class="bound-input">
                  <label for="y-max">Y max :</label>
                  <input id="y-max" v-model.number="yMax" type="number" class="bound-field" />
                </div>
              </div>
            </div>
            
            <!-- Onglet Asymptotes -->
            <div v-show="activeGraphTab === 'asymptotes'" class="tab-panel">
              <h4 class="panel-title">Asymptotes</h4>
              <div class="bound-input">
                <label for="v-asymptotes">Asymptotes verticales (séparées par des virgules) :</label>
                <input 
                  id="v-asymptotes"
                  v-model="verticalAsymptotes" 
                  type="text" 
                  class="bound-field"
                  placeholder="Exemple : -2, 3"
                />
              </div>
              <div class="bound-input">
                <label for="h-asymptotes">Asymptotes horizontales (séparées par des virgules) :</label>
                <input 
                  id="h-asymptotes"
                  v-model="horizontalAsymptotes" 
                  type="text" 
                  class="bound-field"
                  placeholder="Exemple : 0, 5"
                />
              </div>
            </div>
            
            <!-- Onglet Analyse -->
            <div v-show="activeGraphTab === 'analysis'" class="tab-panel">
              <h4 class="panel-title">Analyse de fonctions</h4>
              <div class="display-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showIntersections" />
                  Afficher les intersections entre courbes
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showAxisIntersections" />
                  Afficher les intersections avec les axes
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showRoots" />
                  Afficher les racines
                </label>
              </div>
              
              <!-- Résultats d'analyse -->
              <div v-if="showIntersections && intersectionPoints.length > 0" class="results-section">
                <h5 class="results-title">Points d'intersection entre courbes :</h5>
                <div v-for="(point, index) in intersectionPoints" :key="index" class="result-item">
                  <span>f<sub>{{ point.func1Index }}</sub> ∩ f<sub>{{ point.func2Index }}</sub> : ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})</span>
                </div>
              </div>
              
              <div v-if="showRoots && rootsPoints.length > 0" class="results-section">
                <h5 class="results-title">Racines :</h5>
                <div v-for="(point, index) in rootsPoints" :key="index" class="result-item">
                  <span>f<sub>{{ point.funcIndex }}</sub> : x = {{ point.x.toFixed(3) }}</span>
                </div>
              </div>
              
              <div v-if="showAxisIntersections && axisIntersectionPoints.length > 0" class="results-section">
                <h5 class="results-title">Intersections avec les axes :</h5>
                <div v-for="(point, index) in axisIntersectionPoints" :key="index" class="result-item">
                  <span>f<sub>{{ point.funcIndex }}</sub> : ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})</span>
                </div>
              </div>
            </div>
            
            <!-- Onglet Calcul -->
            <div v-show="activeGraphTab === 'calculus'" class="tab-panel">
              <h4 class="panel-title">Calculs sur le graphique</h4>
              
              <!-- Aire sous la courbe -->
              <div class="calc-section">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showIntegralArea" />
                  Afficher l'aire sous la courbe
                </label>
                <div v-if="showIntegralArea" class="calc-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>Fonction :</label>
                      <select v-model.number="integralFunc1Index" class="bound-field">
                        <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                          f{{ index + 1 }}
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>De a :</label>
                      <input v-model.number="integralA" type="number" step="0.5" class="bound-field" />
                    </div>
                    <div class="bound-input">
                      <label>À b :</label>
                      <input v-model.number="integralB" type="number" step="0.5" class="bound-field" />
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Aire entre deux courbes -->
              <div class="calc-section">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showAreaBetweenCurves" />
                  Afficher l'aire entre deux courbes
                </label>
                <div v-if="showAreaBetweenCurves" class="calc-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>Fonction 1 :</label>
                      <select v-model.number="areaCurve1Index" class="bound-field">
                        <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                          f{{ index + 1 }}
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Fonction 2 :</label>
                      <select v-model.number="areaCurve2Index" class="bound-field">
                        <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                          f{{ index + 1 }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>De a :</label>
                      <input v-model.number="areaA" type="number" step="0.5" class="bound-field" placeholder="auto" />
                    </div>
                    <div class="bound-input">
                      <label>À b :</label>
                      <input v-model.number="areaB" type="number" step="0.5" class="bound-field" placeholder="auto" />
                    </div>
                  </div>
                  <div v-if="areaBetweenResult !== null" class="result-info">
                    <strong>Aire :</strong> {{ areaBetweenResult.toFixed(3) }}
                  </div>
                </div>
              </div>
              
              <!-- Tangente -->
              <div class="calc-section">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showTangent" />
                  Afficher la tangente
                </label>
                <div v-if="showTangent" class="calc-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>Fonction :</label>
                      <select v-model.number="tangentFuncIndex" class="bound-field">
                        <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                          f{{ index + 1 }}
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Point x₀ :</label>
                      <input v-model.number="tangentX" type="number" step="0.1" class="bound-field" />
                    </div>
                  </div>
                  <div v-if="tangentEquation" class="result-info">
                    <strong>Équation :</strong> {{ tangentEquation }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Onglet Formes -->
            <div v-show="activeGraphTab === 'shapes'" class="tab-panel">
              <h4 class="panel-title">Ajouter des formes</h4>
              
              <!-- Points -->
              <div class="shape-section">
                <h5 class="shape-title">Ajouter un point</h5>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>x :</label>
                    <input v-model.number="pointX" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>y :</label>
                    <input v-model.number="pointY" type="number" step="0.5" class="bound-field" />
                  </div>
                </div>
                <button @click="addPoint" class="action-btn">Ajouter le point</button>
                
                <div v-if="points.length > 0" class="shapes-list">
                  <div v-for="(point, index) in points" :key="'point-' + index" class="shape-item">
                    <span class="function-color" :style="{ backgroundColor: point.color }"></span>
                    <span>P{{ index + 1 }} ({{ point.x }}, {{ point.y }})</span>
                    <button @click="removePoint(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>
              
              <!-- Segments -->
              <div class="shape-section">
                <h5 class="shape-title">Ajouter un segment</h5>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>x₁ :</label>
                    <input v-model.number="segmentX1" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>y₁ :</label>
                    <input v-model.number="segmentY1" type="number" step="0.5" class="bound-field" />
                  </div>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>x₂ :</label>
                    <input v-model.number="segmentX2" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>y₂ :</label>
                    <input v-model.number="segmentY2" type="number" step="0.5" class="bound-field" />
                  </div>
                </div>
                <button @click="addSegment" class="action-btn">Ajouter le segment</button>
                
                <div v-if="segments.length > 0" class="shapes-list">
                  <div v-for="(segment, index) in segments" :key="'segment-' + index" class="shape-item">
                    <span class="function-color" :style="{ backgroundColor: segment.color }"></span>
                    <span>S{{ index + 1 }} [({{ segment.x1 }}, {{ segment.y1 }}) → ({{ segment.x2 }}, {{ segment.y2 }})]</span>
                    <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>
              
              <!-- Cercles -->
              <div class="shape-section">
                <h5 class="shape-title">Ajouter un cercle</h5>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>Centre h :</label>
                    <input v-model.number="circleH" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>Centre k :</label>
                    <input v-model.number="circleK" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>Rayon r :</label>
                    <input v-model.number="circleR" type="number" step="0.5" class="bound-field" />
                  </div>
                </div>
                <button @click="addCircle" class="action-btn">Ajouter le cercle</button>
                
                <div v-if="circles.length > 0" class="shapes-list">
                  <div v-for="(circle, index) in circles" :key="'circle-' + index" class="shape-item">
                    <span class="function-color" :style="{ backgroundColor: circle.color }"></span>
                    <span>C{{ index + 1 }} (h={{ circle.h }}, k={{ circle.k }}, r={{ circle.r }})</span>
                    <button @click="removeCircle(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>
            </div>
        </div>
      </div>
      <div class="expr-row">
        <div class="expr-box">
          <!-- Input principal en premier -->
          <div class="input-container">
            <math-field
              ref="mf"
              id="expr"
              class="math-input expr-input"
              virtual-keyboard-mode="onfocus"
              @focus="isFocused = true"
              @blur="isFocused = false"
              @input="onInput"
              @keydown="handleKeyDown"
            ></math-field>
            <span
              v-if="!isFocused && !expressionValue"
              class="math-placeholder"
              ref="placeholderRef"
            ></span>
            <button class="calculate-btn-inline" 
              @click="selectedOperation === 'graph' ? plotFunction() : calculate()" 
              :disabled="isCalculating"
              :title="isCalculating ? 'Calcul en cours...' : (selectedOperation === 'graph' ? 'Tracer la fonction' : `Calculer ${currentOperationName}`)"
            >
              <svg v-if="!isCalculating" class="calculate-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="4,12 8,16 20,6"/>
              </svg>
              <svg v-else class="calculate-icon spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
            </button>
            <button class="vk-btn" @click="toggleVirtualKeyboard" title="Afficher le clavier scientifique">
              <Bars3BottomLeftIcon class="vk-icon" />
            </button>
          </div>

          <!-- Panneaux flottants au-dessus de l'input -->
          <div class="floating-panels">
            <!-- Champs de bornes pour les intégrales -->
            <div v-if="selectedOperation === 'integral'" class="bounds-container floating-panel">
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
            <div v-if="selectedOperation === 'limit'" class="bounds-container floating-panel">
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

          
            <!-- Paramètres de base -->
            <details v-if="activeSection === 'axes'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▼</span>
                <span class="summary-text">⚙️ Axes et fenêtre</span>
              </summary>
              <div class="graph-controls">
              <div class="display-options" style="margin-bottom: 1rem;">
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showGrid" />
                  Afficher la grille
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showAxes" />
                  Afficher les axes
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showTicks" />
                  Afficher les graduations
                </label>
              </div>
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
              </div>
            </details>
            
            <!-- Asymptotes -->
            <details v-if="activeSection === 'asymptotes'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▶</span>
                <span class="summary-text">📐 Asymptotes</span>
              </summary>
              <div class="graph-controls">
              <div class="asymptotes-section">
                <div class="bounds-row">
                  <div class="bound-input">
                    <label for="vertical-asymptotes">Asymptotes verticales (x = ?):</label>
                    <input 
                      id="vertical-asymptotes"
                      v-model="verticalAsymptotes" 
                      type="text" 
                      placeholder="ex: 0, 1.57, -3"
                      class="bound-field"
                    />
                    <small class="help-text">Séparez par des virgules</small>
                  </div>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label for="horizontal-asymptotes">Asymptotes horizontales (y = ?):</label>
                    <input 
                      id="horizontal-asymptotes"
                      v-model="horizontalAsymptotes" 
                      type="text" 
                      placeholder="ex: 0, 2, -1"
                      class="bound-field"
                    />
                    <small class="help-text">Séparez par des virgules</small>
                  </div>
                </div>
              </div>
              </div>
            </details>
            
            <!-- Analyse et intersections -->
            <details v-if="activeSection === 'analysis'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▶</span>
                <span class="summary-text">🔍 Analyse (intersections, racines)</span>
              </summary>
              <div class="graph-controls">
              <div class="intersection-option">
                <label class="intersection-checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="showIntersections"
                  />
                  Afficher les points d'intersection entre courbes
                </label>
                <label class="intersection-checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="showAxisIntersections"
                  />
                  Afficher les intersections avec les axes
                </label>
              </div>
              
              <!-- Option pour afficher les racines -->
              <div class="roots-option">
                <label class="intersection-checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="showRoots"
                  />
                  Afficher les racines (zéros) des fonctions
                </label>
              </div>
              </div>
            </details>
            
            <!-- Calculs avancés -->
            <details v-if="activeSection === 'calculus'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▶</span>
                <span class="summary-text">📊 Calculs (intégrale, tangente)</span>
              </summary>
              <div class="graph-controls">
              <div class="integral-option">
                <label class="intersection-checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="showIntegralArea"
                  />
                  Calculer l'intégrale
                </label>
                
                <div v-if="showIntegralArea" class="integral-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label for="integral-a">Borne a :</label>
                      <input 
                        id="integral-a"
                        v-model.number="integralA" 
                        type="number" 
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="integral-b">Borne b :</label>
                      <input 
                        id="integral-b"
                        v-model.number="integralB" 
                        type="number" 
                        class="bound-field"
                        placeholder="1"
                      />
                    </div>
                  </div>
                  
                  <div class="integral-function-select">
                    <label for="integral-func1">Fonction 1 :</label>
                    <select id="integral-func1" v-model="integralFunc1Index" class="bound-field">
                      <option value="-1">Aucune (axe X)</option>
                      <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                        f{{ index + 1 }} - {{ func.expression }}
                      </option>
                    </select>
                  </div>
                  
                  <div class="integral-function-select">
                    <label for="integral-func2">Fonction 2 (optionnel) :</label>
                    <select id="integral-func2" v-model="integralFunc2Index" class="bound-field">
                      <option value="-1">Aucune (axe X)</option>
                      <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                        f{{ index + 1 }} - {{ func.expression }}
                      </option>
                    </select>
                  </div>
                  
                  <button @click="calculateIntegralArea" class="calculate-integral-btn">
                    Calculer l'intégrale
                  </button>
                  
                  <div v-if="integralResult !== null" class="integral-result">
                    <strong>Résultat :</strong> ∫ = {{ integralResult.toFixed(4) }}
                  </div>
                </div>
              </div>
              
              <div class="tangent-option">
                <label class="intersection-checkbox-label">
                  <input 
                    type="checkbox" 
                    v-model="showTangent"
                  />
                  Tracer la tangente en un point
                </label>
                
                <div v-if="showTangent" class="tangent-controls">
                  <div class="integral-function-select">
                    <label for="tangent-func">Fonction :</label>
                    <select id="tangent-func" v-model="tangentFuncIndex" class="bound-field">
                      <option v-for="(func, index) in graphFunctions.filter(f => f.type === 'function')" :key="index" :value="graphFunctions.indexOf(func)">
                        f{{ graphFunctions.indexOf(func) + 1 }} - {{ func.expression }}
                      </option>
                    </select>
                  </div>
                  
                  <div class="bound-input">
                    <label for="tangent-x">Point x₀ :</label>
                    <input 
                      id="tangent-x"
                      v-model.number="tangentX" 
                      type="number" 
                      step="0.1"
                      class="bound-field"
                      placeholder="0"
                    />
                  </div>
                  
                  <div v-if="tangentEquation" class="tangent-equation">
                    <strong>Équation :</strong> {{ tangentEquation }}
                  </div>
                </div>
              </div>
              </div>
            </details>
            
            <!-- Points -->
            <details v-if="activeSection === 'points'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▼</span>
                <span class="summary-text">🟢 Ajouter des points</span>
              </summary>
              <div class="graph-controls">
              <div class="point-option">
                <h5 class="functions-title">Ajouter un point</h5>
                <div class="point-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label for="point-x">x :</label>
                      <input 
                        id="point-x"
                        v-model.number="pointX" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="point-y">y :</label>
                      <input 
                        id="point-y"
                        v-model.number="pointY" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                  </div>
                  
                  <button @click="addPoint" class="calculate-integral-btn" style="background: #10b981;">
                    Ajouter le point
                  </button>
                </div>
                
                <div v-if="points.length > 0" class="points-list">
                  <h5 class="functions-title">Points tracés :</h5>
                  <div v-for="(point, index) in points" :key="'point-' + index" class="function-item">
                    <span class="function-color" :style="{ backgroundColor: point.color }"></span>
                    <span class="circle-label">
                      P{{ index + 1 }} ({{ point.x }}, {{ point.y }})
                    </span>
                    <button @click="removePoint(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>
              
              <!-- Option pour ajouter des segments -->
              <div class="segment-option">
                <h5 class="functions-title">Ajouter un segment</h5>
                <div class="segment-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label for="segment-x1">Point A - x₁ :</label>
                      <input 
                        id="segment-x1"
                        v-model.number="segmentX1" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="segment-y1">Point A - y₁ :</label>
                      <input 
                        id="segment-y1"
                        v-model.number="segmentY1" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                  </div>
                  
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label for="segment-x2">Point B - x₂ :</label>
                      <input 
                        id="segment-x2"
                        v-model.number="segmentX2" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="1"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="segment-y2">Point B - y₂ :</label>
                      <input 
                        id="segment-y2"
                        v-model.number="segmentY2" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="1"
                      />
                    </div>
                  </div>
                  
                  <button @click="addSegment" class="calculate-integral-btn" style="background: #f59e0b;">
                    Ajouter le segment
                  </button>
                </div>
                
                <div v-if="segments.length > 0" class="segments-list">
                  <h5 class="functions-title">Segments tracés :</h5>
                  <div v-for="(segment, index) in segments" :key="'segment-' + index" class="function-item">
                    <span class="function-color" :style="{ backgroundColor: segment.color }"></span>
                    <span class="circle-label">
                      [AB]{{ index + 1 }} : A({{ segment.x1 }}, {{ segment.y1 }}) → B({{ segment.x2 }}, {{ segment.y2 }})
                    </span>
                    <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>
              </div>
            </details>
            
            <!-- Cercles -->
            <details v-if="activeSection === 'circles'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▼</span>
                <span class="summary-text">⚫ Ajouter des cercles</span>
              </summary>
              <div class="graph-controls">
              <div class="circle-option">
                <h5 class="functions-title">Ajouter un cercle</h5>
                <div class="circle-controls">
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label for="circle-h">Centre x (h) :</label>
                      <input 
                        id="circle-h"
                        v-model.number="circleH" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="circle-k">Centre y (k) :</label>
                      <input 
                        id="circle-k"
                        v-model.number="circleK" 
                        type="number" 
                        step="0.5"
                        class="bound-field"
                        placeholder="0"
                      />
                    </div>
                  </div>
                  
                  <div class="bound-input">
                    <label for="circle-r">Rayon (r) :</label>
                    <input 
                      id="circle-r"
                      v-model.number="circleR" 
                      type="number" 
                      step="0.5"
                      min="0.1"
                      class="bound-field"
                      placeholder="1"
                    />
                  </div>
                  
                  <button @click="addCircle" class="calculate-integral-btn" style="background: #8b5cf6;">
                    Ajouter le cercle
                  </button>
                </div>
                
                <div v-if="circles.length > 0" class="circles-list">
                  <h5 class="functions-title">Cercles tracés :</h5>
                  <div v-for="(circle, index) in circles" :key="'circle-' + index" class="function-item">
                    <span class="function-color" :style="{ backgroundColor: circle.color }"></span>
                    <span class="circle-label">
                      (x - {{ circle.h }})² + (y - {{ circle.k }})² = {{ circle.r }}²
                    </span>
                    <button @click="removeCircle(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>
              </div>
            </details>
            
            <!-- Fonctions tracées -->
            <details v-if="activeSection === 'functions'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▼</span>
                <span class="summary-text">📈 Fonctions tracées</span>
              </summary>
              <div class="graph-controls">
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
            </details>
            
            <!-- Résultats d'analyse -->
            <details v-if="(showIntersections && intersectionPoints.length > 0) || (showRoots && rootsPoints.length > 0) || (showAxisIntersections && axisIntersectionPoints.length > 0)" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▼</span>
                <span class="summary-text">📋 Résultats d'analyse</span>
              </summary>
              <div class="graph-controls">
              <div v-if="showIntersections && intersectionPoints.length > 0" class="intersections-list">
                <h5 class="functions-title">Points d'intersection entre courbes :</h5>
                <div v-for="(point, index) in intersectionPoints" :key="index" class="intersection-item">
                  <div class="intersection-content">
                    <span class="intersection-label">
                      f<sub>{{ point.func1Index }}</sub> ∩ f<sub>{{ point.func2Index }}</sub> :
                    </span>
                    <span class="intersection-point">
                      ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})
                    </span>
                    <span class="intersection-functions" :ref="el => intersectionRefs[index] = el"></span>
                  </div>
                  <button @click="removeIntersection(index)" class="remove-intersection-btn" title="Supprimer cette intersection">×</button>
                </div>
              </div>
              
              <!-- Liste des racines -->
              <div v-if="showRoots && rootsPoints.length > 0" class="intersections-list" style="background: #fef9f3; border-color: #fed7aa;">
                <h5 class="functions-title">Racines (zéros) des fonctions :</h5>
                <div v-for="(point, index) in rootsPoints" :key="'root-' + index" class="intersection-item">
                  <div class="intersection-content">
                    <span class="intersection-label">
                      f<sub>{{ point.funcIndex }}</sub>({{ point.x.toFixed(3) }}) = 0
                    </span>
                    <span class="intersection-point">
                      x = {{ point.x.toFixed(3) }}
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- Liste des intersections avec les axes -->
              <div v-if="showAxisIntersections && axisIntersectionPoints.length > 0" class="intersections-list">
                <h5 class="functions-title">Intersections avec les axes :</h5>
                <div v-for="(point, index) in axisIntersectionPoints" :key="'axis-' + index" class="intersection-item">
                  <div class="intersection-content">
                    <span class="intersection-label">
                      f<sub>{{ point.funcIndex }}</sub> ∩ {{ point.axis === 'x' ? 'axe X' : 'axe Y' }} :
                    </span>
                    <span class="intersection-point">
                      ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})
                    </span>
                  </div>
                  <button @click="removeAxisIntersection(index)" class="remove-intersection-btn" title="Supprimer cette intersection">×</button>
                </div>
              </div>
              </div>
            </details>
          </div> <!-- Fermeture de floating-panels -->
          
          <!-- Panneau modal d'options en grid -->
          <div v-if="selectedOperation === 'graph' && showGraphOptions" class="graph-options-modal" @click.self="showGraphOptions = false">
            <div class="options-modal-content">
              <div class="options-modal-header">
                <h3>Options du graphique</h3>
                <button @click="showGraphOptions = false" class="close-modal-btn">×</button>
              </div>
              <div class="options-grid">
                <!-- Carte Axes -->
                <div class="option-card" @click="toggleSection('axes')">
                  <div class="card-icon">⚙️</div>
                  <div class="card-title">Axes et fenêtre</div>
                  <div class="card-description">Ajuster les bornes X et Y</div>
                </div>
                
                <!-- Carte Asymptotes -->
                <div class="option-card" @click="toggleSection('asymptotes')">
                  <div class="card-icon">📐</div>
                  <div class="card-title">Asymptotes</div>
                  <div class="card-description">Ajouter des asymptotes</div>
                </div>
                
                <!-- Carte Analyse -->
                <div class="option-card" @click="toggleSection('analysis')">
                  <div class="card-icon">🔍</div>
                  <div class="card-title">Analyse</div>
                  <div class="card-description">Intersections et racines</div>
                </div>
                
                <!-- Carte Calculs -->
                <div class="option-card" @click="toggleSection('calculus')">
                  <div class="card-icon">📊</div>
                  <div class="card-title">Calculs</div>
                  <div class="card-description">Intégrale et tangente</div>
                </div>
                
                <!-- Carte Points -->
                <div class="option-card" @click="toggleSection('points')">
                  <div class="card-icon">🟢</div>
                  <div class="card-title">Points</div>
                  <div class="card-description">Ajouter des points</div>
                </div>
                
                <!-- Carte Segments -->
                <div class="option-card" @click="toggleSection('segments')">
                  <div class="card-icon">📍</div>
                  <div class="card-title">Segments</div>
                  <div class="card-description">Tracer des segments</div>
                </div>
                
                <!-- Carte Cercles -->
                <div class="option-card" @click="toggleSection('circles')">
                  <div class="card-icon">⚫</div>
                  <div class="card-title">Cercles</div>
                  <div class="card-description">Dessiner des cercles</div>
                </div>
                
                <!-- Carte Fonctions -->
                <div class="option-card" @click="toggleSection('functions')">
                  <div class="card-icon">📈</div>
                  <div class="card-title">Fonctions tracées</div>
                  <div class="card-description">Gérer les fonctions</div>
                </div>
              </div>
            </div>
          </div>
          
        </div> <!-- Fermeture de expr-box -->
      </div> <!-- Fermeture de expr-row -->

      <div v-if="isAuthenticated && steps.length" class="deriv-steps">
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

      <div v-else-if="!isAuthenticated && hasCalculated" class="steps-cta">
        <h3 class="steps-title">Étapes du calcul</h3>
        <p class="cta-text">Connectez-vous pour afficher les étapes détaillées du calcul.</p>
        <button class="login-cta-btn" @click="openLogin">Se connecter</button>
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
  </component>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import { deriveExpr, integrateExpr, expandExpr, factorExpr, limitExpr } from '@/api'
import { 
  CalculatorIcon, 
  Bars3BottomLeftIcon,
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
import { useUserStore } from '@/stores/user'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

// Store pour les matières
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { openModal } = useModalManager()
const route = useRoute()
const router = useRouter()

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
const placeholderRef = ref(null)
const showSteps = ref(false)
const showCustomKeyboard = ref(false)
const activeTab = ref('algebra')
const isCalculating = ref(false)
const selectedOperation = computed(() => route.query.operation || 'derivative')
const hasCalculated = ref(false)
const isAuthenticated = computed(() => userStore.isAuthenticated)
const layoutComponent = computed(() => isAuthenticated.value ? DashboardLayout : MainLayout)
const layoutListeners = computed(() => isAuthenticated.value ? { 'subject-changed': handleSubjectChange } : {})

function openLogin() {
  openModal(MODAL_IDS.LOGIN)
}

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
const verticalAsymptotes = ref('')
const horizontalAsymptotes = ref('')
const showIntersections = ref(false)
const showAxisIntersections = ref(false)
const intersectionPoints = ref([])
const axisIntersectionPoints = ref([])
const intersectionRefs = ref([])
const hiddenIntersections = ref([])
const hiddenAxisIntersections = ref([])
const showIntegralArea = ref(false)
const integralA = ref(0)
const integralB = ref(1)
const integralFunc1Index = ref(0)
const integralFunc2Index = ref(-1)
const integralResult = ref(null)
const showAreaBetweenCurves = ref(false)
const areaCurve1Index = ref(0)
const areaCurve2Index = ref(1)
const areaA = ref(null)
const areaB = ref(null)
const areaBetweenResult = ref(null)
const showTangent = ref(false)
const tangentFuncIndex = ref(0)
const tangentX = ref(0)
const tangentEquation = ref('')
const showRoots = ref(false)
const rootsPoints = ref([])
const circles = ref([])
const circleH = ref(0)
const circleK = ref(0)
const circleR = ref(1)

// Variables pour l'affichage de la grille et des axes
const showGrid = ref(true)
const showAxes = ref(true)
const showTicks = ref(true)

// Variables pour les points
const points = ref([])
const pointX = ref(0)
const pointY = ref(0)

// Variables pour les segments
const segments = ref([])
const segmentX1 = ref(0)
const segmentY1 = ref(0)
const segmentX2 = ref(1)
const segmentY2 = ref(1)

// Variable pour afficher/masquer le panneau d'options
const showGraphOptions = ref(false)
const activeSection = ref('')
const activeGraphTab = ref('functions')

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

// Sélectionner une opération (via le router)
function selectOperation(operationId) {
  router.push({ 
    name: 'Calculator', 
    query: { operation: operationId } 
  })
}

// Watcher pour réagir aux changements d'opération
watch(selectedOperation, (newOperation, oldOperation) => {
  if (newOperation === oldOperation) return
  
  // Réinitialiser les champs quand on change d'opération
  if (newOperation !== 'integral') {
    lowerBound.value = ''
    upperBound.value = ''
    isDefiniteIntegral.value = false
  }
  if (newOperation !== 'limit') {
    limitPoint.value = ''
    limitDirection.value = ''
  }
  // Initialiser le graphique si on sélectionne l'onglet graphique
  if (newOperation === 'graph') {
    nextTick(() => {
      initializeGraph()
    })
  }
})

// Basculer le type d'intégrale
function toggleIntegralType() {
  if (!isDefiniteIntegral.value) {
    lowerBound.value = ''
    upperBound.value = ''
  }
}

// Obtenir le texte du placeholder selon l'opération
function getPlaceholderData() {
  switch (selectedOperation.value) {
    case 'integral':
      return { text: 'Fonction à intégrer (ex: ', latex: 'x^{2}' }
    case 'derivative':
      return { text: 'Fonction à dériver (ex: ', latex: '(x+1)^{2}' }
    case 'limit':
      return { text: 'Fonction pour la limite (ex: ', latex: '\\frac{x^{2}-1}{x-1}' }
    case 'expand':
      return { text: 'Expression à développer (ex: ', latex: '(x+1)^{2}' }
    case 'factor':
      return { text: 'Expression à factoriser (ex: ', latex: 'x^{2}-1' }
    case 'graph':
      return { text: 'Fonction à tracer (ex: ', latex: 'x^{2}, \\sin(x), \\ln(x)' }
    default:
      return { text: 'Expression (ex: ', latex: '(x+1)^{2}' }
  }
}

// Fonction pour rendre le placeholder avec KaTeX
function renderPlaceholder() {
  if (placeholderRef.value) {
    const data = getPlaceholderData()
    try {
      // Créer un conteneur avec le texte + la formule LaTeX rendue
      const textSpan = document.createElement('span')
      textSpan.textContent = data.text
      textSpan.style.color = '#9ca3af'
      
      const mathSpan = document.createElement('span')
      katex.render(data.latex, mathSpan, {
        throwOnError: false,
        displayMode: false
      })
      mathSpan.style.color = '#9ca3af'
      
      const closeSpan = document.createElement('span')
      closeSpan.textContent = ')'
      closeSpan.style.color = '#9ca3af'
      
      placeholderRef.value.innerHTML = ''
      placeholderRef.value.appendChild(textSpan)
      placeholderRef.value.appendChild(mathSpan)
      placeholderRef.value.appendChild(closeSpan)
    } catch (error) {
      console.error('Erreur de rendu KaTeX pour le placeholder:', error)
      placeholderRef.value.textContent = data.text + data.latex + ')'
    }
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
  
  // Rendre le placeholder initial
  renderPlaceholder()
  
  // Gestionnaire de clic à l'extérieur pour fermer le clavier
  document.addEventListener('click', handleClickOutside)
})

// Watcher pour mettre à jour le placeholder quand l'opération change
watch(() => selectedOperation.value, () => {
  // Réinitialiser tout le contenu quand on change d'opération
  if (mf.value) {
    mf.value.value = ''
  }
  expressionValue.value = ''
  steps.value = []
  hasCalculated.value = false
  
  // Vider le preview
  if (preview.value) {
    preview.value.innerHTML = ''
  }
  
  // Vider le graphique si c'est l'opération graphique
  if (selectedOperation.value === 'graph') {
    clearGraph()
    nextTick(() => initializeGraph())
  }
  
  // Réinitialiser les bornes pour les intégrales et limites
  lowerBound.value = ''
  upperBound.value = ''
  limitPoint.value = ''
  limitDirection.value = ''
  
  // Réinitialiser les asymptotes
  verticalAsymptotes.value = ''
  horizontalAsymptotes.value = ''
  
  nextTick(() => renderPlaceholder())
})

// Watcher pour le type d'intégrale
watch(() => isDefiniteIntegral.value, () => {
  nextTick(() => renderPlaceholder())
})

// Watchers pour les asymptotes - mettre à jour le graphique quand on les modifie
watch([verticalAsymptotes, horizontalAsymptotes], () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour les limites du graphique - redessiner quand on change les bornes
watch([xMin, xMax, yMin, yMax], () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour l'option d'affichage des intersections
watch(showIntersections, () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length >= 2) {
    plotAllFunctions()
  }
})

// Watcher pour l'option d'affichage des intersections avec les axes
watch(showAxisIntersections, () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour l'affichage de la zone d'intégrale
watch(showIntegralArea, () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour les paramètres de l'intégrale (bornes et fonctions)
watch([integralA, integralB, integralFunc1Index, integralFunc2Index], () => {
  if (selectedOperation.value === 'graph' && showIntegralArea.value && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour l'affichage de l'aire entre deux courbes
watch(showAreaBetweenCurves, () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour les paramètres de l'aire entre deux courbes
watch([areaCurve1Index, areaCurve2Index, areaA, areaB], () => {
  if (selectedOperation.value === 'graph' && showAreaBetweenCurves.value && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour l'affichage de la tangente
watch(showTangent, () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour les paramètres de la tangente
watch([tangentFuncIndex, tangentX], () => {
  if (selectedOperation.value === 'graph' && showTangent.value && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour l'affichage des racines
watch(showRoots, () => {
  if (selectedOperation.value === 'graph' && graphFunctions.value.length > 0) {
    plotAllFunctions()
  }
})

// Watcher pour les fonctions tracées - rendre les expressions LaTeX
watch(() => graphFunctions.value.length, () => {
  if (graphFunctions.value.length > 0) {
    nextTick(() => {
      renderFunctionExpressions()
    })
  }
}, { flush: 'post' })

// Watchers pour l'affichage de la grille, des axes et des graduations
watch([showGrid, showAxes, showTicks], () => {
  if (selectedOperation.value === 'graph') {
    plotAllFunctions()
  }
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
    // Appeler la fonction appropriée selon l'opération sélectionnée
    if (selectedOperation.value === 'graph') {
      plotFunction()
    } else {
      calculate()
    }
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
    hasCalculated.value = true
    
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
      case 'graph':
        // Pour le graphique, on ne devrait pas passer par calculate() mais par plotFunction()
        console.warn("Utilisez plotFunction() pour tracer un graphique")
        return
      default:
        // Si l'opération n'est pas reconnue, afficher une erreur
        throw new Error(`Opération non reconnue: ${selectedOperation.value}`)
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

function toggleGraphOptions() {
  showGraphOptions.value = !showGraphOptions.value
}

function toggleSection(section) {
  if (activeSection.value === section) {
    activeSection.value = ''
  } else {
    activeSection.value = section
    showGraphOptions.value = false
  }
}

function toggleVirtualKeyboard() {
  if (mf.value) {
    try {
      // Vérifier que le clavier virtuel est disponible
      if (typeof window.mathVirtualKeyboard !== 'undefined') {
        if (window.mathVirtualKeyboard.visible) {
          window.mathVirtualKeyboard.hide()
        } else {
          window.mathVirtualKeyboard.show()
          mf.value.focus()
        }
      } else {
        // Fallback : changer le mode du clavier virtuel pour le forcer à apparaître
        const currentMode = mf.value.virtualKeyboardMode
        mf.value.virtualKeyboardMode = currentMode === 'onfocus' ? 'manual' : 'onfocus'
        if (mf.value.virtualKeyboardMode === 'onfocus') {
          mf.value.focus()
        }
      }
    } catch (error) {
      console.warn('Erreur lors de l\'affichage du clavier virtuel:', error)
      // Fallback simple : focus sur le champ
      mf.value.focus()
    }
  }
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
    
    // Détecter si c'est une droite verticale (x=nombre) ou horizontale (y=nombre)
    let type = 'function'
    let value = null
    
    const verticalMatch = expression.match(/^x\s*=\s*([\-\d\.]+)$/)
    const horizontalMatch = expression.match(/^y\s*=\s*([\-\d\.]+)$/)
    
    if (verticalMatch) {
      type = 'vertical'
      value = parseFloat(verticalMatch[1])
    } else if (horizontalMatch) {
      type = 'horizontal'
      value = parseFloat(horizontalMatch[1])
    }
    
    // Ajouter la fonction à la liste
    graphFunctions.value.push({
      expression: expression,
      color: color,
      latex: expression,
      type: type,
      value: value
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
      // Traitement spécial pour les droites verticales et horizontales
      if (func.type === 'vertical') {
        // Droite verticale : x = constante
        traces.push({
          x: [func.value, func.value],
          y: [yMin.value, yMax.value],
          type: 'scatter',
          mode: 'lines',
          name: `$${func.expression}$`,
          line: {
            color: func.color,
            width: 2
          },
          legendgroup: `func${index}`,
          showlegend: true,
          hovertemplate: `<b>${func.expression}</b><br>x: ${func.value}<extra></extra>`
        })
      } else if (func.type === 'horizontal') {
        // Droite horizontale : y = constante
        traces.push({
          x: [xMin.value, xMax.value],
          y: [func.value, func.value],
          type: 'scatter',
          mode: 'lines',
          name: `$${func.expression}$`,
          line: {
            color: func.color,
            width: 2
          },
          legendgroup: `func${index}`,
          showlegend: true,
          hovertemplate: `<b>${func.expression}</b><br>y: ${func.value}<extra></extra>`
        })
      } else {
        // Fonction normale
        const { x, y } = generateFunctionData(func.latex)
        
        // Convertir l'expression LaTeX pour l'affichage dans la légende avec MathJax
        const functionLabel = `f_${index + 1}`
        const displayName = `$${functionLabel}(x) = ${func.expression}$`
        
        traces.push({
          x: x,
          y: y,
          type: 'scatter',
          mode: 'lines',
          name: displayName,
          line: {
            color: func.color,
            width: 2
          },
          legendgroup: `func${index}`,
          showlegend: true,
          hovertemplate: `<b>f<sub>${index + 1}</sub>(x)</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
        })
      }
    } catch (error) {
      console.error(`Erreur lors du tracé de la fonction ${func.expression}:`, error)
    }
  })
  
  // Ajouter les asymptotes manuelles
  addManualAsymptotes(traces)
  
  // Calculer et afficher les points d'intersection si l'option est activée
  if (showIntersections.value && graphFunctions.value.length >= 2) {
    calculateIntersections(traces)
  }
  
  // Calculer et afficher les intersections avec les axes si l'option est activée
  if (showAxisIntersections.value && graphFunctions.value.length > 0) {
    calculateAxisIntersections(traces)
  }
  
  // Afficher la zone d'intégration si l'option est activée
  if (showIntegralArea.value && integralFunc1Index.value !== -1) {
    addIntegralAreaToGraph(traces)
  }
  
  // Afficher l'aire entre deux courbes si l'option est activée
  if (showAreaBetweenCurves.value && graphFunctions.value.length >= 2) {
    addAreaBetweenCurvesToGraph(traces)
  }
  
  // Afficher la tangente si l'option est activée
  if (showTangent.value && tangentFuncIndex.value >= 0) {
    addTangentToGraph(traces)
  }
  
  // Calculer et afficher les racines si l'option est activée
  if (showRoots.value && graphFunctions.value.length > 0) {
    calculateRoots(traces)
  }
  
  // Dessiner les points
  if (points.value.length > 0) {
    drawPoints(traces)
  }
  
  // Dessiner les segments
  if (segments.value.length > 0) {
    drawSegments(traces)
  }
  
  // Dessiner les cercles
  if (circles.value.length > 0) {
    drawCircles(traces)
  }

  const layout = {
    xaxis: {
      title: {
        text: 'x',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      },
      range: [xMin.value, xMax.value],
      gridcolor: '#e5e7eb',
      showgrid: showGrid.value,
      zerolinecolor: '#374151',
      zerolinewidth: showAxes.value ? 2 : 0,
      zeroline: showAxes.value,
      fixedrange: true,
      showline: showAxes.value,
      linecolor: '#374151',
      linewidth: 2,
      mirror: false,
      dtick: 2,
      showticklabels: showTicks.value,
      ticks: showTicks.value ? 'outside' : '',
      constrain: 'domain',
      constraintoward: 'center'
    },
    yaxis: {
      title: {
        text: 'y',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      },
      range: [yMin.value, yMax.value],
      gridcolor: '#e5e7eb',
      showgrid: showGrid.value,
      zerolinecolor: '#374151',
      zerolinewidth: showAxes.value ? 2 : 0,
      zeroline: showAxes.value,
      fixedrange: true,
      showline: showAxes.value,
      linecolor: '#374151',
      linewidth: 2,
      dtick: 2,
      mirror: false,
      showticklabels: showTicks.value,
      ticks: showTicks.value ? 'outside' : ''
    },
    annotations: [
      // Flèche pour l'axe X
      {
        x: xMax.value,
        y: 0,
        xref: 'x',
        yref: 'y',
        text: '',
        showarrow: true,
        axref: 'x',
        ayref: 'y',
        ax: xMax.value * 0.95,
        ay: 0,
        arrowhead: 2,
        arrowsize: 1,
        arrowwidth: 2,
        arrowcolor: '#374151'
      },
      // Label "x" à côté de la flèche X
      {
        x: xMax.value,
        y: 0,
        xref: 'x',
        yref: 'y',
        text: '<b>x</b>',
        showarrow: false,
        xanchor: 'left',
        yanchor: 'middle',
        xshift: 10,
        yshift: -15,
        font: {
          size: 16,
          color: '#1e3a8a',
          family: 'Arial, sans-serif'
        }
      },
      // Flèche pour l'axe Y
      {
        x: 0,
        y: yMax.value,
        xref: 'x',
        yref: 'y',
        text: '',
        showarrow: true,
        axref: 'x',
        ayref: 'y',
        ax: 0,
        ay: yMax.value * 0.95,
        arrowhead: 2,
        arrowsize: 1,
        arrowwidth: 2,
        arrowcolor: '#374151'
      },
      // Label "y" à côté de la flèche Y
      {
        x: 0,
        y: yMax.value,
        xref: 'x',
        yref: 'y',
        text: '<b>y</b>',
        showarrow: false,
        xanchor: 'center',
        yanchor: 'bottom',
        xshift: 15,
        yshift: 5,
        font: {
          size: 16,
          color: '#1e3a8a',
          family: 'Arial, sans-serif'
        }
      }
    ],
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    margin: { t: 60, r: 60, b: 60, l: 80 },
    hovermode: 'closest',
    legend: {
      font: { size: 13 },
      bgcolor: 'rgba(255, 255, 255, 0.95)',
      bordercolor: '#e5e7eb',
      borderwidth: 1,
      x: 1.02,
      y: 1,
      xanchor: 'left',
      yanchor: 'top',
      orientation: 'v',
      itemsizing: 'constant',
      itemwidth: 30,
      tracegroupgap: 5
    }
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

function addManualAsymptotes(traces) {
  // Asymptotes verticales
  if (verticalAsymptotes.value.trim()) {
    const values = verticalAsymptotes.value.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v))
    values.forEach(xValue => {
      traces.push({
        x: [xValue, xValue],
        y: [yMin.value, yMax.value],
        type: 'scatter',
        mode: 'lines',
        name: `Asymptote verticale : x = ${xValue}`,
        line: {
          color: '#6b7280',
          width: 1.5,
          dash: 'dash'
        },
        showlegend: true,
        legendgroup: 'asymptotes',
        hoverinfo: 'skip'
      })
    })
  }
  
  // Asymptotes horizontales
  if (horizontalAsymptotes.value.trim()) {
    const values = horizontalAsymptotes.value.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v))
    values.forEach(yValue => {
      traces.push({
        x: [xMin.value, xMax.value],
        y: [yValue, yValue],
        type: 'scatter',
        mode: 'lines',
        name: `Asymptote horizontale : y = ${yValue}`,
        line: {
          color: '#6b7280',
          width: 1.5,
          dash: 'dash'
        },
        showlegend: true,
        legendgroup: 'asymptotes',
        hoverinfo: 'skip'
      })
    })
  }
}

function calculateIntersections(traces) {
  intersectionPoints.value = []
  
  // Comparer toutes les paires de fonctions
  for (let i = 0; i < graphFunctions.value.length; i++) {
    for (let j = i + 1; j < graphFunctions.value.length; j++) {
      const func1 = graphFunctions.value[i]
      const func2 = graphFunctions.value[j]
      
      // Calculer les points d'intersection en fonction des types
      const intersections = findIntersections(func1, func2)
      
      intersections.forEach(point => {
        // Vérifier si cette intersection n'est pas dans la liste des masquées
        const isHidden = hiddenIntersections.value.some(hidden => 
          hidden.func1Index === i + 1 && 
          hidden.func2Index === j + 1 && 
          Math.abs(hidden.x - point.x) < 0.01 && 
          Math.abs(hidden.y - point.y) < 0.01
        )
        
        if (!isHidden) {
          intersectionPoints.value.push({
            x: point.x,
            y: point.y,
            func1: func1.expression,
            func2: func2.expression,
            func1Index: i + 1,
            func2Index: j + 1,
            color1: func1.color,
            color2: func2.color
          })
          
          // Ajouter un point sur le graphique avec le label des fonctions
          const xCoord = Math.abs(point.x) < 0.01 ? 0 : Number(point.x.toFixed(2))
          const yCoord = Math.abs(point.y) < 0.01 ? 0 : Number(point.y.toFixed(2))
          const intersectionLabel = `f${i + 1} ∩ f${j + 1}: (${xCoord}, ${yCoord})`
          
          traces.push({
            x: [point.x],
            y: [point.y],
            type: 'scatter',
            mode: 'markers',
            name: intersectionLabel,
            marker: {
              color: '#dc2626',
              size: 10,
              symbol: 'circle',
              line: {
                color: 'white',
                width: 2
              }
            },
            showlegend: true,
            legendgroup: 'intersections',
            hovertemplate: `<b>Intersection f<sub>${i + 1}</sub> ∩ f<sub>${j + 1}</sub></b><br>Point: (${point.x.toFixed(3)}, ${point.y.toFixed(3)})<extra></extra>`
          })
        }
      })
    }
  }
  
  // Rendre les expressions LaTeX des intersections
  nextTick(() => renderIntersectionExpressions())
}

function findIntersections(func1, func2) {
  const intersections = []
  
  // Cas 1: Intersection entre droite verticale (x=a) et fonction normale
  if (func1.type === 'vertical' && func2.type === 'function') {
    const x = func1.value
    const js = convertLatexToJS(func2.latex)
    const y = evaluateFunction(js, x)
    if (isFinite(y) && y >= yMin.value && y <= yMax.value) {
      intersections.push({ x, y })
    }
  }
  
  // Cas 2: Intersection entre fonction normale et droite verticale (x=a)
  if (func1.type === 'function' && func2.type === 'vertical') {
    const x = func2.value
    const js = convertLatexToJS(func1.latex)
    const y = evaluateFunction(js, x)
    if (isFinite(y) && y >= yMin.value && y <= yMax.value) {
      intersections.push({ x, y })
    }
  }
  
  // Cas 3: Intersection entre droite horizontale (y=b) et fonction normale
  if (func1.type === 'horizontal' && func2.type === 'function') {
    const yTarget = func1.value
    const js = convertLatexToJS(func2.latex)
    
    // Chercher les x où f(x) = yTarget
    const numSamples = 1000
    const step = (xMax.value - xMin.value) / numSamples
    
    for (let i = 0; i < numSamples; i++) {
      const x1 = xMin.value + i * step
      const x2 = xMin.value + (i + 1) * step
      const y1 = evaluateFunction(js, x1)
      const y2 = evaluateFunction(js, x2)
      
      if (isFinite(y1) && isFinite(y2)) {
        const diff1 = y1 - yTarget
        const diff2 = y2 - yTarget
        
        if (diff1 * diff2 <= 0 && Math.abs(diff1) < 100 && Math.abs(diff2) < 100) {
          // Bissection pour trouver le x exact
          const xIntersect = findZeroForHorizontal(js, yTarget, x1, x2)
          if (xIntersect !== null) {
            const isDuplicate = intersections.some(p => Math.abs(p.x - xIntersect) < 0.1)
            if (!isDuplicate) {
              intersections.push({ x: xIntersect, y: yTarget })
            }
          }
        }
      }
    }
  }
  
  // Cas 4: Intersection entre fonction normale et droite horizontale (y=b)
  if (func1.type === 'function' && func2.type === 'horizontal') {
    const yTarget = func2.value
    const js = convertLatexToJS(func1.latex)
    
    // Chercher les x où f(x) = yTarget
    const numSamples = 1000
    const step = (xMax.value - xMin.value) / numSamples
    
    for (let i = 0; i < numSamples; i++) {
      const x1 = xMin.value + i * step
      const x2 = xMin.value + (i + 1) * step
      const y1 = evaluateFunction(js, x1)
      const y2 = evaluateFunction(js, x2)
      
      if (isFinite(y1) && isFinite(y2)) {
        const diff1 = y1 - yTarget
        const diff2 = y2 - yTarget
        
        if (diff1 * diff2 <= 0 && Math.abs(diff1) < 100 && Math.abs(diff2) < 100) {
          const xIntersect = findZeroForHorizontal(js, yTarget, x1, x2)
          if (xIntersect !== null) {
            const isDuplicate = intersections.some(p => Math.abs(p.x - xIntersect) < 0.1)
            if (!isDuplicate) {
              intersections.push({ x: xIntersect, y: yTarget })
            }
          }
        }
      }
    }
  }
  
  // Cas 5: Intersection entre droite verticale et droite horizontale
  if (func1.type === 'vertical' && func2.type === 'horizontal') {
    intersections.push({ x: func1.value, y: func2.value })
  }
  if (func1.type === 'horizontal' && func2.type === 'vertical') {
    intersections.push({ x: func2.value, y: func1.value })
  }
  
  // Cas 6: Intersection entre deux fonctions normales
  if (func1.type === 'function' && func2.type === 'function') {
    const js1 = convertLatexToJS(func1.latex)
    const js2 = convertLatexToJS(func2.latex)
    
    const numSamples = 1000
    const step = (xMax.value - xMin.value) / numSamples
    
    for (let i = 0; i < numSamples; i++) {
      const x1 = xMin.value + i * step
      const x2 = xMin.value + (i + 1) * step
      
      const y1_f1 = evaluateFunction(js1, x1)
      const y2_f1 = evaluateFunction(js1, x2)
      const y1_f2 = evaluateFunction(js2, x1)
      const y2_f2 = evaluateFunction(js2, x2)
      
      // Vérifier si les fonctions se croisent entre x1 et x2
      if (isFinite(y1_f1) && isFinite(y2_f1) && isFinite(y1_f2) && isFinite(y2_f2)) {
        const diff1 = y1_f1 - y1_f2
        const diff2 = y2_f1 - y2_f2
        
        // Si le signe change, il y a une intersection
        if (diff1 * diff2 <= 0 && Math.abs(diff1) < 100 && Math.abs(diff2) < 100) {
          // Utiliser la méthode de la bissection pour affiner
          const xIntersect = bisectionMethod(js1, js2, x1, x2)
          if (xIntersect !== null) {
            const yIntersect = evaluateFunction(js1, xIntersect)
            
            // Vérifier qu'on n'a pas déjà ce point (éviter les doublons)
            const isDuplicate = intersections.some(p => 
              Math.abs(p.x - xIntersect) < 0.1 && Math.abs(p.y - yIntersect) < 0.1
            )
            
            if (!isDuplicate && isFinite(yIntersect)) {
              intersections.push({ x: xIntersect, y: yIntersect })
            }
          }
        }
      }
    }
  }
  
  return intersections
}

// Fonction auxiliaire pour trouver l'intersection avec une droite horizontale
function findZeroForHorizontal(jsFunc, yTarget, xStart, xEnd) {
  const tolerance = 1e-6
  const maxIterations = 50
  let x1 = xStart
  let x2 = xEnd
  
  for (let i = 0; i < maxIterations; i++) {
    const xMid = (x1 + x2) / 2
    const yMid = evaluateFunction(jsFunc, xMid) - yTarget
    
    if (Math.abs(yMid) < tolerance || Math.abs(x2 - x1) < tolerance) {
      return xMid
    }
    
    const y1 = evaluateFunction(jsFunc, x1) - yTarget
    if (y1 * yMid < 0) {
      x2 = xMid
    } else {
      x1 = xMid
    }
  }
  
  return (x1 + x2) / 2
}

function calculateAxisIntersections(traces) {
  axisIntersectionPoints.value = []
  
  // Pour chaque fonction, trouver ses intersections avec les axes
  graphFunctions.value.forEach((func, index) => {
    const js = convertLatexToJS(func.latex)
    
    // Intersection avec l'axe X (y = 0)
    const xAxisIntersections = findAxisIntersections(js, 'x')
    xAxisIntersections.forEach(xValue => {
      // Vérifier si cette intersection n'est pas masquée
      const isHidden = hiddenAxisIntersections.value.some(hidden => 
        hidden.funcIndex === index + 1 && 
        hidden.axis === 'x' && 
        Math.abs(hidden.x - xValue) < 0.01
      )
      
      if (!isHidden) {
        axisIntersectionPoints.value.push({
          x: xValue,
          y: 0,
          funcIndex: index + 1,
          axis: 'x'
        })
        
        // Ajouter un marqueur sur le graphique
        const xCoord = Math.abs(xValue) < 0.01 ? 0 : Number(xValue.toFixed(2))
        traces.push({
        x: [xValue],
        y: [0],
        type: 'scatter',
        mode: 'markers',
        name: `f${index + 1} ∩ axe X: (${xCoord}, 0)`,
        marker: {
          color: '#059669',
          size: 8,
          symbol: 'x',
          line: {
            color: 'white',
            width: 1
          }
        },
        showlegend: true,
        legendgroup: 'axis-intersections',
        hovertemplate: `<b>f<sub>${index + 1}</sub> ∩ axe X</b><br>Point: (${xValue.toFixed(3)}, 0)<extra></extra>`
        })
      }
    })
    
    // Intersection avec l'axe Y (x = 0)
    const yValue = evaluateFunction(js, 0)
    if (isFinite(yValue) && yValue >= yMin.value && yValue <= yMax.value) {
      // Vérifier si cette intersection n'est pas masquée
      const isHidden = hiddenAxisIntersections.value.some(hidden => 
        hidden.funcIndex === index + 1 && 
        hidden.axis === 'y' && 
        Math.abs(hidden.y - yValue) < 0.01
      )
      
      if (!isHidden) {
        axisIntersectionPoints.value.push({
          x: 0,
          y: yValue,
          funcIndex: index + 1,
          axis: 'y'
        })
        
        // Ajouter un marqueur sur le graphique
        const yCoord = Math.abs(yValue) < 0.01 ? 0 : Number(yValue.toFixed(2))
        traces.push({
          x: [0],
          y: [yValue],
          type: 'scatter',
          mode: 'markers',
          name: `f${index + 1} ∩ axe Y: (0, ${yCoord})`,
          marker: {
            color: '#7c3aed',
            size: 8,
            symbol: 'diamond',
            line: {
              color: 'white',
              width: 1
            }
          },
          showlegend: true,
          legendgroup: 'axis-intersections',
          hovertemplate: `<b>f<sub>${index + 1}</sub> ∩ axe Y</b><br>Point: (0, ${yValue.toFixed(3)})<extra></extra>`
        })
      }
    }
  })
}

function findAxisIntersections(jsFunc, axis) {
  const intersections = []
  const numSamples = 1000
  const step = (xMax.value - xMin.value) / numSamples
  
  for (let i = 0; i < numSamples; i++) {
    const x1 = xMin.value + i * step
    const x2 = xMin.value + (i + 1) * step
    
    const y1 = evaluateFunction(jsFunc, x1)
    const y2 = evaluateFunction(jsFunc, x2)
    
    // Vérifier si la fonction croise l'axe X (y = 0)
    if (isFinite(y1) && isFinite(y2) && y1 * y2 <= 0 && Math.abs(y1) < 1000 && Math.abs(y2) < 1000) {
      // Utiliser la méthode de la bissection pour trouver le zéro
      const xZero = findZero(jsFunc, x1, x2)
      if (xZero !== null) {
        // Vérifier qu'on n'a pas déjà ce point (éviter les doublons)
        const isDuplicate = intersections.some(x => Math.abs(x - xZero) < 0.1)
        if (!isDuplicate) {
          intersections.push(xZero)
        }
      }
    }
  }
  
  return intersections
}

function findZero(jsFunc, a, b, tolerance = 0.001, maxIter = 50) {
  let iter = 0
  
  while (iter < maxIter && (b - a) > tolerance) {
    const mid = (a + b) / 2
    const y_a = evaluateFunction(jsFunc, a)
    const y_mid = evaluateFunction(jsFunc, mid)
    
    if (Math.abs(y_mid) < tolerance) {
      return mid
    }
    
    if (y_a * y_mid < 0) {
      b = mid
    } else {
      a = mid
    }
    
    iter++
  }
  
  return (a + b) / 2
}

function bisectionMethod(js1, js2, a, b, tolerance = 0.001, maxIter = 50) {
  let iter = 0
  
  while (iter < maxIter && (b - a) > tolerance) {
    const mid = (a + b) / 2
    const f1_a = evaluateFunction(js1, a)
    const f2_a = evaluateFunction(js2, a)
    const f1_mid = evaluateFunction(js1, mid)
    const f2_mid = evaluateFunction(js2, mid)
    
    const diff_a = f1_a - f2_a
    const diff_mid = f1_mid - f2_mid
    
    if (Math.abs(diff_mid) < tolerance) {
      return mid
    }
    
    if (diff_a * diff_mid < 0) {
      b = mid
    } else {
      a = mid
    }
    
    iter++
  }
  
  return (a + b) / 2
}

function renderIntersectionExpressions() {
  intersectionPoints.value.forEach((point, index) => {
    if (intersectionRefs.value[index]) {
      try {
        // Créer des éléments séparés pour le texte et les formules
        const container = intersectionRefs.value[index]
        container.innerHTML = ''
        
        const textSpan1 = document.createElement('span')
        textSpan1.textContent = 'entre '
        
        const mathSpan1 = document.createElement('span')
        katex.render(point.func1, mathSpan1, {
          throwOnError: false,
          displayMode: false
        })
        
        const textSpan2 = document.createElement('span')
        textSpan2.textContent = ' et '
        
        const mathSpan2 = document.createElement('span')
        katex.render(point.func2, mathSpan2, {
          throwOnError: false,
          displayMode: false
        })
        
        container.appendChild(textSpan1)
        container.appendChild(mathSpan1)
        container.appendChild(textSpan2)
        container.appendChild(mathSpan2)
      } catch (error) {
        console.error('Erreur de rendu KaTeX pour intersection:', error)
        intersectionRefs.value[index].textContent = `entre ${point.func1} et ${point.func2}`
      }
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
  const numPoints = 3000 // Augmenter significativement pour capturer les variations rapides
  const step = (xMax.value - xMin.value) / numPoints
  
  // Filtrage très permissif pour voir toute la courbe même avec de grandes valeurs
  const yLimit = Math.max(Math.abs(yMax.value), Math.abs(yMin.value)) * 100
  
  let lastWasValid = false
  
  for (let i = 0; i <= numPoints; i++) {
    const xi = xMin.value + i * step
    
    const yi = evaluateFunction(jsExpression, xi)
    
    // Vérifier que la valeur est valide
    if (!isNaN(yi) && isFinite(yi) && Math.abs(yi) <= yLimit) {
      x.push(xi)
      y.push(yi)
      lastWasValid = true
    } else {
      // Si la valeur n'est pas valide et qu'on avait des points valides avant,
      // ajouter un point null pour créer une discontinuité visible dans Plotly
      if (lastWasValid && x.length > 0) {
        x.push(xi)
        y.push(null)
        lastWasValid = false
      }
    }
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
  
  // 0.5) Normaliser les signes moins (gérer le signe négatif en début d'expression ou après opérateur)
  // Remplacer - par + et mettre le nombre suivant entre parenthèses avec le signe -
  // Mais seulement si ce n'est pas déjà dans une fraction ou fonction
  js = js.replace(/([+\-*/^(])[\s]*-[\s]*([a-zA-Z0-9().]+)/g, '$1(-$2)')
  // Gérer le cas du début de l'expression
  if (js.trim().startsWith('-')) {
    js = '(0' + js + ')'
  }
  
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

// Fonctions pour gérer les cercles
function addCircle() {
  if (circleR.value <= 0) {
    alert('Le rayon doit être supérieur à 0')
    return
  }
  
  const color = getNextColor()
  circles.value.push({
    h: circleH.value,
    k: circleK.value,
    r: circleR.value,
    color: color
  })
  
  plotAllFunctions()
  
  // Réinitialiser les champs
  circleH.value = 0
  circleK.value = 0
  circleR.value = 1
}

function removeCircle(index) {
  circles.value.splice(index, 1)
  plotAllFunctions()
}

// Fonctions pour gérer les points
function addPoint() {
  const color = getNextColor()
  points.value.push({
    x: pointX.value,
    y: pointY.value,
    color: color
  })
  
  plotAllFunctions()
  
  // Réinitialiser les champs
  pointX.value = 0
  pointY.value = 0
}

function removePoint(index) {
  points.value.splice(index, 1)
  plotAllFunctions()
}

function drawPoints(traces) {
  points.value.forEach((point, index) => {
    traces.push({
      x: [point.x],
      y: [point.y],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: point.color,
        size: 10,
        symbol: 'circle',
        line: {
          color: 'white',
          width: 2
        }
      },
      name: `Point ${index + 1}: (${point.x}, ${point.y})`,
      showlegend: true,
      hovertemplate: `<b>Point ${index + 1}</b><br>(${point.x}, ${point.y})<extra></extra>`
    })
  })
}

// Fonctions pour gérer les segments
function addSegment() {
  const color = getNextColor()
  segments.value.push({
    x1: segmentX1.value,
    y1: segmentY1.value,
    x2: segmentX2.value,
    y2: segmentY2.value,
    color: color
  })
  
  plotAllFunctions()
  
  // Réinitialiser les champs
  segmentX1.value = 0
  segmentY1.value = 0
  segmentX2.value = 1
  segmentY2.value = 1
}

function removeSegment(index) {
  segments.value.splice(index, 1)
  plotAllFunctions()
}

function drawSegments(traces) {
  segments.value.forEach((segment, index) => {
    // Dessiner le segment
    traces.push({
      x: [segment.x1, segment.x2],
      y: [segment.y1, segment.y2],
      type: 'scatter',
      mode: 'lines',
      line: {
        color: segment.color,
        width: 3
      },
      name: `Segment ${index + 1}: [AB]`,
      showlegend: true,
      hovertemplate: `<b>Segment ${index + 1}</b><br>De (${segment.x1}, ${segment.y1}) à (${segment.x2}, ${segment.y2})<extra></extra>`
    })
    
    // Ajouter les points d'extrémité
    traces.push({
      x: [segment.x1, segment.x2],
      y: [segment.y1, segment.y2],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: segment.color,
        size: 8,
        symbol: 'circle',
        line: {
          color: 'white',
          width: 2
        }
      },
      showlegend: false,
      hovertemplate: `<b>Extrémité</b><br>(%{x}, %{y})<extra></extra>`
    })
  })
}

function drawCircles(traces) {
  circles.value.forEach((circle, index) => {
    const numPoints = 200
    const xValues = []
    const yValues = []
    
    // Générer les points du cercle : (x-h)² + (y-k)² = r²
    for (let i = 0; i <= numPoints; i++) {
      const theta = (2 * Math.PI * i) / numPoints
      const x = circle.h + circle.r * Math.cos(theta)
      const y = circle.k + circle.r * Math.sin(theta)
      xValues.push(x)
      yValues.push(y)
    }
    
    traces.push({
      x: xValues,
      y: yValues,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: circle.color,
        width: 2
      },
      name: `Cercle ${index + 1}: centre(${circle.h}, ${circle.k}), r=${circle.r}`,
      showlegend: true,
      hovertemplate: `<b>Cercle ${index + 1}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
    })
    
    // Ajouter un point au centre du cercle
    traces.push({
      x: [circle.h],
      y: [circle.k],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: circle.color,
        size: 6,
        symbol: 'circle'
      },
      name: `Centre (${circle.h}, ${circle.k})`,
      showlegend: false,
      hovertemplate: `<b>Centre du cercle ${index + 1}</b><br>(${circle.h}, ${circle.k})<extra></extra>`
    })
  })
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

function removeIntersection(index) {
  const point = intersectionPoints.value[index]
  if (point) {
    // Ajouter à la liste des intersections masquées
    hiddenIntersections.value.push({
      func1Index: point.func1Index,
      func2Index: point.func2Index,
      x: point.x,
      y: point.y
    })
    plotAllFunctions()
  }
}

function removeAxisIntersection(index) {
  const point = axisIntersectionPoints.value[index]
  if (point) {
    // Ajouter à la liste des intersections avec axes masquées
    hiddenAxisIntersections.value.push({
      funcIndex: point.funcIndex,
      axis: point.axis,
      x: point.x,
      y: point.y
    })
    plotAllFunctions()
  }
}

// Fonction pour calculer l'intégrale numérique (méthode des trapèzes)
function numericalIntegral(jsFunc, a, b, n = 1000) {
  const h = (b - a) / n
  let sum = 0
  
  for (let i = 0; i <= n; i++) {
    const x = a + i * h
    const y = evaluateFunction(jsFunc, x)
    
    if (!isFinite(y)) continue
    
    if (i === 0 || i === n) {
      sum += y
    } else {
      sum += 2 * y
    }
  }
  
  return (h / 2) * sum
}

// Ajouter la zone d'intégration au graphique
function addIntegralAreaToGraph(traces) {
  const func1Index = integralFunc1Index.value
  const func2Index = integralFunc2Index.value
  
  if (func1Index === -1) return
  
  const a = integralA.value
  const b = integralB.value
  
  if (a >= b || a < xMin.value || b > xMax.value) return
  
  const numPoints = 200
  const step = (b - a) / numPoints
  const xValues = []
  const y1Values = []
  const y2Values = []
  
  const func1 = graphFunctions.value[func1Index]
  const func2 = func2Index !== -1 ? graphFunctions.value[func2Index] : null
  
  const js1 = func1.type === 'function' ? convertLatexToJS(func1.latex) : null
  const js2 = func2 && func2.type === 'function' ? convertLatexToJS(func2.latex) : null
  
  // Générer les points
  for (let i = 0; i <= numPoints; i++) {
    const x = a + i * step
    xValues.push(x)
    
    // Calculer y1
    let y1
    if (func1.type === 'horizontal') {
      y1 = func1.value
    } else if (func1.type === 'vertical') {
      y1 = 0
    } else {
      y1 = evaluateFunction(js1, x)
    }
    y1Values.push(isFinite(y1) ? y1 : 0)
    
    // Calculer y2
    let y2
    if (func2) {
      if (func2.type === 'horizontal') {
        y2 = func2.value
      } else if (func2.type === 'vertical') {
        y2 = 0
      } else {
        y2 = evaluateFunction(js2, x)
      }
    } else {
      y2 = 0 // Axe X par défaut
    }
    y2Values.push(isFinite(y2) ? y2 : 0)
  }
  
  // Créer une zone remplie entre les deux courbes
  // D'abord la courbe inférieure (y2)
  traces.push({
    x: xValues,
    y: y2Values,
    type: 'scatter',
    mode: 'lines',
    line: {
      width: 0
    },
    fillcolor: 'transparent',
    name: '',
    showlegend: false,
    hoverinfo: 'skip'
  })
  
  // Puis la courbe supérieure (y1) avec remplissage vers la précédente
  traces.push({
    x: xValues,
    y: y1Values,
    fill: 'tonexty',
    type: 'scatter',
    mode: 'lines',
    line: {
      width: 0
    },
    fillcolor: 'rgba(59, 130, 246, 0.3)',
    name: 'Zone d\'intégration',
    showlegend: true,
    hoverinfo: 'skip'
  })
  
  // Ajouter des lignes verticales aux bornes
  traces.push({
    x: [a, a],
    y: [Math.min(...y1Values, ...y2Values), Math.max(...y1Values, ...y2Values)],
    type: 'scatter',
    mode: 'lines',
    line: {
      color: '#3b82f6',
      width: 2,
      dash: 'dash'
    },
    name: `x = ${a}`,
    showlegend: false,
    hoverinfo: 'skip'
  })
  
  traces.push({
    x: [b, b],
    y: [Math.min(...y1Values, ...y2Values), Math.max(...y1Values, ...y2Values)],
    type: 'scatter',
    mode: 'lines',
    line: {
      color: '#3b82f6',
      width: 2,
      dash: 'dash'
    },
    name: `x = ${b}`,
    showlegend: false,
    hoverinfo: 'skip'
  })
}

// Calculer l'intégrale sous la courbe ou entre deux courbes
function calculateIntegralArea() {
  if (integralA.value >= integralB.value) {
    alert('La borne b doit être supérieure à la borne a')
    return
  }
  
  const func1Index = integralFunc1Index.value
  const func2Index = integralFunc2Index.value
  
  if (func1Index === -1 && func2Index === -1) {
    alert('Sélectionnez au moins une fonction')
    return
  }
  
  let integral = 0
  
  // Cas 1: Intégrale entre deux fonctions
  if (func1Index !== -1 && func2Index !== -1) {
    const func1 = graphFunctions.value[func1Index]
    const func2 = graphFunctions.value[func2Index]
    
    const js1 = func1.type === 'function' ? convertLatexToJS(func1.latex) : null
    const js2 = func2.type === 'function' ? convertLatexToJS(func2.latex) : null
    
    // Calculer l'intégrale de |f1(x) - f2(x)|
    const n = 1000
    const h = (integralB.value - integralA.value) / n
    
    for (let i = 0; i <= n; i++) {
      const x = integralA.value + i * h
      let y1 = 0
      let y2 = 0
      
      if (func1.type === 'vertical') {
        continue // Pas d'intégrale pour une droite verticale
      } else if (func1.type === 'horizontal') {
        y1 = func1.value
      } else {
        y1 = evaluateFunction(js1, x)
      }
      
      if (func2.type === 'vertical') {
        continue
      } else if (func2.type === 'horizontal') {
        y2 = func2.value
      } else {
        y2 = evaluateFunction(js2, x)
      }
      
      const diff = Math.abs(y1 - y2)
      
      if (!isFinite(diff)) continue
      
      if (i === 0 || i === n) {
        integral += diff
      } else {
        integral += 2 * diff
      }
    }
    
    integral = (h / 2) * integral
  } 
  // Cas 2: Intégrale sous une fonction (jusqu'à l'axe X)
  else if (func1Index !== -1) {
    const func1 = graphFunctions.value[func1Index]
    
    if (func1.type === 'vertical') {
      alert('Impossible de calculer l\'intégrale d\'une droite verticale')
      return
    } else if (func1.type === 'horizontal') {
      // Intégrale d'une constante: c * (b - a)
      integral = func1.value * (integralB.value - integralA.value)
    } else {
      const js1 = convertLatexToJS(func1.latex)
      integral = numericalIntegral(js1, integralA.value, integralB.value)
    }
  }
  
  integralResult.value = integral
  plotAllFunctions()
}

// Ajouter l'aire entre deux courbes au graphique
function addAreaBetweenCurvesToGraph(traces) {
  const curve1Index = areaCurve1Index.value
  const curve2Index = areaCurve2Index.value
  
  if (curve1Index === curve2Index || curve1Index >= graphFunctions.value.length || curve2Index >= graphFunctions.value.length) {
    return
  }
  
  const func1 = graphFunctions.value[curve1Index]
  const func2 = graphFunctions.value[curve2Index]
  
  if (func1.type !== 'function' || func2.type !== 'function') {
    return
  }
  
  const js1 = convertLatexToJS(func1.latex)
  const js2 = convertLatexToJS(func2.latex)
  
  let a = areaA.value
  let b = areaB.value
  
  // Si les bornes ne sont pas spécifiées, chercher les intersections automatiquement
  if ((a === null || a === '') && (b === null || b === '')) {
    const intersections = findIntersectionPoints(js1, js2, xMin.value, xMax.value)
    if (intersections.length >= 2) {
      a = intersections[0]
      b = intersections[1]
    } else {
      // Utiliser les bornes du graphique par défaut
      a = Math.max(xMin.value, -10)
      b = Math.min(xMax.value, 10)
    }
  } else {
    a = a === null || a === '' ? xMin.value : Number(a)
    b = b === null || b === '' ? xMax.value : Number(b)
  }
  
  if (a >= b || a < xMin.value || b > xMax.value) return
  
  const numPoints = 200
  const step = (b - a) / numPoints
  const xValues = []
  const y1Values = []
  const y2Values = []
  
  // Générer les points
  for (let i = 0; i <= numPoints; i++) {
    const x = a + i * step
    xValues.push(x)
    
    const y1 = evaluateFunction(js1, x)
    const y2 = evaluateFunction(js2, x)
    
    y1Values.push(isFinite(y1) ? y1 : 0)
    y2Values.push(isFinite(y2) ? y2 : 0)
  }
  
  // Créer une zone remplie entre les deux courbes
  traces.push({
    x: xValues,
    y: y2Values,
    type: 'scatter',
    mode: 'lines',
    line: { width: 0 },
    fillcolor: 'transparent',
    name: '',
    showlegend: false,
    hoverinfo: 'skip'
  })
  
  traces.push({
    x: xValues,
    y: y1Values,
    fill: 'tonexty',
    type: 'scatter',
    mode: 'lines',
    line: { width: 0 },
    fillcolor: 'rgba(34, 197, 94, 0.3)',
    name: 'Aire entre les courbes',
    showlegend: true,
    hoverinfo: 'skip'
  })
  
  // Lignes verticales aux bornes
  traces.push({
    x: [a, a],
    y: [Math.min(...y1Values, ...y2Values), Math.max(...y1Values, ...y2Values)],
    type: 'scatter',
    mode: 'lines',
    line: { color: '#22c55e', width: 2, dash: 'dash' },
    showlegend: false,
    hoverinfo: 'skip'
  })
  
  traces.push({
    x: [b, b],
    y: [Math.min(...y1Values, ...y2Values), Math.max(...y1Values, ...y2Values)],
    type: 'scatter',
    mode: 'lines',
    line: { color: '#22c55e', width: 2, dash: 'dash' },
    showlegend: false,
    hoverinfo: 'skip'
  })
}

// Calculer l'aire entre deux courbes
function calculateAreaBetweenCurves() {
  const curve1Index = areaCurve1Index.value
  const curve2Index = areaCurve2Index.value
  
  if (curve1Index === curve2Index || curve1Index >= graphFunctions.value.length || curve2Index >= graphFunctions.value.length) {
    alert('Sélectionnez deux courbes différentes')
    return
  }
  
  const func1 = graphFunctions.value[curve1Index]
  const func2 = graphFunctions.value[curve2Index]
  
  if (func1.type !== 'function' || func2.type !== 'function') {
    alert('Sélectionnez deux fonctions valides')
    return
  }
  
  const js1 = convertLatexToJS(func1.latex)
  const js2 = convertLatexToJS(func2.latex)
  
  let a = areaA.value
  let b = areaB.value
  
  // Si les bornes ne sont pas spécifiées, chercher les intersections
  if ((a === null || a === '') && (b === null || b === '')) {
    const intersections = findIntersectionPoints(js1, js2, xMin.value, xMax.value)
    if (intersections.length >= 2) {
      a = intersections[0]
      b = intersections[1]
    } else {
      alert('Impossible de trouver automatiquement les bornes. Veuillez les spécifier manuellement.')
      return
    }
  } else {
    a = a === null || a === '' ? xMin.value : Number(a)
    b = b === null || b === '' ? xMax.value : Number(b)
  }
  
  if (a >= b) {
    alert('La borne b doit être supérieure à la borne a')
    return
  }
  
  // Calculer l'intégrale de |f1(x) - f2(x)|
  const n = 1000
  const h = (b - a) / n
  let area = 0
  
  for (let i = 0; i <= n; i++) {
    const x = a + i * h
    const y1 = evaluateFunction(js1, x)
    const y2 = evaluateFunction(js2, x)
    const diff = Math.abs(y1 - y2)
    
    if (!isFinite(diff)) continue
    
    if (i === 0 || i === n) {
      area += diff
    } else {
      area += 2 * diff
    }
  }
  
  area = (h / 2) * area
  areaBetweenResult.value = area
  plotAllFunctions()
}

// Trouver les points d'intersection entre deux fonctions
function findIntersectionPoints(js1, js2, xStart, xEnd) {
  const intersections = []
  const step = (xEnd - xStart) / 1000
  
  for (let x = xStart; x < xEnd; x += step) {
    const y1 = evaluateFunction(js1, x)
    const y2 = evaluateFunction(js2, x)
    const y1Next = evaluateFunction(js1, x + step)
    const y2Next = evaluateFunction(js2, x + step)
    
    if (isFinite(y1) && isFinite(y2) && isFinite(y1Next) && isFinite(y2Next)) {
      const diff = y1 - y2
      const diffNext = y1Next - y2Next
      
      // Changement de signe détecté
      if (diff * diffNext < 0) {
        // Affiner avec la méthode de Newton
        let xIntersect = x
        for (let iter = 0; iter < 10; iter++) {
          const f = evaluateFunction(js1, xIntersect) - evaluateFunction(js2, xIntersect)
          const fPrime = (evaluateFunction(js1, xIntersect + 0.0001) - evaluateFunction(js2, xIntersect + 0.0001) -
                         evaluateFunction(js1, xIntersect - 0.0001) + evaluateFunction(js2, xIntersect - 0.0001)) / 0.0002
          if (Math.abs(fPrime) < 1e-10) break
          xIntersect = xIntersect - f / fPrime
        }
        intersections.push(xIntersect)
      }
    }
  }
  
  return intersections
}

// Calculer la dérivée numérique en un point
function numericalDerivative(jsFunc, x0, h = 0.0001) {
  const f_plus = evaluateFunction(jsFunc, x0 + h)
  const f_minus = evaluateFunction(jsFunc, x0 - h)
  return (f_plus - f_minus) / (2 * h)
}

// Ajouter la tangente au graphique
function addTangentToGraph(traces) {
  const funcIndex = tangentFuncIndex.value
  
  if (funcIndex === undefined || funcIndex === null || funcIndex < 0 || funcIndex >= graphFunctions.value.length) {
    return
  }
  
  const func = graphFunctions.value[funcIndex]
  
  if (func.type !== 'function') {
    return
  }
  
  const x0 = tangentX.value
  const js = convertLatexToJS(func.latex)
  
  // Calculer f(x0)
  const y0 = evaluateFunction(js, x0)
  
  if (!isFinite(y0)) {
    tangentEquation.value = 'Point invalide'
    return
  }
  
  // Calculer f'(x0)
  const slope = numericalDerivative(js, x0)
  
  if (!isFinite(slope)) {
    tangentEquation.value = 'Dérivée non définie en ce point'
    return
  }
  
  // Équation de la tangente : y = f'(x0)(x - x0) + f(x0)
  // Générer les points de la tangente sur tout le graphique
  const xValues = [xMin.value, xMax.value]
  const yValues = [
    slope * (xMin.value - x0) + y0,
    slope * (xMax.value - x0) + y0
  ]
  
  // Formater l'équation pour l'affichage
  const slopeStr = slope.toFixed(3)
  const y0Str = y0.toFixed(3)
  const x0Str = x0.toFixed(3)
  
  if (Math.abs(x0) < 0.001) {
    tangentEquation.value = `y = ${slopeStr}x + ${y0Str}`
  } else {
    tangentEquation.value = `y = ${slopeStr}(x - ${x0Str}) + ${y0Str}`
  }
  
  // Ajouter la ligne de tangente
  traces.push({
    x: xValues,
    y: yValues,
    type: 'scatter',
    mode: 'lines',
    line: {
      color: '#dc2626',
      width: 2,
      dash: 'dash'
    },
    name: `Tangente en x=${x0Str}`,
    showlegend: true,
    hovertemplate: `<b>Tangente</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
  })
  
  // Ajouter un point au point de contact
  traces.push({
    x: [x0],
    y: [y0],
    type: 'scatter',
    mode: 'markers',
    marker: {
      color: '#dc2626',
      size: 8,
      symbol: 'circle',
      line: {
        color: 'white',
        width: 2
      }
    },
    name: `Point (${x0Str}, ${y0Str})`,
    showlegend: false,
    hovertemplate: `<b>Point de tangence</b><br>x: ${x0Str}<br>y: ${y0Str}<extra></extra>`
  })
}

// Calculer et afficher les racines des fonctions
function calculateRoots(traces) {
  rootsPoints.value = []
  
  graphFunctions.value.forEach((func, index) => {
    if (func.type !== 'function') return
    
    const js = convertLatexToJS(func.latex)
    
    // Chercher les racines (f(x) = 0)
    const roots = findRoots(js)
    
    roots.forEach(xRoot => {
      rootsPoints.value.push({
        x: xRoot,
        funcIndex: index + 1,
        color: func.color
      })
      
      // Ajouter un marqueur sur le graphique
      const xCoord = Math.abs(xRoot) < 0.01 ? 0 : Number(xRoot.toFixed(3))
      traces.push({
        x: [xRoot],
        y: [0],
        type: 'scatter',
        mode: 'markers',
        name: `Racine f${index + 1}: x = ${xCoord}`,
        marker: {
          color: '#f97316',
          size: 10,
          symbol: 'x',
          line: {
            color: 'white',
            width: 2
          }
        },
        showlegend: true,
        legendgroup: 'roots',
        hovertemplate: `<b>Racine de f<sub>${index + 1}</sub></b><br>x = ${xRoot.toFixed(3)}<br>f(x) = 0<extra></extra>`
      })
    })
  })
}

// Trouver les racines (zéros) d'une fonction
function findRoots(jsFunc) {
  const roots = []
  const numSamples = 1000
  const step = (xMax.value - xMin.value) / numSamples
  
  for (let i = 0; i < numSamples; i++) {
    const x1 = xMin.value + i * step
    const x2 = xMin.value + (i + 1) * step
    
    const y1 = evaluateFunction(jsFunc, x1)
    const y2 = evaluateFunction(jsFunc, x2)
    
    // Vérifier si la fonction croise l'axe X (y = 0)
    if (isFinite(y1) && isFinite(y2) && y1 * y2 <= 0 && Math.abs(y1) < 1000 && Math.abs(y2) < 1000) {
      // Utiliser la méthode de la bissection pour trouver le zéro
      const xRoot = findZero(jsFunc, x1, x2)
      if (xRoot !== null) {
        // Vérifier qu'on n'a pas déjà ce point (éviter les doublons)
        const isDuplicate = roots.some(r => Math.abs(r - xRoot) < 0.01)
        if (!isDuplicate) {
          roots.push(xRoot)
        }
      }
    }
  }
  
  return roots
}

function renderFunctionExpressions() {
  nextTick(() => {
    graphFunctions.value.forEach((func, index) => {
      const element = functionExpressionRefs.value[index]
      if (element) {
        try {
          katex.render(func.expression, element, { 
            throwOnError: false, 
            displayMode: false
          })
        } catch (error) {
          // En cas d'erreur, afficher le texte brut
          element.textContent = func.expression
        }
      }
    })
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
            fixedrange: true,
            constrain: 'domain',
            constraintoward: 'center'
          },
          yaxis: {
            title: 'f(x)',
            range: [yMin.value, yMax.value],
            gridcolor: '#e5e7eb',
            zerolinecolor: '#374151',
            zerolinewidth: 2,
            fixedrange: true,
            scaleanchor: 'x',
            scaleratio: 1,
            constrain: 'domain',
            constraintoward: 'center'
          },
          plot_bgcolor: '#f8fafc',
          paper_bgcolor: 'white',
          margin: { t: 40, r: 40, b: 40, l: 50 },
          hovermode: 'closest',
          legend: {
            font: { size: 13 },
            bgcolor: 'rgba(255, 255, 255, 0.95)',
            bordercolor: '#e5e7eb',
            borderwidth: 1,
            x: 1.02,
            y: 1,
            xanchor: 'left',
            yanchor: 'top',
            orientation: 'v',
            itemsizing: 'constant',
            itemwidth: 30,
            tracegroupgap: 5
          }
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
  max-width: 100%;
  margin: 0.5rem 0 2rem;
  padding: 1rem;
  width: 100%;
}

.title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.8rem;
  font-weight: bold;
  color: #1e3a8a;
  margin-bottom: 1.5rem;
  text-align: center;
  justify-content: center;
}

.title-icon {
  width: 2rem;
  height: 2rem;
}

/* Styles existants pour la calculatrice */
.expr-row {
  display: flex;
  justify-content: stretch;
  margin-bottom: 1.5rem;
  width: 100%;
  padding: 0;
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

/* Styles pour les asymptotes */
.asymptotes-section {
  margin-top: 1rem;
  padding: 1rem;
  background: #fefce8;
  border: 1px solid #fde047;
  border-radius: 0.5rem;
}

.asymptotes-section .controls-title {
  margin: 0 0 0.75rem 0;
  color: #854d0e;
}

.asymptotes-section .help-text {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #a16207;
}

/* Styles pour l'option d'intersection */
.intersection-option {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.intersection-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #0c4a6e;
  cursor: pointer;
}

.intersection-checkbox-label input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  accent-color: #0284c7;
}

/* Styles pour l'option d'intégrale */
.integral-option {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 0.5rem;
}

.integral-controls {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #d1fae5;
}

.integral-function-select {
  margin-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.integral-function-select label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #065f46;
}

.calculate-integral-btn {
  margin-top: 1rem;
  width: 100%;
  padding: 0.5rem 1rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.calculate-integral-btn:hover {
  background: #059669;
}

.integral-result {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #d1fae5;
  border: 1px solid #10b981;
  border-radius: 0.5rem;
  text-align: center;
  font-size: 1rem;
  color: #065f46;
}

/* Styles pour l'option de tangente */
.tangent-option {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
}

.tangent-controls {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #fee2e2;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tangent-equation {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #fee2e2;
  border: 1px solid #dc2626;
  border-radius: 0.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #7f1d1d;
  font-family: 'Courier New', monospace;
}

/* Styles pour l'option des racines */
.roots-option {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fef9f3;
  border: 1px solid #fed7aa;
  border-radius: 0.5rem;
}

/* Styles pour l'option des cercles */
.circle-option {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
  border-radius: 0.5rem;
}

.circle-controls {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e9d5ff;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.circles-list {
  margin-top: 1rem;
  padding: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e9d5ff;
}

.circle-label {
  font-size: 0.875rem;
  color: #5b21b6;
  font-family: 'Courier New', monospace;
}

/* Liste des intersections */
.intersections-list {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
}

.intersection-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  background: white;
  border: 1px solid #fca5a5;
  border-radius: 0.375rem;
}

.intersection-item:last-child {
  margin-bottom: 0;
}

.intersection-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.remove-intersection-btn {
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

.remove-intersection-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.intersection-label {
  font-weight: 700;
  color: #7c2d12;
  font-size: 0.9rem;
  margin-right: 0.5rem;
}

.intersection-label sub {
  font-size: 0.7rem;
}

.intersection-point {
  font-weight: 600;
  color: #dc2626;
  font-family: 'Courier New', monospace;
  font-size: 0.95rem;
}

.intersection-functions {
  font-size: 0.85rem;
  color: #991b1b;
  margin-top: 0.25rem;
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
  max-width: 100%;
  margin: 0;
  display: flex;
  flex-direction: column-reverse;
}

/* Panneaux flottants au-dessus de l'input */
.floating-panels {
  position: relative;
  z-index: 100;
  margin-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 50vh;
  overflow-y: auto;
}

.floating-panel {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  animation: slideUp 0.2s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.input-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 0.5rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input-container:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

/* Forcer tous les boutons dans l'input-container à ne pas avoir de fond bleu */
.input-container button {
  background: transparent !important;
  background-color: transparent !important;
}

.input-container button:not(:disabled):hover {
  background: rgba(59, 130, 246, 0.1) !important;
  background-color: rgba(59, 130, 246, 0.1) !important;
}

.input-container button svg {
  color: #3b82f6;
}

.input-container button:disabled svg {
  color: #9ca3af;
}

.math-input {
  flex: 1;
  min-height: 50px;
  border: none;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
  background: transparent;
  transition: none;
}

.math-input:focus {
  outline: none;
  border-color: transparent;
}

.math-placeholder {
  position: absolute;
  top: 50%;
  left: 1.5rem;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
  font-size: 0.95rem;
  font-family: 'Times New Roman', serif;
  font-style: italic;
}

/* Bouton de calcul intégré à l'input */
.calculate-btn-inline {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 42px !important;
  height: 42px !important;
  background: transparent !important;
  background-color: transparent !important;
  color: #3b82f6 !important;
  border: none !important;
  border-radius: 0.5rem !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  flex-shrink: 0 !important;
  padding: 0 !important;
  margin: 0 !important;
}

.calculate-btn-inline:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.1) !important;
  background-color: rgba(59, 130, 246, 0.1) !important;
  transform: scale(1.1) !important;
  color: #2563eb !important;
}

.calculate-btn-inline:active:not(:disabled) {
  transform: scale(0.95) !important;
  background: rgba(59, 130, 246, 0.15) !important;
  background-color: rgba(59, 130, 246, 0.15) !important;
}

.calculate-btn-inline:disabled {
  background: transparent !important;
  background-color: transparent !important;
  color: #9ca3af !important;
  cursor: not-allowed !important;
  transform: none !important;
  opacity: 0.5 !important;
}

.calculate-btn-inline:focus {
  outline: none !important;
  box-shadow: none !important;
  background: transparent !important;
  background-color: transparent !important;
}

.calculate-btn-inline .spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Bouton d'options */
.options-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  background: transparent;
  color: #6b7280;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.options-btn:hover {
  background: rgba(107, 114, 128, 0.1);
  color: #374151;
  transform: scale(1.1);
}



.vk-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  background: none;
  border: none;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease;
  flex-shrink: 0;
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
  width: 100%;
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

/* Bloc d'incitation à la connexion pour les étapes */
.steps-cta {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f0f9ff;
  border-radius: 0.75rem;
  border: 1px solid #bfdbfe;
  text-align: center;
  width: 100%;
}

.steps-cta .cta-text {
  color: #1e3a8a;
  margin: 0.5rem 0 1rem;
}

.login-cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.login-cta-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
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
  margin: 2rem 0 0 0;
  padding: 1.5rem 0;
  width: 100%;
  background: white;
  border-radius: 0;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
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
  height: 70vh;
  min-height: 500px;
  max-height: 800px;
  border: none;
  border-radius: 0;
  background: white;
  margin: 0;
}

/* Wrapper pour le système d'onglets */
.graph-tabs-wrapper {
  margin: 1rem 0 1.5rem 0;
}

/* Système d'onglets en haut */
.graph-tabs-container.top-tabs {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem 0.5rem 0 0;
  overflow: hidden;
}

/* Contenu des onglets en haut */
.graph-tab-content-top {
  background: white;
  border: 1px solid #e2e8f0;
  border-top: none;
  border-radius: 0 0 0.5rem 0.5rem;
  padding: 1.5rem;
  min-height: 100px;
}

.graph-tabs {
  display: flex;
  gap: 0;
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
  overflow-x: auto;
}

.graph-tab {
  flex: 1;
  min-width: fit-content;
  padding: 0.875rem 1.25rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.graph-tab:hover {
  background: #f1f5f9;
  color: #3b82f6;
}

.graph-tab.active {
  background: white;
  color: #3b82f6;
  border-bottom-color: #3b82f6;
}

.graph-tab-content {
  padding: 0;
}

.tab-panel {
  padding: 1.5rem;
  animation: fadeIn 0.2s ease;
}

.panel-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e3a8a;
  margin: 0 0 1rem 0;
}

.no-content {
  padding: 2rem;
  text-align: center;
  color: #64748b;
  font-style: italic;
}

.functions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.display-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.95rem;
  color: #374151;
}

.checkbox-label input[type="checkbox"] {
  width: 1.1rem;
  height: 1.1rem;
  cursor: pointer;
}

.calc-section, .shape-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.calc-section:last-child, .shape-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.calc-controls {
  margin-top: 1rem;
}

.shape-title {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.75rem 0;
}

.results-section {
  margin-top: 1rem;
  padding: 1rem;
  background: #f0f9ff;
  border: 1px solid #bfdbfe;
  border-radius: 0.375rem;
}

.results-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e40af;
  margin: 0 0 0.5rem 0;
}

.result-item {
  padding: 0.5rem;
  margin-bottom: 0.25rem;
  background: white;
  border-radius: 0.25rem;
  font-size: 0.9rem;
}

.result-info {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #f0f9ff;
  border: 1px solid #bfdbfe;
  border-radius: 0.375rem;
  font-size: 0.9rem;
}

.action-btn {
  padding: 0.625rem 1.25rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.75rem;
}

.action-btn:hover {
  background: #2563eb;
}

.shapes-list {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.shape-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
}

/* Bouton d'options dans le champ - supprimé car dupliqué et cause des chevauchements */

/* Modal d'options */
.graph-options-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
  padding: 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.options-modal-content {
  background: white;
  border-radius: 1rem;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.options-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.options-modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e40af;
}

.close-modal-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #64748b;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.close-modal-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

/* Grille d'options */
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
}

.option-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.option-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.option-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2);
  transform: translateY(-4px);
}

.option-card:hover::before {
  transform: scaleX(1);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.option-card:hover .card-icon {
  animation: none;
  transform: scale(1.1);
  transition: transform 0.3s ease;
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 0.5rem;
}

.card-description {
  font-size: 0.875rem;
  color: #64748b;
}

/* Panneau d'options */
.graph-options-panel {
  animation: slideDown 0.3s ease-out;
  overflow: hidden;
  margin-top: 1rem;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    max-height: 5000px;
    transform: translateY(0);
  }
}

/* Système pliable pour les contrôles du graphique */
.graph-controls-collapsible {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
  overflow: hidden;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.graph-controls-collapsible.floating-panel {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  margin-bottom: 0.5rem;
}

.graph-controls-summary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  cursor: pointer;
  user-select: none;
  list-style: none;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  transition: all 0.2s;
  border-bottom: 1px solid transparent;
}

.graph-controls-collapsible[open] .graph-controls-summary {
  border-bottom: 1px solid #e5e7eb;
}

.graph-controls-summary:hover {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
}

.graph-controls-summary::-webkit-details-marker {
  display: none;
}

.summary-icon {
  font-size: 0.875rem;
  transition: transform 0.2s ease;
  font-weight: bold;
  min-width: 16px;
}

.graph-controls-collapsible:not([open]) .summary-icon {
  transform: rotate(0deg);
}

.graph-controls-collapsible[open] .summary-icon {
  transform: rotate(90deg);
}

.summary-text {
  font-size: 0.95rem;
  font-weight: 600;
  flex: 1;
}

.graph-controls {
  padding: 1rem;
  background: white;
}

.graph-controls > div:not(:last-child) {
  margin-bottom: 1rem;
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
    height: 60vh;
    min-height: 400px;
  }

  .graph-section {
    margin: 2rem -1rem 0 -1rem;
    padding: 1rem;
  }
  
  .bounds-row {
    grid-template-columns: 1fr 1fr;
  }
}
</style> 