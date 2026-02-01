#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
try:
    django.setup()
    print("✅ Django setup successful")

    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ Database connection successful")

    # Check for images
    from curriculum.models import ExerciceImage
    count = ExerciceImage.objects.count()
    print(f"📊 Found {count} ExerciceImage records in database")

    if count > 0:
        # Show first few images
        images = ExerciceImage.objects.all()[:5]
        for img in images:
            print(f"  - ID {img.id}: {img.image.name if img.image else 'No image'}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
