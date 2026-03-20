<template>
  <MainLayout>
    <main class="blog-page">
      <!-- Fil d'Ariane -->
      <nav class="breadcrumb" aria-label="Fil d'Ariane">
        <RouterLink to="/">Accueil</RouterLink>
        <span class="breadcrumb__sep">/</span>
        <RouterLink to="/blog">Blog</RouterLink>
        <span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">Catégorie : {{ categoryName }}</span>
      </nav>

      <header class="blog-header">
        <h1 class="blog-title">{{ categoryName }}</h1>
        <p v-if="categoryDescription" class="blog-subtitle">{{ categoryDescription }}</p>
      </header>

      <div v-if="loading" class="blog-loading">
        <div class="blog-loading__spinner"></div>
        <p>Chargement…</p>
      </div>

      <div v-else-if="posts.length === 0" class="blog-empty">
        <p>Aucun article dans cette catégorie.</p>
        <RouterLink to="/blog" class="blog-back-link">← Retour au blog</RouterLink>
      </div>

      <div v-else class="blog-grid">
        <article v-for="post in posts" :key="post.id" class="blog-card">
          <RouterLink :to="`/blog/${post.slug}`" class="blog-card__link">
            <div class="blog-card__image-wrap">
              <img v-if="post.image_couverture_url" :src="post.image_couverture_url" :alt="post.titre" class="blog-card__image" loading="lazy" />
              <div v-else class="blog-card__image-placeholder">
                <svg width="48" height="48" fill="none" viewBox="0 0 24 24"><path stroke="#94a3b8" stroke-width="1.5" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"/></svg>
              </div>
            </div>
            <div class="blog-card__body">
              <div class="blog-card__meta">
                <span class="blog-card__date">{{ formatDate(post.date_publication) }}</span>
                <span class="blog-card__reading">{{ post.reading_time }} min</span>
              </div>
              <h2 class="blog-card__title">{{ post.titre }}</h2>
              <p class="blog-card__excerpt">{{ post.extrait }}</p>
            </div>
          </RouterLink>
        </article>
      </div>

      <nav v-if="totalPages > 1" class="blog-pagination" aria-label="Pagination">
        <button class="blog-pagination__btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">← Précédent</button>
        <span class="blog-pagination__info">Page {{ currentPage }} / {{ totalPages }}</span>
        <button class="blog-pagination__btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">Suivant →</button>
      </nav>
    </main>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import { getBlogPosts, getBlogCategoryDetail } from '@/api/blog'
import { setPageSeo, buildBreadcrumbJsonLd } from '@/services/seo'

const route = useRoute()
const router = useRouter()

const posts = ref([])
const loading = ref(true)
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = 12
const categoryName = ref('')
const categoryDescription = ref('')
const categoryMeta = ref(null)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

function goToPage(page) {
  currentPage.value = page
  fetchPosts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function applySeo(cat) {
  const name = cat?.nom || categoryName.value
  const slug = route.params.slug
  const metaDesc = cat?.meta_description || cat?.description || `Articles de la catégorie ${name} sur le blog OptiTAB.`
  const robots = cat?.meta_robots === 'noindex'
    ? 'noindex,follow'
    : 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1'

  const breadcrumbs = [
    { name: 'Accueil', item: '/' },
    { name: 'Blog', item: '/blog' },
    { name: name, item: `/blog/categorie/${slug}` }
  ]
  const breadcrumbGraph = buildBreadcrumbJsonLd(breadcrumbs)

  setPageSeo({
    title: `${name} — Blog OptiTAB`,
    description: metaDesc,
    canonicalPath: `/blog/categorie/${slug}`,
    robots,
    jsonLdGraph: [breadcrumbGraph].filter(Boolean)
  })
}

async function fetchPosts() {
  const slug = route.params.slug
  if (!slug) return
  loading.value = true
  try {
    // Get category info via detail endpoint
    const { data: cat } = await getBlogCategoryDetail(slug)
    categoryMeta.value = cat
    categoryName.value = cat?.nom || slug
    categoryDescription.value = cat?.description || ''
    applySeo(cat)

    const { data } = await getBlogPosts({ categorie: slug, page: currentPage.value, page_size: pageSize })
    posts.value = data.results || []
    totalCount.value = data.count || 0
  } catch (_) {
    posts.value = []
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}

onMounted(fetchPosts)
watch(() => route.params.slug, fetchPosts)
</script>

<style scoped>
.blog-page { min-height: 100vh; background: #fff; padding: 48px 32px 80px; max-width: 1200px; margin: 0 auto; }
.breadcrumb { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; font-size: 13px; color: #64748b; }
.breadcrumb a { color: #3b82f6; text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }
.breadcrumb__sep { color: #cbd5e1; }
.breadcrumb__current { color: #0f172a; font-weight: 600; }
.blog-header { margin-bottom: 32px; }
.blog-title { margin: 0 0 8px; font-size: 32px; font-weight: 900; color: #0f172a; }
.blog-subtitle { margin: 0; font-size: 16px; color: #475569; }
.blog-loading { display: flex; flex-direction: column; align-items: center; padding: 64px 0; color: #64748b; gap: 12px; }
.blog-loading__spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #3b82f6; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.blog-empty { text-align: center; padding: 64px 0; color: #64748b; }
.blog-back-link { color: #3b82f6; font-weight: 600; text-decoration: none; }
.blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; margin-bottom: 48px; }
.blog-card { border-radius: 16px; border: 1px solid #e2e8f0; background: #fff; overflow: hidden; transition: box-shadow 0.2s, transform 0.2s; }
.blog-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.08); transform: translateY(-2px); }
.blog-card__link { display: block; text-decoration: none; color: inherit; }
.blog-card__image-wrap { width: 100%; height: 200px; overflow: hidden; background: #f1f5f9; }
.blog-card__image { width: 100%; height: 100%; object-fit: cover; }
.blog-card__image-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
.blog-card__body { padding: 20px; }
.blog-card__meta { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px; font-size: 12px; color: #64748b; }
.blog-card__title { margin: 0 0 8px; font-size: 18px; font-weight: 800; color: #0f172a; line-height: 1.3; }
.blog-card__excerpt { margin: 0; font-size: 14px; color: #475569; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.blog-pagination { display: flex; align-items: center; justify-content: center; gap: 16px; padding: 24px 0; }
.blog-pagination__btn { padding: 8px 18px; font-size: 14px; font-weight: 600; color: #3b82f6; background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; cursor: pointer; }
.blog-pagination__btn:hover:not(:disabled) { background: #eef2ff; }
.blog-pagination__btn:disabled { opacity: 0.4; cursor: not-allowed; }
.blog-pagination__info { font-size: 14px; color: #64748b; font-weight: 600; }
@media (max-width: 768px) {
  .blog-page { padding: 24px 16px 60px; }
  .blog-title { font-size: 24px; }
  .blog-grid { grid-template-columns: 1fr; }
}
</style>
