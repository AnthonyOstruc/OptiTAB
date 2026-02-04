from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0020_paymenthistory_period_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
