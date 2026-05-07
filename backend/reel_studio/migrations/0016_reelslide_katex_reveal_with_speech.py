from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0015_reelslide_speech_word_timings'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_reveal_with_speech',
            field=models.BooleanField(default=False),
        ),
    ]
