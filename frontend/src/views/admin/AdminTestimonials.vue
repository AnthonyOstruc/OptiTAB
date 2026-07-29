<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import {
  createTestimonial,
  deleteTestimonial,
  getAdminTestimonials,
  getBioLandingStatus,
  reorderTestimonials,
  setBioLandingPublished,
  updateTestimonial
} from '@/api/testimonials'
import { useToast } from '@/composables/useToast'
import { BIO_LANDING_PATH } from '@/config/bioLandingContent'

const { success: toastSuccess, error: toastError } = useToast()

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5 Mo
const ACCEPTED = ['image/png', 'image/jpeg', 'image/webp']

// Listes fermées : on ne peut pas saisir de nom ou de prénom, ni pour la
// personne qui écrit, ni pour son enfant. C'est le seul moyen fiable —
// un champ libre finit toujours par contenir « Maman de Léa ».
// Doit rester aligné avec Testimonial.PROFILE_CHOICES côté backend.
const PROFILE_OPTIONS = [
  "Maman d'élève",
  "Papa d'élève",
  "Parent d'élève",
  'Élève',
  'Étudiant',
  'Étudiante'
]

const LEVEL_OPTIONS = [
  '6e',
  '5e',
  '4e',
  '3e',
  'Seconde',
  'Première',
  'Terminale',
  'BTS',
  'Prépa MPSI',
  'Prépa MP2I',
  'Prépa PCSI',
  'Supérieur'
]

const items = ref([])
const loading = ref(true)
const saving = ref(false)
const editingId = ref(null)
const dragOver = ref(false)
const fileInput = ref(null)

// Aperçu local du fichier choisi. Révoqué à chaque remplacement pour ne pas
// fuir d'URL objet tant que le studio reste ouvert.
const previewUrl = ref('')
let previewObjectUrl = null

function createEmptyForm() {
  return {
    author: '',
    role: '',
    channel: 'whatsapp',
    alt_text: '',
    // Anonyme par défaut : le prénom est l'exception, jamais la norme.
    name_consent: false,
    display_name: '',
    is_published: false,
    is_featured: false
  }
}

const form = reactive(createEmptyForm())
const selectedFile = ref(null)

const isEditing = computed(() => editingId.value !== null)

// Même règle d'affichage que sur la page publique : le prénom prime s'il est
// autorisé, sinon le profil, sinon le niveau.
const effectiveName = computed(() =>
  form.name_consent ? String(form.display_name).trim() : ''
)
const previewPrimary = computed(
  () => effectiveName.value || form.author || form.role || 'Témoignage'
)
const previewSecondary = computed(() =>
  effectiveName.value ? [form.author, form.role].filter(Boolean).join(' · ') : form.author ? form.role : ''
)

const publishedCount = computed(() => items.value.filter((item) => item.is_published).length)

const canSubmit = computed(() => {
  if (saving.value) return false
  // Une capture est obligatoire à la création, facultative en modification.
  if (!isEditing.value && !selectedFile.value) return false
  return true
})

function setPreview(file) {
  if (previewObjectUrl) {
    URL.revokeObjectURL(previewObjectUrl)
    previewObjectUrl = null
  }
  if (!file) {
    previewUrl.value = ''
    return
  }
  previewObjectUrl = URL.createObjectURL(file)
  previewUrl.value = previewObjectUrl
}

function validateFile(file) {
  if (!ACCEPTED.includes(file.type)) {
    toastError('Format non accepté. Utilisez PNG, JPEG ou WebP.')
    return false
  }
  if (file.size > MAX_FILE_SIZE) {
    const mo = (file.size / 1024 / 1024).toFixed(1)
    toastError(`Capture trop lourde (${mo} Mo). Maximum 5 Mo.`)
    return false
  }
  return true
}

function pickFile(file) {
  if (!file || !validateFile(file)) return
  selectedFile.value = file
  setPreview(file)
}

function onFileChange(event) {
  pickFile(event.target.files?.[0])
}

function onDrop(event) {
  dragOver.value = false
  pickFile(event.dataTransfer?.files?.[0])
}

// Retirer l'accord efface le prénom : on ne garde pas une donnée
// personnelle « au cas où », le backend fait le même nettoyage.
function onNameConsentChange() {
  if (!form.name_consent) form.display_name = ''
}

function resetForm() {
  Object.assign(form, createEmptyForm())
  selectedFile.value = null
  setPreview(null)
  editingId.value = null
  if (fileInput.value) fileInput.value.value = ''
}

function startEdit(item) {
  editingId.value = item.id
  form.author = item.author
  form.role = item.role || ''
  form.channel = item.channel
  form.alt_text = item.alt_text || ''
  form.name_consent = item.name_consent
  form.display_name = item.display_name || ''
  form.is_published = item.is_published
  form.is_featured = item.is_featured
  selectedFile.value = null
  setPreview(null)
  previewUrl.value = item.src || ''
  if (fileInput.value) fileInput.value.value = ''
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function rowPrimary(item) {
  const name = item.name_consent ? String(item.display_name || '').trim() : ''
  return name || item.author || item.role || 'Témoignage'
}

function rowSecondary(item) {
  const name = item.name_consent ? String(item.display_name || '').trim() : ''
  if (name) return [item.author, item.role].filter(Boolean).join(' · ')
  return item.author ? item.role : ''
}

// ------------------------------------------------------------
// Mise en ligne de la page publique
// ------------------------------------------------------------

const pagePublished = ref(false)
const pageToggling = ref(false)

async function loadPageStatus() {
  try {
    const { data } = await getBioLandingStatus()
    pagePublished.value = Boolean(data?.published)
  } catch (_) {
    pagePublished.value = false
  }
}

async function togglePage() {
  const next = !pagePublished.value

  if (next && !publishedCount.value) {
    const ok = window.confirm(
      "Aucun témoignage n'est publié : la page s'affichera sans le moindre avis. Mettre quand même en ligne ?"
    )
    if (!ok) return
  }

  pageToggling.value = true
  try {
    const { data } = await setBioLandingPublished(next)
    pagePublished.value = Boolean(data?.published)
    toastSuccess(pagePublished.value ? 'Page mise en ligne.' : 'Page retirée du public.')
  } catch (error) {
    toastError('Impossible de changer la visibilité de la page.')
  } finally {
    pageToggling.value = false
  }
}

async function load() {
  loading.value = true
  try {
    const { data } = await getAdminTestimonials()
    items.value = Array.isArray(data) ? data : []
  } catch (error) {
    toastError("Impossible de charger les témoignages.")
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!canSubmit.value) return

  const payload = { ...form }
  if (selectedFile.value) payload.image = selectedFile.value

  saving.value = true
  try {
    if (isEditing.value) {
      await updateTestimonial(editingId.value, payload)
      toastSuccess('Témoignage mis à jour.')
    } else {
      await createTestimonial(payload)
      toastSuccess('Témoignage ajouté.')
    }
    resetForm()
    await load()
  } catch (error) {
    // On remonte le message précis du backend plutôt qu'une erreur générique.
    const detail = error?.response?.data
    const message =
      (detail && typeof detail === 'object'
        ? Object.values(detail).flat().join(' ')
        : detail) || "L'enregistrement a échoué."
    toastError(String(message))
  } finally {
    saving.value = false
  }
}

async function togglePublished(item) {
  try {
    await updateTestimonial(item.id, { is_published: !item.is_published })
    await load()
  } catch (error) {
    toastError('Modification impossible.')
  }
}

async function setFeatured(item) {
  if (!item.is_published) {
    toastError('Publiez le témoignage avant de le mettre en avant.')
    return
  }
  try {
    await updateTestimonial(item.id, { is_featured: !item.is_featured })
    await load()
  } catch (error) {
    toastError('Modification impossible.')
  }
}

async function remove(item) {
  const ok = window.confirm(
    `Supprimer définitivement ce témoignage (${item.author || item.role || 'sans profil'}) ? La capture sera effacée du stockage.`
  )
  if (!ok) return
  try {
    await deleteTestimonial(item.id)
    if (editingId.value === item.id) resetForm()
    toastSuccess('Témoignage supprimé.')
    await load()
  } catch (error) {
    toastError('Suppression impossible.')
  }
}

async function move(index, direction) {
  const target = index + direction
  if (target < 0 || target >= items.value.length) return

  const next = [...items.value]
  const [moved] = next.splice(index, 1)
  next.splice(target, 0, moved)
  items.value = next

  try {
    await reorderTestimonials(next.map((item) => item.id))
  } catch (error) {
    toastError('Réordonnancement impossible.')
    await load()
  }
}

onMounted(() => {
  load()
  loadPageStatus()
})

onBeforeUnmount(() => {
  if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl)
})
</script>

<template>
  <div class="studio">
    <header class="studio__head">
      <h1>Studio témoignages</h1>

      <div class="studio__aside">
        <button
          type="button"
          class="studio__toggle"
          :class="pagePublished ? 'is-online' : 'is-offline'"
          :disabled="pageToggling"
          @click="togglePage"
        >
          <span class="studio__dot" aria-hidden="true"></span>
          <span v-if="pageToggling">…</span>
          <span v-else-if="pagePublished">Page en ligne — cliquez pour retirer</span>
          <span v-else>Page hors ligne — cliquez pour publier</span>
        </button>

        <a :href="BIO_LANDING_PATH" target="_blank" rel="noopener" class="studio__preview">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M14 4h6v6M20 4l-8.5 8.5M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          Voir la page
          <code>{{ BIO_LANDING_PATH }}</code>
        </a>

        <div class="studio__counts">
          <span class="count"><strong>{{ items.length }}</strong> au total</span>
          <span class="count count--ok"><strong>{{ publishedCount }}</strong> en ligne</span>
        </div>
      </div>
    </header>

    <div class="studio__grid">
      <!-- ========== Formulaire ========== -->
      <section class="panel">
        <h2>{{ isEditing ? 'Modifier le témoignage' : 'Ajouter une capture' }}</h2>

        <div
          class="drop"
          :class="{ 'is-over': dragOver, 'has-image': previewUrl }"
          @dragover.prevent="dragOver = true"
          @dragleave.prevent="dragOver = false"
          @drop.prevent="onDrop"
          @click="fileInput?.click()"
        >
          <img v-if="previewUrl" :src="previewUrl" alt="Aperçu de la capture" class="drop__img" />
          <div v-else class="drop__empty">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M12 16V4m0 0L8 8m4-4 4 4M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <p><strong>Glissez la capture ici</strong></p>
            <p class="drop__hint">ou cliquez pour choisir — PNG, JPEG ou WebP, 5 Mo maximum</p>
          </div>
          <span v-if="previewUrl" class="drop__replace">Cliquez pour remplacer</span>
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/png,image/jpeg,image/webp"
          class="hidden-input"
          @change="onFileChange"
        />

        <label class="field">
          <span>Profil</span>
          <select v-model="form.author">
            <option value="">— Aucun —</option>
            <option v-for="option in PROFILE_OPTIONS" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
        </label>

        <label class="field">
          <span>Niveau</span>
          <select v-model="form.role">
            <option value="">— Aucun —</option>
            <option v-for="option in LEVEL_OPTIONS" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
        </label>

        <label class="field">
          <span>Canal</span>
          <select v-model="form.channel">
            <option value="whatsapp">WhatsApp</option>
            <option value="sms">SMS</option>
          </select>
        </label>

        <label class="field">
          <span>Texte alternatif</span>
          <input
            v-model="form.alt_text"
            type="text"
            placeholder="Message WhatsApp d'une maman : sa fille est passée de 8 à 14"
            maxlength="255"
          />
        </label>

        <label class="check check--consent check--name">
          <input v-model="form.name_consent" type="checkbox" @change="onNameConsentChange" />
          <span>
            <strong>La personne accepte que son prénom apparaisse</strong>
            <em>— accord distinct du précédent. Décoché, le témoignage reste anonyme.</em>
          </span>
        </label>

        <label v-if="form.name_consent" class="field field--name">
          <span>Prénom affiché</span>
          <input
            v-model="form.display_name"
            type="text"
            placeholder="Sandra M."
            maxlength="60"
          />
        </label>

        <label class="check">
          <input v-model="form.is_published" type="checkbox" />
          <span>Publier sur la page</span>
        </label>

        <label class="check" :class="{ 'is-locked': !form.is_published }">
          <input v-model="form.is_featured" type="checkbox" :disabled="!form.is_published" />
          <span>
            Mettre en avant dans le hero
            <em>— un seul témoignage à la fois</em>
          </span>
        </label>

        <div class="actions">
          <button class="btn btn--primary" :disabled="!canSubmit" @click="submit">
            {{ saving ? 'Enregistrement…' : isEditing ? 'Enregistrer' : 'Ajouter' }}
          </button>
          <button v-if="isEditing" class="btn btn--ghost" @click="resetForm">Annuler</button>
        </div>
      </section>

      <!-- ========== Aperçu réel ========== -->
      <section class="panel panel--preview">
        <h2>Aperçu sur la page</h2>
        <div class="card-preview">
          <div class="card-preview__frame">
            <template v-if="previewUrl">
              <img :src="previewUrl" class="card-preview__backdrop" alt="" aria-hidden="true" />
              <img :src="previewUrl" class="card-preview__img" alt="" />
            </template>
            <span v-else class="card-preview__placeholder">La capture apparaîtra ici</span>
          </div>
          <div class="card-preview__meta">
            <span class="card-preview__identity">
              <strong>{{ previewPrimary }}</strong>
              <small v-if="previewSecondary">{{ previewSecondary }}</small>
            </span>
            <span class="card-preview__channel" :class="form.channel">
              {{ form.channel === 'sms' ? 'SMS' : 'WhatsApp' }}
            </span>
          </div>
        </div>
      </section>
    </div>

    <!-- ========== Liste ========== -->
    <section class="panel">
      <h2>Témoignages ({{ items.length }})</h2>

      <p v-if="loading" class="empty">Chargement…</p>

      <p v-else-if="!items.length" class="empty">
        Aucun témoignage pour l'instant. La section est masquée sur la page tant qu'aucune capture
        n'est publiée.
      </p>

      <ul v-else class="list">
        <li v-for="(item, index) in items" :key="item.id" class="row">
          <img :src="item.src" :alt="item.alt_text || 'Capture'" class="row__thumb" />

          <div class="row__body">
            <p class="row__author">
              {{ rowPrimary(item) }}
              <span class="tag" :class="item.channel">
                {{ item.channel === 'sms' ? 'SMS' : 'WhatsApp' }}
              </span>
              <span v-if="item.is_featured" class="tag tag--featured">Hero</span>
              <span v-if="item.name_consent && item.display_name" class="tag tag--named">
                Prénom autorisé
              </span>
            </p>
            <p class="row__role">{{ rowSecondary(item) || '—' }}</p>
            <p class="row__flags">
              <span :class="item.is_published ? 'ok' : 'muted'">
                {{ item.is_published ? 'En ligne' : 'Brouillon' }}
              </span>
            </p>
          </div>

          <div class="row__actions">
            <button class="mini" :disabled="index === 0" title="Monter" @click="move(index, -1)">↑</button>
            <button
              class="mini"
              :disabled="index === items.length - 1"
              title="Descendre"
              @click="move(index, 1)"
            >
              ↓
            </button>
            <button class="mini" @click="togglePublished(item)">
              {{ item.is_published ? 'Retirer' : 'Publier' }}
            </button>
            <button class="mini" @click="setFeatured(item)">
              {{ item.is_featured ? 'Retirer du hero' : 'Hero' }}
            </button>
            <button class="mini" @click="startEdit(item)">Modifier</button>
            <button class="mini mini--danger" @click="remove(item)">Supprimer</button>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped lang="scss">
.studio {
  padding: 20px;
  max-width: 1180px;
  margin: 0 auto;
}

.studio__head {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;

  h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 800;
    color: #0f172a;
  }
}

.studio__counts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.count {
  padding: 5px 11px;
  border-radius: 999px;
  border: 1px solid #dbe4f5;
  background: #f8fafc;
  color: #475569;
  font-size: 0.82rem;

  &--ok {
    border-color: #bfe8cd;
    background: #f0fdf4;
    color: #15803d;
  }

  &--warn {
    border-color: #fcd34d;
    background: #fffbeb;
    color: #92400e;
  }
}

.studio__aside {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 9px;
}

/* Interrupteur de mise en ligne : l'etat doit se lire d'un coup d'oeil,
   c'est l'action la plus lourde de consequences de cet ecran. */
.studio__toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  padding: 0 14px;
  border-radius: 10px;
  font-family: inherit;
  font-size: 0.87rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.18s ease, border-color 0.18s ease;

  &:disabled {
    opacity: 0.6;
    cursor: progress;
  }

  &.is-online {
    border: 1px solid #bfe8cd;
    background: #f0fdf4;
    color: #15803d;
  }

  &.is-offline {
    border: 1px solid #fcd34d;
    background: #fffbeb;
    color: #92400e;
  }
}

.studio__dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;

  .is-online & {
    background: #16a34a;
  }

  .is-offline & {
    background: #d97706;
  }
}

.studio__preview {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 38px;
  padding: 0 14px;
  border-radius: 10px;
  border: 1px solid #c8d6fa;
  background: #ffffff;
  color: #2a38b7;
  font-size: 0.87rem;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.18s ease, border-color 0.18s ease;

  &:hover {
    background: #f4f8ff;
    border-color: #a8c1ff;
    color: #2a38b7;
  }

  svg {
    width: 15px;
    height: 15px;
  }

  code {
    padding: 1px 6px;
    border-radius: 5px;
    background: #eef2ff;
    color: #1e3a8a;
    font-size: 0.8rem;
    font-weight: 600;
  }
}

.studio__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.panel {
  padding: 18px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  background: #ffffff;

  h2 {
    margin: 0 0 14px;
    padding: 0;
    font-size: 1.08rem;
    font-weight: 800;
    color: #0f172a;
  }
}

/* ---------- Zone de dépôt ---------- */

.drop {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 190px;
  margin-bottom: 16px;
  padding: 14px;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  background: #f8fafc;
  cursor: pointer;
  transition: border-color 0.18s ease, background 0.18s ease;

  &:hover,
  &.is-over {
    border-color: #2a38b7;
    background: #eef2ff;
  }
}

.drop__img {
  max-height: 260px;
  max-width: 100%;
  border-radius: 8px;
}

.drop__empty {
  text-align: center;
  color: #64748b;

  svg {
    width: 30px;
    height: 30px;
    margin-bottom: 6px;
    color: #94a3b8;
  }

  p {
    margin: 0;
    font-size: 0.92rem;
  }
}

.drop__hint {
  margin-top: 3px !important;
  font-size: 0.8rem;
}

.drop__replace {
  position: absolute;
  right: 8px;
  bottom: 8px;
  padding: 3px 9px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.75);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 700;
}

.hidden-input {
  display: none;
}

/* ---------- Champs ---------- */

.field {
  display: block;
  margin-bottom: 13px;

  > span {
    display: block;
    margin-bottom: 5px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #1e293b;

    em {
      font-style: normal;
      font-weight: 600;
      color: #b91c1c;
      font-size: 0.78rem;
    }
  }

  input[type='text'],
  select {
    width: 100%;
    min-height: 40px;
    padding: 0 11px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    background: #fff;
    font-family: inherit;
    font-size: 0.92rem;
    color: #0f172a;

    &:focus {
      outline: none;
      border-color: #2a38b7;
      box-shadow: 0 0 0 3px rgba(42, 56, 183, 0.12);
    }
  }

}

.check {
  display: flex;
  align-items: flex-start;
  gap: 9px;
  margin-bottom: 11px;
  font-size: 0.87rem;
  line-height: 1.45;
  color: #1e293b;
  cursor: pointer;

  input {
    margin-top: 2px;
    width: 16px;
    height: 16px;
    flex-shrink: 0;
    accent-color: #2a38b7;
  }

  em {
    font-style: normal;
    color: #94a3b8;
    font-size: 0.82rem;
  }

  &.is-locked {
    color: #94a3b8;
    cursor: not-allowed;
  }
}

.check--consent {
  padding: 11px 12px;
  border-radius: 10px;
  border: 1px solid #cfe0ff;
  background: #f4f8ff;
}

.check--name {
  border-color: #ddd6fe;
  background: #f5f3ff;
}

.field--name {
  margin-top: -2px;
  padding-left: 12px;
  border-left: 2px solid #ddd6fe;
}

.actions {
  display: flex;
  gap: 9px;
  margin-top: 16px;
}

.btn {
  min-height: 42px;
  padding: 0 18px;
  border-radius: 10px;
  border: 1px solid transparent;
  font-family: inherit;
  font-size: 0.92rem;
  font-weight: 700;
  cursor: pointer;

  &--primary {
    background: #2a38b7;
    color: #fff;

    &:disabled {
      background: #cbd5e1;
      cursor: not-allowed;
    }
  }

  &--ghost {
    background: #fff;
    border-color: #cbd5e1;
    color: #334155;
  }
}

/* ---------- Aperçu carte ---------- */

.card-preview {
  max-width: 260px;
  border: 1px solid #d6e1ff;
  border-radius: 14px;
  background: #fff;
  overflow: hidden;
}

/* Doit rester identique au cadre de TestimonialShot.vue : c'est tout
   l'interet de l'apercu. */
.card-preview__frame {
  position: relative;
  aspect-ratio: 4 / 3;
  background: #eef2f7;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-preview__backdrop {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(16px) saturate(1.15);
  transform: scale(1.2);
  opacity: 0.55;
}

.card-preview__img {
  position: relative;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.card-preview__placeholder {
  padding: 0 16px;
  color: #94a3b8;
  font-size: 0.82rem;
  text-align: center;
}

.card-preview__meta {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 13px;
  border-top: 1px solid #e2e9fb;
}

.card-preview__identity {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;

  strong {
    font-size: 0.9rem;
    font-weight: 800;
    color: #0f172a;
  }

  small {
    font-size: 0.76rem;
    color: #475569;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.card-preview__channel {
  flex-shrink: 0;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;

  &.whatsapp {
    background: #e7f8ec;
    border: 1px solid #bfe8cd;
    color: #128c4a;
  }

  &.sms {
    background: #eef4ff;
    border: 1px solid #cfe0ff;
    color: #1e3a8a;
  }
}

/* ---------- Liste ---------- */

.empty {
  margin: 0;
  padding: 22px;
  border-radius: 10px;
  background: #f8fafc;
  color: #64748b;
  font-size: 0.9rem;
  text-align: center;
}

.list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.row {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 11px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
}

.row__thumb {
  width: 54px;
  height: 72px;
  flex-shrink: 0;
  object-fit: cover;
  object-position: top center;
  border-radius: 7px;
  border: 1px solid #e2e8f0;
  background: #f1f5f9;
}

.row__body {
  flex: 1;
  min-width: 0;
}

.row__author {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
  margin: 0 0 3px;
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
}

.row__role {
  margin: 0 0 5px;
  font-size: 0.82rem;
  color: #64748b;
}

.row__flags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0;
  font-size: 0.78rem;
  font-weight: 700;

  .ok {
    color: #15803d;
  }

  .warn {
    color: #b45309;
  }

  .muted {
    color: #94a3b8;
  }
}

.tag {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 700;

  &.whatsapp {
    background: #e7f8ec;
    color: #128c4a;
  }

  &.sms {
    background: #eef4ff;
    color: #1e3a8a;
  }

  &--featured {
    background: #fef3c7;
    color: #92400e;
  }

  &--named {
    background: #ede9fe;
    color: #5b21b6;
  }
}

.row__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  justify-content: flex-end;
}

.mini {
  min-height: 30px;
  padding: 0 10px;
  border: 1px solid #cbd5e1;
  border-radius: 7px;
  background: #fff;
  font-family: inherit;
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
  cursor: pointer;

  &:hover:not(:disabled) {
    background: #f1f5f9;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  &--danger {
    border-color: #fecaca;
    color: #b91c1c;

    &:hover:not(:disabled) {
      background: #fef2f2;
    }
  }
}

@media (min-width: 900px) {
  .studio__grid {
    grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr);
    align-items: start;
  }
}

@media (max-width: 640px) {
  .row {
    flex-wrap: wrap;
  }

  .row__actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
