from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0008_reelslide_katex_inline_offset_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_cumulative_gap_em',
            field=models.FloatField(default=0.4),
        ),
    ]
