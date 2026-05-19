<template>
  <main class="reel-studio-admin">
    <FormatHelp
      :format-template="formatHelpTemplate"
      :formats="studioFormat === 'carousel' ? CAROUSEL_FORMATS : []"
      :show-notes="false"
      :initial-show="false"
    />

    <header class="page-header">
      <div>
        <h1>Reel Studio OptiTAB</h1>
      </div>
    </header>

    <p v-if="feedback.text" :class="['feedback', `feedback--${feedback.type}`]">{{ feedback.text }}</p>

    <p v-if="!canManage" class="feedback feedback--error">
      Accès refusé: cette section est réservée aux utilisateurs admin/staff.
    </p>

    <section v-else class="studio-stack">
      <div class="studio-format-tabs">
        <button
          v-for="tab in FORMAT_TABS"
          :key="tab.value"
          class="studio-format-tab"
          :class="{ 'studio-format-tab--active': studioFormat === tab.value }"
          type="button"
          @click="switchFormat(tab.value)"
        >
          {{ tab.label }}
        </button>
      </div>

      <section class="project-panel">
        <div class="section-toolbar">
          <div>
            <h2>{{ studioFormatConfig.managementTitle }}</h2>
            <p>{{ filteredProjects.length }} {{ filteredProjects.length > 1 ? studioFormatConfig.countPlural : studioFormatConfig.countSingular }} enregistre{{ filteredProjects.length > 1 ? 's' : '' }}</p>
          </div>
          <button class="btn-primary" type="button" @click="openCreateProjectForm">
            {{ studioFormatConfig.createButtonLabel }}
          </button>
        </div>

        <ReelProjectForm
          v-if="projectFormOpen"
          :loading="savingProject"
          :initial-values="projectFormInitialValues"
          :submit-label="projectFormSubmitLabel"
          :form-title="projectFormTitle"
          @submit="handleSubmitProject"
          @cancel="closeProjectForm"
        />

      </section>

      <section ref="editorSectionRef" class="content-grid">
        <section class="right-column">
          <p v-if="loadingProjectDetail" class="loading-state">Chargement du projet...</p>

          <template v-else>
            <p v-if="!selectedProject" class="empty-editor-state">
              {{ studioFormatConfig.emptySelectionLabel }}
            </p>

            <ReelTemplateBuilder
              v-model:template-text="templateDraft"
              :loading="generatingTemplate"
              :saving="savingTemplate"
              :disabled="!selectedProject"
              :title="studioFormatConfig.templateBuilderTitle"
              :textarea-label="studioFormatConfig.templateTextareaLabel"
              :placeholder="studioFormatConfig.templatePlaceholder"
              :show-ai-generate="isCarouselProject"
              :ai-loading="generatingCarouselGemini"
              ai-generate-label="Créer les images avec Gemini"
              ai-loading-label="Gemini génère les images..."
              :ai-prompt-fallback="studioFormatConfig.formatTemplate"
              @generate="handleGenerateFromTemplate"
              @save="handleSaveTemplate"
              @ai-generate="handleGenerateCarouselWithGemini"
            />

            <ReelPreview
              :slides="selectedProject?.slides || []"
              :selected-slide-id="selectedSlideId"
              :generating-speech-slide-id="generatingSpeechSlideId"
              :generating-image-slide-id="generatingImageSlideId"
              :exporting-video="exportingVideo"
              :format="selectedProject?.format_type || studioFormat"
              :pronunciation-overrides="selectedProject?.pronunciation_overrides || []"
              :pronunciation-overrides-by-voice="selectedProject?.pronunciation_overrides_by_voice || {}"
              :active-voice-id="selectedVoiceId"
              :voice-list="currentProviderVoices"
              :project="selectedProject || {}"
              @select-slide="selectedSlideId = $event"
              @diagnostic="handleSlideDiagnostic"
              @update-slide="handlePatchSlide"
              @update-project="handlePatchProjectInline"
              @generate-slide-speech="handleGenerateSlideSpeech"
              @export-video="handleExportVideo"
              @update-pronunciation-overrides="handleUpdatePronunciationOverrides"
              @update-pronunciation-overrides-by-voice="handleUpdatePronunciationOverridesByVoice"
              @toggle-carousel-image="handleToggleCarouselImage"
              @generate-slide-image="handleGenerateSlideImage"
              @clear-slide-image="handleClearSlideImage"
            />

            <section v-if="selectedProject" class="instagram-caption-panel">
              <div class="instagram-caption-header">
                <div>
                  <h3>{{ studioFormatConfig.descriptionTitle }}</h3>
                  <p>{{ studioFormatConfig.descriptionHelp }}</p>
                </div>
                <button
                  class="btn-secondary"
                  type="button"
                  :disabled="!instagramCaptionText"
                  @click="copyInstagramCaption"
                >
                  {{ studioFormatConfig.copyDescriptionLabel }}
                </button>
              </div>
              <textarea
                class="instagram-caption-text"
                :value="instagramCaptionText || studioFormatConfig.emptyDescriptionLabel"
                readonly
                rows="10"
                @focus="$event.target.select()"
              ></textarea>
            </section>

            <section v-if="isCarouselProject" class="gemini-panel">
              <div class="gemini-panel-header">
                <label class="gemini-model-select">
                  Modèle Gemini
                  <input
                    v-model="geminiModelSearch"
                    class="gemini-model-search"
                    type="search"
                    placeholder="Rechercher un modèle..."
                    :disabled="loadingGeminiOptions || generatingCarouselGemini"
                  />
                  <select
                    v-model="selectedGeminiModelId"
                    :disabled="loadingGeminiOptions || generatingCarouselGemini"
                  >
                    <option v-if="!filteredGeminiModels.length" disabled value="">
                      Aucun modèle trouvé
                    </option>
                    <option
                      v-for="model in filteredGeminiModels"
                      :key="model.id"
                      :value="model.id"
                    >
                      {{ modelLabel(model) }}
                    </option>
                  </select>
                </label>
                <button
                  class="btn-secondary btn-compact"
                  type="button"
                  :disabled="loadingGeminiOptions || generatingCarouselGemini"
                  @click="loadGeminiOptions"
                >
                  {{ loadingGeminiOptions ? 'Chargement...' : 'Actualiser' }}
                </button>
                <button
                  class="btn-secondary btn-compact"
                  type="button"
                  :disabled="regeneratingCarouselImages || generatingCarouselGemini || !canRegenerateCarouselImages"
                  :title="canRegenerateCarouselImages ? 'Recréer uniquement les images Gemini sans toucher au texte' : 'Génère d abord les slides'"
                  @click="handleRegenerateCarouselImages"
                >
                  {{ regeneratingCarouselImages ? 'Images en cours...' : 'Régénérer images seulement' }}
                </button>
                <button
                  class="btn-secondary btn-compact btn-instructions"
                  type="button"
                  title="Définir des consignes qui s'appliqueront à toutes les prochaines générations d'image"
                  @click="imageInstructionsDialogOpen = true"
                >
                  📝 Mes instructions
                </button>
              </div>

              <div class="gemini-usage-grid">
                <div class="gemini-usage-card">
                  <span>Dépensé ce mois</span>
                  <strong>{{ formatGeminiMoney(geminiUsage.display_spent) }}</strong>
                </div>
                <div class="gemini-usage-card">
                  <span>Reste</span>
                  <strong>{{ geminiRemainingLabel }}</strong>
                </div>
                <div class="gemini-usage-card">
                  <span>Générations</span>
                  <strong>{{ geminiUsage.usage_count || 0 }}</strong>
                </div>
                <div class="gemini-usage-card">
                  <span>Dernier coût</span>
                  <strong>{{ formatGeminiMoney(lastGeminiUsageDisplayCost) }}</strong>
                </div>
              </div>

              <p v-if="geminiOptionsError" class="gemini-error">{{ geminiOptionsError }}</p>
            </section>

            <section v-if="selectedProject && !isCarouselProject" class="speech-panel">
              <div class="speech-panel-header">
                <div>
                  <h3>Voix par slide</h3>
                  <p>{{ speechStatusLabel }}</p>
                </div>

                <div class="voice-charcount" :class="{ 'voice-charcount--warn': speechCharCountWarning }">
                  <strong>{{ speechCharCount.toLocaleString('fr-FR') }}</strong>
                  <span>caracteres a generer</span>
                  <small v-if="speechCharCountWarning">{{ speechCharCountWarning }}</small>
                </div>
              </div>

              <div class="speech-controls">
                <label class="voice-select voice-select--provider">
                  Fournisseur de voix
                  <select
                    v-model="selectedProviderId"
                    :disabled="loadingVoiceOptions || generatingSpeech || generatingSpeechSlideId || testingVoice"
                    @change="onProviderChange"
                  >
                    <option v-if="loadingVoiceOptions && !providers.length" value="">Chargement...</option>
                    <option
                      v-for="provider in providers"
                      :key="provider.id"
                      :value="provider.id"
                      :disabled="!provider.configured"
                    >
                      {{ provider.label }}{{ provider.configured ? '' : ' (non configure)' }}
                    </option>
                  </select>
                  <span v-if="selectedProviderMeta">{{ selectedProviderMeta }}</span>
                </label>

                <div class="voice-select-row">
                  <label class="voice-select voice-select--voice">
                    {{ selectedProviderId === 'elevenlabs' ? 'Voix favoris' : 'Voix' }}
                    <select
                      v-model="selectedVoiceId"
                      :disabled="loadingVoiceOptions || generatingSpeech || generatingSpeechSlideId || testingVoice || !currentProviderVoices.length"
                      @change="onFavoriteVoiceChange"
                    >
                      <option v-if="loadingVoiceOptions" value="">Chargement...</option>
                      <option v-else-if="!currentProviderVoices.length" value="">Aucune voix trouvee</option>
                      <option
                        v-for="voice in currentProviderVoices"
                        :key="voice.voice_id"
                        :value="voice.voice_id"
                        :disabled="voice.api_usable === false"
                      >
                        {{ voiceOptionLabel(voice) }}
                      </option>
                    </select>
                    <span v-if="selectedVoiceMeta">{{ selectedVoiceMeta }}</span>
                    <span v-if="selectedVoiceWarning" class="voice-warning">{{ selectedVoiceWarning }}</span>
                    <span v-else-if="voiceOptionsError">{{ voiceOptionsError }}</span>
                  </label>

                  <label v-if="selectedProviderId === 'elevenlabs'" class="voice-select voice-select--library">
                    Explorer ElevenLabs
                    <input
                      v-model="voiceLibrarySearch"
                      class="voice-library-search"
                      type="search"
                      placeholder="Rechercher un nom..."
                      :disabled="loadingVoiceLibrary || generatingSpeech || generatingSpeechSlideId || testingVoice"
                      @input="scheduleVoiceLibrarySearch"
                      @keydown.enter.prevent="loadElevenLabsVoiceLibrary"
                    />
                    <div class="voice-library-filters">
                      <select
                        v-model="voiceLibraryFilters.gender"
                        :disabled="loadingVoiceLibrary || generatingSpeech || generatingSpeechSlideId || testingVoice"
                        @change="loadElevenLabsVoiceLibrary"
                      >
                        <option
                          v-for="option in ELEVENLABS_LIBRARY_GENDER_OPTIONS"
                          :key="option.value"
                          :value="option.value"
                        >
                          {{ option.label }}
                        </option>
                      </select>
                      <select
                        v-model="voiceLibraryFilters.age"
                        :disabled="loadingVoiceLibrary || generatingSpeech || generatingSpeechSlideId || testingVoice"
                        @change="loadElevenLabsVoiceLibrary"
                      >
                        <option
                          v-for="option in ELEVENLABS_LIBRARY_AGE_OPTIONS"
                          :key="option.value"
                          :value="option.value"
                        >
                          {{ option.label }}
                        </option>
                      </select>
                      <select
                        v-model="voiceLibraryFilters.quality"
                        :disabled="loadingVoiceLibrary || generatingSpeech || generatingSpeechSlideId || testingVoice"
                        @change="loadElevenLabsVoiceLibrary"
                      >
                        <option
                          v-for="option in ELEVENLABS_LIBRARY_QUALITY_OPTIONS"
                          :key="option.value"
                          :value="option.value"
                        >
                          {{ option.label }}
                        </option>
                      </select>
                    </div>
                    <div class="voice-library-picker">
                      <select
                        v-model="selectedLibraryVoiceId"
                        :disabled="loadingVoiceLibrary || generatingSpeech || generatingSpeechSlideId || testingVoice"
                        @change="onLibraryVoiceChange"
                      >
                        <option value="">
                          {{ loadingVoiceLibrary ? 'Chargement...' : 'Voix French / parisian' }}
                        </option>
                        <option
                          v-for="voice in voiceLibraryOptions"
                          :key="voice.voice_id"
                          :value="voice.voice_id"
                        >
                          {{ libraryVoiceOptionLabel(voice) }}
                        </option>
                      </select>
                      <button
                        class="voice-favorite-toggle"
                        type="button"
                        :class="{ 'is-favorite': selectedLibraryVoiceIsFavorite }"
                        :disabled="!selectedLibraryVoice || loadingVoiceLibrary || generatingSpeech || generatingSpeechSlideId || testingVoice"
                        :title="selectedLibraryVoiceIsFavorite ? 'Retirer des favoris' : 'Ajouter aux favoris'"
                        @click="toggleSelectedLibraryVoiceFavorite"
                      >
                        {{ selectedLibraryVoiceIsFavorite ? '★' : '☆' }}
                      </button>
                    </div>
                    <span v-if="voiceLibraryError" class="voice-warning">{{ voiceLibraryError }}</span>
                  </label>
                </div>

                <section v-if="selectedProviderId === 'elevenlabs'" class="voice-advanced">
                  <div class="voice-advanced-header">
                    <button
                      class="voice-advanced-toggle"
                      type="button"
                      :aria-expanded="String(showElevenLabsAdvanced)"
                      @click="showElevenLabsAdvanced = !showElevenLabsAdvanced"
                    >
                      <span class="voice-advanced-arrow" :class="{ 'is-open': showElevenLabsAdvanced }">></span>
                      <span>Options avancees</span>
                    </button>
                    <button
                      v-if="showElevenLabsAdvanced"
                      class="btn-secondary"
                      type="button"
                      @click="resetElevenLabsSettings"
                    >
                      Reset
                    </button>
                  </div>

                  <div v-if="showElevenLabsAdvanced" class="voice-advanced-grid">
                    <label class="voice-advanced-field voice-advanced-field--wide">
                      Model
                      <select v-model="elevenLabsSettings.model_id">
                        <option
                          v-for="model in ELEVENLABS_MODEL_OPTIONS"
                          :key="model.value"
                          :value="model.value"
                        >
                          {{ model.label }}
                        </option>
                      </select>
                    </label>

                    <label class="voice-advanced-field">
                      Stability
                      <input v-model.number="elevenLabsSettings.stability" type="number" min="0" max="1" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Similarity boost
                      <input v-model.number="elevenLabsSettings.similarity_boost" type="number" min="0" max="1" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Style
                      <input v-model.number="elevenLabsSettings.style" type="number" min="0" max="1" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Speed
                      <input v-model.number="elevenLabsSettings.speed" type="number" min="0.5" max="2" step="0.01" />
                    </label>

                    <label class="voice-advanced-field">
                      Language code
                      <input v-model.trim="elevenLabsSettings.language_code" type="text" maxlength="16" />
                    </label>

                    <label class="voice-advanced-field">
                      Text normalization
                      <select v-model="elevenLabsSettings.apply_text_normalization">
                        <option value="on">on</option>
                        <option value="auto">auto</option>
                        <option value="off">off</option>
                      </select>
                    </label>

                    <label class="voice-toggle">
                      <input v-model="elevenLabsSettings.use_speaker_boost" type="checkbox" />
                      <span>Use speaker boost</span>
                    </label>
                  </div>
                </section>

                <section v-if="selectedProviderId === 'google'" class="voice-advanced">
                  <div class="voice-advanced-header">
                    <button
                      class="voice-advanced-toggle"
                      type="button"
                      :aria-expanded="String(showGoogleAdvanced)"
                      @click="showGoogleAdvanced = !showGoogleAdvanced"
                    >
                      <span class="voice-advanced-arrow" :class="{ 'is-open': showGoogleAdvanced }">></span>
                      <span>Options avancees</span>
                    </button>
                    <button
                      v-if="showGoogleAdvanced"
                      class="btn-secondary"
                      type="button"
                      @click="resetGoogleTtsSettings"
                    >
                      Reset
                    </button>
                  </div>

                  <div v-if="showGoogleAdvanced" class="voice-advanced-grid">
                    <label class="voice-advanced-field">
                      Vitesse
                      <input v-model.number="googleTtsSettings.speaking_rate" type="number" min="0.25" max="4" step="0.05" />
                    </label>

                    <label class="voice-advanced-field">
                      Pitch
                      <input v-model.number="googleTtsSettings.pitch" type="number" min="-20" max="20" step="0.5" />
                    </label>

                    <label class="voice-advanced-field">
                      Volume dB
                      <input v-model.number="googleTtsSettings.volume_gain_db" type="number" min="-96" max="16" step="0.5" />
                    </label>

                    <label class="voice-advanced-field voice-advanced-field--wide">
                      Profil audio
                      <select v-model="googleTtsSettings.effects_profile_id">
                        <option
                          v-for="profile in GOOGLE_EFFECTS_PROFILE_OPTIONS"
                          :key="profile.value"
                          :value="profile.value"
                        >
                          {{ profile.label }}
                        </option>
                      </select>
                    </label>
                  </div>
                </section>

                <div
                  v-if="selectedProviderId === 'elevenlabs'"
                  class="voice-usage"
                  :class="{ 'voice-usage--error': !elevenLabsUsageAvailable }"
                >
                  <div class="voice-usage-header">
                    <strong>Credits ElevenLabs</strong>
                    <span v-if="elevenLabsUsageAvailable">{{ elevenLabsUsagePercentLabel }} utilises</span>
                    <span v-else>Quota indisponible</span>
                  </div>

                  <template v-if="elevenLabsUsageAvailable">
                    <div class="voice-usage-bar" aria-hidden="true">
                      <span :style="elevenLabsUsageBarStyle"></span>
                    </div>
                    <dl class="voice-usage-grid">
                      <div>
                        <dt>Consomme</dt>
                        <dd>{{ elevenLabsUsageConsumedLabel }}</dd>
                      </div>
                      <div>
                        <dt>Total</dt>
                        <dd>{{ elevenLabsUsageTotalLabel }}</dd>
                      </div>
                      <div>
                        <dt>Restant</dt>
                        <dd>{{ elevenLabsUsageRemainingLabel }}</dd>
                      </div>
                      <div>
                        <dt>Pourcentage</dt>
                        <dd>{{ elevenLabsUsagePercentLabel }}</dd>
                      </div>
                    </dl>
                    <p v-if="elevenLabsUsageResetLabel">{{ elevenLabsUsageResetLabel }}</p>
                  </template>

                  <p v-else>{{ elevenLabsUsageErrorLabel }}</p>
                </div>

                <div
                  v-if="selectedProviderId === 'google'"
                  class="voice-usage"
                  :class="{ 'voice-usage--error': !googleUsageAvailable }"
                >
                  <div class="voice-usage-header">
                    <strong>Quota gratuit Google</strong>
                    <span v-if="googleUsageAvailable">{{ googleUsagePercentLabel }} utilisés</span>
                    <span v-else>Quota indisponible</span>
                  </div>

                  <template v-if="googleUsageAvailable">
                    <div class="voice-usage-bar" aria-hidden="true">
                      <span :style="googleUsageBarStyle"></span>
                    </div>
                    <dl class="voice-usage-grid">
                      <div>
                        <dt>Consommé</dt>
                        <dd>{{ googleUsageConsumedLabel }}</dd>
                      </div>
                      <div>
                        <dt>Total free</dt>
                        <dd>{{ googleUsageTotalLabel }}</dd>
                      </div>
                      <div>
                        <dt>Restant</dt>
                        <dd>{{ googleUsageRemainingLabel }}</dd>
                      </div>
                      <div>
                        <dt>Pourcentage</dt>
                        <dd>{{ googleUsagePercentLabel }}</dd>
                      </div>
                    </dl>
                    <p>{{ googleUsageDetailsLabel }}</p>
                  </template>

                  <p v-else>{{ googleUsageErrorLabel }}</p>
                </div>

                <div class="speech-actions">
                  <button
                    class="btn-secondary"
                    type="button"
                    :disabled="testingVoice || loadingVoiceOptions || !selectedVoiceId || !selectedProviderConfigured || !selectedVoiceApiUsable"
                    @click="handleTestVoice"
                    title="Genere un court extrait audio pour preecouter la voix"
                  >
                    {{ testingVoice ? 'Lecture...' : 'Tester la voix' }}
                  </button>

                  <button
                    class="btn-primary"
                    type="button"
                    :disabled="generatingSpeech || loadingVoiceOptions || !canGenerateSpeech || !selectedVoiceCanGenerate || !selectedProviderConfigured"
                    @click="handleGenerateSpeech"
                  >
                    {{ generatingSpeech ? 'Generation des MP3...' : 'Generer les MP3 slides' }}
                  </button>
                </div>
              </div>
              <audio v-if="testAudioUrl" :src="testAudioUrl" controls class="voice-test-audio" />
            </section>

            <section class="manual-editor-wrap">
              <button class="btn-secondary" type="button" @click="showManualEditor = !showManualEditor">
              {{ showManualEditor ? 'Masquer édition manuelle' : 'Afficher édition manuelle' }}
              </button>

              <ReelSlideEditor
                v-if="showManualEditor"
                :slide="selectedSlide"
                :saving="savingSlide"
                :show-voice-fields="!isCarouselProject"
                :show-cumulative-fields="!isCarouselProject"
                @save="handleSaveSlide"
                @delete="handleDeleteSlide"
              />
            </section>
          </template>
        </section>
      </section>

      <section class="project-panel project-panel--list">
        <ReelProjectsList
          :projects="filteredProjects"
          :selected-project-id="selectedProjectId"
          :loading="loadingProjects"
          :title="studioFormatConfig.listTitle"
          :empty-label="studioFormatConfig.emptyListLabel"
          :loading-label="studioFormatConfig.loadingListLabel"
          @select="selectProject"
          @edit="openEditProjectForm"
          @delete="handleDeleteProject"
        />
      </section>
    </section>

    <GeminiImageOptionsDialog
      :open="geminiImageDialogOpen"
      :title="geminiImageDialogMode === 'regenerate' ? 'Régénérer les images Gemini' : 'Générer le carrousel avec Gemini'"
      :subtitle="geminiImageDialogMode === 'regenerate'
        ? 'Choisis le style visuel et les slides à régénérer pour un rendu cohérent et premium.'
        : 'Choisis le style visuel et la portée des images pour un carrousel pro et incitant.'"
      :confirm-label="geminiImageDialogMode === 'regenerate' ? 'Régénérer les images' : 'Générer le carrousel'"
      :total-slides="selectedProject?.slides?.length || 0"
      :initial-carousel-type="lastGeminiCarouselType"
      :initial-strategy="lastGeminiSlideStrategy"
      :initial-use-references="lastGeminiUseReferences"
      @close="closeGeminiImageDialog"
      @confirm="handleGeminiImageDialogConfirm"
    />

    <GeminiImageInstructionsDialog
      :open="imageInstructionsDialogOpen"
      @close="imageInstructionsDialogOpen = false"
    />
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import {
  createReelProject,
  deleteReelProject,
  deleteReelSlide,
  downloadReelVideo,
  exportReelVideo,
  generateCarouselWithGemini,
  regenerateCarouselImages,
  generateReelSlideSpeech,
  generateReelSlideSpeeches,
  generateReelSlideImage,
  clearReelSlideImage,
  generateSlidesFromTemplate,
  getGeminiOptions,
  getReelProject,
  listReelProjects,
  listReelVoiceLibrary,
  listReelVoices,
  saveReelTemplate,
  testReelTTSVoice,
  updateReelProject,
  updateReelSlide,
} from '@/api/reelStudio'
import ReelPreview from '@/components/admin/reel-studio/ReelPreview.vue'
import ReelProjectForm from '@/components/admin/reel-studio/ReelProjectForm.vue'
import ReelProjectsList from '@/components/admin/reel-studio/ReelProjectsList.vue'
import ReelSlideEditor from '@/components/admin/reel-studio/ReelSlideEditor.vue'
import ReelTemplateBuilder from '@/components/admin/reel-studio/ReelTemplateBuilder.vue'
import FormatHelp from '@/components/admin/FormatHelp.vue'
import GeminiImageOptionsDialog from '@/components/admin/reel-studio/GeminiImageOptionsDialog.vue'
import GeminiImageInstructionsDialog from '@/components/admin/reel-studio/GeminiImageInstructionsDialog.vue'

const userStore = useUserStore()
const canManage = computed(() => Boolean(userStore.isAdmin))

const projects = ref([])
const studioFormat = ref('reel')
const selectedProjectId = ref(null)
const selectedProject = ref(null)
const selectedSlideId = ref(null)

const loadingProjects = ref(false)
const loadingProjectDetail = ref(false)
const savingProject = ref(false)
const generatingTemplate = ref(false)
const generatingCarouselGemini = ref(false)
const regeneratingCarouselImages = ref(false)
const generatingImageSlideId = ref(null)
const geminiImageDialogOpen = ref(false)
const geminiImageDialogMode = ref('generate') // 'generate' | 'regenerate'
const pendingGeneratePayload = ref(null)
const lastGeminiCarouselType = ref('marketing')
const lastGeminiSlideStrategy = ref('hook_cta')
const lastGeminiUseReferences = ref(true)
const imageInstructionsDialogOpen = ref(false)
const savingTemplate = ref(false)
const generatingSpeech = ref(false)
const generatingSpeechSlideId = ref(null)
const exportingVideo = ref(false)
const savingSlide = ref(false)
const loadingVoiceOptions = ref(false)
const voiceOptions = ref([])
const selectedVoiceId = ref('')
const voiceOptionsError = ref('')
const loadingVoiceLibrary = ref(false)
const voiceLibraryOptions = ref([])
const selectedLibraryVoiceId = ref('')
const voiceLibraryError = ref('')
const voiceLibrarySearch = ref('')
const voiceLibraryFilters = reactive({
  gender: '',
  age: '',
  quality: '',
})
const providers = ref([])
const selectedProviderId = ref('')
const testingVoice = ref(false)
const testAudioUrl = ref('')
const SPEECH_CHAR_WARNING_THRESHOLD = 4000
const SPEECH_CHAR_HARD_LIMIT = 4500
const showManualEditor = ref(false)
const showElevenLabsAdvanced = ref(false)
const showGoogleAdvanced = ref(false)
const projectFormOpen = ref(false)
const editingProject = ref(null)
const templateDraft = ref('')
const editorSectionRef = ref(null)
const DEFAULT_GEMINI_MODEL_ID = 'gemini-2.5-flash'
const selectedGeminiModelId = ref(DEFAULT_GEMINI_MODEL_ID)
const geminiModelSearch = ref('')
const geminiModels = ref([{ id: DEFAULT_GEMINI_MODEL_ID, display_name: 'Gemini 2.5 Flash' }])
const geminiUsage = ref({
  spent_usd: 0,
  budget_usd: null,
  remaining_usd: null,
  display_currency: 'EUR',
  display_spent: 0,
  display_budget: 10,
  display_remaining: 10,
  eur_per_usd: 0.92,
  usage_count: 0,
})
const lastGeminiUsage = ref(null)
const loadingGeminiOptions = ref(false)
const geminiOptionsError = ref('')

const FORMAT_TABS = Object.freeze([
  { value: 'reel', label: 'Reel' },
  { value: 'carousel', label: 'Carrousel' },
  { value: 'youtube', label: 'YouTube' },
])

function normalizeFormatType(value) {
  return String(value || '').trim().toLowerCase()
}

const filteredProjects = computed(() => {
  return projects.value.filter((p) => {
    const fmt = normalizeFormatType(p.format_type)
    if (studioFormat.value === 'reel') {
      return !fmt || fmt === 'reel'
    }
    if (studioFormat.value === 'carousel') return fmt === 'carousel'
    if (studioFormat.value === 'youtube') return fmt === 'youtube'
    return !fmt || fmt === 'reel'
  })
})

function switchFormat(fmt) {
  if (studioFormat.value === fmt) return
  studioFormat.value = fmt
  selectedProject.value = null
  selectedProjectId.value = null
  selectedSlideId.value = null
  templateDraft.value = ''
  projectFormOpen.value = false
  editingProject.value = null
}
const ELEVENLABS_SETTINGS_STORAGE_KEY = 'reelStudio.elevenLabsSettings.v1'
const GOOGLE_TTS_SETTINGS_STORAGE_KEY = 'reelStudio.googleTtsSettings.v1'
const ELEVENLABS_FAVORITE_VOICES_STORAGE_KEY = 'reelStudio.elevenLabsFavoriteVoices.v1'
const ELEVENLABS_HIDDEN_FAVORITE_IDS_STORAGE_KEY = 'reelStudio.elevenLabsHiddenFavoriteIds.v1'
const ELEVENLABS_MODEL_OPTIONS = [
  { value: 'eleven_multilingual_v3', label: 'eleven_multilingual_v3' },
  { value: 'eleven_multilingual_v2', label: 'eleven_multilingual_v2' },
]
const ELEVENLABS_LIBRARY_DEFAULT_FILTERS = Object.freeze({
  language: 'fr',
  accent: 'parisian',
  page_size: 80,
})
const ELEVENLABS_LIBRARY_GENDER_OPTIONS = Object.freeze([
  { value: '', label: 'Genre: tous' },
  { value: 'male', label: 'Homme' },
  { value: 'female', label: 'Femme' },
  { value: 'neutral', label: 'Neutre' },
])
const ELEVENLABS_LIBRARY_AGE_OPTIONS = Object.freeze([
  { value: '', label: 'Age: tous' },
  { value: 'young', label: 'Jeune' },
  { value: 'middle_aged', label: 'Adulte' },
  { value: 'old', label: 'Senior' },
])
const ELEVENLABS_LIBRARY_QUALITY_OPTIONS = Object.freeze([
  { value: '', label: 'Qualite: toutes' },
  { value: 'high_quality', label: 'High quality' },
  { value: 'featured', label: 'Selection ElevenLabs' },
])
const ELEVENLABS_LIBRARY_SEARCH_DEBOUNCE_MS = 350
const ELEVENLABS_DEFAULT_FAVORITE_VOICE_IDS = Object.freeze([
  '6FXyooAOTqUK8m2HWm32',
  'aQROLel5sQbj1vuIVi6B',
  'WQKwBV2Uzw1gSGr69N8I',
])
const DEFAULT_ELEVENLABS_SETTINGS = Object.freeze({
  model_id: 'eleven_multilingual_v3',
  stability: 0.64,
  similarity_boost: 0.84,
  style: 0.10,
  speed: 1,
  use_speaker_boost: true,
  language_code: 'fr',
  apply_text_normalization: 'on',
})
const GOOGLE_EFFECTS_PROFILE_OPTIONS = Object.freeze([
  { value: '', label: 'Aucun profil' },
  { value: 'headphone-class-device', label: 'Casque / ecouteurs' },
  { value: 'handset-class-device', label: 'Smartphone' },
  { value: 'small-bluetooth-speaker-class-device', label: 'Petite enceinte' },
  { value: 'medium-bluetooth-speaker-class-device', label: 'Enceinte moyenne' },
  { value: 'large-home-entertainment-class-device', label: 'TV / home cinema' },
  { value: 'large-automotive-class-device', label: 'Voiture' },
  { value: 'telephony-class-application', label: 'Telephone' },
  { value: 'wearable-class-device', label: 'Montre / wearable' },
])
const DEFAULT_GOOGLE_TTS_SETTINGS = Object.freeze({
  speaking_rate: 1,
  pitch: 0,
  volume_gain_db: 0,
  effects_profile_id: '',
})
const elevenLabsSettings = reactive(loadStoredElevenLabsSettings())
const googleTtsSettings = reactive(loadStoredGoogleTtsSettings())
const elevenLabsFavoriteVoices = ref(loadStoredElevenLabsFavoriteVoices())
const elevenLabsHiddenFavoriteVoiceIds = ref(loadStoredElevenLabsHiddenFavoriteVoiceIds())

const feedback = reactive({
  type: 'info',
  text: '',
})

const diagnosticsBySlideId = reactive({})
let detailRequestId = 0
let voiceLibrarySearchTimer = 0
let voiceLibraryRequestId = 0
const REEL_FORMAT_TEMPLATE = `FORMAT REEL STUDIO (PRO) - GÉNÉRATION COMPLÈTE

Objectif:
- Écrire toutes les slides d'un coup
- Chaque bloc = 1 slide claire et identifiable
- L'ordre SLIDE 1, 2, 3... détermine la timeline finale
- Tu n'es pas obligé d'avoir 6 slides
- Si une formule dépasse, ne fais pas une ligne horizontale
- Coupe-la en plusieurs lignes KATEX courtes

Structure:
SLIDE <numéro> | <type>
TITLE: ...
TEXT: ...
KATEX: ...
VOICE: ...
---

Voix ElevenLabs (eleven_multilingual_v3):
- Chaque slide doit avoir son VOICE: pour generer son MP3 independant.
- Ajoute les indications de jeu directement dans VOICE avec des tags entre crochets.
- Les tags ne s'affichent pas dans le reel: ils servent seulement a guider la voix.
- Format recommande: VOICE: [thoughtful] On cherche d'abord la bonne identite.
- Mets le tag juste avant le passage concerne, ou juste apres une phrase s'il sert de reaction.
- N'en mets pas trop: 1 a 2 tags par slide suffisent souvent.
- Utilise aussi la ponctuation: ... pour une pause/hesitation, ? pour une intonation interrogative, MAJUSCULES pour insister.

Tags utiles selon ElevenLabs:
- Emotions/direction: [thoughtful], [curious], [excited], [happy], [sad], [angry], [surprised], [annoyed], [appalled], [sarcastic], [mischievously], [crying]
- Livraison: [whispers], [shouts], [dramatically], [warmly], [calm]
- Reactions: [laughs], [laughing], [chuckles], [sighs], [exhales], [clears throat], [inhales deeply], [exhales sharply]
- Pauses: [short pause], [long pause]
- A eviter pour OptiTAB: tags visuels ou non vocaux comme [standing], [grinning], [music].
- Si un tag ne marche pas, teste une variante ou change de voix: ElevenLabs precise que l'effet depend beaucoup de la voix choisie.
- Pour plus d'expressivite, garde ELEVENLABS_MODEL_ID=eleven_multilingual_v3 et une stabilite proche Creative/Natural; Robust rend les tags moins reactifs.

Hook recommandé:
- La slide hook doit contenir une phrase courte + le défi mathématique + une question.
- Utilise TITLE pour la phrase d'accroche, KATEX pour le défi, TEXT pour la question.
- Exemple visuel attendu: "Défi express" + formule au centre + "Tu trouves combien ?"

Correction recommandée:
- La slide 2 doit commencer par TEXT: Correction :
- Ensuite, mets les lignes KATEX de résolution.
- Toutes les slides de calcul suivantes doivent continuer la même correction.
- La slide result, juste avant la CTA, doit être cumulative: elle reprend les lignes de calcul précédentes et ajoute la conclusion finale. Elle ne doit jamais afficher seulement la formule finale.
- Le mot "Correction :" n'est pas ajouté automatiquement: il faut l'écrire explicitement dans TEXT.
- Si la correction devient trop pleine, coche "Nouvelle page" sur une slide: le cumul repart de cette slide en gardant le texte de correction.

CTA recommandé:
- La slide cta doit contenir le résultat final et l'appel à l'action.
- Utilise TITLE pour "Résultat", KATEX pour la formule finale, TEXT pour l'appel à l'action.
- En CTA: titre et texte alignés à gauche, seule la formule est centrée.
- TEXT recommandé sur 3 lignes:
  Abonne-toi à OptiTAB
  Sauvegarde ce Reel
  Commente ton résultat

Description Instagram obligatoire:
- Apres les slides, ajoute un bloc INSTAGRAM_DESCRIPTION copiable.
- Objectif: description Instagram SEO avec style Semji/semantic SEO.
- Commence par une accroche courte avec emoji + mot-cle principal.
- Explique l'exercice en 2 a 4 phrases naturelles avec les mots-cles maths importants.
- Ajoute 3 a 5 benefices/lignes "Dans ce reel".
- Ajoute les appels a l'action: commentaire, sauvegarde, partage, abonnement.
- Termine par exactement 5 hashtags pertinents, pas plus.
- Format obligatoire:
INSTAGRAM_DESCRIPTION:
...
END_INSTAGRAM_DESCRIPTION

Types autorisés:
- hook
- katex
- cumulative_katex
- result
- cta

Mode Auto (IA décide le nombre de slides):
TITLE: Simplification de racines
HOOK: Défi express
KATEX: A=\\frac{\\sqrt{72}+\\sqrt{32}}{\\sqrt{2}}
TEXT: Tu trouves combien ?
KATEX: \\sqrt{72}=6\\sqrt{2}
KATEX: \\sqrt{32}=4\\sqrt{2}
KATEX: A=\\frac{6\\sqrt{2}+4\\sqrt{2}}{\\sqrt{2}}
KATEX: A=10
CTA: Abonne-toi à OptiTAB | Sauvegarde ce Reel | Commente ton résultat

Exemple prêt à copier:
SLIDE 1 | hook
TITLE: Défi express
KATEX: A=\\frac{\\sqrt{72}+\\sqrt{32}}{\\sqrt{2}}
TEXT: Tu trouves combien ?
VOICE: [curious] Défi express... simplifie cette expression.
---
SLIDE 2 | katex
TITLE: Dérivation produit
TEXT: Correction :
KATEX: f(x)=x\\ln(x)
VOICE: [thoughtful] On part de f de x égale x ln x.
---
SLIDE 3 | cumulative_katex
KATEX: u=x \\qquad v=\\ln(x)
VOICE: On reconnaît un produit.
---
SLIDE 4 | cumulative_katex
KATEX: u'=1 \\qquad v'=\\frac{1}{x}
VOICE: [calm] On dérive chaque facteur.
---
SLIDE 5 | result
TITLE: Résultat
KATEX: f(x)=x\\ln(x)
KATEX: u=x \\qquad v=\\ln(x)
KATEX: u'=1 \\qquad v'=\\frac{1}{x}
KATEX: f'(x)=u'v+uv'
KATEX: f'(x)=\\ln(x)+1
VOICE: [excited] Résultat final: ln de x plus un.
---
SLIDE 6 | cta
TITLE: Résultat
KATEX: f'(x)=\\ln(x)+1
TEXT: Abonne-toi à OptiTAB
Sauvegarde ce Reel
Commente ton résultat
VOICE: [warmly] Abonne-toi pour la suite.
---
INSTAGRAM_DESCRIPTION:
🧠 Derivee piegeuse

Essaie de deriver cette fonction avant de regarder la correction :

f(x)=x\\ln(x)

Un exercice classique de terminale pour revoir la derivee d'un produit et les proprietes du logarithme.

Dans ce reel :
✅ derivee d'un produit
✅ derivee de ln(x)
✅ simplification du resultat final

✍️ Donne ta reponse en commentaire
💾 Sauvegarde ce reel pour reviser
📩 Partage-le a un ami
➕ Abonne-toi a OptiTAB pour progresser en maths

#maths #derivation #logarithme #terminale #bac
END_INSTAGRAM_DESCRIPTION
`

const YOUTUBE_FORMAT_TEMPLATE = `FORMAT YOUTUBE STUDIO (PRO) - GÉNÉRATION COMPLÈTE

Objectif:
- Écrire toutes les slides d'une vidéo YouTube en un seul bloc
- Format 16:9 paysage — plus large qu'un reel, plus de contenu par slide possible
- Jusqu'à 6-8 lignes KATEX par slide (vs 3-4 pour un reel)
- Utilise "même ligne" (KATEX sur 2 colonnes) pour montrer étapes en parallèle
- L'ordre SLIDE 1, 2, 3... détermine la timeline finale

Structure (slide standard):
SLIDE <numéro> | <type>
TITLE: ...
TEXT: ...
KATEX: ...
VOICE: ...
---

Structure (slide "méthode à savoir", standalone):
SLIDE <numéro> | <type> | method
TITLE: ...
KATEX: ...
VOICE: ...
---

Structure (slide en split, reprend la méthode déclarée plus haut):
SLIDE <numéro> | <type> | split
VOICE: ...
LEFT:
TEXT: ...
KATEX: ...
RIGHT (repeat)
---

Voix ElevenLabs (eleven_multilingual_v3):
- Chaque slide doit avoir son VOICE: pour générer son MP3 indépendant.
- Ajoute les indications de jeu directement dans VOICE avec des tags entre crochets.
- Les tags ne s'affichent pas dans la vidéo: ils servent seulement à guider la voix.
- Format recommandé: VOICE: [thoughtful] On cherche d'abord la bonne identité.
- Mets le tag juste avant le passage concerné, ou juste après une phrase s'il sert de réaction.
- N'en mets pas trop: 1 à 2 tags par slide suffisent souvent.
- Utilise aussi la ponctuation: ... pour une pause/hésitation, ? pour une intonation interrogative, MAJUSCULES pour insister.

Tags utiles selon ElevenLabs:
- Emotions/direction: [thoughtful], [curious], [excited], [happy], [sad], [surprised], [sarcastic]
- Livraison: [whispers], [shouts], [dramatically], [warmly], [calm]
- Réactions: [laughs], [chuckles], [sighs], [exhales], [clears throat]
- Pauses: [short pause], [long pause]

Hook recommandé:
- La slide hook présente l'exercice ou le cours.
- Utilise TITLE pour le sujet (ex: "Fractions rationnelles"), KATEX pour la question/formule centrale.
- TEXT pour la consigne ou la question posée à l'élève.
- Pas besoin d'être très court: en YouTube tu peux donner plus de contexte.

Correction recommandée:
- La slide 2 doit toujours être l'énoncé, indépendante du cumul: utilise TEXT: Énoncé : et remets la consigne/formule de départ.
- La correction commence seulement à partir de la slide 3 avec TEXT: Correction : (ou "Méthode :", "Démonstration :", selon le contenu).
- Les lignes KATEX de la slide 2 ne doivent pas être reprises dans le cumulative des slides suivantes.
- La slide result est toujours autonome: elle ne reprend ni TEXT: Correction : ni les lignes cumulative_katex précédentes.
- Pour le résultat final, utilise SLIDE N | result avec TITLE: Résultat et uniquement la ou les KATEX du résultat final.
- En YouTube, tu peux mettre plus de lignes KATEX par slide qu'en reel.
- Pour montrer une factorisation et son résultat sur la même slide, utilise KATEX normal + cumulative_katex.
- Si une slide contient un calcul ET son identité remarquable associée: utilise "même ligne" en préfixant avec \\ (dans le template AI, c'est géré automatiquement).

CTA recommandé:
- La slide cta contient le résultat final et l'appel à l'action YouTube.
- Utilise TITLE pour "Résultat", KATEX pour la formule finale, TEXT pour l'appel à l'action.
- TEXT recommandé sur 3 lignes:
  Like et commente ta réponse
  Abonne-toi à OptiTAB
  Active la cloche pour les prochains exercices

Description YouTube obligatoire:
- Après les slides, ajoute un bloc YOUTUBE_DESCRIPTION copiable.
- Commence par une description courte et accrochante de l'exercice (2-3 phrases).
- Explique ce que l'élève va apprendre dans la vidéo.
- Ajoute un timestamp si plusieurs parties (optionnel).
- Ajoute les appels à l'action: like, commentaire, abonnement.
- Termine par 5-8 hashtags maths pertinents.
- Format obligatoire:
YOUTUBE_DESCRIPTION:
...
END_YOUTUBE_DESCRIPTION

Types autorisés:
- hook
- katex
- cumulative_katex
- result (résultat final autonome, jamais cumulatif)
- cta

Layouts autorisés (optionnel, après le type, séparé par |):
- (rien) → layout plein écran par défaut
- method → slide standalone "Méthode à savoir" — son TITLE devient le label, son KATEX devient la formule de référence, et tout est mémorisé pour les slides split qui suivent
- split → split-screen 60% / 40%, réservé au 16:9 YouTube

Ordre recommandé pour une correction YouTube:
1. SLIDE 1 | hook
2. SLIDE 2 | katex (énoncé)
3. SLIDE 3 | katex | method   ← affichage plein écran de la méthode
4. SLIDE 4..N | cumulative_katex | split   avec RIGHT (repeat) → l'étape à gauche, la méthode (slide 3) à droite
5. SLIDE résultat | result   → résultat final seul, sans cumul ni TEXT: Correction :
6. SLIDE final | cta   (toujours indépendant, pas de split)

Mode METHOD (slide standalone):
- S'utilise une seule fois, juste après l'énoncé.
- Présente en grand la formule ou la méthode clé.
- TITLE: devient le label encadré reproduit ensuite à droite (ex: "Méthode IPP").
- KATEX: la formule de référence (1 à 2 lignes max).
- Le slide est rendu en plein écran comme un slide katex normal — pas de split sur cette slide.
- Son contenu est mémorisé et automatiquement repris à droite des slides | split suivantes.

Mode SPLIT (16:9 uniquement):
- S'applique aux slides katex / cumulative_katex (jamais aux hook, method, result, cta).
- Colonne GAUCHE (60% largeur): l'étape de calcul en cours, change à chaque slide.
- Colonne DROITE (40% largeur, panneau indigo clair): la formule/méthode déclarée par la slide method précédente.
- Écris simplement RIGHT (repeat) — pas besoin de re-déclarer le contenu, il provient de la slide method.
- (Optionnel) Tu peux quand même écrire un bloc RIGHT: + LABEL: + KATEX: si tu veux changer la référence en cours de route.
- Max 2 lignes KATEX dans LEFT.
- VOICE: reste au niveau de la slide (au-dessus de LEFT:), jamais à l'intérieur de LEFT/RIGHT.
- TITLE: et TEXT: sont autorisés dans LEFT.
- Les slides non-split (hook, cta, result, method, et slides katex standard) ne sont pas affectées.

Conseils spécifiques YouTube 16:9:
- Une slide peut contenir jusqu'à 8 lignes KATEX simples ou 5 lignes avec fractions (en plein écran).
- En mode split, limite à 2 lignes KATEX par colonne pour rester lisible.
- Profite de la largeur: utilise "même ligne" pour montrer A = ... ; B = ... côte à côte (plein écran) ou le mode split pour garder la méthode visible en permanence (correction).
- Le texte (TEXT:) peut être plus long qu'en reel (3-4 lignes max).
- Utilise result seulement pour la formule finale isolée; garde l'appel à l'action dans cta.
- Chaque slide dure en général 5-10 secondes en YouTube (vs 3-5 pour un reel).

Exemple prêt à copier (intégration par parties, slide méthode + slides split):
SLIDE 1 | hook
TITLE: Intégration par parties
KATEX: I=\\int_0^1 x\\,e^x\\,dx
TEXT: On calcule cette intégrale avec la méthode IPP.
VOICE: [curious] Voici une intégrale classique... le produit d'un polynôme et d'une exponentielle, parfait pour l'IPP.
---
SLIDE 2 | katex
TEXT: Énoncé :
KATEX: I=\\int_0^1 x\\,e^x\\,dx
VOICE: [calm] Énoncé: on cherche la valeur exacte de l'intégrale de x fois e puissance x, entre 0 et 1.
---
SLIDE 3 | katex | method
TITLE: Méthode IPP
KATEX: \\int_a^b u\\,v' = \\Big[u\\,v\\Big]_a^b - \\int_a^b u'\\,v
VOICE: [thoughtful] Voici la formule d'intégration par parties qui va nous guider toute la correction.
---
SLIDE 4 | cumulative_katex | split
VOICE: [calm] On pose u égal x et v prime égal e puissance x.
LEFT:
TEXT: Correction :
KATEX: u = x \\qquad v' = e^x
RIGHT (repeat)
---
SLIDE 5 | cumulative_katex | split
VOICE: [thoughtful] On dérive u et on intègre v prime: u prime vaut 1, v vaut e puissance x.
LEFT:
KATEX: u' = 1 \\qquad v = e^x
RIGHT (repeat)
---
SLIDE 6 | cumulative_katex | split
VOICE: [thoughtful] On applique la formule: u v entre 0 et 1, moins l'intégrale de u prime v.
LEFT:
KATEX: I=\\Big[x\\,e^x\\Big]_0^1 - \\int_0^1 e^x\\,dx
RIGHT (repeat)
---
SLIDE 7 | cumulative_katex | split
VOICE: [calm] Le crochet vaut e moins zéro, et l'intégrale de e puissance x donne e moins 1.
LEFT:
KATEX: I = e - \\Big[e^x\\Big]_0^1
KATEX: I = e - (e - 1)
RIGHT (repeat)
---
SLIDE 8 | result
TITLE: Résultat
KATEX: I = \\int_0^1 x\\,e^x\\,dx = 1
VOICE: [excited] Tout se simplifie... et on obtient un résultat magnifique: 1 !
---
SLIDE 9 | cta
TITLE: Résultat
KATEX: I = 1
TEXT: Like et commente ta réponse
Abonne-toi à OptiTAB
Active la cloche pour les prochains exercices
VOICE: [warmly] Abonne-toi pour la suite des exercices d'intégration.
---
YOUTUBE_DESCRIPTION:
🧮 Intégration par parties — Calcul de ∫₀¹ x·eˣ dx

Dans cette vidéo, on calcule pas à pas l'intégrale de x·eˣ entre 0 et 1 avec la méthode d'intégration par parties (IPP). La formule de référence reste visible en permanence sur la droite de l'écran pour bien comprendre chaque étape.

Au programme :
✅ Choix de u et v'
✅ Calcul de u' et v
✅ Application de la formule IPP
✅ Simplification et résultat final

👇 Donne ta réponse en commentaire avant de regarder la correction !

#maths #intégrale #IPP #intégrationparparties #terminale #bac #mathématiques #lycée #exercicemaths
END_YOUTUBE_DESCRIPTION
`

const CAROUSEL_FORMAT_TEMPLATE = `FORMAT CARROUSEL OPTITAB (PRO)

Objectif:
- Carrousel marketing premium prêt pour Instagram / Facebook / TikTok.
- But principal: donner envie d'aller sur optitab.net et de s'abonner.
- Audience: élèves, parents, lycéens, étudiants qui veulent progresser en maths.
- Format: 4:5 portrait, 1080x1350 px.
- Chaque SLIDE = 1 image indépendante. Pas de cumul entre slides.
- Aucune voix, aucun sous-titre, aucun contenu vidéo, aucun exercice détaillé.
- Style: propre, clair, crédible, professionnel, premium, orienté conversion.

ÉLÉMENTS AUTO-AJOUTÉS PAR LE TEMPLATE (NE LES ÉCRIS PAS DANS LE TEXT):
- Logo "OptiTAB" en haut à gauche de chaque slide (auto).
- Numéro de slide "01 / 07" en haut à droite (auto).
- Mention "optitab.net" en bas de chaque slide (sauf la cover) (auto).
- Bouton "Glisse →" sur la slide 1 (auto).
- Bouton "Abonne-toi sans engagement →" sur la slide CTA (auto).
- URL "optitab.net" mise en avant sur la slide CTA (auto).
⚠️ N'écris PAS ces éléments dans TITLE ni TEXT, sinon ils apparaîtront en double.

Structure obligatoire de chaque slide:
SLIDE <numéro> | <type>
TITLE: <titre court, déjà mis en gros par le template>
VISUEL: <description précise d'une image IA, sans texte dans l'image>
TEXT: <une ligne courte; pour plusieurs lignes répéter TEXT: à chaque fois>
---

Types autorisés:
- hook  → slide 1, COUVERTURE. Titre énorme centré. TEXT = 1 sous-titre court.
- katex → slides intermédiaires, CONTENU. Titre + 1 à 4 puces (bullets) tirées des TEXT.
- cta   → DERNIÈRE slide. Titre = grande promesse. TEXT = 2 à 4 bénéfices courts.

Architecture obligatoire (7 slides):
- SLIDE 1 | hook: COUVERTURE. Le meilleur hook possible. TITLE court et fort, 1 ligne TEXT = sous-titre. ❌ Pas de "Glisse", pas de "optitab.net" (auto).
- SLIDE 2 | katex: PROBLÈME / FRUSTRATION. TITLE + 1-2 TEXT.
- SLIDE 3 | katex: SOLUTION OPTITAB. TITLE + 1-2 TEXT.
- SLIDE 4 | katex: MÉTHODE / FONCTIONNALITÉ PHARE (cours, fiches, corrections pas à pas). TITLE + 2-3 TEXT.
- SLIDE 5 | katex: PREUVES CHIFFRÉES. TITLE + 3-4 TEXT (ex: "+150 chapitres").
- SLIDE 6 | katex: RÉSULTAT / BÉNÉFICE FINAL. TITLE + 2-3 TEXT (verbes d'action).
- SLIDE 7 | cta: CTA FINAL. TITLE = grande promesse style "Prêt à débloquer ton potentiel ?". TEXT = 2-3 bénéfices courts. ❌ Pas de "Abonne-toi", pas de "Va sur optitab.net", pas de "Visite optitab.net" (auto).

Règles TITLE:
- TITLE court, percutant, professionnel.
- 3 à 7 mots maximum. Pas de point final inutile.
- Pas de hashtag, pas d'emoji.

Règles TEXT (= les puces affichées sous le titre):
- 1 ligne TEXT = 1 puce visuelle. Pour plusieurs puces, répète TEXT: à chaque ligne.
- Chaque TEXT: 4 à 12 mots maximum. Court, lisible en 1 seconde.
- 1 à 4 lignes TEXT par slide. Au-delà de 4 c'est trop chargé.
- Pas de mots collés type "Apprendsplusvite". Phrases naturelles.
- Pas d'exagération irréaliste, pas de faux prix, pas de fausses promesses.

Règles VISUEL (servira à générer un FOND sans texte):
- Décris une scène/image précise: composition, sujet, ambiance.
- Univers OptiTAB: maths, cours, fiches de synthèse, exercices corrigés, dashboard, interface bleue/blanche, plateforme éducative premium.
- Préfère: mockup d'interface (cartes, écran), élève qui révise (de dos ou silhouette), composition éditoriale.
- Évite: photos stock génériques, gros plans de visages reconnaissables, capture d'un site réel.
- ⚠️ Le visuel sera généré SANS texte (le texte est ajouté par le template). Donc précise des écrans floutés / formes abstraites pour tout mockup.
- Laisse de l'espace VIDE dans la composition (centre-bas, ou un côté) pour que le texte du template reste lisible.

Description Instagram (obligatoire, à la fin):
- Bloc CAROUSEL_DESCRIPTION copiable.
- Objectif: légende qui donne envie de visiter optitab.net.
- Mentionne l'abonnement sans engagement, l'accès immédiat, la progression en maths.
- Termine par EXACTEMENT 5 hashtags pertinents.
- Format:
CAROUSEL_DESCRIPTION:
...
END_CAROUSEL_DESCRIPTION

Exemple prêt à copier (à adapter, ne pas recopier tel quel):
SLIDE 1 | hook
TITLE: Tes maths méritent mieux
VISUEL: Composition éditoriale bleu/blanc avec un écran d'ordinateur stylisé montrant un mockup OptiTAB (cartes floutées, aucun texte lisible), cahier propre à côté, lumière douce, grand espace vide en bas pour overlay.
TEXT: La plateforme qui structure tes révisions de A à Z.
---
SLIDE 2 | katex
TITLE: Tu te perds dans tes cours
VISUEL: Bureau avec plusieurs onglets de navigateur ouverts en arrière-plan flou, cahier en désordre, ambiance frustration douce, palette bleu/gris, large zone vide à droite.
TEXT: Trop d'onglets, trop de PDF, aucune méthode.
TEXT: Tu révises sans savoir si tu progresses vraiment.
---
SLIDE 3 | katex
TITLE: Un seul endroit, tout structuré
VISUEL: Mockup d'interface OptiTAB sur écran, cartes "Cours" "Fiches" "Exercices" alignées (sans texte lisible dedans), barre latérale épurée, palette OptiTAB.
TEXT: Cours, fiches et corrections au même endroit.
TEXT: Tu sais quoi faire, dans quel ordre.
---
SLIDE 4 | katex
TITLE: Des corrections pas à pas
VISUEL: Mockup de fiche d'exercice corrigé OptiTAB, étapes alignées verticalement (boîtes floutées, aucun texte lisible), repère bleu, fond clair, espace libre à gauche.
TEXT: Comprends la méthode, pas juste le résultat.
TEXT: Repère chaque étape clé.
TEXT: Avance à ton rythme.
---
SLIDE 5 | katex
TITLE: Une vraie base de travail
VISUEL: Composition isométrique avec piles de cartes représentant chapitres / fiches / cours / exercices (formes abstraites floutées, aucun texte), style dashboard premium, ambiance studieuse.
TEXT: +150 chapitres complets
TEXT: +150 fiches de synthèse
TEXT: +150 cours détaillés
TEXT: +1000 exercices corrigés
---
SLIDE 6 | katex
TITLE: Progresse avec méthode
VISUEL: Élève de dos devant un ordinateur ouvert sur la plateforme (écran flouté), cahier propre, ambiance lumineuse et confiante, large espace vide en bas.
TEXT: Comprends plus vite.
TEXT: Révise plus efficacement.
TEXT: Gagne en autonomie.
---
SLIDE 7 | cta
TITLE: Prêt à débloquer ton potentiel ?
VISUEL: Écran final centré, ordinateur et smartphone montrant le mockup OptiTAB (cartes floutées, AUCUN texte lisible), ambiance premium bleu/blanc, fond lumineux, grande zone vide au centre et en bas pour overlay.
TEXT: Choisis ton niveau en 30 secondes.
TEXT: Accès immédiat à toute la plateforme.
TEXT: Sans engagement, résiliable à tout moment.
---
CAROUSEL_DESCRIPTION:
OptiTAB aide les élèves à progresser en maths avec des cours clairs, des fiches de synthèse et des exercices corrigés pas à pas.

La plateforme est pensée pour réviser efficacement, comprendre les méthodes et avancer à ton rythme.

Abonnement sans engagement, accès immédiat.

Découvre OptiTAB sur optitab.net.

#optitab #maths #revision #lycee #soutienscolaire
END_CAROUSEL_DESCRIPTION
`

const CAROUSEL_FORMAT_QUIZ = `FORMAT CARROUSEL QUIZ / QCM

Objectif:
- Carrousel interactif : pose 1 question par slide (sauf cover et reveal/cta).
- But: engager l'audience (commentaires, saves, partages), teaser le contenu OptiTAB.
- Nombre de slides FLEXIBLE: minimum 5, idéalement 7–10. Adapte selon le sujet.
- Structure: cover → N questions (N ≥ 3) → 1 slide reveal des réponses → cta.
- Aucune voix, aucun sous-titre.

ÉLÉMENTS AUTO-AJOUTÉS (NE LES ÉCRIS PAS):
- Logo OptiTAB en haut à gauche, numéro de slide en haut à droite.
- "optitab.net" en bas (sauf cover).
- Bouton "Glisse →" slide 1, bouton CTA dernière slide.

Structure:
SLIDE <n> | <type>
TITLE: <question ou titre>
VISUEL: <description image IA sans texte>
TEXT: <réponse / choix / reveal — 1 ligne = 1 puce>
---

Architecture (nombre de slides variable):
- SLIDE 1 | hook: TITLE = accroche style "Saurais-tu répondre ?". TEXT = 1 ligne teaser.
- SLIDES 2 à N-1 | katex: chaque slide = 1 question. TITLE = la question courte. TEXT = A) … / B) … / C) … / D) … (3 ou 4 choix, A–D max). Ajoute autant de slides questions que nécessaire (3 minimum, jusqu'à 8 si le sujet le mérite).
- AVANT-DERNIÈRE SLIDE | katex: TITLE = "Les réponses 👇". TEXT = 1 ligne par réponse correcte + explication courte.
- DERNIÈRE SLIDE | cta: TITLE = grande promesse. TEXT = 2–3 bénéfices courts.

Règles propositions:
- Lettres autorisées: A, B, C, D uniquement (jamais E ni plus).
- Format obligatoire pour chaque option: "X) contenu" où X ∈ {A, B, C, D}.
- 3 choix minimum, 4 choix maximum par question.
- Nombre de questions à toi de juger selon la profondeur du sujet (3 à 8 questions).

Exemple:
SLIDE 1 | hook
TITLE: Teste tes maths en 4 questions
VISUEL: Composition épurée bleu/blanc, cartes quiz empilées avec points d'interrogation stylisés (aucun texte lisible), fond clair, espace vide en bas.
TEXT: Glisse pour voir si tu es au niveau.
---
SLIDE 2 | katex
TITLE: Qu'est-ce qu'une dérivée ?
VISUEL: Tableau blanc avec courbe esquissée en flouté, craie, ambiance salle de classe premium.
TEXT: A) La vitesse de variation d'une fonction
TEXT: B) L'aire sous une courbe
TEXT: C) Un type d'équation
TEXT: D) Une intégrale définie
---
SLIDE N | cta   (où N = numéro de la dernière slide)
TITLE: Envie de tout maîtriser ?
VISUEL: Écran OptiTAB flouté avec cartes chapitres, ambiance studieuse premium.
TEXT: Cours, fiches et exercices au même endroit.
TEXT: Accès immédiat, sans engagement.
---
CAROUSEL_DESCRIPTION:
Tu as répondu à toutes les questions ? Découvre toutes les notions en détail sur OptiTAB.

Des cours clairs, des fiches de synthèse et des exercices corrigés pour progresser en maths.

Abonnement sans engagement — accès immédiat.

Rejoins-nous sur optitab.net.

#optitab #maths #quiz #revision #lycee
END_CAROUSEL_DESCRIPTION
`

const CAROUSEL_FORMAT_TIPS = `FORMAT CARROUSEL CONSEILS & ASTUCES

Objectif:
- Carrousel "X astuces / méthodes / erreurs" ultra lisible et partageables.
- Chaque slide de contenu = 1 conseil autonome, compréhensible en 2 secondes.
- But: save + partage + trafic vers optitab.net.
- 7 slides : cover → 5 conseils → cta.

ÉLÉMENTS AUTO-AJOUTÉS (NE LES ÉCRIS PAS):
- Logo, numéro, "optitab.net" footer, boutons Glisse/CTA.

Structure:
SLIDE <n> | <type>
TITLE: <titre du conseil ou numéro>
VISUEL: <description image IA sans texte>
TEXT: <explication courte — 1 puce = 1 TEXT:>
---

Architecture (7 slides):
- SLIDE 1 | hook: TITLE = accroche "X astuces pour…". TEXT = 1 promesse courte.
- SLIDE 2–6 | katex: 1 astuce/conseil par slide. TITLE = intitulé de l'astuce. TEXT = 1–3 lignes max.
- SLIDE 7 | cta: TITLE = promesse finale. TEXT = 2–3 bénéfices.

Exemple:
SLIDE 1 | hook
TITLE: 5 astuces pour réviser les maths efficacement
VISUEL: Compositions de fiches stylisées bleu/blanc, cahier propre, stylo, lumière froide premium, espace vide bas.
TEXT: Des méthodes simples qui changent tout.
---
SLIDE 2 | katex
TITLE: Commence par la méthode, pas l'exercice
VISUEL: Mockup fiche méthode OptiTAB (texte flouté), repères visuels colorés, fond blanc épuré.
TEXT: Lire la méthode avant de faire l'exercice = 2× plus efficace.
TEXT: Tu évites les erreurs de départ.
---
SLIDE 7 | cta
TITLE: Mets ces conseils en pratique dès aujourd'hui
VISUEL: Élève de dos devant écran OptiTAB (flouté), ambiance studieuse, lumière confiante.
TEXT: Cours + fiches + corrections au même endroit.
TEXT: Accès immédiat, sans engagement.
---
CAROUSEL_DESCRIPTION:
Ces 5 astuces peuvent vraiment changer ta façon de réviser les maths.

Chez OptiTAB, on a structuré toute la méthode pour toi : cours clairs, fiches de synthèse, exercices corrigés pas à pas.

Sans engagement, accès immédiat sur optitab.net.

#optitab #maths #astuces #revision #methode
END_CAROUSEL_DESCRIPTION
`

const CAROUSEL_FORMAT_AVANTAPRES = `FORMAT CARROUSEL AVANT / APRÈS (TRANSFORMATION)

Objectif:
- Montrer la transformation que vit un élève grâce à OptiTAB.
- Contraste fort : "avant" = douleur / galère → "après" = clarté / confiance.
- 7 slides : cover → 3 slides "avant" → 2 slides "après" → cta.

ÉLÉMENTS AUTO-AJOUTÉS (NE LES ÉCRIS PAS):
- Logo, numéro, footer URL, boutons auto.

Structure:
SLIDE <n> | <type>
TITLE: <titre percutant>
VISUEL: <description image IA sans texte>
TEXT: <ligne courte — 1 TEXT: = 1 puce>
---

Architecture (7 slides):
- SLIDE 1 | hook: TITLE = accroche sur la douleur ou la transformation. TEXT = 1 promesse.
- SLIDE 2 | katex: AVANT 1 — La situation avant. TITLE négatif / frustration. TEXT = 2–3 symptômes.
- SLIDE 3 | katex: AVANT 2 — Les conséquences. TITLE = ce que ça coûte. TEXT = 2–3 lignes.
- SLIDE 4 | katex: AVANT 3 — La cause racine. TITLE = pourquoi ça arrive. TEXT = 1–2 lignes.
- SLIDE 5 | katex: APRÈS 1 — La solution. TITLE = ce qui change. TEXT = 2–3 lignes.
- SLIDE 6 | katex: APRÈS 2 — Le résultat concret. TITLE = bénéfice chiffré ou visuel. TEXT = 3–4 bénéfices.
- SLIDE 7 | cta: TITLE = invitation à la transformation. TEXT = 2–3 bénéfices + urgence douce.

Exemple:
SLIDE 1 | hook
TITLE: Avant OptiTAB vs. Après OptiTAB
VISUEL: Composition deux zones distinctes — côté gauche flouté/sombre (cahier en désordre), côté droit lumineux/épuré (interface OptiTAB), séparation nette, espace texte en bas.
TEXT: Ce que ça change vraiment.
---
SLIDE 2 | katex
TITLE: Tu révises mais rien ne rentre
VISUEL: Bureau encombré, plusieurs PDF ouverts, cahier avec ratures, ambiance fatigue, palette gris-bleu désaturé.
TEXT: Des cours partout, aucune méthode claire.
TEXT: Tu refais les mêmes erreurs sans comprendre pourquoi.
TEXT: Tu perds du temps à chercher les bons docs.
---
SLIDE 7 | cta
TITLE: Ta progression commence maintenant
VISUEL: Écran OptiTAB flouté, ambiance lumineuse confiante, smartphone + ordinateur, espace vide central.
TEXT: Cours + fiches + corrections au même endroit.
TEXT: Choisis ton niveau en 30 secondes.
TEXT: Sans engagement, résiliable à tout moment.
---
CAROUSEL_DESCRIPTION:
Avant OptiTAB : trop d'onglets, aucune méthode, des révisions inefficaces.

Après OptiTAB : une progression structurée, des cours clairs et des exercices corrigés pas à pas.

La différence ? Une plateforme pensée pour toi.

Abonnement sans engagement sur optitab.net.

#optitab #maths #avantapres #revision #lycee
END_CAROUSEL_DESCRIPTION
`

const CAROUSEL_FORMAT_STORYTELLING = `FORMAT CARROUSEL STORYTELLING / NARRATIF

Objectif:
- Raconter une histoire courte et émotionnelle qui aboutit sur OptiTAB.
- Format narratif = personnage → problème → tournant → solution → résultat → invitation.
- 7 slides : setup → tension → tournant → résolution → preuve → bénéfice → cta.

ÉLÉMENTS AUTO-AJOUTÉS (NE LES ÉCRIS PAS):
- Logo, numéro, footer, boutons auto.

Structure:
SLIDE <n> | <type>
TITLE: <titre de l'acte>
VISUEL: <image IA sans texte — doit refléter l'émotion du moment>
TEXT: <narration courte — 1 TEXT: = 1 phrase/puce>
---

Architecture (7 slides):
- SLIDE 1 | hook: SETUP. TITLE = accroche narrative forte. TEXT = présentation du personnage / contexte.
- SLIDE 2 | katex: TENSION. TITLE = le problème. TEXT = frustrations concrètes.
- SLIDE 3 | katex: POINT DE RUPTURE. TITLE = le déclic. TEXT = ce qui a tout changé.
- SLIDE 4 | katex: DÉCOUVERTE. TITLE = découverte d'OptiTAB. TEXT = ce qu'il a trouvé.
- SLIDE 5 | katex: RÉSULTAT. TITLE = ce qui a changé concrètement. TEXT = 3–4 résultats mesurables.
- SLIDE 6 | katex: LEÇON. TITLE = la leçon universelle. TEXT = 2–3 phrases inspirantes.
- SLIDE 7 | cta: INVITATION. TITLE = et toi ? TEXT = 2–3 bénéfices + appel à l'action doux.

Exemple:
SLIDE 1 | hook
TITLE: Il avait 8 en maths en seconde
VISUEL: Silhouette d'élève de dos devant un bureau, lumière d'écran, ambiance soir studieux, palette bleu froid.
TEXT: Aujourd'hui il est en prépa.
TEXT: Voici ce qui a tout changé.
---
SLIDE 7 | cta
TITLE: Et toi, tu commences quand ?
VISUEL: Écran OptiTAB flouté avec interface chapitres, ambiance lumineuse motivante.
TEXT: Accès immédiat à tous les cours.
TEXT: Avance à ton rythme, sans pression.
TEXT: Sans engagement.
---
CAROUSEL_DESCRIPTION:
Une méthode claire peut tout changer.

Chez OptiTAB, on accompagne les élèves avec des cours structurés, des fiches de synthèse et des exercices corrigés pas à pas.

Rejoins des milliers d'élèves qui ont repris confiance en maths.

Accès immédiat, sans engagement — optitab.net.

#optitab #maths #motivation #revision #reussite
END_CAROUSEL_DESCRIPTION
`

const CAROUSEL_FORMAT_NOTION = `FORMAT CARROUSEL NOTION PÉDAGOGIQUE

Objectif:
- Expliquer une notion de maths en 7 slides claires et pédagogiques.
- Chaque slide = 1 étape de compréhension. Peut inclure des formules (KaTeX).
- But: crédibilité / valeur ajoutée → envie de s'abonner à OptiTAB.

ÉLÉMENTS AUTO-AJOUTÉS (NE LES ÉCRIS PAS):
- Logo, numéro, footer, boutons auto.

Structure:
SLIDE <n> | <type>
TITLE: <titre de l'étape>
VISUEL: <image IA sans texte>
TEXT: <explication courte — 1 TEXT: = 1 puce>
KATEX: <formule LaTeX si pertinent — facultatif>
---

Architecture (7 slides):
- SLIDE 1 | hook: TITLE = titre de la notion + accroche. TEXT = 1 promesse pédagogique.
- SLIDE 2 | katex: DÉFINITION. TITLE + 1–2 TEXT + 1 KATEX (définition formelle).
- SLIDE 3 | katex: INTUITION / VISUALISATION. TITLE + 2 TEXT — l'idée géométrique ou physique.
- SLIDE 4 | katex: FORMULE CLÉ. TITLE + KATEX principal. TEXT = lecture de la formule.
- SLIDE 5 | katex: MÉTHODE PAS À PAS. TITLE + 3–4 TEXT (étapes numérotées).
- SLIDE 6 | katex: EXEMPLE RÉSOLU. TITLE + KATEX intermédiaires + TEXT.
- SLIDE 7 | cta: TITLE = invitation à aller plus loin. TEXT = 2–3 bénéfices.

Exemple:
SLIDE 1 | hook
TITLE: La dérivée en 6 slides
VISUEL: Courbe mathématique esquissée sur tableau blanc épuré (flouté, sans texte lisible), couleurs OptiTAB, espace vide bas.
TEXT: Comprendre le concept une fois pour toutes.
---
SLIDE 4 | katex
TITLE: La formule fondamentale
VISUEL: Fiche méthode stylisée (texte flouté), repère visuel bleu, fond blanc.
KATEX: f'(x)=\\lim_{h\\to 0}\\frac{f(x+h)-f(x)}{h}
TEXT: Le taux de variation quand h tend vers 0.
---
SLIDE 7 | cta
TITLE: Maîtrise toutes les notions du lycée
VISUEL: Interface OptiTAB floutée avec liste de chapitres, ambiance studieuse premium.
TEXT: +150 chapitres complets disponibles.
TEXT: Cours, fiches et exercices corrigés.
TEXT: Accès immédiat, sans engagement.
---
CAROUSEL_DESCRIPTION:
Tu veux vraiment comprendre les maths, pas juste mémoriser ?

OptiTAB propose +150 chapitres complets : cours clairs, fiches de synthèse, exercices corrigés pas à pas.

Rejoins la plateforme et progresse à ton rythme.

Abonnement sans engagement — optitab.net.

#optitab #maths #cours #derivee #lycee
END_CAROUSEL_DESCRIPTION
`

const CAROUSEL_FORMATS = [
  {
    id: 'marketing',
    label: 'Marketing / Conversion',
    icon: '🚀',
    description: 'Présenter OptiTAB, convertir en abonnés',
    template: CAROUSEL_FORMAT_TEMPLATE,
  },
  {
    id: 'notion',
    label: 'Notion pédagogique',
    icon: '📐',
    description: 'Expliquer une notion de maths en 7 slides',
    template: CAROUSEL_FORMAT_NOTION,
  },
  {
    id: 'tips',
    label: 'Conseils & Astuces',
    icon: '💡',
    description: '5 conseils / méthodes — très partageable',
    template: CAROUSEL_FORMAT_TIPS,
  },
  {
    id: 'quiz',
    label: 'Quiz / QCM',
    icon: '🎯',
    description: '4 questions + reveal — engagement max',
    template: CAROUSEL_FORMAT_QUIZ,
  },
  {
    id: 'avantapres',
    label: 'Avant / Après',
    icon: '🔄',
    description: 'Transformation émotionnelle — save & share',
    template: CAROUSEL_FORMAT_AVANTAPRES,
  },
  {
    id: 'story',
    label: 'Storytelling',
    icon: '📖',
    description: 'Histoire narrative avec personnage — émotion',
    template: CAROUSEL_FORMAT_STORYTELLING,
  },
]

const TEMPLATE_PLACEHOLDERS = Object.freeze({
  reel: `MODE AUTO (IA décide le nombre de slides)
TITLE: Dérivation produit
HOOK: Défi bac
KATEX: f(x)=x\\ln(x)
KATEX: u=x \\qquad v=\\ln(x)
KATEX: u'=1 \\qquad v'=\\frac{1}{x}
KATEX: f'(x)=\\ln(x)+1
CTA: Abonne-toi à OptiTAB | Sauvegarde ce Reel | Commente ton résultat`,
  youtube: `SLIDE 1 | hook
TITLE: Intégration par parties
KATEX: I=\\int_0^1 x\\,e^x\\,dx
TEXT: On calcule cette intégrale avec la méthode IPP.
VOICE: [curious] Voici une intégrale classique.
---
SLIDE 2 | katex
TEXT: Énoncé :
KATEX: I=\\int_0^1 x\\,e^x\\,dx
VOICE: On pose l'énoncé.`,
  carousel: `SLIDE 1 | hook
TITLE: Tes maths méritent mieux
VISUEL: Composition éditoriale bleu/blanc, écran d'ordinateur stylisé montrant un mockup OptiTAB (cartes floutées, aucun texte lisible), cahier propre à côté, lumière douce, grand espace vide en bas.
TEXT: La plateforme qui structure tes révisions de A à Z.
---
SLIDE 2 | katex
TITLE: Tu te perds dans tes cours
VISUEL: Bureau avec plusieurs onglets de navigateur ouverts en arrière-plan flou, cahier en désordre, ambiance frustration douce, palette bleu/gris, large zone vide à droite.
TEXT: Trop d'onglets, trop de PDF, aucune méthode.
TEXT: Tu révises sans savoir si tu progresses.
---
SLIDE 3 | katex
TITLE: Un seul endroit, tout structuré
VISUEL: Mockup d'interface OptiTAB, cartes "Cours" "Fiches" "Exercices" alignées (sans texte lisible dedans), barre latérale épurée, palette OptiTAB.
TEXT: Cours, fiches et corrections au même endroit.
TEXT: Tu sais quoi faire, dans quel ordre.
---
SLIDE 4 | katex
TITLE: Des corrections pas à pas
VISUEL: Mockup fiche d'exercice corrigé OptiTAB, étapes alignées verticalement (boîtes floutées, aucun texte lisible), repère bleu, espace libre à gauche.
TEXT: Comprends la méthode, pas juste le résultat.
TEXT: Repère chaque étape clé.
TEXT: Avance à ton rythme.
---
SLIDE 5 | katex
TITLE: Une vraie base de travail
VISUEL: Composition isométrique avec piles de cartes (formes abstraites floutées, aucun texte), style dashboard premium, ambiance studieuse.
TEXT: +150 chapitres complets
TEXT: +150 fiches de synthèse
TEXT: +150 cours détaillés
TEXT: +1000 exercices corrigés
---
SLIDE 6 | katex
TITLE: Progresse avec méthode
VISUEL: Élève de dos devant un ordinateur ouvert sur la plateforme (écran flouté), cahier propre, ambiance lumineuse et confiante, espace vide en bas.
TEXT: Comprends plus vite.
TEXT: Révise plus efficacement.
TEXT: Gagne en autonomie.
---
SLIDE 7 | cta
TITLE: Prêt à débloquer ton potentiel ?
VISUEL: Écran final centré, ordinateur et smartphone montrant le mockup OptiTAB (cartes floutées, aucun texte lisible), ambiance premium bleu/blanc, fond lumineux, grande zone vide au centre et en bas.
TEXT: Choisis ton niveau en 30 secondes.
TEXT: Accès immédiat à toute la plateforme.
TEXT: Sans engagement, résiliable à tout moment.
---
CAROUSEL_DESCRIPTION:
Découvre OptiTAB sur optitab.net et progresse en maths avec une plateforme claire, structurée et accessible immédiatement.

Abonnement sans engagement, accès immédiat.

#optitab #maths #revision #lycee #soutienscolaire
END_CAROUSEL_DESCRIPTION`,
})

const FORMAT_CONFIGS = Object.freeze({
  reel: {
    managementTitle: 'Gestion des reels',
    countSingular: 'reel',
    countPlural: 'reels',
    createButtonLabel: 'Nouveau reel',
    emptySelectionLabel: 'Selectionne un reel en base ou cree un nouveau reel.',
    descriptionTitle: 'Description Instagram',
    descriptionHelp: 'Texte SEO pret a copier pour publier le reel.',
    copyDescriptionLabel: 'Copier Instagram',
    emptyDescriptionLabel: 'Ajoute un bloc INSTAGRAM_DESCRIPTION dans le template genere.',
    listTitle: 'Reels en base',
    emptyListLabel: 'Aucun reel enregistre.',
    loadingListLabel: 'Chargement des reels...',
    newProjectTitle: 'Nouveau reel',
    editProjectTitle: 'Modifier le reel',
    createSubmitLabel: 'Creer le reel',
    updateSubmitLabel: 'Mettre a jour',
    templateBuilderTitle: 'Création Reel',
    templateTextareaLabel: 'Format / Script (par slides)',
    templatePlaceholder: TEMPLATE_PLACEHOLDERS.reel,
    formatTemplate: REEL_FORMAT_TEMPLATE,
    entityWithArticle: 'le reel',
    entityDefaultSlug: 'optitab-reel',
  },
  youtube: {
    managementTitle: 'Gestion des vidéos YouTube',
    countSingular: 'vidéo',
    countPlural: 'vidéos',
    createButtonLabel: 'Nouvelle vidéo YouTube',
    emptySelectionLabel: 'Selectionne une vidéo YouTube en base ou cree une nouvelle vidéo.',
    descriptionTitle: 'Description YouTube',
    descriptionHelp: 'Description SEO prete a copier pour YouTube.',
    copyDescriptionLabel: 'Copier YouTube',
    emptyDescriptionLabel: 'Ajoute un bloc YOUTUBE_DESCRIPTION dans le template genere.',
    listTitle: 'Vidéos YouTube en base',
    emptyListLabel: 'Aucune vidéo YouTube enregistree.',
    loadingListLabel: 'Chargement des vidéos YouTube...',
    newProjectTitle: 'Nouvelle vidéo YouTube',
    editProjectTitle: 'Modifier la vidéo YouTube',
    createSubmitLabel: 'Creer la vidéo',
    updateSubmitLabel: 'Mettre a jour',
    templateBuilderTitle: 'Création YouTube',
    templateTextareaLabel: 'Format / Script YouTube (par slides)',
    templatePlaceholder: TEMPLATE_PLACEHOLDERS.youtube,
    formatTemplate: YOUTUBE_FORMAT_TEMPLATE,
    entityWithArticle: 'la vidéo',
    entityDefaultSlug: 'optitab-youtube',
  },
  carousel: {
    managementTitle: 'Gestion des carrousels',
    countSingular: 'carrousel',
    countPlural: 'carrousels',
    createButtonLabel: 'Nouveau carrousel',
    emptySelectionLabel: 'Selectionne un carrousel en base ou cree un nouveau carrousel.',
    descriptionTitle: 'Description carrousel',
    descriptionHelp: 'Texte pret a copier pour attirer vers optitab.net et l abonnement.',
    copyDescriptionLabel: 'Copier description',
    emptyDescriptionLabel: 'Ajoute un bloc CAROUSEL_DESCRIPTION dans le template genere.',
    listTitle: 'Carrousels en base',
    emptyListLabel: 'Aucun carrousel enregistre.',
    loadingListLabel: 'Chargement des carrousels...',
    newProjectTitle: 'Nouveau carrousel',
    editProjectTitle: 'Modifier le carrousel',
    createSubmitLabel: 'Creer le carrousel',
    updateSubmitLabel: 'Mettre a jour',
    templateBuilderTitle: 'Création Carrousel',
    templateTextareaLabel: 'Format carrousel (1 slide = 1 image, pas de voix)',
    templatePlaceholder: TEMPLATE_PLACEHOLDERS.carousel,
    formatTemplate: CAROUSEL_FORMAT_TEMPLATE,
    entityWithArticle: 'le carrousel',
    entityDefaultSlug: 'optitab-carousel',
  },
})

const studioFormatConfig = computed(() => FORMAT_CONFIGS[studioFormat.value] || FORMAT_CONFIGS.reel)
const formatHelpTemplate = computed(() => studioFormatConfig.value.formatTemplate)
const selectedProjectFormat = computed(() => normalizeFormatType(selectedProject.value?.format_type || studioFormat.value))
const isCarouselProject = computed(() => selectedProjectFormat.value === 'carousel')
const canRegenerateCarouselImages = computed(() => (
  isCarouselProject.value && Array.isArray(selectedProject.value?.slides) && selectedProject.value.slides.length > 0
))
const filteredGeminiModels = computed(() => {
  const search = String(geminiModelSearch.value || '').trim().toLowerCase()
  const models = Array.isArray(geminiModels.value) ? geminiModels.value : []
  if (!search) return models

  const selectedModel = models.find((model) => model.id === selectedGeminiModelId.value)
  const matches = models.filter((model) => {
    const haystack = [
      model.id,
      model.display_name,
      model.input_price_per_1m_tokens,
      model.output_price_per_1m_tokens,
    ].filter(Boolean).join(' ').toLowerCase()
    return haystack.includes(search)
  })

  if (selectedModel && !matches.some((model) => model.id === selectedModel.id)) {
    return [selectedModel, ...matches]
  }
  return matches
})
const geminiRemainingLabel = computed(() => {
  if (geminiUsage.value?.display_remaining === null || geminiUsage.value?.display_remaining === undefined) {
    return 'Budget non défini'
  }
  return formatGeminiMoney(geminiUsage.value.display_remaining)
})
const lastGeminiUsageDisplayCost = computed(() => {
  if (!lastGeminiUsage.value) return 0
  if (lastGeminiUsage.value.display_cost !== undefined && lastGeminiUsage.value.display_cost !== null) {
    return lastGeminiUsage.value.display_cost
  }
  const usdCost = Number(lastGeminiUsage.value.total_cost_usd || 0)
  if ((geminiUsage.value?.display_currency || 'USD') === 'EUR') {
    return usdCost * Number(geminiUsage.value?.eur_per_usd || 0.92)
  }
  return usdCost
})

const selectedSlide = computed(() => {
  if (!selectedProject.value?.slides?.length) return null
  return selectedProject.value.slides.find((slide) => Number(slide.id) === Number(selectedSlideId.value)) || null
})

const projectFormInitialValues = computed(() => editingProject.value || {})
const projectFormTitle = computed(() => (
  editingProject.value?.id
    ? studioFormatConfig.value.editProjectTitle
    : studioFormatConfig.value.newProjectTitle
))
const projectFormSubmitLabel = computed(() => (
  editingProject.value?.id
    ? studioFormatConfig.value.updateSubmitLabel
    : studioFormatConfig.value.createSubmitLabel
))
const projectSpeechText = computed(() => buildProjectSpeechText(selectedProject.value))
const slidesSpeechCount = computed(() => countSlidesWithSpeechText(selectedProject.value))
const generatedSlideSpeechCount = computed(() => countGeneratedSlideSpeeches(selectedProject.value))
const canGenerateSpeech = computed(() => Boolean(selectedProject.value?.id && projectSpeechText.value))
const selectedProvider = computed(() => {
  return providers.value.find((p) => p.id === selectedProviderId.value) || null
})
const elevenLabsProvider = computed(() => {
  return providers.value.find((p) => p.id === 'elevenlabs') || null
})
const elevenLabsUsage = computed(() => elevenLabsProvider.value?.usage || null)
const elevenLabsUsageAvailable = computed(() => {
  const usage = elevenLabsUsage.value
  return Boolean(usage?.available && Number(usage.total) > 0)
})
const elevenLabsUsagePercent = computed(() => {
  const percent = Number(elevenLabsUsage.value?.used_percent)
  if (!Number.isFinite(percent)) return 0
  return Math.max(0, Math.min(100, percent))
})
const elevenLabsUsageBarStyle = computed(() => ({
  width: `${elevenLabsUsagePercent.value}%`,
}))
const elevenLabsUsageConsumedLabel = computed(() => formatCreditCount(elevenLabsUsage.value?.used))
const elevenLabsUsageTotalLabel = computed(() => formatCreditCount(elevenLabsUsage.value?.total))
const elevenLabsUsageRemainingLabel = computed(() => formatCreditCount(elevenLabsUsage.value?.remaining))
const elevenLabsUsagePercentLabel = computed(() => `${formatPercent(elevenLabsUsagePercent.value)}%`)
const elevenLabsUsageResetLabel = computed(() => {
  const resetUnix = Number(elevenLabsUsage.value?.reset_unix)
  if (!Number.isFinite(resetUnix) || resetUnix <= 0) return ''
  const resetDate = new Date(resetUnix * 1000)
  if (Number.isNaN(resetDate.getTime())) return ''
  return `Reset le ${resetDate.toLocaleDateString('fr-FR')}`
})
const elevenLabsUsageErrorLabel = computed(() => {
  const usage = elevenLabsUsage.value
  if (usage?.error_code === 'missing_permissions') {
    return 'Permission user_read manquante sur la cle ElevenLabs.'
  }
  return usage?.error || 'Impossible de lire les credits ElevenLabs.'
})
const googleUsage = computed(() => {
  if (selectedProviderId.value !== 'google') return null
  return selectedVoice.value?.quota || null
})
const googleUsageAvailable = computed(() => {
  const usage = googleUsage.value
  return Boolean(usage && Number(usage.free_monthly_character_limit) > 0)
})
const googleUsagePercent = computed(() => {
  const percent = Number(googleUsage.value?.used_percent)
  return Number.isFinite(percent) ? Math.max(0, Math.min(100, percent)) : 0
})
const googleUsageBarStyle = computed(() => ({
  width: `${googleUsagePercent.value}%`,
}))
const googleUsageConsumedLabel = computed(() => formatCreditCount(googleUsage.value?.used_characters))
const googleUsageTotalLabel = computed(() => formatCreditCount(googleUsage.value?.free_monthly_character_limit))
const googleUsageRemainingLabel = computed(() => formatCreditCount(googleUsage.value?.remaining_free_characters))
const googleUsagePercentLabel = computed(() => `${formatPercent(googleUsagePercent.value)}%`)
const googleUsageDetailsLabel = computed(() => {
  const usage = googleUsage.value || {}
  const bucket = String(usage.bucket || '').trim()
  const month = String(usage.month || '').trim()
  const disableRatio = Number(usage.disable_ratio)
  const remainingUntilDisable = Number(usage.remaining_until_disable_characters)
  const parts = []
  if (bucket) parts.push(`Famille ${bucket}`)
  if (month) parts.push(`mois ${month}`)
  if (Number.isFinite(disableRatio) && disableRatio > 0) {
    parts.push(`seuil sécurité ${Math.round(disableRatio * 100)}%`)
  }
  if (Number.isFinite(remainingUntilDisable)) {
    parts.push(`${formatCreditCount(remainingUntilDisable)} avant seuil`)
  }
  return parts.join(' · ')
})
const googleUsageErrorLabel = computed(() => {
  if (!selectedVoice.value) return 'Sélectionne une voix Google.'
  return 'Quota gratuit indisponible pour cette famille de voix.'
})
const selectedProviderConfigured = computed(() => Boolean(selectedProvider.value?.configured))
const baseCurrentProviderVoices = computed(() => selectedProvider.value?.voices || [])
const currentProviderVoices = computed(() => {
  if (selectedProviderId.value !== 'elevenlabs') return baseCurrentProviderVoices.value
  return buildElevenLabsFavoriteVoices(baseCurrentProviderVoices.value)
})
const selectedProviderMeta = computed(() => {
  if (!selectedProvider.value) return ''
  if (!selectedProvider.value.configured) {
    return selectedProvider.value.error
      ? `Non configure: ${selectedProvider.value.error}`
      : 'Non configure (cle API ou credentials manquants)'
  }
  return ''
})
const selectedVoice = computed(() => {
  return currentProviderVoices.value.find((voice) => voice.voice_id === selectedVoiceId.value) || null
})
const favoriteVoiceIds = computed(() => new Set(currentProviderVoices.value.map((voice) => voice.voice_id)))
const selectedLibraryVoice = computed(() => {
  return voiceLibraryOptions.value.find((voice) => voice.voice_id === selectedLibraryVoiceId.value) || null
})
const selectedLibraryVoiceIsFavorite = computed(() => {
  return Boolean(selectedLibraryVoice.value?.voice_id && favoriteVoiceIds.value.has(selectedLibraryVoice.value.voice_id))
})
const selectedVoiceApiUsable = computed(() => {
  if (!selectedVoice.value) return false
  if (selectedVoice.value.api_usable === false) return false
  return true
})
const selectedVoiceCanGenerate = computed(() => {
  if (!selectedVoiceApiUsable.value) return false
  return selectedVoiceHasQuotaForCharacters(speechCharCount.value)
})
const speechCharCount = computed(() => projectSpeechText.value?.length || 0)
const speechCharCountWarning = computed(() => {
  if (!speechCharCount.value) return ''
  if (speechCharCount.value > SPEECH_CHAR_HARD_LIMIT) {
    return `au-dessus de la limite ${SPEECH_CHAR_HARD_LIMIT} caracteres (Google TTS): coupe le texte ou bascule sur ElevenLabs.`
  }
  if (speechCharCount.value > SPEECH_CHAR_WARNING_THRESHOLD) {
    return `proche de la limite ${SPEECH_CHAR_HARD_LIMIT} caracteres.`
  }
  return ''
})
const selectedVoiceMeta = computed(() => {
  if (!selectedVoice.value) return ''
  if (selectedProviderId.value === 'google') {
    return voiceQuotaUsageLabel(selectedVoice.value)
  }
  return ''
  const labels = selectedVoice.value.labels || {}
  return [
    selectedVoice.value.matches_filter ? 'FR accent parisien' : 'compatible API',
    selectedVoice.value.is_custom ? 'ID personnalise' : '',
    labels.language ? labels.language.toUpperCase() : '',
    labels.accent === 'parisian' ? 'accent parisien' : labels.accent,
    selectedVoice.value.category,
  ].filter(Boolean).join(' · ')
})
const selectedVoiceWarning = computed(() => {
  if (!selectedVoice.value) return ''
  if (selectedProviderId.value === 'google') {
    if (selectedVoice.value.api_usable === false) {
      return selectedVoice.value.api_usable_reason || 'Seuil de quota Google atteint pour cette famille de voix.'
    }
    if (!selectedVoiceHasQuotaForCharacters(speechCharCount.value)) {
      return 'Ce projet depasserait le seuil de 90% du quota gratuit pour cette famille de voix.'
    }
    if (selectedVoice.value.quota_status === 'near_limit') {
      return 'Quota Google proche du seuil de grisage.'
    }
    return ''
  }
  return ''
})

function voiceOptionLabel(voice) {
  if (!voice) return ''
  if (voice.tier) {
    return [compactGoogleVoiceName(voice), voiceQuotaPercentLabel(voice)].filter(Boolean).join(' ')
  }
  // ElevenLabs voices
  const label = String(voice.name || voice.voice_id || '').trim()
  const parts = []
  if (voice.category) parts.push(voice.category)
  if (voice.api_usable === false) parts.push('non disponible')
  return parts.length ? `${label} - ${parts.join(', ')}` : label
}

function libraryVoiceOptionLabel(voice) {
  if (!voice) return ''
  const label = String(voice.name || voice.voice_id || '').trim()
  const star = favoriteVoiceIds.value.has(voice.voice_id) ? '★' : '☆'
  const labels = voice.labels || {}
  const details = [
    normalizeLibraryLabel(labels.gender),
    normalizeLibraryLabel(labels.age),
    normalizeLibraryLabel(voice.category),
  ].filter(Boolean)
  return details.length ? `${star} ${label} - ${details.join(', ')}` : `${star} ${label}`
}

function normalizeLibraryLabel(value) {
  return String(value || '').trim().replace(/_/g, ' ')
}

function normalizeElevenLabsFavoriteVoice(voice) {
  const voiceId = String(voice?.voice_id || '').trim()
  if (!voiceId) return null
  const labels = voice.labels && typeof voice.labels === 'object' ? voice.labels : {}
  return {
    voice_id: voiceId,
    name: String(voice.name || voiceId).trim(),
    category: String(voice.category || '').trim(),
    api_usable: voice.api_usable !== false,
    requires_subscription: Boolean(voice.requires_subscription),
    matches_filter: voice.matches_filter !== false,
    preview_url: String(voice.preview_url || '').trim(),
    is_custom: Boolean(voice.is_custom),
    is_library: Boolean(voice.is_library || voiceLibraryOptions.value.some((item) => item.voice_id === voiceId)),
    sort_priority: Number.isFinite(Number(voice.sort_priority)) ? Number(voice.sort_priority) : 50,
    labels: {
      language: String(labels.language || '').trim(),
      accent: String(labels.accent || '').trim(),
      gender: String(labels.gender || '').trim(),
      age: String(labels.age || '').trim(),
      descriptive: String(labels.descriptive || '').trim(),
      use_case: String(labels.use_case || '').trim(),
    },
  }
}

function normalizeStoredFavoriteVoices(value) {
  if (!Array.isArray(value)) return []
  const seen = new Set()
  const voices = []
  value.forEach((voice) => {
    const normalized = normalizeElevenLabsFavoriteVoice(voice)
    if (!normalized || seen.has(normalized.voice_id)) return
    seen.add(normalized.voice_id)
    voices.push(normalized)
  })
  return voices
}

function loadStoredElevenLabsFavoriteVoices() {
  if (typeof window === 'undefined') return []
  try {
    return normalizeStoredFavoriteVoices(JSON.parse(window.localStorage.getItem(ELEVENLABS_FAVORITE_VOICES_STORAGE_KEY) || '[]'))
  } catch (_) {
    return []
  }
}

function loadStoredElevenLabsHiddenFavoriteVoiceIds() {
  if (typeof window === 'undefined') return []
  try {
    const ids = JSON.parse(window.localStorage.getItem(ELEVENLABS_HIDDEN_FAVORITE_IDS_STORAGE_KEY) || '[]')
    if (!Array.isArray(ids)) return []
    return [...new Set(ids.map((id) => String(id || '').trim()).filter(Boolean))]
  } catch (_) {
    return []
  }
}

function persistElevenLabsFavoriteVoices() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(
      ELEVENLABS_FAVORITE_VOICES_STORAGE_KEY,
      JSON.stringify(normalizeStoredFavoriteVoices(elevenLabsFavoriteVoices.value)),
    )
    window.localStorage.setItem(
      ELEVENLABS_HIDDEN_FAVORITE_IDS_STORAGE_KEY,
      JSON.stringify([...new Set(elevenLabsHiddenFavoriteVoiceIds.value)]),
    )
  } catch (_) {
    // Local storage can be unavailable in private contexts.
  }
}

function buildElevenLabsFavoriteVoices(baseVoices = []) {
  const hiddenIds = new Set(elevenLabsHiddenFavoriteVoiceIds.value)
  const seen = new Set()
  const merged = []

  baseVoices.forEach((voice) => {
    const normalized = normalizeElevenLabsFavoriteVoice(voice)
    if (
      !normalized ||
      !ELEVENLABS_DEFAULT_FAVORITE_VOICE_IDS.includes(normalized.voice_id) ||
      hiddenIds.has(normalized.voice_id) ||
      seen.has(normalized.voice_id)
    ) {
      return
    }
    seen.add(normalized.voice_id)
    merged.push(normalized)
  })

  elevenLabsFavoriteVoices.value.forEach((voice) => {
    const normalized = normalizeElevenLabsFavoriteVoice(voice)
    if (!normalized || hiddenIds.has(normalized.voice_id) || seen.has(normalized.voice_id)) return
    seen.add(normalized.voice_id)
    merged.push(normalized)
  })

  return merged
}

function addElevenLabsFavoriteVoice(voice) {
  const normalized = normalizeElevenLabsFavoriteVoice(voice)
  if (!normalized) return false

  elevenLabsHiddenFavoriteVoiceIds.value = elevenLabsHiddenFavoriteVoiceIds.value.filter(
    (voiceId) => voiceId !== normalized.voice_id,
  )

  const nextFavorites = elevenLabsFavoriteVoices.value.filter(
    (item) => item.voice_id !== normalized.voice_id,
  )
  nextFavorites.push(normalized)
  elevenLabsFavoriteVoices.value = nextFavorites

  persistElevenLabsFavoriteVoices()
  selectedVoiceId.value = normalized.voice_id
  return true
}

function removeElevenLabsFavoriteVoice(voice) {
  const voiceId = String(voice?.voice_id || '').trim()
  if (!voiceId) return false

  elevenLabsFavoriteVoices.value = elevenLabsFavoriteVoices.value.filter(
    (item) => item.voice_id !== voiceId,
  )

  const isDefaultFavorite = ELEVENLABS_DEFAULT_FAVORITE_VOICE_IDS.includes(voiceId)
  if (isDefaultFavorite && !elevenLabsHiddenFavoriteVoiceIds.value.includes(voiceId)) {
    elevenLabsHiddenFavoriteVoiceIds.value = [...elevenLabsHiddenFavoriteVoiceIds.value, voiceId]
  }

  persistElevenLabsFavoriteVoices()
  if (selectedVoiceId.value === voiceId) {
    selectedVoiceId.value = ''
    selectVoiceForCurrentProvider()
  }
  return true
}

function compactGoogleVoiceName(voice) {
  const name = String(voice?.name || voice?.voice_id || '').trim()
  const match = name.match(/^(.+?)\s*\(([^-)]+)(?:\s*-\s*[^)]*)?\)$/)
  if (!match) return name
  const voiceName = match[1].trim()
  const model = match[2].trim()
  return model ? `${voiceName} (${model})` : voiceName
}

function voiceQuotaPercentLabel(voice) {
  const quota = voice?.quota || {}
  const percent = Number(quota.used_percent ?? voice?.quota_used_percent ?? 0)
  if (!Number.isFinite(percent)) return ''
  return `${Math.round(percent)}%`
}

function formatCreditCount(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '0'
  return Math.max(0, Math.round(number)).toLocaleString('fr-FR')
}

function formatPercent(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return '0'
  if (number >= 10) return Math.round(number).toLocaleString('fr-FR')
  return Number(number.toFixed(1)).toLocaleString('fr-FR')
}

function voiceQuotaUsageLabel(voice) {
  const quota = voice?.quota || {}
  const used = Number(quota.used_characters ?? voice?.quota_used_characters)
  const limit = Number(quota.free_monthly_character_limit ?? voice?.free_monthly_character_limit)
  if (!Number.isFinite(used) || !Number.isFinite(limit) || limit <= 0) return ''
  return `${Math.max(0, Math.round(used))}/${Math.max(0, Math.round(limit))}`
}

function selectedVoiceRemainingUntilDisable() {
  const voice = selectedVoice.value
  if (!voice || selectedProviderId.value !== 'google') return Number.POSITIVE_INFINITY
  const quota = voice.quota || {}
  return Number(
    quota.remaining_until_disable_characters ??
      voice.quota_remaining_until_disable_characters ??
      Number.POSITIVE_INFINITY,
  )
}

function selectedVoiceHasQuotaForCharacters(characterCount) {
  if (selectedProviderId.value !== 'google') return true
  if (!selectedVoiceApiUsable.value) return false
  const count = Number(characterCount || 0)
  const remaining = selectedVoiceRemainingUntilDisable()
  return !Number.isFinite(remaining) || count <= remaining
}

function clampNumber(value, fallback, min, max) {
  const number = Number(value)
  if (!Number.isFinite(number)) return fallback
  return Math.max(min, Math.min(max, number))
}

function normalizeElevenLabsSettings(value = {}) {
  const modelIds = ELEVENLABS_MODEL_OPTIONS.map((item) => item.value)
  const modelId = modelIds.includes(value.model_id)
    ? value.model_id
    : DEFAULT_ELEVENLABS_SETTINGS.model_id
  const normalizationModes = ['auto', 'on', 'off']
  const textNormalization = normalizationModes.includes(value.apply_text_normalization)
    ? value.apply_text_normalization
    : DEFAULT_ELEVENLABS_SETTINGS.apply_text_normalization

  return {
    model_id: modelId,
    stability: clampNumber(value.stability, DEFAULT_ELEVENLABS_SETTINGS.stability, 0, 1),
    similarity_boost: clampNumber(value.similarity_boost, DEFAULT_ELEVENLABS_SETTINGS.similarity_boost, 0, 1),
    style: clampNumber(value.style, DEFAULT_ELEVENLABS_SETTINGS.style, 0, 1),
    speed: clampNumber(value.speed, DEFAULT_ELEVENLABS_SETTINGS.speed, 0.5, 2),
    use_speaker_boost: typeof value.use_speaker_boost === 'boolean'
      ? value.use_speaker_boost
      : DEFAULT_ELEVENLABS_SETTINGS.use_speaker_boost,
    language_code: String(value.language_code || DEFAULT_ELEVENLABS_SETTINGS.language_code).trim() || 'fr',
    apply_text_normalization: textNormalization,
  }
}

function loadStoredElevenLabsSettings() {
  if (typeof window === 'undefined') return { ...DEFAULT_ELEVENLABS_SETTINGS }
  try {
    const raw = window.localStorage.getItem(ELEVENLABS_SETTINGS_STORAGE_KEY)
    if (!raw) return { ...DEFAULT_ELEVENLABS_SETTINGS }
    return normalizeElevenLabsSettings(JSON.parse(raw))
  } catch (_) {
    return { ...DEFAULT_ELEVENLABS_SETTINGS }
  }
}

function normalizeGoogleTtsSettings(value = {}) {
  const effectProfileIds = GOOGLE_EFFECTS_PROFILE_OPTIONS.map((item) => item.value)
  const effectsProfileId = effectProfileIds.includes(value.effects_profile_id)
    ? value.effects_profile_id
    : DEFAULT_GOOGLE_TTS_SETTINGS.effects_profile_id

  return {
    speaking_rate: clampNumber(value.speaking_rate, DEFAULT_GOOGLE_TTS_SETTINGS.speaking_rate, 0.25, 4),
    pitch: clampNumber(value.pitch, DEFAULT_GOOGLE_TTS_SETTINGS.pitch, -20, 20),
    volume_gain_db: clampNumber(value.volume_gain_db, DEFAULT_GOOGLE_TTS_SETTINGS.volume_gain_db, -96, 16),
    effects_profile_id: effectsProfileId,
  }
}

function loadStoredGoogleTtsSettings() {
  if (typeof window === 'undefined') return { ...DEFAULT_GOOGLE_TTS_SETTINGS }
  try {
    const raw = window.localStorage.getItem(GOOGLE_TTS_SETTINGS_STORAGE_KEY)
    if (!raw) return { ...DEFAULT_GOOGLE_TTS_SETTINGS }
    return normalizeGoogleTtsSettings(JSON.parse(raw))
  } catch (_) {
    return { ...DEFAULT_GOOGLE_TTS_SETTINGS }
  }
}

function persistElevenLabsSettings() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(
      ELEVENLABS_SETTINGS_STORAGE_KEY,
      JSON.stringify(normalizeElevenLabsSettings(elevenLabsSettings)),
    )
  } catch (_) {
    // Local storage can be unavailable in private contexts.
  }
}

function persistGoogleTtsSettings() {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(
      GOOGLE_TTS_SETTINGS_STORAGE_KEY,
      JSON.stringify(normalizeGoogleTtsSettings(googleTtsSettings)),
    )
  } catch (_) {
    // Local storage can be unavailable in private contexts.
  }
}

function resetElevenLabsSettings() {
  Object.assign(elevenLabsSettings, DEFAULT_ELEVENLABS_SETTINGS)
}

function resetGoogleTtsSettings() {
  Object.assign(googleTtsSettings, DEFAULT_GOOGLE_TTS_SETTINGS)
}

function getElevenLabsSettingsPayload() {
  return normalizeElevenLabsSettings(elevenLabsSettings)
}

function getGoogleTtsSettingsPayload() {
  const normalized = normalizeGoogleTtsSettings(googleTtsSettings)
  return {
    google_speaking_rate: normalized.speaking_rate,
    google_pitch: normalized.pitch,
    google_volume_gain_db: normalized.volume_gain_db,
    google_effects_profile_id: normalized.effects_profile_id,
  }
}

function buildSpeechGenerationPayload(extra = {}) {
  const payload = {
    ...extra,
    provider: selectedProviderId.value,
    voice_id: selectedVoiceId.value,
  }
  if (selectedProviderId.value === 'elevenlabs') {
    Object.assign(payload, getElevenLabsSettingsPayload())
  } else if (selectedProviderId.value === 'google') {
    Object.assign(payload, getGoogleTtsSettingsPayload())
  }
  return payload
}

watch(elevenLabsSettings, persistElevenLabsSettings, { deep: true })
watch(googleTtsSettings, persistGoogleTtsSettings, { deep: true })

const speechStatusLabel = computed(() => {
  if (!selectedProject.value?.id) return ''
  if (generatingSpeech.value) return 'Generation en cours'
  if (!projectSpeechText.value) return 'Texte voix indisponible'
  return `${generatedSlideSpeechCount.value}/${slidesSpeechCount.value} slides avec MP3`
})
const instagramCaptionText = computed(() => {
  const projectCaption = String(selectedProject.value?.instagram_caption || '').trim()
  if (projectCaption) return projectCaption
  return extractInstagramCaption(templateDraft.value)
})

function setFeedback(type, text) {
  feedback.type = type
  feedback.text = text
}

function clearDiagnostics() {
  Object.keys(diagnosticsBySlideId).forEach((key) => {
    delete diagnosticsBySlideId[key]
  })
}

function normalizePayload(payload) {
  if (payload && typeof payload === 'object' && payload.success && Object.prototype.hasOwnProperty.call(payload, 'data')) {
    return payload.data
  }
  return payload
}

function normalizeProjectsList(payload) {
  const normalized = normalizePayload(payload)
  if (Array.isArray(normalized)) return normalized
  if (Array.isArray(normalized?.results)) return normalized.results
  return []
}

function normalizeProject(payload) {
  const normalized = normalizePayload(payload)
  return normalized && typeof normalized === 'object' ? normalized : null
}

function upsertProjectSummary(project) {
  if (!project?.id) return

  const summary = {
    id: project.id,
    title: project.title,
    theme: project.theme,
    level: project.level,
    format_type: project.format_type,
    instagram_caption: project.instagram_caption,
    target_duration_seconds: project.target_duration_seconds,
    slide_count: Array.isArray(project.slides) ? project.slides.length : project.slide_count,
    status: project.status,
    speech_audio_url: project.speech_audio_url,
    speech_status: project.speech_status,
    speech_generated_at: project.speech_generated_at,
    video_file_url: project.video_file_url,
    video_status: project.video_status,
    video_generated_at: project.video_generated_at,
    created_at: project.created_at,
    updated_at: project.updated_at,
  }

  const idx = projects.value.findIndex((item) => Number(item.id) === Number(summary.id))
  if (idx === -1) {
    projects.value = [summary, ...projects.value]
  } else {
    projects.value.splice(idx, 1, summary)
  }

  projects.value = [...projects.value].sort((a, b) => new Date(b.updated_at || b.created_at || 0) - new Date(a.updated_at || a.created_at || 0))
}

function closeProjectForm() {
  projectFormOpen.value = false
  editingProject.value = null
}

function openCreateProjectForm() {
  editingProject.value = null
  selectedProject.value = null
  selectedProjectId.value = null
  selectedSlideId.value = null
  templateDraft.value = ''
  clearDiagnostics()
  projectFormOpen.value = true
}

function splitFilledLines(value) {
  return String(value || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
}

function extractInstagramCaption(value) {
  const lines = String(value || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n')
  const captionLines = []
  let capturing = false
  const captionStartPattern =
    /^(INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM|YOUTUBE_DESCRIPTION|DESCRIPTION_YOUTUBE|CAROUSEL_DESCRIPTION|DESCRIPTION_CAROUSEL|SOCIAL_DESCRIPTION|DESCRIPTION_SOCIAL)\s*:\s*(.*)$/i
  const captionEndPattern =
    /^END_(INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM|YOUTUBE_DESCRIPTION|DESCRIPTION_YOUTUBE|CAROUSEL_DESCRIPTION|DESCRIPTION_CAROUSEL|SOCIAL_DESCRIPTION|DESCRIPTION_SOCIAL)$/i

  for (const rawLine of lines) {
    const line = String(rawLine || '').trimEnd()
    const stripped = line.trim()
    const startMatch = stripped.match(captionStartPattern)

    if (capturing) {
      if (captionEndPattern.test(stripped)) {
        break
      }
      captionLines.push(line)
      continue
    }

    if (startMatch) {
      capturing = true
      if (startMatch[2]) captionLines.push(startMatch[2].trim())
    }
  }

  return captionLines.join('\n').trim()
}

function appendInstagramCaptionBlock(value, caption, formatType) {
  const safeCaption = String(caption || '').trim()
  if (!safeCaption) return value

  const body = String(value || '').trim()
  const normalizedFormat = normalizeFormatType(formatType)
  const tag = normalizedFormat === 'youtube'
    ? 'YOUTUBE_DESCRIPTION'
    : normalizedFormat === 'carousel'
      ? 'CAROUSEL_DESCRIPTION'
      : 'INSTAGRAM_DESCRIPTION'
  const captionBlock = `${tag}:\n${safeCaption}\nEND_${tag}`
  return body ? `${body}\n---\n${captionBlock}` : captionBlock
}

async function copyTextToClipboard(value) {
  const text = String(value || '')
  if (!text) return

  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text)
    return
  }

  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand('copy')
  textarea.remove()
}

async function copyInstagramCaption() {
  if (!instagramCaptionText.value) return

  try {
    await copyTextToClipboard(instagramCaptionText.value)
    setFeedback('success', `${studioFormatConfig.value.descriptionTitle} copiee.`)
  } catch (error) {
    setFeedback('error', `Impossible de copier: ${studioFormatConfig.value.descriptionTitle.toLowerCase()}.`)
  }
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

function slideSpeechText(slide) {
  const voice = normalizeSpeechLine(slide?.voice_script)
  if (voice) return voice

  return [slide?.title, slide?.screen_text]
    .map((part) => normalizeSpeechLine(part))
    .filter(Boolean)
    .join('. ')
}

function buildProjectSpeechText(project) {
  if (normalizeFormatType(project?.format_type) === 'carousel') return ''
  const slides = Array.isArray(project?.slides) ? [...project.slides] : []
  slides.sort((a, b) => Number(a.order || 0) - Number(b.order || 0) || Number(a.id || 0) - Number(b.id || 0))
  return slides
    .map((slide) => slideSpeechText(slide))
    .filter(Boolean)
    .join('\n\n')
}

function countSlidesWithSpeechText(project) {
  const slides = Array.isArray(project?.slides) ? project.slides : []
  return slides.filter((slide) => Boolean(slideSpeechText(slide))).length
}

function countGeneratedSlideSpeeches(project) {
  const slides = Array.isArray(project?.slides) ? project.slides : []
  return slides.filter((slide) => slide?.speech_audio_url).length
}

function splitSlideProjectPayload(payload) {
  if (!payload || typeof payload !== 'object') {
    return { slide: null, project: null }
  }

  const { project, ...slide } = payload
  return {
    slide: slide?.id ? slide : null,
    project: project?.id ? project : null,
  }
}

function applyProjectSummary(project) {
  if (!project?.id || !selectedProject.value?.id) return
  if (Number(project.id) !== Number(selectedProject.value.id)) return

  const currentSlides = Array.isArray(selectedProject.value.slides) ? selectedProject.value.slides : []
  selectedProject.value = {
    ...selectedProject.value,
    ...project,
    slides: currentSlides,
  }
  upsertProjectSummary(selectedProject.value)
}

function updateSelectedProjectSlide(updatedSlide) {
  const { slide, project } = splitSlideProjectPayload(updatedSlide)
  if (!slide?.id || !selectedProject.value?.slides) return

  const index = selectedProject.value.slides.findIndex((item) => Number(item.id) === Number(slide.id))
  if (index === -1) return

  selectedProject.value.slides.splice(index, 1, slide)
  if (project?.id) {
    applyProjectSummary(project)
  } else {
    selectedProject.value.updated_at = new Date().toISOString()
    upsertProjectSummary(selectedProject.value)
  }
}

function appendTemplateField(lines, label, value) {
  splitFilledLines(value).forEach((line) => {
    lines.push(`${label}: ${line}`)
  })
}

function slideVisualPrompt(slide) {
  const raw = String(slide?.layout_notes || '').trim()
  if (!raw) return ''
  try {
    const parsed = JSON.parse(raw)
    return String(parsed?.visual_prompt || '').trim()
  } catch (_) {
    return ''
  }
}

function serializeProjectSlides(project) {
  const slides = Array.isArray(project?.slides) ? [...project.slides] : []
  slides.sort((a, b) => Number(a.order || 0) - Number(b.order || 0) || Number(a.id || 0) - Number(b.id || 0))
  const isCarousel = normalizeFormatType(project?.format_type) === 'carousel'
  const includeVoice = !isCarousel

  const slidesText = slides
    .map((slide, index) => {
      const rawSlideType = normalizeFormatType(slide.slide_type) || 'katex'
      const slideType = isCarousel && ['cumulative_katex', 'result'].includes(rawSlideType)
        ? 'katex'
        : rawSlideType
      const lines = [`SLIDE ${slide.order || index + 1} | ${slideType}`]
      appendTemplateField(lines, 'TITLE', slide.title)
      appendTemplateField(lines, 'VISUEL', slideVisualPrompt(slide))
      appendTemplateField(lines, 'TEXT', slide.screen_text)
      appendTemplateField(lines, 'KATEX', slide.katex)
      if (includeVoice) {
        appendTemplateField(lines, 'VOICE', slide.voice_script)
      }
      return lines.join('\n')
    })
    .join('\n---\n')

  return appendInstagramCaptionBlock(slidesText, project?.instagram_caption, project?.format_type)
}

function scrollEditorIntoView() {
  requestAnimationFrame(() => {
    editorSectionRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

async function openEditProjectForm(project) {
  if (!project?.id) return
  closeProjectForm()

  const currentProjectAlreadyLoaded =
    Number(selectedProject.value?.id) === Number(project.id) &&
    Array.isArray(selectedProject.value?.slides)
  const projectToEdit = currentProjectAlreadyLoaded ? selectedProject.value : await selectProject(project.id)
  templateDraft.value = serializeProjectSlides(projectToEdit || selectedProject.value)

  if (!templateDraft.value) {
    setFeedback('info', `Ce projet n a pas encore de slides a modifier.`)
  }

  scrollEditorIntoView()
}

function extractErrorMessage(error, fallback) {
  const data = error?.response?.data || {}
  const fieldMessage = Object.values(data).find((value) => Array.isArray(value) && value.length)
  const apiMessage = data.detail || data.message || fieldMessage?.[0]
  return String(apiMessage || fallback)
}

function formatGeminiMoney(value) {
  const amount = Number(value || 0)
  const currency = geminiUsage.value?.display_currency || 'USD'
  if (!Number.isFinite(amount)) return currency === 'EUR' ? '0,0000 €' : '$0.0000'
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency,
    minimumFractionDigits: amount < 0.01 ? 4 : 2,
    maximumFractionDigits: amount < 0.01 ? 4 : 2,
  }).format(amount)
}

function modelLabel(model) {
  const label = model?.display_name || model?.id || ''
  const inputPrice = model?.input_price_per_1m_tokens
  const outputPrice = model?.output_price_per_1m_tokens
  if (!inputPrice || !outputPrice) return label
  return `${label} ($${inputPrice}/$${outputPrice})`
}

function applyGeminiOptions(payload) {
  const models = Array.isArray(payload?.models) ? payload.models : []
  geminiModels.value = models.length
    ? models
    : [{ id: DEFAULT_GEMINI_MODEL_ID, display_name: 'Gemini 2.5 Flash' }]

  const defaultModel = payload?.default_model_id || DEFAULT_GEMINI_MODEL_ID
  const hasSelectedModel = geminiModels.value.some((model) => model.id === selectedGeminiModelId.value)
  if (!hasSelectedModel) {
    const preferredModel =
      geminiModels.value.find((model) => model.id === defaultModel) ||
      geminiModels.value.find((model) => model.id === DEFAULT_GEMINI_MODEL_ID) ||
      geminiModels.value[0]
    selectedGeminiModelId.value = preferredModel?.id || DEFAULT_GEMINI_MODEL_ID
  }

  if (payload?.usage) {
    geminiUsage.value = {
      spent_usd: payload.usage.spent_usd || 0,
      budget_usd: payload.usage.budget_usd ?? null,
      remaining_usd: payload.usage.remaining_usd ?? null,
      display_currency: payload.usage.display_currency || 'USD',
      display_spent: payload.usage.display_spent || 0,
      display_budget: payload.usage.display_budget ?? null,
      display_remaining: payload.usage.display_remaining ?? null,
      eur_per_usd: payload.usage.eur_per_usd || 0.92,
      usage_count: payload.usage.usage_count || 0,
    }
  }
}

async function loadGeminiOptions() {
  if (!canManage.value) return

  loadingGeminiOptions.value = true
  geminiOptionsError.value = ''
  try {
    const response = await getGeminiOptions()
    applyGeminiOptions(response?.data)
  } catch (error) {
    geminiOptionsError.value = extractErrorMessage(error, 'Impossible de charger les modèles Gemini.')
  } finally {
    loadingGeminiOptions.value = false
  }
}

function buildCarouselGeminiPrompt(rawPrompt) {
  const userPrompt = String(rawPrompt || '').trim()
  const looksLikeExistingCarousel = /^\s*(SLIDE\s+\d+|FORMAT CARROUSEL|CAROUSEL_DESCRIPTION:)/im.test(userPrompt)
  const userBrief = userPrompt && !looksLikeExistingCarousel ? userPrompt : ''
  const project = selectedProject.value || {}
  const contextLines = [
    project.title ? `Titre du projet: ${project.title}` : '',
    project.theme ? `Theme: ${project.theme}` : '',
    project.level ? `Niveau: ${project.level}` : '',
  ].filter(Boolean)
  const carouselRules = [
    'Contraintes non négociables:',
    '- Fais un carrousel professionnel OptiTAB, pas un exercice de maths.',
    '- 7 slides exactement: 1 hook (cover) + 5 katex (contenu) + 1 cta (final).',
    '- TITLE court (3 à 7 mots), TEXT court (4 à 12 mots par ligne, max 4 lignes par slide).',
    '- Chaque slide doit contenir une ligne VISUEL décrivant une SCÈNE SANS TEXTE: tout mockup d écran doit avoir des éléments floutés/abstraits, aucune lettre lisible.',
    '- Laisse de l espace vide dans la composition du VISUEL pour que l overlay texte du template reste lisible.',
    '- N écris PAS dans TEXT: "Glisse", "Va sur optitab.net", "Visite optitab.net", "Abonne-toi", "optitab.net" — ces éléments sont ajoutés automatiquement par le template.',
    '- SLIDE 7 (cta): le TITLE est une grande promesse (ex: "Prêt à débloquer ton potentiel ?"), les TEXT sont 2-3 bénéfices concrets.',
  ].join('\n')

  return [
    CAROUSEL_FORMAT_TEMPLATE,
    carouselRules,
    userBrief ? `Brief utilisateur facultatif:\n${userBrief}` : '',
    contextLines.length ? `Contexte a utiliser:\n${contextLines.join('\n')}` : '',
    'Genere maintenant un carrousel original pret a copier pour OptiTAB.',
    'Reponds uniquement avec les blocs SLIDE et CAROUSEL_DESCRIPTION. Aucun markdown, aucune explication autour.',
  ].filter(Boolean).join('\n\n')
}

async function loadVoiceOptions() {
  if (!canManage.value) return

  loadingVoiceOptions.value = true
  voiceOptionsError.value = ''
  try {
    const response = await listReelVoices()
    const data = response?.data || {}
    const providerList = Array.isArray(data.providers) ? data.providers : []
    providers.value = providerList

    // Pick the best initial provider: previous selection if still available + configured,
    // else the backend-recommended default if configured, else first configured provider.
    const currentProviderStillOk = providerList.some(
      (p) => p.id === selectedProviderId.value && p.configured,
    )
    if (!currentProviderStillOk) {
      const preferred = data.default_provider || ''
      selectedProviderId.value =
        providerList.find((p) => p.id === preferred && p.configured)?.id ||
        providerList.find((p) => p.configured)?.id ||
        providerList[0]?.id ||
        ''
    }

    // Sync legacy voiceOptions to current provider voices for any code that still reads it.
    voiceOptions.value = currentProviderVoices.value

    selectVoiceForCurrentProvider()
    if (selectedProviderId.value === 'elevenlabs') {
      loadElevenLabsVoiceLibrary()
    } else {
      voiceLibraryOptions.value = []
      selectedLibraryVoiceId.value = ''
      voiceLibraryError.value = ''
    }

    if (!providerList.length) {
      voiceOptionsError.value = 'Aucun fournisseur de voix disponible.'
    } else if (!selectedProvider.value?.configured) {
      voiceOptionsError.value = selectedProvider.value?.error || 'Le fournisseur selectionne n est pas configure.'
    }
  } catch (error) {
    providers.value = []
    voiceOptions.value = []
    selectedVoiceId.value = ''
    voiceOptionsError.value = extractErrorMessage(error, 'Impossible de charger les voix.')
  } finally {
    loadingVoiceOptions.value = false
  }
}

async function loadElevenLabsVoiceLibrary() {
  if (!canManage.value || selectedProviderId.value !== 'elevenlabs') return

  const requestId = ++voiceLibraryRequestId
  const search = String(voiceLibrarySearch.value || '').trim()
  const gender = String(voiceLibraryFilters.gender || '').trim()
  const age = String(voiceLibraryFilters.age || '').trim()
  const quality = String(voiceLibraryFilters.quality || '').trim()
  loadingVoiceLibrary.value = true
  voiceLibraryError.value = ''
  selectedLibraryVoiceId.value = ''
  try {
    const response = await listReelVoiceLibrary({
      ...ELEVENLABS_LIBRARY_DEFAULT_FILTERS,
      ...(search ? { search } : {}),
      ...(gender ? { gender } : {}),
      ...(age ? { age } : {}),
      ...(quality === 'high_quality' ? { category: 'high_quality' } : {}),
      ...(quality === 'featured' ? { featured: true } : {}),
    })
    if (requestId !== voiceLibraryRequestId) return
    const data = response?.data || {}
    const voices = Array.isArray(data.voices) ? data.voices : []
    voiceLibraryOptions.value = voices
    if (!voices.length) {
      const hasFilters = Boolean(search || gender || age || quality)
      voiceLibraryError.value = hasFilters
        ? 'Aucune voix ElevenLabs trouvee avec ces filtres.'
        : 'Aucune voix ElevenLabs trouvee avec French / parisian.'
    }
  } catch (error) {
    if (requestId !== voiceLibraryRequestId) return
    voiceLibraryOptions.value = []
    voiceLibraryError.value = extractErrorMessage(error, 'Impossible de charger la Voice Library ElevenLabs.')
  } finally {
    if (requestId === voiceLibraryRequestId) {
      loadingVoiceLibrary.value = false
    }
  }
}

function scheduleVoiceLibrarySearch() {
  if (voiceLibrarySearchTimer) {
    clearTimeout(voiceLibrarySearchTimer)
  }
  voiceLibrarySearchTimer = setTimeout(() => {
    voiceLibrarySearchTimer = 0
    loadElevenLabsVoiceLibrary()
  }, ELEVENLABS_LIBRARY_SEARCH_DEBOUNCE_MS)
}

function selectVoiceForCurrentProvider() {
  const provider = selectedProvider.value
  if (!provider) {
    selectedVoiceId.value = ''
    return
  }
  const voices = provider.voices || []
  const currentExists = voices.some(
    (v) => v.voice_id === selectedVoiceId.value && v.api_usable !== false,
  )
  if (currentExists) return

  const defaultId = provider.default_voice_id || ''
  selectedVoiceId.value =
    voices.find((v) => v.voice_id === defaultId && v.api_usable !== false)?.voice_id ||
    voices.find((v) => v.api_usable !== false)?.voice_id ||
    ''
}

function resetTestAudio() {
  if (testAudioUrl.value) {
    if (String(testAudioUrl.value).startsWith('blob:')) {
      window.URL.revokeObjectURL(testAudioUrl.value)
    }
    testAudioUrl.value = ''
  }
}

function onProviderChange() {
  resetTestAudio()
  selectVoiceForCurrentProvider()
  voiceOptions.value = currentProviderVoices.value
  if (selectedProviderId.value === 'elevenlabs') {
    loadElevenLabsVoiceLibrary()
  } else {
    voiceLibraryOptions.value = []
    selectedLibraryVoiceId.value = ''
    voiceLibraryError.value = ''
  }
}

function onFavoriteVoiceChange() {
  selectedLibraryVoiceId.value = ''
  resetTestAudio()
}

function onLibraryVoiceChange() {
  const voice = selectedLibraryVoice.value
  resetTestAudio()
  if (!voice) return

  const previewUrl = String(voice.preview_url || '').trim()
  if (!previewUrl) {
    setFeedback('error', 'Aucun apercu gratuit ElevenLabs disponible pour cette voix library.')
    return
  }

  testAudioUrl.value = previewUrl
  setFeedback('success', `Apercu gratuit ElevenLabs charge: ${voice.name || voice.voice_id}.`)
}

function toggleSelectedLibraryVoiceFavorite() {
  const voice = selectedLibraryVoice.value
  if (!voice) return

  if (selectedLibraryVoiceIsFavorite.value) {
    removeElevenLabsFavoriteVoice(voice)
    setFeedback('success', `${voice.name || voice.voice_id} retiree des favoris.`)
    return
  }

  addElevenLabsFavoriteVoice(voice)
  setFeedback('success', `${voice.name || voice.voice_id} ajoutee aux favoris.`)
}

async function handleTestVoice() {
  if (selectedProviderId.value === 'elevenlabs') {
    const previewVoice = selectedLibraryVoice.value || selectedVoice.value
    if (!previewVoice) return

    const elevenLabsPreviewUrl = String(previewVoice.preview_url || '').trim()
    if (!elevenLabsPreviewUrl) {
      setFeedback('error', 'Aucun apercu gratuit ElevenLabs disponible pour cette voix.')
      return
    }

    resetTestAudio()
    testAudioUrl.value = elevenLabsPreviewUrl
    setFeedback('success', 'Apercu gratuit ElevenLabs charge pour cette voix.')
    return
  }

  if (!selectedProviderId.value || !selectedVoiceId.value) return
  if (!selectedVoiceApiUsable.value) return

  // Build a short preview: take the first sentence of the project speech text,
  // or fall back to a generic French sample.
  const fullText = projectSpeechText.value || ''
  const firstSentence = fullText.split(/[.!?\n]/).map((s) => s.trim()).find(Boolean) || ''
  const previewText = (firstSentence || 'Bonjour, ceci est un test de voix OptiTAB.').slice(0, 240)
  if (!selectedVoiceHasQuotaForCharacters(previewText.length)) {
    setFeedback('error', 'Cette voix est trop proche du seuil de quota Google pour generer un apercu.')
    return
  }

  testingVoice.value = true
  try {
    const response = await testReelTTSVoice(buildSpeechGenerationPayload({ text: previewText }))

    resetTestAudio()
    const blob = response?.data instanceof Blob ? response.data : new Blob([response?.data], { type: 'audio/mpeg' })
    testAudioUrl.value = window.URL.createObjectURL(blob)

    const cached = response?.headers?.['x-tts-cached'] === '1'
    const chars = response?.headers?.['x-tts-character-count'] || previewText.length
    setFeedback('success', `Apercu voix genere (${chars} caracteres${cached ? ', depuis le cache' : ''}).`)
    if (!cached) loadVoiceOptions()
  } catch (error) {
    const blobMessage = await readBlobErrorMessage(error)
    setFeedback('error', blobMessage || extractErrorMessage(error, 'Impossible de generer l apercu voix.'))
  } finally {
    testingVoice.value = false
  }
}

async function readBlobErrorMessage(error) {
  const data = error?.response?.data
  if (!(data instanceof Blob)) return ''
  try {
    const text = await data.text()
    if (!text) return ''
    try {
      const parsed = JSON.parse(text)
      return parsed?.detail || parsed?.message || ''
    } catch (_) {
      return text.slice(0, 200)
    }
  } catch (_) {
    return ''
  }
}

async function loadProjects() {
  if (!canManage.value) return

  loadingProjects.value = true
  try {
    const response = await listReelProjects()
    projects.value = normalizeProjectsList(response?.data)

    if (!projects.value.length) {
      selectedProject.value = null
      selectedProjectId.value = null
      selectedSlideId.value = null
      return
    }

    const selectedStillExists = projects.value.some((project) => Number(project.id) === Number(selectedProjectId.value))
    if (selectedStillExists) {
      await selectProject(selectedProjectId.value)
    } else {
      selectedProject.value = null
      selectedProjectId.value = null
      selectedSlideId.value = null
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de charger les projets Reel Studio.'))
  } finally {
    loadingProjects.value = false
  }
}

async function handleSubmitProject(payload) {
  if (!canManage.value) return

  const safeTitle = String(payload?.title || '').trim()
  if (!safeTitle) {
    setFeedback('error', `Ajoute un titre avant de creer ${studioFormatConfig.value.entityWithArticle}.`)
    return
  }

  savingProject.value = true
  try {
    const projectId = editingProject.value?.id
    const projectPayload = {
      ...payload,
      title: safeTitle,
    }
    const response = projectId
      ? await updateReelProject(projectId, projectPayload)
      : await createReelProject({ ...projectPayload, slide_count: 0, format_type: studioFormat.value })
    const project = normalizeProject(response?.data)

    if (project?.id) {
      upsertProjectSummary(project)
      selectedProject.value = project
      selectedProjectId.value = Number(project.id)
      selectedSlideId.value = project.slides?.[0]?.id || null
      templateDraft.value = serializeProjectSlides(project)
      clearDiagnostics()
      closeProjectForm()
      setFeedback('success', projectId ? 'Projet mis a jour.' : 'Projet cree en base.')
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, `Impossible de sauvegarder ${studioFormatConfig.value.entityWithArticle}.`))
  } finally {
    savingProject.value = false
  }
}

async function handleDeleteProject(project) {
  if (!project?.id || !canManage.value) return
  if (!window.confirm(`Supprimer ${studioFormatConfig.value.entityWithArticle} "${project.title || project.id}" et toutes ses slides ?`)) return

  savingProject.value = true
  try {
    await deleteReelProject(project.id)
    projects.value = projects.value.filter((item) => Number(item.id) !== Number(project.id))

    if (Number(selectedProjectId.value) === Number(project.id)) {
      selectedProject.value = null
      selectedProjectId.value = null
      selectedSlideId.value = null
      templateDraft.value = ''
      clearDiagnostics()
    }

    if (editingProject.value?.id && Number(editingProject.value.id) === Number(project.id)) {
      closeProjectForm()
    }

    if (!projects.value.length) {
      openCreateProjectForm()
    }

    setFeedback('success', 'Projet supprime.')
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, `Impossible de supprimer ${studioFormatConfig.value.entityWithArticle}.`))
  } finally {
    savingProject.value = false
  }
}

async function selectProject(projectId) {
  if (!projectId || !canManage.value) return null

  selectedProjectId.value = Number(projectId)
  loadingProjectDetail.value = true
  const requestId = ++detailRequestId

  try {
    const response = await getReelProject(projectId)
    if (requestId !== detailRequestId) return null

    const project = normalizeProject(response?.data)
    selectedProject.value = project
    selectedSlideId.value = project?.slides?.[0]?.id || null
    clearDiagnostics()
    upsertProjectSummary(project)
    return project
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de charger le projet sélectionné.'))
    return null
  } finally {
    if (requestId === detailRequestId) {
      loadingProjectDetail.value = false
    }
  }
}

function handleGenerateCarouselWithGemini(payload) {
  if (!selectedProject.value?.id || !isCarouselProject.value) return
  pendingGeneratePayload.value = payload || null
  geminiImageDialogMode.value = 'generate'
  geminiImageDialogOpen.value = true
}

function handleRegenerateCarouselImages() {
  if (!selectedProject.value?.id || !canRegenerateCarouselImages.value) return
  pendingGeneratePayload.value = null
  geminiImageDialogMode.value = 'regenerate'
  geminiImageDialogOpen.value = true
}

function closeGeminiImageDialog() {
  geminiImageDialogOpen.value = false
  pendingGeneratePayload.value = null
}

function handleGeminiImageDialogConfirm({ carouselType, strategy, useReferences } = {}) {
  const safeType = carouselType || 'marketing'
  const safeStrategy = strategy || 'hook_cta'
  const safeUseReferences = useReferences !== false
  lastGeminiCarouselType.value = safeType
  lastGeminiSlideStrategy.value = safeStrategy
  lastGeminiUseReferences.value = safeUseReferences
  geminiImageDialogOpen.value = false
  if (geminiImageDialogMode.value === 'regenerate') {
    runRegenerateCarouselImages({ carouselType: safeType, strategy: safeStrategy, useReferences: safeUseReferences })
  } else {
    runGenerateCarouselWithGemini({
      payload: pendingGeneratePayload.value,
      carouselType: safeType,
      strategy: safeStrategy,
      useReferences: safeUseReferences,
    })
    pendingGeneratePayload.value = null
  }
}

async function runGenerateCarouselWithGemini({ payload, carouselType, strategy, useReferences }) {
  if (!selectedProject.value?.id || !isCarouselProject.value) return

  generatingCarouselGemini.value = true
  try {
    const response = await generateCarouselWithGemini(selectedProject.value.id, {
      prompt: buildCarouselGeminiPrompt(payload?.prompt),
      model_id: selectedGeminiModelId.value || DEFAULT_GEMINI_MODEL_ID,
      max_chars_per_line: 38,
      generate_images: strategy !== 'none',
      slide_image_strategy: strategy,
      carousel_type: carouselType,
      use_site_references: useReferences !== false,
    })
    const updatedProject = normalizeProject(response?.data?.project)
    const generatedTemplateText = String(response?.data?.template_text || '').trim()
    lastGeminiUsage.value = response?.data?.gemini_usage || null
    if (response?.data?.gemini_summary) {
      geminiUsage.value = response.data.gemini_summary
    }

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || null
      templateDraft.value = generatedTemplateText || serializeProjectSlides(updatedProject)
      clearDiagnostics()
      upsertProjectSummary(updatedProject)
      const imageGen = response?.data?.image_generation || {}
      const imageCount = Array.isArray(imageGen.generated) ? imageGen.generated.length : 0
      const errorsList = Array.isArray(imageGen.errors) ? imageGen.errors : []
      const imageErrors = errorsList.length
      const slidesCount = updatedProject.slides?.length || 0
      if (imageErrors && !imageCount) {
        const firstDetail = String(errorsList[0]?.detail || '').slice(0, 220)
        setFeedback(
          'error',
          `Carrousel généré (${slidesCount} slides) mais AUCUNE image Gemini n'a pu être créée. `
          + `${imageErrors} erreur(s). Détail: ${firstDetail || 'inconnu'}`,
        )
      } else if (imageErrors) {
        const firstDetail = String(errorsList[0]?.detail || '').slice(0, 200)
        setFeedback(
          'warning',
          `Carrousel généré (${slidesCount} slides). ${imageCount} images OK, ${imageErrors} en erreur. `
          + `Premier détail: ${firstDetail || 'inconnu'}`,
        )
      } else {
        setFeedback(
          'success',
          `Carrousel généré avec Gemini (${slidesCount} slides). ${imageCount} images générées.`,
        )
      }
    }
  } catch (error) {
    const generatedTemplateText = String(error?.response?.data?.template_text || '').trim()
    if (generatedTemplateText) {
      templateDraft.value = generatedTemplateText
    }
    setFeedback('error', extractErrorMessage(error, 'Impossible de générer le carrousel avec Gemini.'))
  } finally {
    generatingCarouselGemini.value = false
  }
}

async function runRegenerateCarouselImages({ carouselType, strategy, useReferences } = {}) {
  if (!selectedProject.value?.id || !canRegenerateCarouselImages.value) return
  if (strategy === 'none') {
    setFeedback('info', 'Aucune image à générer (option "Aucune image" sélectionnée).')
    return
  }

  regeneratingCarouselImages.value = true
  try {
    const response = await regenerateCarouselImages(selectedProject.value.id, {
      slide_image_strategy: strategy || 'hook_cta',
      carousel_type: carouselType || 'marketing',
      use_site_references: useReferences !== false,
    })
    const updatedProject = normalizeProject(response?.data?.project)
    if (response?.data?.gemini_summary) {
      geminiUsage.value = response.data.gemini_summary
    }

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      upsertProjectSummary(updatedProject)
      const imageGen = response?.data?.image_generation || {}
      const imageCount = Array.isArray(imageGen.generated) ? imageGen.generated.length : 0
      const errorsList = Array.isArray(imageGen.errors) ? imageGen.errors : []
      const imageErrors = errorsList.length
      if (imageErrors && !imageCount) {
        const firstDetail = String(errorsList[0]?.detail || '').slice(0, 220)
        setFeedback(
          'error',
          `AUCUNE image Gemini n'a pu être créée. ${imageErrors} erreur(s). Détail: ${firstDetail || 'inconnu'}`,
        )
      } else if (imageErrors) {
        const firstDetail = String(errorsList[0]?.detail || '').slice(0, 200)
        setFeedback(
          'warning',
          `${imageCount} images OK, ${imageErrors} en erreur. Premier détail: ${firstDetail || 'inconnu'}`,
        )
      } else {
        setFeedback('success', `${imageCount} images Gemini régénérées.`)
      }
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de régénérer les images Gemini.'))
  } finally {
    regeneratingCarouselImages.value = false
  }
}

async function handleGenerateSlideImage(payload) {
  const slideId = Number(payload?.slideId || 0)
  if (!slideId || !selectedProject.value?.id) {
    payload?.onDone?.({ error: 'Aucune slide sélectionnée.' })
    return
  }

  generatingImageSlideId.value = slideId
  try {
    const response = await generateReelSlideImage(slideId, {
      prompt: payload?.prompt || '',
      carousel_type: payload?.carouselType || 'marketing',
      model_id: selectedGeminiModelId.value || DEFAULT_GEMINI_MODEL_ID,
      use_site_references: payload?.useReferences !== false,
    })

    const updatedProject = normalizeProject(response?.data?.project)
    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      upsertProjectSummary(updatedProject)
    }
    if (response?.data?.gemini_summary) {
      geminiUsage.value = response.data.gemini_summary
    }
    payload?.onDone?.({ ok: true })
  } catch (error) {
    const message = extractErrorMessage(error, 'Impossible de générer l\'image Gemini.')
    setFeedback('error', message)
    payload?.onDone?.({ error: message })
  } finally {
    generatingImageSlideId.value = null
  }
}

async function handleClearSlideImage(payload) {
  const slideId = Number(payload?.slideId || 0)
  if (!slideId || !selectedProject.value?.id) {
    payload?.onDone?.({ error: 'Aucune slide sélectionnée.' })
    return
  }

  try {
    const response = await clearReelSlideImage(slideId)
    const updatedProject = normalizeProject(response?.data?.project)
    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      upsertProjectSummary(updatedProject)
    }
    payload?.onDone?.({ ok: true })
  } catch (error) {
    const message = extractErrorMessage(error, 'Impossible de supprimer l\'image.')
    setFeedback('error', message)
    payload?.onDone?.({ error: message })
  }
}

async function handleGenerateFromTemplate(payload) {
  if (!selectedProject.value?.id) return

  generatingTemplate.value = true
  const submittedInstagramCaption = extractInstagramCaption(payload?.template_text)
  try {
    const response = await generateSlidesFromTemplate(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data)

    if (updatedProject?.id) {
      if (submittedInstagramCaption && !String(updatedProject.instagram_caption || '').trim()) {
        updatedProject.instagram_caption = submittedInstagramCaption
      }
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      clearDiagnostics()
      upsertProjectSummary(updatedProject)
      setFeedback('success', `Slides générées depuis template (${updatedProject.slides?.length || 0} slides).`)
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de générer les slides depuis le template.'))
  } finally {
    generatingTemplate.value = false
  }
}

async function handleSaveTemplate(payload) {
  if (!selectedProject.value?.id) return

  savingTemplate.value = true
  const submittedInstagramCaption = extractInstagramCaption(payload?.template_text)
  try {
    const response = await saveReelTemplate(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data)

    if (updatedProject?.id) {
      if (submittedInstagramCaption && !String(updatedProject.instagram_caption || '').trim()) {
        updatedProject.instagram_caption = submittedInstagramCaption
      }
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || selectedSlideId.value || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      clearDiagnostics()
      upsertProjectSummary(updatedProject)
      const readyCount = countGeneratedSlideSpeeches(updatedProject)
      const totalSlides = updatedProject.slides?.length || 0
      const voicePart = readyCount ? ` Voix conservee sur ${readyCount}/${totalSlides} slide${totalSlides > 1 ? 's' : ''}.` : ''
      setFeedback('success', `Projet sauvegarde (${totalSlides} slides).${voicePart}`)
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder le template.'))
  } finally {
    savingTemplate.value = false
  }
}

async function handleGenerateSpeech() {
  if (!selectedProject.value?.id || !canGenerateSpeech.value || !selectedVoiceCanGenerate.value) return

  generatingSpeech.value = true
  try {
    const response = await generateReelSlideSpeeches(
      selectedProject.value.id,
      buildSpeechGenerationPayload(),
    )
    const updatedProject = normalizeProject(response?.data?.project || response?.data)

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      selectedSlideId.value = updatedProject.slides?.[0]?.id || selectedSlideId.value || null
      templateDraft.value = serializeProjectSlides(updatedProject)
      upsertProjectSummary(updatedProject)
      const speechMeta = response?.data?.speech || {}
      const count = speechMeta.generated_count ?? countGeneratedSlideSpeeches(updatedProject)
      const charCount = Number(speechMeta.character_count || 0)
      const cachedCount = Number(speechMeta.cached_count || 0)
      const provider = speechMeta.provider || selectedProviderId.value
      const parts = [`Voix par slide generees (${count} MP3, ${provider})`]
      if (charCount) parts.push(`${charCount.toLocaleString('fr-FR')} caracteres`)
      if (cachedCount) parts.push(`${cachedCount} reutilisees du cache`)
      setFeedback('success', parts.join(' · ') + '.')
      loadVoiceOptions()
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de generer les voix par slide.'))
  } finally {
    generatingSpeech.value = false
  }
}

async function handleGenerateSlideSpeech(payload) {
  const slideId = payload && typeof payload === 'object' ? payload.id : payload
  const requestedText = payload && typeof payload === 'object' ? String(payload.text || '').trim() : ''
  const requestedVoiceScript = payload && typeof payload === 'object' ? String(payload.voice_script || '').trim() : ''
  const shouldSaveVoiceScript = Boolean(payload && typeof payload === 'object' && payload.save_voice_script)

  if (!slideId || !selectedProject.value?.slides) return
  if (!selectedVoiceApiUsable.value) {
    setFeedback('error', 'Selectionne une voix compatible API.')
    return
  }
  let slide = selectedProject.value.slides.find((item) => Number(item.id) === Number(slideId))
  const speechText = requestedText || slideSpeechText(slide)
  if (!speechText) {
    setFeedback('error', 'Aucun texte vocal disponible pour cette slide.')
    return
  }
  if (!selectedVoiceHasQuotaForCharacters(speechText.length)) {
    setFeedback('error', 'Cette slide depasserait le seuil de 90% du quota gratuit Google pour cette voix.')
    return
  }

  generatingSpeechSlideId.value = Number(slideId)
  try {
    if (shouldSaveVoiceScript && requestedVoiceScript !== String(slide?.voice_script || '').trim()) {
      const saveResponse = await updateReelSlide(slideId, { voice_script: requestedVoiceScript })
      const savedSlide = normalizeProject(saveResponse?.data)
      if (savedSlide?.id) {
        updateSelectedProjectSlide(savedSlide)
        templateDraft.value = serializeProjectSlides(selectedProject.value)
        slide = savedSlide
      }
    }

    const response = await generateReelSlideSpeech(
      slideId,
      buildSpeechGenerationPayload({ text: speechText }),
    )
    const updatedSlide = normalizeProject(response?.data)

    if (updatedSlide?.id) {
      updateSelectedProjectSlide(updatedSlide)
      setFeedback('success', `Voix de la slide ${updatedSlide.order || ''} generee.`.trim())
      loadVoiceOptions()
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de generer la voix de cette slide.'))
  } finally {
    generatingSpeechSlideId.value = null
  }
}

function buildVideoFilename(project) {
  const fallbackSlug = FORMAT_CONFIGS[normalizeFormatType(project?.format_type)]?.entityDefaultSlug || 'optitab-reel'
  const safeTitle = String(project?.title || fallbackSlug)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase() || fallbackSlug
  return `${safeTitle}.mp4`
}

function filenameFromContentDisposition(value) {
  const disposition = String(value || '')
  const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i)
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1])
    } catch (_) {
      return utf8Match[1]
    }
  }

  const quotedMatch = disposition.match(/filename="?([^";]+)"?/i)
  return quotedMatch?.[1] || ''
}

function triggerBlobDownload(blob, filename) {
  if (!blob) return
  const objectUrl = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = objectUrl
  link.download = filename
  link.style.display = 'none'
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.setTimeout(() => window.URL.revokeObjectURL(objectUrl), 60000)
}

async function downloadExportedVideo(project, fallbackUrl) {
  const filename = buildVideoFilename(project)

  try {
    const response = await downloadReelVideo(project.id)
    const headerFilename = filenameFromContentDisposition(response?.headers?.['content-disposition'])
    triggerBlobDownload(response?.data, headerFilename || filename)
    return
  } catch (error) {
    if (!fallbackUrl) throw error
  }

  const fallbackOrigin = new URL(fallbackUrl, window.location.href).origin
  const response = await fetch(fallbackUrl, {
    credentials: fallbackOrigin === window.location.origin ? 'same-origin' : 'omit',
  })
  if (!response.ok) {
    throw new Error(`Telechargement MP4 impossible (${response.status}).`)
  }
  const blob = await response.blob()
  triggerBlobDownload(blob, filename)
}

async function handleExportVideo(payload) {
  if (!selectedProject.value?.id || !payload?.frames?.length) return

  exportingVideo.value = true
  try {
    const response = await exportReelVideo(selectedProject.value.id, payload)
    const updatedProject = normalizeProject(response?.data?.project || response?.data)
    const videoUrl = response?.data?.video?.url || updatedProject?.video_file_url

    if (updatedProject?.id) {
      selectedProject.value = updatedProject
      templateDraft.value = serializeProjectSlides(updatedProject)
      upsertProjectSummary(updatedProject)
    }

    if (videoUrl && (updatedProject?.id || selectedProject.value?.id)) {
      await downloadExportedVideo(updatedProject || selectedProject.value, videoUrl)
      setFeedback('success', 'Video MP4 exportee et telechargement lance.')
    } else {
      setFeedback('success', 'Video MP4 generee.')
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible d exporter la video MP4.'))
  } finally {
    exportingVideo.value = false
  }
}

function handleSlideDiagnostic(diagnostic) {
  if (!diagnostic?.slideId) return
  diagnosticsBySlideId[diagnostic.slideId] = diagnostic
}

async function handleSaveSlide(payload) {
  if (!payload?.id || !selectedProject.value) return

  savingSlide.value = true
  try {
    const diagnostic = diagnosticsBySlideId[payload.id]
    const patchData = {
      title: payload.title,
      screen_text: payload.screen_text,
      katex: payload.katex,
      voice_script: payload.voice_script,
      title_scale: payload.title_scale,
      screen_text_scale: payload.screen_text_scale,
      katex_scale: payload.katex_scale,
      katex_inline_with_previous: payload.katex_inline_with_previous,
      katex_inline_separator: payload.katex_inline_separator,
      katex_inline_offset_percent: payload.katex_inline_offset_percent,
      katex_inline_vertical_offset_em: payload.katex_inline_vertical_offset_em,
      katex_cumulative_gap_em: payload.katex_cumulative_gap_em,
      katex_reset_cumulative: payload.katex_reset_cumulative,
      katex_reset_keep_previous_line: payload.katex_reset_keep_previous_line,
      katex_reveal_with_speech: payload.katex_reveal_with_speech,
      katex_drop_previous_line: payload.katex_drop_previous_line,
    }

    if (diagnostic?.status) {
      patchData.layout_status = diagnostic.status
      patchData.layout_notes = diagnostic.notes || ''
    }

    const response = await updateReelSlide(payload.id, patchData)
    const updatedSlide = normalizeProject(response?.data)

    if (updatedSlide?.id) {
      updateSelectedProjectSlide(updatedSlide)
      templateDraft.value = serializeProjectSlides(selectedProject.value)
      setFeedback('success', 'Slide mise à jour.')
    }
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder la slide.'))
  } finally {
    savingSlide.value = false
  }
}

async function handleUpdatePronunciationOverrides(nextOverrides) {
  if (!selectedProject.value?.id) return

  const cleanList = Array.isArray(nextOverrides)
    ? nextOverrides
        .filter((entry) => entry && typeof entry === 'object')
        .map((entry) => ({
          word: String(entry.word || '').trim(),
          pronunciation: String(entry.pronunciation || '').trim(),
        }))
        .filter((entry) => entry.word && entry.pronunciation)
    : []

  const previousOverrides = Array.isArray(selectedProject.value.pronunciation_overrides)
    ? [...selectedProject.value.pronunciation_overrides]
    : []
  selectedProject.value.pronunciation_overrides = cleanList

  try {
    const response = await updateReelProject(selectedProject.value.id, {
      pronunciation_overrides: cleanList,
    })
    const updatedProject = normalizeProject(response?.data)
    if (updatedProject?.id) {
      selectedProject.value.pronunciation_overrides = updatedProject.pronunciation_overrides || []
      selectedProject.value.updated_at = updatedProject.updated_at || selectedProject.value.updated_at
      upsertProjectSummary(selectedProject.value)
    }
    setFeedback('success', 'Prononciations mises à jour.')
  } catch (error) {
    selectedProject.value.pronunciation_overrides = previousOverrides
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder les prononciations.'))
  }
}

async function handleUpdatePronunciationOverridesByVoice({ voiceId, overrides }) {
  if (!selectedProject.value?.id || !voiceId) return

  const current = selectedProject.value.pronunciation_overrides_by_voice || {}
  const previous = { ...current }

  const cleanList = Array.isArray(overrides)
    ? overrides
        .filter((entry) => entry && typeof entry === 'object')
        .map((entry) => ({
          word: String(entry.word || '').trim(),
          pronunciation: String(entry.pronunciation || '').trim(),
          language: String(entry.language || 'fr').trim(),
        }))
        .filter((entry) => entry.word && entry.pronunciation)
    : []

  const next = { ...current }
  if (cleanList.length > 0) {
    next[voiceId] = cleanList
  } else {
    delete next[voiceId]
  }

  selectedProject.value.pronunciation_overrides_by_voice = next

  try {
    const response = await updateReelProject(selectedProject.value.id, {
      pronunciation_overrides_by_voice: next,
    })
    const updatedProject = normalizeProject(response?.data)
    if (updatedProject?.id) {
      selectedProject.value.pronunciation_overrides_by_voice = updatedProject.pronunciation_overrides_by_voice || {}
      selectedProject.value.updated_at = updatedProject.updated_at || selectedProject.value.updated_at
      upsertProjectSummary(selectedProject.value)
    }
    setFeedback('success', 'Prononciations de la voix mises à jour.')
  } catch (error) {
    selectedProject.value.pronunciation_overrides_by_voice = previous
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder les prononciations.'))
  }
}

async function handlePatchProjectInline(payload) {
  if (!payload?.id || !selectedProject.value) return
  if (Number(payload.id) !== Number(selectedProject.value.id)) return
  const patch = payload.patch && typeof payload.patch === 'object' ? payload.patch : {}
  if (!Object.keys(patch).length) return

  const previous = { ...selectedProject.value }
  Object.assign(selectedProject.value, patch)

  try {
    const response = await updateReelProject(selectedProject.value.id, patch)
    const updatedProject = normalizeProject(response?.data)
    if (updatedProject?.id) {
      Object.assign(selectedProject.value, updatedProject)
      upsertProjectSummary(selectedProject.value)
    }
  } catch (error) {
    Object.assign(selectedProject.value, previous)
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder la modification.'))
  }
}

async function handlePatchSlide(payload) {
  if (!payload?.id || !selectedProject.value) return

  const patchData = payload.patch && typeof payload.patch === 'object' ? payload.patch : {}
  const index = selectedProject.value.slides.findIndex((slide) => Number(slide.id) === Number(payload.id))
  if (index === -1 || !Object.keys(patchData).length) return

  const previousSlide = { ...selectedProject.value.slides[index] }
  const nextSlide = { ...previousSlide, ...patchData }
  const speechTextWillChange = slideSpeechText(nextSlide) !== slideSpeechText(previousSlide)
  const optimisticPatch = speechTextWillChange
    ? {
        ...patchData,
        speech_audio: null,
        speech_audio_url: null,
        speech_text: '',
        speech_voice_id: '',
        speech_model_id: '',
        speech_output_format: '',
        speech_status: 'empty',
        speech_error: '',
        speech_generated_at: null,
      }
    : patchData
  selectedProject.value.slides.splice(index, 1, {
    ...selectedProject.value.slides[index],
    ...optimisticPatch,
  })

  try {
    const response = await updateReelSlide(payload.id, patchData)
    const updatedSlide = normalizeProject(response?.data)
    if (updatedSlide?.id) {
      const { slide, project } = splitSlideProjectPayload(updatedSlide)
      selectedProject.value.slides.splice(index, 1, slide || updatedSlide)
      if (project?.id) {
        applyProjectSummary(project)
      } else {
        selectedProject.value.updated_at = new Date().toISOString()
        upsertProjectSummary(selectedProject.value)
      }
      templateDraft.value = serializeProjectSlides(selectedProject.value)
    }
  } catch (error) {
    selectedProject.value.slides.splice(index, 1, previousSlide)
    setFeedback('error', extractErrorMessage(error, 'Impossible de sauvegarder la slide.'))
  }
}

async function handleToggleCarouselImage(payload) {
  if (!payload?.id || !selectedProject.value) return
  const slide = selectedProject.value.slides?.find((item) => Number(item.id) === Number(payload.id))
  if (!slide) return

  let layoutMeta = {}
  const raw = String(slide.layout_notes || '').trim()
  if (raw) {
    try {
      const parsed = JSON.parse(raw)
      if (parsed && typeof parsed === 'object') layoutMeta = parsed
    } catch (_) {
      layoutMeta = {}
    }
  }
  if (payload.hide) {
    layoutMeta.hide_carousel_image = true
  } else {
    delete layoutMeta.hide_carousel_image
  }
  const nextLayoutNotes = Object.keys(layoutMeta).length ? JSON.stringify(layoutMeta) : ''

  await handlePatchSlide({ id: payload.id, patch: { layout_notes: nextLayoutNotes } })
}

async function handleDeleteSlide(slideId) {
  if (!slideId || !selectedProject.value?.id) return
  if (!window.confirm('Supprimer cette slide ?')) return

  savingSlide.value = true
  try {
    await deleteReelSlide(slideId)
    selectedProject.value.slides = selectedProject.value.slides.filter((slide) => Number(slide.id) !== Number(slideId))
    selectedProject.value.slide_count = selectedProject.value.slides.length
    selectedProject.value.updated_at = new Date().toISOString()
    templateDraft.value = serializeProjectSlides(selectedProject.value)
    upsertProjectSummary(selectedProject.value)

    if (Number(selectedSlideId.value) === Number(slideId)) {
      selectedSlideId.value = selectedProject.value.slides[0]?.id || null
    }

    delete diagnosticsBySlideId[slideId]
    setFeedback('success', 'Slide supprimée.')
  } catch (error) {
    setFeedback('error', extractErrorMessage(error, 'Impossible de supprimer la slide.'))
  } finally {
    savingSlide.value = false
  }
}

onMounted(() => {
  loadVoiceOptions()
  loadGeminiOptions()
  loadProjects()
})
</script>

<style src="@/styles/admin-common.css"></style>
<style scoped>
.reel-studio-admin {
  width: 100%;
  min-height: 100%;
  padding: 16px 16px 96px;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.page-header h1 {
  margin: 0;
  color: #0f172a;
  font-size: 28px;
  line-height: 1.2;
}

.feedback {
  margin: 0;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
  font-weight: 700;
}

.feedback--info {
  background: #eff6ff;
  color: #1e40af;
}

.feedback--success {
  background: #dcfce7;
  color: #166534;
}

.feedback--error {
  background: #fee2e2;
  color: #991b1b;
}

.studio-format-tabs {
  display: inline-flex;
  align-items: center;
  gap: 0;
  border: 1px solid #bfdbfe;
  border-radius: 999px;
  background: #eff6ff;
  padding: 4px;
  align-self: flex-start;
}

.studio-format-tab {
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: #1e3a8a;
  font-size: 13px;
  font-weight: 800;
  line-height: 1;
  padding: 9px 20px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.studio-format-tab--active {
  background: #1d4ed8;
  color: #ffffff;
}

.studio-format-tab:hover:not(.studio-format-tab--active) {
  background: #dbeafe;
}

.studio-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 0;
}

.project-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-panel--list {
  order: 9999;
  position: static;
  z-index: auto;
  clear: both;
  margin-top: 56px;
  padding-bottom: 96px;
  transform: none;
}

.section-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 14px 16px;
}

.section-toolbar h2 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.section-toolbar p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 14px;
  min-width: 0;
  min-height: auto;
  flex-shrink: 0;
  scroll-margin-top: 96px;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 0;
  min-height: auto;
}

.right-column > * {
  flex-shrink: 0;
}

.loading-state {
  margin: 0;
  color: #475569;
  font-size: 14px;
}

.empty-editor-state {
  margin: 0;
  border: 1px dashed #bfdbfe;
  border-radius: 12px;
  background: #eff6ff;
  color: #1e40af;
  padding: 16px;
  font-size: 14px;
  font-weight: 800;
}

.gemini-panel {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}


.gemini-panel-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.gemini-model-select {
  flex: 1 1 280px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 800;
  color: #334155;
}

.gemini-model-search,
.gemini-model-select select {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 12px;
  background: #ffffff;
  color: #0f172a;
  font: inherit;
}

.gemini-model-search {
  font-weight: 700;
}

.gemini-model-search::placeholder {
  color: #94a3b8;
}

.gemini-model-search:focus,
.gemini-model-select select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.btn-compact {
  padding: 10px 12px;
}

.btn-instructions {
  background: linear-gradient(180deg, #f4f6ff 0%, #eef2ff 100%);
  border-color: #c7d2fe;
  color: #29428e;
  font-weight: 700;
}
.btn-instructions:hover:not(:disabled) {
  background: #eef2ff;
  border-color: #29428e;
}

.gemini-usage-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.gemini-usage-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  padding: 10px 12px;
  min-width: 0;
}

.gemini-usage-card span {
  display: block;
  color: #64748b;
  font-size: 12px;
  font-weight: 800;
}

.gemini-usage-card strong {
  display: block;
  margin-top: 4px;
  color: #0f172a;
  font-size: 16px;
  line-height: 1.2;
  overflow-wrap: anywhere;
}

.gemini-error {
  margin: 0;
  color: #b91c1c;
  font-size: 13px;
  font-weight: 700;
}

.btn-primary {
  border: 0;
  border-radius: 8px;
  padding: 10px 14px;
  background: #1d4ed8;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.btn-secondary {
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 10px 14px;
  background: #eff6ff;
  color: #1e40af;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.btn-secondary:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.instagram-caption-panel {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.instagram-caption-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.instagram-caption-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 18px;
}

.instagram-caption-header p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}

.instagram-caption-text {
  width: 100%;
  min-height: 220px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #f8fbff;
  color: #0f172a;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  padding: 12px;
  resize: vertical;
  box-sizing: border-box;
}

.speech-panel {
  box-sizing: border-box;
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 18px;
  min-width: 0;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.speech-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.speech-panel-header h3 {
  margin: 0;
  color: #0f172a;
  font-size: 19px;
  line-height: 1.2;
}

.speech-panel-header p {
  margin: 6px 0 0;
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.35;
}

.speech-controls {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  align-items: start;
  gap: 12px;
  min-width: 0;
  max-width: 100%;
}

.voice-select {
  box-sizing: border-box;
  min-width: 0;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
  line-height: 1.25;
}

.voice-select-row {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  min-width: 0;
  max-width: 100%;
}

.voice-library-picker {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 42px;
  gap: 8px;
  min-width: 0;
  max-width: 100%;
}

.voice-library-filters {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px;
  min-width: 0;
  max-width: 100%;
  margin-bottom: 6px;
}

.voice-library-search,
.voice-library-filters select,
.voice-select select {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  max-width: 100%;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #ffffff;
  color: #0f172a;
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.35;
  padding: 9px 10px;
  min-height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.voice-library-search {
  margin-bottom: 2px;
}

.voice-library-search::placeholder {
  color: #94a3b8;
}

.voice-library-search:disabled,
.voice-library-filters select:disabled,
.voice-select select:disabled {
  background: #e2e8f0;
  color: #64748b;
}

.voice-favorite-toggle {
  box-sizing: border-box;
  width: 42px;
  min-width: 42px;
  min-height: 42px;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #eff6ff;
  color: #1e40af;
  font-family: inherit;
  font-size: 19px;
  font-weight: 900;
  line-height: 1;
  cursor: pointer;
}

.voice-favorite-toggle.is-favorite {
  background: #fef3c7;
  border-color: #facc15;
  color: #92400e;
}

.voice-favorite-toggle:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.voice-select span {
  color: #64748b;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.35;
  overflow-wrap: anywhere;
}

.voice-select .voice-warning {
  color: #b45309;
}

.voice-advanced {
  box-sizing: border-box;
  display: grid;
  gap: 10px;
  min-width: 0;
  max-width: 100%;
  border: 1px solid #dbeafe;
  border-radius: 8px;
  background: #ffffff;
  padding: 12px;
}

.voice-advanced-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 0;
}

.voice-advanced-toggle {
  border: 0;
  background: transparent;
  padding: 0;
  color: #1e3a8a;
  font-family: inherit;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.25;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.voice-advanced-arrow {
  display: inline-grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border-radius: 6px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 13px;
  font-weight: 900;
  line-height: 1;
  transition: transform 0.15s ease;
}

.voice-advanced-arrow.is-open {
  transform: rotate(90deg);
}

.voice-advanced-header .btn-secondary {
  min-height: 30px;
  padding: 6px 10px;
  font-size: 12px;
}

.voice-advanced-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(120px, 1fr));
  gap: 10px;
  min-width: 0;
}

.voice-advanced-field,
.voice-toggle {
  box-sizing: border-box;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
  line-height: 1.25;
}

.voice-advanced-field--wide {
  grid-column: span 2;
}

.voice-advanced-field input,
.voice-advanced-field select {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  background: #f8fafc;
  color: #0f172a;
  font-family: inherit;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.35;
  min-height: 36px;
  padding: 7px 9px;
}

.voice-toggle {
  justify-content: end;
  flex-direction: row;
  align-items: center;
}

.voice-toggle input {
  width: 18px;
  height: 18px;
  margin: 0;
}

.voice-toggle span {
  color: #0f172a;
  font-size: 13px;
  font-weight: 800;
  line-height: 1.35;
}

.voice-usage {
  box-sizing: border-box;
  display: grid;
  gap: 10px;
  min-width: 0;
  max-width: 100%;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  background: #f8fafc;
  padding: 12px;
}

.voice-usage-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 0;
}

.voice-usage-header strong {
  color: #0f172a;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.25;
}

.voice-usage-header span,
.voice-usage p {
  color: #475569;
  font-size: 12px;
  font-weight: 800;
  line-height: 1.35;
}

.voice-usage p {
  margin: 0;
}

.voice-usage-bar {
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: #e2e8f0;
}

.voice-usage-bar span {
  display: block;
  height: 100%;
  min-width: 2px;
  border-radius: inherit;
  background: #0284c7;
}

.voice-usage-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
  margin: 0;
}

.voice-usage-grid div {
  min-width: 0;
}

.voice-usage-grid dt {
  color: #64748b;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0;
  line-height: 1.25;
  text-transform: uppercase;
}

.voice-usage-grid dd {
  margin: 2px 0 0;
  color: #0f172a;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.25;
  overflow-wrap: anywhere;
}

.voice-usage--error {
  border-color: #fed7aa;
  background: #fff7ed;
}

.voice-usage--error .voice-usage-header span,
.voice-usage--error p {
  color: #9a3412;
}

.speech-actions {
  box-sizing: border-box;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  width: min(100%, 480px);
  max-width: 100%;
  min-width: 0;
  justify-self: end;
}

.speech-actions .btn-primary,
.speech-actions .btn-secondary {
  width: 100%;
  min-height: 42px;
  line-height: 1.2;
  white-space: normal;
}

.voice-charcount {
  font-size: 12px;
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 9px 12px;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: flex-end;
  gap: 4px 6px;
  max-width: 360px;
  text-align: right;
}

.voice-charcount strong {
  color: #0f172a;
  font-size: 14px;
}

.voice-charcount small {
  flex-basis: 100%;
  color: inherit;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.35;
}

.voice-charcount--warn {
  color: #b45309;
  background: #fef3c7;
  border-color: #fde68a;
}

.voice-charcount--warn strong {
  color: #92400e;
}

.voice-test-audio {
  margin-top: 12px;
  width: 100%;
  max-width: 360px;
}

.speech-audio {
  width: 100%;
}

.manual-editor-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 36px;
}

@media (max-width: 1140px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .speech-controls {
    grid-template-columns: minmax(0, 1fr);
  }

  .speech-actions {
    grid-column: auto;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    justify-self: stretch;
    width: 100%;
  }

  .gemini-usage-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .reel-studio-admin {
    padding: 12px 10px 84px;
  }

  .section-toolbar {
    align-items: stretch;
    flex-direction: column;
  }

  .speech-panel-header {
    align-items: stretch;
    flex-direction: column;
  }

  .speech-controls {
    grid-template-columns: 1fr;
  }

  .voice-select-row {
    grid-template-columns: 1fr;
  }

  .voice-library-filters {
    grid-template-columns: 1fr;
  }

  .voice-usage-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .voice-usage-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .gemini-panel-header {
    align-items: stretch;
    flex-direction: column;
  }

  .gemini-usage-grid {
    grid-template-columns: 1fr;
  }

  .voice-advanced-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .voice-advanced-field--wide {
    grid-column: span 2;
  }

  .speech-actions {
    grid-column: auto;
    grid-template-columns: 1fr;
    min-width: 0;
    justify-self: stretch;
    width: 100%;
  }

  .voice-charcount {
    justify-content: flex-start;
    max-width: none;
    text-align: left;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .page-header h1 {
    font-size: 22px;
  }
}
</style>
