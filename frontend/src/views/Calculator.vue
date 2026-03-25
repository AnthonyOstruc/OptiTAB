<template>
  <component :is="layoutComponent" v-on="layoutListeners">
    <section class="calc">
      <h2 class="title"><CalculatorIcon class="title-icon"/> Outil de Calcul Scientifique</h2>

      <!-- Système d'onglets pour le graphique (mobile uniquement, affiché au-dessus) -->
      <div v-if="selectedOperation === 'graph'" class="graph-tabs-wrapper mobile-only-tabs">
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
              <h4 class="panel-title">Éléments tracés</h4>
              <div v-if="graphFunctions.length > 0" class="functions-list">
                <div v-for="(func, index) in graphFunctions" :key="index" class="function-item function-item-2rows">
                  <div class="function-item-main">
                    <input 
                      type="color" 
                      :value="func.color" 
                      @input="changeColor(index, $event.target.value)"
                      class="function-color-picker"
                      title="Changer la couleur"
                    />
                    <span class="function-name">
                      <template v-if="editingFunctionNameIndex === index">
                        <input
                          :ref="el => functionNameInputRefs[index] = el"
                          v-model="func.name"
                          type="text"
                          inputmode="text"
                          class="function-name-input"
                          maxlength="30"
                          placeholder="f, f', C_f, \alpha..."
                          title="Nom (LaTeX supporté : f', C_f, \\alpha...)"
                          @blur="finishFunctionNameEdit(index)"
                          @keydown.enter.prevent="finishFunctionNameEdit(index)"
                          @keydown.esc.prevent="cancelFunctionNameEdit"
                        />
                        <span class="function-name-suffix">(x) =</span>
                      </template>
                      <template v-else>
                        <span class="function-name-label" :ref="el => functionNameLabelRefs[index] = el" @click="startFunctionNameEdit(index)" title="Cliquer pour renommer"></span>
                        <span class="function-name-suffix">(x) =</span>
                      </template>
                    </span>
                    <span class="function-expression" :ref="el => functionExpressionRefs[index] = el" @click="editFunction(index)" style="cursor: pointer;" title="Cliquer pour modifier"></span>
                    <button @click="removeFunction(index)" class="remove-function-btn">×</button>
                  </div>
                  <div class="function-item-toggles">
                    <select :value="func.lineDash || 'solid'" @change="func.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                      <option value="solid">───</option>
                      <option value="dot">·····</option>
                      <option value="dash">- - -</option>
                      <option value="dashdot">-·-·</option>
                      <option value="longdash">— —</option>
                    </select>
                    <select :value="func.lineWidth || 2" @change="func.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                    </select>
                    <button @click="func.showInLegend = func.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: func.showInLegend !== false }]" :title="func.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                    <button @click="func.showName = func.showName === false ? true : false; plotAllFunctions()" :class="['point-toggle-btn', { active: func.showName !== false }]" :title="func.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                  </div>
                </div>
              </div>

              <!-- Liste des points créés -->
              <div v-if="points.length > 0" class="traced-shapes-section">
                <h5 class="traced-shapes-title">Points</h5>
                <div class="shapes-list">
                  <div v-for="(point, index) in points" :key="'mob-fpt-' + index" class="shape-item shape-item-with-toggles">
                    <div class="shape-item-main">
                      <input type="color" :value="point.color" @input="changeShapeColor('point', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                      <template v-if="isEditingShape('point', index)">
                        <input v-model="point.name" type="text" :class="'shape-name-input shape-name-editing-point-' + index" maxlength="50" placeholder="P" @blur="finishShapeNameEdit('point', index)" @keydown.enter.prevent="finishShapeNameEdit('point', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('point', index)" title="Cliquer pour renommer">{{ point.name }}</span>
                      </template>
                      <span class="shape-item-coords">({{ point.x }}, {{ point.y }})</span>
                      <button @click="removePoint(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="shape-item-toggles">
                      <button @click="point.showName = !point.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showName !== false }]" :title="point.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                      <button @click="point.showCoords = !point.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showCoords !== false }]" :title="point.showCoords !== false ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                      <button @click="cyclePointLabelFormat(point); plotAllFunctions()" :class="['point-toggle-btn', { active: normalizePointLabelFormat(point.labelFormat) !== 'default' }]" :title="getPointLabelFormatTitle(point.labelFormat)">{{ getPointLabelFormatChip(point.labelFormat) }}</button>
                      <button @click="point.showProjections = !point.showProjections; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showProjections === true }]" :title="point.showProjections === true ? 'Masquer les pointillés sur les axes' : 'Afficher les pointillés sur les axes'">Proj</button>
                      <button @click="point.showInLegend = point.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: point.showInLegend !== false }]" :title="point.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                    </div>
                  </div>
                </div>
                <div v-if="points.length >= 2" class="connect-points-row">
                  <label class="connect-points-toggle">
                    <input type="checkbox" v-model="connectPoints" />
                    <span>Relier les points</span>
                  </label>
                  <input v-if="connectPoints" type="color" v-model="connectPointsColor" class="function-color-picker" title="Couleur de la liaison" />
                </div>
              </div>

              <!-- Liste des segments/vecteurs créés -->
              <div v-if="segments.length > 0" class="traced-shapes-section">
                <h5 class="traced-shapes-title">Segments / Vecteurs</h5>
                <div class="shapes-list">
                  <div v-for="(segment, index) in segments" :key="'mob-fseg-' + index" class="shape-item shape-item-with-toggles">
                    <div class="shape-item-main">
                      <input type="color" :value="segment.color" @input="changeShapeColor('segment', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                      <template v-if="isEditingShape('segment', index)">
                        <input v-model="segment.name" type="text" :class="'shape-name-input shape-name-editing-segment-' + index" maxlength="50" placeholder="S" @blur="finishShapeNameEdit('segment', index)" @keydown.enter.prevent="finishShapeNameEdit('segment', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('segment', index)" title="Cliquer pour renommer">{{ segment.name || (segment.isVector ? 'V' : 'S') + (index + 1) }}</span>
                      </template>
                      <span class="shape-item-coords">{{ segment.isVector ? '→' : '—' }} ({{ segment.x1 }},{{ segment.y1 }})→({{ segment.x2 }},{{ segment.y2 }})</span>
                      <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="shape-item-toggles">
                      <button @click="segment.showName = !segment.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showName === true }]" :title="segment.showName === true ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                      <button @click="segment.showCoords = !segment.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showCoords === true }]" :title="segment.showCoords === true ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                      <button @click="segment.showInLegend = segment.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: segment.showInLegend !== false }]" :title="segment.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                      <select :value="segment.lineDash || 'solid'" @change="segment.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                        <option value="solid">───</option>
                        <option value="dot">·····</option>
                        <option value="dash">- - -</option>
                        <option value="dashdot">-·-·</option>
                        <option value="longdash">— —</option>
                      </select>
                      <select :value="segment.lineWidth || 3" @change="segment.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Liste des cercles créés -->
              <div v-if="circles.length > 0" class="traced-shapes-section">
                <h5 class="traced-shapes-title">Cercles</h5>
                <div class="shapes-list">
                  <div v-for="(circle, index) in circles" :key="'mob-fcir-' + index" class="shape-item shape-item-with-toggles">
                    <div class="shape-item-main">
                      <input type="color" :value="circle.color" @input="changeShapeColor('circle', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                      <template v-if="isEditingShape('circle', index)">
                        <input v-model="circle.name" type="text" :class="'shape-name-input shape-name-editing-circle-' + index" maxlength="50" placeholder="C" @blur="finishShapeNameEdit('circle', index)" @keydown.enter.prevent="finishShapeNameEdit('circle', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('circle', index)" title="Cliquer pour renommer">{{ circle.name || 'C' + (index + 1) }}</span>
                      </template>
                      <span class="shape-item-coords">({{ circle.h }}, {{ circle.k }}) r={{ circle.r }}</span>
                      <button @click="removeCircle(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="shape-item-toggles">
                      <button @click="circle.showName = !circle.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: circle.showName !== false }]" :title="circle.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                      <button @click="circle.showInLegend = circle.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: circle.showInLegend !== false }]" :title="circle.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                      <select :value="circle.lineDash || 'solid'" @change="circle.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                        <option value="solid">───</option>
                        <option value="dot">·····</option>
                        <option value="dash">- - -</option>
                        <option value="dashdot">-·-·</option>
                        <option value="longdash">— —</option>
                      </select>
                      <select :value="circle.lineWidth || 2" @change="circle.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Liste des textes créés -->
              <div v-if="textAnnotations.length > 0" class="traced-shapes-section">
                <h5 class="traced-shapes-title">Textes</h5>
                <div class="shapes-list">
                  <div v-for="(ta, index) in textAnnotations" :key="'mob-ftxt-' + index" class="shape-item">
                    <input type="color" :value="ta.color" @input="changeShapeColor('text', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                    <template v-if="isEditingShape('text', index)">
                      <input v-model="ta.content" type="text" :class="'shape-name-input shape-name-editing-text-' + index" maxlength="50" placeholder="Texte" @blur="finishShapeNameEdit('text', index)" @keydown.enter.prevent="finishShapeNameEdit('text', index)" @keydown.esc.prevent="cancelShapeNameEdit" style="flex: 1;" />
                    </template>
                    <template v-else>
                      <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('text', index)" title="Cliquer pour modifier" style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ ta.content }}</span>
                    </template>
                    <button @click="removeTextAnnotation(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>

              <!-- Liste des intersections -->
              <div v-if="intersectionPoints.length > 0" class="traced-shapes-section">
                <h5 class="traced-shapes-title">Intersections</h5>
                <div class="shapes-list">
                  <div v-for="(ipt, index) in intersectionPoints" :key="'mob-fint-' + index" class="shape-item">
                    <input type="color" :value="ipt.color || '#dc2626'" @input="changeShapeColor('intersection', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                    <template v-if="isEditingShape('intersection', index)">
                      <input v-model="ipt.name" type="text" :class="'shape-name-input shape-name-editing-intersection-' + index" maxlength="20" :placeholder="ipt.defaultName" @blur="finishShapeNameEdit('intersection', index)" @keydown.enter.prevent="finishShapeNameEdit('intersection', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                    </template>
                    <template v-else>
                      <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('intersection', index)" title="Cliquer pour renommer">{{ ipt.name || ipt.defaultName }}</span>
                    </template>
                    <span class="shape-item-coords">({{ ipt.x.toFixed(2) }}, {{ ipt.y.toFixed(2) }})</span>
                    <button @click="removeIntersection(index)" class="remove-function-btn">×</button>
                  </div>
                </div>
              </div>

              <div v-if="graphFunctions.length === 0 && points.length === 0 && segments.length === 0 && circles.length === 0 && textAnnotations.length === 0 && intersectionPoints.length === 0" class="no-content">
                Aucun élément tracé.
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
                  <input type="checkbox" v-model="showCenterAxesOnly" />
                  Axes centraux seulement (0,0)
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showClickProjections" />
                  Projections pointillees au clic (x,y)
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="snapToGrid" />
                  Accrocher aux intersections de la grille
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showCurveLabels" />
                  Afficher les noms des courbes
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showPointLabels" />
                  Afficher les labels des points
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showLabelArrows" />
                  Flèches sur les labels
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showLabelBorders" />
                  Encadrement des labels
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showLegend" />
                  Afficher la légende
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="allowPan" />
                  Déplacer le graphique (clic + glisser)
                </label>
              </div>
              <div class="bounds-row">
                <div class="bound-input">
                  <label>Epaisseur des axes :</label>
                  <input v-model.number="axisLineWidth" type="number" min="1" max="10" step="0.5" class="bound-field" />
                </div>
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
                <div v-for="(point, index) in intersectionPoints" :key="index" class="result-item" style="display: flex; align-items: center; gap: 6px;">
                  <input 
                    v-model="point.name" 
                    type="text" 
                    maxlength="15" 
                    @change="renameIntersection(index, point.name); plotAllFunctions()"
                    style="width: 80px; padding: 2px 4px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.85rem;"
                    :placeholder="point.defaultName"
                  />
                  <span>: ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})</span>
                </div>
              </div>
              
              <div v-if="showRoots && rootsPoints.length > 0" class="results-section">
                <h5 class="results-title">Racines :</h5>
                <div v-for="(point, index) in rootsPoints" :key="index" class="result-item" style="display: flex; align-items: center; gap: 6px;">
                  <span>{{ getFunctionDisplayNameByOneBasedIndex(point.funcIndex) }} : x = {{ point.x.toFixed(3) }}</span>
                </div>
              </div>
              
              <div v-if="showAxisIntersections && axisIntersectionPoints.length > 0" class="results-section">
                <h5 class="results-title">Intersections avec les axes :</h5>
                <div v-for="(point, index) in axisIntersectionPoints" :key="index" class="result-item" style="display: flex; align-items: center; gap: 6px;">
                  <input 
                    v-model="point.name" 
                    type="text" 
                    maxlength="15" 
                    @change="renameAxisIntersection(index, point.name); plotAllFunctions()"
                    style="width: 80px; padding: 2px 4px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.85rem;"
                    :placeholder="point.defaultName"
                  />
                  <span>: ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})</span>
                </div>
              </div>
              
              <!-- Résolution d'inéquations -->
              <div class="calc-section" style="margin-top: 0.75rem;">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="showInequality" />
                  Résoudre des inéquations
                </label>
                <div v-if="showInequality && inequalityItems.length >= 2" class="calc-controls">
                  <div v-for="(ineq, ineqIdx) in inequalities" :key="'mob-ineq-' + ineqIdx" style="margin-bottom: 0.75rem; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 8px; position: relative;" :style="{ borderLeftColor: ineq.color.replace('0.15', '0.6'), borderLeftWidth: '3px' }">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                      <div style="display: flex; align-items: center; gap: 0.4rem;">
                        <input type="color" :value="rgbaToHex(ineq.color)" @input="updateInequalityColor(ineqIdx, $event.target.value)" style="width: 22px; height: 22px; border: none; padding: 0; cursor: pointer; border-radius: 4px; background: transparent;" title="Couleur de la zone" />
                        <span style="font-size: 0.8rem; font-weight: 600; color: #374151;">Inéquation {{ ineqIdx + 1 }}</span>
                      </div>
                      <button v-if="inequalities.length > 1" @click="removeInequality(ineqIdx)" class="remove-function-btn" title="Supprimer cette inéquation" style="font-size: 0.9rem;">×</button>
                    </div>
                    <div class="bounds-row">
                      <div class="bound-input">
                        <label>Él. 1 :</label>
                        <select v-model.number="ineq.func1Index" class="bound-field">
                          <option v-for="(item, index) in inequalityItems" :key="'mob-iq1-' + ineqIdx + '-' + item.key" :value="index">
                            {{ item.label }}
                          </option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Signe :</label>
                        <select v-model="ineq.operator" class="bound-field">
                          <option value="<">&lt;</option>
                          <option value=">">&gt;</option>
                          <option value="<=">≤</option>
                          <option value=">=">≥</option>
                          <option value="=">=</option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Él. 2 :</label>
                        <select v-model.number="ineq.func2Index" class="bound-field">
                          <option v-for="(item, index) in inequalityItems" :key="'mob-iq2-' + ineqIdx + '-' + item.key" :value="index">
                            {{ item.label }}
                          </option>
                        </select>
                      </div>
                    </div>
                    <div v-if="ineq.result" class="result-info inequality-result" style="margin-top: 0.3rem;">
                      <strong>Solution :</strong> <span v-html="ineq.result.display"></span>
                    </div>
                  </div>
                  <button @click="addInequality()" class="btn-secondary" style="width: 100%; padding: 0.4rem; font-size: 0.85rem; border-radius: 6px; border: 1px dashed #94a3b8; background: transparent; color: #64748b; cursor: pointer;">
                    + Ajouter une inéquation
                  </button>
                </div>
                <div v-if="showInequality && inequalityItems.length < 2" class="result-info" style="color: #ef4444;">
                  Il faut au moins 2 éléments tracés (fonctions ou segments).
                </div>
              </div>

              <!-- Angles entre segments -->
              <div class="calc-section" style="margin-top: 0.75rem;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.3rem;">
                  <strong style="font-size: 0.9rem;">📐 Angles</strong>
                  <button v-if="segments.length >= 2" @click="addAngleMeasure" class="add-function-btn" style="font-size: 0.8rem; padding: 2px 8px;">+ Angle</button>
                </div>
                <div v-if="segments.length < 2" class="result-info" style="color: #ef4444; font-size: 0.85rem;">
                  Il faut au moins 2 segments tracés.
                </div>
                <div v-for="(angle, aIdx) in angleMeasures" :key="'angle-' + aIdx" style="border-left: 3px solid; padding-left: 0.5rem; margin-bottom: 0.5rem; border-color: currentColor;" :style="{ color: angle.color }">
                  <div style="display: flex; align-items: center; gap: 0.3rem; margin-bottom: 0.25rem;">
                    <input type="color" :value="angle.color" @input="angle.color = $event.target.value; plotAllFunctions()" class="function-color-picker" title="Couleur" />
                    <span style="font-size: 0.85rem; color: var(--text); flex: 1;">Angle {{ aIdx + 1 }}</span>
                    <button @click="removeAngleMeasure(aIdx)" class="remove-function-btn" title="Supprimer">×</button>
                  </div>
                  <div class="bounds-row" style="color: var(--text);">
                    <div class="bound-input">
                      <label>Seg 1 :</label>
                      <select v-model.number="angle.seg1Index" class="bound-field">
                        <option v-for="(seg, si) in segments" :key="'a'+aIdx+'-s1-'+si" :value="si">{{ seg.name || (seg.isVector ? 'V' : 'S') + (si+1) }}</option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Seg 2 :</label>
                      <select v-model.number="angle.seg2Index" class="bound-field">
                        <option v-for="(seg, si) in segments" :key="'a'+aIdx+'-s2-'+si" :value="si">{{ seg.name || (seg.isVector ? 'V' : 'S') + (si+1) }}</option>
                      </select>
                    </div>
                  </div>
                  <div style="display: flex; align-items: center; gap: 0.4rem; margin-top: 0.25rem; flex-wrap: wrap; color: var(--text);">
                    <label class="checkbox-label" style="margin: 0; font-size: 0.8rem;">
                      <input type="checkbox" v-model="angle.showArc" /> Arc
                    </label>
                    <div class="bound-input" style="flex: 0 0 auto;">
                      <label style="font-size: 0.8rem;">Texte :</label>
                      <input v-model="angle.customText" class="bound-field" placeholder="auto" maxlength="30" style="max-width: 80px; font-size: 0.8rem;" />
                    </div>
                    <div class="bound-input" style="flex: 0 0 auto;">
                      <label style="font-size: 0.8rem;">Manuel ° :</label>
                      <input v-model="angle.manualDegrees" class="bound-field" type="number" step="0.1" placeholder="auto" style="max-width: 70px; font-size: 0.8rem;" />
                    </div>
                  </div>
                  <div v-if="angle.result" class="result-info" style="margin-top: 0.3rem; color: var(--text);">
                    <strong>{{ angle.manualDegrees !== '' && !isNaN(parseFloat(angle.manualDegrees)) ? parseFloat(angle.manualDegrees) : angle.result.degrees }}°</strong> ({{ angle.result.radians }} rad)
                    <span v-if="!angle.result.hasCommonVertex" style="display: block; font-size: 0.8rem; color: #f59e0b;">⚠ Pas de sommet commun</span>
                  </div>
                  <div v-else-if="angle.seg1Index === angle.seg2Index" class="result-info" style="color: #ef4444; font-size: 0.8rem;">Choisissez 2 segments différents.</div>
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
                          {{ functionDisplayNames[index] }}
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
                          {{ functionDisplayNames[index] }}
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Fonction 2 :</label>
                      <select v-model.number="areaCurve2Index" class="bound-field">
                        <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                          {{ functionDisplayNames[index] }}
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
                          {{ functionDisplayNames[index] }}
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
                    <label>Nom :</label>
                    <input v-model="pointName" type="text" class="bound-field" placeholder="A" maxlength="10" style="width: 60px;" />
                  </div>
                  <div class="bound-input">
                    <label>x :</label>
                    <input v-model="pointX" type="text" class="bound-field" placeholder="ex: e" />
                  </div>
                  <div class="bound-input">
                    <label>y :</label>
                    <input v-model="pointY" type="text" class="bound-field" placeholder="ex: 1" />
                  </div>
                </div>
                <button @click="addPoint" class="action-btn">Ajouter le point</button>
                
                <div style="margin-top: 8px;">
                  <label style="font-size: 0.8rem; color: #94a3b8;">Plusieurs points :</label>
                  <input v-model="pointsInput" type="text" class="bound-field" placeholder="A(e,1),B(3,4),C(pi,2)" style="width: 100%; margin-top: 4px;" @keyup.enter="addMultiplePoints" />
                  <button @click="addMultiplePoints" class="action-btn" style="margin-top: 4px;">Ajouter les points</button>
                </div>
                
                <div v-if="points.length > 0" class="shapes-list">
                  <div v-for="(point, index) in points" :key="'point-' + index" class="shape-item">
                    <span class="function-color" :style="{ backgroundColor: point.color }"></span>
                    <input 
                      v-model="point.name" 
                      type="text" 
                      class="point-name-input" 
                      maxlength="10" 
                      @change="plotAllFunctions()"
                      style="width: 50px; padding: 2px 4px; border: 1px solid #555; border-radius: 4px; background: #2a2a3e; color: white; font-size: 0.85rem;"
                    />
                    <span>({{ point.x }}, {{ point.y }})</span>
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
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Point 2 :</label>
                      <select v-model.number="segmentPoint2Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="index" :value="index">
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
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
                <button @click="addSegment" class="action-btn">Ajouter le {{ segmentIsVector ? 'vecteur' : 'segment' }}</button>
                <label class="checkbox-label" style="margin-top: 0.5rem;">
                  <input type="checkbox" v-model="segmentIsVector" />
                  Dessiner un vecteur (avec flèche)
                </label>
                
                <div v-if="segments.length > 0" class="shapes-list">
                  <div v-for="(segment, index) in segments" :key="'segment-' + index" class="shape-item shape-item-with-toggles">
                    <div class="shape-item-main">
                      <span class="function-color" :style="{ backgroundColor: segment.color }"></span>
                      <template v-if="isEditingShape('segment', index)">
                        <input v-model="segment.name" type="text" :class="'shape-name-input shape-name-editing-segment-' + index" maxlength="50" placeholder="S" @blur="finishShapeNameEdit('segment', index)" @keydown.enter.prevent="finishShapeNameEdit('segment', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('segment', index)" title="Cliquer pour renommer">{{ segment.name || (segment.isVector ? 'V' : 'S') + (index + 1) }}</span>
                      </template>
                      <span class="shape-item-coords">{{ segment.isVector ? '→' : '—' }} ({{ segment.x1 }},{{ segment.y1 }})→({{ segment.x2 }},{{ segment.y2 }})</span>
                      <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="shape-item-toggles">
                      <button @click="segment.showName = !segment.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showName === true }]" :title="segment.showName === true ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                      <button @click="segment.showCoords = !segment.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showCoords === true }]" :title="segment.showCoords === true ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                      <button @click="segment.showInLegend = segment.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: segment.showInLegend !== false }]" :title="segment.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                      <select :value="segment.lineDash || 'solid'" @change="segment.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                        <option value="solid">───</option>
                        <option value="dot">·····</option>
                        <option value="dash">- - -</option>
                        <option value="dashdot">-·-·</option>
                        <option value="longdash">— —</option>
                      </select>
                      <select :value="segment.lineWidth || 3" @change="segment.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Droites -->
              <div class="shape-section">
                <h5 class="shape-title">Tracer une droite</h5>
                <div class="bounds-row">
                  <label class="radio-label"><input type="radio" v-model="droiteMode" value="2points" /> 2 points</label>
                  <label class="radio-label"><input type="radio" v-model="droiteMode" value="pointSlope" /> Point + pente</label>
                  <label class="radio-label"><input type="radio" v-model="droiteMode" value="pointVector" /> Point + vecteur</label>
                </div>

                <template v-if="droiteMode === '2points'">
                  <div v-if="points.length >= 2" class="bounds-row">
                    <div class="bound-input">
                      <label>Point 1 :</label>
                      <select v-model.number="droitePoint1Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="'fl-dp1-' + index" :value="index">
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Point 2 :</label>
                      <select v-model.number="droitePoint2Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="'fl-dp2-' + index" :value="index">
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                  </div>
                  <p v-else class="helper-text">Créez au moins 2 points d'abord.</p>
                </template>

                <template v-if="droiteMode === 'pointSlope'">
                  <div v-if="points.length >= 1" class="bounds-row">
                    <div class="bound-input">
                      <label>Point :</label>
                      <select v-model.number="droitePointIndex" class="bound-field">
                        <option v-for="(point, index) in points" :key="'fl-dps-' + index" :value="index">
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Pente m :</label>
                      <input v-model.number="droiteSlope" type="number" step="0.5" class="bound-field" />
                    </div>
                  </div>
                  <p v-else class="helper-text">Créez au moins 1 point d'abord.</p>
                </template>

                <template v-if="droiteMode === 'pointVector'">
                  <div v-if="points.length >= 1" class="bounds-row">
                    <div class="bound-input">
                      <label>Point :</label>
                      <select v-model.number="droitePointIndex" class="bound-field">
                        <option v-for="(point, index) in points" :key="'fl-dpv-' + index" :value="index">
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Vec x :</label>
                      <input v-model.number="droiteVecX" type="number" step="0.5" class="bound-field" />
                    </div>
                    <div class="bound-input">
                      <label>Vec y :</label>
                      <input v-model.number="droiteVecY" type="number" step="0.5" class="bound-field" />
                    </div>
                  </div>
                  <p v-else class="helper-text">Créez au moins 1 point d'abord.</p>
                </template>

                <button @click="addDroite" class="action-btn" :disabled="(droiteMode === '2points' && points.length < 2) || ((droiteMode === 'pointSlope' || droiteMode === 'pointVector') && points.length < 1)">Tracer la droite</button>
                <p class="helper-text" style="margin-top: 4px;">Ou saisissez : <code>(AB)</code>, <code>d(A,m=2)</code>, <code>d(A,u(1,2))</code></p>
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
                  <div v-for="(circle, index) in circles" :key="'circle-' + index" class="shape-item shape-item-with-toggles">
                    <div class="shape-item-main">
                      <span class="function-color" :style="{ backgroundColor: circle.color }"></span>
                      <template v-if="isEditingShape('circle', index)">
                        <input v-model="circle.name" type="text" :class="'shape-name-input shape-name-editing-circle-' + index" maxlength="50" placeholder="C" @blur="finishShapeNameEdit('circle', index)" @keydown.enter.prevent="finishShapeNameEdit('circle', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('circle', index)" title="Cliquer pour renommer">{{ circle.name || 'C' + (index + 1) }}</span>
                      </template>
                      <span class="shape-item-coords">(h={{ circle.h }}, k={{ circle.k }}, r={{ circle.r }})</span>
                      <button @click="removeCircle(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="shape-item-toggles">
                      <button @click="circle.showName = !circle.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: circle.showName !== false }]" :title="circle.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                      <button @click="circle.showInLegend = circle.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: circle.showInLegend !== false }]" :title="circle.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                      <select :value="circle.lineDash || 'solid'" @change="circle.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                        <option value="solid">───</option>
                        <option value="dot">·····</option>
                        <option value="dash">- - -</option>
                        <option value="dashdot">-·-·</option>
                        <option value="longdash">— —</option>
                      </select>
                      <select :value="circle.lineWidth || 2" @change="circle.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Textes personnalisés -->
              <div class="shape-section">
                <h5 class="shape-title">✏️ Ajouter un texte</h5>
                <p class="helper-text">Utilisez <code>$...$</code> pour du LaTeX. Ex : <code>$\frac{a}{b}$</code>, <code>$\int_0^1 x\,dx$</code></p>
                <div class="bounds-row">
                  <div class="bound-input" style="flex: 2;">
                    <label>Texte :</label>
                    <input v-model="newTextContent" type="text" class="bound-field" placeholder="$\alpha + \beta = \gamma$" />
                  </div>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>x :</label>
                    <input v-model.number="newTextX" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>y :</label>
                    <input v-model.number="newTextY" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>Taille :</label>
                    <input v-model.number="newTextSize" type="number" min="8" max="120" step="1" class="bound-field" style="width: 70px;" />
                  </div>
                  <div class="bound-input">
                    <label>Couleur :</label>
                    <input v-model="newTextColor" type="color" class="bound-field" style="width: 40px; padding: 2px; height: 32px;" />
                  </div>
                  <div class="bound-input">
                    <label>Style :</label>
                    <label class="checkbox-label" style="margin: 0; gap: 0.35rem;">
                      <input v-model="newTextBold" type="checkbox" />
                      <span>Gras</span>
                    </label>
                  </div>
                </div>
                <button @click="addTextAnnotation" class="action-btn">Ajouter le texte</button>
                
                <div v-if="textAnnotations.length > 0" class="shapes-list">
                  <div v-for="(ta, index) in textAnnotations" :key="'text-' + index" class="shape-item">
                    <span class="function-color" :style="{ backgroundColor: ta.color }"></span>
                    <span style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ ta.content }}</span>
                    <span style="opacity: 0.6; font-size: 0.8rem;">({{ ta.x }}, {{ ta.y }})</span>
                    <button @click="removeTextAnnotation(index)" class="remove-function-btn">×</button>
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
              virtual-keyboard-mode="off"
              @focus="handleMathFieldFocus"
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
                  <input type="checkbox" v-model="showCenterAxesOnly" />
                  Axes centraux seulement (0,0)
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showClickProjections" />
                  Projections pointillees au clic (x,y)
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="snapToGrid" />
                  Accrocher aux intersections de la grille
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showCurveLabels" />
                  Afficher les noms des courbes
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showPointLabels" />
                  Afficher les labels des points
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showLabelArrows" />
                  Flèches sur les labels
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showLabelBorders" />
                  Encadrement des labels
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="showLegend" />
                  Afficher la légende
                </label>
                <label class="integral-type-label">
                  <input type="checkbox" v-model="allowPan" />
                  Déplacer le graphique (clic + glisser)
                </label>
              </div>
              <div class="bounds-row">
                <div class="bound-input">
                  <label>Epaisseur des axes :</label>
                  <input v-model.number="axisLineWidth" type="number" min="1" max="10" step="0.5" class="bound-field" />
                </div>
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
                <!-- Angles entre segments -->
                <div style="margin-top: 0.5rem;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.3rem;">
                    <strong style="font-size: 0.85rem;">📐 Angles</strong>
                    <button v-if="segments.length >= 2" @click="addAngleMeasure" class="add-function-btn" style="font-size: 0.75rem; padding: 1px 6px;">+ Angle</button>
                  </div>
                  <div v-if="segments.length < 2" style="color: #ef4444; font-size: 0.8rem; padding-left: 0.3rem;">Il faut au moins 2 segments.</div>
                  <div v-for="(angle, aIdx) in angleMeasures" :key="'flt-angle-' + aIdx" style="border-left: 3px solid; padding-left: 0.4rem; margin-bottom: 0.4rem;" :style="{ borderColor: angle.color }">
                    <div style="display: flex; align-items: center; gap: 0.2rem; margin-bottom: 0.2rem;">
                      <input type="color" :value="angle.color" @input="angle.color = $event.target.value; plotAllFunctions()" class="function-color-picker" title="Couleur" />
                      <span style="font-size: 0.8rem; flex: 1;">Angle {{ aIdx + 1 }}</span>
                      <button @click="removeAngleMeasure(aIdx)" class="remove-function-btn" title="Supprimer">×</button>
                    </div>
                    <div class="bounds-row">
                      <div class="bound-input">
                        <label>Seg 1 :</label>
                        <select v-model.number="angle.seg1Index" class="bound-field">
                          <option v-for="(seg, si) in segments" :key="'flt-a'+aIdx+'-s1-'+si" :value="si">{{ seg.name || (seg.isVector ? 'V' : 'S') + (si+1) }}</option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Seg 2 :</label>
                        <select v-model.number="angle.seg2Index" class="bound-field">
                          <option v-for="(seg, si) in segments" :key="'flt-a'+aIdx+'-s2-'+si" :value="si">{{ seg.name || (seg.isVector ? 'V' : 'S') + (si+1) }}</option>
                        </select>
                      </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.3rem; margin-top: 0.2rem; flex-wrap: wrap;">
                      <label class="intersection-checkbox-label" style="margin: 0; font-size: 0.8rem;">
                        <input type="checkbox" v-model="angle.showArc" /> Arc
                      </label>
                      <div class="bound-input" style="flex: 0 0 auto;">
                        <label style="font-size: 0.75rem;">Texte :</label>
                        <input v-model="angle.customText" class="bound-field" placeholder="auto" maxlength="30" style="max-width: 70px; font-size: 0.75rem;" />
                      </div>
                      <div class="bound-input" style="flex: 0 0 auto;">
                        <label style="font-size: 0.75rem;">Manuel ° :</label>
                        <input v-model="angle.manualDegrees" class="bound-field" type="number" step="0.1" placeholder="auto" style="max-width: 60px; font-size: 0.75rem;" />
                      </div>
                    </div>
                    <div v-if="angle.result" class="integral-result" style="margin-top: 0.2rem;">
                      <strong>{{ angle.manualDegrees !== '' && !isNaN(parseFloat(angle.manualDegrees)) ? parseFloat(angle.manualDegrees) : angle.result.degrees }}°</strong> ({{ angle.result.radians }} rad)
                      <span v-if="!angle.result.hasCommonVertex" style="display: block; font-size: 0.7rem; color: #f59e0b;">⚠ Pas de sommet commun</span>
                    </div>
                  </div>
                </div>
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
                        {{ functionDisplayNames[index] }} - {{ func.expression }}
                      </option>
                    </select>
                  </div>
                  
                  <div class="integral-function-select">
                    <label for="integral-func2">Fonction 2 (optionnel) :</label>
                    <select id="integral-func2" v-model="integralFunc2Index" class="bound-field">
                      <option value="-1">Aucune (axe X)</option>
                      <option v-for="(func, index) in graphFunctions" :key="index" :value="index">
                        {{ functionDisplayNames[index] }} - {{ func.expression }}
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
                        {{ functionDisplayNames[graphFunctions.indexOf(func)] }} - {{ func.expression }}
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
                      <label for="point-name">Nom :</label>
                      <input 
                        id="point-name"
                        v-model="pointName" 
                        type="text" 
                        class="bound-field"
                        placeholder="A"
                        maxlength="10"
                        style="width: 60px;"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="point-x">x :</label>
                      <input 
                        id="point-x"
                        v-model="pointX" 
                        type="text" 
                        class="bound-field"
                        placeholder="ex: e"
                      />
                    </div>
                    <div class="bound-input">
                      <label for="point-y">y :</label>
                      <input 
                        id="point-y"
                        v-model="pointY" 
                        type="text" 
                        class="bound-field"
                        placeholder="ex: 1"
                      />
                    </div>
                  </div>
                  
                  <button @click="addPoint" class="calculate-integral-btn" style="background: #10b981;">
                    Ajouter le point
                  </button>
                  
                  <div style="margin-top: 8px;">
                    <label style="font-size: 0.8rem; color: #94a3b8;">Plusieurs points :</label>
                    <input v-model="pointsInput" type="text" class="bound-field" placeholder="A(e,1),B(3,4),C(pi,2)" style="width: 100%; margin-top: 4px;" @keyup.enter="addMultiplePoints" />
                    <button @click="addMultiplePoints" class="calculate-integral-btn" style="background: #10b981; margin-top: 4px;">
                      Ajouter les points
                    </button>
                  </div>
                </div>
                
                <div v-if="points.length > 0" class="points-list">
                  <h5 class="functions-title">Points tracés :</h5>
                  <div v-for="(point, index) in points" :key="'point-' + index" class="function-item function-item-with-toggles">
                    <div class="shape-item-main">
                      <span class="function-color" :style="{ backgroundColor: point.color }"></span>
                      <input 
                        v-model="point.name" 
                        type="text" 
                        class="point-name-input" 
                        maxlength="10" 
                        @change="plotAllFunctions()"
                        style="width: 50px; padding: 2px 4px; border: 1px solid #555; border-radius: 4px; background: #2a2a3e; color: white; font-size: 0.85rem;"
                      />
                      <span class="circle-label">
                        ({{ point.x }}, {{ point.y }})
                      </span>
                      <button @click="removePoint(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="shape-item-toggles">
                      <button @click="point.showName = !point.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showName !== false }]" :title="point.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                      <button @click="point.showCoords = !point.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showCoords !== false }]" :title="point.showCoords !== false ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                      <button @click="cyclePointLabelFormat(point); plotAllFunctions()" :class="['point-toggle-btn', { active: normalizePointLabelFormat(point.labelFormat) !== 'default' }]" :title="getPointLabelFormatTitle(point.labelFormat)">{{ getPointLabelFormatChip(point.labelFormat) }}</button>
                      <button @click="point.showProjections = !point.showProjections; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showProjections === true }]" :title="point.showProjections === true ? 'Masquer les pointillés sur les axes' : 'Afficher les pointillés sur les axes'">Proj</button>
                      <button @click="point.showInLegend = point.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: point.showInLegend !== false }]" :title="point.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                    </div>
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
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
                        </option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Point 2 :</label>
                      <select v-model.number="segmentPoint2Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="index" :value="index">
                          {{ point.name }} ({{ point.x }}, {{ point.y }})
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
                    Ajouter le {{ segmentIsVector ? 'vecteur' : 'segment' }}
                  </button>
                  <label class="integral-type-label" style="margin-top: 0.5rem;">
                    <input type="checkbox" v-model="segmentIsVector" />
                    Dessiner un vecteur (avec flèche)
                  </label>
                </div>
                
                <div v-if="segments.length > 0" class="segments-list">
                  <h5 class="functions-title">Segments tracés :</h5>
                  <div v-for="(segment, index) in segments" :key="'segment-' + index" class="function-item">
                    <span class="function-color" :style="{ backgroundColor: segment.color }"></span>
                    <span class="circle-label">
                      {{ segment.isVector ? '→' : '[AB]' }}{{ index + 1 }} : A({{ segment.x1 }}, {{ segment.y1 }}) → B({{ segment.x2 }}, {{ segment.y2 }})
                    </span>
                    <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                  </div>
                </div>

                <!-- Droite dans section points mobile -->
                <h5 class="functions-title" style="margin-top: 1rem;">Tracer une droite</h5>
                <div class="bounds-row">
                  <label class="radio-label"><input type="radio" v-model="droiteMode" value="2points" /> 2 pts</label>
                  <label class="radio-label"><input type="radio" v-model="droiteMode" value="pointSlope" /> Pt+pente</label>
                  <label class="radio-label"><input type="radio" v-model="droiteMode" value="pointVector" /> Pt+vec</label>
                </div>
                <template v-if="droiteMode === '2points'">
                  <div v-if="points.length >= 2" class="bounds-row">
                    <div class="bound-input">
                      <label>Pt 1 :</label>
                      <select v-model.number="droitePoint1Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="'mob-dp1-' + index" :value="index">{{ point.name }} ({{ point.x }}, {{ point.y }})</option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Pt 2 :</label>
                      <select v-model.number="droitePoint2Index" class="bound-field">
                        <option v-for="(point, index) in points" :key="'mob-dp2-' + index" :value="index">{{ point.name }} ({{ point.x }}, {{ point.y }})</option>
                      </select>
                    </div>
                  </div>
                  <p v-else class="helper-text">Créez au moins 2 points.</p>
                </template>
                <template v-if="droiteMode === 'pointSlope'">
                  <div v-if="points.length >= 1" class="bounds-row">
                    <div class="bound-input">
                      <label>Point :</label>
                      <select v-model.number="droitePointIndex" class="bound-field">
                        <option v-for="(point, index) in points" :key="'mob-dps-' + index" :value="index">{{ point.name }} ({{ point.x }}, {{ point.y }})</option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>Pente :</label>
                      <input v-model.number="droiteSlope" type="number" step="0.5" class="bound-field" />
                    </div>
                  </div>
                  <p v-else class="helper-text">Créez au moins 1 point.</p>
                </template>
                <template v-if="droiteMode === 'pointVector'">
                  <div v-if="points.length >= 1" class="bounds-row">
                    <div class="bound-input">
                      <label>Point :</label>
                      <select v-model.number="droitePointIndex" class="bound-field">
                        <option v-for="(point, index) in points" :key="'mob-dpv-' + index" :value="index">{{ point.name }} ({{ point.x }}, {{ point.y }})</option>
                      </select>
                    </div>
                    <div class="bound-input">
                      <label>dx :</label>
                      <input v-model.number="droiteVecX" type="number" step="0.5" class="bound-field" />
                    </div>
                    <div class="bound-input">
                      <label>dy :</label>
                      <input v-model.number="droiteVecY" type="number" step="0.5" class="bound-field" />
                    </div>
                  </div>
                  <p v-else class="helper-text">Créez au moins 1 point.</p>
                </template>
                <button @click="addDroite" class="action-btn" :disabled="(droiteMode === '2points' && points.length < 2) || ((droiteMode === 'pointSlope' || droiteMode === 'pointVector') && points.length < 1)">Tracer la droite</button>

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
            
            <!-- Textes personnalisés (mobile) -->
            <details v-if="activeSection === 'textAnnotations'" class="graph-controls-collapsible floating-panel" open>
              <summary class="graph-controls-summary">
                <span class="summary-icon">▼</span>
                <span class="summary-text">✏️ Ajouter du texte</span>
              </summary>
              <div class="graph-controls">
              <div class="text-annotation-section">
                <h5 class="functions-title">Ajouter un texte</h5>
                <p class="help-text">Utilisez <code>$...$</code> pour du LaTeX. Ex : <code>$\frac{a}{b}$</code></p>
                <div class="bound-input" style="margin-bottom: 0.5rem;">
                  <label>Texte :</label>
                  <input v-model="newTextContent" type="text" class="bound-field" placeholder="$\alpha + \beta$" />
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>x :</label>
                    <input v-model.number="newTextX" type="number" step="0.5" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>y :</label>
                    <input v-model.number="newTextY" type="number" step="0.5" class="bound-field" />
                  </div>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>Taille :</label>
                    <input v-model.number="newTextSize" type="number" min="8" max="120" step="1" class="bound-field" style="width: 70px;" />
                  </div>
                  <div class="bound-input">
                    <label>Couleur :</label>
                    <input v-model="newTextColor" type="color" class="bound-field" style="width: 50px; padding: 2px; height: 36px;" />
                  </div>
                  <div class="bound-input">
                    <label>Style :</label>
                    <label class="checkbox-label" style="margin: 0; gap: 0.35rem;">
                      <input v-model="newTextBold" type="checkbox" />
                      <span>Gras</span>
                    </label>
                  </div>
                </div>
                <button @click="addTextAnnotation" class="calculate-integral-btn" style="background: #1e3a8a; margin-top: 0.5rem;">
                  Ajouter le texte
                </button>
                
                <div v-if="textAnnotations.length > 0" class="circles-list" style="margin-top: 0.75rem;">
                  <h5 class="functions-title">Textes ajoutés :</h5>
                  <div v-for="(ta, index) in textAnnotations" :key="'text-' + index" class="function-item">
                    <span class="function-color" :style="{ backgroundColor: ta.color }"></span>
                    <span style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.85rem;">{{ ta.content }}</span>
                    <span style="opacity: 0.6; font-size: 0.75rem;">({{ ta.x }}, {{ ta.y }})</span>
                    <button @click="removeTextAnnotation(index)" class="remove-function-btn">×</button>
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
                <div v-for="(func, index) in graphFunctions" :key="index" class="function-item function-item-2rows">
                  <div class="function-item-main">
                    <span class="function-color" :style="{ backgroundColor: func.color }"></span>
                    <span class="function-expression" :ref="el => functionExpressionRefs[index] = el"></span>
                    <button @click="removeFunction(index)" class="remove-function-btn">×</button>
                  </div>
                  <div class="function-item-toggles">
                    <select :value="func.lineDash || 'solid'" @change="func.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                      <option value="solid">───</option>
                      <option value="dot">·····</option>
                      <option value="dash">- - -</option>
                      <option value="dashdot">-·-·</option>
                      <option value="longdash">— —</option>
                    </select>
                    <select :value="func.lineWidth || 2" @change="func.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                    </select>
                    <button @click="func.showInLegend = func.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: func.showInLegend !== false }]" :title="func.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                    <button @click="func.showName = func.showName === false ? true : false; plotAllFunctions()" :class="['point-toggle-btn', { active: func.showName !== false }]" :title="func.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                  </div>
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
                    <input 
                      v-model="point.name" 
                      type="text" 
                      maxlength="15" 
                      @change="renameIntersection(index, point.name); plotAllFunctions()"
                      class="intersection-name-input"
                      :placeholder="point.defaultName"
                      style="width: 80px; padding: 2px 4px; border: 1px solid #555; border-radius: 4px; background: #2a2a3e; color: white; font-size: 0.82rem;"
                    />
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
                      {{ getFunctionDisplayNameByOneBasedIndex(point.funcIndex) }}({{ point.x.toFixed(3) }}) = 0
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
                    <input 
                      v-model="point.name" 
                      type="text" 
                      maxlength="15" 
                      @change="renameAxisIntersection(index, point.name); plotAllFunctions()"
                      class="intersection-name-input"
                      :placeholder="point.defaultName"
                      style="width: 80px; padding: 2px 4px; border: 1px solid #555; border-radius: 4px; background: #2a2a3e; color: white; font-size: 0.82rem;"
                    />
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
                
                <!-- Carte Segments / Vecteurs -->
                <div class="option-card" @click="toggleSection('segments')">
                  <div class="card-icon">📍</div>
                  <div class="card-title">Segments</div>
                  <div class="card-description">Segments et vecteurs</div>
                </div>
                
                <!-- Carte Droites -->
                <div class="option-card" @click="toggleSection('droites')">
                  <div class="card-icon">📏</div>
                  <div class="card-title">Droites</div>
                  <div class="card-description">Tracer une droite</div>
                </div>
                
                <!-- Carte Cercles -->
                <div class="option-card" @click="toggleSection('circles')">
                  <div class="card-icon">⚫</div>
                  <div class="card-title">Cercles</div>
                  <div class="card-description">Dessiner des cercles</div>
                </div>
                
                <!-- Carte Textes -->
                <div class="option-card" @click="toggleSection('textAnnotations')">
                  <div class="card-icon">✏️</div>
                  <div class="card-title">Textes</div>
                  <div class="card-description">Ajouter du texte / LaTeX</div>
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

      <!-- Conteneur du graphique avec layout desktop side-by-side -->
      <div v-if="selectedOperation === 'graph'" class="graph-section">
        <div class="graph-layout">
          <!-- Zone principale du graphique (gauche sur desktop) -->
          <div class="graph-main-area">
            <div class="graph-header">
              <h3 class="graph-title">Graphique Interactif</h3>
              <div class="graph-actions">
                <button @click="clearGraph" class="clear-graph-btn">Effacer tout</button>
                <button @click="zoomIn" class="zoom-btn" title="Zoom avant">🔍+</button>
                <button @click="zoomOut" class="zoom-btn" title="Zoom arrière">🔍−</button>
                <button @click="resetZoom" class="reset-zoom-btn">Réinitialiser zoom</button>
                <button @click="showSidePanel = !showSidePanel" class="toggle-panel-btn desktop-only-panel" :title="showSidePanel ? 'Masquer le panneau' : 'Afficher le panneau'">
                  <span v-if="showSidePanel">◀ Masquer options</span>
                  <span v-else>▶ Afficher options</span>
                </button>
              </div>
            </div>
            
            <!-- Barre d'outils de dessin -->
            <div class="drawing-toolbar">
              <span class="drawing-toolbar-label">Dessiner :</span>
              <button 
                :class="['drawing-tool-btn', { active: drawingMode === 'point' }]"
                @click="setDrawingMode('point')"
                title="Cliquer sur le graphe pour ajouter un point"
              >
                🟢 Point
              </button>
              <button 
                :class="['drawing-tool-btn', { active: drawingMode === 'segment' }]"
                @click="setDrawingMode('segment')"
                title="2 clics pour tracer un segment"
              >
                📏 Segment
              </button>
              <button 
                :class="['drawing-tool-btn', { active: drawingMode === 'vector' }]"
                @click="setDrawingMode('vector')"
                title="2 clics pour tracer un vecteur"
              >
                ➡️ Vecteur
              </button>
              <button 
                :class="['drawing-tool-btn', { active: drawingMode === 'circle' }]"
                @click="setDrawingMode('circle')"
                title="1er clic = centre, 2ème clic = rayon"
              >
                ⭕ Cercle
              </button>
              <button 
                v-if="drawingMode !== 'none'"
                class="drawing-tool-btn cancel-btn"
                @click="setDrawingMode('none')"
                title="Désactiver le mode dessin"
              >
                ✖ Annuler
              </button>
              <span v-if="drawingMode === 'segment' || drawingMode === 'vector'" class="drawing-hint">
                {{ drawingTempPoint ? 'Cliquez le 2ème point' : 'Cliquez le 1er point' }}
              </span>
              <span v-else-if="drawingMode === 'circle'" class="drawing-hint">
                {{ drawingTempPoint ? 'Cliquez pour définir le rayon' : 'Cliquez le centre' }}
              </span>
              <span v-else-if="drawingMode === 'point'" class="drawing-hint">
                Cliquez sur le graphe
              </span>
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

          <!-- Panneau latéral avec grille de cartes (desktop uniquement) -->
          <div v-show="showSidePanel" class="graph-side-panel desktop-only-panel">
            <div class="side-panel-header">
              <h4 class="side-panel-title">Options du graphique</h4>
            </div>
            <div class="side-panel-cards">
              <button 
                v-for="tab in allGraphTabs"
                :key="'card-' + tab"
                class="side-card" 
                :class="{ active: activeGraphTab === tab }"
                @click="activeGraphTab = (activeGraphTab === tab ? '' : tab)"
              >
                <span class="side-card-icon">{{ getTabIcon(tab) }}</span>
                <span class="side-card-label">{{ getTabShortLabel(tab) }}</span>
              </button>
            </div>
            <div v-if="activeGraphTab" class="side-panel-content">
              <!-- Onglet Fonctions tracées -->
              <div v-show="activeGraphTab === 'functions'" class="tab-panel">
                <h4 class="panel-title">Éléments tracés</h4>
                <div v-if="graphFunctions.length > 0" class="functions-list">
                  <div v-for="(func, index) in graphFunctions" :key="'side-f-' + index" class="function-item function-item-2rows">
                    <div class="function-item-main">
                      <input 
                        type="color" 
                        :value="func.color" 
                        @input="changeColor(index, $event.target.value)"
                        class="function-color-picker"
                        title="Changer la couleur"
                      />
                      <span class="function-name">
                        <template v-if="editingFunctionNameIndex === index">
                          <input
                            :ref="el => functionNameInputRefs[index] = el"
                            v-model="func.name"
                            type="text"
                            inputmode="text"
                            class="function-name-input"
                            maxlength="30"
                            placeholder="f, f', C_f, \alpha..."
                            title="Nom (LaTeX supporté : f', C_f, \\alpha...)"
                            @blur="finishFunctionNameEdit(index)"
                            @keydown.enter.prevent="finishFunctionNameEdit(index)"
                            @keydown.esc.prevent="cancelFunctionNameEdit"
                          />
                          <span class="function-name-suffix">(x) =</span>
                        </template>
                        <template v-else>
                          <span class="function-name-label" :ref="el => functionNameLabelRefs[index] = el" @click="startFunctionNameEdit(index)" title="Cliquer pour renommer"></span>
                          <span class="function-name-suffix">(x) =</span>
                        </template>
                      </span>
                      <span class="function-expression" :ref="el => functionExpressionRefs[index] = el" @click="editFunction(index)" style="cursor: pointer;" title="Cliquer pour modifier"></span>
                      <button @click="removeFunction(index)" class="remove-function-btn">×</button>
                    </div>
                    <div class="function-item-toggles">
                      <select :value="func.lineDash || 'solid'" @change="func.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                        <option value="solid">───</option>
                        <option value="dot">·····</option>
                        <option value="dash">- - -</option>
                        <option value="dashdot">-·-·</option>
                        <option value="longdash">— —</option>
                      </select>
                      <select :value="func.lineWidth || 2" @change="func.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                      </select>
                      <button @click="func.showInLegend = func.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: func.showInLegend !== false }]" :title="func.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                      <button @click="func.showName = func.showName === false ? true : false; plotAllFunctions()" :class="['point-toggle-btn', { active: func.showName !== false }]" :title="func.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                    </div>
                  </div>
                </div>

                <!-- Liste des points créés -->
                <div v-if="points.length > 0" class="traced-shapes-section">
                  <h5 class="traced-shapes-title">Points</h5>
                  <div class="shapes-list">
                    <div v-for="(point, index) in points" :key="'side-fpt-' + index" class="shape-item shape-item-with-toggles">
                      <div class="shape-item-main">
                        <input type="color" :value="point.color" @input="changeShapeColor('point', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                        <template v-if="isEditingShape('point', index)">
                          <input v-model="point.name" type="text" :class="'shape-name-input shape-name-editing-point-' + index" maxlength="50" placeholder="P" @blur="finishShapeNameEdit('point', index)" @keydown.enter.prevent="finishShapeNameEdit('point', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                        </template>
                        <template v-else>
                          <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('point', index)" title="Cliquer pour renommer">{{ point.name }}</span>
                        </template>
                        <span class="shape-item-coords">({{ point.x }}, {{ point.y }})</span>
                        <button @click="removePoint(index)" class="remove-function-btn">×</button>
                      </div>
                      <div class="shape-item-toggles">
                        <button @click="point.showName = !point.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showName !== false }]" :title="point.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                        <button @click="point.showCoords = !point.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showCoords !== false }]" :title="point.showCoords !== false ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                        <button @click="cyclePointLabelFormat(point); plotAllFunctions()" :class="['point-toggle-btn', { active: normalizePointLabelFormat(point.labelFormat) !== 'default' }]" :title="getPointLabelFormatTitle(point.labelFormat)">{{ getPointLabelFormatChip(point.labelFormat) }}</button>
                        <button @click="point.showProjections = !point.showProjections; plotAllFunctions()" :class="['point-toggle-btn', { active: point.showProjections === true }]" :title="point.showProjections === true ? 'Masquer les pointillés sur les axes' : 'Afficher les pointillés sur les axes'">Proj</button>
                        <button @click="point.showInLegend = point.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: point.showInLegend !== false }]" :title="point.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                      </div>
                    </div>
                  </div>
                  <div v-if="points.length >= 2" class="connect-points-row">
                    <label class="connect-points-toggle">
                      <input type="checkbox" v-model="connectPoints" />
                      <span>Relier les points</span>
                    </label>
                    <input v-if="connectPoints" type="color" v-model="connectPointsColor" class="function-color-picker" title="Couleur de la liaison" />
                  </div>
                </div>

                <!-- Liste des segments/vecteurs créés -->
                <div v-if="segments.length > 0" class="traced-shapes-section">
                  <h5 class="traced-shapes-title">Segments / Vecteurs</h5>
                  <div class="shapes-list">
                    <div v-for="(segment, index) in segments" :key="'side-fseg-' + index" class="shape-item shape-item-with-toggles">
                      <div class="shape-item-main">
                        <input type="color" :value="segment.color" @input="changeShapeColor('segment', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                        <template v-if="isEditingShape('segment', index)">
                          <input v-model="segment.name" type="text" :class="'shape-name-input shape-name-editing-segment-' + index" maxlength="50" placeholder="S" @blur="finishShapeNameEdit('segment', index)" @keydown.enter.prevent="finishShapeNameEdit('segment', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                        </template>
                        <template v-else>
                          <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('segment', index)" title="Cliquer pour renommer">{{ segment.name || (segment.isVector ? 'V' : 'S') + (index + 1) }}</span>
                        </template>
                        <span class="shape-item-coords">{{ segment.isVector ? '→' : '—' }} ({{ segment.x1 }},{{ segment.y1 }})→({{ segment.x2 }},{{ segment.y2 }})</span>
                        <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                      </div>
                      <div class="shape-item-toggles">
                        <button @click="segment.showName = !segment.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showName === true }]" :title="segment.showName === true ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                        <button @click="segment.showCoords = !segment.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showCoords === true }]" :title="segment.showCoords === true ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                        <button @click="segment.showInLegend = segment.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: segment.showInLegend !== false }]" :title="segment.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                        <select :value="segment.lineDash || 'solid'" @change="segment.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                          <option value="solid">───</option>
                          <option value="dot">·····</option>
                          <option value="dash">- - -</option>
                          <option value="dashdot">-·-·</option>
                          <option value="longdash">— —</option>
                        </select>
                        <select :value="segment.lineWidth || 3" @change="segment.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                          <option value="4">4</option>
                          <option value="5">5</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Liste des cercles créés -->
                <div v-if="circles.length > 0" class="traced-shapes-section">
                  <h5 class="traced-shapes-title">Cercles</h5>
                  <div class="shapes-list">
                    <div v-for="(circle, index) in circles" :key="'side-fcir-' + index" class="shape-item shape-item-with-toggles">
                      <div class="shape-item-main">
                        <input type="color" :value="circle.color" @input="changeShapeColor('circle', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                        <template v-if="isEditingShape('circle', index)">
                          <input v-model="circle.name" type="text" :class="'shape-name-input shape-name-editing-circle-' + index" maxlength="50" placeholder="C" @blur="finishShapeNameEdit('circle', index)" @keydown.enter.prevent="finishShapeNameEdit('circle', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                        </template>
                        <template v-else>
                          <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('circle', index)" title="Cliquer pour renommer">{{ circle.name || 'C' + (index + 1) }}</span>
                        </template>
                        <span class="shape-item-coords">({{ circle.h }}, {{ circle.k }}) r={{ circle.r }}</span>
                        <button @click="removeCircle(index)" class="remove-function-btn">×</button>
                      </div>
                      <div class="shape-item-toggles">
                        <button @click="circle.showName = !circle.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: circle.showName !== false }]" :title="circle.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                        <button @click="circle.showInLegend = circle.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: circle.showInLegend !== false }]" :title="circle.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                        <select :value="circle.lineDash || 'solid'" @change="circle.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                          <option value="solid">───</option>
                          <option value="dot">·····</option>
                          <option value="dash">- - -</option>
                          <option value="dashdot">-·-·</option>
                          <option value="longdash">— —</option>
                        </select>
                        <select :value="circle.lineWidth || 2" @change="circle.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                          <option value="4">4</option>
                          <option value="5">5</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Liste des textes créés -->
                <div v-if="textAnnotations.length > 0" class="traced-shapes-section">
                  <h5 class="traced-shapes-title">Textes</h5>
                  <div class="shapes-list">
                    <div v-for="(ta, index) in textAnnotations" :key="'side-ftxt-' + index" class="shape-item">
                      <input type="color" :value="ta.color" @input="changeShapeColor('text', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                      <template v-if="isEditingShape('text', index)">
                        <input v-model="ta.content" type="text" :class="'shape-name-input shape-name-editing-text-' + index" maxlength="50" placeholder="Texte" @blur="finishShapeNameEdit('text', index)" @keydown.enter.prevent="finishShapeNameEdit('text', index)" @keydown.esc.prevent="cancelShapeNameEdit" style="flex: 1;" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('text', index)" title="Cliquer pour modifier" style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ ta.content }}</span>
                      </template>
                      <button @click="removeTextAnnotation(index)" class="remove-function-btn">×</button>
                    </div>
                  </div>
                </div>

                <!-- Liste des intersections -->
                <div v-if="intersectionPoints.length > 0" class="traced-shapes-section">
                  <h5 class="traced-shapes-title">Intersections</h5>
                  <div class="shapes-list">
                    <div v-for="(ipt, index) in intersectionPoints" :key="'side-fint-' + index" class="shape-item">
                      <input type="color" :value="ipt.color || '#dc2626'" @input="changeShapeColor('intersection', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                      <template v-if="isEditingShape('intersection', index)">
                        <input v-model="ipt.name" type="text" :class="'shape-name-input shape-name-editing-intersection-' + index" maxlength="20" :placeholder="ipt.defaultName" @blur="finishShapeNameEdit('intersection', index)" @keydown.enter.prevent="finishShapeNameEdit('intersection', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                      </template>
                      <template v-else>
                        <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('intersection', index)" title="Cliquer pour renommer">{{ ipt.name || ipt.defaultName }}</span>
                      </template>
                      <span class="shape-item-coords">({{ ipt.x.toFixed(2) }}, {{ ipt.y.toFixed(2) }})</span>
                      <button @click="removeIntersection(index)" class="remove-function-btn">×</button>
                    </div>
                  </div>
                </div>

                <div v-if="graphFunctions.length === 0 && points.length === 0 && segments.length === 0 && circles.length === 0 && textAnnotations.length === 0 && intersectionPoints.length === 0" class="no-content">
                  Aucun élément tracé.
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
                    <input type="checkbox" v-model="showCenterAxesOnly" />
                    Axes centraux seulement (0,0)
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showClickProjections" />
                    Projections pointillees au clic (x,y)
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="snapToGrid" />
                    Accrocher aux intersections de la grille
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showCurveLabels" />
                    Afficher les noms des courbes
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showPointLabels" />
                    Afficher les labels des points
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showLabelArrows" />
                    Flèches sur les labels
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showLabelBorders" />
                    Flèches sur les labels
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showLegend" />
                    Afficher la légende
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="allowPan" />
                    Déplacer le graphique (clic + glisser)
                  </label>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>Epaisseur des axes :</label>
                    <input v-model.number="axisLineWidth" type="number" min="1" max="10" step="0.5" class="bound-field" />
                  </div>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>X min :</label>
                    <input v-model.number="xMin" type="number" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>X max :</label>
                    <input v-model.number="xMax" type="number" class="bound-field" />
                  </div>
                </div>
                <div class="bounds-row">
                  <div class="bound-input">
                    <label>Y min :</label>
                    <input v-model.number="yMin" type="number" class="bound-field" />
                  </div>
                  <div class="bound-input">
                    <label>Y max :</label>
                    <input v-model.number="yMax" type="number" class="bound-field" />
                  </div>
                </div>
              </div>
              
              <!-- Onglet Asymptotes -->
              <div v-show="activeGraphTab === 'asymptotes'" class="tab-panel">
                <h4 class="panel-title">Asymptotes</h4>
                <div class="bound-input">
                  <label>Asymptotes verticales (séparées par des virgules) :</label>
                  <input 
                    v-model="verticalAsymptotes" 
                    type="text" 
                    class="bound-field"
                    placeholder="Exemple : -2, 3"
                  />
                </div>
                <div class="bound-input">
                  <label>Asymptotes horizontales (séparées par des virgules) :</label>
                  <input 
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
                  <div v-for="(point, index) in intersectionPoints" :key="'side-int-' + index" class="result-item" style="display: flex; align-items: center; gap: 6px;">
                    <input 
                      v-model="point.name" 
                      type="text" 
                      maxlength="15" 
                      @change="renameIntersection(index, point.name); plotAllFunctions()"
                      style="width: 80px; padding: 2px 4px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.85rem;"
                      :placeholder="point.defaultName"
                    />
                    <span>: ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})</span>
                  </div>
                </div>
                
                <div v-if="showRoots && rootsPoints.length > 0" class="results-section">
                  <h5 class="results-title">Racines :</h5>
                  <div v-for="(point, index) in rootsPoints" :key="'side-root-' + index" class="result-item" style="display: flex; align-items: center; gap: 6px;">
                    <span>{{ getFunctionDisplayNameByOneBasedIndex(point.funcIndex) }} : x = {{ point.x.toFixed(3) }}</span>
                  </div>
                </div>
                
                <div v-if="showAxisIntersections && axisIntersectionPoints.length > 0" class="results-section">
                  <h5 class="results-title">Intersections avec les axes :</h5>
                  <div v-for="(point, index) in axisIntersectionPoints" :key="'side-axis-' + index" class="result-item" style="display: flex; align-items: center; gap: 6px;">
                    <input 
                      v-model="point.name" 
                      type="text" 
                      maxlength="15" 
                      @change="renameAxisIntersection(index, point.name); plotAllFunctions()"
                      style="width: 80px; padding: 2px 4px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.85rem;"
                      :placeholder="point.defaultName"
                    />
                    <span>: ({{ point.x.toFixed(3) }}, {{ point.y.toFixed(3) }})</span>
                  </div>
                </div>
                
                <!-- Résolution d'inéquations -->
                <div class="calc-section" style="margin-top: 0.75rem;">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="showInequality" />
                    Résoudre des inéquations
                  </label>
                  <div v-if="showInequality && inequalityItems.length >= 2" class="calc-controls">
                    <div v-for="(ineq, ineqIdx) in inequalities" :key="'side-ineq-' + ineqIdx" style="margin-bottom: 0.75rem; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 8px; position: relative;" :style="{ borderLeftColor: ineq.color.replace('0.15', '0.6'), borderLeftWidth: '3px' }">
                      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <div style="display: flex; align-items: center; gap: 0.4rem;">
                          <input type="color" :value="rgbaToHex(ineq.color)" @input="updateInequalityColor(ineqIdx, $event.target.value)" style="width: 22px; height: 22px; border: none; padding: 0; cursor: pointer; border-radius: 4px; background: transparent;" title="Couleur de la zone" />
                          <span style="font-size: 0.8rem; font-weight: 600; color: #374151;">Inéquation {{ ineqIdx + 1 }}</span>
                        </div>
                        <button v-if="inequalities.length > 1" @click="removeInequality(ineqIdx)" class="remove-function-btn" title="Supprimer cette inéquation" style="font-size: 0.9rem;">×</button>
                      </div>
                      <div class="bounds-row">
                        <div class="bound-input">
                          <label>Él. 1 :</label>
                          <select v-model.number="ineq.func1Index" class="bound-field">
                            <option v-for="(item, index) in inequalityItems" :key="'side-iq1-' + ineqIdx + '-' + item.key" :value="index">
                              {{ item.label }}
                            </option>
                          </select>
                        </div>
                        <div class="bound-input">
                          <label>Signe :</label>
                          <select v-model="ineq.operator" class="bound-field">
                            <option value="<">&lt;</option>
                            <option value=">">&gt;</option>
                            <option value="<=">≤</option>
                            <option value=">=">≥</option>
                            <option value="=">=</option>
                          </select>
                        </div>
                        <div class="bound-input">
                          <label>Él. 2 :</label>
                          <select v-model.number="ineq.func2Index" class="bound-field">
                            <option v-for="(item, index) in inequalityItems" :key="'side-iq2-' + ineqIdx + '-' + item.key" :value="index">
                              {{ item.label }}
                            </option>
                          </select>
                        </div>
                      </div>
                      <div v-if="ineq.result" class="result-info inequality-result" style="margin-top: 0.3rem;">
                        <strong>Solution :</strong> <span v-html="ineq.result.display"></span>
                      </div>
                    </div>
                    <button @click="addInequality()" class="btn-secondary" style="width: 100%; padding: 0.4rem; font-size: 0.85rem; border-radius: 6px; border: 1px dashed #94a3b8; background: transparent; color: #64748b; cursor: pointer;">
                      + Ajouter une inéquation
                    </button>
                  </div>
                  <div v-if="showInequality && inequalityItems.length < 2" class="result-info" style="color: #ef4444;">
                    Il faut au moins 2 éléments tracés (fonctions ou segments).
                  </div>
                </div>

                <!-- Angles entre segments -->
                <div class="calc-section" style="margin-top: 0.75rem;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.3rem;">
                    <strong style="font-size: 0.9rem;">📐 Angles</strong>
                    <button v-if="segments.length >= 2" @click="addAngleMeasure" class="add-function-btn" style="font-size: 0.8rem; padding: 2px 8px;">+ Angle</button>
                  </div>
                  <div v-if="segments.length < 2" class="result-info" style="color: #ef4444; font-size: 0.85rem;">Il faut au moins 2 segments tracés.</div>
                  <div v-for="(angle, aIdx) in angleMeasures" :key="'mob-angle-' + aIdx" style="border-left: 3px solid; padding-left: 0.5rem; margin-bottom: 0.5rem;" :style="{ borderColor: angle.color }">
                    <div style="display: flex; align-items: center; gap: 0.3rem; margin-bottom: 0.25rem;">
                      <input type="color" :value="angle.color" @input="angle.color = $event.target.value; plotAllFunctions()" class="function-color-picker" title="Couleur" />
                      <span style="font-size: 0.85rem; flex: 1;">Angle {{ aIdx + 1 }}</span>
                      <button @click="removeAngleMeasure(aIdx)" class="remove-function-btn" title="Supprimer">×</button>
                    </div>
                    <div class="bounds-row">
                      <div class="bound-input">
                        <label>Seg 1 :</label>
                        <select v-model.number="angle.seg1Index" class="bound-field">
                          <option v-for="(seg, si) in segments" :key="'mob-a'+aIdx+'-s1-'+si" :value="si">{{ seg.name || (seg.isVector ? 'V' : 'S') + (si+1) }}</option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Seg 2 :</label>
                        <select v-model.number="angle.seg2Index" class="bound-field">
                          <option v-for="(seg, si) in segments" :key="'mob-a'+aIdx+'-s2-'+si" :value="si">{{ seg.name || (seg.isVector ? 'V' : 'S') + (si+1) }}</option>
                        </select>
                      </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.4rem; margin-top: 0.25rem; flex-wrap: wrap;">
                      <label class="checkbox-label" style="margin: 0; font-size: 0.8rem;">
                        <input type="checkbox" v-model="angle.showArc" /> Arc
                      </label>
                      <div class="bound-input" style="flex: 0 0 auto;">
                        <label style="font-size: 0.8rem;">Texte :</label>
                        <input v-model="angle.customText" class="bound-field" placeholder="auto" maxlength="30" style="max-width: 80px; font-size: 0.8rem;" />
                      </div>
                      <div class="bound-input" style="flex: 0 0 auto;">
                        <label style="font-size: 0.8rem;">Manuel ° :</label>
                        <input v-model="angle.manualDegrees" class="bound-field" type="number" step="0.1" placeholder="auto" style="max-width: 70px; font-size: 0.8rem;" />
                      </div>
                    </div>
                    <div v-if="angle.result" class="result-info" style="margin-top: 0.3rem;">
                      <strong>{{ angle.manualDegrees !== '' && !isNaN(parseFloat(angle.manualDegrees)) ? parseFloat(angle.manualDegrees) : angle.result.degrees }}°</strong> ({{ angle.result.radians }} rad)
                      <span v-if="!angle.result.hasCommonVertex" style="display: block; font-size: 0.8rem; color: #f59e0b;">⚠ Pas de sommet commun</span>
                    </div>
                    <div v-else-if="angle.seg1Index === angle.seg2Index" class="result-info" style="color: #ef4444; font-size: 0.8rem;">Choisissez 2 segments différents.</div>
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
                          <option v-for="(func, index) in graphFunctions" :key="'side-if-' + index" :value="index">
                            {{ functionDisplayNames[index] }}
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
                          <option v-for="(func, index) in graphFunctions" :key="'side-ac1-' + index" :value="index">
                            {{ functionDisplayNames[index] }}
                          </option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Fonction 2 :</label>
                        <select v-model.number="areaCurve2Index" class="bound-field">
                          <option v-for="(func, index) in graphFunctions" :key="'side-ac2-' + index" :value="index">
                            {{ functionDisplayNames[index] }}
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
                          <option v-for="(func, index) in graphFunctions" :key="'side-tf-' + index" :value="index">
                            {{ functionDisplayNames[index] }}
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
                      <label>Nom :</label>
                      <input v-model="pointName" type="text" class="bound-field" placeholder="A" maxlength="10" style="width: 60px;" />
                    </div>
                    <div class="bound-input">
                      <label>x :</label>
                      <input v-model="pointX" type="text" class="bound-field" placeholder="ex: e" />
                    </div>
                    <div class="bound-input">
                      <label>y :</label>
                      <input v-model="pointY" type="text" class="bound-field" placeholder="ex: 1" />
                    </div>
                  </div>
                  <button @click="addPoint" class="action-btn">Ajouter le point</button>
                  
                  <div style="margin-top: 8px;">
                    <label style="font-size: 0.8rem; color: #94a3b8;">Plusieurs points :</label>
                    <input v-model="pointsInput" type="text" class="bound-field" placeholder="A(e,1),B(3,4),C(pi,2)" style="width: 100%; margin-top: 4px;" @keyup.enter="addMultiplePoints" />
                    <button @click="addMultiplePoints" class="action-btn" style="margin-top: 4px;">Ajouter les points</button>
                  </div>
                  
                  <div v-if="points.length > 0" class="shapes-list">
                    <div v-for="(point, index) in points" :key="'side-pt-' + index" class="shape-item">
                      <span class="function-color" :style="{ backgroundColor: point.color }"></span>
                      <input 
                        v-model="point.name" 
                        type="text" 
                        class="point-name-input" 
                        maxlength="10" 
                        @change="plotAllFunctions()"
                        style="width: 50px; padding: 2px 4px; border: 1px solid #555; border-radius: 4px; background: #2a2a3e; color: white; font-size: 0.85rem;"
                      />
                      <span>({{ point.x }}, {{ point.y }})</span>
                      <button @click="removePoint(index)" class="remove-function-btn">×</button>
                    </div>
                  </div>
                </div>
                
                <!-- Segments -->
                <div class="shape-section">
                  <h5 class="shape-title">Ajouter un segment</h5>
                  
                  <div v-if="points.length >= 2" class="segment-from-points">
                    <p class="helper-text">Relier deux points :</p>
                    <div class="bounds-row">
                      <div class="bound-input">
                        <label>Point 1 :</label>
                        <select v-model.number="segmentPoint1Index" class="bound-field">
                          <option v-for="(point, index) in points" :key="'side-sp1-' + index" :value="index">
                            {{ point.name }} ({{ point.x }}, {{ point.y }})
                          </option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Point 2 :</label>
                        <select v-model.number="segmentPoint2Index" class="bound-field">
                          <option v-for="(point, index) in points" :key="'side-sp2-' + index" :value="index">
                            {{ point.name }} ({{ point.x }}, {{ point.y }})
                          </option>
                        </select>
                      </div>
                    </div>
                    <button @click="addSegmentFromPoints" class="action-btn">Relier les points</button>
                    <div class="divider-text">ou</div>
                  </div>
                  
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
                  <button @click="addSegment" class="action-btn">Ajouter le {{ segmentIsVector ? 'vecteur' : 'segment' }}</button>
                  <label class="checkbox-label" style="margin-top: 0.5rem;">
                    <input type="checkbox" v-model="segmentIsVector" />
                    Dessiner un vecteur (avec flèche)
                  </label>
                  
                  <div v-if="segments.length > 0" class="shapes-list">
                    <div v-for="(segment, index) in segments" :key="'side-seg-' + index" class="shape-item shape-item-with-toggles">
                      <div class="shape-item-main">
                        <input type="color" :value="segment.color" @input="changeShapeColor('segment', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                        <template v-if="isEditingShape('segment', index)">
                          <input v-model="segment.name" type="text" :class="'shape-name-input shape-name-editing-segment-' + index" maxlength="50" placeholder="S" @blur="finishShapeNameEdit('segment', index)" @keydown.enter.prevent="finishShapeNameEdit('segment', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                        </template>
                        <template v-else>
                          <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('segment', index)" title="Cliquer pour renommer">{{ segment.name || (segment.isVector ? 'V' : 'S') + (index + 1) }}</span>
                        </template>
                        <span class="shape-item-coords">{{ segment.isVector ? '→' : '—' }} ({{ segment.x1 }},{{ segment.y1 }})→({{ segment.x2 }},{{ segment.y2 }})</span>
                        <button @click="removeSegment(index)" class="remove-function-btn">×</button>
                      </div>
                      <div class="shape-item-toggles">
                        <button @click="segment.showName = !segment.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showName === true }]" :title="segment.showName === true ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                        <button @click="segment.showCoords = !segment.showCoords; plotAllFunctions()" :class="['point-toggle-btn', { active: segment.showCoords === true }]" :title="segment.showCoords === true ? 'Masquer les coordonnées' : 'Afficher les coordonnées'">Coord</button>
                        <button @click="segment.showInLegend = segment.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: segment.showInLegend !== false }]" :title="segment.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                        <select :value="segment.lineDash || 'solid'" @change="segment.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                          <option value="solid">───</option>
                          <option value="dot">·····</option>
                          <option value="dash">- - -</option>
                          <option value="dashdot">-·-·</option>
                          <option value="longdash">— —</option>
                        </select>
                        <select :value="segment.lineWidth || 3" @change="segment.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                          <option value="4">4</option>
                          <option value="5">5</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Droites -->
                <div class="shape-section">
                  <h5 class="shape-title">Tracer une droite</h5>
                  <div class="bounds-row">
                    <label class="radio-label"><input type="radio" v-model="droiteMode" value="2points" /> 2 points</label>
                    <label class="radio-label"><input type="radio" v-model="droiteMode" value="pointSlope" /> Point + pente</label>
                    <label class="radio-label"><input type="radio" v-model="droiteMode" value="pointVector" /> Point + vecteur</label>
                  </div>

                  <template v-if="droiteMode === '2points'">
                    <div v-if="points.length >= 2" class="bounds-row">
                      <div class="bound-input">
                        <label>Point 1 :</label>
                        <select v-model.number="droitePoint1Index" class="bound-field">
                          <option v-for="(point, index) in points" :key="'side-dp1-' + index" :value="index">
                            {{ point.name }} ({{ point.x }}, {{ point.y }})
                          </option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Point 2 :</label>
                        <select v-model.number="droitePoint2Index" class="bound-field">
                          <option v-for="(point, index) in points" :key="'side-dp2-' + index" :value="index">
                            {{ point.name }} ({{ point.x }}, {{ point.y }})
                          </option>
                        </select>
                      </div>
                    </div>
                    <p v-else class="helper-text">Créez au moins 2 points d'abord.</p>
                  </template>

                  <template v-if="droiteMode === 'pointSlope'">
                    <div v-if="points.length >= 1" class="bounds-row">
                      <div class="bound-input">
                        <label>Point :</label>
                        <select v-model.number="droitePointIndex" class="bound-field">
                          <option v-for="(point, index) in points" :key="'side-dps-' + index" :value="index">
                            {{ point.name }} ({{ point.x }}, {{ point.y }})
                          </option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Pente m :</label>
                        <input v-model.number="droiteSlope" type="number" step="0.5" class="bound-field" />
                      </div>
                    </div>
                    <p v-else class="helper-text">Créez au moins 1 point d'abord.</p>
                  </template>

                  <template v-if="droiteMode === 'pointVector'">
                    <div v-if="points.length >= 1" class="bounds-row">
                      <div class="bound-input">
                        <label>Point :</label>
                        <select v-model.number="droitePointIndex" class="bound-field">
                          <option v-for="(point, index) in points" :key="'side-dpv-' + index" :value="index">
                            {{ point.name }} ({{ point.x }}, {{ point.y }})
                          </option>
                        </select>
                      </div>
                      <div class="bound-input">
                        <label>Vec x :</label>
                        <input v-model.number="droiteVecX" type="number" step="0.5" class="bound-field" />
                      </div>
                      <div class="bound-input">
                        <label>Vec y :</label>
                        <input v-model.number="droiteVecY" type="number" step="0.5" class="bound-field" />
                      </div>
                    </div>
                    <p v-else class="helper-text">Créez au moins 1 point d'abord.</p>
                  </template>

                  <button @click="addDroite" class="action-btn" :disabled="(droiteMode === '2points' && points.length < 2) || ((droiteMode === 'pointSlope' || droiteMode === 'pointVector') && points.length < 1)">Tracer la droite</button>
                  <p class="helper-text" style="margin-top: 4px;">Ou saisissez : <code>(AB)</code>, <code>d(A,m=2)</code>, <code>d(A,u(1,2))</code></p>
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
                    <div v-for="(circle, index) in circles" :key="'side-cir-' + index" class="shape-item shape-item-with-toggles">
                      <div class="shape-item-main">
                        <input type="color" :value="circle.color" @input="changeShapeColor('circle', index, $event.target.value)" class="function-color-picker" title="Changer la couleur" />
                        <template v-if="isEditingShape('circle', index)">
                          <input v-model="circle.name" type="text" :class="'shape-name-input shape-name-editing-circle-' + index" maxlength="50" placeholder="C" @blur="finishShapeNameEdit('circle', index)" @keydown.enter.prevent="finishShapeNameEdit('circle', index)" @keydown.esc.prevent="cancelShapeNameEdit" />
                        </template>
                        <template v-else>
                          <span class="shape-item-name shape-name-clickable" @click="startShapeNameEdit('circle', index)" title="Cliquer pour renommer">{{ circle.name || 'C' + (index + 1) }}</span>
                        </template>
                        <span class="shape-item-coords">(h={{ circle.h }}, k={{ circle.k }}, r={{ circle.r }})</span>
                        <button @click="removeCircle(index)" class="remove-function-btn">×</button>
                      </div>
                      <div class="shape-item-toggles">
                        <button @click="circle.showName = !circle.showName; plotAllFunctions()" :class="['point-toggle-btn', { active: circle.showName !== false }]" :title="circle.showName !== false ? 'Masquer le nom' : 'Afficher le nom'">Nom</button>
                        <button @click="circle.showInLegend = circle.showInLegend === false ? true : false; plotAllFunctions()" :class="['legend-toggle-btn', { active: circle.showInLegend !== false }]" :title="circle.showInLegend !== false ? 'Masquer de la légende' : 'Afficher dans la légende'">Lég</button>
                        <select :value="circle.lineDash || 'solid'" @change="circle.lineDash = $event.target.value; plotAllFunctions()" class="line-style-select" title="Style de trait">
                          <option value="solid">───</option>
                          <option value="dot">·····</option>
                          <option value="dash">- - -</option>
                          <option value="dashdot">-·-·</option>
                          <option value="longdash">— —</option>
                        </select>
                        <select :value="circle.lineWidth || 2" @change="circle.lineWidth = Number($event.target.value); plotAllFunctions()" class="line-width-select" title="Épaisseur du trait">
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                          <option value="4">4</option>
                          <option value="5">5</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Textes personnalisés -->
                <div class="shape-section">
                  <h5 class="shape-title">✏️ Ajouter un texte</h5>
                  <p class="helper-text">Utilisez <code>$...$</code> pour du LaTeX.</p>
                  <div class="bounds-row">
                    <div class="bound-input" style="flex: 2;">
                      <label>Texte :</label>
                      <input v-model="newTextContent" type="text" class="bound-field" placeholder="$\alpha + \beta = \gamma$" />
                    </div>
                  </div>
                  <div class="bounds-row">
                    <div class="bound-input">
                      <label>x :</label>
                      <input v-model.number="newTextX" type="number" step="0.5" class="bound-field" />
                    </div>
                    <div class="bound-input">
                      <label>y :</label>
                      <input v-model.number="newTextY" type="number" step="0.5" class="bound-field" />
                    </div>
                    <div class="bound-input">
                      <label>Taille :</label>
                      <input v-model.number="newTextSize" type="number" min="8" max="120" step="1" class="bound-field" style="width: 70px;" />
                    </div>
                    <div class="bound-input">
                      <label>Couleur :</label>
                      <input v-model="newTextColor" type="color" class="bound-field" style="width: 40px; padding: 2px; height: 32px;" />
                    </div>
                    <div class="bound-input">
                      <label>Style :</label>
                      <label class="checkbox-label" style="margin: 0; gap: 0.35rem;">
                        <input v-model="newTextBold" type="checkbox" />
                        <span>Gras</span>
                      </label>
                    </div>
                  </div>
                  <button @click="addTextAnnotation" class="action-btn">Ajouter le texte</button>
                  
                  <div v-if="textAnnotations.length > 0" class="shapes-list">
                    <div v-for="(ta, index) in textAnnotations" :key="'side-txt-' + index" class="shape-item">
                      <span class="function-color" :style="{ backgroundColor: ta.color }"></span>
                      <span style="flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ ta.content }}</span>
                      <span style="opacity: 0.6; font-size: 0.8rem;">({{ ta.x }}, {{ ta.y }})</span>
                      <button @click="removeTextAnnotation(index)" class="remove-function-btn">×</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Lien vers page d'aide -->
        <div class="graph-help-link-row">
          <router-link to="/aide-grapheur" target="_blank" class="graph-help-link">
            ❓ Aide — Comment utiliser le grapheur
          </router-link>
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
  pointX, pointY, pointName, pointsInput,
  segmentX1, segmentY1, segmentX2, segmentY2, segmentIsVector, segmentName,
  circleH, circleK, circleR, circleName
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

// === Nommage des fonctions (ex: f, g, h...) ===
const editingFunctionNameIndex = ref(-1)
const originalEditingFunctionName = ref('')
const functionNameInputRefs = ref([])

const MAX_FUNCTION_NAME_LENGTH = 30

function sanitizeFunctionName(value) {
  const raw = (value ?? '').toString().trim()
  if (!raw) return ''
  return raw.slice(0, MAX_FUNCTION_NAME_LENGTH)
}

// Détecte si un nom contient du LaTeX (backslash, underscore, caret, prime)
function isLatexName(name) {
  return /[\\_{^']/.test(name)
}

function getFunctionDisplayName(func, index) {
  const custom = sanitizeFunctionName(func?.name)
  return custom || `f${index + 1}`
}

function splitFunctionNameParts(name) {
  const match = name.match(/^([a-zA-Z]+)([0-9]+)$/)
  if (match) return { base: match[1], sub: match[2] }
  return { base: name, sub: '' }
}

function getFunctionLatexLabel(func, index) {
  const name = getFunctionDisplayName(func, index)
  // Si le nom contient du LaTeX, le retourner tel quel
  if (isLatexName(name)) return name
  // Sinon, transformer f1 → f_{1}
  const match = name.match(/^([a-zA-Z]+)([0-9]+)$/)
  if (match) return `${match[1]}_{${match[2]}}`
  return name
}

const functionDisplayNames = computed(() =>
  graphFunctions.value.map((func, index) => getFunctionDisplayName(func, index))
)

const functionNameParts = computed(() =>
  functionDisplayNames.value.map(splitFunctionNameParts)
)

const functionNameLabelRefs = ref([])

function renderFunctionNameLabels() {
  nextTick(() => {
    graphFunctions.value.forEach((func, index) => {
      const el = functionNameLabelRefs.value[index]
      if (!el) return
      const name = getFunctionDisplayName(func, index)
      try {
        katex.render(name, el, { throwOnError: false, displayMode: false })
      } catch (e) {
        el.textContent = name
      }
    })
  })
}

function getFunctionDisplayNameByOneBasedIndex(oneBasedIndex) {
  const index = Number(oneBasedIndex) - 1
  if (Number.isNaN(index) || index < 0) return `f${oneBasedIndex}`
  return functionDisplayNames.value[index] || `f${oneBasedIndex}`
}

function startFunctionNameEdit(index) {
  const func = graphFunctions.value[index]
  if (!func) return

  originalEditingFunctionName.value = func.name ?? ''
  if (!sanitizeFunctionName(func.name)) {
    // Pré-remplir avec le nom affiché (ex: f1) pour faciliter la modification
    func.name = getFunctionDisplayName(func, index)
  }
  editingFunctionNameIndex.value = index

  nextTick(() => {
    const input = functionNameInputRefs.value[index]
    if (input) {
      input.focus()
      if (typeof input.select === 'function') input.select()
    }
  })
}

function finishFunctionNameEdit(index) {
  const func = graphFunctions.value[index]
  if (!func) return

  const sanitized = sanitizeFunctionName(func.name)
  const defaultName = `f${index + 1}`
  func.name = sanitized && sanitized !== defaultName ? sanitized : ''
  editingFunctionNameIndex.value = -1
  plotAllFunctions()
  nextTick(() => renderFunctionNameLabels())
}

function cancelFunctionNameEdit() {
  const index = editingFunctionNameIndex.value
  if (index < 0) return

  const func = graphFunctions.value[index]
  if (func) func.name = originalEditingFunctionName.value
  editingFunctionNameIndex.value = -1
}

// === Édition des formes (points, segments, cercles, textes) ===
// Type: 'point' | 'segment' | 'circle' | 'text'
const editingShapeType = ref('')
const editingShapeIndex = ref(-1)
const editingShapeOriginalName = ref('')

function startShapeNameEdit(type, index) {
  editingShapeType.value = type
  editingShapeIndex.value = index
  const item = getShapeItem(type, index)
  if (!item) return
  editingShapeOriginalName.value = item.name || item.content || ''
  nextTick(() => {
    // Focus the input that just appeared
    const input = document.querySelector(`.shape-name-editing-${type}-${index}`)
    if (input) {
      input.focus()
      input.select()
    }
  })
}

function finishShapeNameEdit(type, index) {
  if (editingShapeType.value !== type || editingShapeIndex.value !== index) return
  if (type === 'intersection') {
    const pt = intersectionPoints.value[index]
    if (pt) {
      renameIntersection(index, pt.name)
    }
  }
  editingShapeType.value = ''
  editingShapeIndex.value = -1
  plotAllFunctions()
}

function cancelShapeNameEdit() {
  if (editingShapeIndex.value < 0) return
  const item = getShapeItem(editingShapeType.value, editingShapeIndex.value)
  if (item) {
    if (editingShapeType.value === 'text') {
      item.content = editingShapeOriginalName.value
    } else {
      item.name = editingShapeOriginalName.value
    }
  }
  editingShapeType.value = ''
  editingShapeIndex.value = -1
}

function isEditingShape(type, index) {
  return editingShapeType.value === type && editingShapeIndex.value === index
}

function getShapeItem(type, index) {
  switch (type) {
    case 'point': return points.value[index]
    case 'segment': return segments.value[index]
    case 'circle': return circles.value[index]
    case 'text': return textAnnotations.value[index]
    case 'intersection': return intersectionPoints.value[index]
    default: return null
  }
}

function changeShapeColor(type, index, color) {
  if (type === 'intersection') {
    const pt = intersectionPoints.value[index]
    if (pt) {
      pt.color = color
      intersectionCustomColors.value[pt.key] = color
      plotAllFunctions()
    }
    return
  }
  const item = getShapeItem(type, index)
  if (item) {
    item.color = color
    plotAllFunctions()
  }
}

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
const showSidePanel = ref(true)

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

const getTabIcon = (tab) => {
  const icons = {
    functions: '📈',
    axes: '⚙️',
    asymptotes: '📐',
    analysis: '🔍',
    calculus: '📊',
    shapes: '🟢'
  }
  return icons[tab] || '📁'
}

const getTabShortLabel = (tab) => {
  const labels = {
    functions: 'Fonctions',
    axes: 'Axes',
    asymptotes: 'Asymptotes',
    analysis: 'Analyse',
    calculus: 'Calculs',
    shapes: 'Formes'
  }
  return labels[tab] || tab
}

// Mode snap to grid pour les points
const snapToGrid = ref(true)

// === MODE DESSIN INTERACTIF ===
// 'none' = clic ajoute un point (comportement actuel)
// 'point' = clic ajoute un point
// 'segment' = 2 clics pour un segment
// 'vector' = 2 clics pour un vecteur
const drawingMode = ref('none')
const drawingTempPoint = ref(null) // Premier point en attente pour segment/vecteur

function setDrawingMode(mode) {
  if (drawingMode.value === mode) {
    // Désactiver si on reclique
    drawingMode.value = 'none'
  } else {
    drawingMode.value = mode
  }
  drawingTempPoint.value = null
}

// Sélection de points pour créer des segments
const segmentPoint1Index = ref(0)
const segmentPoint2Index = ref(1)

// Création de droites
const droiteMode = ref('2points')  // '2points' | 'pointSlope' | 'pointVector'
const droitePoint1Index = ref(0)
const droitePoint2Index = ref(1)
const droiteSlope = ref(1)
const droiteVecX = ref(1)
const droiteVecY = ref(1)
const droitePointIndex = ref(0)

// Noms personnalisés persistants pour les intersections
const intersectionCustomNames = ref({})
const intersectionCustomColors = ref({})
const axisIntersectionCustomNames = ref({})

function getIntersectionKey(func1Index, func2Index, x, y) {
  return `${func1Index}-${func2Index}-${x.toFixed(3)}-${y.toFixed(3)}`
}

function getAxisIntersectionKey(funcIndex, axis, x, y) {
  return `${funcIndex}-${axis}-${x.toFixed(3)}-${y.toFixed(3)}`
}

function renameIntersection(index, newName) {
  const point = intersectionPoints.value[index]
  if (point) {
    point.name = newName || point.defaultName
    if (newName && newName !== point.defaultName) {
      intersectionCustomNames.value[point.key] = newName
    } else {
      delete intersectionCustomNames.value[point.key]
    }
  }
}

function renameAxisIntersection(index, newName) {
  const point = axisIntersectionPoints.value[index]
  if (point) {
    point.name = newName || point.defaultName
    if (newName && newName !== point.defaultName) {
      axisIntersectionCustomNames.value[point.key] = newName
    } else {
      delete axisIntersectionCustomNames.value[point.key]
    }
  }
}

// === ANNOTATIONS INTERACTIVES (labels déplaçables) ===
// Stocke les positions personnalisées des annotations (clé → {ax, ay})
const annotationPositions = ref({})
// Toggle pour afficher/masquer les annotations
const showCurveLabels = ref(true)
const showPointLabels = ref(true)
// Style des labels : flèches et encadrement
const showLabelArrows = ref(false)
const showLabelBorders = ref(false)
const showLegend = ref(true)

// Autoriser le déplacement (pan) du graphique
const allowPan = ref(false)
// Option: masquer axes/ticks de bord et ne garder que x=0 et y=0
const showCenterAxesOnly = ref(false)
const axisLineWidth = ref(2)
const showClickProjections = ref(true)
const clickedProjectionPoint = ref(null)

const POINT_LABEL_FORMAT_ORDER = ['default', 'normal', 'bold', 'italic', 'boldItalic']

function normalizePointLabelFormat(format) {
  return POINT_LABEL_FORMAT_ORDER.includes(format) ? format : 'default'
}

function cyclePointLabelFormat(point) {
  if (!point) return
  const current = normalizePointLabelFormat(point.labelFormat)
  const index = POINT_LABEL_FORMAT_ORDER.indexOf(current)
  point.labelFormat = POINT_LABEL_FORMAT_ORDER[(index + 1) % POINT_LABEL_FORMAT_ORDER.length]
}

function getPointLabelFormatChip(format) {
  const normalized = normalizePointLabelFormat(format)
  if (normalized === 'normal') return 'N'
  if (normalized === 'bold') return 'B'
  if (normalized === 'italic') return 'I'
  if (normalized === 'boldItalic') return 'BI'
  return 'Fmt'
}

function getPointLabelFormatTitle(format) {
  const normalized = normalizePointLabelFormat(format)
  if (normalized === 'normal') return 'Format normal'
  if (normalized === 'bold') return 'Format gras'
  if (normalized === 'italic') return 'Format italique'
  if (normalized === 'boldItalic') return 'Format gras + italique'
  return 'Format classique (nom en gras)'
}

function applyPointLabelFormat(text, format) {
  const normalized = normalizePointLabelFormat(format)
  if (normalized === 'bold') return `<b>${text}</b>`
  if (normalized === 'italic') return `<i>${text}</i>`
  if (normalized === 'boldItalic') return `<b><i>${text}</i></b>`
  return text
}

// Toggle pour relier les points entre eux (polyline)
const connectPoints = ref(false)
const connectPointsColor = ref('#1e3a8a')

// === RÉSOLUTION D'INÉQUATIONS ===
const showInequality = ref(false)

// === ANGLES ENTRE SEGMENTS ===
const ANGLE_COLORS = ["#f59e0b", "#ef4444", "#3b82f6", "#10b981", "#8b5cf6", "#ec4899"]
const angleMeasures = ref([])
let angleUpdating = false
// Chaque entrée : { seg1Index, seg2Index, showArc, customText, color, result, manualDegrees }
function addAngleMeasure() {
  const colorIdx = angleMeasures.value.length % ANGLE_COLORS.length
  angleUpdating = true
  angleMeasures.value.push({
    seg1Index: 0,
    seg2Index: Math.min(1, segments.value.length - 1),
    showArc: true,
    customText: '',
    color: ANGLE_COLORS[colorIdx],
    result: null,
    manualDegrees: ''
  })
  computeAllAngles()
  angleUpdating = false
  plotAllFunctions()
}
function removeAngleMeasure(idx) {
  // Nettoyer les positions d'annotation sauvegardées
  delete annotationPositions.value[`angle-label-${idx}`]
  angleUpdating = true
  angleMeasures.value.splice(idx, 1)
  // Renuméroter les positions
  const newPositions = {}
  for (const [k, v] of Object.entries(annotationPositions.value)) {
    const m = k.match(/^angle-label-(\d+)$/)
    if (m) {
      const oldIdx = parseInt(m[1])
      if (oldIdx > idx) newPositions[`angle-label-${oldIdx - 1}`] = v
      else newPositions[k] = v
    } else {
      newPositions[k] = v
    }
  }
  annotationPositions.value = newPositions
  angleUpdating = false
  plotAllFunctions()
}
const inequalityFunc1Index = ref(0)
const inequalityFunc2Index = ref(1)
const inequalityOperator = ref('<')  // '<', '>', '<=', '>=', '='
const inequalityResult = ref(null)  // { intervals: [...], intersections: [...] }
const inequalityShadingColor = ref('rgba(59, 130, 246, 0.15)')

// Support pour plusieurs inéquations
const inequalities = ref([
  { func1Index: 0, func2Index: 1, operator: '<', result: null, color: 'rgba(59, 130, 246, 0.15)' }
])

const INEQUALITY_COLORS = [
  'rgba(59, 130, 246, 0.15)',   // bleu
  'rgba(239, 68, 68, 0.15)',    // rouge
  'rgba(34, 197, 94, 0.15)',    // vert
  'rgba(168, 85, 247, 0.15)',   // violet
  'rgba(245, 158, 11, 0.15)',   // orange
  'rgba(6, 182, 212, 0.15)',    // cyan
]

// Conversion rgba(r, g, b, a) → #rrggbb pour le color picker
function rgbaToHex(rgba) {
  const m = rgba.match(/rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)/)
  if (!m) return '#3b82f6'
  const r = parseInt(m[1]).toString(16).padStart(2, '0')
  const g = parseInt(m[2]).toString(16).padStart(2, '0')
  const b = parseInt(m[3]).toString(16).padStart(2, '0')
  return `#${r}${g}${b}`
}

// Conversion #rrggbb → rgba(r, g, b, 0.15) pour le shading
function hexToRgba(hex) {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, 0.15)`
}

function updateInequalityColor(ineqIdx, hexColor) {
  inequalities.value[ineqIdx].color = hexToRgba(hexColor)
}

function addInequality() {
  inequalities.value.push({
    func1Index: 0,
    func2Index: Math.min(1, inequalityItems.value.length - 1),
    operator: '<',
    result: null,
    color: INEQUALITY_COLORS[inequalities.value.length % INEQUALITY_COLORS.length]
  })
}

function removeInequality(index) {
  inequalities.value.splice(index, 1)
  if (inequalities.value.length === 0) {
    inequalities.value.push({ func1Index: 0, func2Index: 1, operator: '<', result: null, color: INEQUALITY_COLORS[0] })
  }
  // Le watcher deep déclenche automatiquement solveAllInequalities + plotAllFunctions
}

// Liste unifiée des éléments sélectionnables pour l'inéquation (fonctions + segments)
const inequalityItems = computed(() => {
  const items = []
  graphFunctions.value.forEach((func, index) => {
    items.push({
      type: 'function',
      index,
      label: getFunctionDisplayName(func, index),
      key: `f-${index}`
    })
  })
  segments.value.forEach((seg, index) => {
    if (!seg.isVector) {
      const name = seg.name || `S${index + 1}`
      items.push({
        type: 'segment',
        index,
        label: name,
        key: `s-${index}`
      })
    }
  })
  return items
})

// === TEXTES PERSONNALISÉS ===
const textAnnotations = ref([])
const newTextContent = ref('')
const newTextX = ref(0)
const newTextY = ref(0)
const newTextColor = ref('#1e3a8a')
const newTextSize = ref(16)
const newTextBold = ref(false)

function addTextAnnotation() {
  const content = String(newTextContent.value || '').trim()
  if (!content) return
  const parsedSize = Number(newTextSize.value)
  const safeSize = Number.isFinite(parsedSize)
    ? Math.max(8, Math.min(120, parsedSize))
    : 16

  textAnnotations.value.push({
    content,
    x: newTextX.value,
    y: newTextY.value,
    color: newTextColor.value,
    size: safeSize,
    bold: newTextBold.value === true
  })
  newTextContent.value = ''
  newTextX.value = 0
  newTextY.value = 0
  plotAllFunctions()
}

function removeTextAnnotation(index) {
  // Supprimer la position sauvegardée
  delete annotationPositions.value[`text-${index}`]
  textAnnotations.value.splice(index, 1)
  // Réindexer les positions
  const newPositions = {}
  Object.keys(annotationPositions.value).forEach(key => {
    if (key.startsWith('text-')) {
      const oldIdx = parseInt(key.split('-')[1])
      if (oldIdx > index) {
        newPositions[`text-${oldIdx - 1}`] = annotationPositions.value[key]
      } else {
        newPositions[key] = annotationPositions.value[key]
      }
    } else {
      newPositions[key] = annotationPositions.value[key]
    }
  })
  annotationPositions.value = newPositions
  plotAllFunctions()
}

// Convertit le texte utilisateur en format Plotly (supporte LaTeX avec $...$)
function getLatexSizeCommand(size) {
  const numeric = Number(size)
  if (!Number.isFinite(numeric)) return ''
  if (numeric <= 12) return '\\small '
  if (numeric <= 16) return ''
  if (numeric <= 20) return '\\large '
  if (numeric <= 24) return '\\Large '
  if (numeric <= 30) return '\\LARGE '
  if (numeric <= 40) return '\\huge '
  return '\\Huge '
}

function styleLatexSegment(content, { size = 16, bold = false } = {}) {
  const raw = String(content ?? '').trim()
  if (!raw) return '$$'
  const sizeCommand = getLatexSizeCommand(size)
  const styled = `${sizeCommand}${raw}`
  if (bold) return `$\\boldsymbol{${styled}}$`
  return `$${styled}$`
}

function formatTextForPlotly(text, { size = 16, bold = false } = {}) {
  // Si le texte contient des délimiteurs LaTeX $...$, on les garde tels quels
  // Plotly/MathJax les interprète nativement
  // Sinon on retourne le texte brut
  const rawText = String(text ?? '')
  const hasLatex = /\$[^$]+\$/.test(rawText)

  if (!hasLatex) {
    return bold ? `<b>${rawText}</b>` : rawText
  }

  const styled = rawText.replace(/\$([^$]+)\$/g, (_match, latexContent) => {
    return styleLatexSegment(latexContent, { size, bold })
  })

  if (!bold) return styled

  return styled
    .split(/(\$[^$]+\$)/g)
    .map(part => {
      if (!part) return part
      if (part.startsWith('$') && part.endsWith('$')) return part
      return `<b>${part}</b>`
    })
    .join('')
}

// === CALCUL D'ANGLE ===
function computeSingleAngle(angle) {
  if (segments.value.length < 2) { angle.result = null; return }
  const i1 = angle.seg1Index
  const i2 = angle.seg2Index
  if (i1 === i2 || !segments.value[i1] || !segments.value[i2]) { angle.result = null; return }
  const s1 = segments.value[i1]
  const s2 = segments.value[i2]

  let vertex = null, angle1Start, angle2Start
  // Vecteurs partant du sommet commun vers les extrémités opposées
  let vx1, vy1, vx2, vy2
  const eps = 0.01
  if (Math.abs(s1.x2 - s2.x1) < eps && Math.abs(s1.y2 - s2.y1) < eps) {
    vertex = { x: s1.x2, y: s1.y2 }
    vx1 = s1.x1 - vertex.x; vy1 = s1.y1 - vertex.y
    vx2 = s2.x2 - vertex.x; vy2 = s2.y2 - vertex.y
  } else if (Math.abs(s1.x1 - s2.x1) < eps && Math.abs(s1.y1 - s2.y1) < eps) {
    vertex = { x: s1.x1, y: s1.y1 }
    vx1 = s1.x2 - vertex.x; vy1 = s1.y2 - vertex.y
    vx2 = s2.x2 - vertex.x; vy2 = s2.y2 - vertex.y
  } else if (Math.abs(s1.x2 - s2.x2) < eps && Math.abs(s1.y2 - s2.y2) < eps) {
    vertex = { x: s1.x2, y: s1.y2 }
    vx1 = s1.x1 - vertex.x; vy1 = s1.y1 - vertex.y
    vx2 = s2.x1 - vertex.x; vy2 = s2.y1 - vertex.y
  } else if (Math.abs(s1.x1 - s2.x2) < eps && Math.abs(s1.y1 - s2.y2) < eps) {
    vertex = { x: s1.x1, y: s1.y1 }
    vx1 = s1.x2 - vertex.x; vy1 = s1.y2 - vertex.y
    vx2 = s2.x1 - vertex.x; vy2 = s2.y1 - vertex.y
  } else {
    // Pas de sommet commun — utiliser les directions brutes
    vx1 = s1.x2 - s1.x1; vy1 = s1.y2 - s1.y1
    vx2 = s2.x2 - s2.x1; vy2 = s2.y2 - s2.y1
  }

  const norm1 = Math.sqrt(vx1*vx1 + vy1*vy1)
  const norm2 = Math.sqrt(vx2*vx2 + vy2*vy2)
  if (norm1 === 0 || norm2 === 0) { angle.result = null; return }

  const dot = vx1*vx2 + vy1*vy2
  let cosAngle = Math.max(-1, Math.min(1, dot / (norm1*norm2)))
  const radians = Math.acos(cosAngle)
  const degrees = radians * 180 / Math.PI

  if (vertex) {
    angle1Start = Math.atan2(vy1, vx1)
    angle2Start = Math.atan2(vy2, vx2)
  }

  angle.result = {
    degrees: Math.round(degrees * 100) / 100,
    radians: Math.round(radians * 10000) / 10000,
    vertex,
    angle1Start: angle1Start ?? null,
    angle2Start: angle2Start ?? null,
    hasCommonVertex: vertex !== null
  }
}
function computeAllAngles() {
  angleMeasures.value.forEach(a => computeSingleAngle(a))
}

// Dessine les arcs d'angle (ou carrés d'angle droit) pour tous les angles
function drawAllAngleArcs(traces) {
  const windowSize = Math.min(xMax.value - xMin.value, yMax.value - yMin.value)
  const baseRadius = windowSize * 0.06

  angleMeasures.value.forEach((angle, idx) => {
    if (!angle.showArc || !angle.result) return
    const res = angle.result
    if (!res.hasCommonVertex || !res.vertex) return
    const color = angle.color || '#f59e0b'
    const arcRadius = baseRadius * (1 + idx * 0.25) // décaler les arcs pour éviter superposition

    let a1 = res.angle1Start
    let a2 = res.angle2Start
    let startAngle = a1, diff = a2 - a1
    while (diff > Math.PI) diff -= 2 * Math.PI
    while (diff < -Math.PI) diff += 2 * Math.PI
    if (diff < 0) { startAngle = a2; diff = -diff }

    // Valeur affichée (manuelle ou calculée)
    const displayDeg = angle.manualDegrees !== '' && !isNaN(parseFloat(angle.manualDegrees))
      ? parseFloat(angle.manualDegrees) : res.degrees
    const isRightAngle = Math.abs(displayDeg - 90) < 0.5

    if (isRightAngle) {
      const sqSize = arcRadius * 0.8
      const u1x = Math.cos(startAngle), u1y = Math.sin(startAngle)
      const u2x = Math.cos(startAngle + diff), u2y = Math.sin(startAngle + diff)
      const p1x = res.vertex.x + sqSize * u1x, p1y = res.vertex.y + sqSize * u1y
      const pmx = res.vertex.x + sqSize * u1x + sqSize * u2x
      const pmy = res.vertex.y + sqSize * u1y + sqSize * u2y
      const p2x = res.vertex.x + sqSize * u2x, p2y = res.vertex.y + sqSize * u2y
      traces.push({
        x: [p1x, pmx, p2x], y: [p1y, pmy, p2y],
        type: 'scatter', mode: 'lines',
        line: { color, width: 2, dash: 'solid' },
        name: '∟ 90°', showlegend: false,
        hovertemplate: '<b>Angle droit</b><br>90°<extra></extra>'
      })
    } else {
      const numPoints = 40, arcX = [], arcY = []
      for (let i = 0; i <= numPoints; i++) {
        const t = startAngle + (diff * i) / numPoints
        arcX.push(res.vertex.x + arcRadius * Math.cos(t))
        arcY.push(res.vertex.y + arcRadius * Math.sin(t))
      }
      traces.push({
        x: arcX, y: arcY,
        type: 'scatter', mode: 'lines',
        line: { color, width: 2, dash: 'solid' },
        name: `∠ ${displayDeg}°`, showlegend: false,
        hovertemplate: `<b>Angle</b><br>${displayDeg}°<extra></extra>`
      })
    }
  })
}

// Texte affiché pour le label d'un angle
function getAngleLabelText(angle) {
  if (angle.customText && angle.customText.trim()) return angle.customText.trim()
  if (!angle.result) return ''
  const displayDeg = angle.manualDegrees !== '' && !isNaN(parseFloat(angle.manualDegrees))
    ? parseFloat(angle.manualDegrees) : angle.result.degrees
  if (Math.abs(displayDeg - 90) < 0.5) return '' // Le carré suffit
  return `${displayDeg}°`
}

// Génère les annotations pour les courbes, points, et intersections
function buildInteractiveAnnotations() {
  const annotations = []
  
  // --- Annotations pour les courbes ---
  if (showCurveLabels.value) {
    graphFunctions.value.forEach((func, index) => {
      if (func.type === 'vertical' || func.type === 'horizontal') return
      if (func.showName === false) return
      
      const funcName = getFunctionDisplayName(func, index)
      const funcLatex = getFunctionLatexLabel(func, index)
      const key = `curve-${index}`
      const saved = annotationPositions.value[key]
      
      // Position par défaut : ~30% de la plage x visible
      const labelX = xMin.value + (xMax.value - xMin.value) * (0.25 + index * 0.15)
      const js = convertLatexToJS(func.latex)
      const labelY = evaluateFunction(js, labelX)
      
      if (isFinite(labelY) && labelY >= yMin.value && labelY <= yMax.value) {
        annotations.push({
          x: labelX,
          y: labelY,
          xref: 'x',
          yref: 'y',
          text: isLatexName(funcName) ? `$${funcLatex}$` : `<b>${funcName}</b>`,
          showarrow: true,
          arrowhead: showLabelArrows.value ? 0 : 0,
          arrowsize: 1,
          arrowwidth: showLabelArrows.value ? 1.5 : 0,
          arrowcolor: showLabelArrows.value ? func.color : 'rgba(0,0,0,0)',
          ax: saved?.ax ?? 0,
          ay: saved?.ay ?? -30,
          font: {
            size: 16,
            color: func.color,
            family: 'Arial, sans-serif'
          },
          bgcolor: showLabelBorders.value ? 'rgba(255,255,255,0.85)' : 'rgba(0,0,0,0)',
          bordercolor: showLabelBorders.value ? func.color : 'rgba(0,0,0,0)',
          borderwidth: showLabelBorders.value ? 1 : 0,
          borderpad: showLabelBorders.value ? 3 : 0,
          captureevents: true,
          _key: key
        })
      }
    })
  }
  
  // --- Annotations pour les points utilisateur ---
  if (showPointLabels.value) {
    points.value.forEach((point, index) => {
      const key = `point-${index}`
      const saved = annotationPositions.value[key]
      const displayName = point.name || `P${index + 1}`
      const showName = point.showName !== false
      const showCoords = point.showCoords !== false
      const labelFormat = normalizePointLabelFormat(point.labelFormat)
      
      // Build annotation text based on visibility flags
      let annotText = ''
      if (labelFormat === 'default') {
        if (showName && showCoords) annotText = `<b>${displayName}</b>(${point.x}, ${point.y})`
        else if (showName) annotText = `<b>${displayName}</b>`
        else if (showCoords) annotText = `(${point.x}, ${point.y})`
      } else {
        let baseText = ''
        if (showName && showCoords) baseText = `${displayName}(${point.x}, ${point.y})`
        else if (showName) baseText = `${displayName}`
        else if (showCoords) baseText = `(${point.x}, ${point.y})`
        annotText = applyPointLabelFormat(baseText, labelFormat)
      }
      
      // Skip annotation entirely if both hidden
      if (!showName && !showCoords) return
      
      annotations.push({
        x: point.x,
        y: point.y,
        xref: 'x',
        yref: 'y',
        text: annotText,
        showarrow: true,
        arrowhead: 0,
        arrowsize: 1,
        arrowwidth: showLabelArrows.value ? 1.5 : 0,
        arrowcolor: showLabelArrows.value ? point.color : 'rgba(0,0,0,0)',
        ax: saved?.ax ?? 20,
        ay: saved?.ay ?? -25,
        font: {
          size: 14,
          color: point.color,
          family: 'Arial, sans-serif'
        },
        bgcolor: showLabelBorders.value ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0)',
        bordercolor: showLabelBorders.value ? point.color : 'rgba(0,0,0,0)',
        borderwidth: showLabelBorders.value ? 1 : 0,
        borderpad: showLabelBorders.value ? 3 : 0,
        captureevents: true,
        _key: key
      })
    })
  }
  
  // --- Annotations pour les segments et vecteurs ---
  if (showPointLabels.value) {
    segments.value.forEach((segment, index) => {
      const key = `segment-${index}`
      const saved = annotationPositions.value[key]
      const displayName = segment.name || (segment.isVector ? `V${index + 1}` : `S${index + 1}`)
      const midX = (segment.x1 + segment.x2) / 2
      const midY = (segment.y1 + segment.y2) / 2
      const segShowName = segment.showName === true
      const segShowCoords = segment.showCoords === true
      
      let segAnnotText = ''
      if (segShowName && segShowCoords) segAnnotText = `<b>${displayName}</b> (${segment.x1},${segment.y1})→(${segment.x2},${segment.y2})`
      else if (segShowName) segAnnotText = `<b>${displayName}</b>`
      else if (segShowCoords) segAnnotText = `(${segment.x1},${segment.y1})→(${segment.x2},${segment.y2})`
      
      if (!segShowName && !segShowCoords) return
      
      annotations.push({
        x: midX,
        y: midY,
        xref: 'x',
        yref: 'y',
        text: segAnnotText,
        showarrow: true,
        arrowhead: 0,
        arrowsize: 1,
        arrowwidth: showLabelArrows.value ? 1.5 : 0,
        arrowcolor: showLabelArrows.value ? segment.color : 'rgba(0,0,0,0)',
        ax: saved?.ax ?? 0,
        ay: saved?.ay ?? -20,
        font: {
          size: 14,
          color: segment.color,
          family: 'Arial, sans-serif'
        },
        bgcolor: showLabelBorders.value ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0)',
        bordercolor: showLabelBorders.value ? segment.color : 'rgba(0,0,0,0)',
        borderwidth: showLabelBorders.value ? 1 : 0,
        borderpad: showLabelBorders.value ? 3 : 0,
        captureevents: true,
        _key: key
      })
    })
  }
  
  // --- Annotations pour les cercles ---
  if (showPointLabels.value) {
    circles.value.forEach((circle, index) => {
      const key = `circle-${index}`
      const saved = annotationPositions.value[key]
      const displayName = circle.name || `C${index + 1}`
      
      if (circle.showName === false) return
      
      annotations.push({
        x: circle.h,
        y: circle.k,
        xref: 'x',
        yref: 'y',
        text: `<b>${displayName}</b>`,
        showarrow: true,
        arrowhead: 0,
        arrowsize: 1,
        arrowwidth: showLabelArrows.value ? 1.5 : 0,
        arrowcolor: showLabelArrows.value ? circle.color : 'rgba(0,0,0,0)',
        ax: saved?.ax ?? 0,
        ay: saved?.ay ?? -20,
        font: {
          size: 14,
          color: circle.color,
          family: 'Arial, sans-serif'
        },
        bgcolor: showLabelBorders.value ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0)',
        bordercolor: showLabelBorders.value ? circle.color : 'rgba(0,0,0,0)',
        borderwidth: showLabelBorders.value ? 1 : 0,
        borderpad: showLabelBorders.value ? 3 : 0,
        captureevents: true,
        _key: key
      })
    })
  }
  
  // --- Annotations pour les intersections ---
  if (showPointLabels.value) {
    intersectionPoints.value.forEach((point, index) => {
      const key = `inter-${index}`
      const saved = annotationPositions.value[key]
      const displayName = point.name || point.defaultName
      const xCoord = Math.abs(point.x) < 0.01 ? 0 : Number(point.x.toFixed(2))
      const yCoord = Math.abs(point.y) < 0.01 ? 0 : Number(point.y.toFixed(2))
      
      annotations.push({
        x: point.x,
        y: point.y,
        xref: 'x',
        yref: 'y',
        text: `<b>${displayName}</b>(${xCoord}, ${yCoord})`,
        showarrow: true,
        arrowhead: 0,
        arrowsize: 1,
        arrowwidth: showLabelArrows.value ? 1.5 : 0,
        arrowcolor: showLabelArrows.value ? '#dc2626' : 'rgba(0,0,0,0)',
        ax: saved?.ax ?? 25,
        ay: saved?.ay ?? -20,
        font: {
          size: 13,
          color: '#dc2626',
          family: 'Arial, sans-serif'
        },
        bgcolor: showLabelBorders.value ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0)',
        bordercolor: showLabelBorders.value ? '#dc2626' : 'rgba(0,0,0,0)',
        borderwidth: showLabelBorders.value ? 1 : 0,
        borderpad: showLabelBorders.value ? 2 : 0,
        captureevents: true,
        _key: key
      })
    })
  }
  
  // --- Annotations pour les textes personnalisés (jamais de flèche ni encadré) ---
  textAnnotations.value.forEach((ta, index) => {
    const key = `text-${index}`
    const saved = annotationPositions.value[key]
    
    annotations.push({
      x: ta.x,
      y: ta.y,
      xref: 'x',
      yref: 'y',
      text: formatTextForPlotly(ta.content, { size: ta.size || 16, bold: ta.bold === true }),
      showarrow: false,
      ax: saved?.ax ?? 0,
      ay: saved?.ay ?? 0,
      font: {
        size: ta.size || 16,
        color: ta.color,
        family: ta.bold === true ? 'Arial Black, Arial, sans-serif' : 'Arial, sans-serif'
      },
      bgcolor: 'rgba(0,0,0,0)',
      bordercolor: 'rgba(0,0,0,0)',
      borderwidth: 0,
      borderpad: 0,
      captureevents: true,
      _key: key
    })
  })
  
  // --- Annotations pour les labels d'angle ---
  const windowSize = Math.min(xMax.value - xMin.value, yMax.value - yMin.value)
  const baseRadius = windowSize * 0.06
  angleMeasures.value.forEach((angle, idx) => {
    if (!angle.showArc || !angle.result || !angle.result.hasCommonVertex) return
    const labelText = getAngleLabelText(angle)
    if (!labelText) return
    const res = angle.result
    const arcRadius = baseRadius * (1 + idx * 0.25)
    
    let a1 = res.angle1Start, a2 = res.angle2Start
    let startAngle = a1, diff = a2 - a1
    while (diff > Math.PI) diff -= 2 * Math.PI
    while (diff < -Math.PI) diff += 2 * Math.PI
    if (diff < 0) { startAngle = a2; diff = -diff }
    
    const midAngle = startAngle + diff / 2
    const labelR = arcRadius * 1.5
    const labelX = res.vertex.x + labelR * Math.cos(midAngle)
    const labelY = res.vertex.y + labelR * Math.sin(midAngle)
    
    const key = `angle-label-${idx}`
    const saved = annotationPositions.value[key]
    const color = angle.color || '#f59e0b'
    
    annotations.push({
      x: labelX,
      y: labelY,
      xref: 'x',
      yref: 'y',
      text: `<b>${labelText}</b>`,
      showarrow: false,
      ax: saved?.ax ?? 0,
      ay: saved?.ay ?? 0,
      font: {
        size: 14,
        color: color,
        family: 'Arial, sans-serif'
      },
      bgcolor: 'rgba(0,0,0,0)',
      bordercolor: 'rgba(0,0,0,0)',
      borderwidth: 0,
      borderpad: 0,
      captureevents: true,
      _key: key
    })
  })
  
  return annotations
}

// Gestion du déplacement des annotations  
function handleAnnotationDrag(eventData) {
  if (!eventData) return
  
  // Plotly envoie les positions modifiées sous forme annotations[i].ax, annotations[i].ay
  const keys = Object.keys(eventData)
  
  // Récupérer la liste actuelle des annotations
  const currentAnnotations = graphContainer.value?.layout?.annotations || []
  
  keys.forEach(key => {
    const match = key.match(/^annotations\[(\d+)\]\.(ax|ay)$/)
    if (match) {
      const annotIdx = parseInt(match[1])
      const prop = match[2]
      const value = eventData[key]
      
      // Retrouver la clé de l'annotation
      // On doit chercher parmi les annotations existantes (les 4 premières sont les axes)
      const axisAnnotationCount = showAxes.value ? 4 : 0
      const interactiveIdx = annotIdx - axisAnnotationCount
      
      if (interactiveIdx >= 0) {
        const interactiveAnnotations = buildInteractiveAnnotations()
        const annotation = interactiveAnnotations[interactiveIdx]
        if (annotation && annotation._key) {
          if (!annotationPositions.value[annotation._key]) {
            annotationPositions.value[annotation._key] = { ax: 0, ay: -30 }
          }
          annotationPositions.value[annotation._key][prop] = value
        }
      }
    }
  })
}

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
      return { text: 'ex: ', latex: 'x^{2},\\, A(1{,}2),\\, [AB],\\, \\vec{AB}', closeParen: false }
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
      closeSpan.textContent = data.closeParen === false ? '' : ')'
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
    hideMathLiveKeyboard()
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
  if (selectedOperation.value === 'graph' && (graphFunctions.value.length >= 2 || segments.value.length > 0 || circles.value.length > 0)) {
    plotAllFunctions()
  }
})

// Watchers pour les toggles de labels
watch([showCurveLabels, showPointLabels, showLabelArrows, showLabelBorders, showLegend, allowPan], () => {
  if (selectedOperation.value === 'graph') {
    plotAllFunctions()
  }
})

// Watcher pour relier les points
watch([connectPoints, connectPointsColor], () => {
  if (selectedOperation.value === 'graph') {
    plotAllFunctions()
  }
})

// Watcher pour les inéquations (multiples)
// Le résultat textuel se met à jour instantanément, le re-plot du graphique est debounced
let inequalityPlotTimeout = null
let inequalitySolving = false
watch([showInequality, inequalities], () => {
  if (inequalitySolving) return // Éviter la boucle infinie (solveAll écrit dans inequalities)
  
  // Résoudre immédiatement pour afficher le résultat textuel sans délai
  if (selectedOperation.value === 'graph' && showInequality.value && inequalityItems.value.length >= 2) {
    inequalitySolving = true
    solveAllInequalities()
    inequalitySolving = false
  } else if (!showInequality.value) {
    inequalitySolving = true
    inequalities.value.forEach(ineq => { ineq.result = null })
    inequalityResult.value = null
    inequalitySolving = false
  }
  // Debouncer le re-plot (shading) car c'est coûteux
  if (inequalityPlotTimeout) clearTimeout(inequalityPlotTimeout)
  inequalityPlotTimeout = setTimeout(() => {
    if (selectedOperation.value === 'graph') {
      plotAllFunctions()
    }
  }, 200)
}, { deep: true })

// Watcher pour l'angle entre segments (debounced)
let anglePlotTimeout = null
watch([angleMeasures, () => segments.value.length], () => {
  if (angleUpdating) return
  // Calculer immédiatement les résultats (léger)
  computeAllAngles()
  // Debouncer le re-plot (coûteux)
  if (anglePlotTimeout) clearTimeout(anglePlotTimeout)
  anglePlotTimeout = setTimeout(() => {
    plotAllFunctions()
  }, 250)
}, { deep: true })

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
watch([showGrid, showAxes, showTicks, showCenterAxesOnly, axisLineWidth, showClickProjections], () => {
  if (selectedOperation.value === 'graph') {
    plotAllFunctions()
  }
})

// Re-render quand le panneau latéral est togglé (le graphe change de taille)
watch(showSidePanel, () => {
  if (selectedOperation.value === 'graph') {
    nextTick(() => {
      plotAllFunctions()
    })
  }
})

// Re-render quand le mode dessin change (pan vs dessin)
watch(drawingMode, () => {
  if (drawingMode.value !== 'none') {
    clickedProjectionPoint.value = null
  }
  if (selectedOperation.value === 'graph') {
    plotAllFunctions()
  }
})

watch(showClickProjections, (enabled) => {
  if (!enabled && clickedProjectionPoint.value) {
    clickedProjectionPoint.value = null
  }
})

// Nettoyer les écouteurs d'événements
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
  if (graphContainer.value?._clickListener) {
    graphContainer.value.removeEventListener('click', graphContainer.value._clickListener)
  }
  if (graphContainer.value?._plotlyClickListener && graphContainer.value.removeListener) {
    graphContainer.value.removeListener('plotly_click', graphContainer.value._plotlyClickListener)
  }
  if (graphContainer.value?._relayoutListener && graphContainer.value.removeListener) {
    graphContainer.value.removeListener('plotly_relayout', graphContainer.value._relayoutListener)
  }
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

function hideMathLiveKeyboard() {
  if (typeof window === 'undefined') return
  const virtualKeyboard = window.mathVirtualKeyboard
  if (virtualKeyboard?.visible) {
    virtualKeyboard.hide()
  }
}

function handleMathFieldFocus() {
  isFocused.value = true
  hideMathLiveKeyboard()
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

function parsePointCoordinateToken(rawToken) {
  const raw = String(rawToken ?? '').trim()
  if (!raw) return NaN

  let normalized = raw
    .replace(',', '.')
    .replace(/π/g, 'pi')
    .replace(/\bpi\b/gi, 'Math.PI')

  const jsExpr = convertLatexToJS(normalized).replace(/\s+/g, '')
  if (!jsExpr || /\bx\b/i.test(jsExpr)) return NaN

  try {
    const value = Function(`"use strict"; return (${jsExpr});`)()
    return (typeof value === 'number' && Number.isFinite(value)) ? value : NaN
  } catch {
    return NaN
  }
}

// === Parser intelligent : détecte les points, segments, vecteurs, cercles dans l'input ===
function parseSmartInput(rawLatex) {
  // Normaliser : retirer \left \right, espaces, accolades MathLive, \operatorname
  const cleaned = rawLatex
    .replace(/\\left/g, '')
    .replace(/\\right/g, '')
    .replace(/\\operatorname\{([^}]*)\}/g, '$1')
    .replace(/\\,/g, ',')
    .replace(/\\lbrack/g, '[')
    .replace(/\\rbrack/g, ']')
    .replace(/\{/g, '')
    .replace(/\}/g, '')
    .replace(/\s+/g, '')

  // Pattern pour un nombre (entier ou décimal, positif ou négatif)
  const num = '-?\\d+(?:\\.\\d+)?'
  // Pattern pour une coordonnée (supporte e, pi, +, -, /, ^)
  const coord = '-?[A-Za-z0-9π\\\\.+*/^\\-]+'
  // Pattern pour un nom de point (lettre majuscule + optionnel alphanum)
  const ptName = '[A-Z][a-zA-Z0-9]*'

  // 1. Plusieurs points : A(1,2),B(3,4),C(5,6) ou A(1;2),B(3;4)
  const multiPointRe = new RegExp(`(${ptName})\\((${coord})[,;](${coord})\\)`, 'g')
  const multiPoints = []
  let mpMatch
  while ((mpMatch = multiPointRe.exec(cleaned)) !== null) {
    const x = parsePointCoordinateToken(mpMatch[2])
    const y = parsePointCoordinateToken(mpMatch[3])
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      return {
        type: 'invalidPointCoord',
        name: mpMatch[1],
        xRaw: mpMatch[2],
        yRaw: mpMatch[3]
      }
    }
    multiPoints.push({
      name: mpMatch[1],
      x,
      y
    })
  }
  if (multiPoints.length >= 2) {
    return { type: 'multipoints', points: multiPoints }
  }

  // 1b. Point unique : A(1,2) ou A(-3.5, 2)
  if (multiPoints.length === 1) {
    return {
      type: 'point',
      name: multiPoints[0].name,
      x: multiPoints[0].x,
      y: multiPoints[0].y
    }
  }

  // 2. Cercle : C(0,0,3) — nom + centre + rayon (3 arguments)
  const circleRe = new RegExp(`^(${ptName})\\((${num}),(${num}),(${num})\\)$`)
  const circleMatch = cleaned.match(circleRe)
  if (circleMatch) {
    return {
      type: 'circle',
      name: circleMatch[1],
      h: parseFloat(circleMatch[2]),
      k: parseFloat(circleMatch[3]),
      r: parseFloat(circleMatch[4])
    }
  }

  // 3. Segment : [AB] — entre deux points existants
  const segmentRe = new RegExp(`^\\[(${ptName})(${ptName})\\]$`)
  const segmentMatch = cleaned.match(segmentRe)
  if (segmentMatch) {
    return {
      type: 'segment',
      point1Name: segmentMatch[1],
      point2Name: segmentMatch[2]
    }
  }

  // 4. Vecteur : \vec{AB} ou \overrightarrow{AB}
  const vecRe = new RegExp(`^\\\\vec(${ptName})(${ptName})$`)
  const vecMatch = cleaned.match(vecRe)
    || cleaned.match(new RegExp(`^\\\\overrightarrow(${ptName})(${ptName})$`))
  if (vecMatch) {
    return {
      type: 'vector',
      point1Name: vecMatch[1],
      point2Name: vecMatch[2]
    }
  }

  // 5. Droite : (AB) — droite passant par deux points
  const lineRe = new RegExp(`^\\((${ptName})(${ptName})\\)$`)
  const lineMatch = cleaned.match(lineRe)
  if (lineMatch) {
    return {
      type: 'line',
      point1Name: lineMatch[1],
      point2Name: lineMatch[2]
    }
  }

  // 6. Droite avec pente : d(A,m=2) ou D(A,m=-0.5)
  const lineSlopeRe = new RegExp(`^[dD]\\((${ptName}),m=(${num})\\)$`)
  const lineSlopeMatch = cleaned.match(lineSlopeRe)
  if (lineSlopeMatch) {
    return {
      type: 'lineSlope',
      pointName: lineSlopeMatch[1],
      slope: parseFloat(lineSlopeMatch[2])
    }
  }

  // 7. Droite avec vecteur directeur : d(A,u(1,2)) ou D(A,u(-1,3))
  const lineVecRe = new RegExp(`^[dD]\\((${ptName}),[uv]\\((${num}),(${num})\\)\\)$`)
  const lineVecMatch = cleaned.match(lineVecRe)
  if (lineVecMatch) {
    return {
      type: 'lineVector',
      pointName: lineVecMatch[1],
      dx: parseFloat(lineVecMatch[2]),
      dy: parseFloat(lineVecMatch[3])
    }
  }

  // 8. Équation de droite : ax+by+c=0 ou ax+by=c ou y=mx+p
  // Accepte des formes comme : 2y+4x+2=0, 3x-y+1=0, y=2x+1, x=3, y=-3x, 2x+3y=6, -x+2y-4=0
  {
    // Normaliser l'équation : tout ramener à gauche (gauche - droite = 0)
    const eqParts = cleaned.split('=')
    if (eqParts.length === 2) {
      const lhs = eqParts[0]
      const rhs = eqParts[1]

      // Fonction pour extraire les coefficients a, b, c d'une expression linéaire en x et y
      function parseLinearExpr(expr) {
        let a = 0, b = 0, c = 0
        let s = expr.replace(/\s/g, '').replace(/\*/g, '')
        if (!s) return { a, b, c }

        // Regex qui capture chaque terme : signe + coefficient optionnel + variable optionnelle
        // Deux alternatives : (1) terme avec variable x/y (2) constante seule
        const termRe = /([+-]?)(\d+(?:\.\d+)?)?([xy])|([+-]?\d+(?:\.\d+)?)/g
        let match
        while ((match = termRe.exec(s)) !== null) {
          if (match[0] === '') { termRe.lastIndex++; continue }
          if (match[3]) {
            // Terme avec variable (x ou y)
            const sign = match[1] === '-' ? -1 : 1
            const coeff = match[2] ? parseFloat(match[2]) : 1
            if (match[3] === 'x') a += sign * coeff
            else b += sign * coeff
          } else if (match[4] !== undefined) {
            // Terme constant
            c += parseFloat(match[4])
          }
        }
        return { a, b, c }
      }

      // Tester si ça ressemble à une équation linéaire (contient x et/ou y, pas de x² ni fonctions)
      const combined = lhs + rhs
      const hasXorY = /[xy]/.test(combined)
      const hasHigherOrder = /[xy]\^|[xy][xy]|sin|cos|tan|log|ln|sqrt|\\/.test(combined)
      
      if (hasXorY && !hasHigherOrder) {
        const left = parseLinearExpr(lhs)
        const right = parseLinearExpr(rhs)
        
        // ax + by + c = 0  →  (left.a - right.a)x + (left.b - right.b)y + (left.c - right.c) = 0
        const A = left.a - right.a
        const B = left.b - right.b
        const C = left.c - right.c
        
        if (A !== 0 || B !== 0) {
          return {
            type: 'lineEquation',
            a: A,
            b: B,
            c: C,
            rawEquation: rawLatex
          }
        }
      }
    }
  }

  return null // Pas un pattern reconnu → traiter comme une fonction
}

function findPointByName(name) {
  return points.value.find(p => p.name === name)
}

function handleSmartInput(parsed) {
  const color = shapes.getNextColor()

  if (parsed.type === 'invalidPointCoord') {
    return {
      success: false,
      message: `Coordonnées invalides pour ${parsed.name}(${parsed.xRaw}, ${parsed.yRaw}). Exemple: ${parsed.name}(e,1)`
    }
  }

  if (parsed.type === 'multipoints') {
    const names = []
    for (const pt of parsed.points) {
      const c = shapes.getNextColor()
      points.value.push({
        x: pt.x,
        y: pt.y,
        color: c,
        name: pt.name,
        showName: true,
        showCoords: true,
        showInLegend: true
      })
      names.push(`${pt.name}(${pt.x}, ${pt.y})`)
    }
    plotAllFunctions()
    return { success: true, message: `${parsed.points.length} points ajoutés : ${names.join(', ')}` }
  }

  if (parsed.type === 'point') {
    points.value.push({
      x: parsed.x,
      y: parsed.y,
      color: color,
      name: parsed.name,
      showName: true,
      showCoords: true,
      showInLegend: true
    })
    plotAllFunctions()
    return { success: true, message: `Point ${parsed.name}(${parsed.x}, ${parsed.y}) ajouté` }
  }

  if (parsed.type === 'circle') {
    if (parsed.r <= 0) {
      return { success: false, message: 'Le rayon doit être supérieur à 0' }
    }
    circles.value.push({
      h: parsed.h,
      k: parsed.k,
      r: parsed.r,
      color: color,
      name: parsed.name,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 2
    })
    plotAllFunctions()
    return { success: true, message: `Cercle ${parsed.name} centre(${parsed.h}, ${parsed.k}) r=${parsed.r} ajouté` }
  }

  if (parsed.type === 'segment' || parsed.type === 'vector') {
    const p1 = findPointByName(parsed.point1Name)
    const p2 = findPointByName(parsed.point2Name)
    if (!p1) return { success: false, message: `Point "${parsed.point1Name}" non trouvé. Créez-le d'abord (ex: ${parsed.point1Name}(1,2))` }
    if (!p2) return { success: false, message: `Point "${parsed.point2Name}" non trouvé. Créez-le d'abord (ex: ${parsed.point2Name}(3,4))` }

    const isVector = parsed.type === 'vector'
    const name = isVector ? `\\vec{${parsed.point1Name}${parsed.point2Name}}` : `[${parsed.point1Name}${parsed.point2Name}]`
    segments.value.push({
      x1: p1.x, y1: p1.y,
      x2: p2.x, y2: p2.y,
      color: color,
      isVector: isVector,
      name: name,
      showName: false,
      showCoords: false,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 3
    })
    plotAllFunctions()
    const label = isVector ? 'Vecteur' : 'Segment'
    return { success: true, message: `${label} ${parsed.point1Name}${parsed.point2Name} ajouté` }
  }

  if (parsed.type === 'line') {
    const p1 = findPointByName(parsed.point1Name)
    const p2 = findPointByName(parsed.point2Name)
    if (!p1) return { success: false, message: `Point "${parsed.point1Name}" non trouvé. Créez-le d'abord (ex: ${parsed.point1Name}(1,2))` }
    if (!p2) return { success: false, message: `Point "${parsed.point2Name}" non trouvé. Créez-le d'abord (ex: ${parsed.point2Name}(3,4))` }

    // Calculer l'équation de la droite y = ax + b
    if (p1.x === p2.x) {
      // Droite verticale x = constante
      graphFunctions.value.push({
        name: `(${parsed.point1Name}${parsed.point2Name})`,
        expression: `x = ${p1.x}`,
        color: color,
        latex: `x = ${p1.x}`,
        type: 'vertical',
        value: p1.x,
        showInLegend: true,
        lineDash: 'solid',
        lineWidth: 2
      })
    } else {
      const a = (p2.y - p1.y) / (p2.x - p1.x)
      const b = p1.y - a * p1.x
      const expr = b >= 0 ? `${a}*x+${b}` : `${a}*x${b}`
      const displayExpr = b >= 0 ? `${a}x + ${b}` : `${a}x - ${Math.abs(b)}`
      graphFunctions.value.push({
        name: `(${parsed.point1Name}${parsed.point2Name})`,
        expression: displayExpr,
        color: color,
        latex: expr,
        type: 'function',
        value: null,
        showInLegend: true,
        lineDash: 'solid',
        lineWidth: 2
      })
    }
    plotAllFunctions()
    nextTick(() => renderFunctionExpressions())
    return { success: true, message: `Droite (${parsed.point1Name}${parsed.point2Name}) ajoutée` }
  }

  // Droite avec pente : d(A,m=2)
  if (parsed.type === 'lineSlope') {
    const p = findPointByName(parsed.pointName)
    if (!p) return { success: false, message: `Point "${parsed.pointName}" non trouvé. Créez-le d'abord (ex: ${parsed.pointName}(1,2))` }

    const m = parsed.slope
    const b = p.y - m * p.x
    const mR = Math.round(m * 10000) / 10000
    const bR = Math.round(b * 10000) / 10000

    const expr = bR >= 0 ? `${mR}*x+${bR}` : `${mR}*x${bR}`
    const displayExpr = bR >= 0 ? `${mR}x + ${bR}` : `${mR}x - ${Math.abs(bR)}`

    graphFunctions.value.push({
      name: `d(${p.name})`,
      expression: displayExpr,
      color: color,
      latex: expr,
      type: 'function',
      value: null,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 2
    })
    plotAllFunctions()
    nextTick(() => renderFunctionExpressions())
    return { success: true, message: `Droite passant par ${p.name} avec pente m=${m} ajoutée` }
  }

  // Droite avec vecteur directeur : d(A,u(1,2))
  if (parsed.type === 'lineVector') {
    const p = findPointByName(parsed.pointName)
    if (!p) return { success: false, message: `Point "${parsed.pointName}" non trouvé. Créez-le d'abord (ex: ${parsed.pointName}(1,2))` }

    const dx = parsed.dx
    const dy = parsed.dy
    if (dx === 0 && dy === 0) return { success: false, message: 'Le vecteur directeur ne peut pas être nul' }

    if (dx === 0) {
      // Droite verticale
      graphFunctions.value.push({
        name: `d(${p.name})`,
        expression: `x = ${p.x}`,
        color: color,
        latex: `x = ${p.x}`,
        type: 'vertical',
        value: p.x,
        showInLegend: true,
        lineDash: 'solid',
        lineWidth: 2
      })
      plotAllFunctions()
      nextTick(() => renderFunctionExpressions())
      return { success: true, message: `Droite verticale x = ${p.x} ajoutée` }
    }

    const m = dy / dx
    const b = p.y - m * p.x
    const mR = Math.round(m * 10000) / 10000
    const bR = Math.round(b * 10000) / 10000

    const expr = bR >= 0 ? `${mR}*x+${bR}` : `${mR}*x${bR}`
    const displayExpr = bR >= 0 ? `${mR}x + ${bR}` : `${mR}x - ${Math.abs(bR)}`

    graphFunctions.value.push({
      name: `d(${p.name})`,
      expression: displayExpr,
      color: color,
      latex: expr,
      type: 'function',
      value: null,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 2
    })
    plotAllFunctions()
    nextTick(() => renderFunctionExpressions())
    return { success: true, message: `Droite passant par ${p.name} avec vecteur (${dx}, ${dy}) ajoutée` }
  }

  // Gérer les équations de droite ax + by + c = 0
  if (parsed.type === 'lineEquation') {
    const { a, b, c, rawEquation } = parsed
    const color = getNextColor()

    if (b === 0 && a !== 0) {
      // Droite verticale x = -c/a
      const xVal = Math.round((-c / a) * 10000) / 10000
      graphFunctions.value.push({
        name: `d${graphFunctions.value.length + 1}`,
        expression: `x = ${xVal}`,
        color: color,
        latex: `x = ${xVal}`,
        type: 'vertical',
        value: xVal,
        showInLegend: true,
        lineDash: 'solid',
        lineWidth: 2
      })
      plotAllFunctions()
      nextTick(() => renderFunctionExpressions())
      return { success: true, message: `Droite verticale x = ${xVal} ajoutée` }
    }

    // y = -(a/b)x - c/b
    const slope = Math.round((-a / b) * 10000) / 10000
    const intercept = Math.round((-c / b) * 10000) / 10000

    const expr = intercept >= 0 ? `${slope}*x+${intercept}` : `${slope}*x${intercept}`
    let displayExpr = ''
    if (slope === 0) {
      displayExpr = `${intercept}`
    } else if (slope === 1) {
      displayExpr = intercept === 0 ? 'x' : (intercept > 0 ? `x + ${intercept}` : `x - ${Math.abs(intercept)}`)
    } else if (slope === -1) {
      displayExpr = intercept === 0 ? '-x' : (intercept > 0 ? `-x + ${intercept}` : `-x - ${Math.abs(intercept)}`)
    } else {
      displayExpr = intercept === 0 ? `${slope}x` : (intercept > 0 ? `${slope}x + ${intercept}` : `${slope}x - ${Math.abs(intercept)}`)
    }

    graphFunctions.value.push({
      name: `d${graphFunctions.value.length + 1}`,
      expression: displayExpr,
      color: color,
      latex: expr,
      type: 'function',
      value: null,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 2
    })
    plotAllFunctions()
    nextTick(() => renderFunctionExpressions())
    return { success: true, message: `Droite ${displayExpr} ajoutée` }
  }

  return { success: false, message: 'Type non reconnu' }
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

    // === Essayer le parser intelligent (points, segments, vecteurs, cercles) ===
    const parsed = parseSmartInput(rawExpression)
    if (parsed) {
      const result = handleSmartInput(parsed)
      if (preview.value) {
        if (result.success) {
          preview.value.innerHTML = `<span style='color:#10b981;font-size:0.9rem;'>${result.message}</span>`
          mf.value.value = ''
          expressionValue.value = ''
        } else {
          preview.value.innerHTML = `<span style='color:#ef4444;font-size:0.9rem;'>${result.message}</span>`
        }
      }
      return
    }

    // === Sinon, traiter comme une fonction normale ===
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
      name: '',
      expression: displayExpression,
      color: color,
      latex: processedExpression,
      type: type,
      value: value,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 2
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
function handlePlotlyPointClick(eventData) {
  if (!showClickProjections.value || drawingMode.value !== 'none') return

  const pointData = eventData?.points?.[0]
  if (!pointData) return
  if (pointData?.data?.meta === 'click-projection-helper' || pointData?.data?.meta === 'point-projection-helper') return

  const x = Number(pointData.x)
  const y = Number(pointData.y)
  if (!Number.isFinite(x) || !Number.isFinite(y)) return

  clickedProjectionPoint.value = { x, y }
  plotAllFunctions()
}

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
  const yRel = 1 - ((yInPx - plotBottom) / plotHeight)
  
  // Convertir en coordonnées du graphique
  const xRange = xaxis.range[1] - xaxis.range[0]
  const yRange = yaxis.range[1] - yaxis.range[0]
  
  let x = xaxis.range[0] + xRel * xRange
  let y = yaxis.range[0] + yRel * yRange
  
  // Vérifier que les coordonnées sont valides
  if (x === undefined || y === undefined || isNaN(x) || isNaN(y)) return
  
  // Snap to grid
  if (snapToGrid.value) {
    x = Math.round(x)
    y = Math.round(y)
  } else {
    const gridX = Math.round(x)
    const gridY = Math.round(y)
    const snapThreshold = 0.15
    if (Math.abs(x - gridX) < snapThreshold) x = gridX
    if (Math.abs(y - gridY) < snapThreshold) y = gridY
    x = Math.round(x * 100) / 100
    y = Math.round(y * 100) / 100
  }
  
  // === MODE CERCLE ===
  if (drawingMode.value === 'circle') {
    if (!drawingTempPoint.value) {
      // Premier clic : stocker le centre
      drawingTempPoint.value = { x, y }
      // Ajouter un marqueur temporaire pour le centre
      const colorIndex = circles.value.length % GRAPH_COLORS.length
      const tempColor = GRAPH_COLORS[colorIndex]
      points.value.push({
        x, y,
        color: tempColor,
        name: `✘`,
        _temp: true
      })
      plotAllFunctions()
    } else {
      // Deuxième clic : créer le cercle (rayon = distance centre → ce point)
      const center = drawingTempPoint.value
      const r = Math.sqrt(Math.pow(x - center.x, 2) + Math.pow(y - center.y, 2))
      
      if (r > 0) {
        const colorIndex = circles.value.length % GRAPH_COLORS.length
        const circleColor = GRAPH_COLORS[colorIndex]
        circles.value.push({
          h: center.x,
          k: center.y,
          r: Math.round(r * 100) / 100,
          color: circleColor,
          name: `C${circles.value.length + 1}`
        })
      }
      
      // Supprimer le point temporaire
      const tempIdx = points.value.findIndex(p => p._temp)
      if (tempIdx !== -1) points.value.splice(tempIdx, 1)
      
      drawingTempPoint.value = null
      plotAllFunctions()
    }
    return
  }
  
  // === MODE SEGMENT ou VECTEUR ===
  if (drawingMode.value === 'segment' || drawingMode.value === 'vector') {
    if (!drawingTempPoint.value) {
      // Premier clic : stocker le point de départ
      drawingTempPoint.value = { x, y }
      // Ajouter un marqueur temporaire
      const colorIndex = segments.value.length % GRAPH_COLORS.length
      const tempColor = GRAPH_COLORS[colorIndex]
      // Ajouter le point de départ comme point temporaire visible
      points.value.push({
        x, y,
        color: tempColor,
        name: `✘`,
        _temp: true
      })
      plotAllFunctions()
    } else {
      // Deuxième clic : créer le segment/vecteur
      const start = drawingTempPoint.value
      const colorIndex = segments.value.length % GRAPH_COLORS.length
      const segColor = GRAPH_COLORS[colorIndex]
      const isVector = drawingMode.value === 'vector'
      
      segments.value.push({
        x1: start.x,
        y1: start.y,
        x2: x,
        y2: y,
        color: segColor,
        isVector: isVector,
        showName: false,
        showCoords: false
      })
      
      // Supprimer le point temporaire
      const tempIdx = points.value.findIndex(p => p._temp)
      if (tempIdx !== -1) points.value.splice(tempIdx, 1)
      
      drawingTempPoint.value = null
      plotAllFunctions()
    }
    return
  }
  
  // === MODE POINT (uniquement si activé) ===
  if (drawingMode.value !== 'point') return
  
  // Vérifier si ce point existe déjà
  const existingPoint = points.value.find(
    p => Math.abs(p.x - x) < 0.01 && Math.abs(p.y - y) < 0.01
  )
  if (existingPoint) return
  
  const colorIndex = points.value.length % GRAPH_COLORS.length
  const pointColor = GRAPH_COLORS[colorIndex]
  const autoIndex = points.value.length + 1
  points.value.push({
    x: x,
    y: y,
    color: pointColor,
    name: `P${autoIndex}`,
    showName: true,
    showCoords: true,
    showInLegend: true
  })
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
          name: func.showName !== false ? `$${func.expression}$` : '',
          line: {
            color: func.color,
            width: func.lineWidth || 2,
            dash: func.lineDash || 'solid'
          },
          legendgroup: `func${index}`,
          showlegend: func.showInLegend !== false,
          hovertemplate: `<b>${func.expression}</b><br>x: ${func.value}<extra></extra>`
        })
      } else if (func.type === 'horizontal') {
        // Droite horizontale : y = constante
        traces.push({
          x: [xMin.value, xMax.value],
          y: [func.value, func.value],
          type: 'scatter',
          mode: 'lines',
          name: func.showName !== false ? `$${func.expression}$` : '',
          line: {
            color: func.color,
            width: func.lineWidth || 2,
            dash: func.lineDash || 'solid'
          },
          legendgroup: `func${index}`,
          showlegend: func.showInLegend !== false,
          hovertemplate: `<b>${func.expression}</b><br>y: ${func.value}<extra></extra>`
        })
      } else {
        // Fonction normale
        const { x, y } = generateFunctionData(func.latex, xMin.value, xMax.value, yMin.value, yMax.value, 3000)
        
        // Convertir l'expression LaTeX pour l'affichage dans la légende avec MathJax
        const functionLabel = getFunctionLatexLabel(func, index)
        const displayName = func.showName !== false ? `$${functionLabel}(x) = ${func.expression}$` : `$${func.expression}$`
        const hoverName = func.showName !== false ? `${getFunctionDisplayName(func, index)}(x)` : func.expression
        
        traces.push({
          x: x,
          y: y,
          type: 'scatter',
          mode: 'lines',
          name: displayName,
          line: {
            color: func.color,
            width: func.lineWidth || 2,
            dash: func.lineDash || 'solid'
          },
          legendgroup: `func${index}`,
          showlegend: func.showInLegend !== false,
          hovertemplate: `<b>${hoverName}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
        })
      }
    } catch (error) {
      console.error(`Erreur lors du tracé de la fonction ${func.expression}:`, error)
    }
  })
  
  // Ajouter les asymptotes manuelles
  addManualAsymptotes(traces)
  
  // Calculer et afficher les points d'intersection si l'option est activée
  const hasEnoughForIntersections = graphFunctions.value.length >= 2 
    || (segments.value.length > 0 && graphFunctions.value.length >= 1) 
    || segments.value.length >= 2
    || (circles.value.length > 0 && (graphFunctions.value.length >= 1 || segments.value.length >= 1))
  if (showIntersections.value && hasEnoughForIntersections) {
    calculateIntersections(traces)
  } else {
    intersectionPoints.value = []
  }
  
  // Calculer et afficher les intersections avec les axes si l'option est activée
  if (showAxisIntersections.value && graphFunctions.value.length > 0) {
    calculateAxisIntersections(traces)
  } else {
    axisIntersectionPoints.value = []
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
  
  // Dessiner l'arc d'angle entre segments
  drawAllAngleArcs(traces)
  
  // Relier les points entre eux (polyline fermée)
  if (connectPoints.value && points.value.length >= 2) {
    const nonTempPoints = points.value.filter(p => !p._temp)
    if (nonTempPoints.length >= 2) {
      // Fermer la forme en ajoutant le premier point à la fin
      const xs = nonTempPoints.map(p => p.x)
      const ys = nonTempPoints.map(p => p.y)
      xs.push(nonTempPoints[0].x)
      ys.push(nonTempPoints[0].y)
      traces.push({
        x: xs,
        y: ys,
        type: 'scatter',
        mode: 'lines',
        line: {
          color: connectPointsColor.value,
          width: 2.5,
          dash: 'solid'
        },
        name: 'Liaison points',
        showlegend: true,
        hoverinfo: 'skip'
      })
    }
  }

  // === Shading pour les inéquations (supporte fonctions, segments, et combinaisons) ===
  if (showInequality.value && inequalityItems.value.length >= 2) {
    // Cache des conversions LaTeX -> JS pour le shading
    const shadingJsCache = {}
    function evalShadingItem(item, x) {
      if (item.type === 'function') {
        const func = graphFunctions.value[item.index]
        if (!func) return NaN
        if (func.type === 'horizontal') return func.value
        if (func.type === 'vertical') return NaN
        if (!shadingJsCache[func.latex]) {
          shadingJsCache[func.latex] = convertLatexToJS(func.latex)
        }
        return evaluateFunction(shadingJsCache[func.latex], x)
      } else if (item.type === 'segment') {
        const seg = segments.value[item.index]
        if (!seg) return NaN
        const minX = Math.min(seg.x1, seg.x2)
        const maxX = Math.max(seg.x1, seg.x2)
        if (x < minX - 1e-9 || x > maxX + 1e-9) return NaN
        if (Math.abs(seg.x2 - seg.x1) < 1e-10) return NaN
        const t = (x - seg.x1) / (seg.x2 - seg.x1)
        return seg.y1 + t * (seg.y2 - seg.y1)
      }
      return NaN
    }

    inequalities.value.forEach((ineq, ineqGlobalIdx) => {
      if (!ineq.result || !ineq.result.intervals || ineq.result.intervals.length === 0) return
      const result = ineq.result
      const item1 = result.item1 || inequalityItems.value[ineq.func1Index]
      const item2 = result.item2 || inequalityItems.value[ineq.func2Index]
      if (!item1 || !item2) return

      result.intervals.forEach((iv, ivIdx) => {
        const left = iv.left === '-∞' ? xMin.value : Number(iv.left)
        const right = iv.right === '+∞' ? xMax.value : Number(iv.right)
        const numPts = 150
        const step = (right - left) / numPts
        
        const xVals = []
        const y1Vals = []
        const y2Vals = []
        
        for (let k = 0; k <= numPts; k++) {
          const xv = left + k * step
          const yv1 = evalShadingItem(item1, xv)
          const yv2 = evalShadingItem(item2, xv)
          if (isFinite(yv1) && isFinite(yv2)) {
            xVals.push(xv)
            y1Vals.push(yv1)
            y2Vals.push(yv2)
          }
        }
        
        if (xVals.length > 0) {
          traces.push({
            x: xVals.concat([...xVals].reverse()),
            y: y1Vals.concat([...y2Vals].reverse()),
            type: 'scatter',
            fill: 'toself',
            fillcolor: ineq.color,
            line: { color: 'rgba(0,0,0,0)', width: 0 },
            name: ivIdx === 0 ? `Zone solution ${ineqGlobalIdx + 1}` : '',
            showlegend: ivIdx === 0,
            hoverinfo: 'skip'
          })
        }
      })
    })
  }

  points.value.forEach((point) => {
    if (!point || point._temp || point.showProjections !== true) return

    const px = Number(point.x)
    const py = Number(point.y)
    if (!Number.isFinite(px) || !Number.isFinite(py)) return

    const helperColor = point.color || '#6b7280'

    traces.push({
      x: [px, px],
      y: [0, py],
      type: 'scatter',
      mode: 'lines',
      line: {
        color: helperColor,
        width: 1.5,
        dash: 'dot'
      },
      showlegend: false,
      hoverinfo: 'skip',
      meta: 'point-projection-helper'
    })

    traces.push({
      x: [0, px],
      y: [py, py],
      type: 'scatter',
      mode: 'lines',
      line: {
        color: helperColor,
        width: 1.5,
        dash: 'dot'
      },
      showlegend: false,
      hoverinfo: 'skip',
      meta: 'point-projection-helper'
    })

    traces.push({
      x: [px, 0],
      y: [0, py],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: '#ffffff',
        size: 7,
        line: { color: helperColor, width: 1.2 }
      },
      showlegend: false,
      hoverinfo: 'skip',
      meta: 'point-projection-helper'
    })
  })
  if (showClickProjections.value && clickedProjectionPoint.value) {
    const px = Number(clickedProjectionPoint.value.x)
    const py = Number(clickedProjectionPoint.value.y)
    if (Number.isFinite(px) && Number.isFinite(py)) {
      const helperColor = '#6b7280'

      traces.push({
        x: [px, px],
        y: [0, py],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: helperColor,
          width: 1.5,
          dash: 'dot'
        },
        showlegend: false,
        hoverinfo: 'skip',
        meta: 'click-projection-helper'
      })

      traces.push({
        x: [0, px],
        y: [py, py],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: helperColor,
          width: 1.5,
          dash: 'dot'
        },
        showlegend: false,
        hoverinfo: 'skip',
        meta: 'click-projection-helper'
      })

      traces.push({
        x: [px],
        y: [py],
        type: 'scatter',
        mode: 'markers',
        marker: {
          color: '#2563eb',
          size: 9,
          line: { color: '#1d4ed8', width: 1.2 }
        },
        showlegend: false,
        hoverinfo: 'skip',
        meta: 'click-projection-helper'
      })

      traces.push({
        x: [px, 0],
        y: [0, py],
        type: 'scatter',
        mode: 'markers',
        marker: {
          color: '#ffffff',
          size: 7,
          line: { color: helperColor, width: 1.2 }
        },
        showlegend: false,
        hoverinfo: 'skip',
        meta: 'click-projection-helper'
      })
    }
  }

  const centerAxesOnly = showAxes.value && showCenterAxesOnly.value
  const edgeTicksVisible = showTicks.value && !centerAxesOnly
  const edgeAxisTitlesVisible = showAxes.value && !centerAxesOnly
  const axisStrokeWidth = Math.min(10, Math.max(1, Number(axisLineWidth.value) || 2))

  const layout = {
    xaxis: {
      title: edgeAxisTitlesVisible ? {
        text: 'x',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      } : { text: '' },
      range: [xMin.value, xMax.value],
      gridcolor: '#e5e7eb',
      showgrid: showGrid.value,
      zerolinecolor: '#374151',
      zerolinewidth: showAxes.value ? axisStrokeWidth : 0,
      zeroline: showAxes.value,
      fixedrange: !allowPan.value || drawingMode.value !== 'none',
      showline: showAxes.value && !centerAxesOnly,
      linecolor: '#374151',
      linewidth: axisStrokeWidth,
      mirror: false,
      tickmode: 'linear',
      tick0: 0,
      dtick: 1,
      ticklabelstep: 2,
      tickfont: { size: mobileViewport ? 9 : 12 },
      showticklabels: edgeTicksVisible,
      ticks: edgeTicksVisible ? 'outside' : '',
      scaleanchor: 'y',
      scaleratio: 1,
      constrain: 'domain',
      constraintoward: 'center'
    },
    yaxis: {
      title: edgeAxisTitlesVisible ? {
        text: 'y',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      } : { text: '' },
      range: [yMin.value, yMax.value],
      gridcolor: '#e5e7eb',
      showgrid: showGrid.value,
      zerolinecolor: '#374151',
      zerolinewidth: showAxes.value ? axisStrokeWidth : 0,
      zeroline: showAxes.value,
      fixedrange: !allowPan.value || drawingMode.value !== 'none',
      showline: showAxes.value && !centerAxesOnly,
      linecolor: '#374151',
      linewidth: axisStrokeWidth,
      dtick: 1,
      mirror: false,
      tickmode: 'linear',
      tick0: 0,
      ticklabelstep: 2,
      tickfont: { size: mobileViewport ? 9 : 12 },
      showticklabels: edgeTicksVisible,
      ticks: edgeTicksVisible ? 'outside' : '',
      constrain: 'domain',
      constraintoward: 'center'
    },
    dragmode: (allowPan.value && drawingMode.value === 'none') ? 'pan' : false,
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
        arrowwidth: axisStrokeWidth,
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
        arrowwidth: axisStrokeWidth,
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
      tracegroupgap: 5,
      visible: showLegend.value
    }
  }
  
  // Ajouter les annotations interactives (labels déplaçables)
  const interactiveAnnotations = buildInteractiveAnnotations()
  const vectorAnnotations = shapes.getVectorAnnotations()
  layout.annotations = [...(layout.annotations || []), ...interactiveAnnotations, ...vectorAnnotations]

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    scrollZoom: allowPan.value,
    staticPlot: false,
    editable: false,
    edits: {
      annotationPosition: true,
      annotationTail: true
    },
    modeBarButtonsToRemove: [
      'zoomIn2d','zoomOut2d','autoScale2d','zoom2d',
      'pan2d','select2d','lasso2d','resetScale2d'
    ],
    toImageButtonOptions: {
      format: 'png',
      filename: 'graphique_optitab',
      scale: 5
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
      if (graphContainer.value._plotlyClickListener && graphContainer.value.removeListener) {
        graphContainer.value.removeListener('plotly_click', graphContainer.value._plotlyClickListener)
      }
      graphContainer.value._plotlyClickListener = handlePlotlyPointClick
      graphContainer.value.on('plotly_click', handlePlotlyPointClick)

      if (graphContainer.value._relayoutListener && graphContainer.value.removeListener) {
        graphContainer.value.removeListener('plotly_relayout', graphContainer.value._relayoutListener)
      }
      graphContainer.value._relayoutListener = handleAnnotationDrag
      
      // Écouter les événements de déplacement des annotations
      graphContainer.value.on('plotly_relayout', handleAnnotationDrag)
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

// === RÉSOLUTION D'INÉQUATIONS ===
function solveInequalityAt(ineqIndex) {
  const items = inequalityItems.value
  const ineq = inequalities.value[ineqIndex]
  if (!ineq) return
  
  if (items.length < 2) {
    ineq.result = null
    return
  }
  
  const item1 = items[ineq.func1Index]
  const item2 = items[ineq.func2Index]
  
  if (!item1 || !item2) {
    ineq.result = null
    return
  }
  
  const op = ineq.operator
  const name1 = item1.label
  const name2 = item2.label
  
  // Cache des conversions LaTeX -> JS pour éviter de re-parser à chaque évaluation
  const jsCache = {}
  function getCachedJS(func) {
    if (!func.latex) return null
    if (!jsCache[func.latex]) {
      jsCache[func.latex] = convertLatexToJS(func.latex)
    }
    return jsCache[func.latex]
  }
  
  // Helper: évaluer un item (fonction ou segment) en x
  function evalItem(item, x) {
    if (item.type === 'function') {
      const func = graphFunctions.value[item.index]
      if (!func) return NaN
      if (func.type === 'horizontal') return func.value
      if (func.type === 'vertical') return NaN
      return evaluateFunction(getCachedJS(func), x)
    } else if (item.type === 'segment') {
      const seg = segments.value[item.index]
      if (!seg) return NaN
      const minX = Math.min(seg.x1, seg.x2)
      const maxX = Math.max(seg.x1, seg.x2)
      if (x < minX - 1e-9 || x > maxX + 1e-9) return NaN
      if (Math.abs(seg.x2 - seg.x1) < 1e-10) return NaN
      const t = (x - seg.x1) / (seg.x2 - seg.x1)
      return seg.y1 + t * (seg.y2 - seg.y1)
    }
    return NaN
  }
  
  // Déterminer le domaine d'étude
  function getItemDomain(item) {
    if (item.type === 'function') {
      const func = graphFunctions.value[item.index]
      if (!func) return { left: xMin.value, right: xMax.value }
      if (func.type === 'horizontal') return { left: xMin.value, right: xMax.value }
      if (func.type === 'vertical') return { left: func.value, right: func.value }
      return { left: xMin.value, right: xMax.value }
    } else if (item.type === 'segment') {
      const seg = segments.value[item.index]
      if (!seg) return { left: xMin.value, right: xMax.value }
      return { left: Math.min(seg.x1, seg.x2), right: Math.max(seg.x1, seg.x2) }
    }
    return { left: xMin.value, right: xMax.value }
  }
  
  const domain1 = getItemDomain(item1)
  const domain2 = getItemDomain(item2)
  const domainLeft = Math.max(domain1.left, domain2.left)
  const domainRight = Math.min(domain1.right, domain2.right)
  const domainIsFinite = item1.type === 'segment' || item2.type === 'segment'
  
  if (domainLeft >= domainRight) {
    ineq.result = { display: '∅ (domaines disjoints)', intervals: [], item1, item2 }
    return
  }
  
  // Trouver les intersections
  const intersections = []
  
  if (item1.type === 'function' && item2.type === 'function') {
    const func1 = graphFunctions.value[item1.index]
    const func2 = graphFunctions.value[item2.index]
    const ints = findIntersections(func1, func2)
    intersections.push(...ints)
  } else if (item1.type === 'segment' && item2.type === 'segment') {
    const seg1 = segments.value[item1.index]
    const seg2 = segments.value[item2.index]
    const pt = findSegmentSegmentIntersection(seg1, seg2)
    if (pt) intersections.push(pt)
  } else {
    const segItem = item1.type === 'segment' ? item1 : item2
    const funcItem = item1.type === 'function' ? item1 : item2
    const seg = segments.value[segItem.index]
    const func = graphFunctions.value[funcItem.index]
    if (seg && func) {
      const ints = findSegmentFunctionIntersections(seg, func)
      intersections.push(...ints)
    }
  }
  
  const filteredIntersections = intersections.filter(p => 
    p.x >= domainLeft - 0.01 && p.x <= domainRight + 0.01
  )
  filteredIntersections.sort((a, b) => a.x - b.x)
  
  if (op === '=') {
    if (filteredIntersections.length === 0) {
      ineq.result = { display: '∅ (aucune solution)', intervals: [], item1, item2 }
    } else {
      const pts = filteredIntersections.map(p => {
        const xv = Math.abs(p.x) < 0.005 ? 0 : Number(p.x.toFixed(2))
        return `x = ${xv}`
      })
      ineq.result = { display: `S = { ${pts.join(' ; ')} }`, intervals: [], item1, item2 }
    }
    return
  }
  
  // --- Détecter les discontinuités (asymptotes, points non définis) ---
  const discontinuityXs = []
  {
    const scanN = 500
    const dx = (domainRight - domainLeft) / scanN
    let prevDiff = null
    let prevFinite = null
    
    for (let i = 0; i <= scanN; i++) {
      const x = domainLeft + i * dx
      const y1 = evalItem(item1, x)
      const y2 = evalItem(item2, x)
      const diff = y1 - y2
      const fin = isFinite(diff)
      
      if (i > 0) {
        const prevX = domainLeft + (i - 1) * dx
        const needRefine =
          (prevFinite && !fin) ||
          (!prevFinite && fin) ||
          (prevFinite && fin && prevDiff * diff < 0 && (Math.abs(prevDiff) + Math.abs(diff)) > 100)
        
        if (needRefine) {
          let lo = prevX, hi = x
          for (let j = 0; j < 40; j++) {
            const mid = (lo + hi) / 2
            const my1 = evalItem(item1, mid)
            const my2 = evalItem(item2, mid)
            const md = my1 - my2
            const mFin = isFinite(md) && Math.abs(md) < 1e12
            if (prevFinite && Math.abs(prevDiff) < 1e12) {
              if (mFin) lo = mid; else hi = mid
            } else {
              if (mFin) hi = mid; else lo = mid
            }
          }
          const discX = (lo + hi) / 2
          const tooClose = filteredIntersections.some(p => Math.abs(p.x - discX) < 0.1)
          if (!tooClose && discX > domainLeft + 0.001 && discX < domainRight - 0.001) {
            discontinuityXs.push(discX)
          }
        }
      }
      
      prevDiff = diff
      prevFinite = fin
    }
  }
  
  // Fusionner intersections et discontinuités en breakpoints tagués
  const allBreakpoints = filteredIntersections.map(p => ({ x: p.x, type: 'intersection' }))
  for (const dx of discontinuityXs) {
    if (!allBreakpoints.some(b => Math.abs(b.x - dx) < 0.05)) {
      allBreakpoints.push({ x: dx, type: 'discontinuity' })
    }
  }
  allBreakpoints.sort((a, b) => a.x - b.x)
  
  const bpXs = allBreakpoints.map(b => b.x)
  const testPoints = []
  
  if (bpXs.length > 0) {
    testPoints.push(Math.max(domainLeft, bpXs[0] - 0.5))
  } else {
    testPoints.push((domainLeft + domainRight) / 2)
  }
  
  for (let i = 0; i < bpXs.length - 1; i++) {
    testPoints.push((bpXs[i] + bpXs[i + 1]) / 2)
  }
  
  if (bpXs.length > 0) {
    testPoints.push(Math.min(domainRight, bpXs[bpXs.length - 1] + 0.5))
  }
  
  const satisfiedIntervals = []
  const strict = (op === '<' || op === '>')
  const wantLess = (op === '<' || op === '<=')
  
  testPoints.forEach((testX, i) => {
    const y1 = evalItem(item1, testX)
    const y2 = evalItem(item2, testX)
    if (!isFinite(y1) || !isFinite(y2)) return
    
    const diff = y1 - y2
    let satisfied = false
    if (wantLess) {
      satisfied = diff < -1e-9
    } else {
      satisfied = diff > 1e-9
    }
    
    if (satisfied) {
      let left, right, leftBracket, rightBracket
      
      if (i === 0 && bpXs.length > 0) {
        if (domainIsFinite) {
          left = Number(domainLeft.toFixed(2))
          leftBracket = '['
        } else {
          left = '-∞'
          leftBracket = ']'
        }
        right = Number(bpXs[0].toFixed(2))
        rightBracket = (strict || allBreakpoints[0].type === 'discontinuity') ? '[' : ']'
      } else if (i === 0 && bpXs.length === 0) {
        if (domainIsFinite) {
          left = Number(domainLeft.toFixed(2))
          leftBracket = '['
          right = Number(domainRight.toFixed(2))
          rightBracket = ']'
        } else {
          left = '-∞'
          leftBracket = ']'
          right = '+∞'
          rightBracket = '['
        }
      } else if (i === testPoints.length - 1) {
        left = Number(bpXs[bpXs.length - 1].toFixed(2))
        leftBracket = (strict || allBreakpoints[allBreakpoints.length - 1].type === 'discontinuity') ? ']' : '['
        if (domainIsFinite) {
          right = Number(domainRight.toFixed(2))
          rightBracket = ']'
        } else {
          right = '+∞'
          rightBracket = '['
        }
      } else {
        const leftBp = allBreakpoints[i - 1]
        const rightBp = allBreakpoints[i]
        left = Number(leftBp.x.toFixed(2))
        leftBracket = (strict || leftBp.type === 'discontinuity') ? ']' : '['
        right = Number(rightBp.x.toFixed(2))
        rightBracket = (strict || rightBp.type === 'discontinuity') ? '[' : ']'
      }
      
      satisfiedIntervals.push({ left, right, leftBracket, rightBracket })
    }
  })
  
  if (satisfiedIntervals.length === 0) {
    ineq.result = { display: '∅ (aucune solution)', intervals: satisfiedIntervals, item1, item2 }
  } else {
    const parts = satisfiedIntervals.map(iv => {
      return `${iv.leftBracket}${iv.left} ; ${iv.right}${iv.rightBracket}`
    })
    const opSymbol = op === '<' ? '&lt;' : op === '>' ? '&gt;' : op === '<=' ? '≤' : op === '>=' ? '≥' : '='
    ineq.result = {
      display: `${name1}(x) ${opSymbol} ${name2}(x) &nbsp;⟹&nbsp; S = ${parts.join(' ∪ ')}`,
      intervals: satisfiedIntervals,
      item1,
      item2
    }
  }
}

function solveAllInequalities() {
  inequalities.value.forEach((ineq, idx) => {
    solveInequalityAt(idx)
  })
  // Synchroniser avec l'ancien ref pour compatibilité
  if (inequalities.value.length > 0) {
    inequalityResult.value = inequalities.value[0].result
  }
}

function solveInequality() {
  solveAllInequalities()
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
          const key = getIntersectionKey(i + 1, j + 1, point.x, point.y)
          const customName = intersectionCustomNames.value[key] || ''
          const xCoord = Math.abs(point.x) < 0.01 ? 0 : Number(point.x.toFixed(2))
          const yCoord = Math.abs(point.y) < 0.01 ? 0 : Number(point.y.toFixed(2))
          const name1 = getFunctionDisplayName(func1, i)
          const name2 = getFunctionDisplayName(func2, j)
          const defaultName = `${name1} ∩ ${name2}`
          const displayName = customName || defaultName
          const ptColor = intersectionCustomColors.value[key] || '#dc2626'
          
          intersectionPoints.value.push({
            x: point.x,
            y: point.y,
            func1: func1.expression,
            func2: func2.expression,
            func1Index: i + 1,
            func2Index: j + 1,
            color1: func1.color,
            color2: func2.color,
            color: ptColor,
            name: displayName,
            key: key,
            defaultName: defaultName
          })
          
          traces.push({
            x: [point.x],
            y: [point.y],
            type: 'scatter',
            mode: 'markers',
            name: `${displayName}: (${xCoord}, ${yCoord})`,
            marker: {
              color: ptColor,
              size: 10,
              symbol: 'circle',
              line: {
                color: 'white',
                width: 2
              }
            },
            showlegend: true,
            legendgroup: 'intersections',
            hovertemplate: `<b>${displayName}</b><br>(${point.x.toFixed(3)}, ${point.y.toFixed(3)})<extra></extra>`
          })
        }
      })
    }
  }
  
  // Rendre les expressions LaTeX des intersections
  nextTick(() => renderIntersectionExpressions())
  
  // === Intersections SEGMENTS × FONCTIONS ===
  if (segments.value.length > 0) {
    segments.value.forEach((seg, sIdx) => {
      // Paramétrer le segment : S(t) = (x1 + t*(x2-x1), y1 + t*(y2-y1)), t ∈ [0,1]
      const dx = seg.x2 - seg.x1
      const dy = seg.y2 - seg.y1
      const segMinX = Math.min(seg.x1, seg.x2)
      const segMaxX = Math.max(seg.x1, seg.x2)
      const segMinY = Math.min(seg.y1, seg.y2)
      const segMaxY = Math.max(seg.y1, seg.y2)
      
      // Segment vs each graphFunction
      graphFunctions.value.forEach((func, fIdx) => {
        const pts = findSegmentFunctionIntersections(seg, func)
        pts.forEach(pt => {
          const isHidden = hiddenIntersections.value.some(h =>
            Math.abs(h.x - pt.x) < 0.01 && Math.abs(h.y - pt.y) < 0.01
          )
          if (!isHidden) {
            const segName = seg.name || (seg.isVector ? `V${sIdx+1}` : `S${sIdx+1}`)
            const funcName = getFunctionDisplayName(func, fIdx)
            const defaultName = `${segName} ∩ ${funcName}`
            const xCoord = Math.abs(pt.x) < 0.01 ? 0 : Number(pt.x.toFixed(2))
            const yCoord = Math.abs(pt.y) < 0.01 ? 0 : Number(pt.y.toFixed(2))
            
            const sfKey = `seg${sIdx}-func${fIdx}-${xCoord}`
            const sfColor = intersectionCustomColors.value[sfKey] || '#dc2626'
            const sfCustomName = intersectionCustomNames.value[sfKey] || ''
            const sfDisplayName = sfCustomName || defaultName
            intersectionPoints.value.push({
              x: pt.x, y: pt.y,
              func1: segName, func2: func.expression,
              func1Index: -1, func2Index: fIdx + 1,
              color1: seg.color, color2: func.color,
              color: sfColor,
              name: sfDisplayName, key: sfKey, defaultName
            })
            traces.push({
              x: [pt.x], y: [pt.y], type: 'scatter', mode: 'markers',
              name: `${sfDisplayName}: (${xCoord}, ${yCoord})`,
              marker: { color: sfColor, size: 10, symbol: 'circle', line: { color: 'white', width: 2 } },
              showlegend: true, legendgroup: 'intersections',
              hovertemplate: `<b>${defaultName}</b><br>(${pt.x.toFixed(3)}, ${pt.y.toFixed(3)})<extra></extra>`
            })
          }
        })
      })
      
      // Segment vs other segments
      for (let sIdx2 = sIdx + 1; sIdx2 < segments.value.length; sIdx2++) {
        const seg2 = segments.value[sIdx2]
        const pt = findSegmentSegmentIntersection(seg, seg2)
        if (pt) {
          const isHidden = hiddenIntersections.value.some(h =>
            Math.abs(h.x - pt.x) < 0.01 && Math.abs(h.y - pt.y) < 0.01
          )
          if (!isHidden) {
            const name1 = seg.name || (seg.isVector ? `V${sIdx+1}` : `S${sIdx+1}`)
            const name2 = seg2.name || (seg2.isVector ? `V${sIdx2+1}` : `S${sIdx2+1}`)
            const defaultName = `${name1} ∩ ${name2}`
            const xCoord = Math.abs(pt.x) < 0.01 ? 0 : Number(pt.x.toFixed(2))
            const yCoord = Math.abs(pt.y) < 0.01 ? 0 : Number(pt.y.toFixed(2))
            const ssKey = `seg${sIdx}-seg${sIdx2}`
            const ssColor = intersectionCustomColors.value[ssKey] || '#dc2626'
            const ssCustomName = intersectionCustomNames.value[ssKey] || ''
            const ssDisplayName = ssCustomName || defaultName
            intersectionPoints.value.push({
              x: pt.x, y: pt.y,
              func1: name1, func2: name2,
              func1Index: -1, func2Index: -1,
              color1: seg.color, color2: seg2.color,
              color: ssColor,
              name: ssDisplayName, key: ssKey, defaultName
            })
            traces.push({
              x: [pt.x], y: [pt.y], type: 'scatter', mode: 'markers',
              name: `${ssDisplayName}: (${xCoord}, ${yCoord})`,
              marker: { color: ssColor, size: 10, symbol: 'circle', line: { color: 'white', width: 2 } },
              showlegend: true, legendgroup: 'intersections',
              hovertemplate: `<b>${defaultName}</b><br>(${pt.x.toFixed(3)}, ${pt.y.toFixed(3)})<extra></extra>`
            })
          }
        }
      }
    })
  }
  
  // === Intersections CERCLES × FONCTIONS ===
  if (circles.value.length > 0) {
    circles.value.forEach((circ, cIdx) => {
      graphFunctions.value.forEach((func, fIdx) => {
        const pts = findCircleFunctionIntersections(circ, func)
        pts.forEach(pt => {
          const isHidden = hiddenIntersections.value.some(h =>
            Math.abs(h.x - pt.x) < 0.01 && Math.abs(h.y - pt.y) < 0.01
          )
          if (!isHidden) {
            const circName = circ.name || `C${cIdx+1}`
            const funcName = getFunctionDisplayName(func, fIdx)
            const defaultName = `${circName} ∩ ${funcName}`
            const xCoord = Math.abs(pt.x) < 0.01 ? 0 : Number(pt.x.toFixed(2))
            const yCoord = Math.abs(pt.y) < 0.01 ? 0 : Number(pt.y.toFixed(2))
            const cfKey = `circ${cIdx}-func${fIdx}-${xCoord}`
            const cfColor = intersectionCustomColors.value[cfKey] || '#dc2626'
            const cfCustomName = intersectionCustomNames.value[cfKey] || ''
            const cfDisplayName = cfCustomName || defaultName
            intersectionPoints.value.push({
              x: pt.x, y: pt.y,
              func1: circName, func2: func.expression,
              func1Index: -1, func2Index: fIdx + 1,
              color1: circ.color, color2: func.color,
              color: cfColor,
              name: cfDisplayName, key: cfKey, defaultName
            })
            traces.push({
              x: [pt.x], y: [pt.y], type: 'scatter', mode: 'markers',
              name: `${cfDisplayName}: (${xCoord}, ${yCoord})`,
              marker: { color: cfColor, size: 10, symbol: 'circle', line: { color: 'white', width: 2 } },
              showlegend: true, legendgroup: 'intersections',
              hovertemplate: `<b>${defaultName}</b><br>(${pt.x.toFixed(3)}, ${pt.y.toFixed(3)})<extra></extra>`
            })
          }
        })
      })
      
      // Cercle vs segments
      segments.value.forEach((seg, sIdx) => {
        const pts = findCircleSegmentIntersections(circ, seg)
        pts.forEach(pt => {
          const isHidden = hiddenIntersections.value.some(h =>
            Math.abs(h.x - pt.x) < 0.01 && Math.abs(h.y - pt.y) < 0.01
          )
          if (!isHidden) {
            const circName = circ.name || `C${cIdx+1}`
            const segName = seg.name || (seg.isVector ? `V${sIdx+1}` : `S${sIdx+1}`)
            const defaultName = `${circName} ∩ ${segName}`
            const xCoord = Math.abs(pt.x) < 0.01 ? 0 : Number(pt.x.toFixed(2))
            const yCoord = Math.abs(pt.y) < 0.01 ? 0 : Number(pt.y.toFixed(2))
            const csKey = `circ${cIdx}-seg${sIdx}-${xCoord}`
            const csColor = intersectionCustomColors.value[csKey] || '#dc2626'
            const csCustomName = intersectionCustomNames.value[csKey] || ''
            const csDisplayName = csCustomName || defaultName
            intersectionPoints.value.push({
              x: pt.x, y: pt.y,
              func1: circName, func2: segName,
              func1Index: -1, func2Index: -1,
              color1: circ.color, color2: seg.color,
              color: csColor,
              name: csDisplayName, key: csKey, defaultName
            })
            traces.push({
              x: [pt.x], y: [pt.y], type: 'scatter', mode: 'markers',
              name: `${csDisplayName}: (${xCoord}, ${yCoord})`,
              marker: { color: csColor, size: 10, symbol: 'circle', line: { color: 'white', width: 2 } },
              showlegend: true, legendgroup: 'intersections',
              hovertemplate: `<b>${defaultName}</b><br>(${pt.x.toFixed(3)}, ${pt.y.toFixed(3)})<extra></extra>`
            })
          }
        })
      })
    })
  }
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

// === INTERSECTIONS: Segment × Fonction ===
function findSegmentFunctionIntersections(seg, func) {
  const intersections = []
  const segMinX = Math.min(seg.x1, seg.x2)
  const segMaxX = Math.max(seg.x1, seg.x2)
  const segMinY = Math.min(seg.y1, seg.y2)
  const segMaxY = Math.max(seg.y1, seg.y2)
  const dx = seg.x2 - seg.x1
  const dy = seg.y2 - seg.y1
  
  // Segment vertical (x constant)
  if (Math.abs(dx) < 1e-10) {
    const xSeg = seg.x1
    if (func.type === 'function') {
      const js = convertLatexToJS(func.latex)
      const yVal = evaluateFunction(js, xSeg)
      if (isFinite(yVal) && yVal >= segMinY && yVal <= segMaxY) {
        intersections.push({ x: xSeg, y: yVal })
      }
    } else if (func.type === 'horizontal') {
      if (func.value >= segMinY && func.value <= segMaxY) {
        intersections.push({ x: xSeg, y: func.value })
      }
    }
    // vertical segment vs vertical line => infinite or none, skip
    return intersections
  }
  
  // Segment horizontal
  if (Math.abs(dy) < 1e-10) {
    const ySeg = seg.y1
    if (func.type === 'function') {
      // Find where f(x) = ySeg within [segMinX, segMaxX]
      const js = convertLatexToJS(func.latex)
      const numSamples = 200
      const step = (segMaxX - segMinX) / numSamples
      for (let i = 0; i < numSamples; i++) {
        const x1 = segMinX + i * step
        const x2 = segMinX + (i + 1) * step
        const d1 = evaluateFunction(js, x1) - ySeg
        const d2 = evaluateFunction(js, x2) - ySeg
        if (isFinite(d1) && isFinite(d2) && d1 * d2 <= 0 && Math.abs(d1) < 100 && Math.abs(d2) < 100) {
          const xInt = findZeroForHorizontal(js, ySeg, x1, x2)
          if (xInt !== null && xInt >= segMinX && xInt <= segMaxX) {
            const isDup = intersections.some(p => Math.abs(p.x - xInt) < 0.05)
            if (!isDup) intersections.push({ x: xInt, y: ySeg })
          }
        }
      }
    } else if (func.type === 'horizontal') {
      // Two horizontal lines — parallel or same
      if (Math.abs(func.value - ySeg) < 1e-6) {
        // Same line — infinite intersections, skip
      }
    } else if (func.type === 'vertical') {
      if (func.value >= segMinX && func.value <= segMaxX) {
        intersections.push({ x: func.value, y: ySeg })
      }
    }
    return intersections
  }
  
  // General segment (oblique) — parametric: segY(x) = y1 + (x - x1) * dy / dx for x in [segMinX, segMaxX]
  if (func.type === 'vertical') {
    const xV = func.value
    if (xV >= segMinX && xV <= segMaxX) {
      const t = (xV - seg.x1) / dx
      if (t >= -0.001 && t <= 1.001) {
        const yV = seg.y1 + t * dy
        intersections.push({ x: xV, y: yV })
      }
    }
    return intersections
  }
  
  if (func.type === 'horizontal') {
    const yH = func.value
    const t = (yH - seg.y1) / dy
    if (t >= -0.001 && t <= 1.001) {
      const xH = seg.x1 + t * dx
      if (xH >= segMinX - 0.001 && xH <= segMaxX + 0.001) {
        intersections.push({ x: xH, y: yH })
      }
    }
    return intersections
  }
  
  // func.type === 'function'
  const js = convertLatexToJS(func.latex)
  const numSamples = 200
  const step = (segMaxX - segMinX) / numSamples
  if (step <= 0) return intersections
  
  for (let i = 0; i < numSamples; i++) {
    const x1 = segMinX + i * step
    const x2 = segMinX + (i + 1) * step
    // segY at x
    const segY1 = seg.y1 + ((x1 - seg.x1) / dx) * dy
    const segY2 = seg.y1 + ((x2 - seg.x1) / dx) * dy
    const fY1 = evaluateFunction(js, x1)
    const fY2 = evaluateFunction(js, x2)
    
    if (isFinite(segY1) && isFinite(segY2) && isFinite(fY1) && isFinite(fY2)) {
      const d1 = segY1 - fY1
      const d2 = segY2 - fY2
      if (d1 * d2 <= 0 && Math.abs(d1) < 100 && Math.abs(d2) < 100) {
        // Bisect to find precise x
        let lo = x1, hi = x2
        for (let iter = 0; iter < 30; iter++) {
          const mid = (lo + hi) / 2
          const segYm = seg.y1 + ((mid - seg.x1) / dx) * dy
          const fYm = evaluateFunction(js, mid)
          if (!isFinite(fYm)) break
          const dm = segYm - fYm
          if (Math.abs(dm) < 1e-8) { lo = hi = mid; break }
          if (d1 * dm < 0) hi = mid; else lo = mid
        }
        const xInt = (lo + hi) / 2
        const yInt = evaluateFunction(js, xInt)
        if (isFinite(yInt)) {
          const isDup = intersections.some(p => Math.abs(p.x - xInt) < 0.05)
          if (!isDup) intersections.push({ x: xInt, y: yInt })
        }
      }
    }
  }
  return intersections
}

// === INTERSECTIONS: Segment × Segment ===
function findSegmentSegmentIntersection(seg1, seg2) {
  const x1 = seg1.x1, y1 = seg1.y1, x2 = seg1.x2, y2 = seg1.y2
  const x3 = seg2.x1, y3 = seg2.y1, x4 = seg2.x2, y4 = seg2.y2
  
  const denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
  if (Math.abs(denom) < 1e-10) return null // parallel
  
  const t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
  const u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
  
  if (t >= -0.001 && t <= 1.001 && u >= -0.001 && u <= 1.001) {
    return { x: x1 + t * (x2 - x1), y: y1 + t * (y2 - y1) }
  }
  return null
}

// === INTERSECTIONS: Cercle × Fonction ===
function findCircleFunctionIntersections(circ, func) {
  const intersections = []
  const { h, k, r } = circ
  
  if (func.type === 'vertical') {
    const xV = func.value
    const dx = xV - h
    if (Math.abs(dx) <= r) {
      const dy = Math.sqrt(r * r - dx * dx)
      intersections.push({ x: xV, y: k + dy })
      if (dy > 1e-8) intersections.push({ x: xV, y: k - dy })
    }
    return intersections
  }
  
  if (func.type === 'horizontal') {
    const yH = func.value
    const dy = yH - k
    if (Math.abs(dy) <= r) {
      const dx = Math.sqrt(r * r - dy * dy)
      intersections.push({ x: h + dx, y: yH })
      if (dx > 1e-8) intersections.push({ x: h - dx, y: yH })
    }
    return intersections
  }
  
  // func.type === 'function': sample x in [h-r, h+r], compare f(x) with circle top/bottom
  const js = convertLatexToJS(func.latex)
  const numSamples = 500
  const xStart = h - r - 0.5
  const xEnd = h + r + 0.5
  const step = (xEnd - xStart) / numSamples
  
  for (let i = 0; i < numSamples; i++) {
    const x1 = xStart + i * step
    const x2 = xStart + (i + 1) * step
    const fY1 = evaluateFunction(js, x1)
    const fY2 = evaluateFunction(js, x2)
    if (!isFinite(fY1) || !isFinite(fY2)) continue
    
    // Circle: (x-h)^2 + (y-k)^2 = r^2 → distance from (x, f(x)) to center
    const distSq1 = (x1 - h) * (x1 - h) + (fY1 - k) * (fY1 - k)
    const distSq2 = (x2 - h) * (x2 - h) + (fY2 - k) * (fY2 - k)
    const r2 = r * r
    const d1 = distSq1 - r2
    const d2 = distSq2 - r2
    
    if (d1 * d2 <= 0) {
      // Bisect for precise crossing
      let lo = x1, hi = x2
      for (let iter = 0; iter < 50; iter++) {
        const mid = (lo + hi) / 2
        const fYm = evaluateFunction(js, mid)
        if (!isFinite(fYm)) break
        const distSqM = (mid - h) * (mid - h) + (fYm - k) * (fYm - k)
        const dm = distSqM - r2
        if (Math.abs(dm) < 1e-10) { lo = hi = mid; break }
        if (d1 * dm < 0) hi = mid; else lo = mid
      }
      const xInt = (lo + hi) / 2
      const yInt = evaluateFunction(js, xInt)
      if (isFinite(yInt)) {
        const isDup = intersections.some(p => Math.abs(p.x - xInt) < 0.05 && Math.abs(p.y - yInt) < 0.05)
        if (!isDup) intersections.push({ x: xInt, y: yInt })
      }
    }
  }
  return intersections
}

// === INTERSECTIONS: Cercle × Segment ===
function findCircleSegmentIntersections(circ, seg) {
  const intersections = []
  const { h, k, r } = circ
  const dx = seg.x2 - seg.x1
  const dy = seg.y2 - seg.y1
  
  // Parametric: P(t) = (x1 + t*dx, y1 + t*dy), t ∈ [0,1]
  // (x1 + t*dx - h)^2 + (y1 + t*dy - k)^2 = r^2
  const fx = seg.x1 - h
  const fy = seg.y1 - k
  const a = dx * dx + dy * dy
  const b = 2 * (fx * dx + fy * dy)
  const c = fx * fx + fy * fy - r * r
  
  let discriminant = b * b - 4 * a * c
  if (discriminant < 0) return intersections
  
  discriminant = Math.sqrt(discriminant)
  const t1 = (-b - discriminant) / (2 * a)
  const t2 = (-b + discriminant) / (2 * a)
  
  for (const t of [t1, t2]) {
    if (t >= -0.001 && t <= 1.001) {
      const x = seg.x1 + t * dx
      const y = seg.y1 + t * dy
      const isDup = intersections.some(p => Math.abs(p.x - x) < 0.01 && Math.abs(p.y - y) < 0.01)
      if (!isDup) intersections.push({ x, y })
    }
  }
  return intersections
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
        const axisKey = getAxisIntersectionKey(index + 1, 'x', xValue, 0)
        const axisCustomName = axisIntersectionCustomNames.value[axisKey] || ''
        const funcName = getFunctionDisplayName(func, index)
        const defaultAxisName = `${funcName} ∩ axe X`
        const axisDisplayName = axisCustomName || defaultAxisName
        
        axisIntersectionPoints.value.push({
          x: xValue,
          y: 0,
          funcIndex: index + 1,
          axis: 'x',
          name: axisDisplayName,
          key: axisKey,
          defaultName: defaultAxisName
        })
        
        // Ajouter un marqueur sur le graphique
        const xCoord = Math.abs(xValue) < 0.01 ? 0 : Number(xValue.toFixed(2))
        traces.push({
          x: [xValue],
          y: [0],
          type: 'scatter',
          mode: 'markers',
          name: `${axisDisplayName}: (${xCoord}, 0)`,
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
          hovertemplate: `<b>${axisDisplayName}</b><br>(${xValue.toFixed(3)}, 0)<extra></extra>`
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
        const axisKeyY = getAxisIntersectionKey(index + 1, 'y', 0, yValue)
        const axisCustomNameY = axisIntersectionCustomNames.value[axisKeyY] || ''
        const funcName = getFunctionDisplayName(func, index)
        const defaultAxisNameY = `${funcName} ∩ axe Y`
        const axisDisplayNameY = axisCustomNameY || defaultAxisNameY
        
        axisIntersectionPoints.value.push({
          x: 0,
          y: yValue,
          funcIndex: index + 1,
          axis: 'y',
          name: axisDisplayNameY,
          key: axisKeyY,
          defaultName: defaultAxisNameY
        })
        
        // Ajouter un marqueur sur le graphique
        const yCoord = Math.abs(yValue) < 0.01 ? 0 : Number(yValue.toFixed(2))
        traces.push({
          x: [0],
          y: [yValue],
          type: 'scatter',
          mode: 'markers',
          name: `${axisDisplayNameY}: (0, ${yCoord})`,
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
          hovertemplate: `<b>${axisDisplayNameY}</b><br>(0, ${yValue.toFixed(3)})<extra></extra>`
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

function addMultiplePoints() {
  shapes.addMultiplePoints(plotAllFunctions)
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

function addDroite() {
  const color = shapes.getNextColor()
  let m, b, px, py, name

  if (droiteMode.value === '2points') {
    if (points.value.length < 2) return
    const p1 = points.value[droitePoint1Index.value]
    const p2 = points.value[droitePoint2Index.value]
    if (!p1 || !p2 || droitePoint1Index.value === droitePoint2Index.value) return

    if (p1.x === p2.x) {
      // Droite verticale
      graphFunctions.value.push({
        name: `(${p1.name}${p2.name})`,
        expression: `x = ${p1.x}`,
        color: color,
        latex: `x = ${p1.x}`,
        type: 'vertical',
        value: p1.x,
        showInLegend: true,
        lineDash: 'solid',
        lineWidth: 2
      })
      plotAllFunctions()
      nextTick(() => renderFunctionExpressions())
      return
    }
    m = (p2.y - p1.y) / (p2.x - p1.x)
    b = p1.y - m * p1.x
    name = `(${p1.name}${p2.name})`
  } else if (droiteMode.value === 'pointSlope') {
    if (points.value.length < 1) return
    const p = points.value[droitePointIndex.value]
    if (!p) return
    m = droiteSlope.value
    b = p.y - m * p.x
    name = `d(${p.name})`
  } else if (droiteMode.value === 'pointVector') {
    if (points.value.length < 1) return
    const p = points.value[droitePointIndex.value]
    if (!p) return
    const dx = droiteVecX.value
    const dy = droiteVecY.value
    if (dx === 0 && dy === 0) return

    if (dx === 0) {
      // Vecteur vertical → droite verticale
      graphFunctions.value.push({
        name: `d(${p.name})`,
        expression: `x = ${p.x}`,
        color: color,
        latex: `x = ${p.x}`,
        type: 'vertical',
        value: p.x,
        showInLegend: true,
        lineDash: 'solid',
        lineWidth: 2
      })
      plotAllFunctions()
      nextTick(() => renderFunctionExpressions())
      return
    }
    m = dy / dx
    b = p.y - m * p.x
    name = `d(${p.name})`
  }

  // Arrondir pour éviter les flottants trop longs
  const mRound = Math.round(m * 10000) / 10000
  const bRound = Math.round(b * 10000) / 10000

  const expr = bRound >= 0 ? `${mRound}*x+${bRound}` : `${mRound}*x${bRound}`
  const displayExpr = bRound >= 0 ? `${mRound}x + ${bRound}` : `${mRound}x - ${Math.abs(bRound)}`

  graphFunctions.value.push({
    name: name,
    expression: displayExpr,
    color: color,
    latex: expr,
    type: 'function',
    value: null,
    showInLegend: true,
    lineDash: 'solid',
    lineWidth: 2
  })
  plotAllFunctions()
  nextTick(() => renderFunctionExpressions())
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
  plotAllFunctions()
  nextTick(() => renderFunctionExpressions())
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

// Ajouter un point d'intersection comme point utilisateur
function addIntersectionAsPoint(x, y, suggestedName) {
  const roundedX = Math.round(x * 1000) / 1000
  const roundedY = Math.round(y * 1000) / 1000
  // Vérifier si un point existe déjà à ces coordonnées
  const exists = points.value.find(p => Math.abs(p.x - roundedX) < 0.001 && Math.abs(p.y - roundedY) < 0.001)
  if (exists) return
  const color = shapes.getNextColor()
  const name = suggestedName || `P${points.value.length + 1}`
  points.value.push({
    x: roundedX,
    y: roundedY,
    color: color,
    name: name,
    showName: true,
    showCoords: true
  })
  plotAllFunctions()
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
      const funcName = getFunctionDisplayName(func, index)
      traces.push({
        x: [xRoot],
        y: [0],
        type: 'scatter',
        mode: 'markers',
        name: `Racine ${funcName}: x = ${xCoord}`,
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
        hovertemplate: `<b>Racine de ${funcName}</b><br>x = ${xRoot.toFixed(3)}<br>${funcName}(x) = 0<extra></extra>`
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
    // Rendre les noms de fonctions avec KaTeX
    renderFunctionNameLabels()
  })
}

async function clearGraph() {
  graphFunctions.value = []
  textAnnotations.value = []
  annotationPositions.value = {}
  intersectionCustomNames.value = {}
  intersectionCustomColors.value = {}
  axisIntersectionCustomNames.value = {}
  hiddenIntersections.value = []
  hiddenAxisIntersections.value = []
  clickedProjectionPoint.value = null
  // Reset inéquations
  inequalities.value = [{ func1Index: 0, func2Index: 1, operator: '<', result: null, color: INEQUALITY_COLORS[0] }]
  inequalityResult.value = null
  showInequality.value = false
  shapes.clearAllShapes()
  if (preview.value) {
    preview.value.innerHTML = ''
  }
  // Retracer un graphique vide
  await plotAllFunctions()
}

async function resetZoom() {
  if (graphContainer.value && Plotly) {
    Plotly.relayout(graphContainer.value, {
      'xaxis.range': [xMin.value, xMax.value],
      'yaxis.range': [yMin.value, yMax.value]
    })
  }
}

function zoomIn() {
  if (!graphContainer.value || !Plotly) return
  const layout = graphContainer.value._fullLayout
  if (!layout) return
  const xRange = layout.xaxis.range
  const yRange = layout.yaxis.range
  const xCenter = (xRange[0] + xRange[1]) / 2
  const yCenter = (yRange[0] + yRange[1]) / 2
  const xHalf = (xRange[1] - xRange[0]) / 2 * 0.7
  const yHalf = (yRange[1] - yRange[0]) / 2 * 0.7
  Plotly.relayout(graphContainer.value, {
    'xaxis.range': [xCenter - xHalf, xCenter + xHalf],
    'yaxis.range': [yCenter - yHalf, yCenter + yHalf]
  })
}

function zoomOut() {
  if (!graphContainer.value || !Plotly) return
  const layout = graphContainer.value._fullLayout
  if (!layout) return
  const xRange = layout.xaxis.range
  const yRange = layout.yaxis.range
  const xCenter = (xRange[0] + xRange[1]) / 2
  const yCenter = (yRange[0] + yRange[1]) / 2
  const xHalf = (xRange[1] - xRange[0]) / 2 * 1.4
  const yHalf = (yRange[1] - yRange[0]) / 2 * 1.4
  Plotly.relayout(graphContainer.value, {
    'xaxis.range': [xCenter - xHalf, xCenter + xHalf],
    'yaxis.range': [yCenter - yHalf, yCenter + yHalf]
  })
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

.add-point-from-intersection-btn {
  width: 1.5rem;
  height: 1.5rem;
  border: none;
  background: #10b981;
  color: white;
  border-radius: 50%;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 1;
}

.add-point-from-intersection-btn:hover {
  background: #059669;
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

/* === DESKTOP SIDE-BY-SIDE LAYOUT === */
/* Layout flex : graphique à gauche, onglets à droite */
.graph-layout {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
  align-items: flex-start;
}

.graph-main-area {
  flex: 1;
  min-width: 0;
}

/* Panneau latéral desktop */
.graph-side-panel.desktop-only-panel {
  width: 380px;
  min-width: 320px;
  max-width: 420px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #fafbfc;
  overflow: hidden;
  max-height: 80vh;
}

/* En-tête du panneau latéral */
.side-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
  border-bottom: 1px solid #e2e8f0;
}

.side-panel-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: white;
}

/* Grille de cartes dans le panneau latéral */
.side-panel-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.side-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.6rem 0.4rem;
  background: white;
  border: 1.5px solid #e5e7eb;
  border-radius: 0.6rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.side-card:hover {
  border-color: #93c5fd;
  background: #f0f7ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.side-card.active {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.side-card-icon {
  font-size: 1.3rem;
  line-height: 1;
}

.side-card-label {
  font-size: 0.72rem;
  font-weight: 600;
  color: #475569;
  line-height: 1.1;
}

.side-card.active .side-card-label {
  color: #1e3a8a;
}

/* Bouton masquer/afficher le panneau */
.toggle-panel-btn {
  padding: 0.5rem 0.85rem;
  background: #f0f7ff;
  border: 1px solid #bfdbfe;
  border-radius: 0.375rem;
  color: #1e3a8a;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.toggle-panel-btn:hover {
  background: #dbeafe;
  border-color: #93c5fd;
}

.side-panel-content {
  flex: 1;
  overflow-y: auto;
  background: white;
}

.side-panel-content .tab-panel {
  padding: 1rem;
}

.side-panel-content .panel-title {
  font-size: 1rem;
  margin-bottom: 0.75rem;
}

.side-panel-content .bounds-row {
  gap: 0.5rem;
}

.side-panel-content .bound-field {
  font-size: 0.85rem;
  padding: 0.35rem 0.5rem;
}

.side-panel-content .checkbox-label {
  font-size: 0.85rem;
}

.side-panel-content .shape-section {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
}

.side-panel-content .shape-title {
  font-size: 0.9rem;
}

.side-panel-content .action-btn {
  padding: 0.4rem 0.75rem;
  font-size: 0.82rem;
}

/* Masquer les onglets du haut sur desktop (garder uniquement le panneau latéral) */
.mobile-only-tabs {
  display: none;
}

/* Tablettes : panneau latéral plus compact */
@media (min-width: 769px) and (max-width: 1100px) {
  .graph-side-panel.desktop-only-panel {
    width: 300px;
    min-width: 260px;
    max-width: 320px;
  }
  
  .side-panel-cards {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.35rem;
    padding: 0.5rem;
  }
  
  .side-card {
    padding: 0.45rem 0.3rem;
  }
  
  .side-card-icon {
    font-size: 1.1rem;
  }
  
  .side-card-label {
    font-size: 0.65rem;
  }
  
  .side-panel-content .tab-panel {
    padding: 0.75rem;
  }
  
  .graph-layout {
    gap: 1rem;
  }
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
.reset-zoom-btn,
.zoom-btn {
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

.zoom-btn:hover {
  background: #f0fdf4;
  border-color: #bbf7d0;
  color: #16a34a;
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

/* Barre d'outils de dessin */
.drawing-toolbar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.drawing-toolbar-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-right: 0.25rem;
}

.drawing-tool-btn {
  padding: 0.35rem 0.75rem;
  background: white;
  border: 1.5px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 0.82rem;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s ease;
}

.drawing-tool-btn:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.drawing-tool-btn.active {
  background: #1e3a8a;
  border-color: #1e3a8a;
  color: white;
  box-shadow: 0 1px 3px rgba(30, 58, 138, 0.3);
}

.drawing-tool-btn.cancel-btn {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.drawing-tool-btn.cancel-btn:hover {
  background: #fee2e2;
  border-color: #f87171;
}

.drawing-hint {
  font-size: 0.8rem;
  color: #1e3a8a;
  font-style: italic;
  margin-left: 0.5rem;
}

.graph-container {
  width: 100%;
  aspect-ratio: 4 / 3;
  min-height: 450px;
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

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  font-size: 0.82rem;
  color: #374151;
  font-weight: 500;
}

.radio-label input[type="radio"] {
  width: 0.9rem;
  height: 0.9rem;
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

.inequality-result {
  background: #f0fdf4;
  border-color: #86efac;
  font-size: 0.95rem;
  line-height: 1.6;
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

.function-item-2rows {
  flex-direction: column;
  align-items: stretch;
  gap: 0.35rem;
}

.function-item-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.function-item-toggles {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding-left: 0.25rem;
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

.function-name-label {
  cursor: pointer;
}

.function-name-input {
  width: 6ch;
  padding: 0.15rem 0.35rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: #1e3a8a;
  background: #ffffff;
}

.function-name-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

.function-name-suffix {
  margin-left: 0.15rem;
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

/* Traced shapes in Fonctions tab */
.traced-shapes-section {
  margin-top: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e5e7eb;
}

.traced-shapes-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 0.4rem 0;
}

.shape-item-name {
  font-weight: 600;
  font-size: 0.85rem;
  color: #1e3a8a;
}

.shape-name-clickable {
  cursor: pointer;
  border-bottom: 1px dashed transparent;
  transition: all 0.2s ease;
}

.shape-name-clickable:hover {
  border-bottom-color: #3b82f6;
  color: #2563eb;
}

.shape-name-input {
  width: 8ch;
  padding: 0.15rem 0.35rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.85rem;
  color: #1e3a8a;
  background: #ffffff;
}

.shape-name-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
}

.shape-item-coords {
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #6b7280;
  margin-left: 0.25rem;
}

/* Point with toggle buttons layout */
.shape-item-with-toggles,
.function-item-with-toggles {
  flex-direction: column !important;
  align-items: stretch !important;
  gap: 4px !important;
}
.shape-item-main {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.shape-item-toggles {
  display: flex;
  gap: 6px;
  padding-left: 28px;
}
.point-toggle-btn {
  padding: 2px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  background: #f1f5f9;
  color: #94a3b8;
}
.point-toggle-btn.active {
  background: #dbeafe;
  color: #1e40af;
  border-color: #93c5fd;
}
.point-toggle-btn:hover {
  background: #e0e7ff;
}
.legend-toggle-btn {
  padding: 2px 6px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.68rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  background: #f1f5f9;
  color: #94a3b8;
  flex-shrink: 0;
  margin-left: 2px;
}
.legend-toggle-btn.active {
  background: #dbeafe;
  color: #1e40af;
  border-color: #93c5fd;
}
.legend-toggle-btn:hover {
  background: #e0e7ff;
}

.line-style-select,
.line-width-select {
  padding: 1px 2px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.68rem;
  cursor: pointer;
  background: #f8fafc;
  color: #475569;
  flex-shrink: 0;
  margin-left: 2px;
  height: 22px;
}
.line-style-select {
  width: 52px;
}
.line-width-select {
  width: 36px;
}
.line-style-select:hover,
.line-width-select:hover {
  border-color: #93c5fd;
  background: #eff6ff;
}

.connect-points-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.4rem 0.5rem;
  background: #f0f4ff;
  border-radius: 0.375rem;
}

.connect-points-toggle {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
  font-weight: 500;
  color: #1e3a8a;
  cursor: pointer;
  user-select: none;
}

.connect-points-toggle input[type="checkbox"] {
  accent-color: #3b82f6;
  width: 15px;
  height: 15px;
  cursor: pointer;
}

/* Responsive pour le graphique */
@media (max-width: 768px) {
  /* === MOBILE: afficher les onglets du haut, masquer le panneau latéral === */
  .mobile-only-tabs {
    display: block !important;
  }
  
  .graph-side-panel.desktop-only-panel {
    display: none !important;
  }
  
  .toggle-panel-btn.desktop-only-panel {
    display: none !important;
  }
  
  .graph-layout {
    flex-direction: column;
  }
  
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

/* ═══ Lien aide ═══ */
.graph-help-link-row {
  text-align: center;
  padding: 16px 0;
}
.graph-help-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 22px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #3b82f6;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
  transition: all 0.2s;
}
.graph-help-link:hover {
  background: #eff6ff;
  border-color: #93c5fd;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}
</style> 






