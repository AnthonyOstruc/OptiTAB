# Rapport — Terminale, notion 89 « Calcul intégral »

**État : prêt.** verifier_notion.py --navigateur : OK (0 problème).

## Texte
- Contrôle : `verif_calcul-integral.py` (sympy + scipy) — 169 contrôles, 0 erreur. Aucune erreur de calcul dans la version en ligne.
- Cours restructuré (modèle pilote) : prérequis, définition (unité d'aire), théorème fondamental + `demonstration` (cas croissant), existence des primitives, propriétés (linéarité, Chasles, positivité, croissance) + exemple d'encadrement de ∫e^{-x²}, aires (signe quelconque, entre deux courbes, méthode), valeur moyenne + piège, IPP + démonstration + choix de u/v', méthode des rectangles (encadrement n = 8 et code Python). Notation `\mathrm{d}x`, intervalles `[a\,;b]`, virgule décimale.
- Fiche : formules clés, propriétés, aires/moyenne, IPP, 4 pièges, réflexe.
- 12 exercices réécrits au format pilote (méthode / étapes / résultat, `attention`, `retenir`, tableaux de signes natifs).
- Corrections de fond (pédagogie / programme) :
  - « Changement de variable » (Id 1237) : hors programme → traité par reconnaissance des formes u'f(u) (au programme) ; le changement de variable est conservé en « Pour aller plus loin ». Titre inchangé.
  - Intégration par parties : règle anglo-saxonne « ILATE » (citant arctan, arcsin, hors programme) et notation du/dv remplacées par u, v' (notation du programme).
  - Modélisation (Id 1240) : unités ajoutées, R(0) = 0 précisé, question 2 complétée (le mobile change de sens : distance parcourue 6 + 8√3/9 ≈ 7,54 m, comme dans le livre Terminale).
  - Décimales « 0.5 », « 70.6°C » → « 0,5 », « 70,6 °C » ; valeurs approchées ajoutées.

## Figures
- 26 images en ligne (matplotlib, fenêtres énormes, style hétérogène) : **toutes refaites**, 0 conservée.
- 32 figures TikZ au style des livres (aires en fill between / closedcycle : vert = compté positivement, orange = sous l'axe ; valeur moyenne : aire bleu pâle + rectangle vert de même aire), 35 emplacements (réutilisations : cours_entre ×3, cours_moyenne ×2, cours_sin_signe ×2).
- Ajouts : cours (démonstration du théorème fondamental, aire algébrique du sinus), Id 1241 (5 figures), Id 1242 (2 figures).
- Contrôle automatique des chevauchements texte/trait : toutes les figures passent, largeur ≤ 900 px ; chaque PNG regardé.

## Remarques pour l'orchestrateur
- Les en-têtes `Image:` d'origine sont conservés ; 1241 et 1242 ont des images sans en-tête (avertissement « utilisée mais non déclarée » de valider_v1, filtré par verifier_notion).
- Textes alternatifs sans accents (volontaire, ASCII).

## Finition 2026-11-02

**État : prêt** (passe de finition, agent finition-T4).

### Titres
- Cours « Calcul intégral » (était « Le calcul intégral »), fiche « Résumé : Calcul intégral ».
- 12 titres d'exercices sans « Calcul Intégral » répété ni majuscules abusives (ex. « Découverte - Calculer une intégrale avec une primitive », « Entraînement - Aire entre deux courbes », « Type examen - Aire, valeur moyenne et intégration par parties »). Types inchangés.

### Exercices
- **2 ajoutés** (12 → 14) : `nouveau-1` « Type examen - Étude d'une suite d'intégrales » (Iₙ = ∫₀¹ xⁿeˣ dx : IPP, récurrence Iₙ₊₁ = e − (n+1)Iₙ, décroissance, encadrement 1/(n+1) ≤ Iₙ ≤ e/(n+1), limites de Iₙ et de (n+1)Iₙ) ; `nouveau-2` « Problème - Encadrer une intégrale par la méthode des rectangles » (J = ∫₀¹ dx/(1+x²), s₄ et S₄ exacts, Sₙ − sₙ = 1/(2n), n = 500, fonction Python, encadrement de π).
- **1242 Q3 réécrite** : c'était exactement 1238 Q4 (∫₀¹ xe²ˣ) ; remplacée par ∫₁ᵉ x ln x dx = (e² + 1)/4 (choix u = ln x).
- Compléments : 1231 Q4 (aire algébrique 14/3 − 1/6), 1232 Q2 (Chasles illustré), 1233 Q3 (compensation 1 − 1), 1238 Q3 (IPP illustrée), 1240 Q2 (déplacement / distance sur le graphe de la vitesse), 1240 Q4 (moyenne ≠ demi-somme).
- Cours : encadré « Étudier une suite d'intégrales » + exemple ∫₀¹ xⁿ/(1+x) dx ; remarque « Interprétation graphique » de l'IPP (rectangle e × 1 = 𝒜₁ + 𝒜₂). Fiche : point « suite d'intégrales » + figure de la valeur moyenne.

### Figures (43 fichiers, 49 emplacements)
- **Revérifiées à l'œil : les 31 existantes** (justesse des courbes et des valeurs, chevauchements, lisibilité) : justes et propres. **1 retouchée** : `e1239_q1` (étiquette 𝒜₁ ajoutée sur la partie orange, citée par le corrigé).
- **12 ajoutées** : cours `cours_encadre` (e^(−x²) entre 1 − x² et 1), `cours_suite` (xⁿ/(1+x), n = 1, 3, 8, légende par style de trait), `cours_ipp` (IPP illustrée) ; exercices `e1231_q4`, `e1232_q2`, `e1233_q3`, `e1240_q2` (vitesse), `e1240_q4` (température moyenne), `e1242_q2`, `e1242_q5` (valeurs moyennes), `en1_suite`, `en2_rect`. Réponses en vert, parties négatives en orange (convention de la notion).
- 1237 (forme u′f(u)) reste sans figure : pur calcul, une figure serait décorative.
- Textes alternatifs : tous réécrits avec accents et symboles (x², π, 𝒜₁…).
- `figures_livre.py` : 43/43, 0 erreur, 0 avertissement.

### Contrôles
- `verif_calcul-integral.py` : 258 contrôles, 0 erreur (dont nouveaux exercices, valeurs des figures, code Python exécuté).
- Formules au téléphone (mesure Chrome 390 px) : 9 formules qui défilaient et une dizaine réduites à moins de 75 % redécoupées (cours, 1232, 1235, 1239, 1240, 1241, nouveau-2) → 0 formule qui défile.
- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures téléphone regardées : cours (encadrement, suite d’intégrales, IPP illustrée, rectangles), exercice nouveau-2 (étapes). Deux ponctuations isolées en début de ligne corrigées dans le cours (Chasles, exemple du sinus).
- controle_apercu.mjs (captures) est resté bloqué à la fermeture de Chrome après la dernière capture (défaut connu) : seul mon processus a été arrêté et son verrou libéré.
- Remarque : la consigne parlait d’aire « hachurée » ; les domaines restent colorés (vert / orange), comme dans le livre Terminale et le reste de la notion, pour ne pas mélanger deux styles.
