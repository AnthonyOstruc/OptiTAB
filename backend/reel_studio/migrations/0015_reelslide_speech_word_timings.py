from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0014_reelproject_pronunciation_overrides'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='speech_word_timings',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
