from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mathrunscore',
            name='category',
            field=models.CharField(
                choices=[
                    ('all',            'Mixte'),
                    ('addition',       'Addition'),
                    ('subtraction',    'Soustraction'),
                    ('multiplication', 'Multiplication'),
                    ('division',       'Division'),
                    ('limits',         'Limites'),
                    ('derivatives',    'Dérivées'),
                    ('integrals',      'Intégrales'),
                    ('sequences',      'Suites'),
                ],
                default='all',
                max_length=20,
            ),
        ),
    ]
