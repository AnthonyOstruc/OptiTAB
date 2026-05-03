from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogpostimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostRelatedLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Cree le')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Modifie le')),
                ('titre', models.CharField(max_length=220, verbose_name='Titre du lien')),
                ('url', models.CharField(max_length=500, verbose_name='URL')),
                ('description', models.CharField(blank=True, default='', max_length=260, verbose_name='Description')),
                ('ordre', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liens_lies', to='blog.blogpost', verbose_name='Article')),
            ],
            options={
                'verbose_name': 'Lien recommande',
                'verbose_name_plural': 'Liens recommandes',
                'ordering': ['ordre', 'id'],
            },
        ),
    ]
