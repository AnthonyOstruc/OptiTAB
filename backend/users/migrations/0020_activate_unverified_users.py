from django.db import migrations


def activate_unverified_accounts(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')
    CustomUser.objects.filter(is_active=False, verification_code__isnull=False).update(is_active=True)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_customuser_verification_code'),
    ]

    operations = [
        migrations.RunPython(activate_unverified_accounts, noop),
    ]
