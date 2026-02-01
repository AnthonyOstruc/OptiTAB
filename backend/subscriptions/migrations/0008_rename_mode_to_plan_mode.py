from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_rename_subscriptions_user_end_idx_subscriptio_user_id_0cd826_idx'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=
                        """
                        DO $$
                        BEGIN
                            IF NOT EXISTS (
                                SELECT 1 FROM information_schema.columns 
                                WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'plan_mode'
                            ) AND EXISTS (
                                SELECT 1 FROM information_schema.columns 
                                WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'mode'
                            ) THEN
                                ALTER TABLE subscriptions_subscriptionplan RENAME COLUMN mode TO plan_mode;
                            ELSIF NOT EXISTS (
                                SELECT 1 FROM information_schema.columns 
                                WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'plan_mode'
                            ) THEN
                                ALTER TABLE subscriptions_subscriptionplan 
                                    ADD COLUMN plan_mode varchar(20) NOT NULL DEFAULT 'subscription';
                                ALTER TABLE subscriptions_subscriptionplan 
                                    ALTER COLUMN plan_mode DROP DEFAULT;
                            END IF;
                        END$$;
                        """,
                    reverse_sql=
                        """
                        DO $$
                        BEGIN
                            IF NOT EXISTS (
                                SELECT 1 FROM information_schema.columns 
                                WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'mode'
                            ) AND EXISTS (
                                SELECT 1 FROM information_schema.columns 
                                WHERE table_name = 'subscriptions_subscriptionplan' AND column_name = 'plan_mode'
                            ) THEN
                                ALTER TABLE subscriptions_subscriptionplan RENAME COLUMN plan_mode TO mode;
                            END IF;
                        END$$;
                        """,
                ),
            ],
            state_operations=[
                migrations.RenameField(
                    model_name='subscriptionplan',
                    old_name='mode',
                    new_name='plan_mode',
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name='subscriptionplan',
            constraint=models.UniqueConstraint(
                fields=['plan_type', 'billing_period', 'plan_mode'],
                name='subscriptionplan_unique_pt_bp_planmode',
            ),
        ),
    ]


