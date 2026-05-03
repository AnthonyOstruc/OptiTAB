from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_taxonomies_fk'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Cree le')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Modifie le')),
                ('image', models.ImageField(upload_to='blog/content/%Y/%m/', verbose_name='Image')),
                ('position', models.PositiveIntegerField(default=1, verbose_name='Position')),
                ('align', models.CharField(choices=[('center', 'Centree'), ('left', 'Gauche'), ('right', 'Droite'), ('full', 'Pleine largeur')], default='center', max_length=20, verbose_name='Alignement')),
                ('width_percent', models.PositiveIntegerField(default=100, verbose_name='Largeur (%)')),
                ('alt_text', models.CharField(blank=True, default='', max_length=250, verbose_name='Texte alternatif')),
                ('caption', models.CharField(blank=True, default='', max_length=300, verbose_name='Legende')),
                ('title_text', models.CharField(blank=True, default='', max_length=160, verbose_name='Titre image')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.blogpost', verbose_name='Article')),
            ],
            options={
                'verbose_name': "Image d'article",
                'verbose_name_plural': "Images d'articles",
                'ordering': ['position', 'id'],
            },
        ),
    ]
