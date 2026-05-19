from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0023_reelslide_quiz_option_gap_em'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelproject',
            name='carousel_title_color',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='carousel_text_color',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]
