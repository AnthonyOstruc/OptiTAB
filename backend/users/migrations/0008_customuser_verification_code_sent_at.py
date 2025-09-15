from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_customuser_users_custo_email_1a70ed_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='verification_code_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]


