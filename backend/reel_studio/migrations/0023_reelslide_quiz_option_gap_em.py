from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0022_reelslide_generated_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='quiz_option_gap_em',
            field=models.FloatField(default=0.4),
        ),
    ]
