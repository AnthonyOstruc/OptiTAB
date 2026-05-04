<template>
  <section class="reel-projects-list">
    <div class="list-header">
      <h3>Reels en base</h3>
    </div>

    <p v-if="loading" class="state-text">Chargement des reels...</p>
    <p v-else-if="!projects.length" class="state-text">Aucun reel enregistre.</p>

    <div v-else class="table-scroll">
      <table class="projects-table">
        <thead>
          <tr>
            <th>Titre</th>
            <th>Slides creees</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="project in projects"
            :key="project.id"
            :class="{ active: Number(selectedProjectId) === Number(project.id) }"
          >
            <td>
              <button class="title-button" type="button" @click="$emit('select', project.id)">
                {{ projectTitle(project) }}
              </button>
            </td>
            <td>
              <span class="slides-count">{{ projectSlideCount(project) }}</span>
            </td>
            <td>
              <div class="row-actions">
                <button class="btn-action btn-action--open" type="button" @click="$emit('select', project.id)">
                  Ouvrir
                </button>
                <button class="btn-action btn-action--edit" type="button" @click="$emit('edit', project)">
                  Modifier
                </button>
                <button class="btn-action btn-action--delete" type="button" @click="$emit('delete', project)">
                  Supprimer
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
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

defineEmits(['select', 'edit', 'delete'])

function projectTitle(project) {
  return String(project?.title || '').trim() || 'Reel sans titre'
}

function projectSlideCount(project) {
  if (Array.isArray(project?.slides)) return project.slides.length
  return Number(project?.slide_count || 0)
}
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

.state-text {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.table-scroll {
  overflow-x: auto;
}

.projects-table {
  width: 100%;
  min-width: 520px;
  border-collapse: collapse;
}

.projects-table th,
.projects-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 12px;
  text-align: left;
  color: #334155;
  font-size: 13px;
  vertical-align: middle;
}

.projects-table th {
  background: #f8fafc;
  color: #475569;
  font-weight: 800;
}

.projects-table tr.active td {
  background: #eff6ff;
}

.projects-table tr:last-child td {
  border-bottom: 0;
}

.title-button {
  border: 0;
  padding: 0;
  background: transparent;
  color: #0f172a;
  font: inherit;
  font-weight: 800;
  text-align: left;
  cursor: pointer;
}

.title-button:hover {
  color: #1d4ed8;
}

.slides-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  min-height: 26px;
  border-radius: 999px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 13px;
  font-weight: 800;
}

.row-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.btn-action {
  border: 0;
  border-radius: 8px;
  padding: 8px 10px;
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}

.btn-action--open {
  background: #2563eb;
}

.btn-action--edit {
  background: #64748b;
}

.btn-action--delete {
  background: #ef4444;
}
</style>
