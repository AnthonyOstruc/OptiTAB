from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0013_add_weekly_billing_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='stripe_invoice_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='hosted_invoice_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='invoice_pdf_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]
