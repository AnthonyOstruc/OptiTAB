<template>
  <section class="reel-preview-panel">
    <div class="preview-header">
      <div class="preview-header-right">
        <button
          class="btn-fullscreen btn-png-export"
          type="button"
          :disabled="!slidesForRender.length || exportingPng || isVideoExportBusy"
          @click="exportAllSlidesPng"
        >
          {{ exportingPng ? `PNG ${pngExportProgress}/${slidesForRender.length}` : 'Exporter PNG' }}
        </button>
        <button
          class="btn-fullscreen btn-video-export"
          type="button"
          :disabled="!videoSlidesForRender.length || exportingPng || isVideoExportBusy"
          @click="exportAllSlidesVideo('hq')"
        >
          {{ videoHqExportButtonLabel }}
        </button>
        <div class="math-size-controls" aria-label="Taille des formules">
          <button class="size-button" type="button" @click="decreaseMathSize">A-</button>
          <span class="size-value">{{ mathSizePercent }}%</span>
          <button class="size-button" type="button" @click="increaseMathSize">A+</button>
          <button class="size-reset" type="button" @click="resetMathSize">Reset</button>
        </div>
        <button
          class="subtitles-toggle"
          :class="{ 'subtitles-toggle--active': showSubtitles }"
          type="button"
          :aria-pressed="showSubtitles ? 'true' : 'false'"
          aria-label="Afficher ou masquer les sous-titres"
          @click="toggleSubtitles"
        >
          <svg class="subtitles-toggle-icon" viewBox="0 0 24 24" aria-hidden="true">
            <rect x="3" y="5" width="18" height="14" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
            <rect x="6.5" y="11" width="4.5" height="1.6" rx="0.8" fill="currentColor"/>
            <rect x="12.5" y="11" width="5" height="1.6" rx="0.8" fill="currentColor"/>
            <rect x="6.5" y="14.5" width="6.5" height="1.6" rx="0.8" fill="currentColor"/>
            <rect x="14.5" y="14.5" width="3" height="1.6" rx="0.8" fill="currentColor"/>
          </svg>
          <span class="subtitles-toggle-label">Sous-titres</span>
        </button>
        <div
          v-if="slidesForRender.length"
          class="preview-gap-controls"
          aria-label="Espacement vertical entre les lignes"
        >
          <span class="preview-gap-label">Lignes</span>
          <button
            class="size-button cumulative-gap-button"
            type="button"
            aria-label="Reduire le vide entre les lignes"
            @click="decreaseCumulativeGap"
          >
            -
          </button>
          <span class="size-value cumulative-gap-value">{{ cumulativeGapLabel }}</span>
          <button
            class="size-button cumulative-gap-button"
            type="button"
            aria-label="Augmenter le vide entre les lignes"
            @click="increaseCumulativeGap"
          >
            +
          </button>
          <button class="size-reset" type="button" @click="resetCumulativeGap">Reset</button>
        </div>
        <span v-if="slidesForRender.length" class="preview-count">{{ slidesForRender.length }} slides</span>
        <span v-if="totalReelDurationLabel" class="preview-count preview-count--duration">{{ totalReelDurationLabel }}</span>
      </div>
    </div>

    <p v-if="!slidesForRender.length" class="empty-state">Aucune slide à afficher.</p>

    <div v-else v-show="!isYoutubeFormat || !isFullscreen" class="reel-preview-list">
      <ReelSlidePreview
        v-for="slide in slidesForRender"
        :key="slide.id"
        :slide="slide"
        :is-selected="Number(selectedSlideId) === Number(slide.id)"
        :math-scale="getMathScale(slide)"
        :safe-zone-x-scale="safeZoneXScale"
        :safe-zone-y-scale="getSafeZoneYScale(slide)"
        :clickable="!isVirtualCoverSlide(slide)"
        :video-format="format"
        :show-subtitles="showSubtitles"
        @select="handleSelectSlide(slide.id)"
        @open="handleOpenSlideFullscreen(slide.id)"
        @diagnostic="$emit('diagnostic', $event)"
      />
    </div>

    <div v-if="pngExportMounted" class="png-export-area" :style="exportFrameStyle" aria-hidden="true">
      <div
        v-for="(slide, index) in slidesForRender"
        :key="`png-export-${slide.id || index}`"
        :ref="(el) => setExportSlideRef(el, index)"
        class="png-export-frame"
        :style="exportFrameStyle"
      >
        <ReelSlidePreview
          :slide="slide"
          :is-selected="false"
          display-mode="export"
          :clickable="false"
          :math-scale="getMathScale(slide)"
          :safe-zone-x-scale="safeZoneXScale"
          :safe-zone-y-scale="getSafeZoneYScale(slide)"
          :video-format="format"
          :show-subtitles="showSubtitles"
          @diagnostic="$emit('diagnostic', $event)"
        />
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="pronunciationEditorOpen"
        class="pronunciation-modal-backdrop"
        @click.self="closePronunciationEditor"
      >
        <div class="pronunciation-modal" role="dialog" aria-label="Éditer la prononciation">
          <h4 class="pronunciation-modal-title">Prononciation</h4>
          <p class="pronunciation-modal-word">
            Mot : <strong>{{ pronunciationEditorWord }}</strong>
          </p>
          <label class="pronunciation-modal-label" for="pronunciation-input">
            Comment ce mot doit être prononcé ?
          </label>
          <input
            id="pronunciation-input"
            ref="pronunciationInputRef"
            v-model="pronunciationEditorPronunciation"
            class="pronunciation-modal-input"
            type="text"
            maxlength="160"
            placeholder="Ex : Optitabe"
            @keydown.enter.prevent="commitPronunciationFromEditor"
            @keydown.esc.prevent="closePronunciationEditor"
            @keydown.stop
          />

          <label class="pronunciation-modal-label" for="pronunciation-language">
            Langue de prononciation
          </label>
          <select
            id="pronunciation-language"
            v-model="pronunciationEditorLanguage"
            class="pronunciation-modal-input pronunciation-modal-select"
            @keydown.stop
          >
            <option v-for="lang in PRONUNCIATION_LANGUAGES" :key="lang.code" :value="lang.code">
              {{ lang.label }}
            </option>
          </select>

          <p class="pronunciation-modal-hint">
            Saisis l'écriture phonétique souhaitée. Si tu choisis une langue différente du français, le mot sera signalé au moteur vocal pour qu'il l'articule dans cette langue.
          </p>
          <div class="pronunciation-modal-actions">
            <button
              class="pronunciation-modal-btn pronunciation-modal-btn--remove"
              type="button"
              :disabled="!pronunciationOverridesByLowerWord.has(pronunciationEditorWord.toLowerCase())"
              @click="removePronunciationFromEditor"
            >
              Retirer
            </button>
            <button
              class="pronunciation-modal-btn pronunciation-modal-btn--cancel"
              type="button"
              @click="closePronunciationEditor"
            >
              Annuler
            </button>
            <button
              class="pronunciation-modal-btn pronunciation-modal-btn--save"
              type="button"
              @click="commitPronunciationFromEditor"
            >
              Enregistrer
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Hidden audio element dedicated to full preview playback (separate from the visible controls player) -->
    <audio
      ref="fullPreviewPlayerRef"
      preload="auto"
      style="display:none"
      @ended="handleSpeechEnded"
      @error="handleSpeechError"
      @timeupdate="handleSpeechTimeUpdate"
      @play="handleSpeechPlay"
      @pause="handleSpeechPause"
    ></audio>

    <Teleport to="body">
      <div
        v-if="isFullscreen && activeSlide"
        class="fullscreen-backdrop"
        :class="{ 'fullscreen-backdrop--youtube': isYoutubeFormat }"
        @click="closeFullscreen"
      >
        <div class="fullscreen-preview-controls" @click.stop>
          <button
            class="full-preview-button"
            :class="{ 'full-preview-button--playing': isFullPreviewPlaying }"
            type="button"
            :disabled="fullPreviewButtonDisabled"
            @click="toggleFullPreview"
          >
            {{ fullPreviewButtonLabel }}
          </button>
        </div>

        <div
          class="fullscreen-content"
          :class="{ 'fullscreen-content--youtube': isYoutubeFormat }"
          @click.stop
        >
          <aside class="fullscreen-speech-panel" aria-label="Voix de la slide">
            <div class="speech-panel-header">
              <div class="speech-tabs" role="tablist" aria-label="Edition slide">
                <button
                  class="speech-tab"
                  :class="{ 'speech-tab--active': fullscreenEditorTab === 'speech' }"
                  type="button"
                  role="tab"
                  :aria-selected="String(fullscreenEditorTab === 'speech')"
                  @click="fullscreenEditorTab = 'speech'"
                >
                  Speech
                </button>
                <button
                  class="speech-tab"
                  :class="{ 'speech-tab--active': fullscreenEditorTab === 'katex' }"
                  type="button"
                  role="tab"
                  :aria-selected="String(fullscreenEditorTab === 'katex')"
                  @click="fullscreenEditorTab = 'katex'"
                >
                  KaTeX
                </button>
              </div>
              <span>{{ activeSlideIndexLabel }}</span>
            </div>

            <template v-if="fullscreenEditorTab === 'speech'">
              <textarea
                class="speech-script"
                :class="{ 'speech-script--dirty': activeSpeechDraftDirty }"
                v-model="speechDraft"
                rows="8"
                maxlength="2500"
                @keydown.stop
              ></textarea>

              <audio
                v-if="activeSlideSpeechAudioUrl"
                ref="speechPlayerRef"
                class="speech-player"
                :src="activeSlideSpeechAudioUrl"
                controls
                preload="auto"
                @ended="handleSpeechEnded"
                @error="handleSpeechError"
                @timeupdate="handleSpeechTimeUpdate"
                @play="handleSpeechPlay"
                @pause="handleSpeechPause"
                @seeked="handleSpeechTimeUpdate"
                @loadedmetadata="handleSpeechLoadedMetadata"
              ></audio>

              <p v-else class="speech-empty">{{ activeSlideSpeechStatusLabel }}</p>

              <div v-if="speechWordTokens.length" class="pronunciation-section" aria-label="Prononciation des mots">
                <div class="pronunciation-header">
                  <span class="pronunciation-title">Prononciation</span>
                  <span class="pronunciation-hint">Clique un mot pour corriger sa prononciation</span>
                </div>
                <div class="pronunciation-text">
                  <template v-for="token in speechWordTokens" :key="token.key">
                    <button
                      v-if="token.type === 'word'"
                      class="pronunciation-word"
                      :class="{ 'pronunciation-word--has-override': Boolean(token.override) }"
                      type="button"
                      :title="token.override ? `Prononcé : ${token.override.pronunciation}` : 'Définir la prononciation'"
                      @click="openPronunciationEditor(token, $event)"
                    >{{ token.text }}</button>
                    <span v-else class="pronunciation-sep">{{ token.text }}</span>
                  </template>
                </div>

                <div v-if="safePronunciationOverrides.length" class="pronunciation-list">
                  <span class="pronunciation-list-label">Surcharges actives :</span>
                  <span
                    v-for="override in safePronunciationOverrides"
                    :key="override.word"
                    class="pronunciation-chip"
                    :class="{ 'pronunciation-chip--foreign': normalizeOverrideLanguage(override.language) !== 'fr' }"
                    :title="`Prononcé : ${override.pronunciation} (${PRONUNCIATION_LANGUAGE_LABELS[normalizeOverrideLanguage(override.language)] || 'FR'})`"
                  >
                    <span class="pronunciation-chip-lang">{{ PRONUNCIATION_LANGUAGE_LABELS[normalizeOverrideLanguage(override.language)] || 'FR' }}</span>
                    <strong>{{ override.word }}</strong>
                    <span class="pronunciation-chip-arrow">→</span>
                    <em>{{ override.pronunciation }}</em>
                  </span>
                </div>

                <div v-if="hasAnyVoiceOverrides" class="voice-overrides-panel">
                  <button
                    class="voice-overrides-toggle"
                    type="button"
                    @click="showVoiceOverridesPanel = !showVoiceOverridesPanel"
                  >
                    <span class="voice-overrides-arrow" :class="{ 'is-open': showVoiceOverridesPanel }">›</span>
                    Surcharges par voix
                  </button>

                  <div v-if="showVoiceOverridesPanel" class="voice-overrides-body">
                    <div
                      v-for="entry in allVoiceOverrideEntries"
                      :key="entry.voiceId"
                      class="voice-overrides-group"
                      :class="{ 'voice-overrides-group--active': entry.voiceId === activeVoiceId }"
                    >
                      <div class="voice-overrides-group-header">
                        <span class="voice-overrides-name">
                          {{ entry.voiceName }}
                          <span v-if="entry.voiceId === activeVoiceId" class="voice-overrides-badge">active</span>
                        </span>
                        <button
                          class="voice-overrides-clear"
                          type="button"
                          :title="`Supprimer toutes les surcharges de ${entry.voiceName}`"
                          @click="clearAllVoiceOverrides(entry.voiceId)"
                        >Tout effacer</button>
                      </div>
                      <div class="voice-overrides-list">
                        <div
                          v-for="override in entry.overrides"
                          :key="override.word"
                          class="voice-override-item"
                        >
                          <span class="voice-override-item-lang">{{ PRONUNCIATION_LANGUAGE_LABELS[normalizeOverrideLanguage(override.language)] || 'FR' }}</span>
                          <strong class="voice-override-item-word">{{ override.word }}</strong>
                          <span class="voice-override-item-arrow">→</span>
                          <em class="voice-override-item-pron">{{ override.pronunciation }}</em>
                          <button
                            class="voice-override-item-delete"
                            type="button"
                            :title="`Supprimer la surcharge de « ${override.word} »`"
                            @click="removeVoiceWordOverride(entry.voiceId, override.word)"
                          >×</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="speech-action-row">
                <button
                  class="speech-save-button"
                  type="button"
                  :disabled="isGeneratingActiveSpeech || !activeSpeechDraftDirty"
                  @click="saveActiveSpeechDraft"
                >
                  Enregistrer speech
                </button>

                <button
                  class="speech-generate-button"
                  type="button"
                  :disabled="isGeneratingActiveSpeech || !activeSpeechDraftText"
                  @click="generateActiveSlideSpeech"
                >
                  {{ speechGenerateButtonLabel }}
                </button>
              </div>
            </template>

            <template v-else>
              <textarea
                ref="katexTextareaRef"
                class="speech-script"
                :class="{ 'speech-script--dirty': activeKatexDraftDirty }"
                v-model="katexDraft"
                rows="8"
                maxlength="5000"
                placeholder="KATEX de cette slide"
                @keydown.stop
              ></textarea>

              <div class="katex-color-row">
                <span class="katex-color-label">Couleur</span>
                <button
                  v-for="color in KATEX_COLORS"
                  :key="color.hex"
                  class="katex-color-btn"
                  :style="{ background: color.hex }"
                  :title="color.label"
                  type="button"
                  @click="applyKatexColor(color.hex)"
                ></button>
              </div>

              <p class="speech-empty">
                Modifie la formule KaTeX de cette slide, puis enregistre.
              </p>

              <div class="speech-action-row">
                <button
                  class="speech-save-button"
                  type="button"
                  :disabled="!activeKatexDraftDirty"
                  @click="saveActiveKatexDraft"
                >
                  Enregistrer KaTeX
                </button>
              </div>
            </template>

            <div class="speech-side-controls" aria-label="Options voix et lecture">
              <div class="speech-side-control" aria-label="Sous-titres">
                <span class="control-label speech-side-control-label">Sous-titres</span>
                <button
                  class="size-reset line-mode-button subtitles-toggle subtitles-toggle--inline"
                  :class="{ 'subtitles-toggle--active': showSubtitles, 'line-mode-button--active': showSubtitles }"
                  type="button"
                  :aria-pressed="showSubtitles ? 'true' : 'false'"
                  @click="toggleSubtitles"
                >
                  <svg class="subtitles-toggle-icon" viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3" y="5" width="18" height="14" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/>
                    <rect x="6.5" y="11" width="4.5" height="1.6" rx="0.8" fill="currentColor"/>
                    <rect x="12.5" y="11" width="5" height="1.6" rx="0.8" fill="currentColor"/>
                    <rect x="6.5" y="14.5" width="6.5" height="1.6" rx="0.8" fill="currentColor"/>
                    <rect x="14.5" y="14.5" width="3" height="1.6" rx="0.8" fill="currentColor"/>
                  </svg>
                  <span>{{ showSubtitles ? 'Activés' : 'Désactivés' }}</span>
                </button>
              </div>

              <div
                v-if="activeSlideCanAnimateKatex"
                class="speech-side-control"
                aria-label="Animation KaTeX avec la voix"
              >
                <span class="control-label speech-side-control-label">KaTeX voix</span>
                <button
                  class="size-reset line-mode-button"
                  :class="{ 'line-mode-button--active': activeSlideKatexRevealWithSpeech }"
                  type="button"
                  :aria-pressed="activeSlideKatexRevealWithSpeech ? 'true' : 'false'"
                  @click="toggleActiveKatexSpeechReveal"
                >
                  {{ katexSpeechRevealLabel }}
                </button>
              </div>
            </div>
          </aside>

          <div class="fullscreen-toolbar">
            <div class="fullscreen-control-group" aria-label="Taille des formules">
              <span class="control-label">{{ mathSizeLabel }}</span>
              <button class="size-button" type="button" @click="decreaseMathSize">A-</button>
              <span class="size-value">{{ mathSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseMathSize">A+</button>
              <button class="size-reset" type="button" @click="resetMathSize">Reset</button>
            </div>

            <div
              v-if="activeSlide && isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Taille du titre hook ou cta"
            >
              <span class="control-label">Titre</span>
              <button class="size-button" type="button" @click="decreaseActiveTitleSize">T-</button>
              <span class="size-value">{{ activeTitleSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseActiveTitleSize">T+</button>
              <button class="size-reset" type="button" @click="resetActiveTitleSize">Reset</button>
            </div>

            <div
              v-if="activeSlide && isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Taille du texte hook ou cta"
            >
              <span class="control-label">Texte</span>
              <button class="size-button" type="button" @click="decreaseActiveTextSize">Txt-</button>
              <span class="size-value">{{ activeTextSizePercent }}%</span>
              <button class="size-button" type="button" @click="increaseActiveTextSize">Txt+</button>
              <button class="size-reset" type="button" @click="resetActiveTextSize">Reset</button>
            </div>

            <div class="fullscreen-control-group" aria-label="Safe zone horizontale">
              <span class="control-label">Safe H</span>
              <button class="size-button" type="button" @click="decreaseSafeZoneX">H-</button>
              <span class="size-value">{{ safeZoneXPercent }}%</span>
              <button class="size-button" type="button" @click="increaseSafeZoneX">H+</button>
              <button class="size-reset" type="button" @click="resetSafeZoneX">Reset</button>
            </div>

            <div class="fullscreen-control-group" aria-label="Safe zone verticale">
              <span class="control-label">{{ safeZoneYLabel }}</span>
              <button class="size-button" type="button" @click="decreaseSafeZoneY">V-</button>
              <span class="size-value">{{ safeZoneYPercent }}%</span>
              <button class="size-button" type="button" @click="increaseSafeZoneY">V+</button>
              <button class="size-reset" type="button" @click="resetSafeZoneY">Reset</button>
            </div>

            <div
              v-if="activeSlide && !isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Disposition KaTeX"
            >
              <div class="inline-layout-row">
              <button
                class="size-reset line-mode-button"
                :class="{ 'line-mode-button--active': activeSlideInline }"
                type="button"
                :disabled="!canToggleKatexLineMode"
                @click="toggleActiveKatexLineMode"
              >
                {{ lineModeLabel }}
              </button>
              <template v-if="activeSlideInline">
                <button
                  class="size-button inline-separator-button"
                  :class="{ 'line-mode-button--active': activeSlideInlineSeparator === 'semicolon' }"
                  type="button"
                  aria-label="Separateur point-virgule"
                  @click="setActiveInlineSeparator('semicolon')"
                >
                  ;
                </button>
                <button
                  class="size-button inline-separator-button"
                  :class="{ 'line-mode-button--active': activeSlideInlineSeparator === 'arrow' }"
                  type="button"
                  aria-label="Separateur fleche"
                  @click="setActiveInlineSeparator('arrow')"
                >
                  →
                </button>
                <button
                  class="size-button inline-separator-button inline-separator-button--none"
                  :class="{ 'line-mode-button--active': activeSlideInlineSeparator === 'none' }"
                  type="button"
                  aria-label="Aucun separateur"
                  @click="setActiveInlineSeparator('none')"
                >
                  rien
                </button>
              </template>
              </div>
              <div v-if="activeSlideInline" class="inline-layout-row inline-layout-row--offset">
                <button
                  class="size-button inline-offset-button"
                  type="button"
                  aria-label="Decaler la formule vers la gauche"
                  @click="decreaseActiveInlineOffset"
                >
                  ←
                </button>
                <span class="size-value inline-offset-value">{{ activeInlineOffsetLabel }}</span>
                <button
                  class="size-button inline-offset-button"
                  type="button"
                  aria-label="Decaler la formule vers la droite"
                  @click="increaseActiveInlineOffset"
                >
                  →
                </button>
                <button class="size-reset" type="button" @click="resetActiveInlineOffset">0</button>
              </div>
              <div v-if="activeSlideInline" class="inline-layout-row inline-layout-row--offset">
                <button
                  class="size-button inline-offset-button"
                  type="button"
                  aria-label="Remonter la formule"
                  @click="decreaseActiveInlineVerticalOffset"
                >
                  ↑
                </button>
                <span class="size-value inline-offset-value">{{ activeInlineVerticalOffsetLabel }}</span>
                <button
                  class="size-button inline-offset-button"
                  type="button"
                  aria-label="Descendre la formule"
                  @click="increaseActiveInlineVerticalOffset"
                >
                  ↓
                </button>
                <button class="size-reset" type="button" @click="resetActiveInlineVerticalOffset">0</button>
              </div>
            </div>

            <div
              v-if="activeSlide && !isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Page de correction"
            >
              <button
                class="size-reset line-mode-button"
                :class="{ 'line-mode-button--active': activeSlideResetsCumulative }"
                type="button"
                @click="toggleActiveResetCumulative"
              >
                {{ resetCumulativeLabel }}
              </button>
            </div>

            <div
              v-if="activeSlide && !isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Suppression de la ligne precedente"
            >
              <button
                class="size-reset line-mode-button"
                :class="{ 'line-mode-button--active': activeSlideDropsPreviousLine }"
                type="button"
                @click="toggleActiveDropPreviousLine"
              >
                {{ dropPreviousLineLabel }}
              </button>
            </div>

            <div
              v-if="activeSlide && !isEdgeSlide(activeSlide)"
              class="fullscreen-control-group"
              aria-label="Espacement cumulatif"
            >
              <span class="control-label">Espacement</span>
              <button
                class="size-button cumulative-gap-button"
                type="button"
                aria-label="Reduire le vide entre les lignes"
                @click="decreaseCumulativeGap"
              >
                -
              </button>
              <span class="size-value cumulative-gap-value">{{ cumulativeGapLabel }}</span>
              <button
                class="size-button cumulative-gap-button"
                type="button"
                aria-label="Augmenter le vide entre les lignes"
                @click="increaseCumulativeGap"
              >
                +
              </button>
              <button class="size-reset" type="button" @click="resetCumulativeGap">Reset</button>
            </div>

            <div
              v-if="activeSlide && !isVirtualCoverSlide(activeSlide)"
              class="fullscreen-control-group ann-group"
              aria-label="Annotations"
            >
              <span class="control-label">Annotations</span>

              <div class="ann-tools">
                <button
                  class="ann-tool-btn"
                  :class="{ 'ann-tool-btn--active': annotationActiveTool === 'select' }"
                  type="button"
                  title="Sélectionner, déplacer, redimensionner"
                  @click="setAnnotationTool('select')"
                >
                  <svg class="ann-tool-icon" viewBox="0 0 16 16" aria-hidden="true">
                    <path d="M3 2 L3 13 L6 10 L8.5 13.5 L10 12.5 L7.5 9 L12 8 Z" fill="currentColor" />
                  </svg>
                  <span class="ann-tool-label">Sélection</span>
                </button>
                <button
                  class="ann-tool-btn"
                  :class="{ 'ann-tool-btn--active': annotationActiveTool === 'circle' }"
                  type="button"
                  title="Tracer un cercle"
                  @click="setAnnotationTool('circle')"
                >
                  <svg class="ann-tool-icon" viewBox="0 0 16 16" aria-hidden="true">
                    <circle cx="8" cy="8" r="5.5" fill="none" stroke="currentColor" stroke-width="1.7" />
                  </svg>
                  <span class="ann-tool-label">Cercle</span>
                </button>
                <button
                  class="ann-tool-btn"
                  :class="{ 'ann-tool-btn--active': annotationActiveTool === 'rect' }"
                  type="button"
                  title="Tracer un rectangle"
                  @click="setAnnotationTool('rect')"
                >
                  <svg class="ann-tool-icon" viewBox="0 0 16 16" aria-hidden="true">
                    <rect x="2.5" y="3" width="11" height="10" fill="none" stroke="currentColor" stroke-width="1.7" rx="1" />
                  </svg>
                  <span class="ann-tool-label">Carré</span>
                </button>
                <button
                  class="ann-tool-btn"
                  :class="{ 'ann-tool-btn--active': annotationActiveTool === 'arrow' }"
                  type="button"
                  title="Tracer une flèche"
                  @click="setAnnotationTool('arrow')"
                >
                  <svg class="ann-tool-icon" viewBox="0 0 16 16" aria-hidden="true">
                    <line x1="2" y1="13" x2="12" y2="3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                    <polygon points="13.5,2 14,7 9,4" fill="currentColor" />
                  </svg>
                  <span class="ann-tool-label">Flèche</span>
                </button>
              </div>

              <div class="ann-colors">
                <button
                  v-for="col in ANNOTATION_COLORS"
                  :key="col"
                  class="ann-color-btn"
                  :class="{ 'ann-color-btn--active': annotationActiveColor === col }"
                  :style="{ background: col }"
                  type="button"
                  :title="col"
                  @click="annotationActiveColor = col"
                ></button>
              </div>

              <div class="ann-stroke">
                <span class="ann-stroke-label">Épais.</span>
                <button class="size-button" type="button" @click="decreaseAnnotationStroke">-</button>
                <span class="size-value ann-stroke-value">{{ annotationStrokeWidth }}px</span>
                <button class="size-button" type="button" @click="increaseAnnotationStroke">+</button>
              </div>

              <div class="ann-actions">
                <button
                  class="ann-action-btn"
                  type="button"
                  :disabled="!annotationSelectedId"
                  @click="deleteSelectedAnnotation"
                >
                  Supprimer
                </button>
                <button
                  class="ann-action-btn ann-action-btn--danger"
                  type="button"
                  :disabled="!activeSlide?.annotations?.length"
                  @click="clearAllAnnotations"
                >
                  Effacer tout
                </button>
              </div>
            </div>

          </div>

          <div class="fullscreen-stage">
            <button
              class="nav-arrow"
              type="button"
              aria-label="Slide précédente"
              @click="goPrev"
            >
              ‹
            </button>

            <ReelSlidePreview
              :key="isYoutubeFormat ? 'youtube-fullscreen-slide' : activeSlide.id"
              :slide="activeSlide"
              :is-selected="true"
              display-mode="fullscreen"
              :clickable="false"
              :math-scale="getMathScale(activeSlide)"
              :safe-zone-x-scale="safeZoneXScale"
              :safe-zone-y-scale="getSafeZoneYScale(activeSlide)"
              :video-format="format"
              :show-subtitles="showSubtitles"
              :audio-current-time="speechAudioCurrentTime"
              :audio-playing="speechAudioPlaying"
              :annotation-editable="!isVirtualCoverSlide(activeSlide)"
              :annotation-active-tool="annotationActiveTool"
              :annotation-active-color="annotationActiveColor"
              :annotation-stroke-width="annotationStrokeWidth"
              :annotation-selected-id="annotationSelectedId"
              @diagnostic="$emit('diagnostic', $event)"
              @annotation-add="handleAnnotationAdd"
              @annotation-update="handleAnnotationUpdate"
              @annotation-update-selected-id="annotationSelectedId = $event"
              @annotation-delete="handleAnnotationDelete"
            />

            <button
              class="nav-arrow"
              type="button"
              aria-label="Slide suivante"
              @click="goNext"
            >
              ›
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import html2canvas from 'html2canvas'
import ReelSlidePreview from './ReelSlidePreview.vue'

const props = defineProps({
  slides: {
    type: Array,
    default: () => [],
  },
  selectedSlideId: {
    type: [Number, String, null],
    default: null,
  },
  generatingSpeechSlideId: {
    type: [Number, String, null],
    default: null,
  },
  exportingVideo: {
    type: Boolean,
    default: false,
  },
  format: {
    type: String,
    default: 'reel',
  },
  pronunciationOverrides: {
    type: Array,
    default: () => [],
  },
  pronunciationOverridesByVoice: {
    type: Object,
    default: () => ({}),
  },
  activeVoiceId: {
    type: String,
    default: '',
  },
  voiceList: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits([
  'select-slide',
  'diagnostic',
  'update-slide',
  'generate-slide-speech',
  'export-video',
  'update-pronunciation-overrides',
  'update-pronunciation-overrides-by-voice',
])

const isFullscreen = ref(false)
const fullscreenIndex = ref(0)
const previousBodyOverflow = ref('')
const SAFE_ZONE_DEFAULT_SCALE = 1.15
const SAFE_ZONE_DEFAULT_SCALE_YOUTUBE = 1.0
const MATH_SCALE_DEFAULT_REEL = 1.0
const MATH_SCALE_DEFAULT_YOUTUBE = 1.0
const CUMULATIVE_GAP_DEFAULT_YOUTUBE = 0.35
const mathScaleCalcul = ref(MATH_SCALE_DEFAULT_REEL)
const mathScaleHook = ref(MATH_SCALE_DEFAULT_REEL)
const mathScaleCta = ref(MATH_SCALE_DEFAULT_REEL)
const safeZoneXScale = ref(SAFE_ZONE_DEFAULT_SCALE)
const safeZoneMathYScale = ref(SAFE_ZONE_DEFAULT_SCALE)
const safeZoneHookYScale = ref(SAFE_ZONE_DEFAULT_SCALE)
const safeZoneCtaYScale = ref(SAFE_ZONE_DEFAULT_SCALE)
const exportingPng = ref(false)
const preparingVideoFrames = ref(false)
const pngExportMounted = ref(false)
const pngExportProgress = ref(0)
const videoFrameProgress = ref(0)
const videoExportMode = ref('fast')
const exportFrameWidth = ref(1080)
const exportFrameHeight = ref(1920)
const exportSlideRefs = ref([])
const speechDraft = ref('')
const speechDraftSavedValue = ref('')
const speechDraftSlideId = ref(null)
const katexDraft = ref('')
const katexDraftSavedValue = ref('')
const katexDraftSlideId = ref(null)
const fullscreenEditorTab = ref('speech')
const katexTextareaRef = ref(null)

const KATEX_COLORS = [
  { hex: '#e74c3c', label: 'Rouge' },
  { hex: '#2980b9', label: 'Bleu' },
  { hex: '#f39c12', label: 'Orange' },
  { hex: '#27ae60', label: 'Vert' },
  { hex: '#8e44ad', label: 'Violet' },
]
const ANNOTATION_COLORS = ['#e74c3c', '#2980b9', '#f39c12', '#27ae60', '#8e44ad']
const speechPlayerRef = ref(null)
const fullPreviewPlayerRef = ref(null)

const annotationActiveTool = ref('select')
const annotationActiveColor = ref('#e74c3c')
const annotationStrokeWidth = ref(3)
const annotationSelectedId = ref(null)

const SUBTITLES_STORAGE_KEY = 'reelStudio.showSubtitles'
const showSubtitles = ref(loadSubtitlesPreference())

const speechAudioCurrentTime = ref(0)
const speechAudioPlaying = ref(false)
let speechAudioRafId = null

const SPEECH_FADE_MS = 70
let speechFadeRafId = null
let speechFullPreviewTargetVolume = 1

function stopSpeechAudioRaf() {
  if (speechAudioRafId !== null) {
    cancelAnimationFrame(speechAudioRafId)
    speechAudioRafId = null
  }
}

function clearSpeechFadeTimers() {
  if (speechFadeRafId !== null) {
    cancelAnimationFrame(speechFadeRafId)
    speechFadeRafId = null
  }
}

function rampSpeechVolume(audio, from, to, durationMs) {
  if (!audio || typeof window === 'undefined') return
  if (speechFadeRafId !== null) {
    cancelAnimationFrame(speechFadeRafId)
    speechFadeRafId = null
  }
  const start = performance.now()
  const startVolume = Math.max(0, Math.min(1, from))
  const targetVolume = Math.max(0, Math.min(1, to))
  audio.volume = startVolume
  const duration = Math.max(1, durationMs)
  const tick = (now) => {
    const ratio = Math.max(0, Math.min(1, (now - start) / duration))
    const nextVolume = startVolume + (targetVolume - startVolume) * ratio
    audio.volume = Math.max(0, Math.min(1, nextVolume))
    if (ratio < 1) {
      speechFadeRafId = requestAnimationFrame(tick)
    } else {
      audio.volume = targetVolume
      speechFadeRafId = null
    }
  }
  speechFadeRafId = requestAnimationFrame(tick)
}


function getActiveSpeechPlayer() {
  return isFullPreviewPlaying.value ? fullPreviewPlayerRef.value : speechPlayerRef.value
}

function startSpeechAudioRaf() {
  stopSpeechAudioRaf()
  const tick = () => {
    const audio = getActiveSpeechPlayer()
    if (!audio || audio.paused || audio.ended) {
      speechAudioRafId = null
      return
    }
    speechAudioCurrentTime.value = Number(audio.currentTime) || 0
    speechAudioRafId = requestAnimationFrame(tick)
  }
  speechAudioRafId = requestAnimationFrame(tick)
}

function loadSubtitlesPreference() {
  if (typeof window === 'undefined' || !window.localStorage) return false
  try {
    return window.localStorage.getItem(SUBTITLES_STORAGE_KEY) === '1'
  } catch (_) {
    return false
  }
}

function toggleSubtitles() {
  showSubtitles.value = !showSubtitles.value
  if (typeof window === 'undefined' || !window.localStorage) return
  try {
    window.localStorage.setItem(SUBTITLES_STORAGE_KEY, showSubtitles.value ? '1' : '0')
  } catch (_) {
    /* noop */
  }
}

const pronunciationEditorOpen = ref(false)
const pronunciationEditorWord = ref('')
const pronunciationEditorPronunciation = ref('')
const pronunciationEditorLanguage = ref('fr')
const pronunciationEditorAnchor = ref(null)
const pronunciationInputRef = ref(null)

const PRONUNCIATION_LANGUAGES = [
  { code: 'fr', label: 'Français', short: 'FR' },
  { code: 'en', label: 'English', short: 'EN' },
  { code: 'es', label: 'Español', short: 'ES' },
  { code: 'de', label: 'Deutsch', short: 'DE' },
  { code: 'it', label: 'Italiano', short: 'IT' },
  { code: 'pt', label: 'Português', short: 'PT' },
]
const PRONUNCIATION_LANGUAGE_LABELS = Object.fromEntries(
  PRONUNCIATION_LANGUAGES.map((l) => [l.code, l.short])
)
const isFullPreviewPlaying = ref(false)
const cumulativeGap = ref(0.4)
let fullPreviewTimerId = null
const localSlidePatches = ref({})
const pendingYoutubeInlinePatches = new Map()
const youtubeInlinePatchTimers = new Map()

const YOUTUBE_INLINE_PATCH_DEBOUNCE_MS = 450
const slidesSafe = computed(() => {
  const slides = Array.isArray(props.slides) ? props.slides : []
  const patches = localSlidePatches.value || {}
  return slides.map((slide) => {
    const patch = slide?.id ? patches[String(slide.id)] : null
    return patch ? { ...slide, ...patch } : slide
  })
})
const NON_MATH_SLIDE_TYPES = new Set(['hook', 'cta'])
const INLINE_OFFSET_MIN = -40
const INLINE_OFFSET_MAX = 40
const INLINE_OFFSET_STEP = 4
const INLINE_VERTICAL_OFFSET_MIN = -1
const INLINE_VERTICAL_OFFSET_MAX = 1
const INLINE_VERTICAL_OFFSET_STEP = 0.05
const INLINE_SEPARATOR_SEMICOLON = 'semicolon'
const INLINE_SEPARATOR_ARROW = 'arrow'
const INLINE_SEPARATOR_NONE = 'none'
const INLINE_SEPARATOR_VALUES = new Set([
  INLINE_SEPARATOR_SEMICOLON,
  INLINE_SEPARATOR_ARROW,
  INLINE_SEPARATOR_NONE,
])
const CUMULATIVE_GAP_MIN = 0
const CUMULATIVE_GAP_MAX = 1.5
const CUMULATIVE_GAP_STEP = 0.1
const CUMULATIVE_GAP_DEFAULT = 0.4
const COVER_SLIDE_ID = '__optitab_reel_cover__'
const COVER_FILENAME = 'optitab-reel-cover.png'
const isYoutubeFormat = computed(() => props.format === 'youtube')
const PNG_EXPORT_WIDTH = computed(() => isYoutubeFormat.value ? 1920 : 1080)
const PNG_EXPORT_HEIGHT = computed(() => isYoutubeFormat.value ? 1080 : 1920)
const VIDEO_EXPORT_PRESETS = computed(() => isYoutubeFormat.value
  ? {
      fast: { width: 1280, height: 720, fps: 24, crf: 24, ffmpegPreset: 'ultrafast', imageType: 'image/jpeg', imageQuality: 0.9 },
      hq: { width: 1920, height: 1080, fps: 30, crf: 18, ffmpegPreset: 'veryfast', imageType: 'image/png', imageQuality: 1 },
    }
  : {
      fast: { width: 720, height: 1280, fps: 24, crf: 24, ffmpegPreset: 'ultrafast', imageType: 'image/jpeg', imageQuality: 0.9 },
      hq: { width: 1080, height: 1920, fps: 30, crf: 18, ffmpegPreset: 'veryfast', imageType: 'image/png', imageQuality: 1 },
    }
)
const mathSizePercent = computed(() => Math.round(getMathScale(activeSlide.value) * 100))
const mathSizeLabel = computed(() => getActiveSlideTypeLabel('Taille'))
const safeZoneXPercent = computed(() => Math.round(safeZoneXScale.value * 100))
const safeZoneYPercent = computed(() => Math.round(getSafeZoneYScale(activeSlide.value) * 100))
const safeZoneYLabel = computed(() => getActiveSlideTypeLabel('Safe V'))
const activeTitleSizePercent = computed(() => Math.round(getSlideScale(activeSlide.value?.title_scale) * 100))
const activeTextSizePercent = computed(() => Math.round(getSlideScale(activeSlide.value?.screen_text_scale) * 100))
const activeSlideIndexLabel = computed(() => {
  if (!videoSlidesForRender.value.length || !activeSlide.value) return ''
  const videoIndex = videoSlidesForRender.value.findIndex((slide) => slide.id === activeSlide.value.id)
  if (videoIndex === -1) return 'Cover'
  return `Slide ${videoIndex + 1}/${videoSlidesForRender.value.length}`
})
const activeSlideSpeechText = computed(() => slideSpeechText(activeSlide.value))
const activeSpeechDraftText = computed(() => normalizeSpeechLine(speechDraft.value))
const activeSpeechDraftDirty = computed(() => (
  normalizeSpeechDraftForCompare(speechDraft.value) !== normalizeSpeechDraftForCompare(speechDraftSavedValue.value)
))
const activeKatexDraftText = computed(() => normalizeKatexDraft(katexDraft.value))
const activeKatexDraftDirty = computed(() => (
  normalizeKatexDraftForCompare(katexDraft.value) !== normalizeKatexDraftForCompare(katexDraftSavedValue.value)
))
const activeSlideSpeechAudioUrl = computed(() => normalizeText(activeSlide.value?.speech_audio_url))
const isGeneratingActiveSpeech = computed(() => (
  activeSlide.value?.id &&
  Number(props.generatingSpeechSlideId) === Number(activeSlide.value.id)
))
const speechGenerateButtonLabel = computed(() => {
  if (isGeneratingActiveSpeech.value) return 'Generation...'
  if (activeSpeechDraftDirty.value) return 'Enregistrer + generer'
  return 'Generer cette slide'
})
const activeSlideSpeechStatusLabel = computed(() => {
  if (isGeneratingActiveSpeech.value) return 'Generation audio en cours.'
  if (activeSlide.value?.speech_status === 'error') return activeSlide.value.speech_error || 'Erreur audio.'
  if (!activeSlideSpeechText.value) return 'Aucun texte vocal pour cette slide.'
  return 'Aucun MP3 genere pour cette slide.'
})
const isVideoExportBusy = computed(() => Boolean(preparingVideoFrames.value || props.exportingVideo))
const exportFrameStyle = computed(() => ({
  '--export-width': `${exportFrameWidth.value}px`,
  '--export-height': `${exportFrameHeight.value}px`,
}))
const videoHqExportButtonLabel = computed(() => {
  if (props.exportingVideo && videoExportMode.value === 'hq') return 'Assemblage HQ...'
  if (preparingVideoFrames.value && videoExportMode.value === 'hq') return `HQ ${videoFrameProgress.value}/${videoSlidesForRender.value.length}`
  return 'MP4 HQ'
})
const fullPreviewButtonLabel = computed(() => (isFullPreviewPlaying.value ? 'Stopper la lecture' : 'Ecouter tout'))
const fullPreviewButtonDisabled = computed(() => (
  !isFullPreviewPlaying.value &&
  (!videoSlidesForRender.value.length || Boolean(props.generatingSpeechSlideId))
))

function normalizeText(value) {
  return String(value || '').trim()
}

function normalizeSpeechLine(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .split('\n')
    .map((line) => line.replace(/\s+/g, ' ').trim())
    .filter(Boolean)
    .join(' ')
}

function normalizeSpeechDraftForCompare(value) {
  return String(value || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim()
}

function normalizeKatexDraft(value) {
  return String(value || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim()
}

function normalizeKatexDraftForCompare(value) {
  return normalizeKatexDraft(value)
}

function slideSpeechText(slide) {
  const voice = normalizeSpeechLine(slide?.voice_script)
  if (voice) return voice

  return [slide?.title, slide?.screen_text]
    .map((part) => normalizeSpeechLine(part))
    .filter(Boolean)
    .join('. ')
}

function getSpeechDraftSource(slide) {
  const voiceScript = String(slide?.voice_script || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').trim()
  return voiceScript || slideSpeechText(slide)
}

function syncSpeechDraftFromActiveSlide({ force = false } = {}) {
  const slide = activeSlide.value
  if (!slide?.id) {
    speechDraft.value = ''
    speechDraftSavedValue.value = ''
    speechDraftSlideId.value = null
    return
  }

  const nextSlideId = Number(slide.id)
  const slideChanged = Number(speechDraftSlideId.value) !== nextSlideId
  if (!force && !slideChanged && activeSpeechDraftDirty.value) return

  const source = getSpeechDraftSource(slide)
  speechDraft.value = source
  speechDraftSavedValue.value = source
  speechDraftSlideId.value = nextSlideId
}

function syncKatexDraftFromActiveSlide({ force = false } = {}) {
  const slide = activeSlide.value
  if (!slide?.id) {
    katexDraft.value = ''
    katexDraftSavedValue.value = ''
    katexDraftSlideId.value = null
    return
  }

  const nextSlideId = Number(slide.id)
  const slideChanged = Number(katexDraftSlideId.value) !== nextSlideId
  if (!force && !slideChanged && activeKatexDraftDirty.value) return

  const source = normalizeKatexDraft(slide.katex)
  katexDraft.value = source
  katexDraftSavedValue.value = source
  katexDraftSlideId.value = nextSlideId
}

function isSlideSpeechAudioStale(slide) {
  const expectedSpeech = slideSpeechText(slide)
  if (!expectedSpeech || !normalizeText(slide?.speech_audio_url)) return false
  if (!Object.prototype.hasOwnProperty.call(slide || {}, 'speech_text')) return false
  return normalizeSpeechLine(slide?.speech_text) !== normalizeSpeechLine(expectedSpeech)
}

function getVideoSlideLabel(slide) {
  const videoIndex = videoSlidesForRender.value.findIndex((videoSlide) => Number(videoSlide.id) === Number(slide?.id))
  return videoIndex === -1 ? 'Slide' : `Slide ${videoIndex + 1}`
}

function validateFullPreviewAudio() {
  if (activeSpeechDraftDirty.value) {
    window.alert('Speech modifie sur cette slide. Enregistre et regenere le MP3 avant la lecture complete.')
    return false
  }

  const missingAudioSlides = videoSlidesForRender.value.filter((slide) => (
    slideSpeechText(slide) && !normalizeText(slide?.speech_audio_url)
  ))
  const staleAudioSlides = videoSlidesForRender.value.filter((slide) => isSlideSpeechAudioStale(slide))

  if (!missingAudioSlides.length && !staleAudioSlides.length) return true

  const details = [
    ...missingAudioSlides.map((slide) => `${getVideoSlideLabel(slide)}: MP3 manquant`),
    ...staleAudioSlides.map((slide) => `${getVideoSlideLabel(slide)}: MP3 pas a jour`),
  ].slice(0, 6)

  const extraCount = missingAudioSlides.length + staleAudioSlides.length - details.length
  window.alert(
    `Lecture complete bloquee: genere ou regenere les MP3 avant de previsualiser. ${details.join('. ')}${extraCount > 0 ? ` (+${extraCount} autres)` : ''}.`
  )
  return false
}

function getSlideType(slide) {
  return normalizeText(slide?.slide_type).toLowerCase()
}

function isVirtualCoverSlide(slide) {
  return Boolean(slide?.is_virtual_cover || slide?.id === COVER_SLIDE_ID)
}

function isHookLikeSlide(slide) {
  return isVirtualCoverSlide(slide) || getSlideType(slide) === 'hook'
}

function isEdgeSlide(slide) {
  return isVirtualCoverSlide(slide) || NON_MATH_SLIDE_TYPES.has(getSlideType(slide))
}

function getActiveSlideTypeLabel(prefix) {
  const slideType = getSlideType(activeSlide.value)
  if (slideType === 'hook') return `${prefix} Hook`
  if (slideType === 'cta') return `${prefix} CTA`
  return `${prefix} Calcul`
}

function getSafeZoneYScale(slide) {
  const slideType = getSlideType(slide)
  if (isHookLikeSlide(slide)) return safeZoneHookYScale.value
  if (slideType === 'cta') return safeZoneCtaYScale.value
  return safeZoneMathYScale.value
}

function getMathScale(slide) {
  const slideType = getSlideType(slide)
  if (isHookLikeSlide(slide)) return mathScaleHook.value
  if (slideType === 'cta') return mathScaleCta.value
  return mathScaleCalcul.value
}

function getActiveSafeZoneYRef() {
  const slideType = getSlideType(activeSlide.value)
  if (slideType === 'hook') return safeZoneHookYScale
  if (slideType === 'cta') return safeZoneCtaYScale
  return safeZoneMathYScale
}

function getActiveMathScaleRef() {
  const slideType = getSlideType(activeSlide.value)
  if (slideType === 'hook') return mathScaleHook
  if (slideType === 'cta') return mathScaleCta
  return mathScaleCalcul
}

function getSlideScale(value) {
  const nextValue = Number(value) || 1
  return Math.min(2, Math.max(0.5, Number(nextValue.toFixed(2))))
}

function isAlignedKatexBlock(value) {
  return /^\\begin\{aligned\}[\s\S]*\\end\{aligned\}$/.test(normalizeText(value))
}

function unwrapAlignedBlock(value) {
  return normalizeText(value)
    .replace(/^\\begin\{aligned\}\s*/, '')
    .replace(/\s*\\end\{aligned\}$/, '')
    .trim()
}

function splitAlignedLines(innerBlock) {
  return String(innerBlock || '')
    .split(/\\\\(?:\[[^\]]*\])?/)
    .map((line) => normalizeKatexLine(line))
    .filter(Boolean)
}

function splitKatexLines(block) {
  const raw = normalizeText(block)
  if (!raw) return []

  if (isAlignedKatexBlock(raw)) {
    return splitAlignedLines(unwrapAlignedBlock(raw))
  }

  return raw
    .split(/\\\\(?:\[[^\]]*\])?/)
    .map((line) => normalizeKatexLine(line))
    .filter(Boolean)
}

function normalizeKatexLine(line) {
  return String(line || '')
    .trim()
    .replace(/(^|[^\\])&+/g, '$1')
    .replace(/\s+/g, ' ')
    .trim()
}

function clampInlineOffset(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  return Math.min(INLINE_OFFSET_MAX, Math.max(INLINE_OFFSET_MIN, numeric))
}

function clampInlineVerticalOffset(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return 0
  const clamped = Math.min(INLINE_VERTICAL_OFFSET_MAX, Math.max(INLINE_VERTICAL_OFFSET_MIN, numeric))
  return Number(clamped.toFixed(3))
}

function normalizeInlineSeparator(value) {
  const raw = String(value || '').trim()
  return INLINE_SEPARATOR_VALUES.has(raw) ? raw : INLINE_SEPARATOR_SEMICOLON
}

function clampCumulativeGap(value) {
  const numeric = Number(value)
  if (!Number.isFinite(numeric)) return CUMULATIVE_GAP_DEFAULT
  return Math.min(CUMULATIVE_GAP_MAX, Math.max(CUMULATIVE_GAP_MIN, Number(numeric.toFixed(2))))
}

function makeKatexRow(line, inlineOffsetPercent = 0, inlineVerticalOffsetEm = 0) {
  return {
    parts: [line],
    inlineSeparators: [],
    inlineOffsetPercent: clampInlineOffset(inlineOffsetPercent),
    inlineVerticalOffsetEm: clampInlineVerticalOffset(inlineVerticalOffsetEm),
  }
}

function cloneKatexRows(rows) {
  return (Array.isArray(rows) ? rows : []).map((row) => ({
    parts: Array.isArray(row?.parts) ? [...row.parts] : [],
    inlineSeparators: Array.isArray(row?.inlineSeparators)
      ? row.inlineSeparators.map((value) => normalizeInlineSeparator(value))
      : [],
    inlineOffsetPercent: clampInlineOffset(row?.inlineOffsetPercent),
    inlineVerticalOffsetEm: clampInlineVerticalOffset(row?.inlineVerticalOffsetEm),
  }))
}

function getKatexRowsLineKeys(rows) {
  return cloneKatexRows(rows)
    .flatMap((row) => row.parts)
    .map((line) => normalizeKatexLine(line))
    .filter(Boolean)
}

function toAlignedKatexRows(rows, rowGap = CUMULATIVE_GAP_DEFAULT) {
  const safeRowGap = clampCumulativeGap(rowGap).toFixed(1)
  const prepared = (Array.isArray(rows) ? rows : [])
    .map((row) => {
      const rowLines = Array.isArray(row) ? row : (Array.isArray(row?.parts) ? row.parts : [row])
      const inlineSeparators = Array.isArray(row?.inlineSeparators) ? row.inlineSeparators : []
      const rowContent = rowLines
        .map((line, index) => {
          const cleanLine = normalizeKatexLine(line)
          if (!cleanLine) return ''
          if (index === 0) return cleanLine
          const separator = normalizeInlineSeparator(inlineSeparators[index - 1])
          if (separator === INLINE_SEPARATOR_NONE) return cleanLine
          const separatorKatex = separator === INLINE_SEPARATOR_ARROW ? '\\Rightarrow' : ';'
          return `${separatorKatex}\\qquad ${cleanLine}`
        })
        .filter(Boolean)
        .join('\\qquad ')
      return rowContent ? `&${rowContent}` : ''
    })
    .filter(Boolean)

  if (!prepared.length) return ''
  return `\\begin{aligned}\n${prepared.join(`\\\\[${safeRowGap}em]\n`)}\n\\end{aligned}`
}

function makeCoverSlide(firstSlide) {
  if (!firstSlide) return null

  return {
    ...firstSlide,
    id: COVER_SLIDE_ID,
    source_slide_id: firstSlide.id,
    order: 0,
    slide_type: 'cover',
    is_virtual_cover: true,
    duration_seconds: 0,
    speech_audio_url: '',
    speech_status: '',
    speech_error: '',
    voice_script: '',
  }
}

const baseSlidesForRender = computed(() => {
  let cumulativeRows = []
  let cumulativeLineKeys = new Set()
  let carriedScreenText = ''

  function resetCumulativeState() {
    cumulativeRows = []
    cumulativeLineKeys = new Set()
  }

  function isYoutubeStatementSlide(index, slideType) {
    return isYoutubeFormat.value && index === 1 && !NON_MATH_SLIDE_TYPES.has(slideType)
  }

  function statementScreenText(baseText) {
    const text = normalizeText(baseText)
    if (!text) return 'Énoncé :'
    const plainText = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
    return /^enonce\s*:/.test(plainText) ? text : `Énoncé :\n${text}`
  }

  function appendKatexLines(currentLines, safeSlide, inlineWithPrevious) {
    let addedInlineLine = false
    for (const line of currentLines) {
      const key = normalizeKatexLine(line)
      if (!key || cumulativeLineKeys.has(key)) continue
      cumulativeLineKeys.add(key)

      if (inlineWithPrevious && !addedInlineLine && cumulativeRows.length > 0) {
        const lastRow = cumulativeRows[cumulativeRows.length - 1]
        lastRow.parts.push(line)
        lastRow.inlineSeparators = Array.isArray(lastRow.inlineSeparators) ? lastRow.inlineSeparators : []
        lastRow.inlineSeparators.push(normalizeInlineSeparator(safeSlide.katex_inline_separator))
        lastRow.inlineOffsetPercent = clampInlineOffset(safeSlide.katex_inline_offset_percent)
        lastRow.inlineVerticalOffsetEm = clampInlineVerticalOffset(safeSlide.katex_inline_vertical_offset_em)
        addedInlineLine = true
        continue
      }

      cumulativeRows.push(makeKatexRow(line))
    }
  }

  function dropPreviousCumulativeLine() {
    if (!cumulativeRows.length) return

    const lastRow = cumulativeRows[cumulativeRows.length - 1]
    const parts = Array.isArray(lastRow?.parts) ? lastRow.parts : []
    if (!parts.length) {
      cumulativeRows.pop()
      cumulativeLineKeys = new Set(getKatexRowsLineKeys(cumulativeRows))
      return
    }

    const removedLine = parts.pop()
    if (Array.isArray(lastRow.inlineSeparators) && lastRow.inlineSeparators.length) {
      lastRow.inlineSeparators.pop()
    }
    if (!parts.length) {
      cumulativeRows.pop()
    }

    const removedKey = normalizeKatexLine(removedLine)
    if (removedKey) {
      cumulativeLineKeys.delete(removedKey)
    } else {
      cumulativeLineKeys = new Set(getKatexRowsLineKeys(cumulativeRows))
    }
  }

  return slidesSafe.value.map((slide, index) => {
    const safeSlide = slide && typeof slide === 'object' ? slide : {}
    const slideType = normalizeText(safeSlide.slide_type).toLowerCase()
    const baseText = normalizeText(safeSlide.screen_text)
    const baseKatex = normalizeText(safeSlide.katex)

    if (NON_MATH_SLIDE_TYPES.has(slideType)) {
      resetCumulativeState()
      carriedScreenText = ''
      return {
        ...safeSlide,
        display_screen_text: baseText,
        display_katex: baseKatex,
      }
    }

    if (isYoutubeStatementSlide(index, slideType)) {
      resetCumulativeState()
      carriedScreenText = ''
      return {
        ...safeSlide,
        display_screen_text: statementScreenText(baseText),
        display_katex_row_gap_em: cumulativeGap.value,
        display_katex_rows: [],
        display_katex: baseKatex,
      }
    }

    if (baseText) {
      carriedScreenText = baseText
    }
    const displayScreenText = baseText || carriedScreenText
    if (slideType === 'katex') {
      const currentLines = splitKatexLines(baseKatex)
      if (safeSlide.katex_drop_previous_line) {
        dropPreviousCumulativeLine()
      }
      const inlineWithPrevious = Boolean(safeSlide.katex_inline_with_previous) && cumulativeRows.length > 0
      appendKatexLines(currentLines, safeSlide, inlineWithPrevious)
      if (safeSlide.katex_reset_cumulative) {
        cumulativeRows = cloneKatexRows(cumulativeRows).slice(-2)
        cumulativeLineKeys = new Set(getKatexRowsLineKeys(cumulativeRows))
      }
      return {
        ...safeSlide,
        display_screen_text: displayScreenText,
        display_katex_row_gap_em: cumulativeGap.value,
        display_katex_rows: cloneKatexRows(cumulativeRows),
        display_katex: toAlignedKatexRows(cumulativeRows, cumulativeGap.value) || baseKatex,
      }
    }

    if (slideType === 'cumulative_katex' || slideType === 'result') {
      const currentLines = splitKatexLines(baseKatex)
      if (safeSlide.katex_drop_previous_line) {
        dropPreviousCumulativeLine()
      }
      const inlineWithPrevious = Boolean(safeSlide.katex_inline_with_previous) && cumulativeRows.length > 0
      appendKatexLines(currentLines, safeSlide, inlineWithPrevious)
      if (safeSlide.katex_reset_cumulative) {
        cumulativeRows = cloneKatexRows(cumulativeRows).slice(-2)
        cumulativeLineKeys = new Set(getKatexRowsLineKeys(cumulativeRows))
      }
      return {
        ...safeSlide,
        display_screen_text: displayScreenText,
        display_katex_row_gap_em: cumulativeGap.value,
        display_katex_rows: cloneKatexRows(cumulativeRows),
        display_katex: toAlignedKatexRows(cumulativeRows, cumulativeGap.value),
      }
    }

    return {
      ...safeSlide,
      display_screen_text: displayScreenText,
      display_katex: baseKatex,
    }
  })
})

const coverSlide = computed(() => makeCoverSlide(baseSlidesForRender.value[0]))
const slidesForRender = computed(() => {
  const cover = coverSlide.value
  return cover ? [cover, ...baseSlidesForRender.value] : baseSlidesForRender.value
})
const videoSlidesForRender = computed(() => slidesForRender.value.filter((slide) => !isVirtualCoverSlide(slide)))

const totalReelDurationLabel = computed(() => {
  const total = videoSlidesForRender.value.reduce((sum, slide) => {
    const s = Number(slide?.duration_seconds)
    return sum + (Number.isFinite(s) && s > 0 ? s : 4)
  }, 0)
  if (!total) return null
  const mins = Math.floor(total / 60)
  const secs = Math.round(total % 60)
  return mins > 0 ? `${mins}m${secs > 0 ? String(secs).padStart(2, '0') + 's' : ''}` : `${secs}s`
})

const activeSlide = computed(() => {
  if (!slidesForRender.value.length) return null
  const index = Math.min(Math.max(fullscreenIndex.value, 0), slidesForRender.value.length - 1)
  return slidesForRender.value[index] || null
})

const activeSlideInline = computed(() => Boolean(activeSlide.value?.katex_inline_with_previous))
const activeSlideInlineOffset = computed(() => clampInlineOffset(activeSlide.value?.katex_inline_offset_percent))
const activeSlideInlineSeparator = computed(() => normalizeInlineSeparator(activeSlide.value?.katex_inline_separator))
const activeSlideInlineVerticalOffset = computed(() => clampInlineVerticalOffset(activeSlide.value?.katex_inline_vertical_offset_em))
const activeInlineOffsetLabel = computed(() => {
  const offset = Math.round(activeSlideInlineOffset.value)
  if (!offset) return 'milieu'
  return offset > 0 ? `+${offset}%` : `${offset}%`
})
const activeInlineVerticalOffsetLabel = computed(() => {
  const offset = activeSlideInlineVerticalOffset.value
  if (!offset) return '0'
  return offset > 0 ? `+${offset.toFixed(2)}em` : `${offset.toFixed(2)}em`
})
const cumulativeGapLabel = computed(() => `${cumulativeGap.value.toFixed(1)}em`)
const activeSlideResetsCumulative = computed(() => Boolean(activeSlide.value?.katex_reset_cumulative))
const activeSlideDropsPreviousLine = computed(() => Boolean(activeSlide.value?.katex_drop_previous_line))
const activeSlideKatexRevealWithSpeech = computed(() => Boolean(activeSlide.value?.katex_reveal_with_speech))
const activeSlideCanAnimateKatex = computed(() => (
  Boolean(activeSlide.value?.id)
  && !isVirtualCoverSlide(activeSlide.value)
  && Boolean(
    activeKatexDraftText.value
    || normalizeText(activeSlide.value?.katex)
    || normalizeText(activeSlide.value?.display_katex)
  )
))
const katexSpeechRevealLabel = computed(() => (activeSlideKatexRevealWithSpeech.value ? 'Activée' : 'Désactivée'))
const canToggleKatexLineMode = computed(() => {
  if (!activeSlide.value || isEdgeSlide(activeSlide.value)) return false

  for (let index = fullscreenIndex.value - 1; index >= 0; index -= 1) {
    const previousSlide = slidesForRender.value[index]
    if (!previousSlide) return false
    if (isVirtualCoverSlide(previousSlide)) return false
    if (isEdgeSlide(previousSlide)) return false
    return true
  }

  return false
})
const lineModeLabel = computed(() => (activeSlideInline.value ? 'Même ligne' : 'Nouvelle ligne'))
const resetCumulativeLabel = computed(() => 'Nouvelle page')
const dropPreviousLineLabel = computed(() => (activeSlideDropsPreviousLine.value ? 'Ligne préc. supprimée' : 'Suppr. ligne préc.'))

function findIndexById(slideId) {
  return slidesForRender.value.findIndex((slide) => Number(slide.id) === Number(slideId))
}

function selectSlideByIndex(index) {
  const slide = slidesForRender.value[index]
  if (!slide?.id || isVirtualCoverSlide(slide)) return
  emit('select-slide', slide.id)
}

function openFullscreenAt(index) {
  if (!slidesForRender.value.length) return
  const maxIndex = slidesForRender.value.length - 1
  const requestedIndex = Math.min(Math.max(index, 0), maxIndex)
  const normalizedIndex = isVirtualCoverSlide(slidesForRender.value[requestedIndex])
    ? firstVideoSlideIndex()
    : requestedIndex
  if (normalizedIndex === -1) return

  fullscreenIndex.value = normalizedIndex
  isFullscreen.value = true
  fullscreenEditorTab.value = 'speech'
  annotationActiveTool.value = 'select'
  annotationSelectedId.value = null
  selectSlideByIndex(normalizedIndex)
  syncSpeechDraftFromActiveSlide({ force: true })
  syncKatexDraftFromActiveSlide({ force: true })
}

function firstVideoSlideIndex() {
  return slidesForRender.value.findIndex((slide) => !isVirtualCoverSlide(slide))
}

function findNextSequentialVideoSlideIndex(startIndex) {
  for (let index = startIndex + 1; index < slidesForRender.value.length; index += 1) {
    if (!isVirtualCoverSlide(slidesForRender.value[index])) return index
  }

  return -1
}

function findAdjacentVideoSlideIndex(startIndex, direction) {
  if (!slidesForRender.value.length) return -1

  const total = slidesForRender.value.length
  for (let step = 1; step <= total; step += 1) {
    const nextIndex = (startIndex + direction * step + total) % total
    if (!isVirtualCoverSlide(slidesForRender.value[nextIndex])) return nextIndex
  }

  return -1
}

function closeFullscreen() {
  stopFullPreview()
  flushYoutubeInlinePatch()
  saveActiveSpeechDraft()
  saveActiveKatexDraft()
  if (isYoutubeFormat.value && activeSlide.value?.id && !isVirtualCoverSlide(activeSlide.value)) {
    emit('select-slide', activeSlide.value.id)
  }
  annotationActiveTool.value = 'select'
  annotationSelectedId.value = null
  isFullscreen.value = false
}

async function moveFullscreenToIndex(index, { syncSelection = !isYoutubeFormat.value, waitForDom = false } = {}) {
  const slide = slidesForRender.value[index]
  if (!slide?.id || isVirtualCoverSlide(slide)) return false

  flushYoutubeInlinePatch(activeSlide.value?.id)
  saveActiveSpeechDraft()
  saveActiveKatexDraft()
  fullscreenEditorTab.value = 'speech'
  annotationSelectedId.value = null
  fullscreenIndex.value = index
  speechAudioCurrentTime.value = 0
  speechAudioPlaying.value = false
  stopSpeechAudioRaf()
  clearSpeechFadeTimers()
  if (syncSelection) {
    selectSlideByIndex(index)
  }
  syncSpeechDraftFromActiveSlide({ force: true })
  syncKatexDraftFromActiveSlide({ force: true })
  if (waitForDom) {
    await nextTick()
  }
  return true
}

function stopFullPreview({ resetAudio = true } = {}) {
  isFullPreviewPlaying.value = false
  clearFullPreviewTimer()
  clearSpeechFadeTimers()

  if (!resetAudio) return
  const audio = fullPreviewPlayerRef.value
  if (!audio) return

  audio.pause()
  audio.volume = speechFullPreviewTargetVolume
  speechAudioPlaying.value = false
  try {
    audio.currentTime = 0
    speechAudioCurrentTime.value = 0
  } catch (error) {
    console.warn('Impossible de remettre la lecture audio au debut:', error)
  }
}

function clearFullPreviewTimer() {
  if (!fullPreviewTimerId || typeof window === 'undefined') return
  window.clearTimeout(fullPreviewTimerId)
  fullPreviewTimerId = null
}

function getFullPreviewSlideDurationMs(slide) {
  const seconds = Number(slide?.duration_seconds)
  const safeSeconds = Number.isFinite(seconds) && seconds > 0 ? seconds : 4
  return Math.max(300, Math.round(safeSeconds * 1000))
}

function scheduleSilentFullPreviewAdvance() {
  if (typeof window === 'undefined') {
    advanceFullPreview()
    return
  }

  clearFullPreviewTimer()
  fullPreviewTimerId = window.setTimeout(() => {
    fullPreviewTimerId = null
    advanceFullPreview()
  }, getFullPreviewSlideDurationMs(activeSlide.value))
}

async function playActiveSpeechForFullPreview() {
  await nextTick()
  if (!isFullPreviewPlaying.value) return

  clearFullPreviewTimer()
  clearSpeechFadeTimers()
  const audio = fullPreviewPlayerRef.value
  if (!audio || !activeSlideSpeechAudioUrl.value) {
    scheduleSilentFullPreviewAdvance()
    return
  }

  try {
    audio.src = activeSlideSpeechAudioUrl.value
    audio.currentTime = 0
    speechAudioCurrentTime.value = 0
    audio.volume = 0
    await audio.play()
    rampSpeechVolume(audio, 0, speechFullPreviewTargetVolume, SPEECH_FADE_MS)
  } catch (error) {
    console.error('Erreur lecture audio complete:', error)
    stopFullPreview()
    window.alert("Lecture audio bloquee par le navigateur. Clique a nouveau sur Ecouter tout.")
  }
}

async function startFullPreview() {
  if (isFullPreviewPlaying.value || !videoSlidesForRender.value.length) return
  if (!validateFullPreviewAudio()) return

  const firstSlideIndex = firstVideoSlideIndex()
  if (firstSlideIndex === -1) {
    window.alert('Aucune slide a lire pour ce reel.')
    return
  }

  isFullPreviewPlaying.value = true
  const moved = await moveFullscreenToIndex(firstSlideIndex)
  if (!moved) {
    stopFullPreview({ resetAudio: false })
    return
  }

  await playActiveSpeechForFullPreview()
}

async function advanceFullPreview() {
  if (!isFullPreviewPlaying.value) return

  const nextSlideIndex = findNextSequentialVideoSlideIndex(fullscreenIndex.value)
  if (nextSlideIndex === -1) {
    stopFullPreview({ resetAudio: false })
    return
  }

  const moved = await moveFullscreenToIndex(nextSlideIndex)
  if (!moved) {
    stopFullPreview({ resetAudio: false })
    return
  }

  await playActiveSpeechForFullPreview()
}

function toggleFullPreview() {
  if (isFullPreviewPlaying.value) {
    stopFullPreview()
    return
  }

  startFullPreview()
}

function handleSpeechEnded() {
  speechAudioPlaying.value = false
  stopSpeechAudioRaf()
  if (!isFullPreviewPlaying.value) return
  advanceFullPreview()
}

function handleSpeechError() {
  speechAudioPlaying.value = false
  stopSpeechAudioRaf()
  if (!isFullPreviewPlaying.value) return
  stopFullPreview({ resetAudio: false })
  window.alert("Lecture complete arretee: le MP3 de cette slide n'a pas pu etre lu.")
}

function handleSpeechTimeUpdate(event) {
  const audio = event?.target
  if (!audio) return
  speechAudioCurrentTime.value = Number(audio.currentTime) || 0
}

function handleSpeechPlay() {
  speechAudioPlaying.value = true
  startSpeechAudioRaf()
}

function handleSpeechPause() {
  speechAudioPlaying.value = false
  stopSpeechAudioRaf()
  clearSpeechFadeTimers()
}

function handleSpeechLoadedMetadata() {}

function saveActiveSpeechDraft() {
  if (!activeSlide.value?.id || !activeSpeechDraftDirty.value) return false

  const voiceScript = String(speechDraft.value || '').trim()
  speechDraft.value = voiceScript
  speechDraftSavedValue.value = voiceScript
  speechDraftSlideId.value = Number(activeSlide.value.id)

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      voice_script: voiceScript,
    },
  })

  return true
}

function saveActiveKatexDraft() {
  if (!activeSlide.value?.id || !activeKatexDraftDirty.value || isVirtualCoverSlide(activeSlide.value)) return false

  const katexValue = activeKatexDraftText.value
  katexDraft.value = katexValue
  katexDraftSavedValue.value = katexValue
  katexDraftSlideId.value = Number(activeSlide.value.id)

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex: katexValue,
    },
  })

  return true
}

function applyKatexColor(colorHex) {
  const el = katexTextareaRef.value
  if (!el) return

  const start = el.selectionStart
  const end = el.selectionEnd
  const current = katexDraft.value

  if (start === end) {
    const before = current.slice(0, start)
    const after = current.slice(end)
    const inserted = `\\textcolor{${colorHex}}{}`
    katexDraft.value = before + inserted + after
    nextTick(() => {
      el.focus()
      const cursorPos = start + inserted.length - 1
      el.setSelectionRange(cursorPos, cursorPos)
    })
    return
  }

  const selected = current.slice(start, end)
  const before = current.slice(0, start)
  const after = current.slice(end)
  const wrapped = `\\textcolor{${colorHex}}{${selected}}`
  katexDraft.value = before + wrapped + after
  nextTick(() => {
    el.focus()
    el.setSelectionRange(start, start + wrapped.length)
  })
}

function clampMathScale(value) {
  return Math.min(1.3, Math.max(0.75, Number(value.toFixed(2))))
}

function decreaseMathSize() {
  const target = getActiveMathScaleRef()
  target.value = clampMathScale(target.value - 0.05)
}

function increaseMathSize() {
  const target = getActiveMathScaleRef()
  target.value = clampMathScale(target.value + 0.05)
}

function resetMathSize() {
  getActiveMathScaleRef().value = 1
}

function clampSafeZoneScale(value) {
  const min = isYoutubeFormat.value ? 0 : 0.7
  return Math.min(1.4, Math.max(min, Number(value.toFixed(2))))
}

function decreaseSafeZoneX() {
  safeZoneXScale.value = clampSafeZoneScale(safeZoneXScale.value - 0.05)
}

function increaseSafeZoneX() {
  safeZoneXScale.value = clampSafeZoneScale(safeZoneXScale.value + 0.05)
}

function safeZoneDefaultForFormat() {
  return isYoutubeFormat.value ? SAFE_ZONE_DEFAULT_SCALE_YOUTUBE : SAFE_ZONE_DEFAULT_SCALE
}

function resetSafeZoneX() {
  safeZoneXScale.value = safeZoneDefaultForFormat()
}

function decreaseSafeZoneY() {
  const target = getActiveSafeZoneYRef()
  target.value = clampSafeZoneScale(target.value - 0.05)
}

function increaseSafeZoneY() {
  const target = getActiveSafeZoneYRef()
  target.value = clampSafeZoneScale(target.value + 0.05)
}

function resetSafeZoneY() {
  getActiveSafeZoneYRef().value = safeZoneDefaultForFormat()
}

function applyFormatDefaults() {
  const isYt = isYoutubeFormat.value
  const safeDefault = isYt ? SAFE_ZONE_DEFAULT_SCALE_YOUTUBE : SAFE_ZONE_DEFAULT_SCALE
  const mathDefault = isYt ? MATH_SCALE_DEFAULT_YOUTUBE : MATH_SCALE_DEFAULT_REEL
  const gapDefault = isYt ? CUMULATIVE_GAP_DEFAULT_YOUTUBE : CUMULATIVE_GAP_DEFAULT
  safeZoneXScale.value = safeDefault
  safeZoneMathYScale.value = safeDefault
  safeZoneHookYScale.value = safeDefault
  safeZoneCtaYScale.value = safeDefault
  mathScaleCalcul.value = mathDefault
  mathScaleHook.value = mathDefault
  mathScaleCta.value = mathDefault
  cumulativeGap.value = gapDefault
}

function patchActiveEdgeSlideScale(field, value) {
  if (!activeSlide.value?.id || !isEdgeSlide(activeSlide.value)) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      [field]: getSlideScale(value),
    },
  })
}

function decreaseActiveTitleSize() {
  patchActiveEdgeSlideScale('title_scale', getSlideScale(activeSlide.value?.title_scale) - 0.05)
}

function increaseActiveTitleSize() {
  patchActiveEdgeSlideScale('title_scale', getSlideScale(activeSlide.value?.title_scale) + 0.05)
}

function resetActiveTitleSize() {
  patchActiveEdgeSlideScale('title_scale', 1)
}

function decreaseActiveTextSize() {
  patchActiveEdgeSlideScale('screen_text_scale', getSlideScale(activeSlide.value?.screen_text_scale) - 0.05)
}

function increaseActiveTextSize() {
  patchActiveEdgeSlideScale('screen_text_scale', getSlideScale(activeSlide.value?.screen_text_scale) + 0.05)
}

function resetActiveTextSize() {
  patchActiveEdgeSlideScale('screen_text_scale', 1)
}

function toggleActiveKatexLineMode() {
  if (!canToggleKatexLineMode.value || !activeSlide.value?.id) return

  const nextInline = !activeSlideInline.value
  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex_inline_with_previous: nextInline,
      ...(nextInline
        ? {
            katex_inline_offset_percent: 0,
            katex_inline_vertical_offset_em: 0,
            katex_inline_separator: activeSlideInlineSeparator.value,
          }
        : {}),
    },
  })
}

function setActiveInlineSeparator(value) {
  if (!activeSlide.value?.id || !activeSlideInline.value || isEdgeSlide(activeSlide.value)) return

  patchActiveYoutubeInlineLayout({
    katex_inline_separator: normalizeInlineSeparator(value),
  })
}

function applyLocalSlidePatch(slideId, patch) {
  if (!slideId || !patch || typeof patch !== 'object') return

  const key = String(slideId)
  localSlidePatches.value = {
    ...localSlidePatches.value,
    [key]: {
      ...(localSlidePatches.value[key] || {}),
      ...patch,
    },
  }
}

function emitSlidePatch(slideId, patch) {
  if (!slideId || !patch || typeof patch !== 'object' || !Object.keys(patch).length) return
  emit('update-slide', { id: slideId, patch })
}

function flushYoutubeInlinePatch(slideId = null) {
  const keys = slideId ? [String(slideId)] : Array.from(pendingYoutubeInlinePatches.keys())
  keys.forEach((key) => {
    const timer = youtubeInlinePatchTimers.get(key)
    if (timer) {
      clearTimeout(timer)
      youtubeInlinePatchTimers.delete(key)
    }

    const patch = pendingYoutubeInlinePatches.get(key)
    pendingYoutubeInlinePatches.delete(key)
    if (patch) {
      emitSlidePatch(key, patch)
    }
  })
}

function patchActiveYoutubeInlineLayout(patch) {
  if (!activeSlide.value?.id || !activeSlideInline.value || isEdgeSlide(activeSlide.value)) return

  const slideId = activeSlide.value.id
  if (!isYoutubeFormat.value || !isFullscreen.value) {
    emitSlidePatch(slideId, patch)
    return
  }

  const key = String(slideId)
  applyLocalSlidePatch(slideId, patch)
  pendingYoutubeInlinePatches.set(key, {
    ...(pendingYoutubeInlinePatches.get(key) || {}),
    ...patch,
  })

  const currentTimer = youtubeInlinePatchTimers.get(key)
  if (currentTimer) clearTimeout(currentTimer)

  youtubeInlinePatchTimers.set(key, window.setTimeout(() => {
    youtubeInlinePatchTimers.delete(key)
    const pendingPatch = pendingYoutubeInlinePatches.get(key)
    pendingYoutubeInlinePatches.delete(key)
    emitSlidePatch(slideId, pendingPatch)
  }, YOUTUBE_INLINE_PATCH_DEBOUNCE_MS))
}

function patchActiveInlineOffset(value) {
  patchActiveYoutubeInlineLayout({
    katex_inline_offset_percent: clampInlineOffset(value),
  })
}

function decreaseActiveInlineOffset() {
  patchActiveInlineOffset(activeSlideInlineOffset.value - INLINE_OFFSET_STEP)
}

function increaseActiveInlineOffset() {
  patchActiveInlineOffset(activeSlideInlineOffset.value + INLINE_OFFSET_STEP)
}

function resetActiveInlineOffset() {
  patchActiveInlineOffset(0)
}

function patchActiveInlineVerticalOffset(value) {
  patchActiveYoutubeInlineLayout({
    katex_inline_vertical_offset_em: clampInlineVerticalOffset(value),
  })
}

function decreaseActiveInlineVerticalOffset() {
  patchActiveInlineVerticalOffset(activeSlideInlineVerticalOffset.value - INLINE_VERTICAL_OFFSET_STEP)
}

function increaseActiveInlineVerticalOffset() {
  patchActiveInlineVerticalOffset(activeSlideInlineVerticalOffset.value + INLINE_VERTICAL_OFFSET_STEP)
}

function resetActiveInlineVerticalOffset() {
  patchActiveInlineVerticalOffset(0)
}

function toggleActiveResetCumulative() {
  if (!activeSlide.value?.id || isEdgeSlide(activeSlide.value)) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex_reset_cumulative: !activeSlideResetsCumulative.value,
    },
  })
}

function toggleActiveDropPreviousLine() {
  if (!activeSlide.value?.id || isEdgeSlide(activeSlide.value)) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex_drop_previous_line: !activeSlideDropsPreviousLine.value,
    },
  })
}

function toggleActiveKatexSpeechReveal() {
  if (!activeSlideCanAnimateKatex.value) return

  emit('update-slide', {
    id: activeSlide.value.id,
    patch: {
      katex_reveal_with_speech: !activeSlideKatexRevealWithSpeech.value,
    },
  })
}

function setCumulativeGap(value) {
  cumulativeGap.value = clampCumulativeGap(value)
}

function decreaseCumulativeGap() {
  setCumulativeGap(cumulativeGap.value - CUMULATIVE_GAP_STEP)
}

function increaseCumulativeGap() {
  setCumulativeGap(cumulativeGap.value + CUMULATIVE_GAP_STEP)
}

function resetCumulativeGap() {
  setCumulativeGap(CUMULATIVE_GAP_DEFAULT)
}

function setAnnotationTool(tool) {
  annotationActiveTool.value = tool
  if (tool !== 'select') annotationSelectedId.value = null
}

function decreaseAnnotationStroke() {
  annotationStrokeWidth.value = Math.max(1, annotationStrokeWidth.value - 1)
}

function increaseAnnotationStroke() {
  annotationStrokeWidth.value = Math.min(10, annotationStrokeWidth.value + 1)
}

function handleAnnotationAdd(shape) {
  if (!activeSlide.value?.id || isVirtualCoverSlide(activeSlide.value)) return
  const current = Array.isArray(activeSlide.value.annotations) ? activeSlide.value.annotations : []
  emit('update-slide', {
    id: activeSlide.value.id,
    patch: { annotations: [...current, shape] },
  })
}

function handleAnnotationUpdate(updated) {
  if (!activeSlide.value?.id || isVirtualCoverSlide(activeSlide.value)) return
  const current = Array.isArray(activeSlide.value.annotations) ? activeSlide.value.annotations : []
  emit('update-slide', {
    id: activeSlide.value.id,
    patch: { annotations: current.map((a) => (a.id === updated.id ? updated : a)) },
  })
}

function deleteSelectedAnnotation() {
  if (!annotationSelectedId.value || !activeSlide.value?.id || isVirtualCoverSlide(activeSlide.value)) return
  const current = Array.isArray(activeSlide.value.annotations) ? activeSlide.value.annotations : []
  const idToDelete = annotationSelectedId.value
  annotationSelectedId.value = null
  emit('update-slide', {
    id: activeSlide.value.id,
    patch: { annotations: current.filter((a) => a.id !== idToDelete) },
  })
}

function handleAnnotationDelete(shapeId) {
  if (!shapeId || !activeSlide.value?.id || isVirtualCoverSlide(activeSlide.value)) return
  const current = Array.isArray(activeSlide.value.annotations) ? activeSlide.value.annotations : []
  if (annotationSelectedId.value === shapeId) {
    annotationSelectedId.value = null
  }
  emit('update-slide', {
    id: activeSlide.value.id,
    patch: { annotations: current.filter((a) => a.id !== shapeId) },
  })
}

function clearAllAnnotations() {
  if (!activeSlide.value?.id || isVirtualCoverSlide(activeSlide.value)) return
  annotationSelectedId.value = null
  emit('update-slide', {
    id: activeSlide.value.id,
    patch: { annotations: [] },
  })
}

const safePronunciationOverrides = computed(() => {
  const voiceId = String(props.activeVoiceId || '').trim()
  if (voiceId) {
    const byVoice = props.pronunciationOverridesByVoice || {}
    const voiceList = byVoice[voiceId]
    if (Array.isArray(voiceList)) {
      return voiceList.filter((o) => o && o.word && o.pronunciation)
    }
  }
  return Array.isArray(props.pronunciationOverrides)
    ? props.pronunciationOverrides.filter((o) => o && o.word && o.pronunciation)
    : []
})

const pronunciationOverridesByLowerWord = computed(() => {
  const map = new Map()
  for (const override of safePronunciationOverrides.value) {
    map.set(String(override.word).toLowerCase(), override)
  }
  return map
})

const speechWordTokens = computed(() => {
  const text = String(speechDraft.value || '')
  if (!text) return []

  const tokens = []
  const regex = /([\p{L}\p{M}][\p{L}\p{M}\p{N}'’-]*)|([^\p{L}\p{M}\p{N}]+)/gu
  let key = 0
  for (const match of text.matchAll(regex)) {
    const word = match[1]
    const separator = match[2]
    if (word) {
      const override = pronunciationOverridesByLowerWord.value.get(word.toLowerCase()) || null
      tokens.push({ key: key++, type: 'word', text: word, override })
    } else if (separator) {
      tokens.push({ key: key++, type: 'sep', text: separator })
    }
  }
  return tokens
})

function normalizeOverrideLanguage(value) {
  const raw = String(value || '').trim().toLowerCase()
  return PRONUNCIATION_LANGUAGE_LABELS[raw] ? raw : 'fr'
}

function openPronunciationEditor(token, event) {
  if (!token || token.type !== 'word') return
  pronunciationEditorWord.value = token.text
  pronunciationEditorPronunciation.value = token.override?.pronunciation || ''
  pronunciationEditorLanguage.value = normalizeOverrideLanguage(token.override?.language)
  pronunciationEditorAnchor.value = event?.currentTarget || null
  pronunciationEditorOpen.value = true
  nextTick(() => {
    pronunciationInputRef.value?.focus()
    pronunciationInputRef.value?.select?.()
  })
}

function closePronunciationEditor() {
  pronunciationEditorOpen.value = false
  pronunciationEditorWord.value = ''
  pronunciationEditorPronunciation.value = ''
  pronunciationEditorLanguage.value = 'fr'
  pronunciationEditorAnchor.value = null
}

function emitPronunciationUpdate(nextOverrides) {
  const voiceId = String(props.activeVoiceId || '').trim()
  if (voiceId) {
    emit('update-pronunciation-overrides-by-voice', { voiceId, overrides: nextOverrides })
  } else {
    emit('update-pronunciation-overrides', nextOverrides)
  }
}

function commitPronunciationFromEditor() {
  const word = String(pronunciationEditorWord.value || '').trim()
  const pronunciation = String(pronunciationEditorPronunciation.value || '').trim()
  const language = normalizeOverrideLanguage(pronunciationEditorLanguage.value)
  if (!word) {
    closePronunciationEditor()
    return
  }

  const lowerWord = word.toLowerCase()
  const filtered = safePronunciationOverrides.value.filter(
    (o) => String(o.word).toLowerCase() !== lowerWord
  )
  const next = pronunciation ? [...filtered, { word, pronunciation, language }] : filtered
  emitPronunciationUpdate(next)
  closePronunciationEditor()
}

function removePronunciationFromEditor() {
  const word = String(pronunciationEditorWord.value || '').trim()
  if (!word) {
    closePronunciationEditor()
    return
  }
  const lowerWord = word.toLowerCase()
  const next = safePronunciationOverrides.value.filter(
    (o) => String(o.word).toLowerCase() !== lowerWord
  )
  emitPronunciationUpdate(next)
  closePronunciationEditor()
}

const showVoiceOverridesPanel = ref(false)

const voiceNameById = computed(() => {
  const map = new Map()
  for (const v of (props.voiceList || [])) {
    if (v?.voice_id) map.set(String(v.voice_id), String(v.name || v.voice_id))
  }
  return map
})

const allVoiceOverrideEntries = computed(() => {
  const byVoice = props.pronunciationOverridesByVoice || {}
  return Object.entries(byVoice)
    .map(([voiceId, overrides]) => ({
      voiceId,
      voiceName: voiceNameById.value.get(voiceId) || voiceId,
      overrides: Array.isArray(overrides) ? overrides.filter((o) => o?.word && o?.pronunciation) : [],
    }))
    .filter((entry) => entry.overrides.length > 0)
})

const hasAnyVoiceOverrides = computed(() => allVoiceOverrideEntries.value.length > 0)

function removeVoiceWordOverride(voiceId, word) {
  const byVoice = props.pronunciationOverridesByVoice || {}
  const currentList = Array.isArray(byVoice[voiceId]) ? byVoice[voiceId] : []
  const lowerWord = String(word || '').toLowerCase()
  const next = currentList.filter((o) => String(o.word || '').toLowerCase() !== lowerWord)
  emit('update-pronunciation-overrides-by-voice', { voiceId, overrides: next })
}

function clearAllVoiceOverrides(voiceId) {
  emit('update-pronunciation-overrides-by-voice', { voiceId, overrides: [] })
}

function generateActiveSlideSpeech() {
  if (!activeSlide.value?.id || !activeSpeechDraftText.value || isGeneratingActiveSpeech.value) return

  const voiceScript = String(speechDraft.value || '').trim()
  const shouldSaveVoiceScript = activeSpeechDraftDirty.value
  if (shouldSaveVoiceScript) {
    speechDraft.value = voiceScript
    speechDraftSavedValue.value = voiceScript
    speechDraftSlideId.value = Number(activeSlide.value.id)
  }

  emit('generate-slide-speech', {
    id: activeSlide.value.id,
    text: activeSpeechDraftText.value,
    voice_script: voiceScript,
    save_voice_script: shouldSaveVoiceScript,
  })
}

function setExportSlideRef(el, index) {
  if (el) {
    exportSlideRefs.value[index] = el
  }
}

function waitForNextPaint() {
  if (typeof window === 'undefined') {
    return Promise.resolve()
  }

  const isDocumentHidden = typeof document !== 'undefined' && document.hidden
  if (isDocumentHidden || typeof window.requestAnimationFrame !== 'function') {
    return new Promise((resolve) => window.setTimeout(resolve, isDocumentHidden ? 80 : 0))
  }

  return new Promise((resolve) => {
    let resolved = false
    let firstFrameId = null
    let secondFrameId = null
    let timeoutId = null

    const finish = () => {
      if (resolved) return
      resolved = true
      if (firstFrameId !== null) window.cancelAnimationFrame(firstFrameId)
      if (secondFrameId !== null) window.cancelAnimationFrame(secondFrameId)
      if (timeoutId !== null) window.clearTimeout(timeoutId)
      resolve()
    }

    timeoutId = window.setTimeout(finish, 250)
    firstFrameId = window.requestAnimationFrame(() => {
      firstFrameId = null
      secondFrameId = window.requestAnimationFrame(finish)
    })
  })
}

async function waitForExportRender() {
  await nextTick()

  if (typeof document !== 'undefined' && document.fonts?.ready) {
    await document.fonts.ready.catch(() => {})
  }

  await waitForNextPaint()
}

async function downloadCanvasPng(canvas, filename) {
  const blob = await new Promise((resolve) => {
    canvas.toBlob((result) => resolve(result), 'image/png', 1)
  })
  const link = document.createElement('a')
  link.download = filename

  if (blob) {
    const url = URL.createObjectURL(blob)
    link.href = url
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.setTimeout(() => URL.revokeObjectURL(url), 1200)
    return
  }

  link.href = canvas.toDataURL('image/png')
  document.body.appendChild(link)
  link.click()
  link.remove()
}

function blobToDataUrl(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(reader.error)
    reader.readAsDataURL(blob)
  })
}

async function canvasToImageDataUrl(canvas, exportPreset) {
  const imageType = exportPreset?.imageType || 'image/png'
  const imageQuality = exportPreset?.imageQuality ?? 1
  const blob = await new Promise((resolve) => {
    canvas.toBlob((result) => resolve(result), imageType, imageQuality)
  })

  if (blob) {
    return blobToDataUrl(blob)
  }

  return canvas.toDataURL(imageType, imageQuality)
}

async function renderExportCanvas(index, dimensions = {}) {
  const frame = exportSlideRefs.value[index]
  const target = frame?.querySelector('.reel-slide') || frame
  if (!target) return null
  const width = dimensions.width || PNG_EXPORT_WIDTH.value
  const height = dimensions.height || PNG_EXPORT_HEIGHT.value

  return html2canvas(target, {
    backgroundColor: '#f8fbff',
    height,
    logging: false,
    scale: 1,
    scrollX: 0,
    scrollY: 0,
    useCORS: true,
    width,
    windowHeight: height,
    windowWidth: width,
  })
}

async function exportAllSlidesPng() {
  if (!slidesForRender.value.length || exportingPng.value) return

  exportFrameWidth.value = PNG_EXPORT_WIDTH.value
  exportFrameHeight.value = PNG_EXPORT_HEIGHT.value
  exportingPng.value = true
  pngExportMounted.value = true
  pngExportProgress.value = 0
  exportSlideRefs.value = []

  try {
    await waitForExportRender()

    let exportedSlideNumber = 0
    for (const [index] of slidesForRender.value.entries()) {
      const canvas = await renderExportCanvas(index)
      if (!canvas) continue

      const isCover = isVirtualCoverSlide(slidesForRender.value[index])
      if (!isCover) exportedSlideNumber += 1
      const filename = isCover
        ? COVER_FILENAME
        : `optitab-reel-slide-${String(exportedSlideNumber).padStart(2, '0')}.png`
      await downloadCanvasPng(canvas, filename)
      pngExportProgress.value = index + 1
      await new Promise((resolve) => window.setTimeout(resolve, 180))
    }
  } catch (error) {
    console.error('Erreur export PNG:', error)
    window.alert("Erreur lors de l'export PNG. Réessaie après avoir vérifié les slides.")
  } finally {
    pngExportMounted.value = false
    exportingPng.value = false
    exportSlideRefs.value = []
  }
}

async function exportAllSlidesVideo(mode = 'fast') {
  const videoSlides = videoSlidesForRender.value
  if (!videoSlides.length || isVideoExportBusy.value || exportingPng.value) return
  const exportPreset = VIDEO_EXPORT_PRESETS.value[mode] || VIDEO_EXPORT_PRESETS.value.fast

  const slidesMissingAudio = videoSlides.filter((slide) => (
    slideSpeechText(slide) && !normalizeText(slide?.speech_audio_url)
  ))
  if (slidesMissingAudio.length) {
    window.alert(`${slidesMissingAudio.length} slide(s) ont un script voix sans MP3. Genere les MP3 slides avant l export MP4.`)
    return
  }

  const slidesWithStaleAudio = videoSlides.filter((slide) => isSlideSpeechAudioStale(slide))
  if (slidesWithStaleAudio.length) {
    window.alert(`${slidesWithStaleAudio.length} slide(s) ont un MP3 pas a jour. Regenere les MP3 slides avant l export MP4.`)
    return
  }

  videoExportMode.value = mode
  exportFrameWidth.value = exportPreset.width
  exportFrameHeight.value = exportPreset.height
  preparingVideoFrames.value = true
  pngExportMounted.value = true
  videoFrameProgress.value = 0
  exportSlideRefs.value = []

  try {
    await waitForExportRender()

    const coverIndex = slidesForRender.value.findIndex((slide) => isVirtualCoverSlide(slide))
    if (coverIndex !== -1) {
      const coverCanvas = await renderExportCanvas(coverIndex, exportPreset)
      if (coverCanvas) {
        await downloadCanvasPng(coverCanvas, COVER_FILENAME)
        await new Promise((resolve) => window.setTimeout(resolve, 180))
      }
    }

    const frames = []
    for (const [index, slide] of videoSlides.entries()) {
      const renderIndex = slidesForRender.value.findIndex((renderSlide) => renderSlide.id === slide.id)
      const canvas = await renderExportCanvas(renderIndex, exportPreset)
      if (!canvas) continue

      frames.push({
        slide_id: slide.id,
        image: await canvasToImageDataUrl(canvas, exportPreset),
        duration_seconds: Number(slide.duration_seconds) || 4,
      })
      videoFrameProgress.value = index + 1
      await waitForNextPaint()
    }

    if (!frames.length) {
      window.alert("Aucune frame video n'a pu etre preparee.")
      return
    }

    emit('export-video', {
      frames,
      width: exportPreset.width,
      height: exportPreset.height,
      fps: exportPreset.fps,
      crf: exportPreset.crf,
      preset: exportPreset.ffmpegPreset,
      show_subtitles: showSubtitles.value,
    })
  } catch (error) {
    console.error('Erreur export video:', error)
    window.alert("Erreur lors de la preparation video. Reessaie apres avoir verifie les slides.")
  } finally {
    pngExportMounted.value = false
    preparingVideoFrames.value = false
    exportSlideRefs.value = []
  }
}

function handleSelectSlide(slideId) {
  const index = findIndexById(slideId)
  if (index === -1) return
  selectSlideByIndex(index)
}

function handleOpenSlideFullscreen(slideId) {
  const index = findIndexById(slideId)
  if (index === -1) return
  openFullscreenAt(index)
}

function openFromCurrent() {
  if (!slidesForRender.value.length) return
  const indexFromSelection = findIndexById(props.selectedSlideId)
  openFullscreenAt(indexFromSelection === -1 ? firstVideoSlideIndex() : indexFromSelection)
}

function goNext() {
  if (!slidesForRender.value.length) return
  stopFullPreview()
  const nextIndex = findAdjacentVideoSlideIndex(fullscreenIndex.value, 1)
  if (nextIndex === -1) return
  moveFullscreenToIndex(nextIndex)
}

function goPrev() {
  if (!slidesForRender.value.length) return
  stopFullPreview()
  const prevIndex = findAdjacentVideoSlideIndex(fullscreenIndex.value, -1)
  if (prevIndex === -1) return
  moveFullscreenToIndex(prevIndex)
}

function handleKeydown(event) {
  if (!isFullscreen.value) return
  if (isEditableKeyTarget(event.target)) return

  if (event.key === 'Escape') {
    event.preventDefault()
    if (annotationSelectedId.value) {
      annotationSelectedId.value = null
    } else if (annotationActiveTool.value !== 'select') {
      annotationActiveTool.value = 'select'
    } else {
      closeFullscreen()
    }
    return
  }

  if ((event.key === 'Delete' || event.key === 'Backspace') && annotationSelectedId.value) {
    event.preventDefault()
    deleteSelectedAnnotation()
    return
  }

  if (event.key === 'ArrowRight') {
    event.preventDefault()
    goNext()
    return
  }

  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    goPrev()
  }
}

function isEditableKeyTarget(target) {
  if (!target || typeof target.closest !== 'function') return false
  return Boolean(target.closest('textarea, input, select, [contenteditable="true"]'))
}

watch(
  () => props.selectedSlideId,
  (slideId) => {
    if (!isFullscreen.value || slideId === null || slideId === undefined) return
    if (
      activeSpeechDraftDirty.value &&
      activeSlide.value?.id &&
      Number(activeSlide.value.id) !== Number(slideId)
    ) {
      saveActiveSpeechDraft()
    }
    if (
      activeKatexDraftDirty.value &&
      activeSlide.value?.id &&
      Number(activeSlide.value.id) !== Number(slideId)
    ) {
      saveActiveKatexDraft()
    }
    const index = findIndexById(slideId)
    if (index !== -1) {
      fullscreenIndex.value = index
      fullscreenEditorTab.value = 'speech'
      syncSpeechDraftFromActiveSlide({ force: true })
      syncKatexDraftFromActiveSlide({ force: true })
    }
  }
)

watch(
  () => [
    activeSlide.value?.id,
    activeSlide.value?.voice_script,
    activeSlide.value?.title,
    activeSlide.value?.screen_text,
    activeSlide.value?.katex,
  ],
  () => {
    syncSpeechDraftFromActiveSlide()
    syncKatexDraftFromActiveSlide()
  },
  { immediate: true }
)

watch(
  () => slidesForRender.value.length,
  (length) => {
    if (!length) {
      closeFullscreen()
      fullscreenIndex.value = 0
      return
    }

    if (fullscreenIndex.value > length - 1) {
      fullscreenIndex.value = length - 1
    }
  }
)

watch(isYoutubeFormat, () => {
  applyFormatDefaults()
}, { immediate: true })

watch(isFullscreen, (open) => {
  if (typeof window === 'undefined' || typeof document === 'undefined') return

  if (open) {
    previousBodyOverflow.value = document.body.style.overflow || ''
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', handleKeydown)
    return
  }

  document.body.style.overflow = previousBodyOverflow.value
  window.removeEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  flushYoutubeInlinePatch()
  stopFullPreview()

  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', handleKeydown)
  }

  if (typeof document !== 'undefined') {
    document.body.style.overflow = previousBodyOverflow.value
  }
})
</script>

<style scoped>
.reel-preview-panel {
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  background: #f8fbff;
  padding: 16px;
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 12px;
}

.preview-header-right {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.math-size-controls,
.preview-gap-controls {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #ffffff;
  padding: 4px;
}

.preview-gap-controls {
  margin-right: 16px;
}

.preview-gap-label {
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  padding: 0 2px;
}

.size-button,
.size-reset {
  border: 0;
  border-radius: 6px;
  background: #eff6ff;
  color: #1e40af;
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
  padding: 7px 8px;
  cursor: pointer;
}

.size-button:hover,
.size-reset:hover {
  background: #dbeafe;
}

.line-mode-button {
  min-width: 104px;
}

.line-mode-button--active {
  background: #1d4ed8;
  color: #ffffff;
}

.line-mode-button--active:hover {
  background: #1e40af;
}

.line-mode-button:disabled {
  background: #e2e8f0;
  color: #64748b;
  cursor: not-allowed;
}

.subtitles-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid #cbd5f5;
  border-radius: 8px;
  background: #f8fafc;
  color: #1e293b;
  font-size: 12px;
  font-weight: 700;
  padding: 7px 10px;
  cursor: pointer;
  transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}

.subtitles-toggle:hover {
  background: #eef2ff;
  border-color: #93c5fd;
}

.subtitles-toggle--active {
  background: #1d4ed8;
  border-color: #1d4ed8;
  color: #ffffff;
}

.subtitles-toggle--active:hover {
  background: #1e40af;
  border-color: #1e40af;
  color: #ffffff;
}

.subtitles-toggle-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.subtitles-toggle-label {
  white-space: nowrap;
}

.subtitles-toggle--inline {
  width: 100%;
  justify-content: center;
}

.size-value {
  min-width: 38px;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  text-align: center;
}

.btn-fullscreen {
  border: 0;
  border-radius: 8px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 12px;
  font-weight: 700;
  padding: 8px 12px;
  cursor: pointer;
}

.btn-fullscreen:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.btn-png-export {
  background: #0f766e;
}

.btn-png-export:hover:not(:disabled) {
  background: #115e59;
}

.btn-video-export {
  background: #7c3aed;
}

.btn-video-export:hover:not(:disabled) {
  background: #6d28d9;
}

.preview-count {
  margin-left: 8px;
  font-size: 12px;
  font-weight: 700;
  color: #1d4ed8;
  background: #dbeafe;
  border-radius: 999px;
  padding: 4px 10px;
}

.preview-count--duration::before {
  content: '⏱ ';
}

.empty-state {
  margin: 0;
  color: #1e3a8a;
  font-size: 14px;
}

.reel-preview-list {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.fullscreen-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.78);
  backdrop-filter: blur(2px);
  z-index: 26000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 72px 20px 20px;
}

.fullscreen-preview-controls {
  position: absolute;
  top: 18px;
  left: 50%;
  z-index: 2;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.full-preview-button {
  min-width: 176px;
  border: 1px solid rgba(191, 219, 254, 0.82);
  border-radius: 999px;
  background: #ffffff;
  color: #1d4ed8;
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.24);
  font-size: 14px;
  font-weight: 900;
  line-height: 1;
  padding: 13px 18px;
  cursor: pointer;
}

.full-preview-button:hover:not(:disabled) {
  background: #eff6ff;
}

.full-preview-button--playing {
  background: #1d4ed8;
  color: #ffffff;
  border-color: rgba(147, 197, 253, 0.9);
}

.full-preview-button--playing:hover:not(:disabled) {
  background: #1e40af;
}

.full-preview-button:disabled {
  background: #e2e8f0;
  color: #64748b;
  cursor: not-allowed;
  box-shadow: none;
}

.fullscreen-content {
  width: min(1500px, 100%);
  max-height: calc(100dvh - 92px);
  display: grid;
  grid-template-columns: minmax(230px, 310px) minmax(0, auto) minmax(230px, 300px);
  gap: 20px;
  align-items: center;
  justify-content: center;
}

.fullscreen-backdrop--youtube {
  padding-inline: clamp(12px, 2vw, 24px);
  background: rgba(15, 23, 42, 0.72);
  backdrop-filter: none;
}

.fullscreen-content--youtube {
  width: min(1760px, calc(100dvw - 40px));
  grid-template-columns: minmax(220px, 280px) minmax(0, 1fr) minmax(220px, 280px);
  gap: clamp(10px, 1.1vw, 16px);
}

.fullscreen-speech-panel {
  grid-column: 1;
  grid-row: 1;
  width: 100%;
  max-height: calc(100dvh - 108px);
  border: 1px solid rgba(191, 219, 254, 0.72);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.96);
  padding: 12px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.22);
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

.speech-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.speech-panel-header h4 {
  margin: 0;
  color: #0f172a;
  font-size: 15px;
}

.speech-tabs {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  background: #eff6ff;
  padding: 3px;
}

.speech-tab {
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: #1e3a8a;
  font-family: inherit;
  font-size: 12px;
  font-weight: 900;
  line-height: 1;
  padding: 7px 10px;
  cursor: pointer;
}

.speech-tab--active {
  background: #1d4ed8;
  color: #ffffff;
}

.speech-tab:hover:not(.speech-tab--active) {
  background: #dbeafe;
}

.speech-panel-header span {
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 8px;
}

.speech-script {
  width: 100%;
  min-height: 132px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  color: #0f172a;
  font: inherit;
  font-size: 13px;
  line-height: 1.45;
  padding: 10px;
  resize: vertical;
}

.speech-script--dirty {
  border-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.16);
}

.speech-player {
  width: 100%;
}

.speech-empty {
  margin: 0;
  border: 1px dashed #bfdbfe;
  border-radius: 8px;
  background: #eff6ff;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.4;
  padding: 10px;
}

.katex-color-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.katex-color-label {
  color: #475569;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-right: 2px;
}

.katex-color-btn {
  width: 26px;
  height: 26px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
  transition: transform 0.1s, box-shadow 0.1s;
}

.katex-color-btn:hover {
  transform: scale(1.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

.speech-action-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.speech-save-button,
.speech-generate-button {
  border: 0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 800;
  padding: 10px 12px;
  cursor: pointer;
}

.speech-save-button {
  background: #dcfce7;
  color: #166534;
}

.speech-save-button:hover:not(:disabled) {
  background: #bbf7d0;
}

.speech-generate-button {
  background: #1d4ed8;
  color: #ffffff;
}

.speech-generate-button:hover:not(:disabled) {
  background: #1e40af;
}

.speech-save-button:disabled,
.speech-generate-button:disabled {
  background: #94a3b8;
  color: #ffffff;
  cursor: not-allowed;
}

.speech-side-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 2px;
}

.speech-side-control {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  flex-wrap: wrap;
}

.speech-side-control-label {
  flex: 0 0 86px;
  padding: 0;
}

.speech-side-control .line-mode-button {
  flex: 1 1 150px;
}

.speech-side-control .subtitles-toggle--inline {
  width: auto;
}

.fullscreen-toolbar {
  grid-column: 3;
  grid-row: 1;
  width: 100%;
  max-height: calc(100dvh - 108px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  overflow-y: auto;
  padding-right: 2px;
}

.fullscreen-control-group {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  flex-wrap: wrap;
  border: 1px solid rgba(191, 219, 254, 0.72);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.96);
  padding: 8px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.22);
}

.control-label {
  flex: 1 0 100%;
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  padding: 0 2px;
}

.inline-layout-row {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  flex-wrap: nowrap;
}

.inline-layout-row--offset {
  padding-top: 2px;
}

.inline-offset-button {
  min-width: 34px;
}

.inline-separator-button {
  min-width: 34px;
}

.inline-separator-button--none {
  min-width: 44px;
}

.inline-offset-value {
  min-width: 48px;
  text-align: center;
}

.cumulative-gap-button {
  min-width: 34px;
}

.cumulative-gap-value {
  min-width: 52px;
  text-align: center;
}

.fullscreen-stage {
  grid-column: 2;
  grid-row: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  justify-items: center;
  gap: 14px;
}

.fullscreen-content--youtube .fullscreen-stage {
  width: 100%;
  min-width: 0;
  position: relative;
  grid-template-columns: minmax(0, 1fr);
  gap: 0;
}

.fullscreen-content--youtube :deep(.slide-card--youtube.slide-card--fullscreen) {
  width: min(100%, calc((100dvh - 180px) * 16 / 9));
  min-width: 0;
}

.fullscreen-content--youtube .nav-arrow {
  position: absolute;
  top: 50%;
  z-index: 8;
  width: 44px;
  height: 44px;
  font-size: 30px;
  transform: translateY(-50%);
}

.fullscreen-content--youtube .nav-arrow:first-child {
  left: clamp(8px, 1vw, 14px);
}

.fullscreen-content--youtube .nav-arrow:last-child {
  right: clamp(8px, 1vw, 14px);
}

.nav-arrow {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  border: 1px solid rgba(59, 130, 246, 0.5);
  background: rgba(29, 78, 216, 0.38);
  color: #eff6ff;
  font-size: 36px;
  line-height: 1;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.nav-arrow:hover {
  background: rgba(37, 99, 235, 0.58);
}

.png-export-area {
  position: fixed;
  top: 0;
  left: -12000px;
  width: var(--export-width, 1080px);
  pointer-events: none;
  visibility: visible;
  z-index: 0;
}

.png-export-frame {
  width: var(--export-width, 1080px);
  height: var(--export-height, 1920px);
  overflow: hidden;
  background: #f8fbff;
}

.png-export-frame :deep(.slide-card) {
  width: var(--export-width, 1080px) !important;
  min-width: var(--export-width, 1080px) !important;
  max-width: var(--export-width, 1080px) !important;
  height: var(--export-height, 1920px) !important;
  padding: 0 !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}

.png-export-frame :deep(.reel-slide) {
  width: var(--export-width, 1080px) !important;
  height: var(--export-height, 1920px) !important;
  aspect-ratio: auto !important;
  border: 0 !important;
  border-radius: 0 !important;
}

@media (max-width: 980px) {
  .fullscreen-content {
    width: 100%;
    max-height: calc(100dvh - 92px);
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .fullscreen-toolbar {
    grid-column: 1;
    grid-row: 3;
    justify-self: center;
    width: min(640px, 100%);
    max-height: 28dvh;
    align-items: stretch;
  }

  .fullscreen-speech-panel {
    grid-column: 1;
    grid-row: 2;
    justify-self: center;
    width: min(640px, 100%);
    max-height: 28dvh;
  }

  .fullscreen-control-group {
    max-width: 100%;
    overflow-x: auto;
  }

  .fullscreen-stage {
    grid-column: 1;
    grid-row: 1;
    gap: 8px;
  }
}

@media (max-width: 680px) {
  .preview-header {
    align-items: center;
  }

  .preview-header-right {
    justify-content: center;
    flex-wrap: wrap;
  }

  .fullscreen-backdrop {
    padding: 64px 10px 10px;
  }

  .fullscreen-content {
    max-height: calc(100dvh - 74px);
  }

  .fullscreen-preview-controls {
    top: 12px;
    width: calc(100% - 20px);
  }

  .full-preview-button {
    width: min(260px, 100%);
    min-width: 0;
    font-size: 13px;
    padding: 12px 16px;
  }

  .fullscreen-toolbar {
    width: 100%;
  }

  .nav-arrow {
    width: 44px;
    height: 44px;
    font-size: 28px;
  }

  .fullscreen-stage {
    gap: 8px;
  }
}

/* ── Annotation panel ── */

.ann-group {
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
}

.ann-tools {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.ann-tool-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #eff6ff;
  color: #1e40af;
  font-size: 11px;
  line-height: 1;
  padding: 8px 4px;
  cursor: pointer;
  text-align: center;
  transition: background 0.12s, border-color 0.12s, transform 0.1s;
}

.ann-tool-btn:hover {
  background: #dbeafe;
  border-color: #93c5fd;
}

.ann-tool-btn:active {
  transform: scale(0.97);
}

.ann-tool-btn--active {
  background: #1d4ed8;
  border-color: #1d4ed8;
  color: #ffffff;
  box-shadow: 0 4px 10px rgba(29, 78, 216, 0.32);
}

.ann-tool-btn--active:hover {
  background: #1e40af;
}

.ann-tool-icon {
  width: 18px;
  height: 18px;
  display: block;
}

.ann-tool-label {
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.02em;
}

.ann-help {
  margin: 0;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
  font-size: 10.5px;
  font-weight: 600;
  line-height: 1.35;
  padding: 6px 8px;
}

.ann-colors {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ann-color-btn {
  width: 24px;
  height: 24px;
  border: 2px solid transparent;
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.1s, border-color 0.1s;
}

.ann-color-btn:hover {
  transform: scale(1.18);
}

.ann-color-btn--active {
  border-color: #ffffff;
  box-shadow: 0 0 0 2px #1d4ed8;
  transform: scale(1.12);
}

.ann-stroke {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ann-stroke-label {
  color: #475569;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-right: 2px;
}

.ann-stroke-value {
  min-width: 32px;
  text-align: center;
}

.ann-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ann-action-btn {
  border: 0;
  border-radius: 8px;
  background: #fef3c7;
  color: #92400e;
  font-size: 12px;
  font-weight: 800;
  padding: 8px 10px;
  cursor: pointer;
  text-align: center;
  transition: background 0.12s;
}

.ann-action-btn:hover:not(:disabled) {
  background: #fde68a;
}

.ann-action-btn--danger {
  background: #fee2e2;
  color: #991b1b;
}

.ann-action-btn--danger:hover:not(:disabled) {
  background: #fecaca;
}

.ann-action-btn:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}

/* ── Pronunciation editor ── */

.pronunciation-section {
  border: 1px solid #bfdbfe;
  border-radius: 10px;
  background: #f8fbff;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pronunciation-header {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.pronunciation-title {
  color: #1e3a8a;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pronunciation-hint {
  color: #475569;
  font-size: 11px;
  font-weight: 600;
}

.pronunciation-text {
  display: block;
  line-height: 1.55;
  color: #0f172a;
  font-size: 13px;
  word-wrap: break-word;
}

.pronunciation-word {
  display: inline;
  border: 0;
  background: transparent;
  color: inherit;
  font: inherit;
  padding: 1px 2px;
  margin: 0;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.12s, color 0.12s;
  border-bottom: 1px dashed transparent;
}

.pronunciation-word:hover {
  background: #dbeafe;
  border-bottom-color: #3b82f6;
}

.pronunciation-word--has-override {
  background: #fef3c7;
  color: #92400e;
  font-weight: 700;
  border-bottom: 1px solid #f59e0b;
}

.pronunciation-word--has-override:hover {
  background: #fde68a;
}

.pronunciation-sep {
  white-space: pre-wrap;
}

.pronunciation-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  border-top: 1px dashed #cbd5e1;
  padding-top: 8px;
}

.pronunciation-list-label {
  color: #475569;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-right: 2px;
}

.pronunciation-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: 1px solid #fcd34d;
  border-radius: 999px;
  background: #fef3c7;
  color: #92400e;
  font-size: 11px;
  padding: 3px 8px;
}

.pronunciation-chip--foreign {
  border-color: #93c5fd;
  background: #dbeafe;
  color: #1e3a8a;
}

.pronunciation-chip-lang {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.7);
  color: inherit;
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.05em;
  padding: 1px 4px;
}

.pronunciation-chip--foreign .pronunciation-chip-lang {
  background: #1d4ed8;
  color: #ffffff;
}

.pronunciation-chip strong {
  font-weight: 800;
}

.pronunciation-chip-arrow {
  opacity: 0.6;
}

.pronunciation-chip em {
  font-style: italic;
}

.pronunciation-modal-select {
  appearance: auto;
  padding: 8px 10px;
}

.pronunciation-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(2px);
  z-index: 27000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.pronunciation-modal {
  width: min(420px, 100%);
  background: #ffffff;
  border-radius: 14px;
  border: 1px solid #bfdbfe;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.4);
  padding: 18px 18px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pronunciation-modal-title {
  margin: 0;
  color: #1e3a8a;
  font-size: 16px;
  font-weight: 900;
}

.pronunciation-modal-word {
  margin: 0;
  color: #0f172a;
  font-size: 13px;
}

.pronunciation-modal-word strong {
  color: #1d4ed8;
}

.pronunciation-modal-label {
  color: #475569;
  font-size: 12px;
  font-weight: 700;
}

.pronunciation-modal-input {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 9px 10px;
  font: inherit;
  font-size: 14px;
  color: #0f172a;
  background: #ffffff;
}

.pronunciation-modal-input:focus {
  outline: none;
  border-color: #1d4ed8;
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.18);
}

.pronunciation-modal-hint {
  margin: 0;
  color: #64748b;
  font-size: 11px;
  line-height: 1.4;
}

.pronunciation-modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 4px;
}

.pronunciation-modal-btn {
  border: 0;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 800;
  padding: 8px 12px;
  cursor: pointer;
}

.pronunciation-modal-btn--cancel {
  background: #e2e8f0;
  color: #1e293b;
}

.pronunciation-modal-btn--cancel:hover {
  background: #cbd5e1;
}

.pronunciation-modal-btn--remove {
  background: #fee2e2;
  color: #991b1b;
  margin-right: auto;
}

.pronunciation-modal-btn--remove:hover:not(:disabled) {
  background: #fecaca;
}

.pronunciation-modal-btn--remove:disabled {
  background: #f1f5f9;
  color: #94a3b8;
  cursor: not-allowed;
}

.pronunciation-modal-btn--save {
  background: #1d4ed8;
  color: #ffffff;
}

.pronunciation-modal-btn--save:hover {
  background: #1e40af;
}

/* ── Voice overrides panel ── */

.voice-overrides-panel {
  margin-top: 8px;
  border-top: 1px solid #e2e8f0;
  padding-top: 8px;
}

.voice-overrides-toggle {
  all: unset;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 2px 0;
  user-select: none;
}

.voice-overrides-toggle:hover {
  color: #1d4ed8;
}

.voice-overrides-arrow {
  font-size: 14px;
  line-height: 1;
  transition: transform 0.15s ease;
  display: inline-block;
}

.voice-overrides-arrow.is-open {
  transform: rotate(90deg);
}

.voice-overrides-body {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.voice-overrides-group {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.voice-overrides-group--active {
  border-color: #93c5fd;
}

.voice-overrides-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 8px;
  background: #f1f5f9;
  gap: 6px;
}

.voice-overrides-group--active .voice-overrides-group-header {
  background: #eff6ff;
}

.voice-overrides-name {
  font-size: 11px;
  font-weight: 700;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.voice-overrides-badge {
  background: #2563eb;
  color: #fff;
  font-size: 9px;
  font-weight: 800;
  padding: 1px 5px;
  border-radius: 10px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.voice-overrides-clear {
  all: unset;
  cursor: pointer;
  font-size: 10px;
  font-weight: 700;
  color: #dc2626;
  padding: 2px 6px;
  border-radius: 5px;
  border: 1px solid #fca5a5;
  background: #fff;
  flex-shrink: 0;
}

.voice-overrides-clear:hover {
  background: #fef2f2;
}

.voice-overrides-list {
  display: flex;
  flex-direction: column;
}

.voice-override-item {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  font-size: 11px;
  border-top: 1px solid #f1f5f9;
}

.voice-override-item-lang {
  font-size: 9px;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  background: #e2e8f0;
  padding: 1px 4px;
  border-radius: 4px;
  flex-shrink: 0;
}

.voice-override-item-word {
  color: #1e3a8a;
  font-weight: 700;
}

.voice-override-item-arrow {
  color: #94a3b8;
  flex-shrink: 0;
}

.voice-override-item-pron {
  color: #0f766e;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.voice-override-item-delete {
  all: unset;
  cursor: pointer;
  color: #94a3b8;
  font-size: 14px;
  line-height: 1;
  flex-shrink: 0;
  padding: 0 2px;
  border-radius: 3px;
}

.voice-override-item-delete:hover {
  color: #dc2626;
  background: #fef2f2;
}
</style>
