from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_paymenthistory_invoice_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='cancel_at_period_end',
            field=models.BooleanField(default=False),
        ),
    ]
