from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0019_paymenthistory_plan_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='period_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paymenthistory',
            name='period_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
