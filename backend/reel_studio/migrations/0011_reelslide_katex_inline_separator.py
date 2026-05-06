from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0010_reelproject_instagram_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelslide',
            name='katex_inline_separator',
            field=models.CharField(
                choices=[
                    ('semicolon', 'Semicolon'),
                    ('arrow', 'Arrow'),
                ],
                default='semicolon',
                max_length=16,
            ),
        ),
    ]
