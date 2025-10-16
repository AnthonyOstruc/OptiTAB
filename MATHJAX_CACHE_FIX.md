# Correction du problème de cache du rendu MathJax

## Problème identifié
Le rendu scientifique (MathJax) se désactivait après un moment à cause du cache. Lorsque l'utilisateur naviguait entre différentes pages (cours, exercices, quiz, synthèse) qui sont mises en cache avec KeepAlive, le rendu mathématique n'était pas réinitialisé correctement.

## Solution mise en œuvre

### 1. Amélioration de la fonction `renderMath()` (scientificRenderer.js)
- Ajout d'un système de nettoyage du cache MathJax avec `typesetClear()`
- Implémentation de multiples tentatives de rendu pour garantir la disponibilité de MathJax
- Ajout de gestion d'erreurs robuste avec des logs pour le débogage

### 2. Ajout du hook `onActivated` dans toutes les vues concernées

Le hook `onActivated` est appelé chaque fois qu'un composant mis en cache avec KeepAlive est réactivé. Il force le rendu MathJax à chaque fois que l'utilisateur revient sur une page.

### 3. Ajout de watchers et de déclencheurs supplémentaires

Pour la page des exercices (`ChapterExercises.vue`), ajout de :
- **Watcher sur `paginated`** : Force le rendu MathJax quand les exercices affichés changent (pagination, filtres)
- **Rendu après `handlePageChange`** : Force le rendu quand l'utilisateur change de page
- **Rendu après `loadData`** : Force le rendu après le chargement initial des données

Pour le composant `ExerciceQCM.vue` :
- **Watcher sur `showSolution`** : Force le rendu quand l'utilisateur affiche/cache la solution
- **Amélioration de `toggleSolution`** : Double appel au rendu pour garantir l'affichage

#### Pages utilisateurs
- ✅ `Cours.vue` - Pages de cours avec contenu LaTeX
- ✅ `ChapterQuiz.vue` - Pages de quiz avec formules mathématiques
- ✅ `ChapterExercises.vue` - Pages d'exercices avec énoncés scientifiques
- ✅ `SheetByNotion.vue` - Fiches de synthèse avec formules
- ✅ `Sheets.vue` - Liste des fiches de synthèse avec modal

#### Pages d'administration
- ✅ `AdminCoursPlus.vue` - Interface d'ajout de cours avec aperçu
- ✅ `AdminQuizPlus.vue` - Interface d'ajout de quiz avec aperçu
- ✅ `AdminSheets.vue` - Interface de gestion des fiches avec aperçu

#### Composants
- ✅ `ExerciceQCM.vue` - Ajout du hook `onUpdated` pour forcer le rendu à chaque mise à jour

### 3. Modifications détaillées

#### scientificRenderer.js
```javascript
export function renderMath() {
  // Fonction pour forcer le rendu MathJax
  const forceRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        // Vider le cache de MathJax pour forcer un nouveau rendu
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        // Forcer le rendu complet
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur lors du rendu:', error)
      }
    }
  }
  
  // Première tentative immédiate
  forceRender()
  
  // Deuxième tentative après un court délai
  setTimeout(forceRender, 50)
  
  // Tentatives supplémentaires avec retry
  let retryCount = 0
  const maxRetries = 8
  const tryRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      forceRender()
    } else if (retryCount < maxRetries) {
      retryCount++
      setTimeout(tryRender, 150)
    }
  }
  setTimeout(tryRender, 100)
}
```

#### Pattern utilisé dans toutes les vues
```javascript
import { onActivated } from 'vue'

// Hook onActivated - appelé quand le composant est réactivé depuis le cache KeepAlive
onActivated(() => {
  // Forcer le rendu MathJax à chaque réactivation
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        // Vider le cache de MathJax
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
    // Second appel après un délai pour s'assurer du rendu
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
    }, 100)
  })
})
```

## Résultat attendu

Maintenant, chaque fois qu'un utilisateur :
1. Ouvre un cours
2. Passe à la page d'exercices
3. Navigue vers un quiz
4. Consulte une fiche de synthèse
5. Revient à une page précédente

Le rendu mathématique sera **automatiquement réinitialisé et mis à jour**, même si la page est mise en cache. Les formules LaTeX s'afficheront correctement à chaque fois, sans nécessiter de rafraîchissement de la page.

## Tests recommandés

1. Ouvrir un cours avec des formules mathématiques
2. Naviguer vers une autre section (ex: exercices)
3. Revenir au cours
4. Vérifier que les formules sont toujours bien affichées
5. Répéter l'opération plusieurs fois
6. Tester sur différents navigateurs (Chrome, Firefox, Safari)
7. Tester sur mobile

## Fichiers modifiés

- `frontend/src/utils/scientificRenderer.js`
- `frontend/src/views/Cours.vue`
- `frontend/src/views/ChapterQuiz.vue`
- `frontend/src/views/ChapterExercises.vue`
- `frontend/src/views/SheetByNotion.vue`
- `frontend/src/views/Sheets.vue`
- `frontend/src/views/admin/AdminCoursPlus.vue`
- `frontend/src/views/admin/AdminQuizPlus.vue`
- `frontend/src/views/admin/AdminSheets.vue`
- `frontend/src/components/UI/ExerciceQCM.vue`

## Corrections supplémentaires pour la page Exercices

La page des exercices nécessitait des déclencheurs supplémentaires car :
1. Les exercices sont paginés (changement de page)
2. Ils peuvent être filtrés (difficulté, statut, recherche)
3. La solution peut être affichée/cachée dynamiquement

Ajouts effectués :

```javascript
// Dans ChapterExercises.vue

// 1. Watcher sur les exercices affichés
watch(paginated, () => {
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  })
}, { deep: true })

// 2. Rendu après changement de page
function handlePageChange(page) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
  saveViewState()
  // Forcer le rendu MathJax
  nextTick(() => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        window.MathJax.typesetPromise()
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  })
}

// 3. Rendu après chargement des données
async function loadData() {
  // ... chargement des données ...
  finally {
    loading.value = false
    await nextTick()
    
    // Forcer le rendu MathJax après le chargement
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        try {
          if (window.MathJax.typesetClear) {
            window.MathJax.typesetClear()
          }
          window.MathJax.typesetPromise()
        } catch (error) {
          console.warn('[MathJax] Erreur:', error)
        }
      }
    }, 100)
  }
}
```

```javascript
// Dans ExerciceQCM.vue

// Watcher sur l'affichage de la solution
watch(showSolution, (newVal) => {
  if (newVal) {
    nextTick(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        try {
          if (window.MathJax.typesetClear) {
            window.MathJax.typesetClear()
          }
          window.MathJax.typesetPromise()
        } catch (error) {
          // Ignorer les erreurs silencieusement
        }
      }
    })
  }
})

// Amélioration de toggleSolution
function toggleSolution() {
  showSolution.value = !showSolution.value
  if (showSolution.value) {
    nextTick(() => {
      renderMath()
      setTimeout(() => {
        renderMath()
      }, 100)
    })
  }
}
```

## Date de modification
16 octobre 2025 (Mise à jour avec correctifs supplémentaires pour la page Exercices)

