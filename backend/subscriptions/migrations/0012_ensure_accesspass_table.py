from django.db import migrations


def create_access_pass_table(apps, schema_editor):
    """Ensure subscriptions_accesspass exists (was missing on some DBs)."""
    AccessPass = apps.get_model('subscriptions', 'AccessPass')
    connection = schema_editor.connection
    existing_tables = connection.introspection.table_names()
    if AccessPass._meta.db_table in existing_tables:
        return
    schema_editor.create_model(AccessPass)


def drop_access_pass_table(apps, schema_editor):
    """Reverse: drop table if we created it."""
    AccessPass = apps.get_model('subscriptions', 'AccessPass')
    connection = schema_editor.connection
    existing_tables = connection.introspection.table_names()
    if AccessPass._meta.db_table not in existing_tables:
        return
    schema_editor.delete_model(AccessPass)


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0011_alter_subscriptionplan_billing_period'),
    ]

    operations = [
        migrations.RunPython(create_access_pass_table, drop_access_pass_table),
    ]

