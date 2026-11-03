import { ref, watch } from 'vue'

// Taille de lecture des cours et fiches, choisie par l'élève et retenue sur
// cet appareil (préférence de confort, pas une donnée importante).
const CLE = 'optitab_taille_texte'
export const TAILLES = [0.9, 1, 1.1, 1.2, 1.3]

function lire() {
  try {
    const v = Number(localStorage.getItem(CLE))
    return TAILLES.includes(v) ? v : 1
  } catch {
    return 1
  }
}

const taille = ref(lire())

watch(taille, (v) => {
  try {
    localStorage.setItem(CLE, String(v))
  } catch {
    // Stockage indisponible (navigation privée) : on garde la valeur en mémoire.
  }
})

export function useTailleTexte() {
  return taille
}
