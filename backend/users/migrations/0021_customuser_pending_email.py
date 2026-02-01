from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_activate_unverified_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pending_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pending_email_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='pending_email_token',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
