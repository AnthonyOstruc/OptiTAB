#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from curriculum.models import ExerciceImage

def find_missing_images():
    """Trouve toutes les images référencées en DB mais manquantes physiquement"""
    print("🔍 Recherche des images manquantes...")

    # Récupérer toutes les images de la DB
    all_images = ExerciceImage.objects.all()

    missing_files = []
    existing_files = []

    for img in all_images:
        if img.image:  # Vérifier qu'il y a bien un chemin d'image
            # Extraire le nom du fichier du chemin complet
            filename = os.path.basename(img.image.name)
            filepath = img.image.path

            if os.path.exists(filepath):
                existing_files.append(filename)
                print(f"✅ {filename} - EXISTS")
            else:
                missing_files.append(filename)
                print(f"❌ {filename} - MISSING")

    print("
📊 Résumé:"    print(f"Total images en DB: {len(all_images)}")
    print(f"Images existantes: {len(existing_files)}")
    print(f"Images manquantes: {len(missing_files)}")

    if missing_files:
        print("
🛠️  Fichiers manquants:"        for filename in missing_files:
            print(f"  - {filename}")

        # Chercher le fichier de base sans suffix
        print("
🔧 Recherche des fichiers de base disponibles..."        base_files = []
        for filename in missing_files:
            # Supprimer le suffix (tout après le dernier underscore avant .png)
            if '_' in filename and '.png' in filename:
                base_name = filename.rsplit('_', 1)[0] + '.png'
                base_path = f"media/exercice_images/{base_name}"
                if os.path.exists(base_path):
                    print(f"  📁 Base file found: {base_name} -> {filename}")
                    base_files.append((base_name, filename))

        return base_files

    return []

if __name__ == "__main__":
    find_missing_images()
