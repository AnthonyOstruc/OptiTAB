<template>
  <EspaceLayout :title="estParent ? 'Espace parent' : 'Accueil'" :parent="estParent">
    <AccueilParent v-if="estParent" :exemple="exemple" />
    <AccueilEleve v-else :exemple="exemple" />
  </EspaceLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import EspaceLayout from '@/components/espace/EspaceLayout.vue'
import AccueilEleve from '@/components/espace/AccueilEleve.vue'
import AccueilParent from '@/components/espace/AccueilParent.vue'
import { useUserStore } from '@/stores/user'
import { peutVoirExemple } from '@/config/espace'

const route = useRoute()
const userStore = useUserStore()

// Démonstrations (compte démo et administrateurs uniquement) :
// ?exemple=1 remplit l'écran avec des données d'exemple,
// ?vue=parent montre l'espace parent avec un enfant d'exemple.
const demo = computed(() => peutVoirExemple(userStore))
const vueParentDemo = computed(() => demo.value && route.query.vue === 'parent')
const exemple = computed(() => demo.value && (route.query.exemple === '1' || vueParentDemo.value))
const estParent = computed(() => userStore.role === 'parent' || vueParentDemo.value)
</script>
