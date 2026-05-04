from django.db import migrations, models

import reel_studio.models


class Migration(migrations.Migration):

    dependencies = [
        ('reel_studio', '0006_reelslide_speech_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelproject',
            name='video_file',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=reel_studio.models.reel_project_video_upload_to,
            ),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='video_status',
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
            name='video_error',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='video_generated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='video_width',
            field=models.PositiveIntegerField(default=1080),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='video_height',
            field=models.PositiveIntegerField(default=1920),
        ),
        migrations.AddField(
            model_name='reelproject',
            name='video_fps',
            field=models.PositiveIntegerField(default=30),
        ),
    ]
