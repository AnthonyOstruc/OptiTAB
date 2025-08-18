# Generated manually for SuiviQuiz gamification

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suivis', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='suiviquiz',
            name='tentative_numero',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='suiviquiz',
            name='xp_gagne',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='suiviquiz',
            unique_together={('user', 'quiz', 'tentative_numero')},
        ),
    ]
