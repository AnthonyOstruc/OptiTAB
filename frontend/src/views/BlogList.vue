<template>
  <MainLayout>
    <main class="blog-page">
      <!-- Fil d'Ariane -->
      <nav class="breadcrumb" aria-label="Fil d'Ariane">
        <RouterLink to="/">Accueil</RouterLink>
        <span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">Blog</span>
      </nav>

      <header class="blog-header">
        <h1 class="blog-title">Blog OptiTAB</h1>
        <p class="blog-subtitle">Conseils, méthodes et astuces pour progresser en maths.</p>
      </header>

      <!-- Barre de recherche + filtres -->
      <div class="blog-toolbar">
        <div class="blog-search">
          <input
            v-model="searchQuery"
            type="search"
            placeholder="Rechercher un article…"
            class="blog-search__input"
            @input="debouncedSearch"
          />
        </div>
        <div class="blog-filters">
          <button
            class="blog-filter-btn"
            :class="{ 'blog-filter-btn--active': !activeCategory }"
            @click="setCategory(null)"
          >
            Tous
          </button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="blog-filter-btn"
            :class="{ 'blog-filter-btn--active': activeCategory === cat.slug }"
            @click="setCategory(cat.slug)"
          >
            {{ cat.nom }}
            <span v-if="cat.articles_count" class="blog-filter-count">{{ cat.articles_count }}</span>
          </button>
        </div>
      </div>

      <!-- Liste des articles -->
      <div v-if="loading" class="blog-loading">
        <div class="blog-loading__spinner"></div>
        <p>Chargement des articles…</p>
      </div>

      <div v-else-if="posts.length === 0" class="blog-empty">
        <p>Aucun article trouvé.</p>
      </div>

      <div v-else class="blog-grid">
        <article
          v-for="post in posts"
          :key="post.id"
          class="blog-card"
        >
          <RouterLink :to="`/blog/${post.slug}`" class="blog-card__link">
            <div class="blog-card__image-wrap">
              <img
                v-if="post.image_couverture_url"
                :src="post.image_couverture_url"
                :alt="post.titre"
                class="blog-card__image"
                loading="lazy"
              />
              <div v-else class="blog-card__image-placeholder">
                <svg width="48" height="48" fill="none" viewBox="0 0 24 24"><path stroke="#94a3b8" stroke-width="1.5" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"/></svg>
              </div>
            </div>
            <div class="blog-card__body">
              <div class="blog-card__meta">
                <span v-if="post.categorie" class="blog-card__category">{{ post.categorie.nom }}</span>
                <span class="blog-card__date">{{ formatDate(post.date_publication) }}</span>
                <span class="blog-card__reading">{{ post.reading_time }} min</span>
              </div>
              <h2 class="blog-card__title">{{ post.titre }}</h2>
              <p class="blog-card__excerpt">{{ post.extrait }}</p>
              <div class="blog-card__tags" v-if="post.tags && post.tags.length">
                <span v-for="tag in post.tags.slice(0, 3)" :key="tag.id" class="blog-card__tag">
                  {{ tag.nom }}
                </span>
              </div>
            </div>
          </RouterLink>
        </article>
      </div>

      <!-- Pagination -->
      <nav v-if="totalPages > 1" class="blog-pagination" aria-label="Pagination">
        <button
          class="blog-pagination__btn"
          :disabled="currentPage <= 1"
          @click="goToPage(currentPage - 1)"
        >
          ← Précédent
        </button>
        <span class="blog-pagination__info">Page {{ currentPage }} / {{ totalPages }}</span>
        <button
          class="blog-pagination__btn"
          :disabled="currentPage >= totalPages"
          @click="goToPage(currentPage + 1)"
        >
          Suivant →
        </button>
      </nav>
    </main>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import { getBlogPosts, getBlogCategories } from '@/api/blog'
import { setPageSeo, buildBreadcrumbJsonLd } from '@/services/seo'

const route = useRoute()
const router = useRouter()

const posts = ref([])
const categories = ref([])
const loading = ref(true)
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = 12
const searchQuery = ref('')
const activeCategory = ref(null)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

function applySeo() {
  const breadcrumbs = [
    { name: 'Accueil', item: '/' },
    { name: 'Blog', item: '/blog' }
  ]
  const breadcrumbGraph = buildBreadcrumbJsonLd(breadcrumbs)

  setPageSeo({
    title: 'Blog maths : conseils, méthodes et astuces | OptiTAB',
    description: 'Retrouvez nos articles, conseils et méthodes pour progresser en maths du collège à la prépa. Blog OptiTAB.',
    canonicalPath: '/blog',
    robots: 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1',
    jsonLdGraph: [breadcrumbGraph].filter(Boolean)
  })
}

let searchTimeout = null
function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchPosts()
  }, 400)
}

function setCategory(slug) {
  activeCategory.value = slug
  currentPage.value = 1
  if (slug) {
    router.replace({ query: { ...route.query, categorie: slug, page: undefined } })
  } else {
    const { categorie, ...rest } = route.query
    router.replace({ query: rest })
  }
  fetchPosts()
}

function goToPage(page) {
  currentPage.value = page
  router.replace({ query: { ...route.query, page: page > 1 ? page : undefined } })
  fetchPosts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function fetchPosts() {
  loading.value = true
  try {
    const params = { page: currentPage.value, page_size: pageSize }
    if (activeCategory.value) params.categorie = activeCategory.value
    if (searchQuery.value.trim()) params.search = searchQuery.value.trim()
    const { data } = await getBlogPosts(params)
    posts.value = data.results || []
    totalCount.value = data.count || 0
  } catch (e) {
    posts.value = []
    totalCount.value = 0
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const { data } = await getBlogCategories()
    categories.value = data || []
  } catch (_) {
    categories.value = []
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

onMounted(() => {
  if (route.query.categorie) activeCategory.value = route.query.categorie
  if (route.query.page) currentPage.value = parseInt(route.query.page) || 1
  fetchCategories()
  fetchPosts()
  applySeo()
})
</script>

<style scoped>
.blog-page {
  min-height: 100vh;
  background: #ffffff;
  padding: 48px 32px 80px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
  font-size: 13px;
  color: #64748b;
}
.breadcrumb a {
  color: #3b82f6;
  text-decoration: none;
}
.breadcrumb a:hover {
  text-decoration: underline;
}
.breadcrumb__sep {
  color: #cbd5e1;
}
.breadcrumb__current {
  color: #0f172a;
  font-weight: 600;
}

/* Header */
.blog-header {
  margin-bottom: 32px;
}
.blog-title {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
}
.blog-subtitle {
  margin: 0;
  font-size: 16px;
  color: #475569;
  line-height: 1.5;
}

/* Toolbar */
.blog-toolbar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}
.blog-search__input {
  width: 100%;
  max-width: 420px;
  padding: 10px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  color: #0f172a;
  background: #f8fafc;
  transition: border-color 0.2s;
}
.blog-search__input:focus {
  outline: none;
  border-color: #3b82f6;
  background: #fff;
}
.blog-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.blog-filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s;
}
.blog-filter-btn:hover {
  background: #e0e7ff;
  color: #3730a3;
}
.blog-filter-btn--active {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}
.blog-filter-count {
  font-size: 11px;
  background: rgba(255,255,255,0.25);
  padding: 1px 6px;
  border-radius: 999px;
}

/* Loading */
.blog-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 64px 0;
  color: #64748b;
  gap: 12px;
}
.blog-loading__spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.blog-empty {
  text-align: center;
  padding: 64px 0;
  color: #64748b;
  font-size: 15px;
}

/* Grid */
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

/* Card */
.blog-card {
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  background: #fff;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
}
.blog-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}
.blog-card__link {
  display: block;
  text-decoration: none;
  color: inherit;
}
.blog-card__image-wrap {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f1f5f9;
}
.blog-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.blog-card__image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
}
.blog-card__body {
  padding: 20px;
}
.blog-card__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 12px;
  color: #64748b;
}
.blog-card__category {
  background: #eef2ff;
  color: #3730a3;
  padding: 2px 10px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 11px;
}
.blog-card__title {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.3;
}
.blog-card__excerpt {
  margin: 0 0 12px;
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.blog-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.blog-card__tag {
  font-size: 11px;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 999px;
}

/* Pagination */
.blog-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 24px 0;
}
.blog-pagination__btn {
  padding: 8px 18px;
  font-size: 14px;
  font-weight: 600;
  color: #3b82f6;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}
.blog-pagination__btn:hover:not(:disabled) {
  background: #eef2ff;
}
.blog-pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.blog-pagination__info {
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 768px) {
  .blog-page {
    padding: 24px 16px 60px;
  }
  .blog-title {
    font-size: 24px;
  }
  .blog-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .blog-card__image-wrap {
    height: 180px;
  }
}
</style>
