from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pays', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='niveau',
            name='exercice_filter_default',
            field=models.CharField(blank=True, default='Tous', max_length=120),
        ),
        migrations.AddField(
            model_name='niveau',
            name='exercice_filter_options',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
