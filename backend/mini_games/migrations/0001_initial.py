import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MathRunScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('category', models.CharField(
                    choices=[
                        ('all', 'Mixte'),
                        ('addition', 'Addition'),
                        ('subtraction', 'Soustraction'),
                        ('multiplication', 'Multiplication'),
                        ('division', 'Division'),
                    ],
                    default='all',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='math_run_scores',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-score', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='mathrunscore',
            index=models.Index(fields=['user', 'category'], name='mr_score_user_cat_idx'),
        ),
        migrations.AddIndex(
            model_name='mathrunscore',
            index=models.Index(fields=['-score'], name='mr_score_score_idx'),
        ),
    ]
