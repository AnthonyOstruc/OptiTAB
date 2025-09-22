"""
Fonctions utilitaires pour la gestion des fichiers S3 et des images
"""
import os
import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)


def upload_file_to_s3(file_content, filename, content_type=None):
    """
    Upload un fichier vers S3

    Args:
        file_content: Contenu du fichier (bytes ou string)
        filename: Nom du fichier
        content_type: Type MIME du fichier (optionnel)

    Returns:
        dict: {'success': bool, 'url': str, 'error': str}
    """
    try:
        # Vérifier si S3 est configuré
        if not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not settings.AWS_ACCESS_KEY_ID:
            logger.warning("S3 non configuré, utilisation du stockage local")
            return {'success': False, 'error': 'S3 non configuré'}

        # Créer le client S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Upload vers S3
        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')

        s3_client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=filename,
            Body=file_content,
            ACL='public-read',
            ContentType=content_type or 'application/octet-stream'
        )

        # Construire l'URL
        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN') and settings.AWS_S3_CUSTOM_DOMAIN:
            url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
        else:
            url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"

        return {'success': True, 'url': url}

    except Exception as e:
        logger.error(f"Erreur upload S3: {str(e)}")
        return {'success': False, 'error': str(e)}


def upload_image_from_base64(base64_data, filename):
    """
    Upload une image encodée en base64 vers S3

    Args:
        base64_data: Données base64 (avec ou sans préfixe data:image/...)
        filename: Nom du fichier

    Returns:
        dict: {'success': bool, 'url': str, 'error': str}
    """
    try:
        # Extraire les données base64 si nécessaire
        if base64_data.startswith('data:'):
            # Format: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...
            header, base64_content = base64_data.split(',', 1)
            content_type = header.split(';')[0].replace('data:', '')
        else:
            base64_content = base64_data
            content_type = 'image/png'  # fallback

        # Décoder base64
        import base64
        file_content = base64.b64decode(base64_content)

        return upload_file_to_s3(file_content, filename, content_type)

    except Exception as e:
        logger.error(f"Erreur upload image base64: {str(e)}")
        return {'success': False, 'error': str(e)}


def delete_file_from_s3(filename):
    """
    Supprime un fichier de S3

    Args:
        filename: Nom du fichier (key dans S3)

    Returns:
        dict: {'success': bool, 'error': str}
    """
    try:
        # Vérifier si S3 est configuré
        if not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not settings.AWS_ACCESS_KEY_ID:
            logger.warning("S3 non configuré")
            return {'success': False, 'error': 'S3 non configuré'}

        # Créer le client S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Supprimer le fichier
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=filename
        )

        return {'success': True}

    except Exception as e:
        logger.error(f"Erreur suppression S3: {str(e)}")
        return {'success': False, 'error': str(e)}


def get_s3_url(filename):
    """
    Génère l'URL S3 pour un fichier

    Args:
        filename: Nom du fichier

    Returns:
        str: URL du fichier sur S3
    """
    if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN') and settings.AWS_S3_CUSTOM_DOMAIN:
        return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{filename}"
    else:
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"


def is_s3_configured():
    """
    Vérifie si S3 est configuré

    Returns:
        bool: True si S3 est configuré
    """
    return (hasattr(settings, 'AWS_ACCESS_KEY_ID') and
            settings.AWS_ACCESS_KEY_ID and
            hasattr(settings, 'AWS_SECRET_ACCESS_KEY') and
            settings.AWS_SECRET_ACCESS_KEY)
