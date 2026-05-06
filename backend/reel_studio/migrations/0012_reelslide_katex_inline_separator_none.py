from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0011_reelslide_katex_inline_separator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reelslide',
            name='katex_inline_separator',
            field=models.CharField(
                choices=[
                    ('semicolon', 'Semicolon'),
                    ('arrow', 'Arrow'),
                    ('none', 'None'),
                ],
                default='semicolon',
                max_length=16,
            ),
        ),
    ]
