# Publie un lot de notions v1 prêtes : relier les nouveau-N, ré-exporter, simuler, puis
# appliquer seulement si la simulation n'a rien refusé, et contrôler le champ contenu.
#   powershell -File publier_lot.ps1 terminale 87 88
param([string]$niveau, [Parameter(ValueFromRemainingArguments = $true)][string[]]$ids)
$ErrorActionPreference = 'Stop'
$racine = 'C:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2'
$o = "$racine\frontend\cours\format_v1\outils"
$c = "$racine\frontend\cours\format_v1\chantier\$niveau"
$py = "$racine\backend\venv\Scripts\python.exe"
$env:PYTHONIOENCODING = 'utf-8'
Set-Location "$racine\backend"
$ds = foreach ($i in $ids) { (Get-ChildItem $c -Directory | Where-Object { $_.Name -match "^$($i)_" } | Select-Object -First 1).FullName }
& $py "$o\relier_nouveaux.py" @ds
$liste = ($ids | ForEach-Object { "'$_'" }) -join ','
& $py manage.py shell -c "import sys; sys.argv=['x',$liste]; exec(open(r'$o\exporter.py', encoding='utf-8').read())" | Select-Object -Last 1
$a = ($ds | ForEach-Object { "r'$_'" }) -join ','
$sim = & $py manage.py shell -c "import sys; sys.argv=['x',$a]; exec(open(r'$o\importer_v1.py', encoding='utf-8').read())"
$sim | Select-String -Pattern '✓|✗|REFUS|créer|titre changé' | ForEach-Object { $_.Line }
if ($sim -match 'REFUSÉE') { Write-Output 'ARRÊT : simulation refusée, rien appliqué.'; exit 1 }
& $py manage.py shell -c "import sys; sys.argv=['x',$a,'--appliquer']; exec(open(r'$o\importer_v1.py', encoding='utf-8').read())" | Select-String -Pattern '✓|✗|relu' | ForEach-Object { $_.Line }
& $py manage.py shell -c "import sys; sys.argv=['x',$a,'--appliquer']; exec(open(r'$o\titres_docs.py', encoding='utf-8').read())" | Select-Object -Skip 1
& $py manage.py shell -c "import sys; sys.argv=['x']; exec(open(r'$o\synchro_contenu.py', encoding='utf-8').read())" | Select-Object -Last 2
