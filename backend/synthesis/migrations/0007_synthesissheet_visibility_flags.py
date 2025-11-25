from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthesis', '0006_synthesissheet_access_scope'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='synthesissheet',
                    name='show_on_home',
                    field=models.BooleanField(
                        default=False,
                        verbose_name="Mettre en avant sur l'accueil",
                        help_text="Active l'affichage de cette fiche sur la page d'accueil.",
                    ),
                ),
                migrations.AddField(
                    model_name='synthesissheet',
                    name='show_on_public_site',
                    field=models.BooleanField(
                        default=True,
                        verbose_name='Visible sur le site public',
                        help_text='Permet de masquer une fiche tout en la conservant en base.',
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE synthesis_synthesissheet
                        ADD COLUMN IF NOT EXISTS show_on_home BOOLEAN NOT NULL DEFAULT FALSE;
                    """,
                    reverse_sql="""
                        ALTER TABLE synthesis_synthesissheet
                        DROP COLUMN IF EXISTS show_on_home;
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE synthesis_synthesissheet
                        ADD COLUMN IF NOT EXISTS show_on_public_site BOOLEAN NOT NULL DEFAULT TRUE;
                    """,
                    reverse_sql="""
                        ALTER TABLE synthesis_synthesissheet
                        DROP COLUMN IF EXISTS show_on_public_site;
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE synthesis_synthesissheet
                        ALTER COLUMN show_on_home SET DEFAULT FALSE;
                    """,
                    reverse_sql="""
                        ALTER TABLE synthesis_synthesissheet
                        ALTER COLUMN show_on_home DROP DEFAULT;
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE synthesis_synthesissheet
                        ALTER COLUMN show_on_public_site SET DEFAULT TRUE;
                    """,
                    reverse_sql="""
                        ALTER TABLE synthesis_synthesissheet
                        ALTER COLUMN show_on_public_site DROP DEFAULT;
                    """,
                ),
            ],
        ),
    ]
