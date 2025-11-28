from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0014_exercice_exercice_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercice',
            name='exercice_type',
        ),
        migrations.RemoveField(
            model_name='exercice',
            name='points',
        ),
        migrations.RemoveField(
            model_name='exercice',
            name='ordre',
        ),
        migrations.AlterModelOptions(
            name='exercice',
            options={
                'ordering': ['notion', 'titre', 'id'],
                'verbose_name': 'Exercice',
                'verbose_name_plural': 'Exercices',
            },
        ),
        migrations.AlterUniqueTogether(
            name='exercice',
            unique_together={('notion', 'titre')},
        ),
    ]
