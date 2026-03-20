<template>
  <div>
    <h2 class="admin-title">Gestion du Blog</h2>

    <!-- Onglets -->
    <div class="blog-tabs">
      <button :class="['tab-btn', { active: activeTab === 'posts' }]" @click="activeTab = 'posts'">
        <span class="tab-icon">📝</span> Articles
        <span class="tab-count" v-if="posts.length">{{ posts.length }}</span>
      </button>
      <button :class="['tab-btn', { active: activeTab === 'categories' }]" @click="activeTab = 'categories'">
        <span class="tab-icon">📁</span> Catégories
        <span class="tab-count" v-if="categories.length">{{ categories.length }}</span>
      </button>
      <button :class="['tab-btn', { active: activeTab === 'tags' }]" @click="activeTab = 'tags'">
        <span class="tab-icon">🏷️</span> Tags
        <span class="tab-count" v-if="tags.length">{{ tags.length }}</span>
      </button>
    </div>

    <!-- ═══════ ARTICLES ═══════ -->
    <template v-if="activeTab === 'posts'">
      <form class="admin-form" @submit.prevent="handleSavePost">
        <h3 class="form-section-title">{{ postForm.id ? 'Modifier l\'article' : 'Nouvel article' }}</h3>

        <div class="form-group">
          <label>Titre de l'article <span class="required">*</span></label>
          <input v-model="postForm.titre" placeholder="Ex: 5 astuces pour réussir sa prépa MPSI" required />
        </div>

        <div class="form-group">
          <label>Slug</label>
          <input v-model="postForm.slug" placeholder="Auto-généré depuis le titre si vide" />
          <small class="field-hint">URL de l'article. Laisser vide = auto.</small>
        </div>

        <div class="form-group">
          <label>Extrait</label>
          <input v-model="postForm.extrait" placeholder="Résumé court affiché dans la liste du blog" maxlength="400" />
          <small class="field-hint">Max 400 car. Affiché dans les cartes du blog.</small>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label>Catégorie</label>
            <select v-model="postForm.categorie">
              <option :value="null">— Aucune catégorie —</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Statut</label>
            <select v-model="postForm.statut">
              <option value="draft">Brouillon</option>
              <option value="published">Publié</option>
            </select>
          </div>
        </div>

        <!-- Tags multi-select chips -->
        <div class="form-group">
          <label>Tags</label>
          <div class="tags-select-row">
            <select v-model="selectedTagId">
              <option value="">Ajouter un tag…</option>
              <option v-for="t in availableTags" :key="t.id" :value="t.id">{{ t.nom }}</option>
            </select>
            <button class="btn-tag-add" type="button" @click="addTag" :disabled="!selectedTagId">+</button>
          </div>
          <div class="chips" v-if="postForm.tags_ids.length">
            <span class="chip" v-for="tid in postForm.tags_ids" :key="tid">
              {{ tagNameById(tid) }}
              <button class="chip-remove" type="button" @click="removeTag(tid)">×</button>
            </span>
          </div>
        </div>

        <div class="form-group">
          <label>Contenu <span class="required">*</span></label>
          <textarea v-model="postForm.contenu" placeholder="Rédigez en Markdown ($formules$ LaTeX supportées)" rows="14"></textarea>
          <small class="field-hint">Supporte Markdown, LaTeX ($formule$) et HTML.</small>
        </div>

        <!-- Image de couverture -->
        <div class="form-group">
          <label>Image de couverture</label>
          <div class="image-upload-zone">
            <input type="file" accept="image/*" @change="onCoverImageChange" />
            <img v-if="postForm._coverPreview" :src="postForm._coverPreview" class="image-preview-lg" />
          </div>
        </div>

        <div class="form-group">
          <label>Alt text image</label>
          <input v-model="postForm.alt_text_image" placeholder="Description textuelle de l'image (accessibilité + SEO)" maxlength="250" />
          <small class="field-hint">Max 250 car. Important pour l'accessibilité et le référencement.</small>
        </div>

        <!-- SEO -->
        <details class="seo-accordion">
          <summary>
            <span class="seo-icon">🔍</span> SEO (optionnel)
            <span class="seo-arrow">▸</span>
          </summary>
          <div class="seo-content">
            <div class="form-row-2">
              <div class="form-group">
                <label>Titre SEO</label>
                <input v-model="postForm.seo_title" placeholder="Titre dans l'onglet Google" maxlength="70" />
                <small class="field-hint">Max 70 car. Si vide = titre article.</small>
              </div>
              <div class="form-group">
                <label>Meta description</label>
                <input v-model="postForm.meta_description" placeholder="Description sous le lien Google" maxlength="160" />
                <small class="field-hint">Max 160 car. Si vide = extrait.</small>
              </div>
            </div>
            <div class="form-row-2">
              <div class="form-group">
                <label>OG Title</label>
                <input v-model="postForm.og_title" placeholder="Titre sur Facebook/LinkedIn" maxlength="100" />
              </div>
              <div class="form-group">
                <label>OG Description</label>
                <input v-model="postForm.og_description" placeholder="Description sur les réseaux" maxlength="200" />
              </div>
            </div>
            <div class="form-group">
              <label>Image OG (Open Graph)</label>
              <div class="image-upload-zone">
                <input type="file" accept="image/*" @change="onOgImageChange" />
                <img v-if="postForm._ogPreview" :src="postForm._ogPreview" class="image-preview-lg" />
              </div>
              <small class="field-hint">Image dédiée réseaux sociaux. Si vide = image couverture. Idéal : 1200×630 px.</small>
            </div>
            <div class="form-group">
              <label>Meta robots</label>
              <select v-model="postForm.meta_robots">
                <option value="index">Index (visible Google)</option>
                <option value="noindex">Noindex (masqué Google)</option>
              </select>
            </div>
          </div>
        </details>

        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ postForm.id ? 'Mettre à jour' : 'Créer' }}</button>
          <button class="btn-secondary" type="button" @click="handlePreview" :disabled="!postForm.contenu.trim()">Prévisualiser</button>
          <button v-if="postForm.id" class="btn-danger" type="button" @click="resetPostForm">Annuler</button>
        </div>
      </form>

      <!-- Aperçu de l'article -->
      <div v-if="showPreview" class="preview-section">
        <div class="preview-header-bar">
          <h3>Aperçu de l'article {{ postForm.id ? '(Mode édition)' : '(Mode création)' }}</h3>
          <button class="btn-close-preview" @click="showPreview = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18"/><path d="M6 6l12 12"/></svg>
            Fermer
          </button>
        </div>
        <div class="preview-article">
          <div class="preview-meta">
            <span :class="['status-badge', postForm.statut]">{{ postForm.statut === 'published' ? 'Publié' : 'Brouillon' }}</span>
            <span v-if="previewCategorie" class="preview-cat">{{ previewCategorie }}</span>
            <span v-if="postForm.tags_ids.length" class="preview-tags">
              <span class="chip" v-for="tid in postForm.tags_ids" :key="tid">{{ tagNameById(tid) }}</span>
            </span>
          </div>
          <h1 class="preview-title">{{ postForm.titre || 'Sans titre' }}</h1>
          <p v-if="postForm.extrait" class="preview-excerpt">{{ postForm.extrait }}</p>
          <div class="preview-content" v-html="previewHtml"></div>
        </div>
      </div>

      <!-- Filtres articles -->
      <div class="filters">
        <div class="filter-group">
          <label>Filtrer par catégorie</label>
          <select v-model="filterCategorie">
            <option value="all">Toutes les catégories</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Filtrer par statut</label>
          <select v-model="filterStatut">
            <option value="all">Tous les statuts</option>
            <option value="published">Publié</option>
            <option value="draft">Brouillon</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Rechercher</label>
          <input v-model="filterSearch" type="text" placeholder="Recherche par titre…" class="filter-input" />
        </div>
      </div>

      <!-- Tableau des articles -->
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Catégorie</th>
            <th>Statut</th>
            <th>Date publication</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoadingPosts">
            <td colspan="6" class="loading-row">Chargement des articles...</td>
          </tr>
          <template v-else>
            <tr v-for="p in filteredPosts" :key="p.id">
              <td>{{ p.id }}</td>
              <td class="title-cell">{{ p.titre }}</td>
              <td>{{ p.categorie_nom || '—' }}</td>
              <td>
                <span :class="['status-badge', p.statut]">{{ p.statut === 'published' ? 'Publié' : 'Brouillon' }}</span>
              </td>
              <td>{{ p.date_publication ? new Date(p.date_publication).toLocaleDateString('fr-FR') : '—' }}</td>
              <td>
                <AdminActionsButtons
                  :item="p"
                  :actions="['edit', 'delete']"
                  edit-label="Éditer"
                  confirm-message="Supprimer cet article ?"
                  @edit="editPost"
                  @delete="handleDeletePost"
                />
              </td>
            </tr>
            <tr v-if="filteredPosts.length === 0">
              <td colspan="6" class="empty-row">Aucun article trouvé.</td>
            </tr>
          </template>
        </tbody>
      </table>

      <div v-if="filteredPosts.length > 0" class="pagination-info">
        {{ filteredPosts.length }} article(s) au total
      </div>
    </template>

    <!-- ═══════ CATÉGORIES ═══════ -->
    <template v-if="activeTab === 'categories'">
      <form class="admin-form" @submit.prevent="handleSaveCategory">
        <h3 class="form-section-title">{{ catForm.id ? 'Modifier la catégorie' : 'Nouvelle catégorie' }}</h3>

        <div class="form-group">
          <label>Nom <span class="required">*</span></label>
          <input v-model="catForm.nom" placeholder="Ex: Méthodologie" required />
        </div>

        <div class="form-group">
          <label>Slug</label>
          <input v-model="catForm.slug" placeholder="Auto-généré depuis le nom si vide" />
          <small class="field-hint">URL-friendly. Laisser vide = auto.</small>
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea v-model="catForm.description" placeholder="Courte description affichée sur la page catégorie" rows="2"></textarea>
        </div>

        <div class="form-group">
          <label>Meta description SEO</label>
          <input v-model="catForm.meta_description" placeholder="Description SEO (max 160 car.)" maxlength="160" />
          <small class="field-hint">Si vide, la description normale est utilisée.</small>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label>Ordre</label>
            <input v-model.number="catForm.ordre" type="number" placeholder="0" min="0" />
            <small class="field-hint">0 = premier, 10 = après, etc.</small>
          </div>
          <div class="form-group">
            <label>Meta robots</label>
            <select v-model="catForm.meta_robots">
              <option value="index">Index (visible Google)</option>
              <option value="noindex">Noindex (masqué Google)</option>
            </select>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ catForm.id ? 'Mettre à jour' : 'Créer' }}</button>
          <button v-if="catForm.id" class="btn-danger" type="button" @click="resetCatForm">Annuler</button>
        </div>
      </form>

      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Slug</th>
            <th>Robots</th>
            <th>Ordre</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in categories" :key="c.id">
            <td>{{ c.id }}</td>
            <td class="title-cell">{{ c.nom }}</td>
            <td><code class="slug-code">{{ c.slug }}</code></td>
            <td>
              <span :class="['robots-badge', c.meta_robots === 'noindex' ? 'noindex' : 'index']">
                {{ c.meta_robots === 'noindex' ? 'Noindex' : 'Index' }}
              </span>
            </td>
            <td>{{ c.ordre }}</td>
            <td>
              <AdminActionsButtons
                :item="c"
                :actions="['edit', 'delete']"
                edit-label="Éditer"
                confirm-message="Supprimer cette catégorie ?"
                @edit="editCategory"
                @delete="handleDeleteCategory"
              />
            </td>
          </tr>
          <tr v-if="!categories.length">
            <td colspan="6" class="empty-row">Aucune catégorie</td>
          </tr>
        </tbody>
      </table>
    </template>

    <!-- ═══════ TAGS ═══════ -->
    <template v-if="activeTab === 'tags'">
      <form class="admin-form" @submit.prevent="handleSaveTag">
        <h3 class="form-section-title">{{ tagForm.id ? 'Modifier le tag' : 'Nouveau tag' }}</h3>

        <div class="form-group">
          <label>Nom <span class="required">*</span></label>
          <input v-model="tagForm.nom" placeholder="Ex: MPSI" required />
        </div>

        <div class="form-group">
          <label>Slug</label>
          <input v-model="tagForm.slug" placeholder="Auto-généré depuis le nom si vide" />
          <small class="field-hint">URL-friendly. Laisser vide = auto.</small>
        </div>

        <div class="form-group">
          <label>Meta description SEO</label>
          <input v-model="tagForm.meta_description" placeholder="Description SEO (max 160 car.)" maxlength="160" />
        </div>

        <div class="form-group">
          <label>Meta robots</label>
          <select v-model="tagForm.meta_robots">
            <option value="index">Index (visible Google)</option>
            <option value="noindex">Noindex (masqué Google)</option>
          </select>
        </div>

        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ tagForm.id ? 'Mettre à jour' : 'Créer' }}</button>
          <button v-if="tagForm.id" class="btn-danger" type="button" @click="resetTagForm">Annuler</button>
        </div>
      </form>

      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom</th>
            <th>Slug</th>
            <th>Robots</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in tags" :key="t.id">
            <td>{{ t.id }}</td>
            <td class="title-cell">{{ t.nom }}</td>
            <td><code class="slug-code">{{ t.slug }}</code></td>
            <td>
              <span :class="['robots-badge', t.meta_robots === 'noindex' ? 'noindex' : 'index']">
                {{ t.meta_robots === 'noindex' ? 'Noindex' : 'Index' }}
              </span>
            </td>
            <td>
              <AdminActionsButtons
                :item="t"
                :actions="['edit', 'delete']"
                edit-label="Éditer"
                confirm-message="Supprimer ce tag ?"
                @edit="editTag"
                @delete="handleDeleteTag"
              />
            </td>
          </tr>
          <tr v-if="!tags.length">
            <td colspan="5" class="empty-row">Aucun tag</td>
          </tr>
        </tbody>
      </table>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import {
  getAdminBlogPosts, createBlogPost, updateBlogPost, deleteBlogPost,
  getAdminBlogCategories, createBlogCategory, updateBlogCategory, deleteBlogCategory,
  getAdminBlogTags, createBlogTag, updateBlogTag, deleteBlogTag,
} from '@/api/blog'
import { AdminActionsButtons } from '@/components/admin'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

const activeTab = ref('posts')

// ── Data ──────────────────────────────────────────────────────────
const posts = ref([])
const categories = ref([])
const tags = ref([])
const isLoadingPosts = ref(false)

// ── Filters ───────────────────────────────────────────────────────
const filterCategorie = ref('all')
const filterStatut = ref('all')
const filterSearch = ref('')

const filteredPosts = computed(() => {
  let result = posts.value
  if (filterCategorie.value !== 'all') {
    result = result.filter(p => p.categorie === filterCategorie.value)
  }
  if (filterStatut.value !== 'all') {
    result = result.filter(p => p.statut === filterStatut.value)
  }
  if (filterSearch.value.trim()) {
    const q = filterSearch.value.toLowerCase()
    result = result.filter(p => (p.titre || '').toLowerCase().includes(q))
  }
  return result
})

// ── Post form ─────────────────────────────────────────────────────
const emptyPost = () => ({
  id: null, titre: '', slug: '', extrait: '', contenu: '',
  categorie: null, tags_ids: [], statut: 'draft',
  seo_title: '', meta_description: '', og_title: '', og_description: '',
  alt_text_image: '', meta_robots: 'index',
  _coverFile: null, _coverPreview: '', _ogFile: null, _ogPreview: '',
})
const postForm = ref(emptyPost())
const selectedTagId = ref('')
const showPreview = ref(false)
const previewHtml = ref('')

const previewCategorie = computed(() => {
  if (!postForm.value.categorie) return ''
  const cat = categories.value.find(c => c.id === postForm.value.categorie)
  return cat ? cat.nom : ''
})

function handlePreview() {
  try {
    previewHtml.value = renderContentWithImages(postForm.value.contenu, [])
    showPreview.value = true
    nextTick(() => renderMath())
  } catch (e) {
    console.error('Erreur prévisualisation:', e)
  }
}

function onCoverImageChange(e) {
  const file = e.target.files?.[0]
  if (file) {
    postForm.value._coverFile = file
    postForm.value._coverPreview = URL.createObjectURL(file)
  }
}

function onOgImageChange(e) {
  const file = e.target.files?.[0]
  if (file) {
    postForm.value._ogFile = file
    postForm.value._ogPreview = URL.createObjectURL(file)
  }
}

const availableTags = computed(() =>
  tags.value.filter(t => !postForm.value.tags_ids.includes(t.id))
)

function tagNameById(id) {
  return tags.value.find(t => t.id === id)?.nom || id
}

function addTag() {
  if (selectedTagId.value && !postForm.value.tags_ids.includes(Number(selectedTagId.value))) {
    postForm.value.tags_ids.push(Number(selectedTagId.value))
  }
  selectedTagId.value = ''
}

function removeTag(id) {
  postForm.value.tags_ids = postForm.value.tags_ids.filter(t => t !== id)
}

function resetPostForm() {
  postForm.value = emptyPost()
  selectedTagId.value = ''
  showPreview.value = false
  previewHtml.value = ''
}

function editPost(post) {
  postForm.value = {
    id: post.id,
    titre: post.titre || '',
    slug: post.slug || '',
    extrait: post.extrait || '',
    contenu: post.contenu || '',
    categorie: post.categorie || null,
    tags_ids: (post.tags_ids || []).map(Number),
    statut: post.statut || 'draft',
    seo_title: post.seo_title || '',
    meta_description: post.meta_description || '',
    og_title: post.og_title || '',
    og_description: post.og_description || '',
    alt_text_image: post.alt_text_image || '',
    meta_robots: post.meta_robots || 'index',
    _coverFile: null,
    _coverPreview: post.image_couverture_url || '',
    _ogFile: null,
    _ogPreview: post.og_image_url || '',
  }
  selectedTagId.value = ''
  activeTab.value = 'posts'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSavePost() {
  if (!postForm.value.titre) return
  try {
    const fd = new FormData()
    fd.append('titre', postForm.value.titre)
    if (postForm.value.slug) fd.append('slug', postForm.value.slug)
    fd.append('extrait', postForm.value.extrait)
    fd.append('contenu', postForm.value.contenu)
    if (postForm.value.categorie) fd.append('categorie', postForm.value.categorie)
    fd.append('statut', postForm.value.statut)
    fd.append('seo_title', postForm.value.seo_title)
    fd.append('meta_description', postForm.value.meta_description)
    fd.append('og_title', postForm.value.og_title)
    fd.append('og_description', postForm.value.og_description)
    fd.append('alt_text_image', postForm.value.alt_text_image)
    fd.append('meta_robots', postForm.value.meta_robots)
    for (const tid of postForm.value.tags_ids) {
      fd.append('tags_ids', tid)
    }
    if (postForm.value._coverFile) {
      fd.append('image_couverture', postForm.value._coverFile)
    }
    if (postForm.value._ogFile) {
      fd.append('og_image', postForm.value._ogFile)
    }
    if (postForm.value.id) {
      await updateBlogPost(postForm.value.id, fd)
    } else {
      await createBlogPost(fd)
    }
    resetPostForm()
    await loadPosts()
  } catch (e) {
    console.error('Erreur sauvegarde article:', e)
  }
}

async function handleDeletePost(post) {
  try {
    await deleteBlogPost(post.id)
    await loadPosts()
  } catch (e) {
    console.error('Erreur suppression article:', e)
  }
}

// ── Category form ─────────────────────────────────────────────────
const emptyCat = () => ({ id: null, nom: '', slug: '', description: '', meta_description: '', meta_robots: 'index', ordre: 0 })
const catForm = ref(emptyCat())

function resetCatForm() { catForm.value = emptyCat() }

function editCategory(cat) {
  catForm.value = {
    id: cat.id, nom: cat.nom, slug: cat.slug,
    description: cat.description || '', meta_description: cat.meta_description || '',
    meta_robots: cat.meta_robots || 'index', ordre: cat.ordre || 0
  }
  activeTab.value = 'categories'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSaveCategory() {
  if (!catForm.value.nom) return
  try {
    const payload = { ...catForm.value }
    delete payload.id
    if (catForm.value.id) {
      await updateBlogCategory(catForm.value.id, payload)
    } else {
      await createBlogCategory(payload)
    }
    resetCatForm()
    await loadCategories()
  } catch (e) {
    console.error('Erreur sauvegarde catégorie:', e)
  }
}

async function handleDeleteCategory(cat) {
  try {
    await deleteBlogCategory(cat.id)
    await loadCategories()
  } catch (e) {
    console.error('Erreur suppression catégorie:', e)
  }
}

// ── Tag form ──────────────────────────────────────────────────────
const emptyTag = () => ({ id: null, nom: '', slug: '', meta_description: '', meta_robots: 'index' })
const tagForm = ref(emptyTag())

function resetTagForm() { tagForm.value = emptyTag() }

function editTag(tag) {
  tagForm.value = {
    id: tag.id, nom: tag.nom, slug: tag.slug,
    meta_description: tag.meta_description || '', meta_robots: tag.meta_robots || 'index'
  }
  activeTab.value = 'tags'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSaveTag() {
  if (!tagForm.value.nom) return
  try {
    const payload = { ...tagForm.value }
    delete payload.id
    if (tagForm.value.id) {
      await updateBlogTag(tagForm.value.id, payload)
    } else {
      await createBlogTag(payload)
    }
    resetTagForm()
    await loadTags()
  } catch (e) {
    console.error('Erreur sauvegarde tag:', e)
  }
}

async function handleDeleteTag(tag) {
  try {
    await deleteBlogTag(tag.id)
    await loadTags()
  } catch (e) {
    console.error('Erreur suppression tag:', e)
  }
}

// ── Loaders ───────────────────────────────────────────────────────
async function loadPosts() {
  isLoadingPosts.value = true
  try {
    const { data } = await getAdminBlogPosts()
    posts.value = data || []
  } catch (e) {
    console.error('Erreur chargement articles:', e)
    posts.value = []
  } finally {
    isLoadingPosts.value = false
  }
}

async function loadCategories() {
  try {
    const { data } = await getAdminBlogCategories()
    categories.value = data || []
  } catch (e) {
    console.error('Erreur chargement catégories:', e)
    categories.value = []
  }
}

async function loadTags() {
  try {
    const { data } = await getAdminBlogTags()
    tags.value = data || []
  } catch (e) {
    console.error('Erreur chargement tags:', e)
    tags.value = []
  }
}

onMounted(async () => {
  await Promise.all([loadPosts(), loadCategories(), loadTags()])
})
</script>

<style scoped>
/* ============================================================================
   TITRE PRINCIPAL
   ============================================================================ */
.admin-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

/* ============================================================================
   ONGLETS
   ============================================================================ */
.blog-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #374151;
  background: #f9fafb;
}

.tab-btn.active {
  color: #2563eb;
  border-bottom-color: #2563eb;
}

.tab-icon {
  font-size: 1rem;
}

.tab-count {
  background: #e5e7eb;
  color: #374151;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 1px 7px;
  border-radius: 9999px;
  min-width: 20px;
  text-align: center;
}

.tab-btn.active .tab-count {
  background: #dbeafe;
  color: #2563eb;
}

/* ============================================================================
   FORMULAIRE
   ============================================================================ */
.admin-form {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 1.25rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.375rem;
  color: #374151;
  font-size: 0.875rem;
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-family: inherit;
  transition: border-color 0.15s, box-shadow 0.15s;
  background: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
  font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
  line-height: 1.5;
}

.field-hint {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #9ca3af;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

/* ============================================================================
   TAGS CHIPS
   ============================================================================ */
.tags-select-row {
  display: flex;
  gap: 0.5rem;
}

.tags-select-row select {
  flex: 1;
}

.btn-tag-add {
  width: 40px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: background 0.15s;
}

.btn-tag-add:hover:not(:disabled) {
  background: #2563eb;
}

.btn-tag-add:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: #eef2ff;
  color: #3730a3;
  border: 1px solid #c7d2fe;
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.chip-remove {
  border: none;
  background: transparent;
  color: #4f46e5;
  cursor: pointer;
  font-size: 0.875rem;
  padding: 0;
  line-height: 1;
}

.chip-remove:hover {
  color: #ef4444;
}

/* ============================================================================
   IMAGE UPLOAD
   ============================================================================ */
.image-upload-zone {
  border: 2px dashed #d1d5db;
  border-radius: 0.5rem;
  padding: 0.75rem;
  background: #f9fafb;
  transition: border-color 0.2s;
}

.image-upload-zone:hover {
  border-color: #3b82f6;
}

.image-upload-zone input[type="file"] {
  width: 100%;
  font-size: 0.875rem;
  border: none;
  padding: 0;
}

.image-preview-lg {
  display: block;
  max-width: 280px;
  max-height: 160px;
  margin-top: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  object-fit: cover;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* ============================================================================
   SEO ACCORDION
   ============================================================================ */
.seo-accordion {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: #f9fafb;
  overflow: hidden;
}

.seo-accordion summary {
  cursor: pointer;
  padding: 0.75rem 1rem;
  font-weight: 500;
  font-size: 0.875rem;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  user-select: none;
  transition: background 0.15s;
}

.seo-accordion summary:hover {
  background: #f3f4f6;
}

.seo-icon {
  font-size: 1rem;
}

.seo-arrow {
  margin-left: auto;
  transition: transform 0.2s;
  font-size: 0.75rem;
}

.seo-accordion[open] .seo-arrow {
  transform: rotate(90deg);
}

.seo-content {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background: white;
}

/* ============================================================================
   BOUTONS
   ============================================================================ */
.btn-primary,
.btn-secondary,
.btn-danger {
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: background-color 0.15s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #4b5563;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-primary:disabled,
.btn-secondary:disabled,
.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ============================================================================
   FILTRES
   ============================================================================ */
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 160px;
}

.filter-group label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #6b7280;
}

.filter-group select,
.filter-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
}

.filter-input {
  min-width: 200px;
}

/* ============================================================================
   TABLEAU
   ============================================================================ */
.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.admin-table th,
.admin-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.admin-table th {
  background: #f9fafb;
  font-weight: 600;
  font-size: 0.8rem;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.admin-table tr:hover {
  background: #f9fafb;
}

.title-cell {
  font-weight: 500;
  color: #1f2937;
  max-width: 300px;
}

.slug-code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 0.8rem;
  color: #475569;
}

.loading-row {
  text-align: center;
  color: #6b7280;
  font-style: italic;
  padding: 2rem 0.75rem !important;
}

.empty-row {
  text-align: center;
  color: #9ca3af;
  font-style: italic;
  padding: 2rem 0.75rem !important;
}

.pagination-info {
  text-align: center;
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.75rem;
  margin-bottom: 1.5rem;
}

/* ============================================================================
   BADGES
   ============================================================================ */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.2rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.published {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.draft {
  background: #fef3c7;
  color: #92400e;
}

.robots-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 600;
}

.robots-badge.index {
  background: #d1fae5;
  color: #065f46;
}

.robots-badge.noindex {
  background: #fee2e2;
  color: #991b1b;
}

/* ============================================================================
   PREVIEW
   ============================================================================ */
.preview-section {
  margin-top: 1.5rem;
  margin-bottom: 2rem;
  border: 2px solid #3b82f6;
  border-radius: 0.5rem;
  overflow: hidden;
  background: white;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.preview-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.25rem;
  background: #eff6ff;
  border-bottom: 1px solid #bfdbfe;
}

.preview-header-bar h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e40af;
}

.btn-close-preview {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: transparent;
  border: 1px solid #93c5fd;
  color: #2563eb;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 500;
  transition: background 0.15s;
}

.btn-close-preview:hover {
  background: #dbeafe;
}

.preview-article {
  padding: 1.5rem 2rem;
}

.preview-meta {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.preview-cat {
  background: #f3f4f6;
  color: #374151;
  padding: 0.15rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.preview-tags {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.preview-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.75rem;
  line-height: 1.3;
}

.preview-excerpt {
  font-size: 1rem;
  color: #6b7280;
  margin: 0 0 1.25rem;
  line-height: 1.6;
  font-style: italic;
}

.preview-content {
  font-size: 0.95rem;
  line-height: 1.75;
  color: #374151;
}

.preview-content :deep(h1),
.preview-content :deep(h2),
.preview-content :deep(h3) {
  color: #111827;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.preview-content :deep(h2) {
  font-size: 1.375rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.375rem;
}

.preview-content :deep(h3) {
  font-size: 1.125rem;
}

.preview-content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  font-size: 0.8rem;
}

.preview-content :deep(code) {
  background: #f1f5f9;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.preview-content :deep(pre code) {
  background: transparent;
  padding: 0;
}

.preview-content :deep(blockquote) {
  border-left: 4px solid #2563eb;
  padding: 0.5rem 1rem;
  margin: 1rem 0;
  background: #f8fafc;
  color: #475569;
}

.preview-content :deep(ul),
.preview-content :deep(ol) {
  padding-left: 1.5rem;
}

.preview-content :deep(img) {
  max-width: 100%;
  border-radius: 0.5rem;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */
@media (max-width: 768px) {
  .form-row-2 {
    grid-template-columns: 1fr;
  }

  .filters {
    flex-direction: column;
  }

  .filter-group {
    width: 100%;
  }

  .blog-tabs {
    overflow-x: auto;
  }

  .preview-article {
    padding: 1rem;
  }

  .preview-title {
    font-size: 1.375rem;
  }

  .admin-table {
    font-size: 0.8rem;
  }
}
</style>
