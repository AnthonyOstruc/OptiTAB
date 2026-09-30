from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('reel_studio', '0025_alter_reelslide_quiz_option_gap_em_default')]

    operations = [
        migrations.AddField(
            model_name='reelproject', name='batch_id',
            field=models.UUIDField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='reelproject', name='batch_title',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='reelproject', name='batch_order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
