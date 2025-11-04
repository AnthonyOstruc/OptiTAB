from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0009_alter_exercice_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matiere',
            name='show_on_home',
            field=models.BooleanField(default=True, verbose_name="Afficher sur la page d'accueil"),
        ),
    ]

