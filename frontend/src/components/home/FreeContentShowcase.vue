<template>
  <section class="free-showcase">
    <div class="showcase-container">
      <div class="showcase-header">
        <span class="eyebrow">
          <SparklesIcon class="eyebrow-icon" />
          Aperçus gratuits
        </span>
        <h2 class="main-title">Découvrez la méthode <span class="highlight-brand">OptiTAB</span></h2>
        <p class="subtitle">
          Testez gratuitement nos cours structurés et exercices corrigés pour comprendre pourquoi les élèves progressent avec nous.
        </p>
      </div>

      <div class="cards-grid">
        <article
          v-for="item in items"
          :key="item.type"
          class="preview-card"
          @click="goTo(item)"
        >
          <div class="card-header">
            <div class="badge" :class="`badge-${item.type}`">
              {{ item.badge }}
            </div>
            <div class="card-icon">
              <component :is="getIcon(item.type)" />
            </div>
          </div>
          
          <h3 class="card-title">{{ item.title }}</h3>
          <p class="card-highlight">{{ item.highlight }}</p>
          <p class="card-description">{{ item.description }}</p>
          
          <ul class="features-list">
            <li v-for="bullet in item.bullets" :key="bullet">
              <CheckCircleIcon class="check-icon" />
              {{ bullet }}
            </li>
          </ul>
          
          <button class="explore-btn">
            <span>Explorer gratuitement</span>
            <ArrowRightIcon class="arrow-icon" />
          </button>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { 
  SparklesIcon, 
  CheckCircleIcon, 
  ArrowRightIcon,
  BookOpenIcon,
  AcademicCapIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const router = useRouter()

const goTo = (item) => {
  if (!item?.to) return
  router.push(item.to)
}

const getIcon = (type) => {
  const icons = {
    course: BookOpenIcon,
    exercise: AcademicCapIcon,
    summary: DocumentTextIcon
  }
  return icons[type] || BookOpenIcon
}
</script>

<style scoped>
.free-showcase {
  padding: 100px 20px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.showcase-container {
  max-width: 1200px;
  margin: 0 auto;
}

.showcase-header {
  text-align: center;
  margin-bottom: 64px;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #fef3c7;
  border: 1px solid #fbbf24;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  color: #92400e;
  margin-bottom: 20px;
}

.eyebrow-icon {
  width: 18px;
  height: 18px;
  color: #f59e0b;
}

.main-title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.main-title .highlight-brand {
  color: #2563eb;
}

.subtitle {
  font-size: 18px;
  color: #64748b;
  margin: 0;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
}

.preview-card {
  background: #ffffff;
  border: 2px solid #e2e8f0;
  border-radius: 24px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  overflow: hidden;
}

.preview-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.preview-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 48px rgba(59, 130, 246, 0.15);
  border-color: #93c5fd;
}

.preview-card:hover::before {
  transform: scaleX(1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-course {
  background: #dbeafe;
  color: #1e40af;
}

.badge-exercise {
  background: #d1fae5;
  color: #065f46;
}

.badge-summary {
  background: #fce7f3;
  color: #9f1239;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
}

.card-icon svg {
  width: 24px;
  height: 24px;
}

.card-title {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  line-height: 1.3;
}

.card-highlight {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6366f1;
  margin: 0;
}

.card-description {
  font-size: 16px;
  color: #475569;
  margin: 0;
  line-height: 1.6;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 8px 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.features-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #334155;
  line-height: 1.4;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #22c55e;
  flex-shrink: 0;
}

.explore-btn {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  background: #0f172a;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.explore-btn:hover {
  background: #1e293b;
  transform: translateX(4px);
}

.arrow-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.2s ease;
}

.explore-btn:hover .arrow-icon {
  transform: translateX(4px);
}

@media (max-width: 768px) {
  .free-showcase {
    padding: 60px 16px;
  }

  .showcase-header {
    margin-bottom: 48px;
  }

  .main-title {
    font-size: 32px;
  }

  .subtitle {
    font-size: 16px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .preview-card {
    padding: 24px;
  }

  .card-title {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .card-icon {
    width: 40px;
    height: 40px;
  }

  .card-icon svg {
    width: 20px;
    height: 20px;
  }
}
</style>
