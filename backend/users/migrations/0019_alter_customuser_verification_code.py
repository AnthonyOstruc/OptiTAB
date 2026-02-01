from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_parentchild_responded_at_parentchild_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
