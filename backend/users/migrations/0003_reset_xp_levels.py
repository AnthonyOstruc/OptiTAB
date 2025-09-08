# Migration pour remettre tous les XP et niveaux à zéro
# Seuls les quiz donnent maintenant des XP

from django.db import migrations


def reset_xp_and_levels(apps, schema_editor):
    """Reset tous les XP à 0 (le champ level n'existe pas encore)"""
    CustomUser = apps.get_model('users', 'CustomUser')
    CustomUser.objects.all().update(xp=0)


def reverse_reset(apps, schema_editor):
    """Cette migration est irréversible"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_xp'),
    ]

    operations = [
        migrations.RunPython(reset_xp_and_levels, reverse_reset),
    ]
