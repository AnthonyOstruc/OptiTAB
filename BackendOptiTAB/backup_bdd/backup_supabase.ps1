# Variables de connexion
$dbHost = "aws-0-eu-west-3.pooler.supabase.com"
$dbUser = "postgres.yjwvietwtcrzfkmahfpy"
$dbName = "postgres"
$dbPort = 5432

# Génère un horodatage pour le fichier (format : yyyyMMdd_HHmmss)
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Nom du fichier avec date et heure
$backupFile = "backup_supabase_$timestamp.dump"

# Demande du mot de passe (sans l’afficher)
Write-Host "Entrez le mot de passe PostgreSQL :"
$securePass = Read-Host -AsSecureString
$plainPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePass))

# Met le mot de passe dans la variable d'environnement pour pg_dump
$env:PGPASSWORD = $plainPass

# Lance la commande pg_dump
pg_dump -h $dbHost -U $dbUser -d $dbName -p $dbPort -F c -f $backupFile

# Supprime la variable d’environnement PGPASSWORD pour la sécurité
Remove-Item Env:PGPASSWORD

Write-Host "Backup terminé et sauvegardé dans $backupFile"
