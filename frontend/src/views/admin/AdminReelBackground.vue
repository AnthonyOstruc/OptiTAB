<template>
  <div class="reel-bg-admin">

    <!-- Layout: Preview centré + Sidebar droite fixe -->
    <div class="main-layout">

      <!-- Zone centrale: Preview -->
      <div class="preview-column">
        <div class="preview-wrapper">
          <div class="preview-label">Aperçu {{ canvasWidth }}×{{ canvasHeight }}</div>
          <div class="preview-container" ref="previewContainer" :style="{ width: previewScale + 'px', height: Math.round(previewScale * canvasHeight / canvasWidth) + 'px' }">
            <div
              ref="reelCanvas"
              class="reel-canvas"
              :style="canvasStyleWithTransform"
            >
              <!-- Image de fond personnalisée -->
              <div v-if="bgImageUrl" class="bg-image-layer" :style="bgImageStyle"></div>

          <!-- Grille mathématique -->
          <svg class="grid-layer" :width="canvasWidth" :height="canvasHeight" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="smallGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" :stroke="gridColor" :stroke-width="0.5" :stroke-opacity="gridOpacity" />
              </pattern>
              <pattern id="bigGrid" width="200" height="200" patternUnits="userSpaceOnUse">
                <rect width="200" height="200" fill="url(#smallGrid)" />
                <path d="M 200 0 L 0 0 0 200" fill="none" :stroke="gridColor" :stroke-width="1" :stroke-opacity="gridOpacity * 1.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#bigGrid)" />
          </svg>

          <!-- Symboles mathématiques discrets -->
          <div class="symbols-layer" :style="{ opacity: symbolsOpacity }">
            <span class="math-sym" style="top:8%;left:6%;font-size:28px;transform:rotate(-12deg)">∫</span>
            <span class="math-sym" style="top:5%;right:12%;font-size:22px;transform:rotate(8deg)">∑</span>
            <span class="math-sym" style="top:12%;left:75%;font-size:20px;transform:rotate(-5deg)">π</span>
            <span class="math-sym" style="top:15%;left:20%;font-size:18px;transform:rotate(15deg)">∞</span>
            <span class="math-sym" style="top:22%;right:8%;font-size:24px;transform:rotate(-8deg)">Δ</span>
            <span class="math-sym" style="top:25%;left:10%;font-size:16px;transform:rotate(20deg)">√</span>
            <span class="math-sym" style="top:30%;right:18%;font-size:18px;transform:rotate(-15deg)">∂</span>
            <span class="math-sym" style="bottom:28%;left:8%;font-size:22px;transform:rotate(10deg)">θ</span>
            <span class="math-sym" style="bottom:25%;right:10%;font-size:20px;transform:rotate(-18deg)">λ</span>
            <span class="math-sym" style="bottom:18%;left:22%;font-size:16px;transform:rotate(6deg)">α</span>
            <span class="math-sym" style="bottom:15%;right:20%;font-size:24px;transform:rotate(-10deg)">∮</span>
            <span class="math-sym" style="bottom:8%;left:12%;font-size:18px;transform:rotate(12deg)">ε</span>
            <span class="math-sym" style="bottom:5%;right:6%;font-size:26px;transform:rotate(-6deg)">Σ</span>
            <span class="math-sym" style="top:3%;left:45%;font-size:14px;transform:rotate(3deg)">f(x)</span>
            <span class="math-sym" style="bottom:3%;left:55%;font-size:14px;transform:rotate(-4deg)">dy/dx</span>
            <span class="math-sym" style="top:35%;left:4%;font-size:16px;transform:rotate(7deg)">±</span>
            <span class="math-sym" style="bottom:35%;right:5%;font-size:18px;transform:rotate(-12deg)">≈</span>
            <span class="math-sym" style="top:18%;left:88%;font-size:15px;transform:rotate(14deg)">∇</span>
            <span class="math-sym" style="bottom:12%;left:85%;font-size:16px;transform:rotate(-9deg)">φ</span>
            <span class="math-sym" style="top:9%;left:40%;font-size:13px;transform:rotate(5deg)">lim</span>
          </div>

          <!-- Images overlay -->
          <template v-for="imgOv in imageOverlays" :key="'img-ov-' + imgOv.id">
            <img
              v-if="imgOv.url"
              :src="imgOv.url"
              class="image-overlay-preview"
              :class="{ 'img-dragging': draggingOverlay && draggingOverlay.id === imgOv.id }"
              :data-overlay-id="imgOv.id"
              data-overlay-type="image"
              :style="{
                left: imgOv.x + '%',
                top: imgOv.y + '%',
                width: imgOv.widthPct + '%',
                opacity: imgOv.opacity,
                transform: 'translate(-50%, -50%) rotate(' + imgOv.rotation + 'deg)'
              }"
              @mousedown.prevent="startDragOverlay($event, imgOv)"
              @wheel.prevent="wheelZoomOverlay($event, imgOv)"
            />
          </template>

          <!-- Textes libres -->
          <div
            v-for="txt in textOverlays"
            :key="txt.id"
            class="text-overlay-wrapper"
            :class="{ 'text-dragging': draggingText && draggingText.id === txt.id, 'text-selected': selectedTextId === txt.id }"
            :data-overlay-id="txt.id"
            data-overlay-type="text"
            :style="{
              left: txt.x + '%',
              top: txt.y + '%',
              width: txt.boxWidth + '%',
              transform: 'translate(-50%, -50%) rotate(' + txt.rotation + 'deg)',
              opacity: txt.opacity,
            }"
            draggable="false"
            @dragstart.prevent
          >
            <div
              class="text-overlay-content"
              :style="{
                fontSize: txt.fontSize + 'px',
                fontFamily: txt.fontFamily,
                fontWeight: txt.bold ? 'bold' : 'normal',
                fontStyle: txt.italic ? 'italic' : 'normal',
                color: txt.color,
                textAlign: txt.align,
                textShadow: txt.shadow ? '2px 2px 8px rgba(0,0,0,0.6)' : 'none',
                letterSpacing: txt.letterSpacing + 'px',
                lineHeight: txt.lineHeight,
                whiteSpace: 'pre-wrap',
                wordWrap: 'break-word',
              }"
              draggable="false"
              @mousedown.prevent="selectAndDragText($event, txt)"
              @dragstart.prevent
              @wheel.prevent="wheelFontSize($event, txt)"
            >{{ txt.text }}</div>
            <!-- Poignées de redimensionnement -->
            <template v-if="selectedTextId === txt.id">
              <div class="resize-handle resize-left" @mousedown.stop.prevent="startResizeText($event, txt, 'left')"></div>
              <div class="resize-handle resize-right" @mousedown.stop.prevent="startResizeText($event, txt, 'right')"></div>
            </template>
          </div>

          <!-- Formules LaTeX -->
          <div
            v-for="overlay in latexOverlays"
            :key="'prev-' + overlay.id"
            class="latex-overlay-wrapper"
            :class="{ 'latex-dragging': draggingLatex && draggingLatex.id === overlay.id, 'latex-selected': selectedLatexId === overlay.id }"
            :data-overlay-id="overlay.id"
            data-overlay-type="latex"
            :style="{
              left: overlay.x + '%',
              top: overlay.y + '%',
              fontSize: overlay.fontSize + 'px',
              color: overlay.color,
              opacity: overlay.opacity,
              transform: 'translate(-50%, -50%) rotate(' + overlay.rotation + 'deg)',
              textShadow: overlay.shadow ? '2px 2px 8px rgba(0,0,0,0.6)' : 'none',
            }"
          >
            <div
              class="latex-overlay-content"
              @mousedown.prevent="selectAndDragLatex($event, overlay)"
              @wheel.prevent="wheelLatexSize($event, overlay)"
              v-html="renderLatex(overlay.latex)"
            ></div>
          </div>

          <!-- Vignettage -->
          <div class="vignette-layer" :style="vignetteStyle"></div>

          <!-- Guides d'alignement (style Canva) -->
          <svg v-if="activeGuides.length > 0 || activeDistances.length > 0 || activeEqualSpacing.length > 0" class="guides-layer" :width="canvasWidth" :height="canvasHeight">
            <!-- Lignes de guide -->
            <template v-for="(g, i) in activeGuides" :key="'guide-' + i">
              <line
                v-if="g.axis === 'x'"
                :x1="g.pos / 100 * canvasWidth" y1="0"
                :x2="g.pos / 100 * canvasWidth" :y2="canvasHeight"
                class="guide-line"
              />
              <line
                v-if="g.axis === 'y'"
                x1="0" :y1="g.pos / 100 * canvasHeight"
                :x2="canvasWidth" :y2="g.pos / 100 * canvasHeight"
                class="guide-line"
              />
            </template>
            <!-- Distance indicators -->
            <template v-for="(d, i) in activeDistances" :key="'dist-' + i">
              <line
                :x1="d.x1 / 100 * canvasWidth" :y1="d.y1 / 100 * canvasHeight"
                :x2="d.x2 / 100 * canvasWidth" :y2="d.y2 / 100 * canvasHeight"
                class="distance-line"
              />
              <rect
                :x="((d.x1 + d.x2) / 2 / 100 * canvasWidth) - 28"
                :y="((d.y1 + d.y2) / 2 / 100 * canvasHeight) - 10"
                width="56" height="20" rx="4" class="distance-label-bg"
              />
              <text
                :x="(d.x1 + d.x2) / 2 / 100 * canvasWidth"
                :y="(d.y1 + d.y2) / 2 / 100 * canvasHeight + 5"
                class="distance-label"
              >{{ d.label }}</text>
            </template>
            <!-- Equal spacing markers -->
            <template v-for="(eq, i) in activeEqualSpacing" :key="'eq-' + i">
              <!-- Vertical equal spacing -->
              <template v-if="eq.axis === 'y'">
                <line
                  :x1="eq.atX / 100 * canvasWidth - 15"
                  :y1="eq.from / 100 * canvasHeight"
                  :x2="eq.atX / 100 * canvasWidth - 15"
                  :y2="eq.to / 100 * canvasHeight"
                  class="equal-spacing-line"
                />
                <rect
                  :x="eq.atX / 100 * canvasWidth - 40"
                  :y="(eq.from + eq.to) / 2 / 100 * canvasHeight - 9"
                  width="50" height="18" rx="3" class="equal-spacing-bg"
                />
                <text
                  :x="eq.atX / 100 * canvasWidth - 15"
                  :y="(eq.from + eq.to) / 2 / 100 * canvasHeight + 4"
                  class="equal-spacing-label"
                >{{ eq.label }}</text>
              </template>
              <!-- Horizontal equal spacing -->
              <template v-if="eq.axis === 'x'">
                <line
                  :x1="eq.from / 100 * canvasWidth"
                  :y1="eq.atY / 100 * canvasHeight - 15"
                  :x2="eq.to / 100 * canvasWidth"
                  :y2="eq.atY / 100 * canvasHeight - 15"
                  class="equal-spacing-line"
                />
                <rect
                  :x="(eq.from + eq.to) / 2 / 100 * canvasWidth - 25"
                  :y="eq.atY / 100 * canvasHeight - 28"
                  width="50" height="18" rx="3" class="equal-spacing-bg"
                />
                <text
                  :x="(eq.from + eq.to) / 2 / 100 * canvasWidth"
                  :y="eq.atY / 100 * canvasHeight - 16"
                  class="equal-spacing-label"
                >{{ eq.label }}</text>
              </template>
            </template>
          </svg>

          <!-- Zone safe (haut/bas/gauche/droite) -->
              <div class="safe-zone-indicator">
                <div class="safe-zone-top" :style="{ height: (safeZoneV / canvasHeight * 100) + '%' }"></div>
                <div class="safe-zone-bottom" :style="{ height: (safeZoneV / canvasHeight * 100) + '%' }"></div>
                <div class="safe-zone-left" :style="{ width: (safeZoneH / canvasWidth * 100) + '%' }"></div>
                <div class="safe-zone-right" :style="{ width: (safeZoneH / canvasWidth * 100) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filmstrip diapos -->
        <div class="filmstrip" :style="{ '--canvas-ratio': (canvasHeight / canvasWidth).toFixed(3) }">
          <div class="filmstrip-slides">
            <div
              v-for="(slide, idx) in slides"
              :key="idx"
              class="filmstrip-item"
              :class="{ active: idx === currentSlideIndex }"
              @click="switchToSlide(idx)"
            >
              <div class="filmstrip-thumb" :style="{ background: `linear-gradient(160deg, ${lighten(slide.primaryColor, 15)}, ${slide.primaryColor}, ${darken(slide.primaryColor, 20)})` }">
                <span class="filmstrip-num">{{ idx + 1 }}</span>
              </div>
              <div class="filmstrip-actions">
                <button class="filmstrip-btn" @click.stop="duplicateSlide(idx)" title="Dupliquer">⧉</button>
                <button class="filmstrip-btn del" @click.stop="deleteSlide(idx)" title="Supprimer" :disabled="slides.length <= 1">✕</button>
              </div>
            </div>
            <button class="filmstrip-add" @click="addSlide" title="Nouvelle diapo">＋</button>
          </div>
        </div>
      </div>

      <!-- Sidebar droite fixe -->
      <div class="sidebar-column">
        <!-- Header + Export actions -->
        <div class="sidebar-header">
          <h2>🎬 Fond Reel</h2>
          <div class="sidebar-header-actions">
            <button class="btn-header-action primary" @click="exportPNG" title="Exporter PNG">📥 PNG</button>
            <button class="btn-header-action save" @click="saveProjectToFile" title="Sauvegarder le projet">💾</button>
            <button class="btn-header-action" @click="triggerLoadProject" title="Charger un projet">📂</button>
            <button class="btn-header-action" @click="openInNewTab" title="Ouvrir dans un nouvel onglet">🔗</button>
          </div>
        </div>

        <!-- Tabs -->
        <div class="sidebar-tabs">
          <button class="sidebar-tab" :class="{ active: sidebarTab === 'general' }" @click="sidebarTab = 'general'">⚙️ Général</button>
          <button class="sidebar-tab" :class="{ active: sidebarTab === 'images' }" @click="sidebarTab = 'images'">🖼️ Images</button>
          <button class="sidebar-tab" :class="{ active: sidebarTab === 'texte' }" @click="sidebarTab = 'texte'">✏️ Texte</button>
          <button class="sidebar-tab" :class="{ active: sidebarTab === 'latex' }" @click="sidebarTab = 'latex'">𝑓 LaTeX</button>
        </div>

        <div class="sidebar-scroll">

          <!-- Toast notification -->
          <transition name="toast-fade">
            <div v-if="toastMsg" class="toast-notification" :class="toastType">
              {{ toastMsg }}
            </div>
          </transition>

          <!-- Sauvegarde fichier local -->
          <div class="sidebar-section">
            <div class="section-title">💾 Projet</div>
            <div class="project-actions-row">
              <button class="btn-project-action" @click="saveProjectToFile">⬇️ Télécharger .json</button>
              <button class="btn-project-action" @click="triggerLoadProject">⬆️ Charger .json</button>
            </div>
            <div class="empty-hint">Sauvegarde locale en fichier .json — mets-le dans Image_Reel/</div>
            <input type="file" ref="fileInputRef" accept=".json" style="display:none" @change="loadProjectFromFile" />
          </div>

          <!-- ══ TAB: Général ══ -->
          <template v-if="sidebarTab === 'general'">

            <!-- Format -->
            <div class="sidebar-section">
              <div class="section-title">Format</div>
              <div class="format-presets">
                <button
                  v-for="fmt in formatPresets"
                  :key="fmt.label"
                  class="format-btn"
                  :class="{ active: canvasWidth === fmt.w && canvasHeight === fmt.h }"
                  @click="applyFormat(fmt)"
                >{{ fmt.label }}</button>
              </div>
              <div class="format-custom">
                <input type="number" v-model.number="canvasWidth" min="100" max="4000" class="dim-input" />
                <span class="dim-sep">×</span>
                <input type="number" v-model.number="canvasHeight" min="100" max="4000" class="dim-input" />
              </div>
            </div>

            <!-- Couleur & Presets -->
            <div class="sidebar-section">
              <div class="section-title">Couleur</div>
              <div class="color-row">
                <input type="color" v-model="primaryColor" />
                <input type="text" v-model="primaryColor" class="color-input" />
              </div>
              <div class="presets">
                <button @click="applyPreset('navy')" class="preset-btn navy">Navy</button>
                <button @click="applyPreset('dark')" class="preset-btn dark">Dark</button>
                <button @click="applyPreset('light')" class="preset-btn light">Light</button>
                <button @click="applyPreset('gradient')" class="preset-btn gradient">Grad</button>
              </div>
            </div>

            <!-- Effets -->
            <div class="sidebar-section">
              <div class="section-title">Effets</div>
              <div class="control-group">
                <label>Grille <span class="val">{{ gridOpacity }}</span></label>
                <input type="range" min="0" max="0.3" step="0.01" v-model.number="gridOpacity" />
              </div>
              <div class="control-group">
                <label>Symboles <span class="val">{{ symbolsOpacity }}</span></label>
                <input type="range" min="0" max="0.25" step="0.01" v-model.number="symbolsOpacity" />
              </div>
              <div class="control-group">
                <label>Vignettage <span class="val">{{ vignetteIntensity }}</span></label>
                <input type="range" min="0" max="1" step="0.05" v-model.number="vignetteIntensity" />
              </div>
            </div>

            <!-- Safe Zone -->
            <div class="sidebar-section">
              <div class="section-title">Safe Zone</div>
              <div class="control-group">
                <label>Vertical <span class="val">{{ safeZoneV }}px</span></label>
                <input type="range" min="0" max="400" step="5" v-model.number="safeZoneV" />
              </div>
              <div class="control-group">
                <label>Horizontal <span class="val">{{ safeZoneH }}px</span></label>
                <input type="range" min="0" max="300" step="5" v-model.number="safeZoneH" />
              </div>
            </div>

            <!-- Aperçu -->
            <div class="sidebar-section">
              <div class="section-title">Aperçu</div>
              <div class="control-group">
                <label>Taille <span class="val">{{ previewScale }}px</span></label>
                <input type="range" min="200" max="600" step="10" v-model.number="previewScale" />
              </div>
            </div>
          </template>

          <!-- ══ TAB: Images ══ -->
          <template v-if="sidebarTab === 'images'">

            <!-- Image de fond -->
            <div class="sidebar-section">
              <div class="section-title">Image de fond</div>
              <div class="control-group">
                <div class="upload-zone" @click="$refs.bgFileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
                  <input ref="bgFileInput" type="file" accept="image/*" style="display:none" @change="handleFileSelect" />
                  <span v-if="!bgImageUrl" class="upload-placeholder">📁 Cliquer ou glisser-déposer</span>
                  <span v-else class="upload-done">✅ Image chargée</span>
                </div>
                <button v-if="bgImageUrl" class="btn-remove-bg" @click="removeBgImage">✕ Supprimer</button>
              </div>
              <div class="control-group">
                <label>Opacité <span class="val">{{ bgImageOpacity }}</span></label>
                <input type="range" min="0" max="1" step="0.05" v-model.number="bgImageOpacity" :disabled="!bgImageUrl" />
              </div>
              <div class="sidebar-row-2">
                <div class="control-group">
                  <label>Ajustement</label>
                  <select v-model="bgImageFit" :disabled="!bgImageUrl" class="select-input">
                    <option value="cover">Cover</option>
                    <option value="contain">Contain</option>
                    <option value="stretch">Étirer</option>
                    <option value="original">Original</option>
                  </select>
                </div>
                <div class="control-group">
                  <label>Fusion</label>
                  <select v-model="bgImageBlend" :disabled="!bgImageUrl" class="select-input">
                    <option value="normal">Normal</option>
                    <option value="multiply">Multiply</option>
                    <option value="overlay">Overlay</option>
                    <option value="screen">Screen</option>
                    <option value="soft-light">Soft Light</option>
                    <option value="luminosity">Luminosity</option>
                  </select>
                </div>
              </div>
              <div class="control-group">
                <label>Position</label>
                <select v-model="bgImagePosition" :disabled="!bgImageUrl" class="select-input">
                  <option value="center center">Centre</option>
                  <option value="top center">Haut</option>
                  <option value="bottom center">Bas</option>
                  <option value="center left">Gauche</option>
                  <option value="center right">Droite</option>
                </select>
              </div>
            </div>

            <!-- Images overlay -->
            <div class="sidebar-section">
              <div class="section-title-row">
                <span class="section-title">Overlay</span>
                <button class="btn-add-item" @click="addImageOverlay">+ Image</button>
              </div>
              <div v-if="imageOverlays.length === 0" class="empty-hint">Aucune image ajoutée.</div>
              <div v-for="(imgOv, index) in imageOverlays" :key="imgOv.id" class="item-card">
                <div class="item-card-header">
                  <span class="item-card-num">Image {{ index + 1 }}</span>
                  <button class="btn-remove-overlay" @click="removeImageOverlay(imgOv.id)">✕</button>
                </div>
                <div class="control-group">
                  <div
                    class="upload-zone"
                    @click="$refs['imgOvInput' + imgOv.id]?.[0]?.click()"
                    @dragover.prevent
                    @drop.prevent="handleImageOverlayDrop($event, imgOv)"
                  >
                    <input
                      :ref="'imgOvInput' + imgOv.id"
                      type="file"
                      accept="image/*"
                      style="display:none"
                      @change="handleImageOverlaySelect($event, imgOv)"
                    />
                    <span v-if="!imgOv.url" class="upload-placeholder">📁 Cliquer ou glisser</span>
                    <span v-else class="upload-done">✅ Image chargée</span>
                  </div>
                </div>
                <div v-if="imgOv.url" class="img-overlay-thumb">
                  <img :src="imgOv.url" />
                </div>
                <div class="sidebar-row-2">
                  <div class="control-group">
                    <label>X <span class="val">{{ formatPercent(getOverlayEdgePercent(imgOv, 'image', 'x')) }}%</span></label>
                    <input
                      type="range"
                      :min="getOverlayEdgeMin(imgOv, 'image', 'x')"
                      :max="getOverlayEdgeMax(imgOv, 'image', 'x')"
                      step="0.1"
                      :value="getOverlayEdgePercent(imgOv, 'image', 'x')"
                      @input="onOverlayEdgeInput($event, imgOv, 'image', 'x')"
                    />
                  </div>
                  <div class="control-group">
                    <label>Y <span class="val">{{ formatPercent(getOverlayEdgePercent(imgOv, 'image', 'y')) }}%</span></label>
                    <input
                      type="range"
                      :min="getOverlayEdgeMin(imgOv, 'image', 'y')"
                      :max="getOverlayEdgeMax(imgOv, 'image', 'y')"
                      step="0.1"
                      :value="getOverlayEdgePercent(imgOv, 'image', 'y')"
                      @input="onOverlayEdgeInput($event, imgOv, 'image', 'y')"
                    />
                  </div>
                </div>
                <div class="sidebar-row-2">
                  <div class="control-group">
                    <label>Largeur <span class="val">{{ imgOv.widthPct }}%</span></label>
                    <input type="range" min="5" max="100" step="1" v-model.number="imgOv.widthPct" />
                  </div>
                  <div class="control-group">
                    <label>Opacité <span class="val">{{ imgOv.opacity }}</span></label>
                    <input type="range" min="0" max="1" step="0.05" v-model.number="imgOv.opacity" />
                  </div>
                </div>
                <div class="control-group">
                  <label>Rotation <span class="val">{{ imgOv.rotation }}°</span></label>
                  <input type="range" min="-180" max="180" step="1" v-model.number="imgOv.rotation" />
                </div>
              </div>
            </div>
          </template>

          <!-- ══ TAB: Texte ══ -->
          <template v-if="sidebarTab === 'texte'">
            <div class="sidebar-section">
              <div class="latex-hint">Glisser sur l'aperçu · Molette = taille</div>
            </div>
            <!-- Zone de saisie nouveau texte -->
            <div class="sidebar-section">
              <div class="section-title-row">
                <span class="section-title">Nouveau texte</span>
              </div>
              <div class="control-group">
                <textarea v-model="textInput" class="text-textarea" rows="2" placeholder="Mon texte..." @keydown.enter.exact.prevent="addTextFromInput"></textarea>
                <button class="btn-add-item" style="margin-top:6px;width:100%" @click="addTextFromInput" :disabled="!textInput.trim()">Ajouter ↵</button>
              </div>
            </div>

            <!-- Liste des textes -->
            <div class="sidebar-section">
              <div class="section-title-row">
                <span class="section-title">Textes</span>
                <span class="val" v-if="textOverlays.length">{{ textOverlays.length }}</span>
              </div>
              <div v-if="textOverlays.length === 0" class="empty-hint">Aucun texte ajouté.</div>
              <div
                v-for="(txt, index) in textOverlays"
                :key="txt.id"
                class="formula-list-item"
                :class="{ selected: selectedTextId === txt.id }"
                @click="selectedTextId = selectedTextId === txt.id ? null : txt.id"
              >
                <div class="formula-list-row">
                  <span class="formula-list-num">{{ index + 1 }}</span>
                  <div class="formula-list-preview text-list-preview" :style="{ fontFamily: txt.fontFamily, fontWeight: txt.bold ? 'bold' : 'normal', fontStyle: txt.italic ? 'italic' : 'normal', color: txt.color }">{{ txt.text }}</div>
                  <button class="btn-remove-overlay" @click.stop="removeTextOverlay(txt.id)">✕</button>
                </div>

                <!-- Panneau de propriétés (visible seulement quand sélectionné) -->
                <div v-if="selectedTextId === txt.id" class="formula-props" @click.stop>
                  <!-- Texte éditable -->
                  <div class="control-group">
                    <label>Contenu</label>
                    <textarea v-model="txt.text" class="text-textarea" rows="2" placeholder="Mon texte..."></textarea>
                  </div>

                  <!-- Police + Taille -->
                  <div class="sidebar-row-2">
                    <div class="control-group">
                      <label>Police</label>
                      <select v-model="txt.fontFamily" class="select-input">
                        <option value="'Arial', sans-serif">Arial</option>
                        <option value="'Georgia', serif">Georgia</option>
                        <option value="'Times New Roman', serif">Times New Roman</option>
                        <option value="'Courier New', monospace">Courier New</option>
                        <option value="'Trebuchet MS', sans-serif">Trebuchet</option>
                        <option value="'Impact', sans-serif">Impact</option>
                        <option value="'Palatino', serif">Palatino</option>
                        <option value="'Verdana', sans-serif">Verdana</option>
                      </select>
                    </div>
                    <div class="control-group">
                      <label>Taille <span class="val">{{ txt.fontSize }}px</span></label>
                      <input type="range" min="10" max="300" step="2" v-model.number="txt.fontSize" />
                    </div>
                  </div>

                  <!-- Couleur -->
                  <div class="control-group">
                    <label>Couleur</label>
                    <div class="color-row">
                      <input type="color" v-model="txt.color" />
                      <input type="text" v-model="txt.color" class="color-input" />
                    </div>
                  </div>

                  <!-- Style -->
                  <div class="control-group">
                    <label>Style</label>
                    <div class="text-style-row">
                      <button class="style-btn" :class="{ active: txt.bold }" @click="txt.bold = !txt.bold"><b>G</b></button>
                      <button class="style-btn" :class="{ active: txt.italic }" @click="txt.italic = !txt.italic"><i>I</i></button>
                      <button class="style-btn" :class="{ active: txt.shadow }" @click="txt.shadow = !txt.shadow" title="Ombre">◫</button>
                      <button class="style-btn" :class="{ active: txt.align === 'left' }" @click="txt.align = 'left'">⬅</button>
                      <button class="style-btn" :class="{ active: txt.align === 'center' }" @click="txt.align = 'center'">☰</button>
                      <button class="style-btn" :class="{ active: txt.align === 'right' }" @click="txt.align = 'right'">➡</button>
                    </div>
                  </div>

                  <!-- Position -->
                  <div class="sidebar-row-2">
                    <div class="control-group">
                      <label>X <span class="val">{{ formatPercent(getOverlayEdgePercent(txt, 'text', 'x')) }}%</span></label>
                      <input
                        type="range"
                        :min="getOverlayEdgeMin(txt, 'text', 'x')"
                        :max="getOverlayEdgeMax(txt, 'text', 'x')"
                        step="0.1"
                        :value="getOverlayEdgePercent(txt, 'text', 'x')"
                        @input="onOverlayEdgeInput($event, txt, 'text', 'x')"
                      />
                    </div>
                    <div class="control-group">
                      <label>Y <span class="val">{{ formatPercent(getOverlayEdgePercent(txt, 'text', 'y')) }}%</span></label>
                      <input
                        type="range"
                        :min="getOverlayEdgeMin(txt, 'text', 'y')"
                        :max="getOverlayEdgeMax(txt, 'text', 'y')"
                        step="0.1"
                        :value="getOverlayEdgePercent(txt, 'text', 'y')"
                        @input="onOverlayEdgeInput($event, txt, 'text', 'y')"
                      />
                    </div>
                  </div>

                  <!-- Opacité + Rotation -->
                  <div class="sidebar-row-2">
                    <div class="control-group">
                      <label>Opacité <span class="val">{{ txt.opacity }}</span></label>
                      <input type="range" min="0" max="1" step="0.05" v-model.number="txt.opacity" />
                    </div>
                    <div class="control-group">
                      <label>Rotation <span class="val">{{ txt.rotation }}°</span></label>
                      <input type="range" min="-180" max="180" step="1" v-model.number="txt.rotation" />
                    </div>
                  </div>

                  <!-- Largeur boîte -->
                  <div class="control-group">
                    <label>Largeur boîte <span class="val">{{ txt.boxWidth }}%</span></label>
                    <input type="range" min="10" max="95" step="1" v-model.number="txt.boxWidth" />
                  </div>

                  <!-- Espacement + Interligne -->
                  <div class="sidebar-row-2">
                    <div class="control-group">
                      <label>Espacement <span class="val">{{ txt.letterSpacing }}px</span></label>
                      <input type="range" min="-5" max="30" step="1" v-model.number="txt.letterSpacing" />
                    </div>
                    <div class="control-group">
                      <label>Interligne <span class="val">{{ txt.lineHeight }}</span></label>
                      <input type="range" min="0.8" max="3" step="0.1" v-model.number="txt.lineHeight" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- ══ TAB: LaTeX ══ -->
          <template v-if="sidebarTab === 'latex'">
            <div class="sidebar-section">
              <div class="latex-hint">Supporte <code>\\frac</code>, <code>\\int</code>, <code>\\sum</code>, <code>\\begin{'{'}aligned{'}'}</code>…<br/>Glisser sur l'aperçu · Molette = taille</div>
            </div>
            <!-- Zone de saisie LaTeX -->
            <div class="sidebar-section">
              <div class="section-title-row">
                <span class="section-title">Nouvelle formule</span>
              </div>
              <div class="control-group">
                <textarea v-model="latexInput" class="text-textarea latex-textarea" rows="5" placeholder="Ex: \frac{a}{b} ou \begin{aligned}...\end{aligned}" @keydown.shift.enter.prevent="addLatexFromInput"></textarea>
                <div v-if="latexInput" class="latex-preview-mini" v-html="renderLatex(latexInput)"></div>
                <button class="btn-add-item" style="margin-top:6px;width:100%" @click="addLatexFromInput" :disabled="!latexInput.trim()">Ajouter (Shift+↵)</button>
              </div>
            </div>

            <!-- Liste des formules -->
            <div class="sidebar-section">
              <div class="section-title-row">
                <span class="section-title">Formules</span>
                <span class="val" v-if="latexOverlays.length">{{ latexOverlays.length }}</span>
              </div>
              <div v-if="latexOverlays.length === 0" class="empty-hint">Aucune formule ajoutée.</div>
              <div
                v-for="(overlay, index) in latexOverlays"
                :key="overlay.id"
                class="formula-list-item"
                :class="{ selected: selectedLatexId === overlay.id }"
                @click="selectedLatexId = selectedLatexId === overlay.id ? null : overlay.id"
              >
                <div class="formula-list-row">
                  <span class="formula-list-num">{{ index + 1 }}</span>
                  <div class="formula-list-preview" v-html="renderLatex(overlay.latex)"></div>
                  <button class="btn-remove-overlay" @click.stop="removeLatexOverlay(overlay.id)">✕</button>
                </div>

                <!-- Panneau de propriétés (visible seulement quand sélectionné) -->
                <div v-if="selectedLatexId === overlay.id" class="formula-props" @click.stop>
                  <!-- Code LaTeX éditable -->
                  <div class="control-group">
                    <label>Code LaTeX</label>
                    <textarea v-model="overlay.latex" class="text-textarea latex-textarea" rows="3" placeholder="Ex: \\frac{a}{b}"></textarea>
                  </div>

                  <!-- Taille -->
                  <div class="control-group">
                    <label>Taille <span class="val">{{ overlay.fontSize }}px</span></label>
                    <input type="range" min="12" max="300" step="2" v-model.number="overlay.fontSize" />
                  </div>

                  <!-- Couleur -->
                  <div class="control-group">
                    <label>Couleur</label>
                    <div class="color-row">
                      <input type="color" v-model="overlay.color" />
                      <input type="text" v-model="overlay.color" class="color-input" />
                    </div>
                  </div>

                  <!-- Style -->
                  <div class="control-group">
                    <label>Style</label>
                    <div class="text-style-row">
                      <button class="style-btn" :class="{ active: overlay.shadow }" @click="overlay.shadow = !overlay.shadow" title="Ombre">◫ Ombre</button>
                    </div>
                  </div>

                  <!-- Position -->
                  <div class="sidebar-row-2">
                    <div class="control-group">
                      <label>X <span class="val">{{ formatPercent(getOverlayEdgePercent(overlay, 'latex', 'x')) }}%</span></label>
                      <input
                        type="range"
                        :min="getOverlayEdgeMin(overlay, 'latex', 'x')"
                        :max="getOverlayEdgeMax(overlay, 'latex', 'x')"
                        step="0.1"
                        :value="getOverlayEdgePercent(overlay, 'latex', 'x')"
                        @input="onOverlayEdgeInput($event, overlay, 'latex', 'x')"
                      />
                    </div>
                    <div class="control-group">
                      <label>Y <span class="val">{{ formatPercent(getOverlayEdgePercent(overlay, 'latex', 'y')) }}%</span></label>
                      <input
                        type="range"
                        :min="getOverlayEdgeMin(overlay, 'latex', 'y')"
                        :max="getOverlayEdgeMax(overlay, 'latex', 'y')"
                        step="0.1"
                        :value="getOverlayEdgePercent(overlay, 'latex', 'y')"
                        @input="onOverlayEdgeInput($event, overlay, 'latex', 'y')"
                      />
                    </div>
                  </div>

                  <!-- Opacité + Rotation -->
                  <div class="sidebar-row-2">
                    <div class="control-group">
                      <label>Opacité <span class="val">{{ overlay.opacity }}</span></label>
                      <input type="range" min="0" max="1" step="0.05" v-model.number="overlay.opacity" />
                    </div>
                    <div class="control-group">
                      <label>Rotation <span class="val">{{ overlay.rotation }}°</span></label>
                      <input type="range" min="-180" max="180" step="1" v-model.number="overlay.rotation" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import katex from 'katex'
import katexCSSRaw from 'katex/dist/katex.min.css?raw'
import html2canvas from 'html2canvas'

// ─── Slides (diapos) ───
function createSlideState() {
  return {
    primaryColor: '#455e92',
    gridOpacity: 0.08,
    symbolsOpacity: 0.06,
    vignetteIntensity: 0.65,
    bgImageUrl: '/OptiTAB_bg.png',
    bgImageBase64: '/OptiTAB_bg.png',
    bgImageOpacity: 1,
    bgImageFit: 'cover',
    bgImagePosition: 'center center',
    bgImageBlend: 'normal',
    imageOverlays: [],
    latexOverlays: [],
    textOverlays: [],
  }
}

const slides = ref([createSlideState()])
const currentSlideIndex = ref(0)
const currentSlide = computed(() => slides.value[currentSlideIndex.value])

function saveCurrentSlideState() {
  const s = slides.value[currentSlideIndex.value]
  s.primaryColor = primaryColor.value
  s.gridOpacity = gridOpacity.value
  s.symbolsOpacity = symbolsOpacity.value
  s.vignetteIntensity = vignetteIntensity.value
  s.bgImageUrl = bgImageUrl.value
  s.bgImageBase64 = bgImageBase64.value
  s.bgImageOpacity = bgImageOpacity.value
  s.bgImageFit = bgImageFit.value
  s.bgImagePosition = bgImagePosition.value
  s.bgImageBlend = bgImageBlend.value
  s.imageOverlays = JSON.parse(JSON.stringify(imageOverlays.value))
  s.latexOverlays = JSON.parse(JSON.stringify(latexOverlays.value))
  s.textOverlays = JSON.parse(JSON.stringify(textOverlays.value))
}

function loadSlideState(index) {
  const s = slides.value[index]
  primaryColor.value = s.primaryColor
  gridOpacity.value = s.gridOpacity
  symbolsOpacity.value = s.symbolsOpacity
  vignetteIntensity.value = s.vignetteIntensity
  bgImageUrl.value = s.bgImageUrl
  bgImageBase64.value = s.bgImageBase64
  bgImageOpacity.value = s.bgImageOpacity
  bgImageFit.value = s.bgImageFit
  bgImagePosition.value = s.bgImagePosition
  bgImageBlend.value = s.bgImageBlend
  imageOverlays.value = s.imageOverlays.map(o => ({ ...o }))
  latexOverlays.value = s.latexOverlays.map(o => ({ ...o }))
  textOverlays.value = (s.textOverlays || []).map(o => ({ ...o }))
}

function switchToSlide(index) {
  if (index === currentSlideIndex.value) return
  saveCurrentSlideState()
  currentSlideIndex.value = index
  loadSlideState(index)
}

function addSlide() {
  saveCurrentSlideState()
  slides.value.push(createSlideState())
  currentSlideIndex.value = slides.value.length - 1
  loadSlideState(currentSlideIndex.value)
}

function duplicateSlide(index) {
  saveCurrentSlideState()
  const source = slides.value[index]
  const copy = JSON.parse(JSON.stringify(source))
  slides.value.splice(index + 1, 0, copy)
  currentSlideIndex.value = index + 1
  loadSlideState(currentSlideIndex.value)
}

function deleteSlide(index) {
  if (slides.value.length <= 1) return
  slides.value.splice(index, 1)
  if (currentSlideIndex.value >= slides.value.length) {
    currentSlideIndex.value = slides.value.length - 1
  }
  loadSlideState(currentSlideIndex.value)
}

// ─── Variables de personnalisation ───
const primaryColor = ref('#455e92')
const gridOpacity = ref(0.08)
const symbolsOpacity = ref(0.06)
const vignetteIntensity = ref(0.65)
const previewScale = ref(360)
const safeZoneV = ref(400)
const safeZoneH = ref(95)

// ─── Dimensions du canvas ───
const canvasWidth = ref(1080)
const canvasHeight = ref(1920)
const formatPresets = [
  { label: 'Reel / Story', w: 1080, h: 1920 },
  { label: 'Post carré', w: 1080, h: 1080 },
  { label: 'Post portrait', w: 1080, h: 1350 },
  { label: 'Post paysage', w: 1200, h: 628 },
  { label: 'YouTube', w: 1280, h: 720 },
  { label: 'Banner', w: 1920, h: 1080 },
]
function applyFormat(preset) {
  canvasWidth.value = preset.w
  canvasHeight.value = preset.h
}

// ─── Image de fond personnalisée ───
const bgImageUrl = ref('/OptiTAB_bg.png')
const bgImageBase64 = ref('/OptiTAB_bg.png')
const bgImageOpacity = ref(1)
const bgImageFit = ref('cover')
const bgImagePosition = ref('center center')
const bgImageBlend = ref('normal')

// ─── Sidebar tab ───
const sidebarTab = ref('general')

// ─── Text overlays ───
const textOverlays = ref([])
let nextTextId = 0

function removeTextOverlay(id) {
  textOverlays.value = textOverlays.value.filter(o => o.id !== id)
  if (selectedTextId.value === id) selectedTextId.value = null
}

const selectedTextId = ref(null)
const draggingText = ref(null)
let dragTextStartX = 0, dragTextStartY = 0, dragTextStartOvX = 0, dragTextStartOvY = 0

const textInput = ref('')

function getNextTextId() {
  const maxExisting = textOverlays.value.reduce((maxId, ov) => Math.max(maxId, Number(ov.id) || 0), 0)
  nextTextId = Math.max(nextTextId, maxExisting)
  nextTextId += 1
  return nextTextId
}

function addTextFromInput() {
  const content = textInput.value.trim()
  if (!content) return
  const newId = getNextTextId()
  textOverlays.value.push({
    id: newId,
    text: content,
    x: 50,
    y: 50,
    fontSize: 80,
    fontFamily: "'Arial', sans-serif",
    bold: false,
    italic: false,
    shadow: true,
    color: '#29428e',
    align: 'center',
    opacity: 1,
    rotation: 0,
    letterSpacing: 0,
    lineHeight: 1.2,
    boxWidth: 60,
  })
  textInput.value = ''
  selectedTextId.value = newId
}

function selectAndDragText(e, txt) {
  selectedTextId.value = txt.id
  sidebarTab.value = 'texte'
  startDragText(e, txt)
}

function startDragText(e, txt) {
  draggingText.value = txt
  dragTextStartX = e.clientX
  dragTextStartY = e.clientY
  dragTextStartOvX = txt.x
  dragTextStartOvY = txt.y
  window.addEventListener('mousemove', onDragText)
  window.addEventListener('mouseup', stopDragText)
}

function onDragText(e) {
  if (!draggingText.value) return
  const scale = previewScale.value / canvasWidth.value
  const dx = (e.clientX - dragTextStartX) / scale
  const dy = (e.clientY - dragTextStartY) / scale
  const bounds = getOverlayMoveBounds('text', draggingText.value.id)
  const rawX = dragTextStartOvX + (dx / canvasWidth.value) * 100
  const rawY = dragTextStartOvY + (dy / canvasHeight.value) * 100
  const clampedX = clampValue(rawX, bounds.minX, bounds.maxX)
  const clampedY = clampValue(rawY, bounds.minY, bounds.maxY)
  const snapped = computeSnap(clampedX, clampedY, draggingText.value.id, 'text')
  draggingText.value.x = clampValue(snapped.x, bounds.minX, bounds.maxX)
  draggingText.value.y = clampValue(snapped.y, bounds.minY, bounds.maxY)
}

function stopDragText() {
  draggingText.value = null
  clearGuides()
  window.removeEventListener('mousemove', onDragText)
  window.removeEventListener('mouseup', stopDragText)
}

function wheelFontSize(e, txt) {
  txt.fontSize = Math.max(10, Math.min(300, txt.fontSize + (e.deltaY > 0 ? -2 : 2)))
  clampOverlayToBounds(txt, 'text')
}

// ─── Resize text box ───
const resizingText = ref(null)
let resizeSide = ''
let resizeStartX = 0
let resizeStartWidth = 0
let resizeStartPosX = 0

function startResizeText(e, txt, side) {
  resizingText.value = txt
  resizeSide = side
  resizeStartX = e.clientX
  resizeStartWidth = txt.boxWidth
  resizeStartPosX = txt.x
  window.addEventListener('mousemove', onResizeText)
  window.addEventListener('mouseup', stopResizeText)
}

function onResizeText(e) {
  if (!resizingText.value) return
  const scale = previewScale.value / canvasWidth.value
  const dxPx = (e.clientX - resizeStartX) / scale
  const dxPct = (dxPx / canvasWidth.value) * 100

  if (resizeSide === 'right') {
    // Expand/shrink right side: width changes, center moves right by half
    const newWidth = Math.max(10, Math.min(95, resizeStartWidth + dxPct * 2))
    resizingText.value.boxWidth = Math.round(newWidth)
  } else if (resizeSide === 'left') {
    // Expand/shrink left side: width changes, center moves left by half
    const newWidth = Math.max(10, Math.min(95, resizeStartWidth - dxPct * 2))
    resizingText.value.boxWidth = Math.round(newWidth)
  }
  clampOverlayToBounds(resizingText.value, 'text')
}

function stopResizeText() {
  resizingText.value = null
  window.removeEventListener('mousemove', onResizeText)
  window.removeEventListener('mouseup', stopResizeText)
}

// ─── Images en overlay ───
const imageOverlays = ref([])
let nextImageOverlayId = 0

function addImageOverlay() {
  imageOverlays.value.push({
    id: ++nextImageOverlayId,
    url: '',
    base64: '',
    x: 50,
    y: 50,
    widthPct: 30,
    opacity: 1,
    rotation: 0
  })
}

function removeImageOverlay(id) {
  imageOverlays.value = imageOverlays.value.filter(o => o.id !== id)
}

function handleImageOverlaySelect(e, overlay) {
  const file = e.target.files?.[0]
  if (file && file.type.startsWith('image/')) loadOverlayImage(file, overlay)
}

function handleImageOverlayDrop(e, overlay) {
  const file = e.dataTransfer.files?.[0]
  if (file && file.type.startsWith('image/')) loadOverlayImage(file, overlay)
}

function loadOverlayImage(file, overlay) {
  const reader = new FileReader()
  reader.onload = (ev) => {
    overlay.url = ev.target.result
    overlay.base64 = ev.target.result
  }
  reader.readAsDataURL(file)
}

// ─── Formules LaTeX ───
const latexOverlays = ref([])
let nextOverlayId = 0
const latexInput = ref('')
const selectedLatexId = ref(null)

function getNextLatexId() {
  const maxExisting = latexOverlays.value.reduce((maxId, ov) => Math.max(maxId, Number(ov.id) || 0), 0)
  nextOverlayId = Math.max(nextOverlayId, maxExisting)
  nextOverlayId += 1
  return nextOverlayId
}

function addLatexFromInput() {
  const code = latexInput.value.trim()
  if (!code) return
  const newId = getNextLatexId()
  latexOverlays.value.push({
    id: newId,
    latex: code,
    x: 50,
    y: 50,
    fontSize: 80,
    color: '#29428e',
    opacity: 1,
    rotation: 0,
    shadow: false,
  })
  latexInput.value = ''
  selectedLatexId.value = newId
}

function addLatexOverlay() {
  addLatexFromInput()
}

// Drag LaTeX overlays
const draggingLatex = ref(null)
let dragLatexStartX = 0, dragLatexStartY = 0, dragLatexOvX = 0, dragLatexOvY = 0

function selectAndDragLatex(e, overlay) {
  selectedLatexId.value = overlay.id
  sidebarTab.value = 'latex'
  startDragLatex(e, overlay)
}

function startDragLatex(e, overlay) {
  draggingLatex.value = overlay
  dragLatexStartX = e.clientX
  dragLatexStartY = e.clientY
  dragLatexOvX = overlay.x
  dragLatexOvY = overlay.y
  window.addEventListener('mousemove', onDragLatex)
  window.addEventListener('mouseup', stopDragLatex)
}

function onDragLatex(e) {
  if (!draggingLatex.value) return
  const scale = previewScale.value / canvasWidth.value
  const dx = (e.clientX - dragLatexStartX) / scale
  const dy = (e.clientY - dragLatexStartY) / scale
  const bounds = getOverlayMoveBounds('latex', draggingLatex.value.id)
  const rawX = dragLatexOvX + (dx / canvasWidth.value) * 100
  const rawY = dragLatexOvY + (dy / canvasHeight.value) * 100
  const clampedX = clampValue(rawX, bounds.minX, bounds.maxX)
  const clampedY = clampValue(rawY, bounds.minY, bounds.maxY)
  const snapped = computeSnap(clampedX, clampedY, draggingLatex.value.id, 'latex')
  draggingLatex.value.x = clampValue(snapped.x, bounds.minX, bounds.maxX)
  draggingLatex.value.y = clampValue(snapped.y, bounds.minY, bounds.maxY)
}

function stopDragLatex() {
  draggingLatex.value = null
  clearGuides()
  window.removeEventListener('mousemove', onDragLatex)
  window.removeEventListener('mouseup', stopDragLatex)
}

function wheelLatexSize(e, overlay) {
  overlay.fontSize = Math.max(12, Math.min(300, overlay.fontSize + (e.deltaY > 0 ? -2 : 2)))
  clampOverlayToBounds(overlay, 'latex')
}

function removeLatexOverlay(id) {
  latexOverlays.value = latexOverlays.value.filter(o => o.id !== id)
  if (selectedLatexId.value === id) selectedLatexId.value = null
}

function renderLatex(latex) {
  try {
    let cleaned = cleanLatexInput(latex)
    return katex.renderToString(cleaned, { throwOnError: false, displayMode: true, trust: true })
  } catch (e) {
    return `<span style="color:#e74c3c">${latex}</span>`
  }
}

// Nettoie le LaTeX : strip delimiters + convertit \textcolor[HTML]{...} → \textcolor{#...}
function cleanLatexInput(latex) {
  let cleaned = latex.trim()
  // Strip delimiters that KaTeX doesn't need (displayMode handles it)
  if (cleaned.startsWith('\\[') && cleaned.endsWith('\\]')) {
    cleaned = cleaned.slice(2, -2).trim()
  } else if (cleaned.startsWith('$$') && cleaned.endsWith('$$')) {
    cleaned = cleaned.slice(2, -2).trim()
  } else if (cleaned.startsWith('$') && cleaned.endsWith('$')) {
    cleaned = cleaned.slice(1, -1).trim()
  }
  // Convert \textcolor[HTML]{XXXXXX} → \textcolor{#XXXXXX} (KaTeX doesn't support [HTML] model)
  cleaned = cleaned.replace(/\\textcolor\[HTML\]\{([0-9A-Fa-f]{3,8})\}/g, '\\textcolor{#$1}')
  // Also handle \color[HTML]{XXXXXX} → \color{#XXXXXX}
  cleaned = cleaned.replace(/\\color\[HTML\]\{([0-9A-Fa-f]{3,8})\}/g, '\\color{#$1}')
  return cleaned
}

// ─── Guides d'alignement (style Canva) ───
const SNAP_THRESHOLD = 1.5 // % de tolérance pour le snap
const EQUAL_SPACING_THRESHOLD = 1.0 // % de tolérance pour l'espacement égal
const activeGuides = ref([])
const activeDistances = ref([])
const activeEqualSpacing = ref([])
const reelCanvas = ref(null)

function getSafeBoundsPct() {
  const safeTop = safeZoneV.value / canvasHeight.value * 100
  const safeBottom = 100 - safeTop
  const safeLeft = safeZoneH.value / canvasWidth.value * 100
  const safeRight = 100 - safeLeft
  return { safeTop, safeBottom, safeLeft, safeRight }
}

function getOverlayHalfSizePct(overlayType, overlayId) {
  const canvasEl = reelCanvas.value
  if (!canvasEl) return { halfW: 0, halfH: 0 }
  const overlayEl = canvasEl.querySelector(
    `[data-overlay-type="${overlayType}"][data-overlay-id="${overlayId}"]`
  )
  if (!overlayEl) return { halfW: 0, halfH: 0 }
  const canvasRect = canvasEl.getBoundingClientRect()
  const rect = overlayEl.getBoundingClientRect()
  if (!canvasRect.width || !canvasRect.height) return { halfW: 0, halfH: 0 }
  return {
    halfW: (rect.width / canvasRect.width) * 50,
    halfH: (rect.height / canvasRect.height) * 50,
  }
}

function getOverlayMoveBounds(overlayType, overlayId) {
  const { safeTop, safeBottom, safeLeft, safeRight } = getSafeBoundsPct()
  const { halfW, halfH } = getOverlayHalfSizePct(overlayType, overlayId)
  let minX = safeLeft + halfW
  let maxX = safeRight - halfW
  let minY = safeTop + halfH
  let maxY = safeBottom - halfH
  if (minX > maxX) {
    const midX = (safeLeft + safeRight) / 2
    minX = midX
    maxX = midX
  }
  if (minY > maxY) {
    const midY = (safeTop + safeBottom) / 2
    minY = midY
    maxY = midY
  }
  return { minX, maxX, minY, maxY, halfW, halfH }
}

function clampValue(value, min, max) {
  return Math.max(min, Math.min(max, value))
}

function clampOverlayToBounds(overlay, overlayType) {
  if (!overlay) return
  const bounds = getOverlayMoveBounds(overlayType, overlay.id)
  overlay.x = clampValue(overlay.x, bounds.minX, bounds.maxX)
  overlay.y = clampValue(overlay.y, bounds.minY, bounds.maxY)
}

function getOverlayEdgePercent(overlay, overlayType, axis) {
  if (!overlay) return 0
  const bounds = getOverlayMoveBounds(overlayType, overlay.id)
  const center = axis === 'x' ? overlay.x : overlay.y
  const half = axis === 'x' ? bounds.halfW : bounds.halfH
  return center - half
}

function getOverlayEdgeMin(overlay, overlayType, axis) {
  const bounds = getOverlayMoveBounds(overlayType, overlay.id)
  return axis === 'x' ? bounds.minX - bounds.halfW : bounds.minY - bounds.halfH
}

function getOverlayEdgeMax(overlay, overlayType, axis) {
  const bounds = getOverlayMoveBounds(overlayType, overlay.id)
  return axis === 'x' ? bounds.maxX - bounds.halfW : bounds.maxY - bounds.halfH
}

function onOverlayEdgeInput(event, overlay, overlayType, axis) {
  const value = Number(event?.target?.value)
  if (!Number.isFinite(value)) return
  const bounds = getOverlayMoveBounds(overlayType, overlay.id)
  const half = axis === 'x' ? bounds.halfW : bounds.halfH
  if (axis === 'x') overlay.x = value + half
  else overlay.y = value + half
  clampOverlayToBounds(overlay, overlayType)
}

function formatPercent(value) {
  if (!Number.isFinite(value)) return '0'
  return (Math.round(value * 10) / 10).toString()
}

// ─── Copy / Paste overlays ───
const overlayClipboard = ref(null)

function deepClone(value) {
  return JSON.parse(JSON.stringify(value))
}

function getSelectedOverlayForClipboard() {
  if (selectedTextId.value !== null) {
    const txt = textOverlays.value.find(t => t.id === selectedTextId.value)
    if (txt) return { type: 'text', overlay: txt }
  }
  if (selectedLatexId.value !== null) {
    const latex = latexOverlays.value.find(o => o.id === selectedLatexId.value)
    if (latex) return { type: 'latex', overlay: latex }
  }
  return null
}

function copySelectedOverlay() {
  const selected = getSelectedOverlayForClipboard()
  if (!selected) return false

  overlayClipboard.value = {
    type: selected.type,
    data: deepClone(selected.overlay),
    pasteCount: 0,
  }

  // Best effort: expose plain content in system clipboard too.
  const plain = selected.type === 'text' ? selected.overlay.text : selected.overlay.latex
  if (plain && navigator?.clipboard?.writeText) {
    navigator.clipboard.writeText(plain).catch(() => {})
  }
  showToast(`${selected.type === 'text' ? 'Texte' : 'Formule'} copié`)
  return true
}

function pasteOverlayFromClipboard() {
  const clip = overlayClipboard.value
  if (!clip || !clip.data) return false

  const offsetPct = 2 * ((clip.pasteCount || 0) + 1)

  if (clip.type === 'text') {
    const clone = deepClone(clip.data)
    clone.id = getNextTextId()
    clone.x = Number(clone.x || 50) + offsetPct
    clone.y = Number(clone.y || 50) + offsetPct
    textOverlays.value.push(clone)
    clampOverlayToBounds(clone, 'text')
    selectedTextId.value = clone.id
    selectedLatexId.value = null
    sidebarTab.value = 'texte'
    clip.pasteCount = (clip.pasteCount || 0) + 1
    showToast('Texte collé')
    return true
  }

  if (clip.type === 'latex') {
    const clone = deepClone(clip.data)
    clone.id = getNextLatexId()
    clone.x = Number(clone.x || 50) + offsetPct
    clone.y = Number(clone.y || 50) + offsetPct
    latexOverlays.value.push(clone)
    clampOverlayToBounds(clone, 'latex')
    selectedLatexId.value = clone.id
    selectedTextId.value = null
    sidebarTab.value = 'latex'
    clip.pasteCount = (clip.pasteCount || 0) + 1
    showToast('Formule collée')
    return true
  }

  return false
}

// Lit les bounding boxes réelles des éléments sur le canvas (en %)
function getElementEdges(excludeId, excludeType) {
  const edges = []
  const canvasEl = reelCanvas.value
  if (!canvasEl) return edges
  const cw = canvasWidth.value
  const ch = canvasHeight.value

  // Canvas edges & center (safe zone from each edge)
  const safeTopPct = safeZoneV.value / ch * 100
  const safeBotPct = 100 - safeTopPct
  const safeLeftPct = safeZoneH.value / cw * 100
  const safeRightPct = 100 - safeLeftPct
  edges.push({ id: '__top__', left: safeLeftPct, right: safeRightPct, top: safeTopPct, bottom: safeTopPct, cx: 50, cy: safeTopPct })
  edges.push({ id: '__bottom__', left: safeLeftPct, right: safeRightPct, top: safeBotPct, bottom: safeBotPct, cx: 50, cy: safeBotPct })
  edges.push({ id: '__left__', left: safeLeftPct, right: safeLeftPct, top: safeTopPct, bottom: safeBotPct, cx: safeLeftPct, cy: 50 })
  edges.push({ id: '__right__', left: safeRightPct, right: safeRightPct, top: safeTopPct, bottom: safeBotPct, cx: safeRightPct, cy: 50 })
  edges.push({ id: '__center__', left: 50, right: 50, top: 50, bottom: 50, cx: 50, cy: 50 })

  // Query all overlay elements on the canvas
  const overlayEls = canvasEl.querySelectorAll('[data-overlay-id]')
  overlayEls.forEach(el => {
    const rect = el.getBoundingClientRect()
    const canvasRect = canvasEl.getBoundingClientRect()
    const scale = cw / canvasRect.width
    // Convert to canvas coordinates (px), then to %
    const elLeft = (rect.left - canvasRect.left) * scale
    const elTop = (rect.top - canvasRect.top) * scale
    const elRight = elLeft + rect.width * scale
    const elBottom = elTop + rect.height * scale
    const elCx = (elLeft + elRight) / 2
    const elCy = (elTop + elBottom) / 2

    // Identify this element via data attributes
    const elId = parseInt(el.dataset.overlayId)
    const elType = el.dataset.overlayType
    if (elType === excludeType && elId === excludeId) return

    edges.push({
      id: elId,
      left: elLeft / cw * 100,
      right: elRight / cw * 100,
      top: elTop / ch * 100,
      bottom: elBottom / ch * 100,
      cx: elCx / cw * 100,
      cy: elCy / ch * 100,
    })
  })
  return edges
}

function computeSnap(rawX, rawY, excludeId, excludeType) {
  const edgeList = getElementEdges(excludeId, excludeType)
  const guides = []
  const distances = []
  const equalSpacing = []
  let snappedX = rawX
  let snappedY = rawY
  let bestDx = SNAP_THRESHOLD + 1
  let bestDy = SNAP_THRESHOLD + 1

  // Estimate current element half-size (approx from DOM)
  let myHalfW = 0, myHalfH = 0
  const canvasEl = reelCanvas.value
  if (canvasEl) {
    const cw = canvasWidth.value, ch = canvasHeight.value
    let dragEl = null
    if (excludeType === 'text') dragEl = canvasEl.querySelector('.text-dragging')
    else if (excludeType === 'latex') dragEl = canvasEl.querySelector('.latex-dragging')
    else if (excludeType === 'image') dragEl = canvasEl.querySelector('.img-dragging')
    if (dragEl) {
      const r = dragEl.getBoundingClientRect()
      const cr = canvasEl.getBoundingClientRect()
      const scale = cw / cr.width
      myHalfW = (r.width * scale / 2) / cw * 100
      myHalfH = (r.height * scale / 2) / ch * 100
    }
  }

  // My edges
  const myLeft = rawX - myHalfW
  const myRight = rawX + myHalfW
  const myTop = rawY - myHalfH
  const myBottom = rawY + myHalfH

  // ── Snap on all edge combinations ──
  for (const other of edgeList) {
    // X snaps: my left ↔ other left, my center ↔ other center, my right ↔ other right
    // Also: my left ↔ other right, my right ↔ other left (edge-to-edge)
    const xChecks = [
      { myEdge: myLeft, otherEdge: other.left, label: 'left-left' },
      { myEdge: myRight, otherEdge: other.right, label: 'right-right' },
      { myEdge: rawX, otherEdge: other.cx, label: 'cx-cx' },
      { myEdge: myLeft, otherEdge: other.right, label: 'left-right' },
      { myEdge: myRight, otherEdge: other.left, label: 'right-left' },
      { myEdge: myLeft, otherEdge: other.cx, label: 'left-cx' },
      { myEdge: myRight, otherEdge: other.cx, label: 'right-cx' },
    ]
    for (const chk of xChecks) {
      const dx = Math.abs(chk.myEdge - chk.otherEdge)
      if (dx < SNAP_THRESHOLD && dx < bestDx) {
        bestDx = dx
        // Adjust rawX so that myEdge aligns with otherEdge
        snappedX = rawX + (chk.otherEdge - chk.myEdge)
      }
    }

    // Y snaps
    const yChecks = [
      { myEdge: myTop, otherEdge: other.top, label: 'top-top' },
      { myEdge: myBottom, otherEdge: other.bottom, label: 'bot-bot' },
      { myEdge: rawY, otherEdge: other.cy, label: 'cy-cy' },
      { myEdge: myTop, otherEdge: other.bottom, label: 'top-bot' },
      { myEdge: myBottom, otherEdge: other.top, label: 'bot-top' },
      { myEdge: myTop, otherEdge: other.cy, label: 'top-cy' },
      { myEdge: myBottom, otherEdge: other.cy, label: 'bot-cy' },
    ]
    for (const chk of yChecks) {
      const dy = Math.abs(chk.myEdge - chk.otherEdge)
      if (dy < SNAP_THRESHOLD && dy < bestDy) {
        bestDy = dy
        snappedY = rawY + (chk.otherEdge - chk.myEdge)
      }
    }
  }

  // Recalculate my edges after snap
  const sLeft = snappedX - myHalfW
  const sRight = snappedX + myHalfW
  const sTop = snappedY - myHalfH
  const sBottom = snappedY + myHalfH

  // ── Build guide lines for matched edges ──
  for (const other of edgeList) {
    // Vertical guide lines (X-axis alignment)
    for (const xPos of [sLeft, snappedX, sRight]) {
      for (const oPos of [other.left, other.cx, other.right]) {
        if (Math.abs(xPos - oPos) < 0.05) {
          guides.push({ axis: 'x', pos: xPos })
        }
      }
    }
    // Horizontal guide lines (Y-axis alignment)
    for (const yPos of [sTop, snappedY, sBottom]) {
      for (const oPos of [other.top, other.cy, other.bottom]) {
        if (Math.abs(yPos - oPos) < 0.05) {
          guides.push({ axis: 'y', pos: yPos })
        }
      }
    }
  }

  // ── Distance indicators to nearby elements ──
  const realEdges = edgeList.filter(e => !(typeof e.id === 'string' && e.id.startsWith('__')))
  for (const other of realEdges) {
    const dx = Math.abs(snappedX - other.cx)
    const dy = Math.abs(snappedY - other.cy)
    if (dx < 5 && dy > 0.5) {
      const distPx = Math.round(dy / 100 * canvasHeight.value)
      distances.push({
        x1: snappedX, y1: Math.min(snappedY, other.cy),
        x2: snappedX, y2: Math.max(snappedY, other.cy),
        label: distPx + 'px'
      })
    }
    if (dy < 5 && dx > 0.5) {
      const distPx = Math.round(dx / 100 * canvasWidth.value)
      distances.push({
        x1: Math.min(snappedX, other.cx), y1: snappedY,
        x2: Math.max(snappedX, other.cx), y2: snappedY,
        label: distPx + 'px'
      })
    }
  }

  // ── Equal spacing markers ──
  const yPositions = realEdges.map(o => o.cy)
  const allY = [...yPositions, snappedY].sort((a, b) => a - b)
  if (allY.length >= 3) {
    const gaps = []
    for (let i = 0; i < allY.length - 1; i++) gaps.push(allY[i + 1] - allY[i])
    const avgGap = gaps.reduce((s, g) => s + g, 0) / gaps.length
    const allEqual = gaps.every(g => Math.abs(g - avgGap) < EQUAL_SPACING_THRESHOLD)
    if (allEqual && avgGap > 1) {
      for (let i = 0; i < allY.length - 1; i++) {
        equalSpacing.push({
          axis: 'y', from: allY[i], to: allY[i + 1], atX: snappedX,
          label: Math.round(avgGap / 100 * canvasHeight.value) + 'px'
        })
      }
    }
  }
  const xPositions = realEdges.map(o => o.cx)
  const allX = [...xPositions, snappedX].sort((a, b) => a - b)
  if (allX.length >= 3) {
    const gaps = []
    for (let i = 0; i < allX.length - 1; i++) gaps.push(allX[i + 1] - allX[i])
    const avgGap = gaps.reduce((s, g) => s + g, 0) / gaps.length
    const allEqual = gaps.every(g => Math.abs(g - avgGap) < EQUAL_SPACING_THRESHOLD)
    if (allEqual && avgGap > 1) {
      for (let i = 0; i < allX.length - 1; i++) {
        equalSpacing.push({
          axis: 'x', from: allX[i], to: allX[i + 1], atY: snappedY,
          label: Math.round(avgGap / 100 * canvasWidth.value) + 'px'
        })
      }
    }
  }

  // Deduplicate guides
  const uniqueGuides = []
  const seen = new Set()
  for (const g of guides) {
    const key = g.axis + '-' + g.pos.toFixed(1)
    if (!seen.has(key)) { seen.add(key); uniqueGuides.push(g) }
  }

  activeGuides.value = uniqueGuides
  activeDistances.value = distances
  activeEqualSpacing.value = equalSpacing
  return { x: snappedX, y: snappedY }
}

function clearGuides() {
  activeGuides.value = []
  activeDistances.value = []
  activeEqualSpacing.value = []
}

// ─── Computed ───
const gridColor = computed(() => '#F7F9FC')

const canvasStyle = computed(() => ({
  '--primary-color': primaryColor.value,
  '--grid-opacity': gridOpacity.value,
  '--symbols-opacity': symbolsOpacity.value,
  '--vignette-intensity': vignetteIntensity.value,
  background: `linear-gradient(160deg, ${lighten(primaryColor.value, 15)} 0%, ${primaryColor.value} 40%, ${darken(primaryColor.value, 20)} 100%)`
}))

const canvasStyleWithTransform = computed(() => ({
  ...canvasStyle.value,
  width: canvasWidth.value + 'px',
  height: canvasHeight.value + 'px',
  transform: `scale(${previewScale.value / canvasWidth.value})`
}))

const vignetteStyle = computed(() => ({
  background: `radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,${vignetteIntensity.value}) 100%)`
}))

const bgImageStyle = computed(() => {
  const fitMap = {
    cover: { backgroundSize: 'cover' },
    contain: { backgroundSize: 'contain' },
    stretch: { backgroundSize: '100% 100%' },
    original: { backgroundSize: 'auto' }
  }
  return {
    backgroundImage: `url(${bgImageUrl.value})`,
    backgroundPosition: bgImagePosition.value,
    backgroundRepeat: 'no-repeat',
    opacity: bgImageOpacity.value,
    mixBlendMode: bgImageBlend.value,
    ...fitMap[bgImageFit.value]
  }
})

// ─── Upload handlers ───
function handleFileSelect(e) {
  const file = e.target.files?.[0]
  if (file) loadImage(file)
}

function handleDrop(e) {
  const file = e.dataTransfer.files?.[0]
  if (file && file.type.startsWith('image/')) loadImage(file)
}

function loadImage(file) {
  const reader = new FileReader()
  reader.onload = (e) => {
    bgImageUrl.value = e.target.result
    bgImageBase64.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function removeBgImage() {
  bgImageUrl.value = ''
  bgImageBase64.value = ''
}

// ─── Presets ───
function applyPreset(name) {
  switch (name) {
    case 'navy':
      primaryColor.value = '#455e92'
      gridOpacity.value = 0.08
      symbolsOpacity.value = 0.06
      vignetteIntensity.value = 0.65
      break
    case 'dark':
      primaryColor.value = '#0F1E46'
      gridOpacity.value = 0.05
      symbolsOpacity.value = 0.04
      vignetteIntensity.value = 0.75
      break
    case 'light':
      primaryColor.value = '#29428E'
      gridOpacity.value = 0.1
      symbolsOpacity.value = 0.08
      vignetteIntensity.value = 0.5
      break
    case 'gradient':
      primaryColor.value = '#1a1a4e'
      gridOpacity.value = 0.06
      symbolsOpacity.value = 0.05
      vignetteIntensity.value = 0.7
      break
  }
}

// ─── Color helpers ───
function hexToHSL(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255
  const g = parseInt(hex.slice(3, 5), 16) / 255
  const b = parseInt(hex.slice(5, 7), 16) / 255
  const max = Math.max(r, g, b), min = Math.min(r, g, b)
  let h, s, l = (max + min) / 2
  if (max === min) { h = s = 0 } else {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break
      case g: h = ((b - r) / d + 2) / 6; break
      case b: h = ((r - g) / d + 4) / 6; break
    }
  }
  return { h: h * 360, s: s * 100, l: l * 100 }
}

function hslToHex(h, s, l) {
  s /= 100; l /= 100
  const a = s * Math.min(l, 1 - l)
  const f = n => {
    const k = (n + h / 30) % 12
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
    return Math.round(255 * color).toString(16).padStart(2, '0')
  }
  return `#${f(0)}${f(8)}${f(4)}`
}

function lighten(hex, amount) {
  const { h, s, l } = hexToHSL(hex)
  return hslToHex(h, s, Math.min(100, l + amount))
}

function darken(hex, amount) {
  const { h, s, l } = hexToHSL(hex)
  return hslToHex(h, s, Math.max(0, l - amount))
}

// ─── Text wrapping helper for canvas export ───
function wrapCanvasText(ctx, text, maxWidth) {
  const paragraphs = text.split('\n')
  const lines = []
  for (const para of paragraphs) {
    if (para === '') { lines.push(''); continue }
    const words = para.split(' ')
    let currentLine = ''
    for (const word of words) {
      const testLine = currentLine ? currentLine + ' ' + word : word
      if (ctx.measureText(testLine).width > maxWidth && currentLine) {
        lines.push(currentLine)
        currentLine = word
      } else {
        currentLine = testLine
      }
    }
    if (currentLine) lines.push(currentLine)
  }
  return lines.length ? lines : ['']
}

function drawTextWithLetterSpacing(ctx, text, x, y, spacing) {
  const savedAlign = ctx.textAlign
  let totalWidth = 0
  for (const ch of text) totalWidth += ctx.measureText(ch).width + spacing
  totalWidth -= spacing
  let startX = x
  if (savedAlign === 'center') startX = x - totalWidth / 2
  else if (savedAlign === 'right') startX = x - totalWidth
  ctx.textAlign = 'left'
  let cx = startX
  for (const ch of text) {
    ctx.fillText(ch, cx, y)
    cx += ctx.measureText(ch).width + spacing
  }
  ctx.textAlign = savedAlign
}

// ─── LaTeX to Image (for Canvas export) ───
async function renderLatexToImage(latexStr, fontSize, color) {
  const cleanStr = cleanLatexInput(latexStr)
  // Render KaTeX to DOM for measurement
  const measureEl = document.createElement('div')
  measureEl.style.cssText = `position:fixed;left:-9999px;top:-9999px;font-size:${fontSize}px;display:inline-block;`
  katex.render(cleanStr, measureEl, { throwOnError: false, displayMode: true, trust: true })
  document.body.appendChild(measureEl)
  const rect = measureEl.getBoundingClientRect()
  document.body.removeChild(measureEl)
  if (rect.width === 0 || rect.height === 0) return null

  const scale = 2
  const w = Math.ceil(rect.width * scale) + 20
  const h = Math.ceil(rect.height * scale) + 20

  // Render at 2x for quality
  const renderEl = document.createElement('div')
  renderEl.style.cssText = `display:inline-block;padding:10px;font-size:${fontSize * scale}px;color:${color};`
  katex.render(cleanStr, renderEl, { throwOnError: false, displayMode: true, trust: true })

  const serializer = new XMLSerializer()
  const contentXML = serializer.serializeToString(renderEl)

  // Strip @font-face (fonts can't load in SVG image context)
  const cssClean = katexCSSRaw.replace(/@font-face\s*\{[^}]*\}/g, '')

  const svgData = [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">`,
    `<foreignObject width="100%" height="100%">`,
    `<div xmlns="http://www.w3.org/1999/xhtml">`,
    `<style type="text/css"><![CDATA[${cssClean}\n.katex { color: ${color}; }]]></style>`,
    contentXML,
    `</div>`,
    `</foreignObject>`,
    `</svg>`
  ].join('')

  const dataUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgData)
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve({ img, displayWidth: w / scale, displayHeight: h / scale })
    img.onerror = () => resolve(null)
    img.src = dataUrl
  })
}

// ─── Export ───
function generateStandaloneHTML() {
  return `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=${canvasWidth.value}">
<title>OptiTAB – Fond ${canvasWidth.value}×${canvasHeight.value}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/katex.min.css" crossorigin="anonymous">
<style>
/* ═══════════════════════════════════════════════════
   VARIABLES — Modifier ici pour personnaliser
   ═══════════════════════════════════════════════════ */
:root {
  /* 1. Couleur principale */
  --primary: ${primaryColor.value};
  --primary-light: ${lighten(primaryColor.value, 15)};
  --primary-dark: ${darken(primaryColor.value, 20)};
  
  /* 2. Intensité de la grille (0 à 0.3) */
  --grid-opacity: ${gridOpacity.value};
  
  /* 3. Opacité des symboles (0 à 0.25) */
  --symbols-opacity: ${symbolsOpacity.value};
  
  /* 4. Intensité du vignettage (0 à 1) */
  --vignette-intensity: ${vignetteIntensity.value};
  
  /* Couleur de la grille */
  --grid-color: #F7F9FC;
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background: #1a1a1a;
  padding: 20px;
}

/* ═══════════════════════════════════════════════════
   CANVAS PRINCIPAL — ${canvasWidth.value} x ${canvasHeight.value} px
   ═══════════════════════════════════════════════════ */
.reel-canvas {
  position: relative;
  width: ${canvasWidth.value}px;
  height: ${canvasHeight.value}px;
  overflow: hidden;
  /* Dégradé de fond premium */
  background: linear-gradient(160deg, var(--primary-light) 0%, var(--primary) 40%, var(--primary-dark) 100%);
}

/* Image de fond personnalisée */
.bg-image-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

/* ═══════════════════════════════════════════════════
   GRILLE MATHÉMATIQUE
   ═══════════════════════════════════════════════════ */
.grid-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

/* ═══════════════════════════════════════════════════
   SYMBOLES MATHÉMATIQUES DISCRETS
   ═══════════════════════════════════════════════════ */
.symbols-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: var(--symbols-opacity);
  z-index: 3;
}
.math-sym {
  position: absolute;
  color: var(--grid-color);
  font-family: 'Georgia', 'Times New Roman', serif;
  font-weight: 300;
  user-select: none;
}

/* ═══════════════════════════════════════════════════
   VIGNETTAGE
   ═══════════════════════════════════════════════════ */
.vignette-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,var(--vignette-intensity)) 100%);
  z-index: 4;
}

/* Image de fond personnalisée */
.bg-image-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

/* Formules LaTeX */
.latex-overlay-export {
  position: absolute;
  pointer-events: none;
  transform: translate(-50%, -50%);
  z-index: 3;
  line-height: normal;
}

.latex-overlay-export .katex-display {
  margin: 0;
  overflow: visible;
}
</style>
</head>
<body>

<div class="reel-canvas">
  <!-- Image de fond personnalisée -->
  ${bgImageBase64.value ? `<div class="bg-image-layer" style="background-image:url(${bgImageBase64.value});background-size:${bgImageFit.value === 'stretch' ? '100% 100%' : bgImageFit.value === 'original' ? 'auto' : bgImageFit.value};background-position:${bgImagePosition.value};background-repeat:no-repeat;opacity:${bgImageOpacity.value};mix-blend-mode:${bgImageBlend.value}"></div>` : ''}

  <!-- Grille mathématique -->
  <svg class="grid-layer" width="${canvasWidth.value}" height="${canvasHeight.value}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <pattern id="smallGrid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="var(--grid-color)" stroke-width="0.5" stroke-opacity="var(--grid-opacity)" />
      </pattern>
      <pattern id="bigGrid" width="200" height="200" patternUnits="userSpaceOnUse">
        <rect width="200" height="200" fill="url(#smallGrid)" />
        <path d="M 200 0 L 0 0 0 200" fill="none" stroke="var(--grid-color)" stroke-width="1" stroke-opacity="calc(var(--grid-opacity) * 1.5)" />
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#bigGrid)" />
  </svg>

  <!-- Symboles mathématiques -->
  <div class="symbols-layer">
    <span class="math-sym" style="top:8%;left:6%;font-size:28px;transform:rotate(-12deg)">∫</span>
    <span class="math-sym" style="top:5%;right:12%;font-size:22px;transform:rotate(8deg)">∑</span>
    <span class="math-sym" style="top:12%;left:75%;font-size:20px;transform:rotate(-5deg)">π</span>
    <span class="math-sym" style="top:15%;left:20%;font-size:18px;transform:rotate(15deg)">∞</span>
    <span class="math-sym" style="top:22%;right:8%;font-size:24px;transform:rotate(-8deg)">Δ</span>
    <span class="math-sym" style="top:25%;left:10%;font-size:16px;transform:rotate(20deg)">√</span>
    <span class="math-sym" style="top:30%;right:18%;font-size:18px;transform:rotate(-15deg)">∂</span>
    <span class="math-sym" style="bottom:28%;left:8%;font-size:22px;transform:rotate(10deg)">θ</span>
    <span class="math-sym" style="bottom:25%;right:10%;font-size:20px;transform:rotate(-18deg)">λ</span>
    <span class="math-sym" style="bottom:18%;left:22%;font-size:16px;transform:rotate(6deg)">α</span>
    <span class="math-sym" style="bottom:15%;right:20%;font-size:24px;transform:rotate(-10deg)">∮</span>
    <span class="math-sym" style="bottom:8%;left:12%;font-size:18px;transform:rotate(12deg)">ε</span>
    <span class="math-sym" style="bottom:5%;right:6%;font-size:26px;transform:rotate(-6deg)">Σ</span>
    <span class="math-sym" style="top:3%;left:45%;font-size:14px;transform:rotate(3deg)">f(x)</span>
    <span class="math-sym" style="bottom:3%;left:55%;font-size:14px;transform:rotate(-4deg)">dy/dx</span>
    <span class="math-sym" style="top:35%;left:4%;font-size:16px;transform:rotate(7deg)">±</span>
    <span class="math-sym" style="bottom:35%;right:5%;font-size:18px;transform:rotate(-12deg)">≈</span>
    <span class="math-sym" style="top:18%;left:88%;font-size:15px;transform:rotate(14deg)">∇</span>
    <span class="math-sym" style="bottom:12%;left:85%;font-size:16px;transform:rotate(-9deg)">φ</span>
    <span class="math-sym" style="top:9%;left:40%;font-size:13px;transform:rotate(5deg)">lim</span>
  </div>

  <!-- Images overlay -->
  ${imageOverlays.value.filter(o => o.base64).map(o => `<img src="${o.base64}" style="position:absolute;left:${o.x}%;top:${o.y}%;width:${o.widthPct}%;opacity:${o.opacity};transform:translate(-50%,-50%) rotate(${o.rotation}deg);pointer-events:none;z-index:3;" />`).join('\n  ')}

  <!-- Textes libres -->
  ${textOverlays.value.map(t => `<div style="position:absolute;left:${t.x}%;top:${t.y}%;width:${t.boxWidth}%;transform:translate(-50%,-50%) rotate(${t.rotation}deg);opacity:${t.opacity};z-index:4;pointer-events:none;"><div style="font-size:${t.fontSize}px;font-family:${t.fontFamily};font-weight:${t.bold ? 'bold' : 'normal'};font-style:${t.italic ? 'italic' : 'normal'};color:${t.color};text-align:${t.align};text-shadow:${t.shadow ? '2px 2px 8px rgba(0,0,0,0.6)' : 'none'};letter-spacing:${t.letterSpacing}px;line-height:${t.lineHeight};white-space:pre-wrap;word-wrap:break-word;">${t.text}</div></div>`).join('\n  ')}

  <!-- Formules LaTeX -->
  ${latexOverlays.value.map(o => `<div class="latex-overlay-export" style="left:${o.x}%;top:${o.y}%;font-size:${o.fontSize}px;color:${o.color};">${katex.renderToString(cleanLatexInput(o.latex), { throwOnError: false, displayMode: true, trust: true })}</div>`).join('\n  ')}

  <!-- Vignettage -->
  <div class="vignette-layer"></div>
</div>

</body>
</html>`
}

function openInNewTab() {
  const html = generateStandaloneHTML()
  const blob = new Blob([html], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank')
}

async function exportPNG() {
  const el = reelCanvas.value
  if (!el) return

  const W = canvasWidth.value
  const H = canvasHeight.value
  const SCALE = 2 // haute résolution 2x

  // Désélectionner le texte pour cacher les poignées de resize
  const prevSelected = selectedTextId.value
  selectedTextId.value = null

  // Cacher les guides d'alignement
  const prevGuides = [...activeGuides.value]
  const prevDistances = [...activeDistances.value]
  const prevEqualSpacing = [...activeEqualSpacing.value]
  activeGuides.value = []
  activeDistances.value = []
  activeEqualSpacing.value = []

  // Cacher la zone safe
  const safeZoneEl = el.querySelector('.safe-zone-indicator')
  if (safeZoneEl) safeZoneEl.style.display = 'none'

  // Attendre un tick pour que Vue retire les poignées du DOM
  await new Promise(r => setTimeout(r, 50))

  // Temporairement remettre le canvas à sa taille réelle (retirer le scale CSS)
  const origTransform = el.style.transform
  const origWidth = el.style.width
  const origHeight = el.style.height
  el.style.transform = 'none'
  el.style.width = W + 'px'
  el.style.height = H + 'px'

  try {
    const canvas = await html2canvas(el, {
      scale: SCALE,
      width: W,
      height: H,
      useCORS: true,
      allowTaint: true,
      backgroundColor: null,
      logging: false,
    })

    const link = document.createElement('a')
    link.download = 'optitab-reel-background.png'
    link.href = canvas.toDataURL('image/png')
    link.click()
  } catch (e) {
    console.error('Erreur export PNG:', e)
    alert('Erreur lors de l\'export. Veuillez réessayer.')
  } finally {
    // Restaurer le transform CSS du preview
    el.style.transform = origTransform
    el.style.width = origWidth
    el.style.height = origHeight
    selectedTextId.value = prevSelected
    activeGuides.value = prevGuides
    activeDistances.value = prevDistances
    activeEqualSpacing.value = prevEqualSpacing
    // Restaurer la zone safe
    if (safeZoneEl) safeZoneEl.style.display = ''
  }
}

// ─── Drag & zoom overlay images ───
const draggingOverlay = ref(null)
let dragStartX = 0
let dragStartY = 0
let dragStartOvX = 0
let dragStartOvY = 0

function startDragOverlay(e, imgOv) {
  draggingOverlay.value = imgOv
  dragStartX = e.clientX
  dragStartY = e.clientY
  dragStartOvX = imgOv.x
  dragStartOvY = imgOv.y
  window.addEventListener('mousemove', onDragOverlay)
  window.addEventListener('mouseup', stopDragOverlay)
}

function onDragOverlay(e) {
  if (!draggingOverlay.value) return
  const scale = previewScale.value / canvasWidth.value
  const dx = (e.clientX - dragStartX) / scale
  const dy = (e.clientY - dragStartY) / scale
  const bounds = getOverlayMoveBounds('image', draggingOverlay.value.id)
  const rawX = dragStartOvX + (dx / canvasWidth.value) * 100
  const rawY = dragStartOvY + (dy / canvasHeight.value) * 100
  const clampedX = clampValue(rawX, bounds.minX, bounds.maxX)
  const clampedY = clampValue(rawY, bounds.minY, bounds.maxY)
  const snapped = computeSnap(clampedX, clampedY, draggingOverlay.value.id, 'image')
  draggingOverlay.value.x = clampValue(snapped.x, bounds.minX, bounds.maxX)
  draggingOverlay.value.y = clampValue(snapped.y, bounds.minY, bounds.maxY)
}

function stopDragOverlay() {
  draggingOverlay.value = null
  clearGuides()
  window.removeEventListener('mousemove', onDragOverlay)
  window.removeEventListener('mouseup', stopDragOverlay)
}

function wheelZoomOverlay(e, imgOv) {
  const delta = e.deltaY > 0 ? -2 : 2
  imgOv.widthPct = Math.max(5, Math.min(200, imgOv.widthPct + delta))
  clampOverlayToBounds(imgOv, 'image')
}

// ── Bloquer le scroll parent ──
function onKeyDown(e) {
  const isModifier = e.ctrlKey || e.metaKey
  const key = (e.key || '').toLowerCase()
  const tag = document.activeElement?.tagName

  if (isModifier && (key === 'c' || key === 'v')) {
    // Preserve native copy/paste when editing inputs/textareas.
    if (tag === 'INPUT' || tag === 'TEXTAREA') return
    if (key === 'c') {
      const copied = copySelectedOverlay()
      if (copied) e.preventDefault()
      return
    }
    if (key === 'v') {
      const pasted = pasteOverlayFromClipboard()
      if (pasted) e.preventDefault()
      return
    }
  }

  if (e.key === 'Delete' || e.key === 'Backspace') {
    // Preserve native delete behavior when editing inputs/textareas.
    if (tag === 'INPUT' || tag === 'TEXTAREA') return

    if (selectedTextId.value !== null) {
      removeTextOverlay(selectedTextId.value)
      clearGuides()
      e.preventDefault()
      showToast('Texte supprimé')
      return
    }

    if (selectedLatexId.value !== null) {
      removeLatexOverlay(selectedLatexId.value)
      clearGuides()
      e.preventDefault()
      showToast('Formule supprimée')
      return
    }
  }

  if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
    // Don't move if user is typing in an input/textarea
    if (tag === 'INPUT' || tag === 'TEXTAREA') return

    const step = e.shiftKey ? 5 : 1 // Shift = 5px, sinon 1px

    let target = null
    let targetType = null
    if (selectedTextId.value !== null) {
      target = textOverlays.value.find(t => t.id === selectedTextId.value)
      targetType = 'text'
    } else if (selectedLatexId.value !== null) {
      target = latexOverlays.value.find(o => o.id === selectedLatexId.value)
      targetType = 'latex'
    }
    if (!target || !targetType) return

    e.preventDefault()
    const dxPct = step / canvasWidth.value * 100
    const dyPct = step / canvasHeight.value * 100
    const bounds = getOverlayMoveBounds(targetType, target.id)

    if (e.key === 'ArrowLeft') target.x = clampValue(target.x - dxPct, bounds.minX, bounds.maxX)
    if (e.key === 'ArrowRight') target.x = clampValue(target.x + dxPct, bounds.minX, bounds.maxX)
    if (e.key === 'ArrowUp') target.y = clampValue(target.y - dyPct, bounds.minY, bounds.maxY)
    if (e.key === 'ArrowDown') target.y = clampValue(target.y + dyPct, bounds.minY, bounds.maxY)
  }
}

// ─── Toast notification ───
const toastMsg = ref('')
const toastType = ref('success')
let toastTimer = null
function showToast(msg, type = 'success', duration = 3000) {
  toastMsg.value = msg
  toastType.value = type
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toastMsg.value = '' }, duration)
}

// ─── Sauvegarde / Chargement de projets (fichier local) ───
const fileInputRef = ref(null)

function getProjectData() {
  saveCurrentSlideState()
  return {
    _savedAt: new Date().toLocaleString('fr-FR'),
    _version: 1,
    canvasWidth: canvasWidth.value,
    canvasHeight: canvasHeight.value,
    safeZoneV: safeZoneV.value,
    safeZoneH: safeZoneH.value,
    previewScale: previewScale.value,
    slides: JSON.parse(JSON.stringify(slides.value)),
    currentSlideIndex: currentSlideIndex.value,
  }
}

function saveProjectToFile() {
  const name = prompt('Nom du fichier :', 'mon-projet')
  if (!name || !name.trim()) return
  const key = name.trim().replace(/[^a-zA-Z0-9_\-\u00C0-\u024F]/g, '_')
  try {
    const data = getProjectData()
    const json = JSON.stringify(data, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = key + '.json'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showToast('Fichier « ' + key + '.json » téléchargé ✓')
  } catch (e) {
    console.error('[OptiTAB] Erreur sauvegarde fichier:', e)
    showToast('Erreur lors de la sauvegarde.', 'error')
  }
}

function triggerLoadProject() {
  fileInputRef.value?.click()
}

function loadProjectFromFile(event) {
  const file = event.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const proj = JSON.parse(e.target.result)
      if (!proj.slides || !Array.isArray(proj.slides)) {
        showToast('Fichier invalide : pas de slides.', 'error')
        return
      }
      canvasWidth.value = proj.canvasWidth || 1080
      canvasHeight.value = proj.canvasHeight || 1920
      safeZoneV.value = proj.safeZoneV ?? 325
      safeZoneH.value = proj.safeZoneH ?? 95
      previewScale.value = proj.previewScale || 360
      slides.value = proj.slides
      currentSlideIndex.value = Math.min(proj.currentSlideIndex || 0, slides.value.length - 1)
      loadSlideState(currentSlideIndex.value)
      showToast('Projet chargé depuis « ' + file.name + ' » ✓')
    } catch (err) {
      console.error('[OptiTAB] Erreur lecture fichier:', err)
      showToast('Fichier JSON invalide.', 'error')
    }
  }
  reader.readAsText(file)
  // Reset pour pouvoir recharger le même fichier
  event.target.value = ''
}

onMounted(() => {
  window.addEventListener('keydown', onKeyDown)
  const main = document.querySelector('.dashboard-main')
  if (main) {
    main.style.padding = '0'
    main.style.overflow = 'hidden'
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyDown)
  const main = document.querySelector('.dashboard-main')
  if (main) {
    main.style.padding = ''
    main.style.overflow = ''
  }
})
</script>

<style scoped>
.reel-bg-admin {
  flex: 1;
  min-height: 0;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ── Main Layout ── */
.main-layout {
  display: flex;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* ── Preview (centre) ── */
.preview-column {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: transparent;
  position: relative;
}

.preview-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.preview-label {
  font-size: 0.7rem;
  color: rgba(0,0,0,0.35);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.preview-container {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  border: none;
}

.reel-canvas {
  position: relative;
  overflow: hidden;
  transform-origin: top left;
}

/* ── Sidebar droite ── */
.sidebar-column {
  width: 320px;
  flex-shrink: 0;
  background: #f8f9fb;
  border-left: 1px solid #e2e6ed;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  /* Prendre toute la hauteur disponible via le flex parent */
  align-self: stretch;
}

.sidebar-header {
  padding: 10px 14px;
  border-bottom: 1px solid #e2e6ed;
  background: white;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-header h2 {
  font-size: 0.95rem;
  color: #1F3F8F;
  margin: 0;
  font-weight: 700;
}

.sidebar-header-actions {
  display: flex;
  gap: 6px;
}

.btn-header-action {
  padding: 5px 10px;
  border: 1px solid #d0d5dd;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  background: white;
  color: #444;
  transition: all 0.15s;
}

.btn-header-action:hover {
  border-color: #1F3F8F;
  color: #1F3F8F;
}

.btn-header-action.primary {
  background: #1F3F8F;
  color: white;
  border-color: #1F3F8F;
}

.btn-header-action.primary:hover {
  background: #122A5A;
}

/* ── Tabs ── */
.sidebar-tabs {
  display: flex;
  border-bottom: 2px solid #e2e6ed;
  background: white;
  flex-shrink: 0;
}

.sidebar-tab {
  flex: 1;
  padding: 9px 0;
  font-size: 0.75rem;
  font-weight: 600;
  color: #888;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-tab:hover {
  color: #1F3F8F;
  background: #f7f8fc;
}

.sidebar-tab.active {
  color: #1F3F8F;
  border-bottom-color: #1F3F8F;
}

/* ── Sidebar scroll ── */
.sidebar-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* ── Sections (replacing old panels) ── */
.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-title {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1F3F8F;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.section-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-add-item {
  padding: 4px 10px;
  background: #1F3F8F;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-add-item:hover {
  background: #122A5A;
}

.empty-hint {
  color: #999;
  font-size: 0.76rem;
  font-style: italic;
}

/* Project actions */
.project-actions-row {
  display: flex;
  gap: 8px;
}
.btn-project-action {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #d0d5dd;
  border-radius: 7px;
  background: white;
  color: #1f3f8f;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  text-align: center;
}
.btn-project-action:hover {
  background: #eef1f8;
  border-color: #1f3f8f;
}

/* Toast notification */
.toast-notification {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  text-align: center;
  animation: toast-in 0.3s ease;
}
.toast-notification.success {
  background: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #a5d6a7;
}
.toast-notification.error {
  background: #fce4ec;
  color: #c62828;
  border: 1px solid #ef9a9a;
}
.toast-fade-enter-active { animation: toast-in 0.3s ease; }
.toast-fade-leave-active { animation: toast-in 0.3s ease reverse; }
@keyframes toast-in {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.btn-header-action.save {
  background: #2d8a4e;
  color: white;
}

.item-card {
  border: 1px solid #e2e6ed;
  border-radius: 7px;
  padding: 10px;
  background: white;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.item-card-num {
  font-size: 0.76rem;
  font-weight: 700;
  color: #1F3F8F;
}

/* ── Formula / Text list ── */
.formula-list-item {
  border: 1px solid #e2e6ed;
  border-radius: 7px;
  background: white;
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s;
  overflow: hidden;
}

.text-list-preview {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
  pointer-events: none;
}
.formula-list-item:hover {
  border-color: #b0bdd4;
}
.formula-list-item.selected {
  border-color: #1F3F8F;
  box-shadow: 0 0 0 2px rgba(31, 63, 143, 0.13);
}
.formula-list-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
}
.formula-list-num {
  font-size: 0.7rem;
  font-weight: 700;
  color: #1F3F8F;
  background: #eef1f8;
  border-radius: 4px;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.formula-list-preview {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
  font-size: 14px;
  color: #1F3F8F;
  pointer-events: none;
}
.formula-list-preview .katex {
  font-size: 0.9em;
}

.formula-list-preview :deep(.katex-display),
.latex-preview-mini :deep(.katex-display) {
  margin: 0;
}
.formula-props {
  padding: 10px;
  border-top: 1px solid #e2e6ed;
  display: flex;
  flex-direction: column;
  gap: 8px;
  cursor: default;
}

.dim-sep {
  color: #999;
  font-size: 0.85rem;
}

.sidebar-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

/* ── Controls ── */
.control-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.control-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #333;
}

.control-group label .val {
  font-weight: 400;
  color: #999;
  font-size: 0.72rem;
}

.color-row {
  display: flex;
  gap: 6px;
  align-items: center;
}

.color-row input[type="color"] {
  width: 34px;
  height: 34px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  padding: 2px;
  flex-shrink: 0;
}

.color-input {
  flex: 1;
  min-width: 0;
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 0.82rem;
  font-family: 'Courier New', monospace;
  letter-spacing: 0.5px;
}

.color-input:focus {
  outline: none;
  border-color: #1F3F8F;
  box-shadow: 0 0 0 2px rgba(31,63,143,0.15);
}

input[type="range"] {
  width: 100%;
  accent-color: #1F3F8F;
}

.presets {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.preset-btn {
  padding: 4px 10px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.preset-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.preset-btn.navy { background: #122A5A; color: white; border-color: #122A5A; }
.preset-btn.dark { background: #0F1E46; color: white; border-color: #0F1E46; }
.preset-btn.light { background: #29428E; color: white; border-color: #29428E; }
.preset-btn.gradient { background: linear-gradient(135deg, #1a1a4e, #29428E); color: white; border-color: #1a1a4e; }

/* ── Format presets ── */
.format-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 6px;
}
.format-btn {
  padding: 4px 8px;
  font-size: 0.7rem;
  border: 1px solid #d0d5dd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  color: #333;
  transition: all 0.15s;
}
.format-btn:hover {
  border-color: #1F3F8F;
  color: #1F3F8F;
}
.format-btn.active {
  background: #1F3F8F;
  color: white;
  border-color: #1F3F8F;
}
.format-custom {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #666;
}
.dim-input {
  width: 65px;
  padding: 4px 6px;
  border: 1px solid #d0d5dd;
  border-radius: 4px;
  font-size: 0.8rem;
  text-align: center;
}

/* \u2500\u2500 Upload \u2500\u2500 */\n.upload-zone {
  border: 2px dashed #c5cce0;
  border-radius: 7px;
  padding: 10px 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #fafbfc;
}

.upload-zone:hover {
  border-color: #1F3F8F;
  background: #F7F9FC;
}

.upload-placeholder {
  color: #999;
  font-size: 0.78rem;
  cursor: pointer;
  pointer-events: none;
}

.upload-done {
  color: #27ae60;
  font-size: 0.78rem;
  font-weight: 500;
  cursor: pointer;
  pointer-events: none;
}

.btn-remove-bg {
  padding: 3px 8px;
  border: 1px solid #e74c3c;
  background: white;
  color: #e74c3c;
  border-radius: 5px;
  font-size: 0.72rem;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-start;
}

.btn-remove-bg:hover {
  background: #e74c3c;
  color: white;
}

.select-input {
  padding: 5px 8px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 0.78rem;
  background: white;
  cursor: pointer;
}

.select-input:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ── Canvas layers ── */
.grid-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.symbols-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.math-sym {
  position: absolute;
  color: #F7F9FC;
  font-family: 'Georgia', 'Times New Roman', serif;
  font-weight: 300;
  user-select: none;
}

.vignette-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.bg-image-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.safe-zone-indicator {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 5;
}

.safe-zone-top,
.safe-zone-bottom,
.safe-zone-left,
.safe-zone-right {
  position: absolute;
  background: repeating-linear-gradient(
    -45deg,
    rgba(255, 45, 135, 0.04),
    rgba(255, 45, 135, 0.04) 4px,
    transparent 4px,
    transparent 10px
  );
  border: none;
}

.safe-zone-top {
  top: 0;
  left: 0;
  right: 0;
  border-bottom: 1px dashed rgba(255, 45, 135, 0.25);
}

.safe-zone-bottom {
  bottom: 0;
  left: 0;
  right: 0;
  border-top: 1px dashed rgba(255, 45, 135, 0.25);
}

.safe-zone-left {
  top: 0;
  bottom: 0;
  left: 0;
  border-right: 1px dashed rgba(255, 45, 135, 0.25);
}

.safe-zone-right {
  top: 0;
  bottom: 0;
  right: 0;
  border-left: 1px dashed rgba(255, 45, 135, 0.25);
}

/* ── Guides d'alignement (style Canva) ── */
.guides-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 50;
  overflow: visible;
}

.guide-line {
  stroke: #FF2D87;
  stroke-width: 1.5;
  stroke-dasharray: 6 3;
  opacity: 0.85;
}

.distance-line {
  stroke: #FF2D87;
  stroke-width: 1;
  stroke-dasharray: 3 2;
  opacity: 0.7;
  marker-start: url(#arrowStart);
  marker-end: url(#arrowEnd);
}

.distance-label-bg {
  fill: #FF2D87;
  opacity: 0.9;
}

.distance-label {
  fill: white;
  font-size: 13px;
  font-weight: 700;
  font-family: 'Arial', sans-serif;
  text-anchor: middle;
  dominant-baseline: middle;
}

/* Equal spacing markers */
.equal-spacing-line {
  stroke: #8B5CF6;
  stroke-width: 2;
  stroke-dasharray: 4 3;
  opacity: 0.9;
}

.equal-spacing-bg {
  fill: #8B5CF6;
  opacity: 0.9;
}

.equal-spacing-label {
  fill: white;
  font-size: 11px;
  font-weight: 700;
  font-family: 'Arial', sans-serif;
  text-anchor: middle;
  dominant-baseline: middle;
}

/* ── LaTeX ── */
.latex-textarea {
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
}

.latex-hint {
  font-size: 0.72rem;
  color: #888;
  background: #f4f5f8;
  border: 1px solid #e2e6ed;
  border-radius: 6px;
  padding: 7px 10px;
  line-height: 1.5;
}

.latex-hint code {
  background: #e8eaf2;
  border-radius: 3px;
  padding: 1px 4px;
  font-size: 0.7rem;
  color: #1F3F8F;
}

/* old classes kept for compat – now unused */

.btn-remove-overlay {
  padding: 2px 8px;
  border: 1px solid #e74c3c;
  background: white;
  color: #e74c3c;
  border-radius: 4px;
  font-size: 0.72rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-remove-overlay:hover {
  background: #e74c3c;
  color: white;
}

.latex-text-input {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 0.78rem;
  font-family: 'Courier New', monospace;
  background: white;
}

.latex-text-input:focus {
  outline: none;
  border-color: #1F3F8F;
  box-shadow: 0 0 0 2px rgba(31, 63, 143, 0.15);
}

.latex-preview-mini {
  margin-top: 3px;
  padding: 5px 8px;
  background: #1F3F8F;
  border-radius: 5px;
  color: white;
  min-height: 28px;
  display: flex;
  align-items: center;
  overflow-x: auto;
}

.latex-preview-mini :deep(.katex) {
  color: white;
}

/* ── Overlays in preview ── */
.latex-overlay-wrapper {
  position: absolute;
  pointer-events: none;
  transform: translate(-50%, -50%);
  z-index: 3;
  line-height: normal;
}

.latex-overlay-wrapper.latex-dragging {
  z-index: 10;
}

.latex-overlay-wrapper.latex-selected {
  outline: 2px dashed rgba(31, 63, 143, 0.6);
  outline-offset: 4px;
  border-radius: 4px;
  z-index: 10;
}

.latex-overlay-content {
  pointer-events: auto;
  cursor: grab;
  user-select: none;
  width: fit-content;
}

.latex-overlay-wrapper.latex-dragging .latex-overlay-content {
  cursor: grabbing;
}

.latex-overlay-wrapper :deep(.katex) {
  color: inherit;
}

.latex-overlay-wrapper :deep(.katex-display) {
  margin: 0;
  overflow: visible;
}

.text-overlay-wrapper {
  position: absolute;
  pointer-events: none;
  z-index: 3;
  box-sizing: border-box;
  -webkit-user-drag: none;
}

.text-overlay-wrapper.text-dragging {
  cursor: grabbing;
  z-index: 10;
}

.text-overlay-wrapper.text-selected {
  outline: 2px solid rgba(31, 63, 143, 0.5);
  outline-offset: 2px;
  border-radius: 3px;
  z-index: 10;
}

.text-overlay-content {
  width: fit-content;
  max-width: 100%;
  word-wrap: break-word;
  overflow-wrap: break-word;
  pointer-events: auto;
  cursor: grab;
  user-select: none;
  -webkit-user-drag: none;
}

/* Poignées de redimensionnement */
.resize-handle {
  position: absolute;
  top: 0;
  width: 8px;
  height: 100%;
  cursor: ew-resize;
  z-index: 10;
  pointer-events: auto;
}

.resize-handle::after {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 28px;
  background: #1F3F8F;
  border-radius: 3px;
  opacity: 0.7;
  transition: opacity 0.15s;
}

.resize-handle:hover::after {
  opacity: 1;
}

.resize-handle.resize-left {
  left: -6px;
}
.resize-handle.resize-left::after {
  left: 0;
}

.resize-handle.resize-right {
  right: -6px;
}
.resize-handle.resize-right::after {
  right: 0;
}

.image-overlay-preview {
  position: absolute;
  pointer-events: auto;
  z-index: 3;
  height: auto;
  object-fit: contain;
  cursor: grab;
  user-select: none;
}

/* ── Text controls ── */
.text-textarea {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 0.78rem;
  background: white;
  resize: vertical;
  font-family: inherit;
}

.text-textarea:focus {
  outline: none;
  border-color: #1F3F8F;
  box-shadow: 0 0 0 2px rgba(31,63,143,0.15);
}

.text-style-row {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.style-btn {
  padding: 4px 8px;
  border: 1px solid #d0d5dd;
  border-radius: 5px;
  background: white;
  color: #444;
  font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.15s;
  min-width: 30px;
}

.style-btn:hover {
  border-color: #1F3F8F;
  color: #1F3F8F;
}

.style-btn.active {
  background: #1F3F8F;
  color: white;
  border-color: #1F3F8F;
}

.image-overlay-preview.img-dragging {
  cursor: grabbing;
}

.img-overlay-thumb {
  border-radius: 5px;
  overflow: hidden;
  border: 1px solid #e2e6ed;
  max-height: 60px;
}

.img-overlay-thumb img {
  width: 100%;
  height: 100%;
  max-height: 60px;
  object-fit: cover;
}

/* ── Filmstrip diapos ── */
.filmstrip {
  width: 100%;
  padding: 3px 12px;
  background: #f8f9fb;
  border-top: 1px solid #e2e6ed;
  flex-shrink: 0;
}

.filmstrip-slides {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 2px;
}

.filmstrip-slides::-webkit-scrollbar {
  height: 4px;
}

.filmstrip-slides::-webkit-scrollbar-thumb {
  background: #c5cad3;
  border-radius: 2px;
}

.filmstrip-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  flex-shrink: 0;
}

.filmstrip-thumb {
  width: 38px;
  height: calc(38px * var(--canvas-ratio, 1.778));
  border-radius: 6px;
  border: 2px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.15s, box-shadow 0.15s;
  position: relative;
  overflow: hidden;
}

.filmstrip-item.active .filmstrip-thumb {
  border-color: #455e92;
  box-shadow: 0 0 0 2px rgba(69, 94, 146, 0.25);
}

.filmstrip-item:hover:not(.active) .filmstrip-thumb {
  border-color: #b0bdd0;
}

.filmstrip-num {
  font-size: 13px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.7);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.filmstrip-actions {
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.15s;
  z-index: 2;
  background: rgba(0,0,0,0.45);
  border-radius: 4px;
  padding: 1px 3px;
}

.filmstrip-item:hover .filmstrip-actions,
.filmstrip-item.active .filmstrip-actions {
  opacity: 1;
}

.filmstrip-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 11px;
  color: rgba(255,255,255,0.85);
  padding: 1px 3px;
  border-radius: 3px;
  line-height: 1;
  transition: background 0.12s, color 0.12s;
}

.filmstrip-btn:hover {
  background: rgba(255,255,255,0.25);
  color: #fff;
}

.filmstrip-btn.del:hover {
  background: rgba(192, 57, 43, 0.6);
  color: #fff;
}

.filmstrip-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.filmstrip-add {
  width: 38px;
  height: calc(38px * var(--canvas-ratio, 1.778));
  border-radius: 5px;
  border: 2px dashed #c5cad3;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  color: #8e99a8;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
}

.filmstrip-add:hover {
  border-color: #455e92;
  color: #455e92;
  background: rgba(69, 94, 146, 0.05);
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .reel-bg-admin {
    height: auto;
    overflow: auto;
  }
  .main-layout {
    flex-direction: column;
  }
  .preview-column {
    min-height: 500px;
  }
  .sidebar-column {
    width: 100%;
    border-left: none;
    border-top: 1px solid #e2e6ed;
    height: auto;
  }
}
</style>
