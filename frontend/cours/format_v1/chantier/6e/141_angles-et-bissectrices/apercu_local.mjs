// Page d'aperçu autonome d'une notion du chantier (format OptiTAB v1).
//
// Usage :
//   node apercu_notion.mjs <dossier_notion> [sortie.html] [--artifact]
//
// Lit <dossier>/cours_<id>.txt, fiche_<id>.txt, exercices.txt (versions
// finales), source_en_ligne/meta.json (titres, images en ligne) et
// figures/correspondance.json (nouvelles figures, prioritaires).
// Les images en ligne sont téléchargées une fois dans images_en_ligne/.
// La page embarque le vrai moteur (src/utils/optitabDoc.js), tuneMathOverflow
// et les vraies feuilles de style du site. Sortie par défaut : <dossier>/apercu.html
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = "C:\\Users\\SWEELCO-AT\\Desktop\\SWINDER\\OptiTABV2\\frontend\\cours\\format_v1\\outils"
const front = path.resolve(here, '../../..')
const args = process.argv.slice(2)
const ARTIFACT = args.includes('--artifact')
// --retour <lien> : lien « ← Tous les chapitres » en tête de page (aperçu d'un niveau)
const kRetour = args.indexOf('--retour')
const RETOUR = kRetour >= 0 ? args[kRetour + 1] : ''
const [dir, outArg] = args.filter((a, i) => !a.startsWith('--') && !(kRetour >= 0 && i === kRetour + 1))
if (!dir) {
  console.error('Usage : node apercu_notion.mjs <dossier_notion> [sortie.html] [--artifact]')
  process.exit(1)
}
const out = outArg || path.join(dir, 'apercu.html')
const read = (p) => fs.readFileSync(p, 'utf8')

// --- moteur et styles du site -------------------------------------------
const engine = read(path.join(front, 'src/utils/optitabDoc.js')).replace(/^export /gm, '')
const sci = read(path.join(front, 'src/utils/scientificRenderer.js'))
const tuneStart = sci.indexOf('export function tuneMathOverflow')
const tuneEnd = sci.indexOf('\n}\n', tuneStart) + 3
const tune = sci.slice(tuneStart, tuneEnd).replace(/^export /, '')
const css = read(path.join(front, 'src/styles/scientific-content.css')) + '\n' + read(path.join(front, 'src/styles/optitab-doc.css'))

// --- métadonnées et images -----------------------------------------------
const meta = {"notion": 141, "titre": "Angles et bissectrices", "theme": 62, "contexte": 43, "cours": [{"id": 149, "titre": "Angles et bissectrices", "images": [{"id": 205, "position": 1, "nom": "cours_images/cours-rapporteur_6e_a2469bfce68cb7aa8c71.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/cours-rapporteur_6e_a2469bfce68cb7aa8c71.png", "width": 1132, "height": 351, "alt": "Cours de 6e : Angles et bissectrices — rapporteur"}, {"id": 206, "position": 2, "nom": "cours_images/cours-paires-bissectrice_6e_e33591798f32d69551c0.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/cours-paires-bissectrice_6e_e33591798f32d69551c0.png", "width": 1076, "height": 327, "alt": "Cours de 6e : Angles et bissectrices — paires bissectrice"}, {"id": 207, "position": 3, "nom": "cours_images/angles_rapporteur.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_rapporteur.png", "width": null, "height": null, "alt": "Angles - Angles rapporteur"}, {"id": 208, "position": 4, "nom": "cours_images/angles_mesure.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_mesure.png", "width": null, "height": null, "alt": "Angles - Angles mesure"}, {"id": 209, "position": 5, "nom": "cours_images/angles_trace.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_trace.png", "width": null, "height": null, "alt": "Angles - Angles trace"}, {"id": 210, "position": 6, "nom": "cours_images/angles_equerre.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_equerre.png", "width": null, "height": null, "alt": "Angles - Angles equerre"}, {"id": 211, "position": 7, "nom": "cours_images/angles_exercice_differents_angles.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_exercice_differents_angles.png", "width": null, "height": null, "alt": "Angles - Angles exercice differents angles"}, {"id": 212, "position": 8, "nom": "cours_images/angles_exercice_mesure.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_exercice_mesure.png", "width": null, "height": null, "alt": "Angles - Angles exercice mesure"}, {"id": 213, "position": 9, "nom": "cours_images/angles_exercice_trace.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/angles_exercice_trace.png", "width": null, "height": null, "alt": "Angles - Angles exercice trace"}]}], "fiches": [{"id": 213, "titre": "Résumé : Angles et bissectrices", "images": [{"id": 264, "position": 1, "nom": "synthesis_images/cours-rapporteur_6e_a2469bfce68cb7aa8c71.png", "url": "https://optitab-media.s3.amazonaws.com/synthesis_images/cours-rapporteur_6e_a2469bfce68cb7aa8c71.png", "width": 1132, "height": 351, "alt": "Fiche de 6e : Angles et bissectrices"}]}], "exercices": [{"id": 3482, "titre": "Découverte - Angles et bissectrices - 1. Mesurer puis partager un angle", "images": [{"id": 2440, "position": 1, "nom": "exercice_images/angles_6e_1_1_ebe7eb7931b258b828a5.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_1_ebe7eb7931b258b828a5.png", "width": 647, "height": 392, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 1. Mesurer puis partager un angle"}, {"id": 2441, "position": 2, "nom": "exercice_images/angles_6e_1_1_corrige_6948e8bcbf91bb61288b.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_1_corrige_6948e8bcbf91bb61288b.png", "width": 647, "height": 475, "alt": "Correction annotée — Découverte - Angles et bissectrices - 1. Mesurer puis partager un angle"}]}, {"id": 3483, "titre": "Découverte - Angles et bissectrices - 2. Mesurer puis partager un angle", "images": [{"id": 2442, "position": 1, "nom": "exercice_images/angles_6e_1_2_a2744230e96255ce7fba.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_2_a2744230e96255ce7fba.png", "width": 573, "height": 418, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 2. Mesurer puis partager un angle"}, {"id": 2443, "position": 2, "nom": "exercice_images/angles_6e_1_2_corrige_95cede103e3e816ad729.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_2_corrige_95cede103e3e816ad729.png", "width": 573, "height": 489, "alt": "Correction annotée — Découverte - Angles et bissectrices - 2. Mesurer puis partager un angle"}]}, {"id": 3484, "titre": "Découverte - Angles et bissectrices - 3. Mesurer puis partager un angle", "images": [{"id": 2444, "position": 1, "nom": "exercice_images/angles_6e_1_3_4e386a835f189eca3a5a.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_3_4e386a835f189eca3a5a.png", "width": 523, "height": 435, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 3. Mesurer puis partager un angle"}, {"id": 2445, "position": 2, "nom": "exercice_images/angles_6e_1_3_corrige_2316ba7145f49587f50f.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_3_corrige_2316ba7145f49587f50f.png", "width": 523, "height": 498, "alt": "Correction annotée — Découverte - Angles et bissectrices - 3. Mesurer puis partager un angle"}]}, {"id": 3485, "titre": "Découverte - Angles et bissectrices - 4. Mesurer puis partager un angle", "images": [{"id": 2446, "position": 1, "nom": "exercice_images/angles_6e_1_4_5c9936f2882d3020c1b6.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_4_5c9936f2882d3020c1b6.png", "width": 488, "height": 446, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 4. Mesurer puis partager un angle"}, {"id": 2447, "position": 2, "nom": "exercice_images/angles_6e_1_4_corrige_1b146821a5566a6257fe.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_4_corrige_1b146821a5566a6257fe.png", "width": 488, "height": 504, "alt": "Correction annotée — Découverte - Angles et bissectrices - 4. Mesurer puis partager un angle"}]}, {"id": 3486, "titre": "Découverte - Angles et bissectrices - 5. Mesurer puis partager un angle", "images": [{"id": 2448, "position": 1, "nom": "exercice_images/angles_6e_1_5_2f601413a7940842b7be.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_5_2f601413a7940842b7be.png", "width": 466, "height": 454, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 5. Mesurer puis partager un angle"}, {"id": 2449, "position": 2, "nom": "exercice_images/angles_6e_1_5_corrige_3a5c8ef24c446041d9d1.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_5_corrige_3a5c8ef24c446041d9d1.png", "width": 466, "height": 508, "alt": "Correction annotée — Découverte - Angles et bissectrices - 5. Mesurer puis partager un angle"}]}, {"id": 3487, "titre": "Découverte - Angles et bissectrices - 6. Mesurer puis partager un angle", "images": [{"id": 2450, "position": 1, "nom": "exercice_images/angles_6e_1_6_6a06df6eaec7ba076752.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_6_6a06df6eaec7ba076752.png", "width": 453, "height": 459, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 6. Mesurer puis partager un angle"}, {"id": 2451, "position": 2, "nom": "exercice_images/angles_6e_1_6_corrige_780f1c86cee092990734.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_6_corrige_780f1c86cee092990734.png", "width": 453, "height": 511, "alt": "Correction annotée — Découverte - Angles et bissectrices - 6. Mesurer puis partager un angle"}]}, {"id": 3488, "titre": "Découverte - Angles et bissectrices - 7. Mesurer puis partager un angle", "images": [{"id": 2452, "position": 1, "nom": "exercice_images/angles_6e_1_7_098fa69ab002d4d027b6.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_7_098fa69ab002d4d027b6.png", "width": 449, "height": 459, "alt": "Schéma de travail — Découverte - Angles et bissectrices - 7. Mesurer puis partager un angle"}, {"id": 2453, "position": 2, "nom": "exercice_images/angles_6e_1_7_corrige_f75abc2da6857b25f5d8.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_1_7_corrige_f75abc2da6857b25f5d8.png", "width": 449, "height": 511, "alt": "Correction annotée — Découverte - Angles et bissectrices - 7. Mesurer puis partager un angle"}]}, {"id": 3489, "titre": "Entraînement - Angles et bissectrices - 1. Mesurer puis partager un angle", "images": [{"id": 2454, "position": 1, "nom": "exercice_images/angles_6e_2_1_1944f59ccdf385c2194d.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_1_1944f59ccdf385c2194d.png", "width": 607, "height": 406, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 1. Mesurer puis partager un angle"}, {"id": 2455, "position": 2, "nom": "exercice_images/angles_6e_2_1_corrige_5c4b468a394e5bebd602.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_1_corrige_5c4b468a394e5bebd602.png", "width": 607, "height": 483, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 1. Mesurer puis partager un angle"}]}, {"id": 3490, "titre": "Entraînement - Angles et bissectrices - 2. Mesurer puis partager un angle", "images": [{"id": 2456, "position": 1, "nom": "exercice_images/angles_6e_2_2_7074a7394c904bf399b1.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_2_7074a7394c904bf399b1.png", "width": 546, "height": 427, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 2. Mesurer puis partager un angle"}, {"id": 2457, "position": 2, "nom": "exercice_images/angles_6e_2_2_corrige_a8f468257ba15000461e.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_2_corrige_a8f468257ba15000461e.png", "width": 546, "height": 494, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 2. Mesurer puis partager un angle"}]}, {"id": 3491, "titre": "Entraînement - Angles et bissectrices - 3. Mesurer puis partager un angle", "images": [{"id": 2458, "position": 1, "nom": "exercice_images/angles_6e_2_3_b63722c18dd4b1405502.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_3_b63722c18dd4b1405502.png", "width": 504, "height": 441, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 3. Mesurer puis partager un angle"}, {"id": 2459, "position": 2, "nom": "exercice_images/angles_6e_2_3_corrige_d87dee3dc1fd80fef159.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_3_corrige_d87dee3dc1fd80fef159.png", "width": 504, "height": 501, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 3. Mesurer puis partager un angle"}]}, {"id": 3492, "titre": "Entraînement - Angles et bissectrices - 4. Mesurer puis partager un angle", "images": [{"id": 2460, "position": 1, "nom": "exercice_images/angles_6e_2_4_aba8402c212a81a293b0.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_4_aba8402c212a81a293b0.png", "width": 475, "height": 451, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 4. Mesurer puis partager un angle"}, {"id": 2461, "position": 2, "nom": "exercice_images/angles_6e_2_4_corrige_a7c0e2ecdee8c8d4c9ca.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_4_corrige_a7c0e2ecdee8c8d4c9ca.png", "width": 475, "height": 507, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 4. Mesurer puis partager un angle"}]}, {"id": 3493, "titre": "Entraînement - Angles et bissectrices - 5. Mesurer puis partager un angle", "images": [{"id": 2462, "position": 1, "nom": "exercice_images/angles_6e_2_5_ff13d37b4b526d0b8de8.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_5_ff13d37b4b526d0b8de8.png", "width": 458, "height": 457, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 5. Mesurer puis partager un angle"}, {"id": 2463, "position": 2, "nom": "exercice_images/angles_6e_2_5_corrige_9f993d3047995aa50b3b.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_5_corrige_9f993d3047995aa50b3b.png", "width": 458, "height": 510, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 5. Mesurer puis partager un angle"}]}, {"id": 3494, "titre": "Entraînement - Angles et bissectrices - 6. Mesurer puis partager un angle", "images": [{"id": 2464, "position": 1, "nom": "exercice_images/angles_6e_2_6_34cc910b023b55634351.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_6_34cc910b023b55634351.png", "width": 450, "height": 459, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 6. Mesurer puis partager un angle"}, {"id": 2465, "position": 2, "nom": "exercice_images/angles_6e_2_6_corrige_1c4ca8e0605561fa696b.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_6_corrige_1c4ca8e0605561fa696b.png", "width": 450, "height": 511, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 6. Mesurer puis partager un angle"}]}, {"id": 3495, "titre": "Entraînement - Angles et bissectrices - 7. Mesurer puis partager un angle", "images": [{"id": 2466, "position": 1, "nom": "exercice_images/angles_6e_2_7_7456f23304d47382c6a0.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_7_7456f23304d47382c6a0.png", "width": 458, "height": 459, "alt": "Schéma de travail — Entraînement - Angles et bissectrices - 7. Mesurer puis partager un angle"}, {"id": 2467, "position": 2, "nom": "exercice_images/angles_6e_2_7_corrige_4c767888d62d3a15116e.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_2_7_corrige_4c767888d62d3a15116e.png", "width": 458, "height": 511, "alt": "Correction annotée — Entraînement - Angles et bissectrices - 7. Mesurer puis partager un angle"}]}, {"id": 3496, "titre": "Problème - Angles et bissectrices - 1. Mesurer puis partager un angle", "images": [{"id": 2468, "position": 1, "nom": "exercice_images/angles_6e_3_1_a2744230e96255ce7fba.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_1_a2744230e96255ce7fba.png", "width": 573, "height": 418, "alt": "Schéma de travail — Problème - Angles et bissectrices - 1. Mesurer puis partager un angle"}, {"id": 2469, "position": 2, "nom": "exercice_images/angles_6e_3_1_corrige_95cede103e3e816ad729.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_1_corrige_95cede103e3e816ad729.png", "width": 573, "height": 489, "alt": "Correction annotée — Problème - Angles et bissectrices - 1. Mesurer puis partager un angle"}]}, {"id": 3497, "titre": "Problème - Angles et bissectrices - 2. Mesurer puis partager un angle", "images": [{"id": 2470, "position": 1, "nom": "exercice_images/angles_6e_3_2_4e386a835f189eca3a5a.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_2_4e386a835f189eca3a5a.png", "width": 523, "height": 435, "alt": "Schéma de travail — Problème - Angles et bissectrices - 2. Mesurer puis partager un angle"}, {"id": 2471, "position": 2, "nom": "exercice_images/angles_6e_3_2_corrige_2316ba7145f49587f50f.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_2_corrige_2316ba7145f49587f50f.png", "width": 523, "height": 498, "alt": "Correction annotée — Problème - Angles et bissectrices - 2. Mesurer puis partager un angle"}]}, {"id": 3498, "titre": "Problème - Angles et bissectrices - 3. Mesurer puis partager un angle", "images": [{"id": 2472, "position": 1, "nom": "exercice_images/angles_6e_3_3_5c9936f2882d3020c1b6.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_3_5c9936f2882d3020c1b6.png", "width": 488, "height": 446, "alt": "Schéma de travail — Problème - Angles et bissectrices - 3. Mesurer puis partager un angle"}, {"id": 2473, "position": 2, "nom": "exercice_images/angles_6e_3_3_corrige_1b146821a5566a6257fe.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_3_corrige_1b146821a5566a6257fe.png", "width": 488, "height": 504, "alt": "Correction annotée — Problème - Angles et bissectrices - 3. Mesurer puis partager un angle"}]}, {"id": 3499, "titre": "Problème - Angles et bissectrices - 4. Mesurer puis partager un angle", "images": [{"id": 2474, "position": 1, "nom": "exercice_images/angles_6e_3_4_2f601413a7940842b7be.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_4_2f601413a7940842b7be.png", "width": 466, "height": 454, "alt": "Schéma de travail — Problème - Angles et bissectrices - 4. Mesurer puis partager un angle"}, {"id": 2475, "position": 2, "nom": "exercice_images/angles_6e_3_4_corrige_3a5c8ef24c446041d9d1.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_4_corrige_3a5c8ef24c446041d9d1.png", "width": 466, "height": 508, "alt": "Correction annotée — Problème - Angles et bissectrices - 4. Mesurer puis partager un angle"}]}, {"id": 3500, "titre": "Problème - Angles et bissectrices - 5. Mesurer puis partager un angle", "images": [{"id": 2476, "position": 1, "nom": "exercice_images/angles_6e_3_5_6a06df6eaec7ba076752.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_5_6a06df6eaec7ba076752.png", "width": 453, "height": 459, "alt": "Schéma de travail — Problème - Angles et bissectrices - 5. Mesurer puis partager un angle"}, {"id": 2477, "position": 2, "nom": "exercice_images/angles_6e_3_5_corrige_780f1c86cee092990734.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_5_corrige_780f1c86cee092990734.png", "width": 453, "height": 511, "alt": "Correction annotée — Problème - Angles et bissectrices - 5. Mesurer puis partager un angle"}]}, {"id": 3501, "titre": "Problème - Angles et bissectrices - 6. Mesurer puis partager un angle", "images": [{"id": 2478, "position": 1, "nom": "exercice_images/angles_6e_3_6_098fa69ab002d4d027b6.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_6_098fa69ab002d4d027b6.png", "width": 449, "height": 459, "alt": "Schéma de travail — Problème - Angles et bissectrices - 6. Mesurer puis partager un angle"}, {"id": 2479, "position": 2, "nom": "exercice_images/angles_6e_3_6_corrige_f75abc2da6857b25f5d8.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_6_corrige_f75abc2da6857b25f5d8.png", "width": 449, "height": 511, "alt": "Correction annotée — Problème - Angles et bissectrices - 6. Mesurer puis partager un angle"}]}, {"id": 3502, "titre": "Problème - Angles et bissectrices - 7. Mesurer puis partager un angle", "images": [{"id": 2480, "position": 1, "nom": "exercice_images/angles_6e_3_7_dcc006bf83ab79f26a97.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_7_dcc006bf83ab79f26a97.png", "width": 492, "height": 459, "alt": "Schéma de travail — Problème - Angles et bissectrices - 7. Mesurer puis partager un angle"}, {"id": 2481, "position": 2, "nom": "exercice_images/angles_6e_3_7_corrige_7a217f6282befe4d7dc9.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/angles_6e_3_7_corrige_7a217f6282befe4d7dc9.png", "width": 492, "height": 511, "alt": "Correction annotée — Problème - Angles et bissectrices - 7. Mesurer puis partager un angle"}]}]}
const corrPath = path.join(dir, 'figures', 'correspondance.json')
const corr = fs.existsSync(corrPath) ? JSON.parse(read(corrPath)) : {}
const cache = path.join(dir, 'images_en_ligne')
fs.mkdirSync(cache, { recursive: true })

const mimeOf = (f) => {
  const ext = path.extname(f).slice(1).toLowerCase()
  return ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg' : ext === 'svg' ? 'image/svg+xml' : ext === 'webp' ? 'image/webp' : 'image/png'
}
const dataUri = (file) => `data:${mimeOf(file)};base64,${fs.readFileSync(file).toString('base64')}`
const pngHalf = (file) => {
  const b = fs.readFileSync(file)
  return { w: Math.round(b.readUInt32BE(16) / 2), h: Math.round(b.readUInt32BE(20) / 2) }
}

async function onlineImage(im) {
  const file = path.join(cache, path.basename(im.nom))
  if (!fs.existsSync(file)) {
    const r = await fetch(im.url)
    if (!r.ok) throw new Error(`téléchargement impossible : ${im.url} (${r.status})`)
    fs.writeFileSync(file, Buffer.from(await r.arrayBuffer()))
  }
  return { src: dataUri(file), size: im.width && im.height ? { w: im.width, h: im.height } : null, alt: im.alt || '' }
}

// genre : "cours" | "fiches" | "exercices"
async function imagesOf(genre, item) {
  const map = {}
  for (const im of item.images || []) map[im.position] = await onlineImage(im)
  const nouvelles = (corr[genre] || {})[String(item.id)] || {}
  for (const [pos, v] of Object.entries(nouvelles)) {
    const fichier = typeof v === 'string' ? v : v.fichier
    const file = path.join(dir, 'figures', 'images', fichier)
    if (!fs.existsSync(file)) {
      console.error(`⚠ figure absente : ${file}`)
      continue
    }
    map[pos] = { src: dataUri(file), size: pngHalf(file), alt: typeof v === 'string' ? '' : v.alt || '', nouvelle: true }
  }
  return map
}

// --- contenu -------------------------------------------------------------
const body = (txt) => {
  const k = txt.indexOf('<!-- optitab:1 -->')
  return k >= 0 ? txt.slice(k) : txt.replace(/^Titre:.*\n/, '')
}

function parseExercises(raw) {
  return raw
    .split(/^===[ \t]*$/m)
    .map((b) => b.trim())
    .filter(Boolean)
    .map((b) => {
      const titre = b.split('\n')[0].replace(/^===\s*/, '').trim()
      const brut = (b.match(/^Id:\s*(\S+)/m) || [])[1] || ''
      const id = /^\d+$/.test(brut) ? Number(brut) : brut
      const diff = (b.match(/^Difficulté:\s*(\w+)/m) || [])[1] || 'medium'
      const field = (name, next) => {
        const s = b.indexOf(`${name}:`)
        const e = next ? b.indexOf(`${next}:`, s) : b.length
        return b.slice(s + name.length + 1, e).trim()
      }
      return { id, titre, difficulte: diff, enonce: field('Énoncé', 'Étapes'), etapes: field('Étapes', 'Solution'), solution: field('Solution', null) }
    })
}

const docs = []
for (const c of meta.cours) {
  const f = path.join(dir, `cours_${c.id}.txt`)
  if (fs.existsSync(f)) docs.push({ key: `c${c.id}`, label: meta.cours.length > 1 ? `Cours ${c.id}` : 'Cours', ctx: 'course', text: body(read(f)), images: await imagesOf('cours', c) })
}
for (const s of meta.fiches) {
  const f = path.join(dir, `fiche_${s.id}.txt`)
  if (fs.existsSync(f)) docs.push({ key: `f${s.id}`, label: meta.fiches.length > 1 ? `Fiche ${s.id}` : 'Fiche de synthèse', ctx: 'sheet', text: body(read(f)), images: await imagesOf('fiches', s) })
}
const exFile = path.join(dir, 'exercices.txt')
const exercices = fs.existsSync(exFile) ? parseExercises(read(exFile)) : []
const exMeta = Object.fromEntries(meta.exercices.map((e) => [e.id, e]))
for (const ex of exercices) ex.images = await imagesOf('exercices', exMeta[ex.id] || { id: ex.id, images: [] })

const payload = { titre: meta.titre, sousTitre: `Notion ${meta.notion} · ${docs.length} document(s) · ${exercices.length} exercice(s)`, docs, exercices }
const json = JSON.stringify(payload).replace(/</g, '\\u003c')

const html = `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${meta.titre.replace(/</g, '&lt;')}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&display=swap">
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  },
  svg: { fontCache: 'none', scale: 1, minScale: 0.5, mtextInheritFont: true },
  options: { enableMenu: false },
  startup: { typeset: false }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>
<style>
:root { --page: #f4f6fb; --card: #ffffff; --line: #e3e9f4; --ink: #1c2130; --muted: #6b7385; --navy: #1b3c8e; color-scheme: light; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--page); }
body { font-family: 'Segoe UI', system-ui, -apple-system, Roboto, sans-serif; color: var(--ink); -webkit-font-smoothing: antialiased; }
.ap-top { background: #fff; border-bottom: 1px solid var(--line); position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: #fff; }
.ap-top-in { max-width: 1120px; margin: 0 auto; padding-block: 14px 0; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.ap-back { display: inline-block; margin-bottom: 8px; font: 600 13px/1.4 Montserrat, sans-serif; color: var(--navy); text-decoration: none; }
.ap-back:hover, .ap-back:focus-visible { text-decoration: underline; }
.ap-kicker { font: 700 11px/1.4 Montserrat, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #3b8544; }
.ap-title { font: 600 clamp(20px, 4.5vw, 26px)/1.25 Montserrat, sans-serif; margin: 4px 0 2px; }
.ap-sub { color: var(--muted); font-size: 14px; }
.ap-tabs { display: flex; gap: 4px; margin-top: 12px; overflow-x: auto; }
.ap-tab { appearance: none; border: 0; background: none; font: 600 14px/1 Montserrat, sans-serif; color: var(--muted); padding: 12px 14px 13px; border-bottom: 3px solid transparent; cursor: pointer; white-space: nowrap; }
.ap-tab[aria-selected="true"] { color: var(--navy); border-bottom-color: var(--navy); }
.ap-main { max-width: 1120px; margin: 0 auto; padding-block: 20px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.ap-panel[hidden] { display: none; }
.ap-card { background: var(--card); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 10px 30px rgba(15,23,42,.05); padding: 28px 32px 34px; }
.ex-list { display: flex; flex-direction: column; gap: 22px; }
.ex-card { background: var(--card); border: 1px solid var(--line); border-radius: 18px; box-shadow: 0 10px 30px rgba(15,23,42,.05); overflow: hidden; }
.ex-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 16px 22px 12px; }
.ex-level { font: 700 10.5px/1 Montserrat, sans-serif; letter-spacing: .1em; text-transform: uppercase; padding: 6px 9px; border-radius: 999px; }
.ex-level--easy { background: #eaf4ea; color: #3b8544; }
.ex-level--medium { background: #f1f3f8; color: #1b3c8e; }
.ex-level--hard { background: #fef6eb; color: #a86a1c; }
.ex-id { margin-left: auto; color: var(--muted); font: 600 11px/1 Montserrat, sans-serif; }
.ex-title { flex: 1 1 100%; order: 3; font: 600 17px/1.4 Montserrat, sans-serif; text-wrap: balance; }
.ex-tabs { display: flex; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); background: #fafbfd; }
.ex-tab { flex: 1; appearance: none; border: 0; background: none; padding: 13px 8px; font: 600 13.5px/1 Montserrat, sans-serif; color: var(--muted); border-bottom: 3px solid transparent; cursor: pointer; }
.ex-tab[aria-selected="true"] { color: var(--navy); border-bottom-color: var(--navy); background: #fff; }
.ex-panel { padding: 22px 24px 26px; }
.ex-panel[hidden] { display: none; }
figure.course-figure { margin: 1.2em 0; text-align: center; }
figure.course-figure img { max-width: 100%; height: auto; border-radius: 10px; }
@media (max-width: 640px) {
  .ap-main { padding-block: 14px 48px; }
  .ap-card { padding: 18px 14px 22px; border-radius: 14px; }
  .ex-head { padding: 14px 16px 10px; }
  .ex-panel { padding: 18px 14px 22px; }
  .ex-title { font-size: 15.5px; }
}
${css}
</style>
</head>
<body>
<header class="ap-top"><div class="ap-top-in">
  ${RETOUR ? `<a class="ap-back" href="${RETOUR.replace(/"/g, '&quot;')}">← Tous les chapitres</a>` : ''}
  <div class="ap-kicker">Aperçu · nouveau format</div>
  <h1 class="ap-title" id="ap-title"></h1>
  <p class="ap-sub" id="ap-sub"></p>
  <nav class="ap-tabs" role="tablist" id="ap-tabs"></nav>
</div></header>
<main class="ap-main" id="ap-main"></main>
<script id="data" type="application/json">${json}</script>
<script>
${engine}
${tune}

const DATA = JSON.parse(document.getElementById('data').textContent)
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;')

function withImages(html, map) {
  return html.replace(/\\[\\s*IMAGE\\s*_?\\s*(\\d+)\\s*\\]/gi, (m, pos) => {
    const img = map && map[pos]
    if (!img || !img.src) return m
    const dims = img.size ? ' width="' + img.size.w + '" height="' + img.size.h + '"' : ''
    return '<figure class="course-figure"><img alt="' + esc(img.alt || ('Illustration ' + pos)) + '"' + dims + ' src="' + img.src + '"></figure>'
  })
}

const typeset = async (el) => {
  if (!el || el.dataset.typeset) return
  el.dataset.typeset = '1'
  await MathJax.startup.promise
  await MathJax.typesetPromise([el])
  tuneMathOverflow(el)
}

document.getElementById('ap-title').textContent = DATA.titre
document.getElementById('ap-sub').textContent = DATA.sousTitre
const tabs = document.getElementById('ap-tabs')
const main = document.getElementById('ap-main')
const keys = []
DATA.docs.forEach((d) => {
  keys.push(d.key)
  tabs.insertAdjacentHTML('beforeend', '<button class="ap-tab" role="tab" data-tab="' + d.key + '" aria-selected="false">' + esc(d.label) + '</button>')
  main.insertAdjacentHTML('beforeend', '<section class="ap-panel" id="p-' + d.key + '" hidden><div class="ap-card"><div class="sci-doc" id="' + d.key + '"></div></div></section>')
  document.getElementById(d.key).innerHTML = withImages(renderOptitabDoc(d.text, { context: d.ctx }), d.images)
})
if (DATA.exercices.length) {
  tabs.insertAdjacentHTML('beforeend', '<button class="ap-tab" role="tab" data-tab="exercices" aria-selected="false">Exercices (' + DATA.exercices.length + ')</button>')
  main.insertAdjacentHTML('beforeend', '<section class="ap-panel" id="p-exercices" hidden><div class="ex-list" id="exercices"></div></section>')
}

const LEVELS = { easy: 'Découverte', medium: 'Entraînement', hard: 'Approfondissement' }
const list = document.getElementById('exercices')
DATA.exercices.forEach((ex) => {
  const card = document.createElement('article')
  card.className = 'ex-card'
  card.dataset.id = ex.id
  const t = [['Énoncé', ex.enonce], ['Étapes', ex.etapes], ['Solution', ex.solution]]
  card.innerHTML =
    '<header class="ex-head"><span class="ex-level ex-level--' + ex.difficulte + '">' + (LEVELS[ex.difficulte] || '') + '</span>' +
    '<span class="ex-id">Id ' + ex.id + '</span>' +
    '<h2 class="ex-title">' + esc(ex.titre) + '</h2></header>' +
    '<div class="ex-tabs" role="tablist">' + t.map((x, i) => '<button class="ex-tab" role="tab" data-i="' + i + '" aria-selected="' + (i === 0) + '">' + x[0] + '</button>').join('') + '</div>' +
    t.map((x, i) => '<div class="ex-panel sci-doc"' + (i ? ' hidden' : '') + '>' + withImages(renderOptitabDoc(x[1], { context: 'exercise' }), ex.images) + '</div>').join('')
  card.querySelectorAll('.ex-tab').forEach((b) => b.addEventListener('click', () => {
    card.querySelectorAll('.ex-tab').forEach((x) => x.setAttribute('aria-selected', String(x === b)))
    card.querySelectorAll('.ex-panel').forEach((p, i) => { p.hidden = String(i) !== b.dataset.i })
    typeset(card.querySelectorAll('.ex-panel')[Number(b.dataset.i)])
  }))
  list.appendChild(card)
})

function show(key) {
  document.querySelectorAll('.ap-tab').forEach((x) => x.setAttribute('aria-selected', String(x.dataset.tab === key)))
  document.querySelectorAll('.ap-panel').forEach((p) => { p.hidden = p.id !== 'p-' + key })
  window.scrollTo({ top: 0 })
  if (key === 'exercices') return Promise.all([...document.querySelectorAll('.ex-panel:not([hidden])')].map(typeset))
  return typeset(document.getElementById(key))
}
document.querySelectorAll('.ap-tab').forEach((b) => b.addEventListener('click', () => show(b.dataset.tab)))
window.__ready = show(keys[0] || 'exercices')
</script>
</body>
</html>
`

const final = ARTIFACT
  ? html
      .replace(/^<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport"[^\n]*\n/, '')
      .replace('</head>\n<body>\n', '')
      .replace(/<\/body>\n<\/html>\n?$/, '')
  : html
fs.writeFileSync(out, final)
console.log('Aperçu :', out, `(${Math.round(html.length / 1024)} Ko)`)
