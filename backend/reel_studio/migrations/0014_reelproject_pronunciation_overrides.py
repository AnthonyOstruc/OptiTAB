from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0013_reelslide_annotations'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelproject',
            name='pronunciation_overrides',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
