from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0017_reelslide_katex_drop_previous_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelproject',
            name='pronunciation_overrides_by_voice',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
