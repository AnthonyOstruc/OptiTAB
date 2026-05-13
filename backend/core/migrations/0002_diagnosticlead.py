from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticLead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Créé le')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Modifié le')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, default='', max_length=120, verbose_name='Prénom')),
                ('level', models.CharField(choices=[('college', 'Collège'), ('seconde', 'Seconde'), ('premiere', 'Première'), ('terminale', 'Terminale'), ('prepa', 'Prépa'), ('bts', 'BTS'), ('parent', 'Parent')], db_index=True, max_length=20, verbose_name='Niveau')),
                ('difficulty', models.CharField(choices=[('cours_vs_exercices', 'Comprend le cours mais pas les exercices'), ('organisation', 'Organisation / révision'), ('methode', 'Pas de méthode claire'), ('bac', 'Préparation Bac'), ('motivation', 'Motivation')], db_index=True, max_length=30, verbose_name='Difficulté principale')),
                ('consent_email_marketing', models.BooleanField(default=False, verbose_name='Consentement marketing email')),
                ('consent_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Timestamp de consentement')),
                ('consent_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP de consentement')),
                ('form_location', models.CharField(choices=[('hero', 'Hero'), ('main', 'Formulaire principal'), ('final', 'CTA final')], default='main', max_length=20, verbose_name='Emplacement formulaire')),
                ('lead_magnet', models.CharField(default='diagnostic_maths', max_length=60, verbose_name='Lead magnet')),
                ('landing_path', models.CharField(blank=True, default='', max_length=255, verbose_name="Page d'atterrissage")),
                ('referrer', models.URLField(blank=True, default='', max_length=500, verbose_name='Referrer')),
                ('utm_source', models.CharField(blank=True, default='', max_length=100, verbose_name='utm_source')),
                ('utm_medium', models.CharField(blank=True, default='', max_length=100, verbose_name='utm_medium')),
                ('utm_campaign', models.CharField(blank=True, default='', max_length=100, verbose_name='utm_campaign')),
                ('utm_content', models.CharField(blank=True, default='', max_length=100, verbose_name='utm_content')),
                ('utm_term', models.CharField(blank=True, default='', max_length=100, verbose_name='utm_term')),
                ('gclid', models.CharField(blank=True, default='', max_length=255, verbose_name='gclid')),
                ('fbclid', models.CharField(blank=True, default='', max_length=255, verbose_name='fbclid')),
                ('ttclid', models.CharField(blank=True, default='', max_length=255, verbose_name='ttclid')),
                ('msclkid', models.CharField(blank=True, default='', max_length=255, verbose_name='msclkid')),
                ('diagnostic_sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Diagnostic envoyé le')),
                ('linked_subscriber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diagnostic_leads', to='core.newslettersubscriber', verbose_name='Abonné newsletter associé')),
            ],
            options={
                'verbose_name': 'Lead diagnostic',
                'verbose_name_plural': 'Leads diagnostic',
                'ordering': ['-date_creation'],
                'indexes': [
                    models.Index(fields=['email', '-date_creation'], name='core_diagno_email_286056_idx'),
                    models.Index(fields=['level', 'difficulty'], name='core_diagno_level_a97d3c_idx'),
                    models.Index(fields=['utm_source', 'utm_campaign'], name='core_diagno_utm_sou_27489b_idx'),
                ],
            },
        ),
    ]
