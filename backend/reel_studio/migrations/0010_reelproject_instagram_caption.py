from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0009_reelslide_katex_cumulative_gap_em'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelproject',
            name='instagram_caption',
            field=models.TextField(blank=True, default=''),
        ),
    ]
