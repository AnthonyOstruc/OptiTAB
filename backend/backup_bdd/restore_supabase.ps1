# Variables de connexion
$dbHost = "db.yjwvietwtcrzfkmahfpy.supabase.co"
$dbUser = "postgres"
$dbName = "postgres"
$dbPort = 5432

# Chemin du fichier de sauvegarde à restaurer (à adapter)
$backupFile = ".\backup_supabase_20250807_115342.dump"

# Demande du mot de passe (sans l’afficher)
Write-Host "Entrez le mot de passe PostgreSQL :"
$securePass = Read-Host -AsSecureString
$plainPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePass))

# Met le mot de passe dans la variable d'environnement pour pg_restore
$env:PGPASSWORD = $plainPass

# Lance la restauration (option -c = clean = supprime objets existants)
pg_restore -h $dbHost -U $dbUser -d $dbName -p $dbPort -c $backupFile

# Supprime la variable d’environnement PGPASSWORD pour la sécurité
Remove-Item Env:PGPASSWORD

Write-Host "Restauration terminée depuis $backupFile"
