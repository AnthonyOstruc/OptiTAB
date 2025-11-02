from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_customuser_login_streak_count_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name = 'users_customuser'
                          AND column_name = 'streak'
                    ) THEN
                        ALTER TABLE users_customuser DROP COLUMN streak;
                    END IF;
                END $$;
            """,
            reverse_sql="""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name = 'users_customuser'
                          AND column_name = 'streak'
                    ) THEN
                        ALTER TABLE users_customuser
                        ADD COLUMN streak integer NOT NULL DEFAULT 0;
                    END IF;
                END $$;
            """,
        ),
    ]

