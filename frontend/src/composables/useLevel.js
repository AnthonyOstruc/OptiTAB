/**
 * Composable pour les calculs de niveau et XP
 * Utilise la même logique que le backend
 */

/**
 * Calcule le niveau, les XP requis pour le niveau suivant et les XP manquants
 * Progression exponentielle : niveau N nécessite N * N * 10 XP
 * 
 * @param {number} totalXp - Total des XP de l'utilisateur
 * @returns {Object} - { level, next_level_xp, xp_to_next }
 */
export function calculateUserLevel(totalXp) {
  if (totalXp <= 0) {
    return { level: 0, next_level_xp: 10, xp_to_next: 10 }
  }
  
  let level = 0
  while (true) {
    const xpForNextLevel = (level + 1) * (level + 1) * 10
    if (totalXp < xpForNextLevel) {
      break
    }
    level += 1
  }
  
  const nextLevelXp = (level + 1) * (level + 1) * 10
  const xpToNext = nextLevelXp - totalXp
  
  return { level, next_level_xp: nextLevelXp, xp_to_next: xpToNext }
}

/**
 * Composable pour la gestion des niveaux
 */
export function useLevel() {
  return {
    calculateUserLevel
  }
}
