# Variables de connexion à la base Supabase
$dbHost = "db.yjwvietwtcrzfkmahfpy.supabase.co"
$dbUser = "postgres"
$dbName = "postgres"
$dbPort = 5432

# Demande le mot de passe PostgreSQL
Write-Host "Entrez le mot de passe PostgreSQL :"
$securePass = Read-Host -AsSecureString
$plainPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePass))

# Met le mot de passe dans la variable d'environnement pour psql
$env:PGPASSWORD = $plainPass

# SQL pour supprimer toutes les tables dans le schema public
$sqlDrop = @"
DO \$\$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END \$\$;
"@

# Exécute la commande psql avec la requête
psql -h $dbHost -U $dbUser -d $dbName -p $dbPort -c $sqlDrop

# Nettoyage de la variable d'environnement
Remove-Item Env:PGPASSWORD

Write-Host "Toutes les tables ont été supprimées dans la base."

# Suppression locale des fichiers de migrations Django
Write-Host "Suppression des fichiers migrations et caches locaux..."

# Supprimer les fichiers *.py dans dossiers migrations sauf __init__.py
Get-ChildItem -Recurse -Path . -Include *.py | Where-Object {
    $_.FullName -like "*\migrations\*" -and $_.Name -ne "__init__.py"
} | Remove-Item -Force

# Supprimer les fichiers *.pyc dans dossiers migrations
Get-ChildItem -Recurse -Path . -Include *.pyc | Where-Object {
    $_.FullName -like "*\migrations\*"
} | Remove-Item -Force

# Supprimer tous les dossiers __pycache__
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

Write-Host "Fichiers de migration et caches supprimés localement."
