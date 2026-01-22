<template>
  <component :is="layoutComponent" v-on="layoutListeners">
    <section class="calc">
      <h2 class="title"><CalculatorIcon class="title-icon"/> Outil de Calcul Scientifique</h2>

      <!-- Système d'onglets pour le graphique -->
      <div v-if="selectedOperation === 'graph'" class="graph-tabs-wrapper">
        <div class="graph-tabs-container top-tabs">
          <button 
            class="tabs-nav-btn tabs-nav-prev" 
            @click="scrollTabsLeft"
            :disabled="!canScrollLeft"
          >
            ‹
          </button>
          <div class="graph-tabs">
            <button 
              v-for="tab in visibleTabs"
              :key="tab"
              class="graph-tab" 
              :class="{ active: activeGraphTab === tab }"
              @click="activeGraphTab = tab"
            >
              {{ getTabLabel(tab) }}
            </button>
          </div>
          <button 
            class="tabs-nav-btn tabs-nav-next" 
            @click="scrollTabsRight"
            :disabled="!canScrollRight"
          >
            ›
          </button>
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
                  <input 
                    type="color" 
                    :value="func.color" 
                    @input="changeColor(index, $event.target.value)"
                    class="function-color-picker"
                    title="Changer la couleur"
                  />
                  <span class="function-name">f<sub>{{ index + 1 }}</sub>(x) =</span>
                  <span class="function-expression" :ref="el => functionExpressionRefs[index] = el" @click="editFunction(index)" style="cursor: pointer;" title="Cliquer pour modifier"></span>
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
                <label class="checkbox-label">
                  <input type="checkbox" v-model="snapToGrid" />
                  Accrocher aux intersections de la grille
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
                
                <!-- Option 1: Relier deux points existants -->
                <div v-if="points.length >= 2" class="segment-from-points">
                  <p class="helper-text">Relier deux points :</p>
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>Point 1 :</label>
                      <select v-model.number="segmentPoint1Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="index" :value="index">
                          P{{ index + 1 }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Point 2 :</label>
                      <select v-model.number="segmentPoint2Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="index" :value="index">
                          P{{ index + 1 }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                  </div>
                  <button @click="addSegmentFromPoints" class="action-btn">Relier les points</button>
                  <div class="divider-text">ou</div>
                </div>
                
                <!-- Option 2: Saisir manuellement les coordonnées -->
                <p class="helper-text">Saisir les coordonnées :</p>
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

      <!-- Zone de résultat pour les opérations non-graphique (affichée en haut) -->
      <div v-if="selectedOperation !== 'graph'" class="result-preview-container">
        <div ref="preview" class="result-preview"></div>
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
            <button class="vk-btn" @click="toggleCustomKeyboard" title="Afficher le clavier scientifique">
              <svg class="vk-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="2" y="4" width="20" height="14" rx="2"/>
                <line x1="5" y1="8" x2="7" y2="8"/>
                <line x1="9" y1="8" x2="11" y2="8"/>
                <line x1="13" y1="8" x2="15" y2="8"/>
                <line x1="17" y1="8" x2="19" y2="8"/>
                <line x1="5" y1="12" x2="7" y2="12"/>
                <line x1="9" y1="12" x2="11" y2="12"/>
                <line x1="13" y1="12" x2="15" y2="12"/>
                <line x1="17" y1="12" x2="19" y2="12"/>
                <line x1="7" y1="16" x2="17" y2="16"/>
              </svg>
            </button>
          </div>

          <!-- Clavier scientifique personnalisé -->
          <Transition name="keyboard-slide">
            <ScientificKeyboard 
              v-if="showCustomKeyboard"
              :visible="showCustomKeyboard"
              @insert="handleKeyboardInsert"
              @backspace="handleKeyboardBackspace"
              @submit="handleKeyboardSubmit"
              @calculate="handleKeyboardCalculate"
              @moveLeft="handleKeyboardMoveLeft"
              @moveRight="handleKeyboardMoveRight"
            />
          </Transition>

          <!-- Message d'erreur professionnel -->
          <div v-if="errorMessage" class="error-message-container">
            <div class="error-message-content">
              <svg class="error-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div class="error-text">
                <div class="error-title">{{ errorMessage.title }}</div>
                <div class="error-description">{{ errorMessage.description }}</div>
                <div v-if="errorMessage.examples" class="error-examples">{{ errorMessage.examples }}</div>
              </div>
            </div>
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
                <label class="integral-type-label">
                  <input type="checkbox" v-model="snapToGrid" />
                  Accrocher aux intersections de la grille
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
                
                <!-- Option 1: Relier deux points existants -->
                <div v-if="points.length >= 2" class="segment-from-points">
                  <p class="helper-text">Relier deux points :</p>
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>Point 1 :</label>
                      <select v-model.number="segmentPoint1Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="index" :value="index">
                          P{{ index + 1 }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Point 2 :</label>
                      <select v-model.number="segmentPoint2Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="index" :value="index">
                          P{{ index + 1 }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                  </div>
                  <button @click="addSegmentFromPoints" class="calculate-integral-btn" style="background: #10b981;">
                    Relier les points
                  </button>
                  <div class="divider-text">ou</div>
                </div>
                
                <!-- Option 2: Saisir manuellement les coordonnées -->
                <div class="segment-controls">
                  <p class="helper-text">Saisir les coordonnées :</p>
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

      <!-- Conteneur du graphique -->
      <div v-if="selectedOperation === 'graph'" class="graph-section">
        <div class="graph-header">
          <h3 class="graph-title">Graphique Interactif</h3>
          <div class="graph-actions">
            <button @click="clearGraph" class="clear-graph-btn">Effacer tout</button>
            <button @click="resetZoom" class="reset-zoom-btn">Réinitialiser zoom</button>
          </div>
        </div>
        

        
        <div class="graph-container-wrapper">
          <!-- Indicateur de chargement de Plotly -->
          <div v-if="isPlotlyLoading" class="plotly-loading-overlay">
            <div class="plotly-loading-spinner"></div>
            <span>Chargement du graphique...</span>
          </div>
          <div ref="graphContainer" class="graph-container"></div>
        </div>
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

import { useSubjectsStore } from '@/stores/subjects/index'
import { useUserStore } from '@/stores/user'
import { useModalManager, MODAL_IDS } from '@/composables/useModalManager'

// Import des composables calculator
import { 
  useGraph, 
  useGraphShapes, 
  useGraphAnalysis,
  GRAPH_COLORS,
  KEYBOARD_TOOLS,
  createGraphLayout,
  PLOTLY_CONFIG,
  convertLatexToJS,
  evaluateFunction,
  generateFunctionData
} from '@/composables/calculator'

// Import du clavier scientifique
import ScientificKeyboard from '@/components/calculator/ScientificKeyboard.vue'

// Store pour les matières
const subjectsStore = useSubjectsStore()
const userStore = useUserStore()
const { openModal } = useModalManager()
const route = useRoute()
const router = useRouter()

// Initialisation des composables
const graph = useGraph()
const shapes = useGraphShapes()

// Destructuration du composable graph pour utilisation dans le template
const { 
  graphContainer, 
  functionExpressionRefs,
  xMin, xMax, yMin, yMax, 
  showGrid, showAxes, showTicks,
  graphFunctions
} = graph

// Destructuration du composable shapes
const {
  points, segments, circles,
  pointX, pointY,
  segmentX1, segmentY1, segmentX2, segmentY2,
  circleH, circleK, circleR
} = shapes

// Initialisation du composable analysis avec les refs du graph
const analysis = useGraphAnalysis(graphFunctions, xMin, xMax, yMin, yMax)

// Destructuration du composable analysis
const {
  showIntersections, intersectionPoints, hiddenIntersections, intersectionRefs,
  showAxisIntersections, axisIntersectionPoints, hiddenAxisIntersections,
  verticalAsymptotes, horizontalAsymptotes,
  showIntegralArea, integralA, integralB, integralFunc1Index, integralFunc2Index, integralResult,
  showAreaBetweenCurves, areaCurve1Index, areaCurve2Index, areaA, areaB, areaBetweenResult,
  showTangent, tangentFuncIndex, tangentX, tangentEquation,
  showRoots, rootsPoints
} = analysis

const preview = ref(null)
const mf = ref(null)
const isFocused = ref(false)
const expressionValue = ref('')
const originalExpressionRef = ref(null)
const resultData = ref(null)
const placeholderRef = ref(null)
const showCustomKeyboard = ref(false)  // Clavier caché par défaut
const activeTab = ref('algebra')
const isCalculating = ref(false)
const selectedOperation = computed(() => route.query.operation || 'graph')
const hasCalculated = ref(false)
const errorMessage = ref(null)

// Plotly est chargé dynamiquement pour optimiser le temps de chargement initial
let Plotly = null
const isPlotlyLoading = ref(false)
const isPlotlyLoaded = ref(false)

async function loadPlotly() {
  if (Plotly) return Plotly
  if (isPlotlyLoading.value) {
    // Attendre que le chargement en cours se termine
    while (isPlotlyLoading.value) {
      await new Promise(resolve => setTimeout(resolve, 50))
    }
    return Plotly
  }
  
  isPlotlyLoading.value = true
  try {
    const module = await import('plotly.js-dist-min')
    Plotly = module.default
    isPlotlyLoaded.value = true
    return Plotly
  } catch (error) {
    console.error('Erreur lors du chargement de Plotly:', error)
    throw error
  } finally {
    isPlotlyLoading.value = false
  }
}

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

// Variable pour afficher/masquer le panneau d'options
const showGraphOptions = ref(false)
const activeSection = ref('')
const activeGraphTab = ref('functions')

// Navigation des onglets sur mobile (carousel de 4 onglets)
const allGraphTabs = ['functions', 'axes', 'asymptotes', 'analysis', 'calculus', 'shapes']
const tabsStartIndex = ref(0)
const visibleTabsCount = 4

const visibleTabs = computed(() => {
  return allGraphTabs.slice(tabsStartIndex.value, tabsStartIndex.value + visibleTabsCount)
})

const canScrollLeft = computed(() => tabsStartIndex.value > 0)
const canScrollRight = computed(() => tabsStartIndex.value < allGraphTabs.length - visibleTabsCount)

const scrollTabsLeft = () => {
  if (canScrollLeft.value) {
    tabsStartIndex.value--
  }
}

const scrollTabsRight = () => {
  if (canScrollRight.value) {
    tabsStartIndex.value++
  }
}

const getTabLabel = (tab) => {
  const labels = {
    functions: '📈 Fonctions',
    axes: '⚙️ Axes',
    asymptotes: '📐 Asymptotes',
    analysis: '🔍 Analyse',
    calculus: '📊 Calcul',
    shapes: '🟢 Formes'
  }
  return labels[tab] || tab
}

// Mode snap to grid pour les points
const snapToGrid = ref(true)

// Sélection de points pour créer des segments
const segmentPoint1Index = ref(0)
const segmentPoint2Index = ref(1)

// Outils pour le clavier personnalisé (depuis la config)
const algebraTools = KEYBOARD_TOOLS.algebra
const trigonometryTools = KEYBOARD_TOOLS.trigonometry
const exponentialTools = KEYBOARD_TOOLS.exponential
const specialFunctions = KEYBOARD_TOOLS.special

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
    graphFunctions.value = []
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
      return { text: 'Fonction à tracer (ex: ', latex: 'x^{2}, \\sin(x)' }
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

// Variable pour le debounce du resize
let resizeTimeout = null

// Gestionnaire de redimensionnement pour adapter le graphique mobile/desktop
function handleResize() {
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }
  resizeTimeout = setTimeout(() => {
    if (selectedOperation.value === 'graph' && graphContainer.value) {
      // Re-render le graphique avec la nouvelle configuration mobile/desktop
      plotAllFunctions()
    }
  }, 250) // Debounce 250ms
}

onMounted(async () => {
  await nextTick()
  if (mf.value) {
    mf.value.virtualKeyboardMode = 'off'
  }
  
  // Rendre le placeholder initial
  renderPlaceholder()
  
  // Initialiser le graphique si on est sur l'opération graph
  if (selectedOperation.value === 'graph') {
    nextTick(() => initializeGraph())
  } else {
    // Précharger Plotly en arrière-plan après un court délai
    // pour que le graphique soit prêt quand l'utilisateur clique dessus
    setTimeout(() => {
      loadPlotly().catch(() => {
        // Silencieux - le chargement sera réessayé si nécessaire
      })
    }, 1000)
  }
  
  // Gestionnaire de clic à l'extérieur pour fermer le clavier
  document.addEventListener('click', handleClickOutside)
  
  // Gestionnaire de redimensionnement pour adapter le graphique
  window.addEventListener('resize', handleResize)
})

// Watcher pour mettre à jour le placeholder quand l'opération change
watch(() => selectedOperation.value, () => {
  // Réinitialiser tout le contenu quand on change d'opération
  if (mf.value) {
    mf.value.value = ''
  }
  expressionValue.value = ''
  hasCalculated.value = false
  
  // Vider le preview
  if (preview.value) {
    preview.value.innerHTML = ''
  }
  
  // Vider le graphique si c'est l'opération graphique
  if (selectedOperation.value === 'graph') {
    graphFunctions.value = []
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

// Nettoyer les écouteurs d'événements
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }
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
    } else if (val === '\\sqrt[n]{}' || val === '\\sqrt[{}]{}') {
      field.executeCommand('insert', '\\sqrt[#0]{#0}');
    } else if (val === '\\sqrt{}') {
      field.executeCommand('insert', '\\sqrt{#0}');
    } else if (val === '\\frac{}{}') {
      field.executeCommand('insert', '\\frac{#0}{#0}');
    } else if (val === '\\binom{}{}') {
      field.executeCommand('insert', '\\binom{#0}{#0}');
    } else if (val === '^{}') {
      field.executeCommand('insert', '^{#0}');
    } else if (val === '_{}') {
      field.executeCommand('insert', '_{#0}');
    } else if (val === '^2') {
      field.executeCommand('insert', '^{2}');
    } else if (val === '|{}|') {
      field.executeCommand('insert', '\\left|#0\\right|');
    } else if (val === '{}!') {
      field.executeCommand('insert', '{#0}!');
    } else if (val === '\\lfloor{}\\rfloor') {
      field.executeCommand('insert', '\\lfloor{#0}\\rfloor');
    } else if (val === '\\lceil{}\\rceil') {
      field.executeCommand('insert', '\\lceil{#0}\\rceil');
    } else if (val === '\\log_{}') {
      field.executeCommand('insert', '\\log_{#0}');
    } else if (val === '\\int_{}^{}') {
      field.executeCommand('insert', '\\int_{#0}^{#0}');
    } else if (val === 'e^{}') {
      field.executeCommand('insert', 'e^{#0}');
    } else if (val === 'x_{}') {
      field.executeCommand('insert', 'x_{#0}');
    } else if (val === 'y_{}') {
      field.executeCommand('insert', 'y_{#0}');
    } else if (val === 'x^{}') {
      field.executeCommand('insert', 'x^{#0}');
    } else if (val === '\\overline{}') {
      field.executeCommand('insert', '\\overline{#0}');
    } else if (val === '\\vec{}') {
      field.executeCommand('insert', '\\vec{#0}');
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
    // Afficher uniquement le résultat final
    if (preview.value && data.result_latex) {
      try {
        katex.render(data.result_latex, preview.value, { throwOnError: false, displayMode: true })
      } catch (e) {
        preview.value.innerText = data.result_latex
      }
    }
  } catch (e) {
    let msg = e?.response?.data?.detail || e.message || 'Erreur inconnue'
    resultData.value = null
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

// Fonction pour basculer le clavier personnalisé
function toggleCustomKeyboard() {
  showCustomKeyboard.value = !showCustomKeyboard.value
  if (showCustomKeyboard.value && mf.value) {
    mf.value.focus()
  }
}

// Fonctions pour gérer les événements du clavier personnalisé
function handleKeyboardInsert(val) {
  insert(val)
}

function handleKeyboardBackspace() {
  if (mf.value) {
    mf.value.executeCommand('deleteBackward')
    mf.value.focus()
  }
}

function handleKeyboardSubmit() {
  if (selectedOperation.value === 'graph') {
    plotFunction()
  } else {
    calculate()
  }
}

function handleKeyboardCalculate() {
  if (selectedOperation.value === 'graph') {
    plotFunction()
  } else {
    calculate()
  }
}

function handleKeyboardMoveLeft() {
  if (mf.value) {
    mf.value.executeCommand('moveToPreviousChar')
    mf.value.focus()
  }
}

function handleKeyboardMoveRight() {
  if (mf.value) {
    mf.value.executeCommand('moveToNextChar')
    mf.value.focus()
  }
}

// Fonctions pour le graphique
// Fonction pour isoler y dans une équation simple
function solveForY(leftSide, rightSide) {
  try {
    // Remplacer les espaces
    let left = leftSide.replace(/\s/g, '')
    let right = rightSide.replace(/\s/g, '')
    
    // Cas 1: y est seul à gauche (y = ...)
    if (left === 'y') {
      return right
    }
    
    // Cas 2: y est seul à droite (... = y)
    if (right === 'y') {
      return left
    }
    
    // Cas 3: Équations linéaires simples comme y+2x=0 ou 2x+y=3
    // On cherche y isolé ou avec un coefficient
    
    // Si y est à gauche
    if (left.includes('y')) {
      // Déplacer tout ce qui n'est pas y vers la droite
      // Pattern: y + terme ou y - terme ou terme + y ou terme - y
      
      // y + terme = right  =>  y = right - terme
      let match = left.match(/^y\+(.+)$/)
      if (match) {
        return `(${right})-(${match[1]})`
      }
      
      // y - terme = right  =>  y = right + terme
      match = left.match(/^y-(.+)$/)
      if (match) {
        return `(${right})+(${match[1]})`
      }
      
      // terme + y = right  =>  y = right - terme
      match = left.match(/^(.+)\+y$/)
      if (match) {
        return `(${right})-(${match[1]})`
      }
      
      // terme - y = right  =>  y = terme - right
      match = left.match(/^(.+)-y$/)
      if (match) {
        return `(${match[1]})-(${right})`
      }
      
      // coef*y = right  =>  y = right / coef
      match = left.match(/^([\-\d\.]*)\*?y$/)
      if (match && match[1]) {
        const coef = match[1] === '-' ? '-1' : match[1]
        return `(${right})/(${coef})`
      }
      
      // Si y est le seul terme
      if (left === 'y') {
        return right
      }
    }
    
    // Si y est à droite, inverser
    if (right.includes('y')) {
      return solveForY(right, left)
    }
    
    return null
  } catch (error) {
    console.error('Erreur solveForY:', error)
    return null
  }
}

async function plotFunction() {
  if (!mf.value?.value || !mf.value.value.trim()) {
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Veuillez saisir une fonction à tracer</span>`
    }
    return
  }

  try {
    let rawExpression = mf.value.value.trim()
    const color = getNextColor()
    
    // Nettoyer l'expression : remplacer les espaces multiples
    rawExpression = rawExpression.replace(/\s+/g, ' ')
    
    // Vérifier qu'il n'y a pas de variables autres que x et y
    // Créer une copie pour l'analyse
    let testExpression = rawExpression
      // Retirer les commandes LaTeX courantes
      .replace(/\\(sin|cos|tan|ln|log|exp|sqrt|frac|left|right|vert|pi|abs)/g, '')
      .replace(/\\[a-zA-Z]+/g, '') // Retirer toutes les autres commandes LaTeX
      .replace(/Math\.[a-zA-Z]+/g, '') // Retirer Math.xxx
      .replace(/\d+(\.\d+)?/g, '') // Retirer les nombres (entiers et décimaux)
      .replace(/[+\-*/^()={}[\]|.\s,]/g, '') // Retirer les opérateurs et symboles
    
    // Trouver toutes les lettres qui restent (ce sont des variables potentielles)
    const variables = testExpression.match(/[a-zA-Z]/g) || []
    
    // Filtrer pour garder uniquement les variables invalides (ni x, ni y, ni e)
    const invalidVars = variables.filter(v => v !== 'x' && v !== 'y' && v !== 'e')
    
    // Si on trouve des variables invalides, afficher un avertissement
    if (invalidVars.length > 0) {
      const uniqueInvalidVars = [...new Set(invalidVars)].join(', ')
      
      // Afficher un message d'erreur professionnel
      errorMessage.value = {
        title: `Variable(s) non autorisée(s) : "${uniqueInvalidVars}"`,
        description: 'Pour tracer un graphique, utilisez uniquement les variables x et/ou y.',
        examples: 'Exemples : y = 2x + 3, x² + 3, y + 2x = 0'
      }
      
      return
    }
    
    // Effacer le message d'erreur si tout est OK
    errorMessage.value = null
    
    let processedExpression = rawExpression
    let displayExpression = rawExpression
    
    // Détecter si c'est une droite verticale (x=nombre) ou horizontale (y=nombre)
    let type = 'function'
    let value = null
    
    const verticalMatch = rawExpression.match(/^x\s*=\s*([\-\d\.]+)$/)
    const horizontalMatch = rawExpression.match(/^y\s*=\s*([\-\d\.]+)$/)
    
    if (verticalMatch) {
      type = 'vertical'
      value = parseFloat(verticalMatch[1])
      processedExpression = rawExpression
    } else if (horizontalMatch) {
      type = 'horizontal'
      value = parseFloat(horizontalMatch[1])
      processedExpression = rawExpression
    } else {
      // Gérer les équations avec y = ...
      const yEqualsMatch = rawExpression.match(/^y\s*=\s*(.+)$/)
      if (yEqualsMatch) {
        // Si l'utilisateur écrit y = x^2+3, on prend juste x^2+3
        processedExpression = yEqualsMatch[1].trim()
        displayExpression = rawExpression // Garder y = pour l'affichage
      } else {
        // Gérer les équations linéaires comme y+2x=0
        const equationMatch = rawExpression.match(/^(.+?)=(.+?)$/)
        if (equationMatch) {
          const leftSide = equationMatch[1].trim()
          const rightSide = equationMatch[2].trim()
          
          // Si le côté gauche ou droit contient y
          if (leftSide.includes('y') || rightSide.includes('y')) {
            // Essayer d'isoler y (pour les équations linéaires)
            processedExpression = solveForY(leftSide, rightSide)
            if (!processedExpression) {
              if (preview.value) {
                preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Impossible de résoudre cette équation. Utilisez le format y = ...</span>`
              }
              return
            }
            displayExpression = rawExpression
          }
        }
      }
    }
    
    // Ajouter la fonction à la liste
    graphFunctions.value.push({
      expression: displayExpression,
      color: color,
      latex: processedExpression,
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

// Gérer le clic sur le graphique pour ajouter un point
function handleGraphClick(event) {
  if (!graphContainer.value || !graphContainer.value._fullLayout) return
  
  // Ne rien faire si c'est un clic sur les boutons de la barre d'outils
  if (event.target.closest('.modebar')) return
  
  const xaxis = graphContainer.value._fullLayout.xaxis
  const yaxis = graphContainer.value._fullLayout.yaxis
  
  // Obtenir la position du clic par rapport au conteneur du graphique
  const plotArea = graphContainer.value.querySelector('.plotly')
  if (!plotArea) return
  
  const bb = plotArea.getBoundingClientRect()
  
  // Position du clic dans le conteneur
  const xInPx = event.clientX - bb.left
  const yInPx = event.clientY - bb.top
  
  // Dimensions et position de la zone de tracé
  const plotWidth = xaxis._length
  const plotHeight = yaxis._length
  const plotLeft = xaxis._offset
  const plotBottom = yaxis._offset
  
  // Vérifier que le clic est dans la zone de tracé
  if (xInPx < plotLeft || xInPx > plotLeft + plotWidth || 
      yInPx < plotBottom || yInPx > plotBottom + plotHeight) {
    return
  }
  
  // Calculer la position relative dans la zone de tracé (0 à 1)
  const xRel = (xInPx - plotLeft) / plotWidth
  const yRel = 1 - ((yInPx - plotBottom) / plotHeight) // Inverser Y car les pixels commencent en haut
  
  // Convertir en coordonnées du graphique
  const xRange = xaxis.range[1] - xaxis.range[0]
  const yRange = yaxis.range[1] - yaxis.range[0]
  
  let x = xaxis.range[0] + xRel * xRange
  let y = yaxis.range[0] + yRel * yRange
  
  // Vérifier que les coordonnées sont valides
  if (x === undefined || y === undefined || isNaN(x) || isNaN(y)) return
  
  // Si le mode snap to grid est activé, forcer l'accrochage à la grille
  if (snapToGrid.value) {
    x = Math.round(x)
    y = Math.round(y)
  } else {
    // Sinon, arrondir aux intersections de la grille si proche
    const gridX = Math.round(x)
    const gridY = Math.round(y)
    const snapThreshold = 0.15 // Seuil pour accrocher à la grille
    
    if (Math.abs(x - gridX) < snapThreshold) x = gridX
    if (Math.abs(y - gridY) < snapThreshold) y = gridY
    
    // Arrondir à 2 décimales pour éviter les valeurs trop longues
    x = Math.round(x * 100) / 100
    y = Math.round(y * 100) / 100
  }
  
  // Vérifier si ce point existe déjà
  const existingPoint = points.value.find(
    p => Math.abs(p.x - x) < 0.01 && Math.abs(p.y - y) < 0.01
  )
  
  if (existingPoint) {
    // Si le point existe déjà, on ne l'ajoute pas
    return
  }
  
  // Choisir une couleur différente pour chaque point (rotation dans GRAPH_COLORS)
  const colorIndex = points.value.length % GRAPH_COLORS.length
  const pointColor = GRAPH_COLORS[colorIndex]
  
  // Ajouter le point au tableau (utilise le tableau points du composable shapes)
  points.value.push({
    x: x,
    y: y,
    color: pointColor
  })
  
  // Redessiner le graphique avec le nouveau point
  plotAllFunctions()
}

async function plotAllFunctions() {
  if (!graphContainer.value) return
  
  // Charger Plotly dynamiquement si ce n'est pas déjà fait
  try {
    await loadPlotly()
  } catch (error) {
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>Erreur de chargement du graphique</span>`
    }
    return
  }

  const mobileViewport =
    typeof window !== 'undefined' &&
    (window.matchMedia?.('(max-width: 768px)')?.matches ?? window.innerWidth <= 768)

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
        const { x, y } = generateFunctionData(func.latex, xMin.value, xMax.value, yMin.value, yMax.value, 3000)
        
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
      title: showAxes.value ? {
        text: 'x',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      } : { text: '' },
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
      tickmode: 'linear',
      tick0: 0,
      dtick: 1,
      ticklabelstep: 2,
      tickfont: { size: mobileViewport ? 9 : 12 },
      showticklabels: showTicks.value,
      ticks: showTicks.value ? 'outside' : '',
      scaleanchor: 'y',
      scaleratio: 1,
      constrain: 'domain',
      constraintoward: 'center'
    },
    yaxis: {
      title: showAxes.value ? {
        text: 'y',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      } : { text: '' },
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
      dtick: 1,
      mirror: false,
      tickmode: 'linear',
      tick0: 0,
      ticklabelstep: 2,
      tickfont: { size: mobileViewport ? 9 : 12 },
      showticklabels: showTicks.value,
      ticks: showTicks.value ? 'outside' : '',
      constrain: 'domain',
      constraintoward: 'center'
    },
    annotations: showAxes.value ? [
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
        xshift: 8,
        yshift: 0,
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
        xshift: 1,
        yshift: 8,
        font: {
          size: 16,
          color: '#1e3a8a',
          family: 'Arial, sans-serif'
        }
      }
    ] : [],
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    margin: { t: 60, r: 60, b: 60, l: 80 },
    hovermode: 'closest',
    legend: {
      font: { size: 13 },
      bgcolor: 'rgba(255, 255, 255, 0.95)',
      bordercolor: '#e5e7eb',
      borderwidth: 1,
      x: 1,
      y: 1,
      xanchor: 'right',
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
    ],
    toImageButtonOptions: {
      format: 'png',
      filename: 'graphique_optitab',
      width: 1400,
      height: 1000,
      scale: 2
    }
  }

  Plotly.newPlot(graphContainer.value, traces, layout, config)
    .then(() => {
      // Rerendre les expressions après le tracé
      nextTick(() => renderFunctionExpressions())
      
      // Retirer l'ancien écouteur s'il existe
      if (graphContainer.value._clickListener) {
        graphContainer.value.removeEventListener('click', graphContainer.value._clickListener)
      }
      
      // Ajouter l'écouteur de clic pour ajouter des points
      graphContainer.value._clickListener = handleGraphClick
      graphContainer.value.addEventListener('click', handleGraphClick)
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

// Note: generateFunctionData, convertLatexToJS et evaluateFunction sont importés depuis @/composables/calculator

// Utiliser getNextColor depuis le composable shapes
const getNextColor = () => shapes.getNextColor()

// Fonctions pour gérer les cercles - délègue au composable shapes
function addCircle() {
  shapes.addCircle(plotAllFunctions)
}

function removeCircle(index) {
  shapes.removeCircle(index, plotAllFunctions)
}

// Fonctions pour gérer les points - délègue au composable shapes
function addPoint() {
  shapes.addPoint(plotAllFunctions)
}

function removePoint(index) {
  shapes.removePoint(index, plotAllFunctions)
}

// Fonctions pour gérer les segments - délègue au composable shapes
function addSegment() {
  shapes.addSegment(plotAllFunctions)
}

function addSegmentFromPoints() {
  if (points.value.length < 2) return
  
  const point1 = points.value[segmentPoint1Index.value]
  const point2 = points.value[segmentPoint2Index.value]
  
  if (!point1 || !point2 || segmentPoint1Index.value === segmentPoint2Index.value) {
    return
  }
  
  // Créer le segment en utilisant les coordonnées des points sélectionnés
  segmentX1.value = point1.x
  segmentY1.value = point1.y
  segmentX2.value = point2.x
  segmentY2.value = point2.y
  
  // Ajouter le segment
  shapes.addSegment(plotAllFunctions)
}

function removeSegment(index) {
  shapes.removeSegment(index, plotAllFunctions)
}

// Fonctions de dessin - délègue au composable shapes
function drawPoints(traces) {
  shapes.drawPoints(traces)
}

function drawSegments(traces) {
  shapes.drawSegments(traces)
}

function drawCircles(traces) {
  shapes.drawCircles(traces)
}

function editFunction(index) {
  const func = graphFunctions.value[index]
  if (func && mf.value) {
    // Charger l'expression dans le champ de saisie
    mf.value.value = func.expression
    expressionValue.value = func.expression
    
    // Supprimer la fonction de la liste pour permettre la modification
    removeFunction(index)
    
    // Mettre le focus sur le champ de saisie
    nextTick(() => {
      if (mf.value) {
        mf.value.focus()
      }
    })
    
    if (preview.value) {
      preview.value.innerHTML = `<span style='color:#3b82f6;font-size:0.9rem;'>Fonction chargée pour modification</span>`
    }
  }
}

function removeFunction(index) {
  graphFunctions.value.splice(index, 1)
  if (graphFunctions.value.length > 0) {
    plotAllFunctions()
    // Rerendre les expressions après suppression
    nextTick(() => renderFunctionExpressions())
  } else {
    clearGraph()
    nextTick(() => initializeGraph())
  }
}

function changeColor(index, newColor) {
  if (graphFunctions.value[index]) {
    graphFunctions.value[index].color = newColor
    plotAllFunctions()
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

async function clearGraph() {
  graphFunctions.value = []
  if (graphContainer.value && Plotly) {
    Plotly.purge(graphContainer.value)
  }
  if (preview.value) {
    preview.value.innerHTML = ''
  }
}

async function resetZoom() {
  if (graphContainer.value && graphFunctions.value.length > 0 && Plotly) {
    Plotly.relayout(graphContainer.value, {
      'xaxis.range': [xMin.value, xMax.value],
      'yaxis.range': [yMin.value, yMax.value]
    })
  }
}

// Initialiser le graphique quand l'onglet graphique est sélectionné
async function initializeGraph() {
  if (selectedOperation.value === 'graph') {
    await nextTick()
    if (graphContainer.value) {
      // Utiliser plotAllFunctions pour garantir la même taille de graphique
      // qu'il soit vide ou avec des fonctions
      await plotAllFunctions()
    }
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

/* Message d'erreur professionnel */
.error-message-container {
  margin-top: 0.75rem;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-message-content {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-left: 4px solid #ef4444;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.error-icon {
  flex-shrink: 0;
  color: #ef4444;
  margin-top: 0.125rem;
}

.error-text {
  flex: 1;
}

.error-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: #991b1b;
  margin-bottom: 0.25rem;
}

.error-description {
  font-size: 0.875rem;
  color: #7f1d1d;
  line-height: 1.5;
}

.error-examples {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #fecaca;
  font-size: 0.8125rem;
  color: #991b1b;
  font-style: italic;
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
  flex-direction: column;
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

/* Zone de résultat pour les opérations non-graphique */
.result-preview-container {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  width: 100%;
  min-height: 60px;
}

.result-preview {
  text-align: center;
  padding: 0.5rem;
  font-size: 1.1rem;
}

.result-preview .katex {
  font-size: 1.2em;
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
    padding: 0.75rem;
    margin: 0.25rem 0 1rem;
  }
  
  /* Titre plus compact sur mobile */
  .title {
    font-size: 1.1rem;
    gap: 0.35rem;
    margin-bottom: 0.75rem;
  }
  
  .title-icon {
    width: 1.25rem;
    height: 1.25rem;
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
  
  /* Input container mobile */
  .input-container {
    gap: 0.35rem;
  }
  
  .math-input {
    font-size: 1rem;
    padding: 0.6rem 0.75rem;
  }
  
  .calculate-btn-inline,
  .vk-btn {
    padding: 0.5rem;
    min-width: 36px;
  }
  
  .expr-row {
    margin-bottom: 1rem;
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

.graph-container-wrapper {
  position: relative;
  width: 100%;
}

.graph-container {
  width: 100%;
  aspect-ratio: 4 / 3;
  min-height: 500px;
  max-height: 85vh;
  border: none;
  border-radius: 0;
  background: white;
  margin: 0;
}

/* Indicateur de chargement de Plotly */
.plotly-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  z-index: 10;
  gap: 1rem;
  color: #64748b;
  font-size: 0.95rem;
}

.plotly-loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: plotly-spin 0.8s linear infinite;
}

@keyframes plotly-spin {
  to {
    transform: rotate(360deg);
  }
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
  display: flex;
  align-items: stretch;
}

/* Boutons de navigation des onglets */
.tabs-nav-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  min-width: 32px;
  background: #f8fafc;
  border: none;
  color: #64748b;
  font-size: 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.tabs-nav-btn:hover:not(:disabled) {
  background: #e2e8f0;
  color: #3b82f6;
}

.tabs-nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.tabs-nav-prev {
  border-right: 1px solid #e2e8f0;
}

.tabs-nav-next {
  border-left: 1px solid #e2e8f0;
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
  flex: 1;
  gap: 0;
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
  overflow: hidden;
}

.graph-tab {
  flex: 1;
  min-width: 0;
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

.helper-text {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0.5rem 0;
  font-weight: 500;
}

.divider-text {
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
  margin: 0.75rem 0;
  position: relative;
}

.divider-text::before,
.divider-text::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #e5e7eb;
}

.divider-text::before {
  left: 0;
}

.divider-text::after {
  right: 0;
}

.segment-from-points {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
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

.function-color-picker {
  width: 2.5rem;
  height: 2rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.375rem;
  cursor: pointer;
  flex-shrink: 0;
  padding: 0;
  transition: all 0.2s ease;
}

.function-color-picker:hover {
  border-color: #3b82f6;
  transform: scale(1.05);
}

.function-color-picker::-webkit-color-swatch-wrapper {
  padding: 0;
}

.function-color-picker::-webkit-color-swatch {
  border: none;
  border-radius: 0.25rem;
}

.function-color-picker::-moz-color-swatch {
  border: none;
  border-radius: 0.25rem;
}

.function-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: #1e3a8a;
  white-space: nowrap;
  flex-shrink: 0;
}

.function-name sub {
  font-size: 0.75rem;
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
    padding: 0 0.75rem;
  }
  
  .graph-actions {
    width: 100%;
    justify-content: stretch;
  }
  
  .clear-graph-btn,
  .reset-zoom-btn {
    flex: 1;
  }
  
  /* Container graphique mobile optimisé - VRAIE pleine largeur */
  .graph-container-wrapper {
    width: 100vw !important;
    margin-left: calc(-50vw + 50%) !important;
    margin-right: calc(-50vw + 50%) !important;
  }
  
  .graph-container {
    width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    height: auto !important;
    aspect-ratio: 1 / 1;
    min-height: 300px;
    max-height: 85vh;
    border-radius: 0;
    background: #fff;
  }
  
  /* Deep selector pour forcer Plotly à s'adapter */
  .graph-container :deep(.js-plotly-plot),
  .graph-container :deep(.plotly),
  .graph-container :deep(.plot-container) {
    width: 100% !important;
    height: 100% !important;
  }
  
  .graph-container :deep(.main-svg) {
    width: 100% !important;
    height: 100% !important;
  }
  
  /* Supprimer les marges internes de Plotly sur mobile */
  .graph-container :deep(.plotly .main-svg) {
    overflow: visible;
  }

  .graph-section {
    margin: 1rem 0 0 0;
    padding: 0;
    border-radius: 0;
    width: 100%;
  }
  
  /* Onglets plus compacts sur mobile - pleine largeur */
  .graph-tabs-wrapper {
    margin: 0.5rem 0 0.75rem 0;
    width: 100vw;
    margin-left: calc(-50vw + 50%);
  }
  
  .graph-tabs-container.top-tabs {
    border-radius: 0;
    border-left: none;
    border-right: none;
  }
  
  .tabs-nav-btn {
    width: 28px;
    min-width: 28px;
    font-size: 1.2rem;
  }
  
  .graph-tabs {
    padding: 0;
  }
  
  .graph-tab {
    padding: 0.5rem 0.4rem;
    font-size: 0.7rem;
  }
  
  /* Contenu des onglets */
  .graph-tab-content-top {
    border-radius: 0;
    border-left: none;
    border-right: none;
    padding: 0.75rem;
    width: 100vw;
    margin-left: calc(-50vw + 50%);
  }
  
  .tab-panel {
    padding: 0.5rem;
  }
  
  .panel-title {
    font-size: 0.95rem;
  }
  
  .bounds-row {
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .bound-input label {
    font-size: 0.8rem;
  }
  
  .bound-field {
    font-size: 0.85rem;
    padding: 0.4rem 0.6rem;
  }
  
  /* Liste des fonctions sur mobile */
  .functions-list {
    gap: 0.375rem;
  }
  
  .function-item {
    padding: 0.5rem;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  .function-expression {
    font-size: 0.85rem;
    max-width: calc(100% - 80px);
    overflow-x: auto;
  }
  
  /* Formes et analyse */
  .shapes-list, .shape-item {
    gap: 0.375rem;
  }
  
  .shape-section, .calc-section {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
  }
  
  .shape-title {
    font-size: 0.9rem;
  }
  
  /* Options d'affichage */
  .display-options {
    gap: 0.5rem;
  }
  
  .checkbox-label {
    font-size: 0.85rem;
  }
  
  /* Résultats d'analyse */
  .results-section {
    padding: 0.75rem;
  }
  
  .results-title {
    font-size: 0.85rem;
  }
  
  .result-item {
    font-size: 0.8rem;
    padding: 0.375rem;
  }
}

/* Extra petit écran - onglets encore plus compacts */
@media (max-width: 420px) {
  .tabs-nav-btn {
    width: 24px;
    min-width: 24px;
    font-size: 1rem;
  }
  
  .graph-tab {
    padding: 0.4rem 0.3rem;
    font-size: 0.6rem;
  }
}

/* Transition animation pour le clavier */
.keyboard-slide-enter-active,
.keyboard-slide-leave-active {
  transition: all 0.3s ease;
}

.keyboard-slide-enter-from,
.keyboard-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style> 
