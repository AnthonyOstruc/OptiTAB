<template>
  <DashboardLayout>
    <div class="progress-page">
      <h2 class="progress-title">Suivi de mes exercices</h2>

      <!-- Tabs statut -->
      <Tabs :items="statusOptions" v-model="statusFilter" />

      <!-- Filtres -->
      <div class="filters">
        <div class="filter-group">
          <span class="filter-label">Difficulté :</span>
          <button v-for="d in diffOptions" :key="d" :class="['filter-btn', {active: d===diffFilter}]" @click="diffFilter=d">
            {{ diffLabel[d] }}
          </button>
        </div>
      </div>

      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Titre</th>
            <th>Chapitre</th>
            <th>Difficulté</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in filteredList" :key="e.id">
            <td>{{ e.id }}</td>
            <td>{{ e.titre }}</td>
            <td>{{ chapitreName(e.chapitre) }}</td>
            <td>{{ diffLabel[e.difficulty] }}</td>
            <td>{{ statusEmoji(statusMap[e.id]) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import Tabs from '@/components/common/Tabs.vue'
import { getExercices, getChapitres, getStatuses } from '@/api'

const exercices = ref([])
const chapitres = ref([])
const statusMap = ref({})

const diffOptions = ['all','easy','medium','hard']
const diffLabel = { all:'Toutes', easy:'★', medium:'★★', hard:'★★★' }
const statusOptions = [ {key:'all', label:'Exercices restants'}, {key:'acquired', label:'✅'}, {key:'not_acquired', label:'❌'} ]

const diffFilter = ref('all')
const statusFilter = ref('all')

onMounted(async () => {
  const [{ data: ex }, { data: ch }, { data: st }] = await Promise.all([
    getExercices(''),
    getChapitres(''),
    getStatuses()
  ])
  exercices.value = ex
  chapitres.value = ch
  statusMap.value = Object.fromEntries(st.map(s=>[s.exercice, s.status]))
})

function chapitreName(id){
  const c = chapitres.value.find(c=>c.id===id)
  return c ? c.nom : id
}
function statusEmoji(s){
  if(s==='acquired') return '✅'
  if(s==='not_acquired') return '❌'
  return '—'
}

const filteredList = computed(()=>{
  let list = exercices.value
  if(diffFilter.value!=='all') list = list.filter(e=>e.difficulty===diffFilter.value)

  if(statusFilter.value==='all') {
    // Restants : pas encore de statut enregistré
    list = list.filter(e => !statusMap.value[e.id])
  } else {
    list = list.filter(e => statusMap.value[e.id]===statusFilter.value)
  }
  return list
})
</script>

<style scoped>
.progress-page{padding:2rem;}
.progress-title{font-size:1.6rem;font-weight:800;color:#193e8e;margin-bottom:1.5rem;}
.filters{display:flex;gap:1.5rem;margin-bottom:1rem;flex-wrap:wrap;}
.filter-group{display:flex;align-items:center;gap:0.6rem;}
.filter-label{font-weight:600;}
.filter-btn{background:#e5e7eb;border:none;border-radius:6px;padding:6px 12px;cursor:pointer;font-weight:600;}
.filter-btn.active{background:#6366f1;color:#fff;}
.filter-btn:hover:not(.active){background:#cbd5e1;}
.admin-table{width:100%;border-collapse:collapse;}
.admin-table th,.admin-table td{border:1px solid #e5e7eb;padding:6px 8px;text-align:left;}
.admin-table th{background:#f3f4f6;}
</style> 