<template>
  <MainLayout>
    <main class="blog-detail-page">
      <!-- Fil d'Ariane -->
      <nav class="breadcrumb" aria-label="Fil d'Ariane" itemscope itemtype="https://schema.org/BreadcrumbList">
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <RouterLink to="/" itemprop="item"><span itemprop="name">Accueil</span></RouterLink>
          <meta itemprop="position" content="1" />
        </span>
        <span class="breadcrumb__sep">/</span>
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <RouterLink to="/blog" itemprop="item"><span itemprop="name">Blog</span></RouterLink>
          <meta itemprop="position" content="2" />
        </span>
        <span class="breadcrumb__sep">/</span>
        <span v-if="post" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
          <span class="breadcrumb__current" itemprop="name">{{ post.titre }}</span>
          <meta itemprop="position" content="3" />
        </span>
      </nav>

      <!-- Loading -->
      <div v-if="loading" class="blog-loading">
        <div class="blog-loading__spinner"></div>
        <p>Chargement de l'article…</p>
      </div>

      <!-- 404 -->
      <div v-else-if="!post" class="blog-not-found">
        <h1>Article introuvable</h1>
        <p>Cet article n'existe pas ou n'est plus disponible.</p>
        <RouterLink to="/blog" class="blog-back-link">← Retour au blog</RouterLink>
      </div>

      <!-- Article -->
      <article v-else class="blog-article" itemscope itemtype="https://schema.org/BlogPosting">
        <meta itemprop="mainEntityOfPage" :content="canonicalUrl" />
        <meta v-if="post.date_publication" itemprop="datePublished" :content="post.date_publication" />

        <header class="blog-article__header">
          <h1 class="blog-article__title" itemprop="headline">{{ post.titre }}</h1>
          <p v-if="post.extrait" class="blog-article__excerpt" itemprop="description">{{ post.extrait }}</p>
        </header>

        <!-- Image de couverture -->
        <div v-if="post.image_couverture_url" class="blog-article__cover">
          <img
            :src="post.image_couverture_url"
            :alt="post.alt_text_image || post.titre"
            itemprop="image"
            class="blog-article__cover-img"
          />
        </div>

        <div class="blog-article__layout">
          <!-- Table of Contents -->
          <aside v-if="toc.length > 1" class="blog-toc" aria-label="Sommaire">
            <button
              type="button"
              class="blog-toc__toggle"
              :aria-expanded="isTocExpanded"
              aria-controls="blog-article-toc"
              @click="isTocExpanded = !isTocExpanded"
            >
              <span class="blog-toc__title">Sommaire</span>
              <span class="blog-toc__state">{{ isTocExpanded ? 'Masquer' : 'Afficher' }}</span>
              <ChevronDownIcon
                class="blog-toc__chevron"
                :class="{ 'blog-toc__chevron--open': isTocExpanded }"
                aria-hidden="true"
              />
            </button>
            <ul
              v-show="isTocExpanded"
              id="blog-article-toc"
              class="blog-toc__list"
            >
              <li v-for="item in toc" :key="item.id" :class="`blog-toc__item--h${item.level}`">
                <a :href="`#${item.id}`" class="blog-toc__link">{{ item.text }}</a>
              </li>
            </ul>
          </aside>

          <!-- Contenu principal -->
          <div class="blog-article__content" itemprop="articleBody" v-html="renderedContent"></div>
        </div>

        <!-- Tags -->
        <div v-if="post.tags && post.tags.length" class="blog-article__tags">
          <RouterLink
            v-for="tag in post.tags"
            :key="tag.id"
            :to="`/blog/tag/${tag.slug}`"
            class="blog-article__tag"
          >
            #{{ tag.nom }}
          </RouterLink>
        </div>

        <!-- Hidden microdata -->
        <meta v-if="!isModifiedAfterPublication(post)"
          itemprop="dateModified" :content="post.date_modification || post.date_publication" />
      </article>

      <!-- Articles liés -->
      <section v-if="post && post.articles_lies && post.articles_lies.length" class="blog-related">
        <h2 class="blog-related__title">Articles similaires</h2>
        <div class="blog-related__grid">
          <article
            v-for="related in post.articles_lies"
            :key="related.id"
            class="blog-related-card"
          >
            <RouterLink :to="`/blog/${related.slug}`" class="blog-related-card__link">
              <div class="blog-related-card__image-wrap">
                <img
                  v-if="related.image_couverture_url"
                  :src="related.image_couverture_url"
                  :alt="related.alt_text_image || related.titre"
                  class="blog-related-card__image"
                  loading="lazy"
                />
                <time
                  v-if="related.date_publication"
                  class="blog-related-card__date-badge"
                  :datetime="related.date_publication"
                  :title="formatDate(related.date_publication)"
                >
                  <span>{{ formatDateDay(related.date_publication) }}</span>
                  <small>{{ formatDateMonth(related.date_publication) }}</small>
                </time>
              </div>
              <div class="blog-related-card__body">
                <h3 class="blog-related-card__title">{{ related.titre }}</h3>
                <p class="blog-related-card__excerpt">{{ related.extrait }}</p>
                <span class="blog-related-card__cta">Lire plus</span>
              </div>
            </RouterLink>
          </article>
        </div>
      </section>

    </main>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'
import 'katex/dist/katex.min.css'
import '@/assets/styles/blogArticle.css'
import MainLayout from '@/components/layout/MainLayout.vue'
import { getBlogPost } from '@/api/blog'
import { setPageSeo, buildArticleJsonLd, buildBreadcrumbJsonLd } from '@/services/seo'
import { extractBlogToc, renderBlogMarkdown } from '@/utils/blogRenderer'

const route = useRoute()
const post = ref(null)
const loading = ref(true)
const isTocExpanded = ref(false)

const canonicalUrl = computed(() => {
  const base = 'https://www.optitab.net'
  return post.value ? `${base}/blog/${post.value.slug}` : `${base}/blog`
})

// Rendu Markdown → HTML
const renderedContent = computed(() => {
  if (!post.value?.contenu) return ''
  return renderBlogMarkdown(post.value.contenu, {
    title: post.value.titre,
    images: post.value.images || [],
  })
})

// Table of Contents
const toc = computed(() => {
  if (!post.value?.contenu) return []
  return extractBlogToc(post.value.contenu)
})

function parseDate(dateStr) {
  if (!dateStr) return null
  const date = new Date(dateStr)
  return Number.isNaN(date.getTime()) ? null : date
}

function formatDate(dateStr) {
  const date = parseDate(dateStr)
  if (!date) return ''
  return date.toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

function formatDateDay(dateStr) {
  const date = parseDate(dateStr)
  if (!date) return ''
  return date.toLocaleDateString('fr-FR', { day: '2-digit' })
}

function formatDateMonth(dateStr) {
  const date = parseDate(dateStr)
  if (!date) return ''
  return date.toLocaleDateString('fr-FR', { month: 'short' }).replace('.', '')
}

function isModifiedAfterPublication(post) {
  if (!post.date_modification || !post.date_publication) return false
  const pub = new Date(post.date_publication)
  const mod = new Date(post.date_modification)
  // Show "updated" only if modification is at least 1 day after publication
  return (mod - pub) > 86400000
}

function applySeo() {
  if (!post.value) return
  const p = post.value
  const seoTitle = p.seo_title || p.titre
  const seoDescription = p.meta_description || p.extrait || ''
  const ogTitle = seoTitle
  const ogDescription = seoDescription
  const ogImage = p.image_couverture_url || p.og_image_url || ''

  // Robots: noindex pour brouillons ou si meta_robots = noindex
  const isDraft = p.statut !== 'published'
  const isNoindex = p.meta_robots === 'noindex'
  const robots = (isDraft || isNoindex)
    ? 'noindex,follow'
    : 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1'

  const breadcrumbs = [
    { name: 'Accueil', item: '/' },
    { name: 'Blog', item: '/blog' },
    { name: p.titre, item: `/blog/${p.slug}` }
  ]

  const articleGraph = buildArticleJsonLd({
    url: `/blog/${p.slug}`,
    headline: seoTitle,
    description: seoDescription,
    datePublished: p.date_publication,
    dateModified: p.date_modification,
    image: ogImage,
    author: { '@type': 'Person', name: p.auteur_nom || 'OptiTAB' },
  })

  const breadcrumbGraph = buildBreadcrumbJsonLd(breadcrumbs)

  setPageSeo({
    title: seoTitle,
    description: seoDescription,
    canonicalPath: `/blog/${p.slug}`,
    ogType: 'article',
    image: ogImage,
    robots,
    jsonLdGraph: [articleGraph, breadcrumbGraph].filter(Boolean)
  })

  // OG overrides
  if (typeof document !== 'undefined') {
    const setMeta = (prop, content) => {
      if (!content) return
      let el = document.querySelector(`meta[property="${prop}"]`)
      if (!el) {
        el = document.createElement('meta')
        el.setAttribute('property', prop)
        document.head.appendChild(el)
      }
      el.setAttribute('content', content)
    }
    setMeta('og:title', ogTitle)
    setMeta('og:description', ogDescription)
    if (ogImage) setMeta('og:image', ogImage)
    setMeta('article:published_time', p.date_publication)
    setMeta('article:modified_time', p.date_modification)
    if (p.tags?.length) {
      p.tags.forEach(t => setMeta('article:tag', t.nom))
    }
  }
}

async function fetchPost() {
  const slug = route.params.slug
  if (!slug) return
  loading.value = true
  try {
    const { data } = await getBlogPost(slug)
    post.value = data
    applySeo()
  } catch (_) {
    post.value = null
  } finally {
    loading.value = false
  }
}

onMounted(fetchPost)
watch(() => route.params.slug, fetchPost)
</script>

<style scoped>
.blog-detail-page {
  min-height: 100vh;
  background: #f7f9fc;
  padding: 40px 20px 80px;
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 1080px;
  margin: 0 auto 24px;
  font-size: 13px;
  color: #64748b;
}
.breadcrumb a { color: #3b82f6; text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb__sep { color: #cbd5e1; }
.breadcrumb__current { color: #0f172a; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 300px; }

/* Loading / Error */
.blog-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 0;
  color: #64748b;
  gap: 12px;
}
.blog-loading__spinner {
  width: 32px; height: 32px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.blog-not-found {
  text-align: center;
  padding: 80px 0;
  color: #475569;
}
.blog-not-found h1 { font-size: 24px; color: #0f172a; margin-bottom: 8px; }
.blog-back-link { color: #3b82f6; font-weight: 600; text-decoration: none; }
.blog-back-link:hover { text-decoration: underline; }

/* Article Header */
.blog-article {
  max-width: 1080px;
  margin: 0 auto;
  padding: 40px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
}

.blog-article__header {
  margin-bottom: 34px;
  padding-bottom: 28px;
  border-bottom: 1px solid #e2e8f0;
}
.blog-article__title {
  margin: 0 0 12px;
  font-size: clamp(28px, 3.4vw, 38px);
  font-weight: 600;
  color: #10257f;
  line-height: 1.18;
  letter-spacing: 0;
}
.blog-article__excerpt {
  margin: 0 0 12px;
  max-width: 780px;
  font-size: 18px;
  color: #475569;
  line-height: 1.6;
}
/* Cover */
.blog-article__cover {
  margin-bottom: 32px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}
.blog-article__cover-img {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 12px;
}

/* Layout: TOC + Content */
.blog-article__layout {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 28px;
}

/* Table of Contents */
.blog-toc {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0;
  margin-bottom: 32px;
  overflow: hidden;
}
.blog-toc__toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-align: left;
}
.blog-toc__title {
  margin: 0;
  font-size: 14px;
  font-weight: 800;
  color: #111827;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  flex: 1;
}
.blog-toc__state {
  color: #64748b;
  font-size: 13px;
  font-weight: 700;
}
.blog-toc__chevron {
  width: 20px;
  height: 20px;
  flex: 0 0 20px;
  color: #64748b;
  transition: transform 0.2s ease;
  transform-origin: center;
}
.blog-toc__chevron--open {
  transform: rotate(180deg);
}
.blog-toc__list {
  list-style: none;
  margin: 0;
  padding: 0 20px 16px;
}
.blog-toc__list li {
  margin-bottom: 6px;
}
.blog-toc__item--h3 {
  padding-left: 16px;
}
.blog-toc__link {
  color: #2563eb;
  text-decoration: none;
  font-size: 14px;
  line-height: 1.5;
}
.blog-toc__link:hover {
  text-decoration: underline;
}

/* Article Content (Markdown rendered) */
.blog-article__content {
  font-size: 17px;
  line-height: 1.75;
  color: #1e293b;
  word-break: break-word;
}
.blog-article__content :deep(h2) {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin: 44px 0 18px;
  padding: 0 0 12px;
  border-bottom: 3px solid #6366f1;
  letter-spacing: -0.01em;
}
.blog-article__content :deep(h3) {
  font-size: 19px;
  font-weight: 700;
  color: #374151;
  margin: 32px 0 12px;
  padding-left: 16px;
  border-left: 4px solid #6366f1;
  letter-spacing: -0.005em;
}
.blog-article__content :deep(p) {
  margin: 0 0 20px;
}
.blog-article__content :deep(a) {
  color: #2563eb;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.blog-article__content :deep(strong) {
  font-weight: 700;
  color: #111827;
}
.blog-article__content :deep(ul),
.blog-article__content :deep(ol) {
  margin: 0 0 20px;
  padding-left: 24px;
}
.blog-article__content :deep(li) {
  margin-bottom: 6px;
}
.blog-article__content :deep(blockquote) {
  margin: 24px 0;
  padding: 16px 24px;
  border-left: 4px solid #2563eb;
  background: #eff6ff;
  border-radius: 0 10px 10px 0;
  color: #1e40af;
  font-style: italic;
}
.blog-article__content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 24px 0;
}

.blog-article__content :deep(.blog-inline-image) {
  max-width: min(var(--blog-image-width, 100%), 100%);
  margin: 28px auto;
  clear: both;
}

.blog-article__content :deep(.blog-inline-image--left) {
  float: left;
  clear: left;
  margin: 8px 28px 20px 0;
  max-width: min(var(--blog-image-width, 45%), 52%);
}

.blog-article__content :deep(.blog-inline-image--right) {
  float: right;
  clear: right;
  margin: 8px 0 20px 28px;
  max-width: min(var(--blog-image-width, 45%), 52%);
}

.blog-article__content :deep(.blog-inline-image--full) {
  max-width: 100%;
}

.blog-article__content :deep(.blog-inline-image img) {
  display: block;
  width: 100%;
  height: auto;
  margin: 0;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.10);
}

.blog-article__content :deep(.blog-inline-image__caption) {
  margin-top: 10px;
  font-size: 14px;
  line-height: 1.5;
  color: #64748b;
  text-align: center;
}

.blog-article__content :deep(.blog-image-placeholder) {
  margin: 24px 0;
  padding: 18px;
  border: 1px dashed #f59e0b;
  border-radius: 10px;
  background: #fffbeb;
  color: #92400e;
  font-weight: 600;
  text-align: center;
}

.blog-article__content :deep(.blog-cta-card) {
  clear: both;
  display: grid;
  gap: 0;
  margin: 36px 0;
  overflow: hidden;
  border: 1px solid #dbe4ff;
  border-radius: 22px;
  background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
  box-shadow: 0 18px 42px rgba(15, 23, 42, 0.14);
}

.blog-article__content :deep(.blog-cta-card--split.blog-cta-card--has-image) {
  grid-template-columns: minmax(0, 1.05fr) minmax(260px, 0.95fr);
}

.blog-article__content :deep(.blog-cta-card--image-left.blog-cta-card--has-image .blog-cta-card__media) {
  order: -1;
}

.blog-article__content :deep(.blog-cta-card--image-bottom.blog-cta-card--has-image) {
  grid-template-columns: 1fr;
}

.blog-article__content :deep(.blog-cta-card--image-bottom .blog-cta-card__media) {
  order: 2;
}

.blog-article__content :deep(.blog-cta-card--solid) {
  display: block;
  background: linear-gradient(135deg, #4db6a6 0%, #99e5c7 100%);
  border-color: #74d2bd;
}

.blog-article__content :deep(.blog-cta-card--light) {
  background: #ffffff;
}

.blog-article__content :deep(.blog-cta-card--green) {
  background: linear-gradient(135deg, #4db6a6 0%, #99e5c7 100%);
  border-color: #74d2bd;
}

.blog-article__content :deep(.blog-cta-card__body) {
  padding: 30px 32px;
}

.blog-article__content :deep(.blog-cta-card__eyebrow) {
  margin: 0 0 10px;
  color: #16a34a;
  font-size: 13px;
  font-weight: 900;
  line-height: 1.2;
  text-transform: uppercase;
}

.blog-article__content :deep(.blog-cta-card__title) {
  margin: 0 0 10px;
  color: #0f2f6f;
  font-size: 30px;
  font-weight: 900;
  line-height: 1.08;
  letter-spacing: 0;
}

.blog-article__content :deep(.blog-cta-card__text) {
  max-width: 560px;
  margin: 0 0 20px;
  color: #334155;
  font-size: 17px;
  line-height: 1.55;
}

.blog-article__content :deep(.blog-cta-card__button) {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 18px;
  border-radius: 10px;
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
  font-size: 16px;
  font-weight: 900;
  line-height: 1.2;
  text-decoration: none;
  box-shadow: 0 10px 22px rgba(33, 85, 216, 0.24);
}

.blog-article__content :deep(.blog-cta-card__button:hover) {
  background: linear-gradient(180deg, #2a64e6 0%, #1d4ed8 100%);
  text-decoration: none;
}

.blog-article__content :deep(.blog-cta-card__media) {
  display: block;
  min-height: 100%;
  background: #e2e8f0;
}

.blog-article__content :deep(.blog-cta-card__media img) {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 250px;
  margin: 0;
  object-fit: cover;
  border: 0;
  border-radius: 0;
  box-shadow: none;
}

.blog-article__content :deep(.blog-cta-card__media--empty) {
  display: grid;
  place-items: center;
  min-height: 220px;
  padding: 24px;
  color: #64748b;
  font-weight: 800;
}

.blog-article__content :deep(.blog-cta-card--green .blog-cta-card__eyebrow),
.blog-article__content :deep(.blog-cta-card--green .blog-cta-card__title),
.blog-article__content :deep(.blog-cta-card--green .blog-cta-card__text) {
  color: #ffffff;
}

.blog-article__content :deep(.blog-cta-card--green .blog-cta-card__button) {
  background: linear-gradient(180deg, #2f6df4 0%, #2155d8 100%);
  color: #ffffff;
}

.blog-article__content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 20px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 24px 0;
  font-size: 14px;
}
.blog-article__content :deep(code) {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  color: #e11d48;
}
.blog-article__content :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.blog-article__content :deep(.blog-math) {
  color: #0f172a;
}

.blog-article__content :deep(.blog-math--inline) {
  display: inline-flex;
  max-width: 100%;
  vertical-align: -0.1em;
}

.blog-article__content :deep(.blog-math--display) {
  display: block;
  margin: 24px 0;
  padding: 18px 20px;
  overflow-x: auto;
  background: #f8fbff;
  border: 1px solid #dbeafe;
  border-radius: 10px;
  text-align: center;
}

.blog-article__content :deep(.blog-math--display .katex-display) {
  margin: 0;
}

.blog-article__content :deep(.blog-math--display .katex) {
  font-size: 1.12em;
}

.blog-article__content :deep(.blog-math-error) {
  background: #fff1f2;
  color: #be123c;
  border: 1px solid #fecdd3;
}

/* Tags */
.blog-article__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
  clear: both;
}
.blog-article__tag {
  font-size: 13px;
  color: #3b82f6;
  background: #eef2ff;
  padding: 4px 12px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 600;
}
.blog-article__tag:hover {
  background: #dbeafe;
}

/* Related Articles */
.blog-related {
  max-width: 1080px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 56px;
  padding-top: 40px;
  border-top: 1px solid #e2e8f0;
}
.blog-related__title {
  margin: 0 0 24px;
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  padding-bottom: 12px;
  border-bottom: 3px solid #6366f1;
  letter-spacing: -0.01em;
}
.blog-related__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}
.blog-related-card {
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 12px 34px rgba(16, 24, 40, 0.06);
  transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s;
}
.blog-related-card:hover {
  border-color: #bfd0ff;
  box-shadow: 0 18px 42px rgba(16, 24, 40, 0.12);
  transform: translateY(-3px);
}
.blog-related-card__link {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
}
.blog-related-card__image-wrap {
  position: relative;
  aspect-ratio: 16 / 10;
  background: #f1f5f9;
  overflow: hidden;
}
.blog-related-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.blog-related-card__date-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 54px;
  min-height: 58px;
  display: grid;
  place-items: center;
  padding: 7px 5px;
  border-radius: 4px;
  background: #1f3c88;
  color: #ffffff;
  text-align: center;
  box-shadow: 0 12px 26px rgba(16, 24, 40, 0.22);
}
.blog-related-card__date-badge span {
  font-size: 21px;
  font-weight: 900;
  line-height: 1;
}
.blog-related-card__date-badge small {
  color: #eaf1ff;
  font-size: 10px;
  font-weight: 900;
  line-height: 1;
  text-transform: uppercase;
}
.blog-related-card__body {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
}
.blog-related-card__title {
  margin: 0 0 6px;
  font-size: 16px;
  font-weight: 800;
  color: #111827;
  line-height: 1.3;
}
.blog-related-card__excerpt {
  margin: 0;
  font-size: 13px;
  color: #64748b;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.blog-related-card__cta {
  margin-top: auto;
  padding-top: 16px;
  color: #315eea;
  font-size: 13px;
  font-weight: 900;
}

/* Responsive */
@media (min-width: 1100px) {
  .blog-article__layout {
    grid-template-columns: minmax(0, 1fr);
    align-items: start;
  }
}

@media (max-width: 768px) {
  .blog-detail-page {
    padding: 24px 14px 60px;
  }
  .blog-article {
    padding: 24px 18px;
    border-radius: 12px;
  }
  .blog-article__title {
    font-size: 26px;
  }
  .blog-article__excerpt {
    font-size: 16px;
  }
  .blog-article__content {
    font-size: 16px;
  }
  .blog-article__content :deep(.blog-inline-image--left),
  .blog-article__content :deep(.blog-inline-image--right) {
    float: none;
    clear: both;
    max-width: 100%;
    margin: 24px auto;
  }
  .blog-article__content :deep(.blog-cta-card),
  .blog-article__content :deep(.blog-cta-card--split.blog-cta-card--has-image) {
    grid-template-columns: 1fr;
  }
  .blog-article__content :deep(.blog-cta-card--image-left.blog-cta-card--has-image .blog-cta-card__media) {
    order: 0;
  }
  .blog-article__content :deep(.blog-cta-card__body) {
    padding: 24px 20px;
  }
  .blog-article__content :deep(.blog-cta-card__title) {
    font-size: 24px;
  }
  .blog-article__content :deep(.blog-cta-card__media img) {
    min-height: 190px;
  }
  .blog-related__grid {
    grid-template-columns: 1fr;
  }
}
</style>
