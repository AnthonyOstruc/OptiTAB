filepath = r'c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\exercices\2nd\exercice_probabilites_modeliserle_hasard_seconde.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ---- FIX 1 : Q5 Maîtrise - remplacer Idée/Conclusion par Méthode/Étape1/Étape2/Résultat ----
old_q5_maitrise = (
    "   ● **Idée :** La probabilité $\\displaystyle 0{,}5$ est une valeur **du modèle** ; la fréquence dépend des résultats d'un échantillon\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Conclusion :** La fréquence varie d'un échantillon à l'autre (hasard), et se rapproche souvent de $\\displaystyle 0{,}5$ quand $\\displaystyle n$ devient grand\n"
    "    $\\\\$"
)

new_q5_maitrise = (
    "    ● **Méthode :** Distinguer la probabilité (valeur du modèle théorique) de la fréquence (observation sur un échantillon)\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Étape 1 :** La probabilité est une valeur fixe du modèle\n"
    "        $\\qquad$• Le modèle suppose que la pièce est équilibrée : $\\displaystyle P(\\text{Pile})=0{,}5$\n"
    "        $\\\\$\n"
    "        $\\qquad$• Cette valeur est théorique — elle ne dépend pas des résultats obtenus\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Étape 2 :** La fréquence est une observation, variable selon l'échantillon\n"
    "        $\\qquad$• $\\displaystyle f_A=0{,}65$ (40 lancers) et $\\displaystyle f_B=0{,}54$ (200 lancers) sont deux observations différentes\n"
    "        $\\\\$\n"
    "        $\\qquad$• Le hasard fait varier les fréquences d'un échantillon à l'autre, même si le modèle est fixe\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Résultat :** La fréquence peut différer de $\\displaystyle 0{,}5$ à cause du hasard ; plus $\\displaystyle n$ est grand, plus elle se stabilise autour de $\\displaystyle 0{,}5$ (loi des grands nombres)\n"
    "    $\\\\$"
)

if old_q5_maitrise in content:
    content = content.replace(old_q5_maitrise, new_q5_maitrise, 1)
    print("FIX 1 (Q5 Maîtrise) : OK")
else:
    print("FIX 1 (Q5 Maîtrise) : INTROUVABLE — vérifier le texte")
    # Debug: find approximate location
    idx = content.find("**Idée :**")
    if idx != -1:
        print("  Contexte trouvé:", repr(content[idx-5:idx+150]))

# ---- FIX 2 : Exercice "Modèle ou fréquences" — remplacer Principe uniquement par Q1-Q5 ----
old_principe = (
    "    ● **Modèle théorique :** univers connu et hypothèse d'équiprobabilité (dés, pièces, urnes décrites…)\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Fréquences :** phénomène réel dépendant de données historiques (météo, sport, pannes, comportements…). Attention : on peut aussi construire des **modèles** pour ces situations, mais ils nécessitent des données passées pour être calibrés.\n"
    "    $\\\\$"
)

new_principe = (
    "    ● **Modèle théorique :** univers connu et hypothèse d'équiprobabilité (dés, pièces, urnes décrites…)\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Fréquences :** phénomène réel dépendant de données historiques (météo, sport, pannes, comportements…). Attention : on peut aussi construire des **modèles** pour ces situations, mais ils nécessitent des données passées pour être calibrés.\n"
    "    $\\\\$\n"
    "\n"
    "**Question 1 : Urne avec 5 boules numérotées**\n"
    "\n"
    "    ● **Étape 1 :** L'univers est connu et les issues sont équiprobables\n"
    "        $\\qquad$• $\\displaystyle \\Omega=\\{1,2,3,4,5\\}$, toutes les boules sont équivalentes\n"
    "        $\\\\$\n"
    "        $\\qquad$• On applique l'équiprobabilité : $\\displaystyle P(\\{k\\})=\\dfrac{1}{5}$ pour chaque issue\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Résultat :** → **Modèle théorique équiprobable**\n"
    "    $\\\\$\n"
    "\n"
    "**Question 2 : Probabilité de pluie demain**\n"
    "\n"
    "    ● **Étape 1 :** Peut-on supposer l'équiprobabilité ?\n"
    "        $\\qquad$• La météo dépend de nombreux facteurs complexes — l'équiprobabilité ne s'applique pas a priori\n"
    "        $\\\\$\n"
    "        $\\qquad$• On utilise des données météo historiques pour estimer la fréquence de jours de pluie\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Résultat :** → **Estimation par fréquences** (données météo historiques)\n"
    "    $\\\\$\n"
    "\n"
    "**Question 3 : Probabilité qu'un message soit un spam**\n"
    "\n"
    "    ● **Étape 1 :** Identifier la nature de la situation\n"
    "        $\\qquad$• Le comportement des spams dépend de statistiques réelles sur les messages reçus\n"
    "        $\\\\$\n"
    "        $\\qquad$• On compte le nombre de spams parmi les messages passés pour estimer la fréquence\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Résultat :** → **Estimation par fréquences** (statistiques de spams)\n"
    "    $\\\\$\n"
    "\n"
    "**Question 4 : Dé équilibré à 10 faces, multiple de 3**\n"
    "\n"
    "    ● **Étape 1 :** L'univers est connu et équiprobable\n"
    "        $\\qquad$• $\\displaystyle \\Omega=\\{1,2,3,\\ldots,10\\}$, toutes les faces équiprobables : $\\displaystyle P(\\{k\\})=\\dfrac{1}{10}$\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Étape 2 :** Identifier les multiples de 3 dans $\\displaystyle \\Omega$\n"
    "        $\\qquad$• Multiples de 3 : $\\displaystyle \\{3,6,9\\}$ → 3 issues\n"
    "        $\\\\$\n"
    "        $\\qquad$• $\\displaystyle P(\\text{multiple de 3})=\\dfrac{3}{10}$\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Résultat :** → **Modèle théorique équiprobable**\n"
    "    $\\\\$\n"
    "\n"
    "**Question 5 : Probabilité de victoire de l'équipe**\n"
    "\n"
    "    ● **Étape 1 :** Identifier la nature de la situation\n"
    "        $\\qquad$• Les résultats sportifs ne sont pas équiprobables — ils dépendent de la forme des équipes, du terrain…\n"
    "        $\\\\$\n"
    "        $\\qquad$• On utilise les résultats passés (victoires, défaites, matchs nuls) pour estimer la probabilité\n"
    "    $\\\\$\n"
    "    \n"
    "    ● **Résultat :** → **Estimation par fréquences** (résultats sportifs passés)\n"
    "    $\\\\$"
)

if old_principe in content:
    content = content.replace(old_principe, new_principe, 1)
    print("FIX 2 (Principe Q1-Q5) : OK")
else:
    print("FIX 2 (Principe Q1-Q5) : INTROUVABLE — vérifier le texte")
    idx = content.find("**Modèle théorique :** univers connu")
    if idx != -1:
        print("  Contexte trouvé:", repr(content[idx-5:idx+200]))

# Sauvegarder
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fichier sauvegardé.")
