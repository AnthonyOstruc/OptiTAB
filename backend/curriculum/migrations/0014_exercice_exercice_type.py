from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0013_add_exercice_access_scope'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercice',
            name='exercice_type',
            field=models.CharField(blank=True, default='', max_length=120, verbose_name="Type d'exercice"),
        ),
    ]
