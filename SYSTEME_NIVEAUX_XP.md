# 🎮 Système de Niveaux et XP - OptiTAB

## 📋 Vue d'ensemble

Le système de gamification d'OptiTAB utilise une **progression exponentielle** pour encourager l'apprentissage régulier et la maîtrise des compétences. Seuls les **quiz** donnent des points d'expérience (XP), les exercices guidés étant dédiés à l'apprentissage sans pression.

---

## 🎯 Formule de Progression

### Calcul des Niveaux
**Formule :** `Niveau N nécessite N × N × 10 XP au total`

**Exemples :**
- Niveau 1 = 1² × 10 = **10 XP**
- Niveau 2 = 2² × 10 = **40 XP** 
- Niveau 3 = 3² × 10 = **90 XP**
- Niveau 10 = 10² × 10 = **1000 XP**

---

## 📊 Tableau Complet des Niveaux

| **Niveau** | **XP à Gagner** | **XP Total Requis** | **Écart avec Niveau Précédent** |
|------------|-----------------|---------------------|----------------------------------|
| **0** | 0 | 0 | *Point de départ* |
| **1** | 10 | 10 | +10 |
| **2** | 30 | 40 | +30 |
| **3** | 50 | 90 | +50 |
| **4** | 70 | 160 | +70 |
| **5** | 90 | 250 | +90 |
| **6** | 110 | 360 | +110 |
| **7** | 130 | 490 | +130 |
| **8** | 150 | 640 | +150 |
| **9** | 170 | 810 | +170 |
| **10** | 190 | 1000 | +190 |
| **15** | 440 | 2250 | +440 |
| **20** | 790 | 4000 | +790 |

---

## 🎮 Comment Gagner des XP

### 📚 Exercices Guidés
- **XP Gagné :** `0 XP` (toujours)
- **Objectif :** Apprentissage et compréhension
- **Aucune pression de performance**

### 🧠 Quiz

#### 🏆 Règle Principale : SEULE LA 1ÈRE TENTATIVE DONNE DES XP

#### 📈 Calcul des XP par Difficulté

| **Difficulté** | **Coefficient** | **Temps par Question** | **Formule XP** |
|----------------|-----------------|------------------------|----------------|
| **Facile** | ×1.0 | 20 secondes | `Score × 1.0` |
| **Moyen** | ×1.5 | 25 secondes | `Score × 1.5` |
| **Difficile** | ×2.0 | 30 secondes | `Score × 2.0` |

#### ⚡ Bonus de Vitesse
- **Condition :** Terminer en moins de 50% du temps autorisé
- **Bonus :** `+1 XP` (uniquement 1ère tentative)
- **Calcul temps total :** `Nombre de questions × Temps par question`

**Exemple :**
- Quiz moyen de 10 questions = 10 × 25s = 250s autorisées
- Bonus si terminé en moins de 125s

---

## 🔄 Système de Cooldown

### ⏰ Règles des Tentatives
- **1ère tentative :** XP selon score et difficulté
- **2ème, 3ème, 4ème... tentatives :** `0 XP`
- **Cooldown :** `1h30` entre chaque tentative
- **Objectif :** Éviter la mémorisation, encourager la compréhension

### 🎯 Stratégie Recommandée
1. **Réviser le contenu** avant le quiz
2. **Viser la perfection** dès la 1ère tentative
3. **Gérer son temps** pour le bonus vitesse
4. **Progresser graduellement** en difficulté

---

## 💡 Exemples Concrets

### Exemple 1 : Quiz Facile
- **Questions :** 10
- **Score :** 8/10
- **Temps :** 150s (temps autorisé : 200s)
- **Calcul :** `8 × 1.0 = 8 XP` (pas de bonus vitesse)

### Exemple 2 : Quiz Moyen avec Bonus
- **Questions :** 12
- **Score :** 10/12
- **Temps :** 140s (temps autorisé : 300s)
- **Calcul :** `10 × 1.5 = 15 XP + 1 bonus = 16 XP`

### Exemple 3 : Quiz Difficile Parfait
- **Questions :** 8
- **Score :** 8/8
- **Temps :** 100s (temps autorisé : 240s)
- **Calcul :** `8 × 2.0 = 16 XP + 1 bonus = 17 XP`

---

## 🚀 Progression Réaliste

### Pour Atteindre Niveau 5 (250 XP)
- **Option 1 :** ~25 quiz faciles parfaits (10/10)
- **Option 2 :** ~17 quiz moyens parfaits (10/10)
- **Option 3 :** ~13 quiz difficiles parfaits (10/10)
- **Option 4 :** ~20 quiz mixtes avec bonnes performances

### Pour Atteindre Niveau 10 (1000 XP)
- **Option 1 :** ~100 quiz faciles parfaits
- **Option 2 :** ~67 quiz moyens parfaits
- **Option 3 :** ~50 quiz difficiles parfaits
- **Option 4 :** ~75 quiz mixtes avec stratégie optimisée

---

## 🎯 Stratégies Avancées

### 🥇 Optimisation des Points
1. **Commencer par les quiz faciles** pour prendre confiance
2. **Progresser vers les quiz moyens** pour plus d'XP
3. **Maîtriser les quiz difficiles** pour maximiser les gains
4. **Viser systématiquement le bonus vitesse** (+1 XP)

### ⏱️ Gestion du Temps
- **Quiz Facile :** Viser <10s par question pour le bonus
- **Quiz Moyen :** Viser <12.5s par question pour le bonus
- **Quiz Difficile :** Viser <15s par question pour le bonus

### 📈 Planification Long Terme
- **Niveau 1-3 :** Se familiariser avec le système
- **Niveau 4-7 :** Développer une routine d'étude
- **Niveau 8+ :** Viser l'excellence et les bonus vitesse

---

## 🔧 Aspects Techniques

### Frontend (Vue.js)
- **Composable :** `useXP.js` et `useLevel.js`
- **Store :** Pinia pour la gestion d'état
- **Mise à jour :** Instantanée dans l'interface

### Backend (Django)
- **Modèle :** `CustomUser.xp`
- **Calcul :** `calculate_user_level()` 
- **Validation :** Système de cooldown intégré

### Synchronisation
- **Temps réel :** Mise à jour immédiate de l'XP
- **Persistance :** Sauvegarde en base de données
- **Cohérence :** Même logique frontend/backend

---

## 📱 Interface Utilisateur

### Affichage des Informations
- **Header :** Niveau actuel et XP
- **Barre de progression :** Avancement vers niveau suivant
- **Quiz :** Score coloré selon performance
- **Cooldown :** Timer en temps réel

### Codes Couleur des Scores
- **🔴 Rouge :** Score < 5/10 (sous la moyenne)
- **🟠 Orange :** Score = 5/10 (moyenne)
- **🟢 Vert :** Score > 5/10 (au-dessus de la moyenne)

---

## 🎉 Conclusion

Le système d'XP d'OptiTAB est conçu pour :
- **Encourager la qualité** plutôt que la quantité
- **Récompenser la vitesse** et la précision
- **Éviter la triche** par mémorisation
- **Maintenir l'engagement** à long terme

**Devise du système :** *"Une première tentative réussie vaut mieux que dix tentatives moyennes !"* 🏆
