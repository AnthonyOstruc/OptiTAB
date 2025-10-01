#!/usr/bin/env python3
"""
Script de migration des images existantes vers S3
"""
import os
import sys
import django
from pathlib import Path
import argparse

# Configuration Django
sys.path.append(str(Path(__file__).parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

try:
    django.setup()
except Exception as e:
    print(f"Erreur Django setup: {e}")
    sys.exit(1)

from curriculum.models import ExerciceImage
from quiz.models import QuizImage
from cours.models import CoursImage, Cours
from core.utils import upload_file_to_s3, is_s3_configured
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_exercice_images():
    """Migre les images d'exercices vers S3"""
    print("=== Migration des images d'exercices ===")

    if not is_s3_configured():
        print("❌ S3 n'est pas configuré. Migration impossible.")
        return False

    migrated = 0
    failed = 0

    for img in ExerciceImage.objects.all():
        try:
            if img.image and img.image.path:
                print(f"Migration: {img.image.name}")

                # Lire le contenu du fichier
                with open(img.image.path, 'rb') as f:
                    file_content = f.read()

                # Déterminer le type MIME
                content_type = None
                if img.image.name.lower().endswith('.png'):
                    content_type = 'image/png'
                elif img.image.name.lower().endswith('.jpg') or img.image.name.lower().endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif img.image.name.lower().endswith('.gif'):
                    content_type = 'image/gif'

                # Upload vers S3
                result = upload_file_to_s3(
                    file_content,
                    f"exercice_images/{img.image.name.split('/')[-1]}",
                    content_type
                )

                if result['success']:
                    print(f"  ✅ Migré vers: {result['url']}")
                    migrated += 1
                else:
                    print(f"  ❌ Erreur: {result['error']}")
                    failed += 1

        except Exception as e:
            print(f"  ❌ Erreur lors de la migration: {e}")
            failed += 1

    print(f"Images d'exercices: {migrated} migrées, {failed} erreurs")
    return migrated > 0


def migrate_quiz_images():
    """Migre les images de quiz vers S3"""
    print("\n=== Migration des images de quiz ===")

    if not is_s3_configured():
        print("❌ S3 n'est pas configuré. Migration impossible.")
        return False

    migrated = 0
    failed = 0

    for img in QuizImage.objects.all():
        try:
            if img.image and img.image.path:
                print(f"Migration: {img.image.name}")

                with open(img.image.path, 'rb') as f:
                    file_content = f.read()

                content_type = None
                if img.image.name.lower().endswith('.png'):
                    content_type = 'image/png'
                elif img.image.name.lower().endswith('.jpg') or img.image.name.lower().endswith('.jpeg'):
                    content_type = 'image/jpeg'

                result = upload_file_to_s3(
                    file_content,
                    f"quiz_images/{img.image.name.split('/')[-1]}",
                    content_type
                )

                if result['success']:
                    print(f"  ✅ Migré vers: {result['url']}")
                    migrated += 1
                else:
                    print(f"  ❌ Erreur: {result['error']}")
                    failed += 1

        except Exception as e:
            print(f"  ❌ Erreur lors de la migration: {e}")
            failed += 1

    print(f"Images de quiz: {migrated} migrées, {failed} erreurs")
    return migrated > 0


def migrate_cours_images():
    """Migre les images de cours vers S3"""
    print("\n=== Migration des images de cours ===")

    if not is_s3_configured():
        print("❌ S3 n'est pas configuré. Migration impossible.")
        return False

    migrated = 0
    failed = 0

    for img in CoursImage.objects.all():
        try:
            if img.image and img.image.path:
                print(f"Migration: {img.image.name}")

                with open(img.image.path, 'rb') as f:
                    file_content = f.read()

                content_type = None
                if img.image.name.lower().endswith('.png'):
                    content_type = 'image/png'
                elif img.image.name.lower().endswith('.jpg') or img.image.name.lower().endswith('.jpeg'):
                    content_type = 'image/jpeg'

                result = upload_file_to_s3(
                    file_content,
                    f"cours_images/{img.image.name.split('/')[-1]}",
                    content_type
                )

                if result['success']:
                    print(f"  ✅ Migré vers: {result['url']}")
                    migrated += 1
                else:
                    print(f"  ❌ Erreur: {result['error']}")
                    failed += 1

        except Exception as e:
            print(f"  ❌ Erreur lors de la migration: {e}")
            failed += 1

    print(f"Images de cours: {migrated} migrées, {failed} erreurs")
    return migrated > 0


def migrate_cours_pdfs():
    """Migre les PDF des cours vers S3"""
    print("\n=== Migration des PDF de cours ===")

    if not is_s3_configured():
        print("❌ S3 n'est pas configuré. Migration impossible.")
        return False

    migrated = 0
    failed = 0

    for cours in Cours.objects.all():
        try:
            pdf_field = getattr(cours, 'pdf_file', None)
            if pdf_field and getattr(pdf_field, 'path', None):
                print(f"Migration: {pdf_field.name}")

                with open(pdf_field.path, 'rb') as f:
                    file_content = f.read()

                # Forcer le type MIME PDF
                content_type = 'application/pdf'

                # Conserver la clé existante (ex: cours_pdfs/monfichier.pdf)
                result = upload_file_to_s3(
                    file_content,
                    pdf_field.name,
                    content_type
                )

                if result['success']:
                    print(f"  ✅ Migré vers: {result['url']}")
                    migrated += 1
                else:
                    print(f"  ❌ Erreur: {result['error']}")
                    failed += 1

        except Exception as e:
            print(f"  ❌ Erreur lors de la migration: {e}")
            failed += 1

    print(f"PDF de cours: {migrated} migrés, {failed} erreurs")
    return migrated > 0


def main():
    """Fonction principale"""
    print("Migration des images vers S3")
    print("=" * 40)

    if not is_s3_configured():
        print("❌ Configuration S3 manquante.")
        print("Veuillez configurer les variables d'environnement AWS.")
        return

    # Arguments CLI
    parser = argparse.ArgumentParser(description="Migrer les médias existants vers S3")
    parser.add_argument('-y', '--yes', action='store_true', help="Confirmer sans demander")
    args = parser.parse_args()

    # Demander confirmation si nécessaire
    if not args.yes:
        print("⚠️  Cette opération va migrer toutes les images et PDF existants vers S3.")
        print("   Assurez-vous que S3 est correctement configuré.")
        print("   Les fichiers locaux ne seront pas supprimés.")
        print()
        confirm = input("Voulez-vous continuer? (y/N): ")
        if confirm.lower() != 'y':
            print("Migration annulée.")
            return

    # Migrer les images
    success = False
    success |= migrate_exercice_images()
    success |= migrate_quiz_images()
    success |= migrate_cours_images()
    success |= migrate_cours_pdfs()

    print("\n" + "=" * 40)
    if success:
        print("✅ Migration terminée avec succès!")
        print("   Les images sont maintenant disponibles sur S3.")
        print("   Le système utilisera automatiquement les URLs S3.")
    else:
        print("❌ Aucune image migrée ou toutes les migrations ont échoué.")


if __name__ == "__main__":
    main()
