from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0008_rename_mode_to_plan_mode'),
    ]

    operations = [
        migrations.RunSQL(
            sql=
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'access_days'
                    ) THEN
                        ALTER TABLE subscriptions_subscriptionplan 
                            ADD COLUMN access_days integer NULL;
                    END IF;
                END$$;
                """,
            reverse_sql=
                """
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'access_days'
                    ) THEN
                        ALTER TABLE subscriptions_subscriptionplan 
                            DROP COLUMN access_days;
                    END IF;
                END$$;
                """,
        ),
    ]


