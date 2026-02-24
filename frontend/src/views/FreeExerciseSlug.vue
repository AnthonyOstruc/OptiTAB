<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FreeCourseDetail from '@/views/FreeCourseDetail.vue'
import FreeExerciseChapter from '@/views/FreeExerciseChapter.vue'
import { getFreeResources } from '@/api/free-content'
import { buildExerciseChapterSlug, formatPaysSlug, formatMatiereSlug, formatNiveauGroupSlug, DEFAULT_PAYS_SLUG, DEFAULT_MATIERE_SLUG } from '@/utils/freeExerciseSlug'
import { setPageSeo } from '@/services/seo'
import {
  buildDynamicSeo,
  DYNAMIC_SEO_PAGE_TYPES,
  topicFromSlug
} from '@/composables/useDynamicSeo'

const route = useRoute()
const router = useRouter()

const slug = computed(() => String(route.params.slug || ''))
const pays = computed(() => String(route.params.pays || ''))
const niveauGroup = computed(() => String(route.params.niveauGroup || ''))
const matiere = computed(() => String(route.params.matiere || ''))
const slugIdParam = computed(() => String(route.params.id || ''))
const isExerciseDetail = computed(() => slug.value.startsWith('exercice-gratuit-'))

const normalizePathname = (pathname) => {
  const raw = String(pathname || '').trim()
  if (!raw) return '/'
  const withSlash = raw.startsWith('/') ? raw : `/${raw}`
  if (withSlash.length === 1) return withSlash
  return withSlash.replace(/\/+$/, '')
}

const routePathMatches = (currentPath, canonicalPath) => {
  return normalizePathname(currentPath) === normalizePathname(canonicalPath)
}

const buildCanonicalPathFromRoute = (routeName, params) => {
  try {
    const resolved = router.resolve({ name: routeName, params })
    return normalizePathname(resolved?.path || '')
  } catch (_) {
    return ''
  }
}

const applyNonCanonicalSeo = ({ canonicalPath, pageType, topic, level, sourceText }) => {
  const normalizedCanonicalPath = normalizePathname(canonicalPath)
  const currentPath = normalizePathname(route.path)
  if (!normalizedCanonicalPath || !currentPath) return
  const seoPayload = buildDynamicSeo({
    pageType: pageType || DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER,
    topic: topic || topicFromSlug(slug.value),
    level,
    sourceText
  })
  setPageSeo({
    title: seoPayload.title,
    description: seoPayload.description,
    canonicalPath: currentPath,
    canonicalUrl: normalizedCanonicalPath,
    robots: 'noindex,follow',
    ogType: seoPayload.ogType
  })
}

const parseSlugWithId = (value) => {
  const match = String(value || '').match(/^(.*?)-(\d+)$/)
  if (!match) return { slug: String(value || ''), id: '' }
  return { slug: match[1], id: match[2] }
}

const normalizeLegacySlug = (value) => {
  return String(value || '')
    .replace(/^terminale-bac-/, 'terminal-bac-')
    .replace(/^premiere-bac-/, 'premiere-1er-')
}

const resolving = ref(false)
const resolveError = ref('')
const resolvedNotionId = ref(null)
const resolvedTitle = ref('')

const resolveNotionBySlug = async () => {
  if (isExerciseDetail.value) {
    resolvedNotionId.value = null
    resolvedTitle.value = ''
    resolveError.value = ''
    resolving.value = false
    return
  }
  const parsed = parseSlugWithId(slug.value)
  const rawSlug = parsed.slug
  const targetSlug = normalizeLegacySlug(parsed.slug)
  const targetPays = formatPaysSlug(pays.value)
  const targetMatiere = formatMatiereSlug(matiere.value)
  const targetId = slugIdParam.value || parsed.id
  if (!targetSlug) {
    resolveError.value = "Chapitre introuvable."
    resolvedNotionId.value = null
    return
  }

  resolving.value = true
  resolveError.value = ''
  resolvedNotionId.value = null
  resolvedTitle.value = ''

  try {
    if (targetId) {
      const data = await getFreeResources({ type: 'exercise', notion: targetId, page_size: 1 })
      const list = Array.isArray(data?.results) ? data.results : data
      const first = list && list.length ? list[0] : null
      if (first) {
        const canonicalPays = formatPaysSlug(first?.pays_nom || '') || DEFAULT_PAYS_SLUG
        const canonicalGroup = formatNiveauGroupSlug(first?.niveau_nom || '')
        const canonicalMatiere = formatMatiereSlug(first?.matiere_nom || first?.matiere || '') || DEFAULT_MATIERE_SLUG
        const canonicalSlug = buildExerciseChapterSlug({
          niveauNom: first?.niveau_nom,
          name: first?.notion_nom || first?.name || first?.titre
        })
        resolvedNotionId.value = first?.notion || first?.id || targetId
        resolvedTitle.value = first?.notion_nom || first?.name || ''
        resolving.value = false

        if (canonicalSlug) {
          const currentPays = formatPaysSlug(pays.value)
          const currentGroup = formatNiveauGroupSlug(niveauGroup.value)
          const currentMatiere = formatMatiereSlug(matiere.value)
          const routeName = canonicalGroup ? 'FreeExerciseChapterSlugGrouped' : 'FreeExerciseChapterSlug'
          const params = canonicalGroup
            ? { pays: canonicalPays, niveauGroup: canonicalGroup, matiere: canonicalMatiere, slug: canonicalSlug, id: targetId }
            : { pays: canonicalPays, matiere: canonicalMatiere, slug: canonicalSlug, id: targetId }
          if (
            canonicalPays !== currentPays ||
            canonicalGroup !== currentGroup ||
            canonicalMatiere !== currentMatiere ||
            canonicalSlug !== rawSlug ||
            String(targetId) !== String(slugIdParam.value || parsed.id)
          ) {
            const canonicalPath = buildCanonicalPathFromRoute(routeName, params)
            applyNonCanonicalSeo({
              canonicalPath,
              pageType: DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER,
              topic: resolvedTitle.value || first?.notion_nom || topicFromSlug(canonicalSlug),
              level: first?.niveau_nom || canonicalGroup,
              sourceText: first?.accroche || first?.question || first?.contenu || first?.excerpt || ''
            })
            router.replace({
              name: routeName,
              params,
              query: route.query,
              hash: route.hash
            }).catch(() => {})
          }
        }
        return
      }
    }

    const pageSize = 200
    let page = 1
    let totalPages = 1

    while (page <= totalPages) {
      const data = await getFreeResources({
        type: 'exercise',
        group_by: 'notion',
        page,
        page_size: pageSize
      })
      const list = Array.isArray(data?.results) ? data.results : data
      const count = Number(data?.count || 0)
      totalPages = count > 0 ? Math.max(1, Math.ceil(count / pageSize)) : 1

      const match = (list || []).find((item) => {
        const itemSlug = buildExerciseChapterSlug({
          niveauNom: item?.niveau_nom,
          name: item?.notion_nom || item?.name || item?.titre
        })
        if (itemSlug !== targetSlug) return false
        if (!targetPays) return true
        const itemPays = formatPaysSlug(item?.pays_nom || '')
        if (itemPays && itemPays !== targetPays) return false
        if (targetMatiere) {
          const itemMatiere = formatMatiereSlug(item?.matiere_nom || item?.matiere || '')
          if (itemMatiere && itemMatiere !== targetMatiere) return false
        }
        return true
      })

      if (match) {
        const canonicalPays = formatPaysSlug(match?.pays_nom || '') || DEFAULT_PAYS_SLUG
        const canonicalGroup = formatNiveauGroupSlug(match?.niveau_nom || '')
        const canonicalMatiere = formatMatiereSlug(match?.matiere_nom || match?.matiere || '') || DEFAULT_MATIERE_SLUG
        const canonicalSlug = buildExerciseChapterSlug({
          niveauNom: match?.niveau_nom,
          name: match?.notion_nom || match?.name || match?.titre
        })
        const resolvedId = match?.notion || match?.id || ''
        resolvedNotionId.value = resolvedId || null
        resolvedTitle.value = match?.notion_nom || match?.name || ''
        resolving.value = false

        if (canonicalSlug && resolvedId) {
          const currentPays = formatPaysSlug(pays.value)
          const currentGroup = formatNiveauGroupSlug(niveauGroup.value)
          const currentMatiere = formatMatiereSlug(matiere.value)
          const routeName = canonicalGroup ? 'FreeExerciseChapterSlugGrouped' : 'FreeExerciseChapterSlug'
          const params = canonicalGroup
            ? { pays: canonicalPays, niveauGroup: canonicalGroup, matiere: canonicalMatiere, slug: canonicalSlug, id: resolvedId }
            : { pays: canonicalPays, matiere: canonicalMatiere, slug: canonicalSlug, id: resolvedId }
          if (
            canonicalPays !== currentPays ||
            canonicalGroup !== currentGroup ||
            canonicalMatiere !== currentMatiere ||
            canonicalSlug !== rawSlug ||
            String(resolvedId) !== String(targetId)
          ) {
            const canonicalPath = buildCanonicalPathFromRoute(routeName, params)
            applyNonCanonicalSeo({
              canonicalPath,
              pageType: DYNAMIC_SEO_PAGE_TYPES.EXERCISE_CHAPTER,
              topic: resolvedTitle.value || match?.notion_nom || topicFromSlug(canonicalSlug),
              level: match?.niveau_nom || canonicalGroup,
              sourceText: match?.accroche || match?.question || match?.contenu || match?.excerpt || ''
            })
            router.replace({
              name: routeName,
              params,
              query: route.query,
              hash: route.hash
            }).catch(() => {})
          }
        }
        return
      }

      page += 1
    }

    resolveError.value = "Chapitre introuvable."
  } catch (err) {
    resolveError.value = err?.message || "Impossible de charger ce chapitre."
  } finally {
    resolving.value = false
  }
}

const goBack = () => {
  router.push({ name: 'FreeExercises' }).catch(() => {})
}

watch([slug, pays, niveauGroup, matiere, slugIdParam], () => {
  resolveNotionBySlug()
}, { immediate: true })

watch([isExerciseDetail, slug, () => route.path], ([detailMode, currentSlug]) => {
  if (!detailMode) return
  const safeSlug = String(currentSlug || '').trim()
  if (!safeSlug) return

  const canonicalPath = normalizePathname(`/ressources-gratuites/exercices/${safeSlug}`)
  if (routePathMatches(route.path, canonicalPath)) return

  applyNonCanonicalSeo({
    canonicalPath,
    pageType: DYNAMIC_SEO_PAGE_TYPES.EXERCISE_DETAIL,
    topic: topicFromSlug(safeSlug),
    level: niveauGroup.value,
    sourceText: safeSlug
  })

  router.replace({
    name: 'FreeExerciseDetail',
    params: { slug: safeSlug },
    query: route.query,
    hash: route.hash
  }).catch(() => {})
}, { immediate: true })
</script>

<template>
  <FreeCourseDetail v-if="isExerciseDetail" resourceType="exercise" />
  <div v-else-if="resolving" class="state-card">
    <div class="state-card__spinner" aria-hidden="true"></div>
    <p>Chargement du chapitre...</p>
  </div>
  <div v-else-if="resolveError" class="state-card">
    <p>{{ resolveError }}</p>
    <button @click="goBack">Retour aux exercices gratuits</button>
  </div>
  <FreeExerciseChapter
    v-else-if="resolvedNotionId"
    :notion-id-override="resolvedNotionId"
    :notion-title-override="resolvedTitle"
  />
  <div v-else class="state-card">
    <p>Chapitre introuvable.</p>
    <button @click="goBack">Retour aux exercices gratuits</button>
  </div>
</template>

<style scoped>
.state-card {
  max-width: 720px;
  margin: 140px auto;
  padding: 24px;
  border-radius: 18px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  background: #fff;
  text-align: center;
  color: #1f2937;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.state-card__spinner {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  border: 3px solid rgba(59, 130, 246, 0.25);
  border-top-color: #3b82f6;
  animation: spin 0.9s linear infinite;
}

.state-card button {
  border: none;
  background: #2563eb;
  color: #fff;
  padding: 10px 16px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
