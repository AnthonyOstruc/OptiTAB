from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0024_reelproject_carousel_colors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reelslide',
            name='quiz_option_gap_em',
            field=models.FloatField(default=0.7),
        ),
    ]
