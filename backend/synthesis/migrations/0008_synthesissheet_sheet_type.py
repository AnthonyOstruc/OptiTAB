# Generated manually for sheet_type support
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthesis', '0007_synthesissheet_visibility_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='synthesissheet',
            name='sheet_type',
            field=models.CharField(
                choices=[('summary', 'Fiche de synthese'), ('table', 'Tableau & Formules')],
                db_index=True,
                default='summary',
                help_text='Definit le type de fiche (synthese ou tableau/formules).',
                max_length=10,
            ),
        ),
        migrations.AlterUniqueTogether(
            name='synthesissheet',
            unique_together={('notion', 'titre', 'sheet_type')},
        ),
    ]
