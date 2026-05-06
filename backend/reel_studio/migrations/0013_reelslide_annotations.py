from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0012_reelslide_katex_inline_separator_none'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='annotations',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
