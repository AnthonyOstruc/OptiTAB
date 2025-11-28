from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0015_remove_exercice_points_type_and_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciceimage',
            name='image_type',
        ),
        migrations.RemoveField(
            model_name='exerciceimage',
            name='legende',
        ),
    ]
