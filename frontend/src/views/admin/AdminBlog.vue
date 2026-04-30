<template>
  <div>
    <FormatHelp v-if="activeTab === 'posts'" :format-template="BLOG_FORMAT_TEMPLATE" :show-notes="false" />
    
    <h2 class="admin-title">Gestion du Blog</h2>

    <div class="blog-tabs">
      <button :class="['tab-btn', { active: activeTab === 'posts' }]" @click="activeTab = 'posts'">
        <span class="tab-icon">A</span> Articles
        <span class="tab-count" v-if="posts.length">{{ posts.length }}</span>
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

        <div class="post-meta-row">
          <div class="form-group">
            <label>Type de contenu</label>
            <select v-model="postForm.type_contenu">
              <option :value="null">- Aucun type -</option>
              <option v-for="t in contentTypes" :key="t.id" :value="t.id">{{ t.nom }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Niveau (classe)</label>
            <select v-model="postForm.niveau">
              <option :value="null">- Aucun niveau -</option>
              <option v-for="n in niveaux" :key="n.id" :value="n.id">{{ n.nom }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Statut</label>
            <select v-model="postForm.statut">
              <option value="published">Publi&eacute;</option>
              <option value="draft">Brouillon</option>
            </select>
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
        </div>

        <div class="form-group related-posts-panel">
          <label>Articles similaires</label>
          <small class="field-hint">
            Ces articles seront affich&eacute;s en cartes &agrave; la fin de l'article public.
          </small>
          <div class="tags-select-row">
            <select v-model="selectedRelatedPostId">
              <option value="">Ajouter un article similaire...</option>
              <option v-for="p in availableRelatedPosts" :key="p.id" :value="p.id">{{ p.titre }}</option>
            </select>
            <button class="btn-tag-add" type="button" @click="addRelatedPost" :disabled="!selectedRelatedPostId">+</button>
          </div>
          <div class="chips" v-if="postForm.articles_lies_ids.length">
            <span class="chip" v-for="pid in postForm.articles_lies_ids" :key="pid">
              {{ postTitleById(pid) }}
              <button class="chip-remove" type="button" @click="removeRelatedPost(pid)">x</button>
            </span>
          </div>
        </div>

        <div class="form-group">
          <div class="content-field-head">
            <label>Contenu <span class="required">*</span></label>
            <div class="content-tools">
              <label class="cta-position-control">
                <span>CTA perso</span>
                <select v-model="ctaImagePosition">
                  <option value="droite">Droite</option>
                  <option value="gauche">Gauche</option>
                  <option value="bas">Sous le texte</option>
                </select>
              </label>
              <button type="button" class="btn-marker" @click="insertDefaultCtaPreset('cours')">CTA cours</button>
              <button type="button" class="btn-marker" @click="insertDefaultCtaPreset('abonnement')">CTA abonnement</button>
              <button type="button" class="btn-marker" @click="insertCtaBlock">CTA personnalis&eacute;</button>
            </div>
          </div>
          <textarea
            ref="contentTextarea"
            v-model="postForm.contenu"
            :placeholder="SMART_CONTENT_PLACEHOLDER"
            rows="14"
          ></textarea>
          <small class="field-hint">Tu peux coller ici Titre de l'article, Slug, Extrait, Titre SEO, Meta description puis Contenu. Les 2 CTA par d&eacute;faut s'ajoutent automatiquement en fin d'article.</small>
        </div>

        <div class="form-group inline-images-panel">
          <div class="inline-images-head">
            <div>
              <label>Images dans l'article</label>
              <small class="field-hint">
                La premi&egrave;re image ajout&eacute;e devient la couverture. Les suivantes se placent avec <code>[IMAGE_1]</code>, <code>[IMAGE_2]</code>, etc. Le bloc complet permet de r&eacute;gler alt, description, l&eacute;gende, alignement et largeur dans le contenu.
              </small>
            </div>
            <label class="btn-upload-inline">
              Ajouter des images
              <input
                ref="inlineImagesInput"
                type="file"
                accept="image/*"
                multiple
                @change="onInlineImagesChange"
              />
            </label>
          </div>

          <div v-if="!hasBlogImages" class="inline-images-empty">
            Aucune image. Ajoutez une ou plusieurs images : la premi&egrave;re sera utilis&eacute;e en couverture, les suivantes pourront &ecirc;tre ins&eacute;r&eacute;es dans le contenu.
          </div>

          <div v-else class="inline-images-list">
            <article v-if="hasCoverImage" class="inline-image-card inline-image-card--cover">
              <div class="inline-image-preview">
                <img :src="postForm._coverPreview" :alt="postForm.alt_text_image || postForm.titre || 'Image de couverture'" />
              </div>
              <div class="inline-image-fields">
                <div class="inline-image-card__top">
                  <code>[IMAGE_0]</code>
                  <span class="cover-image-badge">Couverture</span>
                  <span class="inline-image-help">Premi&egrave;re image de l'article, configur&eacute;e dans le contenu avec <code>[IMAGE_0]</code>.</span>
                  <button type="button" class="btn-marker" @click="insertCoverImageOptions">Ins&eacute;rer les options SEO</button>
                  <button type="button" class="btn-remove-image" @click="removeCoverImage">Supprimer</button>
                </div>
                <div class="form-group compact">
                  <label>Alt SEO/accessibilit&eacute;</label>
                  <input v-model="postForm.alt_text_image" maxlength="250" placeholder="Description textuelle de l'image de couverture" />
                  <small class="field-hint">Utilis&eacute; pour la couverture, l'accessibilit&eacute; et le SEO.</small>
                </div>
              </div>
            </article>

            <article v-for="(image, index) in postForm.images" :key="image._key" class="inline-image-card">
              <div class="inline-image-preview">
                <img v-if="image._preview" :src="image._preview" :alt="image.alt_text || `Image ${image.position}`" />
                <div v-else class="inline-image-preview__empty">Image</div>
              </div>
              <div class="inline-image-fields">
                <div class="inline-image-card__top">
                  <code>[IMAGE_{{ image.position }}]</code>
                  <button type="button" class="btn-marker" @click="insertImageMarker(image)">Ins&eacute;rer dans le contenu</button>
                  <button type="button" class="btn-remove-image" @click="removeInlineImage(index)">Supprimer</button>
                </div>
                <div class="form-row-4">
                  <div class="form-group compact">
                    <label>Position</label>
                    <input v-model.number="image.position" type="number" min="1" step="1" @change="handleInlineImagePositionChange(image)" />
                  </div>
                  <div class="form-group compact">
                    <label>Alignement</label>
                    <select v-model="image.align" @change="normalizeInlineImage(image)">
                      <option value="center">Centr&eacute;e</option>
                      <option value="left">Gauche</option>
                      <option value="right">Droite</option>
                      <option value="full">Pleine largeur</option>
                    </select>
                  </div>
                  <div class="form-group compact">
                    <label>Largeur (%)</label>
                    <input v-model.number="image.width_percent" type="number" min="20" max="100" step="5" @change="normalizeInlineImage(image)" />
                  </div>
                  <div class="form-group compact">
                    <label>Titre</label>
                    <input v-model="image.title_text" maxlength="160" placeholder="Optionnel" />
                  </div>
                </div>
                <div class="form-row-2">
                  <div class="form-group compact">
                    <label>Alt SEO/accessibilit&eacute;</label>
                    <input v-model="image.alt_text" maxlength="250" placeholder="Description de l'image" />
                  </div>
                  <div class="form-group compact">
                    <label>L&eacute;gende</label>
                    <input v-model="image.caption" maxlength="300" placeholder="Texte affich&eacute; sous l'image" />
                  </div>
                </div>
              </div>
            </article>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn-primary" type="submit">{{ postForm.id ? 'Mettre \u00e0 jour' : 'Cr\u00e9er' }}</button>
          <button class="btn-secondary" type="button" @click="handlePreview" :disabled="!postForm.contenu.trim()">Pr&eacute;visualiser</button>
          <button v-if="postForm.id" class="btn-danger" type="button" @click="resetPostForm">Annuler</button>
        </div>
      </form>

      <div v-if="showPreview" class="preview-section">
        <div class="preview-header-bar">
          <h3>Aper&ccedil;u de l'article {{ postForm.id ? '(Mode \u00e9dition)' : '(Mode cr\u00e9ation)' }}</h3>
          <button class="btn-close-preview" @click="showPreview = false">Fermer</button>
        </div>
        <article class="blog-article">
          <header class="blog-article__header">
            <h1 class="blog-article__title">{{ postForm.titre || 'Sans titre' }}</h1>
            <p v-if="postForm.extrait" class="blog-article__excerpt">{{ postForm.extrait }}</p>
          </header>

          <div v-if="postForm._coverPreview" class="blog-article__cover">
            <img
              :src="postForm._coverPreview"
              :alt="postForm.alt_text_image || postForm.titre || 'Image de couverture'"
              class="blog-article__cover-img"
            />
          </div>

          <div class="blog-article__layout">
            <aside v-if="previewToc.length > 1" class="blog-toc" aria-label="Sommaire">
              <button
                type="button"
                class="blog-toc__toggle"
                :aria-expanded="isPreviewTocExpanded"
                aria-controls="admin-blog-preview-toc"
                @click="isPreviewTocExpanded = !isPreviewTocExpanded"
              >
                <span class="blog-toc__title">Sommaire</span>
                <span class="blog-toc__state">{{ isPreviewTocExpanded ? 'Masquer' : 'Afficher' }}</span>
                <ChevronDownIcon
                  class="blog-toc__chevron"
                  :class="{ 'blog-toc__chevron--open': isPreviewTocExpanded }"
                  aria-hidden="true"
                />
              </button>
              <ul
                v-show="isPreviewTocExpanded"
                id="admin-blog-preview-toc"
                class="blog-toc__list"
              >
                <li v-for="item in previewToc" :key="item.id" :class="`blog-toc__item--h${item.level}`">
                  <a :href="`#${item.id}`" class="blog-toc__link">{{ item.text }}</a>
                </li>
              </ul>
            </aside>

            <div class="blog-article__content" v-html="previewHtml"></div>
          </div>

          <div v-if="postForm.tags_ids.length" class="blog-article__tags">
            <span
              v-for="tid in postForm.tags_ids"
              :key="tid"
              class="blog-article__tag"
            >
              #{{ tagNameById(tid) }}
            </span>
          </div>
        </article>
      </div>

      <div class="filters" aria-label="Filtres des articles">
        <div class="filters__head">
          <div>
            <p class="filters__title">Filtres</p>
            <p class="filters__count">
              {{ filteredPosts.length }} article{{ filteredPosts.length > 1 ? 's' : '' }}
            </p>
          </div>
          <button
            v-if="hasActiveFilters"
            type="button"
            class="filters__reset"
            @click="resetFilters"
          >
            R&eacute;initialiser
          </button>
        </div>

        <div class="filters__controls">
          <label class="filter-control">
            <span>Niveau</span>
            <select v-model="filterNiveau">
              <option value="all">Tous les niveaux</option>
              <option v-for="n in niveaux" :key="n.id" :value="n.id">{{ n.nom }}</option>
            </select>
          </label>
          <label class="filter-control">
            <span>Type</span>
            <select v-model="filterTypeContenu">
              <option value="all">Tous les types</option>
              <option v-for="t in contentTypes" :key="t.id" :value="t.id">{{ t.nom }}</option>
            </select>
          </label>
          <label class="filter-control">
            <span>Statut</span>
            <select v-model="filterStatut">
              <option value="all">Tous les statuts</option>
              <option value="published">Publi&eacute;</option>
              <option value="draft">Brouillon</option>
            </select>
          </label>
          <label class="filter-control filter-control--search">
            <span>Recherche</span>
            <input v-model="filterSearch" type="search" placeholder="Titre de l'article..." />
          </label>
        </div>
      </div>

      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Niveau</th>
            <th>Type</th>
            <th>Statut</th>
            <th>Date publication</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoadingPosts">
            <td colspan="7" class="loading-row">Chargement des articles...</td>
          </tr>
          <template v-else>
            <tr v-for="p in filteredPosts" :key="p.id">
              <td>{{ p.id }}</td>
              <td class="title-cell">{{ p.titre }}</td>
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
              <td colspan="7" class="empty-row">Aucun article trouv&eacute;.</td>
            </tr>
          </template>
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
import { ref, computed, onMounted, watch } from 'vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'
import {
  getAdminBlogPosts, createBlogPost, updateBlogPost, deleteBlogPost,
  createBlogPostImage, updateBlogPostImage, deleteBlogPostImage,
  getAdminBlogTags, createBlogTag, updateBlogTag, deleteBlogTag,
  getAdminBlogNiveaux, createBlogNiveau, updateBlogNiveau, deleteBlogNiveau,
  getAdminBlogContentTypes, createBlogContentType, updateBlogContentType, deleteBlogContentType,
} from '@/api/blog'
import { AdminActionsButtons } from '@/components/admin'
import FormatHelp from '@/components/admin/FormatHelp.vue'
import { extractBlogToc, renderBlogMarkdown } from '@/utils/blogRenderer'
import '@/assets/styles/blogArticle.css'
import 'katex/dist/katex.min.css'

const BLOG_FORMAT_TEMPLATE = `Titre de l'article: Titre clair et precis de l'article
Slug: titre-clair-et-precis-de-l-article
Extrait: Resume court de 120 a 220 caracteres qui explique le benefice de l'article.
Titre SEO: Titre Google clair avec le mot-cle principal, idealement 50 a 65 caracteres
Meta description: Description Google de 140 a 160 caracteres qui donne envie de lire l'article.
Contenu:
[IMAGE_0]
nom: Image de couverture de l'article
alt seo: Description precise de l'image de couverture avec le mot-cle principal
description seo: Image principale de l'article, utile pour comprendre le sujet traite
[/IMAGE_0]

# Titre clair et precis de l'article

Introduction courte : presenter le sujet, le niveau concerne et ce que l'eleve va apprendre.

## 1. Idee principale

Texte simple en paragraphes courts. Mettre les mots vraiment importants en **gras**.

Exemple de formule LaTeX dans une phrase : $\\ln(ab)=\\ln(a)+\\ln(b)$.

Formule centree sur une ligne separee :

$$
\\ln\\left(\\frac{a}{b}\\right)=\\ln(a)-\\ln(b)
$$

## 2. Methode a retenir

- Etape 1 : expliquer l'action a faire.
- Etape 2 : expliquer pourquoi elle fonctionne.
- Erreur classique : dire clairement ce qu'il faut eviter.

### Exemple corrige

Enonce de l'exemple, puis correction detaillee.

$$
\\ln(e^3)=3
$$

Explication du calcul en 2 ou 3 phrases simples.

[IMAGE_1]
nom: Schema de la methode
alt seo: Schema clair qui explique la methode pas a pas
description seo: Image pedagogique pour comprendre la methode de l'article
legende: Methode a retenir.
alignement: centre
largeur: 100
[/IMAGE_1]

## 3. Application ou exercice type

Texte de l'application ou exercice rapide a retenir.

[IMAGE_2]
nom: Exemple corrige
alt seo: Exemple corrige detaille pour appliquer la methode
description seo: Illustration de l'exemple corrige presente dans l'article
legende: Exemple corrige.
alignement: centre
largeur: 100
[/IMAGE_2]

## CTA par defaut

Deux bannieres CTA sont ajoutees automatiquement en fin d'article :
- CTA cours particuliers
- CTA abonnement / plateforme

Si tu veux choisir leur emplacement exact, place simplement :
[CTA_1]
[CTA_2]

Pour ne pas afficher les CTA par defaut sur un article precis :
[CTA_AUCUN]

Pour une banniere exceptionnelle, utilise le bouton "CTA personnalise" dans l'admin.

## Video explicative facultative

<iframe width="100%" height="380" src="https://www.youtube.com/embed/VIDEO_ID" title="Video explicative" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Liens dans l'article

Format a utiliser : [texte visible du lien](URL)

Lien vers un autre article du blog :
[Lire aussi : comprendre les fonctions](/blog/comprendre-les-fonctions)

Lien vers une page interne du site :
[Voir les exercices corriges](/ressources-gratuites/exercices)

Lien externe vers un autre site :
[Consulter une ressource officielle](https://www.exemple.com)

Les liens internes commencent par /blog/..., /ressources-gratuites/..., /cours-particuliers, etc.
Les liens externes commencent par https:// et s'ouvrent automatiquement dans un nouvel onglet.

Bouton HTML simple facultatif :

<a href="/cours-particuliers" style="display:inline-block;padding:10px 16px;border-radius:8px;background:#2563eb;color:#ffffff;text-decoration:none;font-weight:700;">Demander un cours particulier</a>

## Conclusion

Resume les points cles en quelques lignes.

## NOTES IMPORTANTES (a ne pas publier)

- Cette partie est dans le bloc pour pouvoir tout copier d'un coup. Elle est retiree automatiquement lors de la creation si le titre reste exactement comme ici.
- Les lignes du debut permettent de tout creer d'un coup : "Titre de l'article:", "Slug:", "Extrait:", "Titre SEO:", "Meta description:" et "Contenu:".
- Le champ "Slug" doit etre en minuscules, sans accents, avec des tirets entre les mots.
- Le champ "Extrait" doit rester court : idealement 120 a 220 caracteres, maximum 400.
- Le champ "Titre SEO" est le titre dans Google : idealement 50 a 65 caracteres, maximum 70.
- Le champ "Meta description" est la description sous le lien Google : idealement 140 a 160 caracteres.
- Titres Markdown : # pour le titre principal, ## pour les grandes parties, ### pour les sous-parties.
- LaTeX : utiliser $f'(x)=2x$ dans une phrase et $$f'(x)=2x$$ pour une formule centree.
- Images ajoutees dans l'admin : la premiere image ajoutee dans "Images dans l'article" devient la couverture. Les images suivantes se placent avec [IMAGE_1], [IMAGE_2], etc. dans le contenu.
- Couverture : utiliser [IMAGE_0] ... [/IMAGE_0] dans le contenu pour renseigner nom, alt seo et description seo. Ce bloc ne s'affiche pas dans l'article, il sert a la couverture.
- Options image dans le contenu : utiliser un bloc [IMAGE_1] ... [/IMAGE_1] avec nom, alt seo, description seo, legende, alignement et largeur. Le marqueur simple [IMAGE_1] fonctionne aussi.
- Image externe possible : ![Texte alternatif](https://.../image.png), mais preferer les images uploadees dans l'admin.
- CTA par defaut : les deux bannieres fixes sont ajoutees automatiquement. Utiliser [CTA_1] ou [CTA_2] seulement pour choisir l'emplacement. Utiliser [CTA_AUCUN] pour les masquer sur un article precis.
- CTA personnalise : utiliser [CTA]...[/CTA] seulement pour une banniere exceptionnelle. Positions possibles : image_position: droite, gauche ou bas.
- Liens : mettre les liens directement dans le contenu avec [texte visible](URL). Exemple article interne : [Lire aussi](/blog/slug-de-l-article). Exemple lien externe : [Ressource officielle](https://www.exemple.com).
- Articles similaires : les cartes se reglent dans le bloc admin "Articles similaires", pas dans le texte.
- Avant de publier : cliquer sur "Previsualiser" et verifier le rendu.`

const SMART_CONTENT_PLACEHOLDER = `Titre de l'article: 5 astuces pour reussir sa prepa MPSI
Slug: 5-astuces-reussir-prepa-mpsi
Extrait: Resume court affiche dans la liste du blog.
Titre SEO: 5 astuces pour reussir sa prepa MPSI
Meta description: Decouvre 5 conseils simples pour mieux travailler en prepa MPSI et progresser en maths avec une methode claire.
Contenu:
[IMAGE_0]
nom: Couverture article prepa MPSI
alt seo: Eleve en prepa MPSI qui organise son travail en mathematiques
description seo: Image de couverture pour un article sur les methodes de travail en prepa MPSI
[/IMAGE_0]

# 5 astuces pour reussir sa prepa MPSI

Texte de l'article...`

const activeTab = ref('posts')
const posts = ref([])
const niveaux = ref([])
const contentTypes = ref([])
const tags = ref([])
const isLoadingPosts = ref(false)
const inlineImagesInput = ref(null)
const contentTextarea = ref(null)
const deletedInlineImageIds = ref([])

const BLOG_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml']
const BLOG_IMAGE_MAX_SIZE = 10 * 1024 * 1024

const filterNiveau = ref('all')
const filterTypeContenu = ref('all')
const filterStatut = ref('all')
const filterSearch = ref('')

const filteredPosts = computed(() => {
  let result = posts.value
  if (filterNiveau.value !== 'all') result = result.filter(p => Number(p.niveau) === Number(filterNiveau.value))
  if (filterTypeContenu.value !== 'all') result = result.filter(p => Number(p.type_contenu) === Number(filterTypeContenu.value))
  if (filterStatut.value !== 'all') result = result.filter(p => p.statut === filterStatut.value)
  if (filterSearch.value.trim()) {
    const q = filterSearch.value.toLowerCase()
    result = result.filter(p => (p.titre || '').toLowerCase().includes(q))
  }
  return result
})

const hasActiveFilters = computed(() => (
  filterNiveau.value !== 'all'
  || filterTypeContenu.value !== 'all'
  || filterStatut.value !== 'all'
  || Boolean(filterSearch.value.trim())
))

function resetFilters() {
  filterNiveau.value = 'all'
  filterTypeContenu.value = 'all'
  filterStatut.value = 'all'
  filterSearch.value = ''
}

const emptyPost = () => ({
  id: null, titre: '', slug: '', extrait: '', contenu: '',
  niveau: null, type_contenu: null, tags_ids: [], articles_lies_ids: [], statut: 'published',
  seo_title: '', meta_description: '',
  alt_text_image: '',
  _coverFile: null, _coverPreview: '', _coverName: '', _coverRemoved: false,
  images: [],
})

const postForm = ref(emptyPost())
const selectedTagId = ref('')
const selectedRelatedPostId = ref('')
const ctaImagePosition = ref('droite')
const showPreview = ref(false)
const previewHtml = ref('')
const previewToc = ref([])
const isPreviewTocExpanded = ref(false)

const previewNiveau = computed(() => niveauLabel(postForm.value.niveau))
const previewTypeContenu = computed(() => typeContenuLabel(postForm.value.type_contenu))
const hasCoverImage = computed(() => Boolean(postForm.value._coverPreview || postForm.value._coverFile))
const hasBlogImages = computed(() => hasCoverImage.value || postForm.value.images.length > 0)

const emptyNiveau = () => ({ id: null, nom: '', slug: '', ordre: 0, est_actif: true })
const niveauForm = ref(emptyNiveau())
const emptyContentType = () => ({ id: null, nom: '', slug: '', ordre: 0, est_actif: true })
const contentTypeForm = ref(emptyContentType())
const emptyTag = () => ({ id: null, nom: '', slug: '', meta_description: '', meta_robots: 'index' })
const tagForm = ref(emptyTag())

const availableTags = computed(() => tags.value.filter(t => !postForm.value.tags_ids.includes(t.id)))
const availableRelatedPosts = computed(() => {
  const selected = new Set(postForm.value.articles_lies_ids.map(Number))
  return posts.value.filter((post) => {
    if (postForm.value.id && Number(post.id) === Number(postForm.value.id)) return false
    return !selected.has(Number(post.id))
  })
})

const ARTICLE_FIELD_ALIASES = {
  titre: ['titre', 'titre article', 'titre de l article', 'title'],
  slug: ['slug', 'url'],
  extrait: ['extrait', 'resume', 'description', 'excerpt'],
  seo_title: ['titre seo', 'titre google', 'titre meta', 'seo title', 'meta title', 'title seo'],
  meta_description: ['meta description', 'description meta', 'description seo', 'seo description', 'meta desc'],
  contenu: ['contenu', 'content', 'article', 'texte'],
}

function normalizeArticleLabel(label) {
  return String(label || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/['\u2019]/g, ' ')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
}

function articleFieldFromLabel(label) {
  const normalized = normalizeArticleLabel(label)
  return Object.entries(ARTICLE_FIELD_ALIASES).find(([, aliases]) => aliases.includes(normalized))?.[0] || ''
}

function compactInlineText(lines) {
  return lines
    .map(line => String(line || '').trim())
    .filter(Boolean)
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function stripInternalTemplateNotes(content) {
  return String(content || '')
    .replace(/\n?## NOTES IMPORTANTES \(a ne pas publier\)[\s\S]*$/i, '')
    .trim()
}

function parseContentOptionFields(rawBlock) {
  const fields = {}
  String(rawBlock || '')
    .split('\n')
    .map(line => line.trim())
    .filter(Boolean)
    .forEach((line) => {
      const separatorIndex = line.indexOf(':')
      if (separatorIndex === -1) return
      const key = normalizeArticleLabel(line.slice(0, separatorIndex))
      const value = line.slice(separatorIndex + 1).trim()
      if (key) fields[key] = value
    })
  return fields
}

function contentOptionValue(fields, aliases) {
  for (const alias of aliases) {
    const value = fields[normalizeArticleLabel(alias)]
    if (value) return value
  }
  return ''
}

function parseImageWidthPercent(value) {
  const match = String(value || '').match(/\d+/)
  if (!match) return null
  return Math.min(100, Math.max(20, Number.parseInt(match[0], 10) || 100))
}

function normalizeImageAlignFromContent(value) {
  const compact = normalizeArticleLabel(value).replace(/\s+/g, '')
  if (['left', 'gauche', 'agauche'].includes(compact)) return 'left'
  if (['right', 'droite', 'adroite'].includes(compact)) return 'right'
  if (['full', 'wide', 'pleinelargeur', 'largeurcomplete', '100'].includes(compact)) return 'full'
  return 'center'
}

function imageOptionsFromContentBlock(rawBlock) {
  const fields = parseContentOptionFields(rawBlock)
  const title = contentOptionValue(fields, ['nom', 'nom image', 'nom de l image', 'titre', 'titre image', 'title'])
  const alt = contentOptionValue(fields, ['alt', 'alt seo', 'texte alternatif', 'accessibilite'])
  const description = contentOptionValue(fields, ['description', 'description seo', 'desc', 'seo description'])
  const caption = contentOptionValue(fields, ['legende', 'caption'])
  const align = contentOptionValue(fields, ['alignement', 'align', 'position', 'placement'])
  const width = parseImageWidthPercent(contentOptionValue(fields, ['largeur', 'largeur %', 'width', 'width percent', 'width_percent']))

  const options = {}
  if (title || description) options.title_text = compactInlineText([title || description]).slice(0, 160)
  if (alt || description) options.alt_text = compactInlineText([alt || description]).slice(0, 250)
  if (caption) options.caption = compactInlineText([caption]).slice(0, 300)
  if (align) options.align = normalizeImageAlignFromContent(align)
  if (width) options.width_percent = width
  return options
}

function extractInlineImageOptions(content) {
  const byPosition = new Map()
  String(content || '').replace(
    /\n?\[\s*IMAGE\s*_?\s*(\d+)\s*\]([\s\S]*?)\[\s*\/\s*IMAGE(?:\s*_?\s*\1)?\s*\]\n?/gi,
    (_match, rawPosition, rawBlock) => {
      const position = Number.parseInt(rawPosition, 10)
      if (!Number.isFinite(position) || position < 1) return _match
      const options = imageOptionsFromContentBlock(rawBlock)
      if (Object.keys(options).length) {
        byPosition.set(position, { position, ...options })
      }
      return _match
    }
  )
  return byPosition
}

function setImageOption(image, key, value) {
  if (value === undefined || value === null || value === '') return false
  if (image[key] === value) return false
  image[key] = value
  return true
}

function applyInlineImageOptionsToForm(inlineImageOptions) {
  if (!inlineImageOptions?.size) return false

  let applied = false
  for (const [position, options] of inlineImageOptions.entries()) {
    const image = postForm.value.images.find(item => Number(item.position) === Number(position))
    if (!image) continue

    applied = setImageOption(image, 'title_text', options.title_text) || applied
    applied = setImageOption(image, 'alt_text', options.alt_text) || applied
    applied = setImageOption(image, 'caption', options.caption) || applied
    applied = setImageOption(image, 'align', options.align) || applied
    applied = setImageOption(image, 'width_percent', options.width_percent) || applied
    normalizeInlineImage(image)
  }

  return applied
}

function coverAltFromOptions({ alt, description, name }) {
  const parts = []
  if (alt) parts.push(alt)
  if (description && normalizeArticleLabel(description) !== normalizeArticleLabel(alt)) {
    parts.push(description)
  }
  if (!parts.length && name) parts.push(name)
  return compactInlineText(parts).slice(0, 250)
}

function extractCoverImageOptions(content) {
  let coverName = ''
  let coverAlt = ''
  let hasCoverOptions = false
  const cleanedContent = String(content || '')
    .replace(/\n?\[\s*IMAGE\s*_?\s*0\s*\]([\s\S]*?)\[\s*\/\s*IMAGE(?:\s*_?\s*0)?\s*\]\n?/gi, (_match, rawBlock) => {
      hasCoverOptions = true
      const fields = parseContentOptionFields(rawBlock)
      coverName = contentOptionValue(fields, ['nom', 'nom image', 'nom de l image', 'titre', 'titre image', 'title'])
      const alt = contentOptionValue(fields, ['alt', 'alt seo', 'texte alternatif', 'accessibilite', 'accessibilité'])
      const description = contentOptionValue(fields, ['description', 'description seo', 'desc', 'seo description'])
      coverAlt = coverAltFromOptions({ alt, description, name: coverName })
      return '\n\n'
    })
    .replace(/^\s*\[\s*IMAGE\s*_?\s*0\s*\]\s*$/gmi, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()

  return {
    content: cleanedContent,
    hasCoverOptions,
    coverName,
    coverAlt,
  }
}

function parseArticleDraft(rawText) {
  const text = String(rawText || '').replace(/\r\n/g, '\n').trim()
  const values = {
    titre: [],
    slug: [],
    extrait: [],
    seo_title: [],
    meta_description: [],
    contenu: [],
  }
  const contentLines = []
  let currentField = ''
  let hasMetadata = false
  const seenFields = new Set()

  for (const line of text.split('\n')) {
    if (currentField === 'contenu') {
      values.contenu.push(line)
      continue
    }

    const labelMatch = line.match(/^\s*([^:]{1,80})\s*:\s*(.*)$/)
    const field = labelMatch ? articleFieldFromLabel(labelMatch[1]) : ''

    if (field) {
      currentField = field
      hasMetadata = true
      seenFields.add(field)
      if (labelMatch[2]) values[field].push(labelMatch[2])
      continue
    }

    if (currentField) {
      if (line.trim()) values[currentField].push(line.trim())
      else currentField = ''
      continue
    }

    contentLines.push(line)
  }

  const rawContent = stripInternalTemplateNotes((values.contenu.length ? values.contenu : contentLines).join('\n'))
  const coverOptions = extractCoverImageOptions(rawContent)
  const contenu = coverOptions.content
  const inlineImageOptions = extractInlineImageOptions(contenu)
  const inferredTitle = contenu.match(/^\s*#\s+(.+?)\s*$/m)?.[1]?.replace(/\s+#*$/, '').trim() || ''

  return {
    hasMetadata,
    seenFields,
    titre: compactInlineText(values.titre) || inferredTitle,
    slug: compactInlineText(values.slug),
    extrait: compactInlineText(values.extrait).slice(0, 400),
    seo_title: compactInlineText(values.seo_title).slice(0, 70),
    meta_description: compactInlineText(values.meta_description).slice(0, 160),
    hasCoverOptions: coverOptions.hasCoverOptions,
    cover_image_name: coverOptions.coverName,
    cover_alt_text: coverOptions.coverAlt,
    hasInlineImageOptions: inlineImageOptions.size > 0,
    inline_image_options: inlineImageOptions,
    contenu,
  }
}

function applyParsedArticleDraft(parsed) {
  if (!parsed.hasMetadata && !parsed.contenu && !parsed.hasCoverOptions && !parsed.hasInlineImageOptions) return false

  const seen = parsed.seenFields || new Set()
  let applied = false
  if (seen.has('titre') && parsed.titre) {
    postForm.value.titre = parsed.titre
    applied = true
  }
  if (seen.has('slug')) {
    postForm.value.slug = parsed.slug
    applied = true
  }
  if (seen.has('extrait')) {
    postForm.value.extrait = parsed.extrait
    applied = true
  }
  if (seen.has('seo_title')) {
    postForm.value.seo_title = parsed.seo_title
    applied = true
  }
  if (seen.has('meta_description')) {
    postForm.value.meta_description = parsed.meta_description
    applied = true
  }
  if (parsed.hasCoverOptions) {
    postForm.value._coverName = parsed.cover_image_name
    postForm.value.alt_text_image = parsed.cover_alt_text
    applied = true
  }

  return applyInlineImageOptionsToForm(parsed.inline_image_options) || applied
}

function buildCoverEditorContent(post) {
  if (!post.image_couverture_url && !post.alt_text_image) return ''
  if (/\[\s*IMAGE\s*_?\s*0\s*\]/i.test(post.contenu || '')) return ''
  return [
    '[IMAGE_0]',
    `nom: ${post.titre || 'Image de couverture'}`,
    `alt seo: ${post.alt_text_image || ''}`,
    `description seo: ${post.alt_text_image || ''}`,
    '[/IMAGE_0]',
  ].join('\n')
}

function buildPostEditorContent(post) {
  const coverBlock = buildCoverEditorContent(post)
  return [
    `Titre de l'article: ${post.titre || ''}`,
    `Slug: ${post.slug || ''}`,
    `Extrait: ${post.extrait || ''}`,
    `Titre SEO: ${post.seo_title || ''}`,
    `Meta description: ${post.meta_description || ''}`,
    'Contenu:',
    coverBlock,
    post.contenu || '',
  ].filter(part => part !== '').join('\n')
}

function syncArticleFieldsFromContent() {
  const parsed = parseArticleDraft(postForm.value.contenu)
  const applied = applyParsedArticleDraft(parsed)
  if (parsed.hasMetadata || parsed.hasCoverOptions) return applied

  if (!postForm.value.titre.trim() && parsed.titre) {
    postForm.value.titre = parsed.titre
    return true
  }

  return applied
}

function getArticleBodyForRender() {
  const parsed = parseArticleDraft(postForm.value.contenu)
  return parsed.contenu
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

function postTitleById(id) {
  return posts.value.find(p => Number(p.id) === Number(id))?.titre || `Article ${id}`
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

function addRelatedPost() {
  const id = Number(selectedRelatedPostId.value)
  if (id && !postForm.value.articles_lies_ids.includes(id)) {
    postForm.value.articles_lies_ids.push(id)
  }
  selectedRelatedPostId.value = ''
}

function removeRelatedPost(id) {
  postForm.value.articles_lies_ids = postForm.value.articles_lies_ids.filter(postId => Number(postId) !== Number(id))
}

function nextInlineImagePosition() {
  const positions = postForm.value.images.map(image => Number(image.position || 0))
  return Math.max(0, ...positions) + 1
}

function normalizeInlineImage(image) {
  image.position = Math.max(1, Number.parseInt(image.position, 10) || nextInlineImagePosition())
  image.align = ['left', 'right', 'center', 'full'].includes(image.align) ? image.align : 'center'
  image.width_percent = image.align === 'full'
    ? 100
    : Math.min(100, Math.max(20, Number.parseInt(image.width_percent, 10) || 100))
}

function handleInlineImagePositionChange(image) {
  normalizeInlineImage(image)
  syncArticleFieldsFromContent()
}

function imageTitleFromFilename(filename = '') {
  return String(filename)
    .split(/[\\/]/)
    .pop()
    .replace(/\.[^.]+$/, '')
    .trim()
}

function buildInlineImageFromFile(file) {
  const position = nextInlineImagePosition()
  const previewUrl = URL.createObjectURL(file)
  const defaultTitle = imageTitleFromFilename(file.name)
  return {
    _key: `new-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    id: null,
    _file: file,
    _preview: previewUrl,
    preview_url: previewUrl,
    image_url: previewUrl,
    position,
    align: 'center',
    width_percent: 100,
    alt_text: '',
    caption: '',
    title_text: defaultTitle,
    est_actif: true,
  }
}

function setCoverImageFromFile(file) {
  const coverName = imageTitleFromFilename(file.name)
  postForm.value._coverFile = file
  postForm.value._coverPreview = URL.createObjectURL(file)
  postForm.value._coverName = coverName
  postForm.value._coverRemoved = false
  if (!postForm.value.alt_text_image.trim()) {
    postForm.value.alt_text_image = coverName
  }
}

function normalizeExistingInlineImage(image, index = 0) {
  const normalized = {
    _key: `existing-${image.id || index}`,
    id: image.id || null,
    _file: null,
    _preview: image.image_url || '',
    preview_url: image.image_url || '',
    image_url: image.image_url || '',
    position: Number(image.position || index + 1),
    align: image.align || 'center',
    width_percent: Number(image.width_percent || 100),
    alt_text: image.alt_text || '',
    caption: image.caption || '',
    title_text: image.title_text || '',
    est_actif: image.est_actif !== false,
  }
  normalizeInlineImage(normalized)
  return normalized
}

function onInlineImagesChange(event) {
  const files = Array.from(event.target.files || [])
  files.forEach(file => {
    if (!BLOG_IMAGE_TYPES.includes(file.type)) {
      console.warn(`Type d'image non supporte: ${file.name}`)
      return
    }
    if (file.size > BLOG_IMAGE_MAX_SIZE) {
      console.warn(`Image trop lourde: ${file.name}`)
      return
    }
    if (!hasCoverImage.value) {
      setCoverImageFromFile(file)
      return
    }
    postForm.value.images.push(buildInlineImageFromFile(file))
  })
  if (inlineImagesInput.value) inlineImagesInput.value.value = ''
  syncArticleFieldsFromContent()
}

function removeCoverImage() {
  postForm.value._coverRemoved = Boolean(postForm.value._coverPreview && !postForm.value._coverFile)
  postForm.value._coverFile = null
  postForm.value._coverPreview = ''
  postForm.value._coverName = ''
  postForm.value.alt_text_image = ''
}

function removeInlineImage(index) {
  const image = postForm.value.images[index]
  if (image?.id) {
    deletedInlineImageIds.value.push(image.id)
  }
  postForm.value.images.splice(index, 1)
}

function insertContentSnippet(snippet) {
  const textarea = contentTextarea.value
  if (!textarea) {
    postForm.value.contenu = `${postForm.value.contenu || ''}${snippet}`
    return
  }

  const start = textarea.selectionStart ?? postForm.value.contenu.length
  const end = textarea.selectionEnd ?? start
  const before = postForm.value.contenu.slice(0, start)
  const after = postForm.value.contenu.slice(end)
  postForm.value.contenu = `${before}${snippet}${after}`

  requestAnimationFrame(() => {
    textarea.focus()
    const nextPosition = start + snippet.length
    textarea.setSelectionRange(nextPosition, nextPosition)
  })
}

function imageAlignContentValue(value) {
  if (value === 'left') return 'gauche'
  if (value === 'right') return 'droite'
  if (value === 'full') return 'pleine largeur'
  return 'centre'
}

function imageContentBlock(image) {
  normalizeInlineImage(image)
  const position = image.position
  return `\n\n[IMAGE_${position}]\nnom: ${image.title_text || ''}\nalt seo: ${image.alt_text || ''}\ndescription seo: ${image.title_text || image.alt_text || ''}\nlegende: ${image.caption || ''}\nalignement: ${imageAlignContentValue(image.align)}\nlargeur: ${image.width_percent || 100}\n[/IMAGE_${position}]\n\n`
}

function coverImageContentBlock() {
  const name = postForm.value._coverName || postForm.value.titre || 'Image de couverture'
  const alt = postForm.value.alt_text_image || ''
  return `\n\n[IMAGE_0]\nnom: ${name}\nalt seo: ${alt}\ndescription seo: ${alt}\n[/IMAGE_0]\n\n`
}

function insertCoverImageOptions() {
  insertContentSnippet(coverImageContentBlock())
}

function insertImageMarker(image) {
  insertContentSnippet(imageContentBlock(image))
}

function insertDefaultCtaPreset(type) {
  const marker = type === 'abonnement' ? '[CTA_2]' : '[CTA_1]'
  insertContentSnippet(`\n\n${marker}\n\n`)
}

function insertCtaBlock() {
  const selectedPosition = ['droite', 'gauche', 'bas'].includes(ctaImagePosition.value)
    ? ctaImagePosition.value
    : 'droite'
  const snippet = `\n\n[CTA]\nsurtitre: Banniere personnalisee\ntitre: Titre de la banniere\ntexte: Texte court qui explique l'action proposee.\nbouton: Texte du bouton\nurl: /cours-particuliers\nimage: /cta-banner-cours-particuliers.png\nimage_alt: Description SEO de l'image de la banniere\nimage_position: ${selectedPosition}\nstyle: split\ntheme: optitab\n[/CTA]\n\n`
  insertContentSnippet(snippet)
}

function buildInlineImageFormData(image) {
  normalizeInlineImage(image)
  const fd = new FormData()
  if (image._file) fd.append('image', image._file)
  fd.append('position', image.position)
  fd.append('align', image.align)
  fd.append('width_percent', image.width_percent)
  fd.append('alt_text', image.alt_text || '')
  fd.append('caption', image.caption || '')
  fd.append('title_text', image.title_text || '')
  fd.append('est_actif', image.est_actif === false ? 'false' : 'true')
  return fd
}

async function syncInlineImages(postId) {
  if (!postId) return

  for (const imageId of deletedInlineImageIds.value) {
    await deleteBlogPostImage(postId, imageId)
  }

  for (const image of postForm.value.images) {
    const fd = buildInlineImageFormData(image)
    if (image.id) {
      await updateBlogPostImage(postId, image.id, fd)
    } else if (image._file) {
      await createBlogPostImage(postId, fd)
    }
  }
}

function refreshPreviewHtml() {
  try {
    const articleBody = getArticleBodyForRender()
    previewToc.value = extractBlogToc(articleBody)
    previewHtml.value = renderBlogMarkdown(articleBody, {
      title: postForm.value.titre,
      images: postForm.value.images,
      preview: true,
    })
  } catch (e) {
    console.error('Erreur preview:', e)
  }
}

function handlePreview() {
  syncArticleFieldsFromContent()
  isPreviewTocExpanded.value = false
  refreshPreviewHtml()
  showPreview.value = true
}

watch(
  () => postForm.value.contenu,
  () => {
    syncArticleFieldsFromContent()
    if (showPreview.value) {
      refreshPreviewHtml()
    }
  }
)

watch(
  () => [postForm.value.titre, postForm.value.images],
  () => {
    if (showPreview.value) refreshPreviewHtml()
  },
  { deep: true }
)

function resetPostForm() {
  postForm.value = emptyPost()
  selectedTagId.value = ''
  selectedRelatedPostId.value = ''
  deletedInlineImageIds.value = []
  showPreview.value = false
  previewHtml.value = ''
  previewToc.value = []
  isPreviewTocExpanded.value = false
  if (inlineImagesInput.value) inlineImagesInput.value.value = ''
}

function editPost(post) {
  postForm.value = {
    id: post.id,
    titre: post.titre || '',
    slug: post.slug || '',
    extrait: post.extrait || '',
    contenu: buildPostEditorContent(post),
    niveau: post.niveau ? Number(post.niveau) : null,
    type_contenu: post.type_contenu ? Number(post.type_contenu) : null,
    tags_ids: (post.tags_ids || []).map(Number),
    articles_lies_ids: (post.articles_lies_ids || []).map(Number),
    statut: post.statut || 'published',
    seo_title: post.seo_title || '',
    meta_description: post.meta_description || '',
    alt_text_image: post.alt_text_image || '',
    _coverFile: null,
    _coverPreview: post.image_couverture_url || '',
    _coverName: post.titre || '',
    _coverRemoved: false,
    images: (post.images || []).map(normalizeExistingInlineImage),
  }
  syncArticleFieldsFromContent()
  deletedInlineImageIds.value = []
  selectedTagId.value = ''
  selectedRelatedPostId.value = ''
  activeTab.value = 'posts'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleSavePost() {
  syncArticleFieldsFromContent()
  if (!postForm.value.titre.trim()) return
  try {
    const articleBody = getArticleBodyForRender()
    const fd = new FormData()
    fd.append('titre', postForm.value.titre)
    fd.append('slug', postForm.value.slug || '')
    fd.append('extrait', postForm.value.extrait)
    fd.append('contenu', articleBody)
    fd.append('categorie', '')
    fd.append('niveau', postForm.value.niveau || '')
    fd.append('type_contenu', postForm.value.type_contenu || '')
    fd.append('statut', postForm.value.statut)
    const generatedOgTitle = (postForm.value.seo_title || postForm.value.titre || '').trim()
    const generatedOgDescription = (postForm.value.meta_description || postForm.value.extrait || '').trim()
    fd.append('seo_title', postForm.value.seo_title)
    fd.append('meta_description', postForm.value.meta_description)
    fd.append('og_title', generatedOgTitle)
    fd.append('og_description', generatedOgDescription)
    fd.append('alt_text_image', postForm.value.alt_text_image)
    fd.append('meta_robots', 'index')
    fd.append('tags_ids_present', 'true')
    for (const tid of postForm.value.tags_ids) fd.append('tags_ids', tid)
    fd.append('articles_lies_ids_present', 'true')
    for (const pid of postForm.value.articles_lies_ids) fd.append('articles_lies_ids', pid)
    if (postForm.value._coverFile) fd.append('image_couverture', postForm.value._coverFile)
    else if (postForm.value._coverRemoved) fd.append('clear_image_couverture', 'true')

    const response = postForm.value.id
      ? await updateBlogPost(postForm.value.id, fd)
      : await createBlogPost(fd)

    const savedPost = response?.data || response
    const postId = savedPost?.id || postForm.value.id
    await syncInlineImages(postId)

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

.content-field-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.content-field-head label {
  margin-bottom: 0;
}

.content-tools {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.cta-position-control {
  display: inline-flex !important;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  color: #4b5563;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
}

.cta-position-control select {
  width: auto;
  min-width: 132px;
  padding: 0.45rem 0.625rem;
  font-size: 0.82rem;
}

.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-row-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }
.post-meta-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }

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

.related-posts-panel {
  border: 1px solid #dbeafe;
  border-radius: 0.75rem;
  padding: 1rem;
  background: #f8fbff;
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

.btn-primary:disabled,
.btn-secondary:disabled,
.btn-danger:disabled,
.btn-marker:disabled,
.btn-tag-add:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.filters {
  display: grid;
  gap: 0.875rem;
  margin-bottom: 1.25rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #ffffff;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
}

.filters__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.filters__title {
  margin: 0;
  color: #111827;
  font-size: 0.95rem;
  font-weight: 800;
}

.filters__count {
  margin: 0.15rem 0 0;
  color: #64748b;
  font-size: 0.78rem;
  font-weight: 600;
}

.filters__reset {
  min-height: 34px;
  padding: 0.45rem 0.75rem;
  border: 1px solid #dbe4ff;
  border-radius: 0.5rem;
  background: #f5f8ff;
  color: #2557d6;
  cursor: pointer;
  font-size: 0.78rem;
  font-weight: 800;
}

.filters__reset:hover {
  border-color: #b7c8ff;
  background: #eef3ff;
}

.filters__controls {
  display: grid;
  grid-template-columns: minmax(140px, 0.8fr) minmax(150px, 0.85fr) minmax(140px, 0.8fr) minmax(240px, 1.4fr);
  gap: 0.75rem;
  align-items: end;
}

.filter-control {
  display: grid;
  gap: 0.35rem;
  min-width: 0;
}

.filter-control span {
  color: #475569;
  font-size: 0.72rem;
  font-weight: 800;
}

.filter-control select,
.filter-control input {
  width: 100%;
  min-height: 40px;
  padding: 0.55rem 0.75rem;
  border: 1px solid #cfd8e6;
  border-radius: 0.55rem;
  background: #f8fafc;
  color: #111827;
  font: inherit;
  font-size: 0.88rem;
  transition: border-color 0.15s, box-shadow 0.15s, background-color 0.15s;
}

.filter-control select:focus,
.filter-control input:focus {
  outline: none;
  border-color: #315eea;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(49, 94, 234, 0.12);
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

.inline-images-panel {
  border: 1px solid #dbeafe;
  border-radius: 0.75rem;
  padding: 1rem;
  background: #f8fbff;
}

.inline-images-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.inline-images-head label {
  margin-bottom: 0.25rem;
}

.inline-images-head .btn-upload-inline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 38px;
  padding: 0.5rem 0.8rem;
  border-radius: 0.5rem;
  background: #2563eb;
  color: #fff;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  white-space: nowrap;
}

.btn-upload-inline input {
  display: none;
}

.inline-images-empty {
  border: 1px dashed #bfdbfe;
  border-radius: 0.625rem;
  padding: 1rem;
  background: #fff;
  color: #64748b;
  font-size: 0.9rem;
}

.inline-images-list {
  display: grid;
  gap: 0.875rem;
}

.inline-image-card {
  display: grid;
  grid-template-columns: 170px minmax(0, 1fr);
  gap: 1rem;
  padding: 0.875rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #fff;
}

.inline-image-card--cover {
  border-color: #bfdbfe;
  background: #f8fbff;
}

.inline-image-preview {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: 0.625rem;
  overflow: hidden;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
}

.inline-image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.inline-image-preview__empty {
  height: 100%;
  display: grid;
  place-items: center;
  color: #64748b;
  font-weight: 700;
}

.inline-image-fields {
  min-width: 0;
}

.inline-image-card__top {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.inline-image-card__top code {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
  border-radius: 0.375rem;
  padding: 0.25rem 0.45rem;
  font-weight: 700;
}

.cover-image-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0.25rem 0.55rem;
  border-radius: 0.375rem;
  background: #10257f;
  color: #fff;
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.inline-image-help {
  color: #64748b;
  font-size: 0.82rem;
  font-weight: 600;
}

.btn-marker,
.btn-remove-image {
  border: 1px solid #cbd5e1;
  border-radius: 0.45rem;
  padding: 0.35rem 0.6rem;
  background: #fff;
  color: #334155;
  font-weight: 600;
  cursor: pointer;
}

.btn-marker {
  border-color: #93c5fd;
  color: #1d4ed8;
}

.btn-remove-image {
  margin-left: auto;
  border-color: #fecaca;
  color: #b91c1c;
}

.form-row-4 {
  display: grid;
  grid-template-columns: 110px 160px 120px minmax(0, 1fr);
  gap: 0.75rem;
}

.form-row-4 .span-2 {
  grid-column: span 2;
}

.form-group.compact {
  margin-bottom: 0.75rem;
}

.form-group.compact label {
  font-size: 0.76rem;
}

.preview-section {
  background: #f7f9fc;
  border: 1px solid #dbeafe;
  border-radius: 0.875rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.preview-section .blog-article {
  margin: 1.25rem auto;
}

.preview-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #eef4ff;
  border-bottom: 1px solid #dbeafe;
  padding: 0.875rem 1rem;
}

.preview-header-bar h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #1e3a8a;
}

.btn-close-preview {
  border: 1px solid #93c5fd;
  background: #fff;
  color: #2563eb;
  border-radius: 0.375rem;
  padding: 0.35rem 0.65rem;
  cursor: pointer;
}

.preview-article {
  max-width: 1080px;
  margin: 1.25rem auto;
  padding: 2rem 2.5rem;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
}

.preview-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
  align-items: center;
}

.preview-taxonomy {
  padding: 0.2rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.preview-taxonomy {
  background: #f1f5f9;
  color: #475569;
}

.preview-tags {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.preview-title {
  font-size: clamp(2rem, 3.5vw, 3.1rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #111827;
  margin: 0 0 1rem;
}

.preview-excerpt {
  font-size: 1.12rem;
  line-height: 1.7;
  color: #475569;
  margin: 0 0 1.5rem;
}

.preview-cover {
  margin: 0 0 2rem;
  border-radius: 0.875rem;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
}

.preview-cover img {
  display: block;
  width: 100%;
  max-height: 420px;
  object-fit: cover;
}

.preview-content {
  font-size: 1.0625rem;
  line-height: 1.75;
  color: #1e293b;
  word-break: break-word;
}

.preview-content :deep(h1) {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  margin: 2rem 0 1rem;
  letter-spacing: -0.03em;
}

.preview-content :deep(h2) {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 2.75rem 0 1.125rem;
  padding: 0 0 0.75rem;
  border-bottom: 3px solid #6366f1;
  letter-spacing: -0.01em;
}

.preview-content :deep(h3) {
  font-size: 1.1875rem;
  font-weight: 700;
  color: #374151;
  margin: 2rem 0 0.75rem;
  padding-left: 1rem;
  border-left: 4px solid #6366f1;
  letter-spacing: -0.005em;
}

.preview-content :deep(p) {
  margin: 0 0 1.25rem;
}

.preview-content :deep(a) {
  color: #2563eb;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.preview-content :deep(strong) {
  font-weight: 700;
  color: #111827;
}

.preview-content :deep(ul),
.preview-content :deep(ol) {
  margin: 0 0 1.25rem;
  padding-left: 1.5rem;
}

.preview-content :deep(li) {
  margin-bottom: 0.375rem;
}

.preview-content :deep(blockquote) {
  margin: 1.5rem 0;
  padding: 1rem 1.5rem;
  border-left: 4px solid #2563eb;
  background: #eff6ff;
  border-radius: 0 0.625rem 0.625rem 0;
  color: #1e40af;
  font-style: italic;
}

.preview-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.75rem;
  margin: 1.5rem 0;
}

.preview-content :deep(.blog-inline-image) {
  max-width: min(var(--blog-image-width, 100%), 100%);
  margin: 1.75rem auto;
  clear: both;
}

.preview-content :deep(.blog-inline-image--left) {
  float: left;
  clear: left;
  margin: 0.5rem 1.75rem 1.25rem 0;
  max-width: min(var(--blog-image-width, 45%), 52%);
}

.preview-content :deep(.blog-inline-image--right) {
  float: right;
  clear: right;
  margin: 0.5rem 0 1.25rem 1.75rem;
  max-width: min(var(--blog-image-width, 45%), 52%);
}

.preview-content :deep(.blog-inline-image--full) {
  max-width: 100%;
}

.preview-content :deep(.blog-inline-image img) {
  display: block;
  width: 100%;
  height: auto;
  margin: 0;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.10);
}

.preview-content :deep(.blog-inline-image__caption) {
  margin-top: 0.625rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #64748b;
  text-align: center;
}

.preview-content :deep(.blog-image-placeholder) {
  margin: 1.5rem 0;
  padding: 1rem;
  border: 1px dashed #f59e0b;
  border-radius: 0.625rem;
  background: #fffbeb;
  color: #92400e;
  font-weight: 700;
  text-align: center;
}

.preview-content :deep(.blog-cta-card) {
  clear: both;
  display: grid;
  gap: 0;
  margin: 2.25rem 0;
  overflow: hidden;
  border: 1px solid #dbe4ff;
  border-radius: 1.375rem;
  background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.14);
}

.preview-content :deep(.blog-cta-card--split.blog-cta-card--has-image) {
  grid-template-columns: minmax(0, 1.05fr) minmax(260px, 0.95fr);
}

.preview-content :deep(.blog-cta-card--image-left.blog-cta-card--has-image .blog-cta-card__media) {
  order: -1;
}

.preview-content :deep(.blog-cta-card--image-bottom.blog-cta-card--has-image) {
  grid-template-columns: 1fr;
}

.preview-content :deep(.blog-cta-card--image-bottom .blog-cta-card__media) {
  order: 2;
}

.preview-content :deep(.blog-cta-card--solid) {
  display: block;
}

.preview-content :deep(.blog-cta-card--green) {
  background: linear-gradient(135deg, #4db6a6 0%, #99e5c7 100%);
  border-color: #74d2bd;
}

.preview-content :deep(.blog-cta-card--light) {
  background: #fff;
}

.preview-content :deep(.blog-cta-card__body) {
  padding: 1.875rem 2rem;
}

.preview-content :deep(.blog-cta-card__eyebrow) {
  margin: 0 0 0.625rem;
  color: #16a34a;
  font-size: 0.8125rem;
  font-weight: 900;
  line-height: 1.2;
  text-transform: uppercase;
}

.preview-content :deep(.blog-cta-card__title) {
  margin: 0 0 0.625rem;
  color: #0f2f6f;
  font-size: 1.875rem;
  font-weight: 900;
  line-height: 1.08;
  letter-spacing: 0;
}

.preview-content :deep(.blog-cta-card__text) {
  max-width: 35rem;
  margin: 0 0 1.25rem;
  color: #334155;
  font-size: 1.0625rem;
  line-height: 1.55;
}

.preview-content :deep(.blog-cta-card__button) {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.75rem;
  padding: 0.625rem 1.125rem;
  border-radius: 0.625rem;
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
  font-size: 1rem;
  font-weight: 900;
  line-height: 1.2;
  text-decoration: none;
  box-shadow: 0 10px 22px rgba(33, 85, 216, 0.24);
}

.preview-content :deep(.blog-cta-card__button:hover) {
  background: linear-gradient(180deg, #2a64e6 0%, #1d4ed8 100%);
  text-decoration: none;
}

.preview-content :deep(.blog-cta-card__media) {
  display: block;
  min-height: 100%;
  background: #e2e8f0;
}

.preview-content :deep(.blog-cta-card__media img) {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 15.625rem;
  margin: 0;
  object-fit: cover;
  border: 0;
  border-radius: 0;
  box-shadow: none;
}

.preview-content :deep(.blog-cta-card__media--empty) {
  display: grid;
  place-items: center;
  min-height: 13.75rem;
  padding: 1.5rem;
  color: #64748b;
  font-weight: 800;
}

.preview-content :deep(.blog-cta-card--green .blog-cta-card__eyebrow),
.preview-content :deep(.blog-cta-card--green .blog-cta-card__title),
.preview-content :deep(.blog-cta-card--green .blog-cta-card__text) {
  color: #fff;
}

.preview-content :deep(.blog-cta-card--green .blog-cta-card__button) {
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
}

.preview-content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1.25rem;
  border-radius: 0.625rem;
  overflow-x: auto;
  margin: 1.5rem 0;
  font-size: 0.875rem;
}

.preview-content :deep(code) {
  background: #f1f5f9;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.9em;
  color: #e11d48;
}

.preview-content :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.preview-content :deep(.blog-math) {
  color: #0f172a;
}

.preview-content :deep(.blog-math--inline) {
  display: inline-flex;
  max-width: 100%;
  vertical-align: -0.1em;
}

.preview-content :deep(.blog-math--display) {
  display: block;
  margin: 1.5rem 0;
  padding: 1.125rem 1.25rem;
  overflow-x: auto;
  background: #f8fbff;
  border: 1px solid #dbeafe;
  border-radius: 0.625rem;
  text-align: center;
}

.preview-content :deep(.blog-math--display .katex-display) {
  margin: 0;
}

.preview-content :deep(.blog-math--display .katex) {
  font-size: 1.12em;
}

.preview-content :deep(.blog-math-error) {
  background: #fff1f2;
  color: #be123c;
  border: 1px solid #fecdd3;
}

@media (max-width: 768px) {
  .form-row-2 { grid-template-columns: 1fr; }
  .form-row-3 { grid-template-columns: 1fr; }
  .post-meta-row { grid-template-columns: 1fr; }
  .form-row-4 { grid-template-columns: 1fr; }
  .form-row-4 .span-2 { grid-column: auto; }
  .filters { padding: 0.875rem; }
  .filters__head { align-items: flex-start; }
  .filters__controls { grid-template-columns: 1fr; }
  .admin-table { font-size: 0.8rem; display: block; overflow-x: auto; }
  .inline-images-head { flex-direction: column; }
  .content-field-head { flex-direction: column; align-items: flex-start; }
  .content-tools { justify-content: flex-start; width: 100%; }
  .inline-image-card { grid-template-columns: 1fr; }
  .preview-article { margin: 0; padding: 1.5rem; border-radius: 0; }
  .preview-title { font-size: 2rem; }
  .preview-content { font-size: 1rem; }
  .preview-content :deep(.blog-inline-image--left),
  .preview-content :deep(.blog-inline-image--right) {
    float: none;
    clear: both;
    max-width: 100%;
    margin: 1.5rem auto;
  }
  .preview-content :deep(.blog-cta-card),
  .preview-content :deep(.blog-cta-card--split.blog-cta-card--has-image) {
    grid-template-columns: 1fr;
  }
  .preview-content :deep(.blog-cta-card--image-left.blog-cta-card--has-image .blog-cta-card__media) {
    order: 0;
  }
  .preview-content :deep(.blog-cta-card__body) {
    padding: 1.5rem 1.25rem;
  }
  .preview-content :deep(.blog-cta-card__title) {
    font-size: 1.5rem;
  }
  .preview-content :deep(.blog-cta-card__media img) {
    min-height: 11.875rem;
  }
}
</style>
