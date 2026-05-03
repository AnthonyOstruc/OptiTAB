<template>
  <MainLayout>
    <main class="blog-page">
      <section
        class="blog-hero"
        :style="heroStyle"
        aria-labelledby="blog-title"
      >
      </section>

      <section class="blog-content">
        <nav class="breadcrumb" aria-label="Fil d'Ariane">
          <RouterLink to="/">Accueil</RouterLink>
          <span class="breadcrumb__sep">/</span>
          <span class="breadcrumb__current">Blog</span>
        </nav>

        <div class="blog-toolbar" aria-label="Recherche et filtres du blog">
          <div class="blog-toolbar__header">
            <h2>ARTICLES RÉCENTS</h2>
          </div>

        </div>

        <div v-if="loading" class="blog-loading">
          <div class="blog-loading__spinner"></div>
          <p>Chargement des articles...</p>
        </div>

        <div v-else-if="posts.length === 0" class="blog-empty">
          <p>Aucun article trouvé pour cette recherche.</p>
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
                  <span>OptiTAB</span>
                </div>

                <time
                  v-if="post.date_publication"
                  class="blog-card__date-badge"
                  :datetime="post.date_publication"
                  :title="formatDate(post.date_publication)"
                >
                  <span>{{ formatDateDay(post.date_publication) }}</span>
                  <small>{{ formatDateMonth(post.date_publication) }}</small>
                </time>
              </div>

              <div class="blog-card__body">
                <div class="blog-card__meta">
                  <span class="blog-card__reading">{{ post.reading_time }} min</span>
                </div>

                <h3 class="blog-card__title">{{ post.titre }}</h3>
                <p class="blog-card__excerpt">{{ post.extrait }}</p>

                <div class="blog-card__footer">
                  <div v-if="post.tags && post.tags.length" class="blog-card__tags">
                    <span
                      v-for="tag in post.tags.slice(0, 3)"
                      :key="tag.id"
                      class="blog-card__tag"
                    >
                      {{ tag.nom }}
                    </span>
                  </div>
                  <span class="blog-card__cta">Lire l'article</span>
                </div>
              </div>
            </RouterLink>
          </article>
        </div>

        <nav v-if="totalPages > 1" class="blog-pagination" aria-label="Pagination">
          <button
            class="blog-pagination__btn"
            :disabled="currentPage <= 1"
            type="button"
            @click="goToPage(currentPage - 1)"
          >
            Précédent
          </button>
          <span class="blog-pagination__info">Page {{ currentPage }} / {{ totalPages }}</span>
          <button
            class="blog-pagination__btn"
            :disabled="currentPage >= totalPages"
            type="button"
            @click="goToPage(currentPage + 1)"
          >
            Suivant
          </button>
        </nav>
      </section>
    </main>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
const blogHeroImage = '/Banner-blog.png'
import { getBlogPosts } from '@/api/blog'
import { setPageSeo, buildBreadcrumbJsonLd } from '@/services/seo'

const route = useRoute()
const router = useRouter()

const posts = ref([])
const loading = ref(true)
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = 12
const searchQuery = ref('')

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

const heroStyle = computed(() => ({
  backgroundImage: `url(${blogHeroImage})`
}))

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

function parseDate(dateStr) {
  if (!dateStr) return null
  const date = new Date(dateStr)
  return Number.isNaN(date.getTime()) ? null : date
}

function formatDate(dateStr) {
  const date = parseDate(dateStr)
  if (!date) return ''

  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
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

onMounted(() => {
  if (route.query.page) currentPage.value = parseInt(route.query.page) || 1

  fetchPosts()
  applySeo()
})
</script>

<style scoped>
.blog-page {
  min-height: 100vh;
  background: #f6f8fc;
}

.blog-hero {
  min-height: 330px;
  display: flex;
  align-items: center;
  background-position: center;
  background-size: cover;
  color: #ffffff;
}

.blog-hero__content {
  width: min(1120px, calc(100% - 48px));
  margin: 0 auto;
  padding: 64px 0;
}

.blog-hero__eyebrow {
  margin: 0 0 14px;
  color: #7bd389;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: 0;
}

.blog-hero h1 {
  max-width: 760px;
  margin: 0;
  color: #ffffff;
  font-size: clamp(34px, 5vw, 58px);
  font-weight: 900;
  hyphens: none;
  line-height: 1.04;
  letter-spacing: 0;
}

.blog-hero p:last-child {
  max-width: 640px;
  margin: 18px 0 0;
  color: rgba(255, 255, 255, 0.88);
  font-size: 18px;
  hyphens: none;
  line-height: 1.6;
}

.blog-content {
  width: min(1120px, calc(100% - 48px));
  margin: 0 auto;
  padding: 34px 0 80px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
  color: #667085;
  font-size: 13px;
}

.breadcrumb a {
  color: #315eea;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.breadcrumb__sep {
  color: #b8c0cc;
}

.breadcrumb__current {
  color: #111827;
  font-weight: 700;
}

.blog-toolbar {
  margin-bottom: 28px;
  padding-bottom: 22px;
  border-bottom: 1px solid #dfe5ef;
}

.blog-toolbar__header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-bottom: 20px;
}

.blog-kicker {
  margin: 0 0 7px;
  color: #315eea;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0;
  text-transform: uppercase;
}

.blog-toolbar h2 {
  margin: 0;
  color: #101828;
  font-size: 30px;
  font-weight: 900;
  line-height: 1.16;
}

.blog-toolbar p {
  margin: 8px 0 0;
  color: #5b6678;
  font-size: 15px;
  line-height: 1.5;
}

.blog-search {
  flex: 0 1 390px;
}

.blog-search__input {
  width: 100%;
  min-height: 44px;
  padding: 11px 14px;
  border: 1px solid #cfd8e6;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  font-size: 15px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.blog-search__input:focus {
  outline: none;
  border-color: #315eea;
  box-shadow: 0 0 0 3px rgba(49, 94, 234, 0.14);
}

.blog-loading,
.blog-empty {
  display: grid;
  place-items: center;
  min-height: 260px;
  color: #667085;
  text-align: center;
}

.blog-loading {
  gap: 12px;
}

.blog-loading__spinner {
  width: 34px;
  height: 34px;
  border: 3px solid #dce3ee;
  border-top-color: #315eea;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 26px;
  margin-bottom: 48px;
}

.blog-card {
  min-height: 100%;
  overflow: hidden;
  border: 1px solid #dfe5ef;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 12px 34px rgba(16, 24, 40, 0.06);
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}

.blog-card:hover {
  border-color: #bfd0ff;
  box-shadow: 0 18px 42px rgba(16, 24, 40, 0.12);
  transform: translateY(-3px);
}

.blog-card__link {
  min-height: 100%;
  display: flex;
  flex-direction: column;
  color: inherit;
  text-decoration: none;
}

.blog-card__image-wrap {
  position: relative;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: #e9eef8;
}

.blog-card__image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  transition: transform 0.25s;
}

.blog-card:hover .blog-card__image {
  transform: scale(1.035);
}

.blog-card__image-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  background:
    linear-gradient(135deg, rgba(49, 94, 234, 0.16), rgba(123, 211, 137, 0.18)),
    #eef3fb;
  color: #1f3c88;
  font-size: 13px;
  font-weight: 900;
}

.blog-card__date-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  width: 58px;
  min-height: 62px;
  display: grid;
  place-items: center;
  padding: 7px 5px;
  border-radius: 4px;
  background: #1f3c88;
  color: #ffffff;
  text-align: center;
  box-shadow: 0 14px 28px rgba(16, 24, 40, 0.2);
}

.blog-card__date-badge span {
  font-size: 23px;
  font-weight: 900;
  line-height: 1;
}

.blog-card__date-badge small {
  color: #eaf1ff;
  font-size: 11px;
  font-weight: 900;
  line-height: 1;
  text-transform: uppercase;
}

.blog-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.blog-card__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 9px;
  margin-bottom: 12px;
  color: #667085;
  font-size: 12px;
  font-weight: 700;
}

.blog-card__title {
  margin: 0 0 10px;
  color: #101828;
  font-size: 20px;
  font-weight: 900;
  line-height: 1.28;
}

.blog-card__excerpt {
  margin: 0;
  color: #475467;
  font-size: 14px;
  line-height: 1.65;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.blog-card__footer {
  margin-top: auto;
  padding-top: 18px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14px;
}

.blog-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}

.blog-card__tag {
  padding: 4px 8px;
  border-radius: 999px;
  background: #f1f4f9;
  color: #5b6678;
  font-size: 11px;
  font-weight: 800;
}

.blog-card__cta {
  flex: 0 0 auto;
  color: #315eea;
  font-size: 13px;
  font-weight: 900;
}

.blog-card:hover .blog-card__cta {
  color: #1f3c88;
}

.blog-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding-top: 12px;
}

.blog-pagination__btn {
  min-height: 40px;
  padding: 9px 18px;
  border: 1px solid #cfd8e6;
  border-radius: 8px;
  background: #ffffff;
  color: #315eea;
  cursor: pointer;
  font-size: 14px;
  font-weight: 800;
  transition: background-color 0.2s, border-color 0.2s;
}

.blog-pagination__btn:hover:not(:disabled) {
  border-color: #315eea;
  background: #eef3ff;
}

.blog-pagination__btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.blog-pagination__info {
  color: #667085;
  font-size: 14px;
  font-weight: 800;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 820px) {
  .blog-hero {
    min-height: 280px;
  }

  .blog-hero__content,
  .blog-content {
    width: min(100% - 32px, 1120px);
  }

  .blog-hero__content {
    padding: 48px 0;
  }

  .blog-hero h1 {
    font-size: 34px;
  }

  .blog-hero p:last-child {
    font-size: 16px;
  }

  .blog-content {
    padding: 26px 0 60px;
  }

  .blog-toolbar__header {
    display: block;
  }

  .blog-search {
    display: block;
    margin-top: 18px;
  }

  .blog-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }

  .blog-card__footer {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 520px) {
  .blog-hero {
    min-height: 250px;
    background-position: 58% center;
  }

  .blog-hero h1 {
    font-size: 30px;
  }

  .blog-toolbar h2 {
    font-size: 25px;
  }

  .blog-pagination {
    flex-wrap: wrap;
  }
}
</style>
