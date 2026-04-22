<template>
  <div>
    <FormatHelp v-if="activeTab === 'posts'" :format-template="BLOG_FORMAT_TEMPLATE">
      <template #notes>
        <ul>
          <li>Tu peux mixer Markdown, LaTeX et HTML dans <code>Contenu</code></li>
          <li>Image Markdown: <code>![alt](https://...)</code></li>
          <li>Vid&eacute;o YouTube: colle un bloc <code>&lt;iframe ...&gt;&lt;/iframe&gt;</code></li>
          <li>Bouton: utilise le lien HTML avec style inline montr&eacute; dans le template</li>
          <li>Toujours v&eacute;rifier avec le bouton <strong>Pr&eacute;visualiser</strong></li>
        </ul>
      </template>
    </FormatHelp>
    
    <h2 class="admin-title">Gestion du Blog</h2>

    <div class="blog-tabs">
      <button :class="['tab-btn', { active: activeTab === 'posts' }]" @click="activeTab = 'posts'">
        <span class="tab-icon">A</span> Articles
        <span class="tab-count" v-if="posts.length">{{ posts.length }}</span>
      </button>
      <button :class="['tab-btn', { active: activeTab === 'categories' }]" @click="activeTab = 'categories'">
        <span class="tab-icon">C</span> Chapitres
        <span class="tab-count" v-if="categories.length">{{ categories.length }}</span>
      </button>
      <button :class="['tab-btn', { active: activeTab === 'niveaux' }]" @click="activeTab = 'niveaux'">
        <span class="tab-icon">N</span> Niveaux
        <span class="tab-count" v-if="niveaux.length">{{ niveaux.length }}</span>
      </button>
      <button :class="['tab-btn', { active: activeTab === 'types' }]" @click="activeTab = 'types'">
        <span class="tab-icon">T</span> Types de contenu
        <span class="tab-count" v-if="contentTypes.length">{{ contentTypes.length }}</span>
      </button>
      <button :class="['tab-btn', { active: activeTab === 'tags' }]" @click="activeTab = 'tags'">
        <span class="tab-icon">#</span> Tags
        <span class="tab-count" v-if="tags.length">{{ tags.length }}</span>
      </button>
    </div>

    <template v-if="activeTab === 'posts'">
      <form class="admin-form" @submit.prevent="handleSavePost">
        <h3 class="form-section-title">{{ postForm.id ? 'Modifier article' : 'Nouvel article' }}</h3>

        <div class="form-group">
          <label>Titre de l'article <span class="required">*</span></label>
          <input v-model="postForm.titre" placeholder="Ex: 5 astuces pour r&eacute;ussir sa pr&eacute;pa MPSI" required />
        </div>

        <div class="form-group">
          <label>Slug</label>
          <input v-model="postForm.slug" placeholder="Auto-g&eacute;n&eacute;r&eacute; depuis le titre si vide" />
          <small class="field-hint">URL de l'article. Laisser vide = auto.</small>
        </div>

        <div class="form-group">
          <label class="label-with-counter">
            <span>Extrait</span>
            <span :class="counterClass(postForm.extrait.length, 120, 220, 400)">
              {{ postForm.extrait.length }}/400 (id&eacute;al 120-220)
            </span>
          </label>
          <input v-model="postForm.extrait" placeholder="R&eacute;sum&eacute; court affich&eacute; dans la liste du blog" maxlength="400" />
          <small class="field-hint">Max 400 car. Affich&eacute; dans les cartes du blog.</small>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label>Cat&eacute;gorie (chapitre)</label>
            <select v-model="postForm.categorie">
              <option :value="null">- Aucun chapitre -</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Niveau (classe)</label>
            <select v-model="postForm.niveau">
              <option :value="null">- Aucun niveau -</option>
              <option v-for="n in niveaux" :key="n.id" :value="n.id">{{ n.nom }}</option>
            </select>
          </div>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label>Type de contenu</label>
            <select v-model="postForm.type_contenu">
              <option :value="null">- Aucun type -</option>
              <option v-for="t in contentTypes" :key="t.id" :value="t.id">{{ t.nom }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Statut</label>
            <select v-model="postForm.statut">
              <option value="draft">Brouillon</option>
              <option value="published">Publi&eacute;</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Tags</label>
          <div class="tags-select-row">
            <select v-model="selectedTagId">
              <option value="">Ajouter un tag...</option>
              <option v-for="t in availableTags" :key="t.id" :value="t.id">{{ t.nom }}</option>
            </select>
            <button class="btn-tag-add" type="button" @click="addTag" :disabled="!selectedTagId">+</button>
          </div>
          <div class="chips" v-if="postForm.tags_ids.length">
            <span class="chip" v-for="tid in postForm.tags_ids" :key="tid">
              {{ tagNameById(tid) }}
              <button class="chip-remove" type="button" @click="removeTag(tid)">x</button>
            </span>
          </div>
        </div>

        <div class="form-group">
          <label>Contenu <span class="required">*</span></label>
          <textarea v-model="postForm.contenu" placeholder="R&eacute;digez en Markdown ($formules$ LaTeX support&eacute;es)" rows="14"></textarea>
          <small class="field-hint">Supporte Markdown, LaTeX ($formule$) et HTML.</small>
        </div>

        <div class="form-group">
          <label>Image de couverture</label>
          <div class="image-upload-zone">
            <input type="file" accept="image/*" @change="onCoverImageChange" />
            <img v-if="postForm._coverPreview" :src="postForm._coverPreview" class="image-preview-lg" />
          </div>
        </div>

        <div class="form-group">
          <label>Alt text image</label>
          <input v-model="postForm.alt_text_image" placeholder="Description textuelle de l'image (accessibilit&eacute; + SEO)" maxlength="250" />
          <small class="field-hint">Max 250 car.</small>
        </div>

        <details class="seo-accordion">
          <summary>
            <span class="seo-icon">SEO</span> SEO (optionnel)
            <span class="seo-arrow">></span>
          </summary>
          <div class="seo-content">
            <div class="form-row-2">
              <div class="form-group">
                <label class="label-with-counter">
                  <span>Titre SEO</span>
                  <span :class="counterClass(postForm.seo_title.length, 50, 65, 70)">
                    {{ postForm.seo_title.length }}/70 (id&eacute;al 50-65)
                  </span>
                </label>
                <input v-model="postForm.seo_title" placeholder="Titre dans l'onglet Google" maxlength="70" />
              </div>
              <div class="form-group">
                <label class="label-with-counter">
                  <span>Meta description</span>
                  <span :class="counterClass(postForm.meta_description.length, 140, 160, 160)">
                    {{ postForm.meta_description.length }}/160 (id&eacute;al 140-160)
                  </span>
                </label>
                <input v-model="postForm.meta_description" placeholder="Description sous le lien Google" maxlength="160" />
              </div>
            </div>
            <div class="form-row-2">
              <div class="form-group">
                <label>OG Title</label>
                <input v-model="postForm.og_title" placeholder="Titre sur Facebook/LinkedIn" maxlength="100" />
              </div>
              <div class="form-group">
                <label>OG Description</label>
                <input v-model="postForm.og_description" placeholder="Description sur les r&eacute;seaux" maxlength="200" />
              </div>
            </div>
            <div class="form-group">
              <label>Image OG (Open Graph)</label>
              <div class="image-upload-zone">
                <input type="file" accept="image/*" @change="onOgImageChange" />
                <img v-if="postForm._ogPreview" :src="postForm._ogPreview" class="image-preview-lg" />
              </div>
            </div>
            <div class="form-group">
              <label>Meta robots</label>
              <select v-model="postForm.meta_robots">
                <option value="index">Index (visible Google)</option>
                <option value="noindex">Noindex (masque Google)</option>
              </select>
            </div>
          </div>
        </details>

        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ postForm.id ? 'Mettre \u00e0 jour' : 'Cr\u00e9er' }}</button>
          <button class="btn-secondary" type="button" @click="handlePreview" :disabled="!postForm.contenu.trim()">Pr\u00e9visualiser</button>
          <button v-if="postForm.id" class="btn-danger" type="button" @click="resetPostForm">Annuler</button>
        </div>
      </form>

      <div v-if="showPreview" class="preview-section">
        <div class="preview-header-bar">
          <h3>Aper\u00e7u de l'article {{ postForm.id ? '(Mode \u00e9dition)' : '(Mode cr\u00e9ation)' }}</h3>
          <button class="btn-close-preview" @click="showPreview = false">Fermer</button>
        </div>
        <div class="preview-article">
          <div class="preview-meta">
            <span :class="['status-badge', postForm.statut]">{{ postForm.statut === 'published' ? 'Publi\u00e9' : 'Brouillon' }}</span>
            <span v-if="previewCategorie" class="preview-cat">{{ previewCategorie }}</span>
            <span v-if="previewNiveau" class="preview-taxonomy">{{ previewNiveau }}</span>
            <span v-if="previewTypeContenu" class="preview-taxonomy">{{ previewTypeContenu }}</span>
            <span v-if="postForm.tags_ids.length" class="preview-tags">
              <span class="chip" v-for="tid in postForm.tags_ids" :key="tid">{{ tagNameById(tid) }}</span>
            </span>
          </div>
          <h1 class="preview-title">{{ postForm.titre || 'Sans titre' }}</h1>
          <p v-if="postForm.extrait" class="preview-excerpt">{{ postForm.extrait }}</p>
          <div class="preview-content" v-html="previewHtml"></div>
        </div>
      </div>

      <div class="filters">
        <div class="filter-group">
          <label>Filtrer par cat&eacute;gorie</label>
          <select v-model="filterCategorie">
            <option value="all">Toutes les cat&eacute;gories</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Filtrer par niveau</label>
          <select v-model="filterNiveau">
            <option value="all">Tous les niveaux</option>
            <option v-for="n in niveaux" :key="n.id" :value="n.id">{{ n.nom }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Filtrer par type</label>
          <select v-model="filterTypeContenu">
            <option value="all">Tous les types</option>
            <option v-for="t in contentTypes" :key="t.id" :value="t.id">{{ t.nom }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Filtrer par statut</label>
          <select v-model="filterStatut">
            <option value="all">Tous les statuts</option>
            <option value="published">Publi\u00e9</option>
            <option value="draft">Brouillon</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Rechercher</label>
          <input v-model="filterSearch" type="text" placeholder="Recherche par titre..." class="filter-input" />
        </div>
      </div>

      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Cat&eacute;gorie</th>
            <th>Niveau</th>
            <th>Type</th>
            <th>Statut</th>
            <th>Date publication</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoadingPosts">
            <td colspan="8" class="loading-row">Chargement des articles...</td>
          </tr>
          <template v-else>
            <tr v-for="p in filteredPosts" :key="p.id">
              <td>{{ p.id }}</td>
              <td class="title-cell">{{ p.titre }}</td>
              <td>{{ p.categorie_nom || '-' }}</td>
              <td>{{ p.niveau_nom || niveauLabel(p.niveau) || '-' }}</td>
              <td>{{ p.type_contenu_nom || typeContenuLabel(p.type_contenu) || '-' }}</td>
              <td><span :class="['status-badge', p.statut]">{{ p.statut === 'published' ? 'Publi\u00e9' : 'Brouillon' }}</span></td>
              <td>{{ formatDate(p.date_publication) }}</td>
              <td>
                <AdminActionsButtons
                  :item="p"
                  :actions="['edit', 'delete']"
                  edit-label="&Eacute;diter"
                  confirm-message="Supprimer cet article ?"
                  @edit="editPost"
                  @delete="handleDeletePost"
                />
              </td>
            </tr>
            <tr v-if="filteredPosts.length === 0">
              <td colspan="8" class="empty-row">Aucun article trouv&eacute;.</td>
            </tr>
          </template>
        </tbody>
      </table>
    </template>

    <template v-if="activeTab === 'categories'">
      <form class="admin-form" @submit.prevent="handleSaveCategory">
        <h3 class="form-section-title">{{ catForm.id ? 'Modifier le chapitre' : 'Nouveau chapitre' }}</h3>
        <div class="form-group">
          <label>Nom <span class="required">*</span></label>
          <input v-model="catForm.nom" required />
        </div>
        <div class="form-group">
          <label>Slug</label>
          <input v-model="catForm.slug" placeholder="Auto-g&eacute;n&eacute;r&eacute; depuis le nom si vide" />
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="catForm.description" rows="2"></textarea>
        </div>
        <div class="form-group">
          <label>Meta description</label>
          <input v-model="catForm.meta_description" maxlength="160" />
        </div>
        <div class="form-row-2">
          <div class="form-group">
            <label>Meta robots</label>
            <select v-model="catForm.meta_robots">
              <option value="index">Index</option>
              <option value="noindex">Noindex</option>
            </select>
          </div>
          <div class="form-group">
            <label>Ordre</label>
            <input v-model.number="catForm.ordre" type="number" min="0" />
          </div>
        </div>
        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ catForm.id ? 'Mettre \u00e0 jour' : 'Cr\u00e9er' }}</button>
          <button v-if="catForm.id" class="btn-danger" type="button" @click="resetCatForm">Annuler</button>
        </div>
      </form>

      <table class="admin-table">
        <thead>
          <tr><th>ID</th><th>Nom</th><th>Slug</th><th>Description</th><th>Robots</th><th>Actions</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in categories" :key="c.id">
            <td>{{ c.id }}</td>
            <td class="title-cell">{{ c.nom }}</td>
            <td><code class="slug-code">{{ c.slug }}</code></td>
            <td>{{ c.description || '-' }}</td>
            <td><span :class="['robots-badge', c.meta_robots === 'noindex' ? 'noindex' : 'index']">{{ c.meta_robots === 'noindex' ? 'Noindex' : 'Index' }}</span></td>
            <td>
              <AdminActionsButtons
                :item="c"
                :actions="['edit', 'delete']"
                edit-label="&Eacute;diter"
                confirm-message="Supprimer ce chapitre ?"
                @edit="editCategory"
                @delete="handleDeleteCategory"
              />
            </td>
          </tr>
          <tr v-if="!categories.length"><td colspan="6" class="empty-row">Aucun chapitre</td></tr>
        </tbody>
      </table>
    </template>

    <template v-if="activeTab === 'niveaux'">
      <form class="admin-form" @submit.prevent="handleSaveNiveau">
        <h3 class="form-section-title">{{ niveauForm.id ? 'Modifier niveau' : 'Nouveau niveau' }}</h3>
        <div class="form-group">
          <label>Nom <span class="required">*</span></label>
          <input v-model="niveauForm.nom" required />
        </div>
        <div class="form-group">
          <label>Slug</label>
          <input v-model="niveauForm.slug" placeholder="Auto-g&eacute;n&eacute;r&eacute; depuis le nom si vide" />
        </div>
        <div class="form-group">
          <label>Ordre</label>
          <input v-model.number="niveauForm.ordre" type="number" min="0" />
        </div>
        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ niveauForm.id ? 'Mettre \u00e0 jour' : 'Cr\u00e9er' }}</button>
          <button v-if="niveauForm.id" class="btn-danger" type="button" @click="resetNiveauForm">Annuler</button>
        </div>
      </form>

      <table class="admin-table">
        <thead><tr><th>ID</th><th>Nom</th><th>Slug</th><th>Ordre</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="n in niveaux" :key="n.id">
            <td>{{ n.id }}</td>
            <td class="title-cell">{{ n.nom }}</td>
            <td><code class="slug-code">{{ n.slug }}</code></td>
            <td>{{ n.ordre }}</td>
            <td>
              <AdminActionsButtons
                :item="n"
                :actions="['edit', 'delete']"
                edit-label="&Eacute;diter"
                confirm-message="Supprimer ce niveau ?"
                @edit="editNiveau"
                @delete="handleDeleteNiveau"
              />
            </td>
          </tr>
          <tr v-if="!niveaux.length"><td colspan="5" class="empty-row">Aucun niveau</td></tr>
        </tbody>
      </table>
    </template>

    <template v-if="activeTab === 'types'">
      <form class="admin-form" @submit.prevent="handleSaveContentType">
        <h3 class="form-section-title">{{ contentTypeForm.id ? 'Modifier type' : 'Nouveau type de contenu' }}</h3>
        <div class="form-group">
          <label>Nom <span class="required">*</span></label>
          <input v-model="contentTypeForm.nom" required />
        </div>
        <div class="form-group">
          <label>Slug</label>
          <input v-model="contentTypeForm.slug" placeholder="Auto-g&eacute;n&eacute;r&eacute; depuis le nom si vide" />
        </div>
        <div class="form-group">
          <label>Ordre</label>
          <input v-model.number="contentTypeForm.ordre" type="number" min="0" />
        </div>
        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ contentTypeForm.id ? 'Mettre \u00e0 jour' : 'Cr\u00e9er' }}</button>
          <button v-if="contentTypeForm.id" class="btn-danger" type="button" @click="resetContentTypeForm">Annuler</button>
        </div>
      </form>

      <table class="admin-table">
        <thead><tr><th>ID</th><th>Nom</th><th>Slug</th><th>Ordre</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="t in contentTypes" :key="t.id">
            <td>{{ t.id }}</td>
            <td class="title-cell">{{ t.nom }}</td>
            <td><code class="slug-code">{{ t.slug }}</code></td>
            <td>{{ t.ordre }}</td>
            <td>
              <AdminActionsButtons
                :item="t"
                :actions="['edit', 'delete']"
                edit-label="&Eacute;diter"
                confirm-message="Supprimer ce type de contenu ?"
                @edit="editContentType"
                @delete="handleDeleteContentType"
              />
            </td>
          </tr>
          <tr v-if="!contentTypes.length"><td colspan="5" class="empty-row">Aucun type de contenu</td></tr>
        </tbody>
      </table>
    </template>

    <template v-if="activeTab === 'tags'">
      <form class="admin-form" @submit.prevent="handleSaveTag">
        <h3 class="form-section-title">{{ tagForm.id ? 'Modifier tag' : 'Nouveau tag' }}</h3>
        <div class="form-group">
          <label>Nom <span class="required">*</span></label>
          <input v-model="tagForm.nom" required />
        </div>
        <div class="form-group">
          <label>Slug</label>
          <input v-model="tagForm.slug" placeholder="Auto-g&eacute;n&eacute;r&eacute; depuis le nom si vide" />
        </div>
        <div class="form-group">
          <label>Meta description</label>
          <input v-model="tagForm.meta_description" maxlength="160" />
        </div>
        <div class="form-group">
          <label>Meta robots</label>
          <select v-model="tagForm.meta_robots">
            <option value="index">Index</option>
            <option value="noindex">Noindex</option>
          </select>
        </div>
        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ tagForm.id ? 'Mettre \u00e0 jour' : 'Cr\u00e9er' }}</button>
          <button v-if="tagForm.id" class="btn-danger" type="button" @click="resetTagForm">Annuler</button>
        </div>
      </form>

      <table class="admin-table">
        <thead><tr><th>ID</th><th>Nom</th><th>Slug</th><th>Robots</th><th>Actions</th></tr></thead>
        <tbody>
          <tr v-for="t in tags" :key="t.id">
            <td>{{ t.id }}</td>
            <td class="title-cell">{{ t.nom }}</td>
            <td><code class="slug-code">{{ t.slug }}</code></td>
            <td><span :class="['robots-badge', t.meta_robots === 'noindex' ? 'noindex' : 'index']">{{ t.meta_robots === 'noindex' ? 'Noindex' : 'Index' }}</span></td>
            <td>
              <AdminActionsButtons
                :item="t"
                :actions="['edit', 'delete']"
                edit-label="&Eacute;diter"
                confirm-message="Supprimer ce tag ?"
                @edit="editTag"
                @delete="handleDeleteTag"
              />
            </td>
          </tr>
          <tr v-if="!tags.length"><td colspan="5" class="empty-row">Aucun tag</td></tr>
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
  getAdminBlogNiveaux, createBlogNiveau, updateBlogNiveau, deleteBlogNiveau,
  getAdminBlogContentTypes, createBlogContentType, updateBlogContentType, deleteBlogContentType,
} from '@/api/blog'
import { AdminActionsButtons } from '@/components/admin'
import FormatHelp from '@/components/admin/FormatHelp.vue'
import { renderContentWithImages, renderMath } from '@/utils/scientificRenderer'

const BLOG_FORMAT_TEMPLATE = `# Titre de l'article

## Introduction
Explique en 3-4 phrases l'objectif du chapitre.

## Methode
- Etape 1
- Etape 2
- Etape 3

## Exemple
![Texte alternatif image](https://www.exemple.com/image.jpg)

## Video explicative
<iframe width="100%" height="380" src="https://www.youtube.com/embed/VIDEO_ID" title="Video explicative" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Lien utile
[Voir la fiche complete](https://www.exemple.com)

## Bouton CTA
<a href="https://www.exemple.com" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:10px 16px;border-radius:8px;background:#1d4ed8;color:#ffffff;text-decoration:none;font-weight:600;">Voir l'exercice complet</a>

---

## Conclusion
Resume les points cles et la prochaine etape.`

const activeTab = ref('posts')
const posts = ref([])
const categories = ref([])
const niveaux = ref([])
const contentTypes = ref([])
const tags = ref([])
const isLoadingPosts = ref(false)

const filterCategorie = ref('all')
const filterNiveau = ref('all')
const filterTypeContenu = ref('all')
const filterStatut = ref('all')
const filterSearch = ref('')

const filteredPosts = computed(() => {
  let result = posts.value
  if (filterCategorie.value !== 'all') result = result.filter(p => Number(p.categorie) === Number(filterCategorie.value))
  if (filterNiveau.value !== 'all') result = result.filter(p => Number(p.niveau) === Number(filterNiveau.value))
  if (filterTypeContenu.value !== 'all') result = result.filter(p => Number(p.type_contenu) === Number(filterTypeContenu.value))
  if (filterStatut.value !== 'all') result = result.filter(p => p.statut === filterStatut.value)
  if (filterSearch.value.trim()) {
    const q = filterSearch.value.toLowerCase()
    result = result.filter(p => (p.titre || '').toLowerCase().includes(q))
  }
  return result
})

const emptyPost = () => ({
  id: null, titre: '', slug: '', extrait: '', contenu: '',
  categorie: null, niveau: null, type_contenu: null, tags_ids: [], statut: 'draft',
  seo_title: '', meta_description: '', og_title: '', og_description: '',
  alt_text_image: '', meta_robots: 'index',
  _coverFile: null, _coverPreview: '', _ogFile: null, _ogPreview: '',
})

const postForm = ref(emptyPost())
const selectedTagId = ref('')
const showPreview = ref(false)
const previewHtml = ref('')

const previewCategorie = computed(() => categories.value.find(c => c.id === postForm.value.categorie)?.nom || '')
const previewNiveau = computed(() => niveauLabel(postForm.value.niveau))
const previewTypeContenu = computed(() => typeContenuLabel(postForm.value.type_contenu))

const emptyCat = () => ({ id: null, nom: '', slug: '', description: '', meta_description: '', meta_robots: 'index', ordre: 0 })
const catForm = ref(emptyCat())
const emptyNiveau = () => ({ id: null, nom: '', slug: '', ordre: 0, est_actif: true })
const niveauForm = ref(emptyNiveau())
const emptyContentType = () => ({ id: null, nom: '', slug: '', ordre: 0, est_actif: true })
const contentTypeForm = ref(emptyContentType())
const emptyTag = () => ({ id: null, nom: '', slug: '', meta_description: '', meta_robots: 'index' })
const tagForm = ref(emptyTag())

const availableTags = computed(() => tags.value.filter(t => !postForm.value.tags_ids.includes(t.id)))

function counterClass(length, minIdeal, maxIdeal, hardMax) {
  if (hardMax && length > hardMax) return 'char-counter char-counter--danger'
  if (length >= minIdeal && length <= maxIdeal) return 'char-counter char-counter--good'
  if (length === 0) return 'char-counter'
  return 'char-counter char-counter--warn'
}

function formatDate(value) {
  if (!value) return '-'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return '-'
  return d.toLocaleDateString('fr-FR')
}

function niveauLabel(value) {
  const id = Number(value)
  return niveaux.value.find(n => Number(n.id) === id)?.nom || ''
}

function typeContenuLabel(value) {
  const id = Number(value)
  return contentTypes.value.find(t => Number(t.id) === id)?.nom || ''
}

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

function onCoverImageChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  postForm.value._coverFile = file
  postForm.value._coverPreview = URL.createObjectURL(file)
}

function onOgImageChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  postForm.value._ogFile = file
  postForm.value._ogPreview = URL.createObjectURL(file)
}

function handlePreview() {
  try {
    previewHtml.value = renderContentWithImages(postForm.value.contenu, [])
    showPreview.value = true
    nextTick(() => renderMath())
  } catch (e) {
    console.error('Erreur preview:', e)
  }
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
    categorie: post.categorie ? Number(post.categorie) : null,
    niveau: post.niveau ? Number(post.niveau) : null,
    type_contenu: post.type_contenu ? Number(post.type_contenu) : null,
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
    fd.append('categorie', postForm.value.categorie || '')
    fd.append('niveau', postForm.value.niveau || '')
    fd.append('type_contenu', postForm.value.type_contenu || '')
    fd.append('statut', postForm.value.statut)
    fd.append('seo_title', postForm.value.seo_title)
    fd.append('meta_description', postForm.value.meta_description)
    fd.append('og_title', postForm.value.og_title)
    fd.append('og_description', postForm.value.og_description)
    fd.append('alt_text_image', postForm.value.alt_text_image)
    fd.append('meta_robots', postForm.value.meta_robots)
    for (const tid of postForm.value.tags_ids) fd.append('tags_ids', tid)
    if (postForm.value._coverFile) fd.append('image_couverture', postForm.value._coverFile)
    if (postForm.value._ogFile) fd.append('og_image', postForm.value._ogFile)

    if (postForm.value.id) await updateBlogPost(postForm.value.id, fd)
    else await createBlogPost(fd)

    resetPostForm()
    await loadPosts()
  } catch (e) {
    console.error('Erreur sauvegarde article:', e, e?.response?.data)
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

function resetCatForm() { catForm.value = emptyCat() }
function editCategory(cat) {
  catForm.value = {
    id: cat.id,
    nom: cat.nom || '',
    slug: cat.slug || '',
    description: cat.description || '',
    meta_description: cat.meta_description || '',
    meta_robots: cat.meta_robots || 'index',
    ordre: Number(cat.ordre || 0),
  }
  activeTab.value = 'categories'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSaveCategory() {
  if (!catForm.value.nom) return
  try {
    const payload = { ...catForm.value }
    delete payload.id
    if (catForm.value.id) await updateBlogCategory(catForm.value.id, payload)
    else await createBlogCategory(payload)
    resetCatForm()
    await loadCategories()
  } catch (e) {
    console.error('Erreur sauvegarde categorie:', e, e?.response?.data)
  }
}

async function handleDeleteCategory(cat) {
  try {
    await deleteBlogCategory(cat.id)
    await loadCategories()
  } catch (e) {
    console.error('Erreur suppression categorie:', e)
  }
}

function resetNiveauForm() { niveauForm.value = emptyNiveau() }
function editNiveau(niveau) {
  niveauForm.value = {
    id: niveau.id,
    nom: niveau.nom || '',
    slug: niveau.slug || '',
    ordre: Number(niveau.ordre || 0),
    est_actif: niveau.est_actif !== false,
  }
  activeTab.value = 'niveaux'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSaveNiveau() {
  if (!niveauForm.value.nom) return
  try {
    const payload = { ...niveauForm.value }
    delete payload.id
    if (niveauForm.value.id) await updateBlogNiveau(niveauForm.value.id, payload)
    else await createBlogNiveau(payload)
    resetNiveauForm()
    await Promise.all([loadNiveaux(), loadPosts()])
  } catch (e) {
    console.error('Erreur sauvegarde niveau:', e, e?.response?.data)
  }
}

async function handleDeleteNiveau(niveau) {
  try {
    await deleteBlogNiveau(niveau.id)
    await Promise.all([loadNiveaux(), loadPosts()])
  } catch (e) {
    console.error('Erreur suppression niveau:', e)
  }
}

function resetContentTypeForm() { contentTypeForm.value = emptyContentType() }
function editContentType(item) {
  contentTypeForm.value = {
    id: item.id,
    nom: item.nom || '',
    slug: item.slug || '',
    ordre: Number(item.ordre || 0),
    est_actif: item.est_actif !== false,
  }
  activeTab.value = 'types'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSaveContentType() {
  if (!contentTypeForm.value.nom) return
  try {
    const payload = { ...contentTypeForm.value }
    delete payload.id
    if (contentTypeForm.value.id) await updateBlogContentType(contentTypeForm.value.id, payload)
    else await createBlogContentType(payload)
    resetContentTypeForm()
    await Promise.all([loadContentTypes(), loadPosts()])
  } catch (e) {
    console.error('Erreur sauvegarde type:', e, e?.response?.data)
  }
}

async function handleDeleteContentType(item) {
  try {
    await deleteBlogContentType(item.id)
    await Promise.all([loadContentTypes(), loadPosts()])
  } catch (e) {
    console.error('Erreur suppression type:', e)
  }
}

function resetTagForm() { tagForm.value = emptyTag() }
function editTag(tag) {
  tagForm.value = {
    id: tag.id,
    nom: tag.nom || '',
    slug: tag.slug || '',
    meta_description: tag.meta_description || '',
    meta_robots: tag.meta_robots || 'index',
  }
  activeTab.value = 'tags'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSaveTag() {
  if (!tagForm.value.nom) return
  try {
    const payload = { ...tagForm.value }
    delete payload.id
    if (tagForm.value.id) await updateBlogTag(tagForm.value.id, payload)
    else await createBlogTag(payload)
    resetTagForm()
    await loadTags()
  } catch (e) {
    console.error('Erreur sauvegarde tag:', e, e?.response?.data)
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
    console.error('Erreur chargement categories:', e)
    categories.value = []
  }
}

async function loadNiveaux() {
  try {
    const { data } = await getAdminBlogNiveaux()
    niveaux.value = data || []
  } catch (e) {
    console.error('Erreur chargement niveaux:', e)
    niveaux.value = []
  }
}

async function loadContentTypes() {
  try {
    const { data } = await getAdminBlogContentTypes()
    contentTypes.value = data || []
  } catch (e) {
    console.error('Erreur chargement types:', e)
    contentTypes.value = []
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
  await Promise.all([
    loadPosts(),
    loadCategories(),
    loadNiveaux(),
    loadContentTypes(),
    loadTags(),
  ])
})
</script>

<style src="@/styles/admin-common.css"></style>
<style scoped>
.admin-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.blog-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e5e7eb;
  overflow-x: auto;
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
  white-space: nowrap;
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
  width: 16px;
  text-align: center;
  font-size: 0.75rem;
  font-weight: 700;
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

.admin-form {
  background: #fff;
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

.form-group { margin-bottom: 1rem; }
.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.375rem;
  color: #374151;
  font-size: 0.875rem;
}

.required { color: #ef4444; }

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
  background: #fff;
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

.label-with-counter {
  display: flex !important;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.char-counter {
  font-size: 0.7rem;
  font-weight: 600;
  color: #6b7280;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 9999px;
  white-space: nowrap;
}

.char-counter--good { color: #065f46; background: #d1fae5; }
.char-counter--warn { color: #92400e; background: #fef3c7; }
.char-counter--danger { color: #991b1b; background: #fee2e2; }

.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.tags-select-row { display: flex; gap: 0.5rem; }
.tags-select-row select { flex: 1; }

.btn-tag-add {
  width: 40px;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
}

.chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
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

.image-upload-zone {
  border: 2px dashed #d1d5db;
  border-radius: 0.5rem;
  padding: 0.75rem;
  background: #f9fafb;
}

.image-preview-lg {
  display: block;
  max-width: 280px;
  max-height: 160px;
  margin-top: 0.75rem;
  border-radius: 0.5rem;
}

.btn-primary, .btn-secondary, .btn-danger {
  border: none;
  border-radius: 0.375rem;
  padding: 0.55rem 0.9rem;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
}

.btn-primary { background: #2563eb; color: #fff; }
.btn-secondary { background: #e5e7eb; color: #111827; }
.btn-danger { background: #ef4444; color: #fff; }

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.filter-group label {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
  display: block;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
}

.admin-table th,
.admin-table td {
  border-bottom: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: left;
  vertical-align: middle;
  font-size: 0.85rem;
}

.admin-table thead th { background: #f9fafb; color: #374151; font-weight: 600; }
.title-cell { font-weight: 600; color: #1f2937; }
.empty-row, .loading-row { text-align: center; color: #6b7280; }

.status-badge {
  display: inline-block;
  padding: 0.2rem 0.55rem;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 600;
}

.status-badge.published { background: #dcfce7; color: #166534; }
.status-badge.draft { background: #fef3c7; color: #92400e; }

.robots-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 600;
}

.robots-badge.index { background: #dcfce7; color: #166534; }
.robots-badge.noindex { background: #fee2e2; color: #991b1b; }

.slug-code {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 0.25rem;
  padding: 0.1rem 0.35rem;
  font-size: 0.75rem;
}

.preview-section {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  overflow: hidden;
}

.preview-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #eff6ff;
  border-bottom: 1px solid #dbeafe;
  padding: 0.75rem 1rem;
}

.btn-close-preview {
  border: 1px solid #93c5fd;
  background: #fff;
  color: #2563eb;
  border-radius: 0.375rem;
  padding: 0.35rem 0.65rem;
  cursor: pointer;
}

.preview-article { padding: 1rem 1.25rem; }
.preview-meta { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem; }
.preview-cat { background: #f3f4f6; color: #374151; padding: 0.15rem 0.625rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; }
.preview-taxonomy { background: #ecfeff; color: #155e75; padding: 0.15rem 0.625rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; }
.preview-tags { display: flex; gap: 0.375rem; flex-wrap: wrap; }
.preview-title { font-size: 1.75rem; font-weight: 700; color: #111827; margin: 0 0 0.75rem; }
.preview-excerpt { font-size: 1rem; color: #6b7280; margin: 0 0 1.25rem; font-style: italic; }
.preview-content { font-size: 0.95rem; line-height: 1.75; color: #374151; }
.preview-content :deep(img) { max-width: 100%; border-radius: 0.5rem; }

@media (max-width: 768px) {
  .form-row-2 { grid-template-columns: 1fr; }
  .label-with-counter { flex-direction: column; align-items: flex-start; }
  .filters { grid-template-columns: 1fr; }
  .admin-table { font-size: 0.8rem; display: block; overflow-x: auto; }
}
</style>
