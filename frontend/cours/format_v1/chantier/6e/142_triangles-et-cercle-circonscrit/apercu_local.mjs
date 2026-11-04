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
const meta = {"notion": 142, "titre": "Triangles et cercle circonscrit", "theme": 62, "contexte": 43, "cours": [{"id": 283, "titre": "Triangles et cercle circonscrit", "images": [{"id": 613, "position": 1, "nom": "cours_images/cours-construction-triangle_6e_b95602cbc7536086dbd9.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/cours-construction-triangle_6e_b95602cbc7536086dbd9.png", "width": 507, "height": 391, "alt": "Cours de 6e : Triangles et cercle circonscrit — construction triangle"}, {"id": 614, "position": 2, "nom": "cours_images/cours-somme-angles_6e_b22829e04e9c2cfce8fb.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/cours-somme-angles_6e_b22829e04e9c2cfce8fb.png", "width": 727, "height": 254, "alt": "Cours de 6e : Triangles et cercle circonscrit — somme angles"}, {"id": 615, "position": 3, "nom": "cours_images/cours-cercle-circonscrit_6e_69f962a8a74c3044ab32.png", "url": "https://optitab-media.s3.amazonaws.com/cours_images/cours-cercle-circonscrit_6e_69f962a8a74c3044ab32.png", "width": 790, "height": 454, "alt": "Cours de 6e : Triangles et cercle circonscrit — cercle circonscrit"}]}], "fiches": [{"id": 214, "titre": "Résumé : Triangles et cercle circonscrit", "images": [{"id": 265, "position": 1, "nom": "synthesis_images/cours-construction-triangle_6e_b95602cbc7536086dbd9.png", "url": "https://optitab-media.s3.amazonaws.com/synthesis_images/cours-construction-triangle_6e_b95602cbc7536086dbd9.png", "width": 507, "height": 391, "alt": "Fiche de 6e : Triangles et cercle circonscrit"}]}], "exercices": [{"id": 3503, "titre": "Découverte - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle", "images": [{"id": 2482, "position": 1, "nom": "exercice_images/triangles_6e_1_1_447b909525e544328f4c.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_1_447b909525e544328f4c.png", "width": 363, "height": 488, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle"}, {"id": 2483, "position": 2, "nom": "exercice_images/triangles_6e_1_1_corrige_2dbf0c4aa65f1c13fd0c.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_1_corrige_2dbf0c4aa65f1c13fd0c.png", "width": 457, "height": 488, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle"}]}, {"id": 3504, "titre": "Découverte - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles", "images": [{"id": 2484, "position": 1, "nom": "exercice_images/triangles_6e_1_2_730d33c249fac24525e5.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_2_730d33c249fac24525e5.png", "width": 846, "height": 456, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles"}, {"id": 2485, "position": 2, "nom": "exercice_images/triangles_6e_1_2_corrige_bb1a246c433ab4f55d58.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_2_corrige_bb1a246c433ab4f55d58.png", "width": 846, "height": 456, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles"}]}, {"id": 3505, "titre": "Découverte - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle", "images": [{"id": 2486, "position": 1, "nom": "exercice_images/triangles_6e_1_3_404e259d1f934f429acb.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_3_404e259d1f934f429acb.png", "width": 408, "height": 489, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle"}, {"id": 2487, "position": 2, "nom": "exercice_images/triangles_6e_1_3_corrige_70aec6c3d4932202a8e2.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_3_corrige_70aec6c3d4932202a8e2.png", "width": 493, "height": 521, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle"}]}, {"id": 3506, "titre": "Découverte - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles", "images": [{"id": 2488, "position": 1, "nom": "exercice_images/triangles_6e_1_4_c5db67222ab92c6dfed8.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_4_c5db67222ab92c6dfed8.png", "width": 846, "height": 465, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles"}, {"id": 2489, "position": 2, "nom": "exercice_images/triangles_6e_1_4_corrige_3ba0aeafde2aa1b3279d.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_4_corrige_3ba0aeafde2aa1b3279d.png", "width": 846, "height": 465, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles"}]}, {"id": 3507, "titre": "Découverte - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle", "images": [{"id": 2490, "position": 1, "nom": "exercice_images/triangles_6e_1_5_ba8c97d9ea0ab79a25ec.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_5_ba8c97d9ea0ab79a25ec.png", "width": 432, "height": 483, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle"}, {"id": 2491, "position": 2, "nom": "exercice_images/triangles_6e_1_5_corrige_9783dae95f08d01e46d9.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_5_corrige_9783dae95f08d01e46d9.png", "width": 511, "height": 536, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle"}]}, {"id": 3508, "titre": "Découverte - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles", "images": [{"id": 2492, "position": 1, "nom": "exercice_images/triangles_6e_1_6_71dfcadd22a293075487.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_6_71dfcadd22a293075487.png", "width": 846, "height": 472, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles"}, {"id": 2493, "position": 2, "nom": "exercice_images/triangles_6e_1_6_corrige_059bb30a1f853eac582f.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_6_corrige_059bb30a1f853eac582f.png", "width": 846, "height": 472, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles"}]}, {"id": 3509, "titre": "Découverte - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle", "images": [{"id": 2494, "position": 1, "nom": "exercice_images/triangles_6e_1_7_f7b6102b4bb1e8ae4a17.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_7_f7b6102b4bb1e8ae4a17.png", "width": 448, "height": 479, "alt": "Schéma de travail — Découverte - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle"}, {"id": 2495, "position": 2, "nom": "exercice_images/triangles_6e_1_7_corrige_7893bd178cddd7f8ac2a.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_1_7_corrige_7893bd178cddd7f8ac2a.png", "width": 523, "height": 546, "alt": "Correction annotée — Découverte - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle"}]}, {"id": 3510, "titre": "Entraînement - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle", "images": [{"id": 2496, "position": 1, "nom": "exercice_images/triangles_6e_2_1_607731e1ef2f50539e1b.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_1_607731e1ef2f50539e1b.png", "width": 323, "height": 503, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle"}, {"id": 2497, "position": 2, "nom": "exercice_images/triangles_6e_2_1_corrige_7cf3565e8944045909e8.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_1_corrige_7cf3565e8944045909e8.png", "width": 461, "height": 503, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle"}]}, {"id": 3511, "titre": "Entraînement - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles", "images": [{"id": 2498, "position": 1, "nom": "exercice_images/triangles_6e_2_2_c8e1454582273f33a72d.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_2_c8e1454582273f33a72d.png", "width": 846, "height": 470, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles"}, {"id": 2499, "position": 2, "nom": "exercice_images/triangles_6e_2_2_corrige_7228c215738fbb79ed09.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_2_corrige_7228c215738fbb79ed09.png", "width": 846, "height": 470, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles"}]}, {"id": 3512, "titre": "Entraînement - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle", "images": [{"id": 2500, "position": 1, "nom": "exercice_images/triangles_6e_2_3_36f738f0585febb4c70c.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_3_36f738f0585febb4c70c.png", "width": 377, "height": 509, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle"}, {"id": 2501, "position": 2, "nom": "exercice_images/triangles_6e_2_3_corrige_3375b0ef4c2a0c6e4e09.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_3_corrige_3375b0ef4c2a0c6e4e09.png", "width": 501, "height": 527, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle"}]}, {"id": 3513, "titre": "Entraînement - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles", "images": [{"id": 2502, "position": 1, "nom": "exercice_images/triangles_6e_2_4_d93c4b9581013001cbd6.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_4_d93c4b9581013001cbd6.png", "width": 846, "height": 480, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles"}, {"id": 2503, "position": 2, "nom": "exercice_images/triangles_6e_2_4_corrige_389b5a16665c251bedb1.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_4_corrige_389b5a16665c251bedb1.png", "width": 846, "height": 480, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles"}]}, {"id": 3514, "titre": "Entraînement - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle", "images": [{"id": 2504, "position": 1, "nom": "exercice_images/triangles_6e_2_5_07bbc1d6c242dd1dcb7c.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_5_07bbc1d6c242dd1dcb7c.png", "width": 406, "height": 502, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle"}, {"id": 2505, "position": 2, "nom": "exercice_images/triangles_6e_2_5_corrige_4cdcf7a03130229be31d.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_5_corrige_4cdcf7a03130229be31d.png", "width": 515, "height": 540, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle"}]}, {"id": 3515, "titre": "Entraînement - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles", "images": [{"id": 2506, "position": 1, "nom": "exercice_images/triangles_6e_2_6_52b50c01de687b76a0a5.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_6_52b50c01de687b76a0a5.png", "width": 846, "height": 488, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles"}, {"id": 2507, "position": 2, "nom": "exercice_images/triangles_6e_2_6_corrige_5c7956fbcc6d0dc1b375.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_6_corrige_5c7956fbcc6d0dc1b375.png", "width": 846, "height": 488, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles"}]}, {"id": 3516, "titre": "Entraînement - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle", "images": [{"id": 2508, "position": 1, "nom": "exercice_images/triangles_6e_2_7_d1e6dd919c6bb174ae5d.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_7_d1e6dd919c6bb174ae5d.png", "width": 425, "height": 496, "alt": "Schéma de travail — Entraînement - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle"}, {"id": 2509, "position": 2, "nom": "exercice_images/triangles_6e_2_7_corrige_5014be3f7bca8b87a623.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_2_7_corrige_5014be3f7bca8b87a623.png", "width": 525, "height": 549, "alt": "Correction annotée — Entraînement - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle"}]}, {"id": 3517, "titre": "Problème - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle", "images": [{"id": 2510, "position": 1, "nom": "exercice_images/triangles_6e_3_1_2e1e681310f040d5749c.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_1_2e1e681310f040d5749c.png", "width": 294, "height": 513, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle"}, {"id": 2511, "position": 2, "nom": "exercice_images/triangles_6e_3_1_corrige_fdab67867830f29dfeea.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_1_corrige_fdab67867830f29dfeea.png", "width": 469, "height": 513, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 1. Construire un triangle et son cercle"}]}, {"id": 3518, "titre": "Problème - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles", "images": [{"id": 2512, "position": 1, "nom": "exercice_images/triangles_6e_3_2_dd09490d005fdb91cd7c.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_2_dd09490d005fdb91cd7c.png", "width": 846, "height": 483, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles"}, {"id": 2513, "position": 2, "nom": "exercice_images/triangles_6e_3_2_corrige_8a0e93b68d52541e0f8a.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_2_corrige_8a0e93b68d52541e0f8a.png", "width": 846, "height": 483, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 2. Préparer une construction avec deux angles"}]}, {"id": 3519, "titre": "Problème - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle", "images": [{"id": 2514, "position": 1, "nom": "exercice_images/triangles_6e_3_3_5b044dbc09359480a8ed.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_3_5b044dbc09359480a8ed.png", "width": 351, "height": 523, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle"}, {"id": 2515, "position": 2, "nom": "exercice_images/triangles_6e_3_3_corrige_241a91d274b9e8691a00.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_3_corrige_241a91d274b9e8691a00.png", "width": 507, "height": 533, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 3. Construire un triangle et son cercle"}]}, {"id": 3520, "titre": "Problème - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles", "images": [{"id": 2516, "position": 1, "nom": "exercice_images/triangles_6e_3_4_6ff2e7e6d490feb2b4e1.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_4_6ff2e7e6d490feb2b4e1.png", "width": 846, "height": 493, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles"}, {"id": 2517, "position": 2, "nom": "exercice_images/triangles_6e_3_4_corrige_d3e217332047d85f0fe7.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_4_corrige_d3e217332047d85f0fe7.png", "width": 846, "height": 493, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 4. Préparer une construction avec deux angles"}]}, {"id": 3521, "titre": "Problème - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle", "images": [{"id": 2518, "position": 1, "nom": "exercice_images/triangles_6e_3_5_2708074db27c10b14950.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_5_2708074db27c10b14950.png", "width": 383, "height": 515, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle"}, {"id": 2519, "position": 2, "nom": "exercice_images/triangles_6e_3_5_corrige_e6797a4b571d122d1fe7.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_5_corrige_e6797a4b571d122d1fe7.png", "width": 521, "height": 544, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 5. Construire un triangle et son cercle"}]}, {"id": 3522, "titre": "Problème - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles", "images": [{"id": 2520, "position": 1, "nom": "exercice_images/triangles_6e_3_6_74f5c1d6e7c72078af5f.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_6_74f5c1d6e7c72078af5f.png", "width": 846, "height": 502, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles"}, {"id": 2521, "position": 2, "nom": "exercice_images/triangles_6e_3_6_corrige_b4a848cbce4b724912fa.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_6_corrige_b4a848cbce4b724912fa.png", "width": 846, "height": 502, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 6. Préparer une construction avec deux angles"}]}, {"id": 3523, "titre": "Problème - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle", "images": [{"id": 2522, "position": 1, "nom": "exercice_images/triangles_6e_3_7_c8d67ff933a219342c65.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_7_c8d67ff933a219342c65.png", "width": 405, "height": 508, "alt": "Schéma de travail — Problème - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle"}, {"id": 2523, "position": 2, "nom": "exercice_images/triangles_6e_3_7_corrige_23ff443f9331edf7ef2e.png", "url": "https://optitab-media.s3.amazonaws.com/exercice_images/triangles_6e_3_7_corrige_23ff443f9331edf7ef2e.png", "width": 529, "height": 551, "alt": "Correction annotée — Problème - Triangles et cercle circonscrit - 7. Construire un triangle et son cercle"}]}]}
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
