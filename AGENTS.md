# Consignes pour les assistants IA (Codex, Claude, autres)

Projet OptiTAB : site de cours de maths (Vue 3 + Django). Le propriétaire est
francophone et non technicien ; il veut un résultat « ultra propre, impeccable,
professionnel » et des comptes rendus courts en français.

## Avant toute chose
- `backend/.env` pointe sur la base et le stockage de **PRODUCTION** : tout ce qui
  est écrit en local est en ligne immédiatement. Toujours une sauvegarde et une
  simulation avant d'écrire.
- Aucun `git commit` / `git push` sans accord explicite du propriétaire.
- Ne jamais copier de livre, PDF ou audio sur le Bureau.

## Refaire ou améliorer un chapitre du site (cours, fiche, exercices, schémas)
Tout est documenté dans `frontend/cours/format_v1/` :
1. `GUIDE_CHANTIER.md` — méthode complète : consignes du propriétaire (pédagogie,
   structure des exercices et des corrigés, où mettre les schémas, style des
   figures), règles, déroulé, contrôles, orchestration (§ 8).
2. `FORMAT.md` — syntaxe du format OptiTAB v1 (encadrés, tableaux, code, images).
3. Chapitres modèles déjà en ligne : voir le début de `GUIDE_CHANTIER.md`.
4. `FILE_3E.md` / `FILE_FINITION.md` — ce qui est fait, ce qui reste, dans quel ordre.

Chaque chapitre a son dossier `frontend/cours/format_v1/chantier/<niveau>/<id>_<slug>/`
avec `RAPPORT.md` (historique) et `etat.json` (a_faire / en_cours / pret / importe).
Ne jamais travailler sur un dossier « en_cours » d'un autre agent.
