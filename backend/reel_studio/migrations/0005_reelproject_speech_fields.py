from django.db import migrations, models

import reel_studio.models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0004_reelslide_katex_reset_cumulative'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelproject',
            name='speech_audio',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=reel_studio.models.reel_project_speech_upload_to,
            ),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_voice_id',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_model_id',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_output_format',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_status',
            field=models.CharField(
                choices=[
                    ('empty', 'Empty'),
                    ('ready', 'Ready'),
                    ('error', 'Error'),
                ],
                default='empty',
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_error',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='speech_generated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
