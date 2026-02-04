from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_customuser_pending_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
