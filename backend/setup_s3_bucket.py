#!/usr/bin/env python3
"""
Script pour créer et configurer le bucket S3 optitab-media
"""
import os
import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region):
    """Créer un bucket S3"""
    try:
        # Créer le client S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=region
        )
        
        # Créer le bucket
        if region == 'us-east-1':
            # us-east-1 ne nécessite pas de paramètre LocationConstraint
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        print(f"✅ Bucket '{bucket_name}' créé avec succès dans la région '{region}'")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists':
            print(f"ℹ️ Bucket '{bucket_name}' existe déjà")
            return True
        elif error_code == 'BucketAlreadyOwnedByYou':
            print(f"ℹ️ Bucket '{bucket_name}' vous appartient déjà")
            return True
        else:
            print(f"❌ Erreur lors de la création du bucket: {e}")
            return False

def configure_bucket_policy(bucket_name):
    """Configurer la politique du bucket pour l'accès public"""
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=str(bucket_policy).replace("'", '"')
        )
        
        print(f"✅ Politique d'accès public configurée pour le bucket '{bucket_name}'")
        return True
        
    except ClientError as e:
        print(f"❌ Erreur lors de la configuration de la politique: {e}")
        return False

def configure_cors(bucket_name):
    """Configurer CORS pour le bucket"""
    cors_configuration = {
        'CORSRules': [
            {
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE'],
                'AllowedOrigins': ['*'],
                'MaxAgeSeconds': 3000
            }
        ]
    }
    
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        s3_client.put_bucket_cors(
            Bucket=bucket_name,
            CORSConfiguration=cors_configuration
        )
        
        print(f"✅ Configuration CORS ajoutée pour le bucket '{bucket_name}'")
        return True
        
    except ClientError as e:
        print(f"❌ Erreur lors de la configuration CORS: {e}")
        return False

def main():
    """Fonction principale"""
    print("Configuration du bucket S3 pour OptiTAB")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        print("❌ Variables d'environnement AWS manquantes")
        print("Assurez-vous que AWS_ACCESS_KEY_ID et AWS_SECRET_ACCESS_KEY sont définies")
        return False
    
    bucket_name = 'optitab-media'
    region = 'eu-west-3'
    
    # Créer le bucket
    if not create_bucket(bucket_name, region):
        return False
    
    # Configurer la politique
    if not configure_bucket_policy(bucket_name):
        return False
    
    # Configurer CORS
    if not configure_cors(bucket_name):
        return False
    
    print("\n" + "=" * 50)
    print("✅ Configuration S3 terminée avec succès!")
    print(f"📦 Bucket: {bucket_name}")
    print(f"🌍 Région: {region}")
    print(f"🔗 URL de base: https://{bucket_name}.s3.{region}.amazonaws.com/")
    
    return True

if __name__ == "__main__":
    main()
