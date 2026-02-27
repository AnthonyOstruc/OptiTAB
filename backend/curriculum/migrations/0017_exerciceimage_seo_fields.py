from django.db import migrations, models
import django.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0016_remove_exerciceimage_image_type_legende'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciceimage',
            name='alt_text',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='exerciceimage',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exerciceimage',
            name='legende',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='exerciceimage',
            name='title_text',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='exerciceimage',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='exerciceimage',
            constraint=models.UniqueConstraint(
                condition=django.db.models.Q(position__isnull=False),
                fields=('exercice', 'position'),
                name='unique_exerciceimage_position_per_exercice',
            ),
        ),
    ]
