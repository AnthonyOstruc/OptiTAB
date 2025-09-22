#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from curriculum.models import ExerciceImage

def check_images():
    print("Checking for hero-illustration images in database...")
    images = ExerciceImage.objects.filter(image__icontains='hero-illustration')

    if not images:
        print("No images found with 'hero-illustration' in filename")
        return

    for img in images:
        print(f"ID: {img.id}")
        print(f"Image field: {img.image}")
        print(f"Image URL: {img.image.url}")
        print(f"Image path: {img.image.path}")
        print(f"File exists: {os.path.exists(img.image.path)}")
        print("---")

if __name__ == "__main__":
    check_images()
