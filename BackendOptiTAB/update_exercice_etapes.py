#!/usr/bin/env python
"""
Script pour mettre à jour les étapes des exercices
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from curriculum.models import Exercice

def update_exercice_etapes():
    # Mettre à jour l'exercice ID 47 avec les étapes
    try:
        exercice = Exercice.objects.get(id=47)
        print(f"Exercice trouvé: {exercice.titre}")
        
        etapes_text = """**Question 1 : Calcul des cinq premiers termes**
🔵 Étape 1 : Commencer avec le premier terme
    $u_0 = 3$

🔵 Étape 2 : Calculer les termes suivants
    $u_1 = u_0 + 2 = 3 + 2 = 5$
    $u_2 = u_1 + 2 = 5 + 2 = 7$
    $u_3 = u_2 + 2 = 7 + 2 = 9$
    $u_4 = u_3 + 2 = 9 + 2 = 11$

**Question 2 : Formule générale**
🔵 Étape 1 : Identifier le type de suite
    La suite augmente de manière constante (+2), c'est donc une suite arithmétique.

🔵 Étape 2 : Appliquer la formule d'une suite arithmétique
    $u_n = u_0 + n \\cdot r$
    Ici $r = 2$, donc $u_n = 3 + 2n$

🔵 Étape 3 : Vérification
    Pour $n = 4$, $u_4 = 3 + 2 \\cdot 4 = 11$, ce qui correspond au calcul précédent."""
        
        exercice.etapes = etapes_text
        exercice.save()
        print("Étapes mises à jour avec succès!")
        print(f"Longueur des étapes: {len(etapes_text)} caractères")
        
    except Exercice.DoesNotExist:
        print("Exercice ID 47 non trouvé")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    update_exercice_etapes()
