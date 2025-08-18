#!/usr/bin/env python
"""
Script pour lister les exercices et mettre à jour leurs étapes
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from curriculum.models import Exercice

def list_and_update_exercices():
    # Lister tous les exercices
    exercices = Exercice.objects.all()
    print(f"Nombre d'exercices trouvés: {exercices.count()}")
    
    for exercice in exercices:
        print(f"ID: {exercice.id} - Titre: {exercice.titre}")
        print(f"  Question: {exercice.question[:100]}...")
        print(f"  Étapes actuelles: {exercice.etapes}")
        print("---")
    
    # Mettre à jour le premier exercice de suites arithmétiques
    exercice_suite = exercices.filter(titre__icontains="suite arithmétique").first()
    if exercice_suite:
        print(f"\nMise à jour de l'exercice: {exercice_suite.titre} (ID: {exercice_suite.id})")
        
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
        
        exercice_suite.etapes = etapes_text
        exercice_suite.save()
        print("✅ Étapes mises à jour avec succès!")
    else:
        print("Aucun exercice de suite arithmétique trouvé")

if __name__ == "__main__":
    list_and_update_exercices()
