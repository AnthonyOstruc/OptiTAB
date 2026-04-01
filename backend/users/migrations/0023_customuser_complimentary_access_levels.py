from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pays', '0003_niveau_demo_exercices_niveau_demo_notion'),
        ('users', '0022_customuser_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='complimentary_access_levels',
            field=models.ManyToManyField(
                blank=True,
                help_text=(
                    "Si des niveaux sont sélectionnés, l'accès premium offert est limité à ces niveaux. "
                    "Laisser vide pour un accès global."
                ),
                related_name='users_with_complimentary_access',
                to='pays.niveau',
                verbose_name='Niveaux premium offerts',
            ),
        ),
    ]
