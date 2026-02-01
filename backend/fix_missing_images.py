#!/usr/bin/env python
"""
Script pour corriger automatiquement les images manquantes en production.
Copie les fichiers de base vers les noms attendus par la base de données.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from curriculum.models import ExerciceImage

def fix_missing_images():
    """Corrige automatiquement les images manquantes"""
    print("🔧 Correction automatique des images manquantes...")

    all_images = ExerciceImage.objects.all()
    fixed_count = 0

    for img in all_images:
        if not img.image:
            continue

        filename = os.path.basename(img.image.name)
        filepath = img.image.path

        # Si le fichier n'existe pas
        if not os.path.exists(filepath):
            print(f"❌ Image manquante: {filename}")

            # Chercher le fichier de base (sans suffix)
            base_name = filename.rsplit('_', 1)[0] + '.png' if '_' in filename else filename
            base_path = os.path.join(os.path.dirname(filepath), base_name)

            if os.path.exists(base_path):
                print(f"  📁 Fichier de base trouvé: {base_name}")
                print(f"  🔄 Copie vers: {filename}")

                # Copier le fichier de base vers le nom attendu
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(base_path, 'rb') as src, open(filepath, 'wb') as dst:
                    dst.write(src.read())

                # Copier aussi vers le répertoire media racine pour la production
                root_media_path = os.path.join('..', 'media', 'exercice_images', filename)
                os.makedirs(os.path.dirname(root_media_path), exist_ok=True)
                with open(base_path, 'rb') as src, open(root_media_path, 'wb') as dst:
                    dst.write(src.read())

                fixed_count += 1
                print(f"  ✅ Corrigé: {filename}")
            else:
                print(f"  ⚠️  Fichier de base non trouvé: {base_name}")
        else:
            print(f"✅ {filename} - OK")

    print(f"\n📊 Résumé: {fixed_count} images corrigées")
    return fixed_count

if __name__ == "__main__":
    fix_missing_images()
