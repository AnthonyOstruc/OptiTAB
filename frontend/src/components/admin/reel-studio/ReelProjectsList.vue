<template>
  <section class="reel-projects-list">
    <div class="list-header">
      <h3>Reels existants</h3>
      <span class="count">{{ projects.length }}</span>
    </div>

    <p v-if="loading" class="state-text">Chargement des projets...</p>
    <p v-else-if="!projects.length" class="state-text">Aucun reel pour le moment.</p>

    <ul v-else>
      <li
        v-for="project in projects"
        :key="project.id"
        class="project-item"
        :class="{ active: Number(selectedProjectId) === Number(project.id) }"
      >
        <button class="project-main" type="button" @click="$emit('select', project.id)">
          <strong>{{ project.title }}</strong>
          <span>{{ project.level || 'Niveau non défini' }} · {{ project.format_type || 'Format non défini' }}</span>
          <span>{{ project.slide_count || 0 }} slides · {{ project.target_duration_seconds || 0 }}s</span>
        </button>
        <button
          class="project-delete"
          type="button"
          title="Supprimer"
          @click="$emit('delete', project.id)"
        >
          Suppr.
        </button>
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  projects: {
    type: Array,
    default: () => [],
  },
  selectedProjectId: {
    type: [Number, String, null],
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['select', 'delete'])
</script>

<style scoped>
.reel-projects-list {
  border: 1px solid #dbe4ee;
  border-radius: 12px;
  background: #ffffff;
  padding: 16px;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.list-header h3 {
  margin: 0;
  font-size: 18px;
  color: #0f172a;
}

.count {
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 700;
}

.state-text {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.project-item {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  background: #f8fafc;
}

.project-item.active {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.project-main {
  border: 0;
  background: transparent;
  text-align: left;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
}

.project-main strong {
  color: #0f172a;
  font-size: 14px;
}

.project-main span {
  color: #475569;
  font-size: 12px;
}

.project-delete {
  border: 0;
  border-left: 1px solid #e2e8f0;
  background: #fee2e2;
  color: #b91c1c;
  padding: 10px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
</style>
