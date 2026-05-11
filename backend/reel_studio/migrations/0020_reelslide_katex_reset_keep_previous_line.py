from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0019_reelslide_katex_inline_vertical_offset_em'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_reset_keep_previous_line',
            field=models.BooleanField(default=True),
        ),
    ]
