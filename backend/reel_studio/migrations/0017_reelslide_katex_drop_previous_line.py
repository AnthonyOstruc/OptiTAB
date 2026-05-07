from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0016_reelslide_katex_reveal_with_speech'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_drop_previous_line',
            field=models.BooleanField(default=False),
        ),
    ]
