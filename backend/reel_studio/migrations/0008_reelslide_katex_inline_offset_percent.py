from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0007_reelproject_video_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_inline_offset_percent',
            field=models.FloatField(default=0.0),
        ),
    ]
