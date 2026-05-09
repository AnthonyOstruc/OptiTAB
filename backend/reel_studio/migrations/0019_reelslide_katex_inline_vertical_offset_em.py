from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0018_reelproject_pronunciation_overrides_by_voice'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_inline_vertical_offset_em',
            field=models.FloatField(default=0.0),
        ),
    ]
