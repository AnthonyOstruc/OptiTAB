/**
 * FICHIER DE COMPATIBILITÉ
 * 
 * Ce fichier maintient la compatibilité avec l'ancien import :
 * import { useSubjectsStore } from '@/stores/subjects'
 * 
 * Il redirige simplement vers la nouvelle structure modulaire.
 * 
 * ⚠️  ATTENTION : Ce fichier sera supprimé dans une future version.
 *    Utilisez plutôt : import { useSubjectsStore } from '@/stores/subjects/index'
 */

// Redirection vers la nouvelle structure modulaire
export { useSubjectsStore } from './subjects/index'

// Message de dépréciation en mode développement
if (process.env.NODE_ENV === 'development') {
  console.warn(`
🚨 DEPRECATION WARNING 🚨

L'import depuis '@/stores/subjects' est déprécié.
Utilisez plutôt : import { useSubjectsStore } from '@/stores/subjects/index'

Cette redirection sera supprimée dans une future version.
  `)
} 