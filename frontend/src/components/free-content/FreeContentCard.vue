<template>
  <article class="free-card">
    <div class="card-top">
      <span v-if="resource.badge" class="badge">
        {{ resource.badge }}
      </span>
      <span v-if="resource.type_label" class="type-pill">{{ resource.type_label }}</span>
    </div>

    <h3>{{ resource.titre }}</h3>
    <p class="excerpt">{{ resource.excerpt || resource.accroche }}</p>

    <ul class="tags">
      <li v-if="resource.matiere_nom">
        <AcademicCapIcon />
        {{ resource.matiere_nom }}
      </li>
      <li v-if="resource.niveau_nom">
        <BuildingLibraryIcon />
        {{ resource.niveau_nom }}
      </li>
      <li v-if="resource.lecture_duree">
        <ClockIcon />
        {{ resource.lecture_duree }}
      </li>
    </ul>

    <div class="cta-row">
      <button class="cta-primary" @click="$emit('open-subscription')">
        Débloquer tout OptiTAB
      </button>
      <a href="/#tarifs" class="cta-secondary">
        Voir les tarifs
      </a>
    </div>
  </article>
</template>

<script setup>
import { AcademicCapIcon, BuildingLibraryIcon, ClockIcon } from '@heroicons/vue/24/outline'

defineProps({
  resource: {
    type: Object,
    required: true
  }
})

defineEmits(['open-subscription'])
</script>

<style scoped lang="scss">
.free-card {
  border-radius: 24px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  padding: 28px;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 280px;
  box-shadow: 0 16px 35px rgba(15, 23, 42, 0.06);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.badge {
  background: #0f172a;
  color: #fff;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}

.type-pill {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  background: #e0f2fe;
  color: #0369a1;
  font-weight: 600;
  text-transform: uppercase;
}

h3 {
  margin: 0;
  font-size: 20px;
  line-height: 1.3;
  color: #0f172a;
}

.excerpt {
  margin: 0;
  color: #475569;
  font-size: 15px;
  line-height: 1.5;
}

.tags {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 0;
  margin: 12px 0;
}

.tags li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f1f5f9;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 13px;
  color: #0f172a;
}

.tags svg {
  width: 16px;
  height: 16px;
}

.cta-row {
  margin-top: auto;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.cta-primary {
  flex: 1;
  min-width: 180px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(120deg, #2563eb, #7c3aed);
  color: #fff;
  font-weight: 600;
  padding: 12px 18px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.cta-primary:hover {
  transform: translateY(-1px);
}

.cta-secondary {
  flex: 1;
  min-width: 160px;
  border-radius: 12px;
  border: 1px solid #cbd5f5;
  color: #2563eb;
  text-align: center;
  text-decoration: none;
  padding: 12px 18px;
  font-weight: 600;
}

@media (max-width: 600px) {
  .cta-row {
    flex-direction: column;
  }
}
</style>
