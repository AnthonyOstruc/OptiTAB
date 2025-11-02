from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0012_ensure_accesspass_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='billing_period',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('daily', 'Journalier'),
                    ('weekly', 'Hebdomadaire'),
                    ('monthly', 'Mensuel'),
                    ('yearly', 'Annuel'),
                ],
            ),
        ),
    ]

