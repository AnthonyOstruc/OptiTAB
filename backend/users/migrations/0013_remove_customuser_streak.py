from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_customuser_streak'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='streak',
        ),
    ]


