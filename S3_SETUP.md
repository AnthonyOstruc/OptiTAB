# Configuration AWS S3 pour OptiTAB

Ce guide explique comment configurer AWS S3 pour stocker les images d'exercices, de quiz et de cours.

## Prérequis

1. Un compte AWS avec accès à S3
2. Un bucket S3 créé (par défaut : `optitab-media`)
3. Les permissions appropriées configurées

## Configuration Backend

### 1. Variables d'environnement

Ajoutez ces variables dans votre fichier `.env` (backend) :

```env
# Configuration AWS S3
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_STORAGE_BUCKET_NAME=optitab-media
AWS_S3_REGION_NAME=eu-west-3
AWS_S3_CUSTOM_DOMAIN=optitab-media.s3.eu-west-3.amazonaws.com
```

### 2. Installation des dépendances

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configuration Django

Le système détecte automatiquement si S3 est configuré et bascule entre le stockage local et S3 :

- **Avec S3 configuré** : Les images sont uploadées directement dans S3
- **Sans S3** : Les images sont stockées localement dans le dossier `media/`

## Configuration Frontend

### Variables d'environnement

Ajoutez cette variable dans votre fichier d'environnement frontend :

```env
VITE_S3_MEDIA_URL=https://optitab-media.s3.eu-west-3.amazonaws.com
```

Ou définissez-la dans le fichier `.env` du frontend si vous en avez un.

## Utilisation

### Upload d'images

Les images sont automatiquement uploadées vers S3 lors de :

1. **Création d'exercices** avec des images
2. **Création de quiz** avec des images
3. **Création de cours** avec des images

### Affichage des images

Les images sont automatiquement servies depuis S3 dans :

- Composant `ExerciceQCM.vue`
- Modal d'affichage d'images
- Tous les endroits où les images sont affichées

### Fonctionnement automatique

1. **Si S3 est configuré** :
   - Les nouvelles images sont uploadées dans S3
   - Les URLs S3 sont utilisées pour l'affichage
   - Les images existantes restent accessibles

2. **Si S3 n'est pas configuré** :
   - Les images sont stockées localement
   - Les URLs locales sont utilisées
   - Fonctionnement normal avec le backend Django

## Migration des images existantes

Pour migrer les images existantes vers S3, vous pouvez utiliser ce script :

```python
# Dans un script de migration
from core.utils import upload_file_to_s3
from django.core.files import File

# Exemple pour migrer les images d'exercices
from curriculum.models import ExerciceImage
import os

for img in ExerciceImage.objects.all():
    if img.image:
        # Upload vers S3
        result = upload_file_to_s3(
            img.image.read(),
            f"exercice_images/{img.image.name.split('/')[-1]}"
        )
        if result['success']:
            print(f"Image migrée: {img.image.name} -> {result['url']}")
```

## Structure des dossiers S3

Les images sont organisées dans S3 comme suit :

```
optitab-media/
├── exercice_images/
│   ├── image1.png
│   ├── image2.png
│   └── ...
├── quiz_images/
│   ├── quiz1.png
│   ├── quiz2.png
│   └── ...
└── cours_images/
    ├── cours1.png
    ├── cours2.png
    └── ...
```

## Permissions S3

Assurez-vous que votre bucket S3 a les bonnes permissions :

1. **ACL** : `public-read` pour les objets
2. **CORS** : Configuré pour votre domaine
3. **Policy** : Accès en lecture/écriture pour votre clé AWS

## Dépannage

### Images qui ne s'affichent pas

1. Vérifiez que les variables S3 sont correctement configurées
2. Vérifiez que le bucket existe et est accessible
3. Vérifiez les permissions CORS du bucket
4. Consultez les logs Django pour les erreurs d'upload

### Erreurs d'upload

1. Vérifiez les clés AWS
2. Vérifiez que le bucket existe
3. Vérifiez les permissions IAM
4. Vérifiez la configuration réseau/firewall

## Sécurité

- Ne jamais commiter les clés AWS dans le code
- Utiliser des variables d'environnement uniquement
- Configurer les permissions IAM de manière restrictive
- Activer le logging pour surveiller l'accès aux images

## Support

En cas de problème, vérifiez :
1. La configuration des variables d'environnement
2. Les logs Django
3. Les permissions AWS
4. La configuration CORS du bucket S3
