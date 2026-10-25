"""Ajoute les constructions manquantes aux sources, avec sauvegarde préalable."""
from pathlib import Path
import re,shutil,json
from figures_revision import produire
ROOT=Path(__file__).resolve().parent
ARCH=ROOT/'build/avant-revision-20261024'

def edit(path,env,n,content):
    old=path.read_text(encoding='utf-8')
    pattern=r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}'
    blocks=list(re.finditer(pattern,old,re.S))
    block=blocks[n-1]
    if content.strip() in block.group():return
    new=block.group().replace('\\end{'+env+'}',content+'\n\\end{'+env+'}')
    save=ARCH/path.relative_to(ROOT);save.parent.mkdir(parents=True,exist_ok=True)
    if not save.exists():shutil.copy2(path,save)
    path.write_text(old[:block.start()]+new+old[block.end():],encoding='utf-8')

def main():
    produire()
    files={int(p.name[:2]):p for p in (ROOT/'corriges').glob('*.tex')}
    meta=json.loads((ROOT/'build/revision-figures.json').read_text(encoding='utf-8'))
    captions={
      '03-ex07-cor':'Allure pour l’acide éthanoïque, dilution négligée ; ordonnée en unités arbitraires.',
      '09-ex11-cor':'Les deux formes totalisent 100 \\% ; elles sont en proportions égales pour pH = pKa.',
      '09-ex12-cor':'La position du pH étudié permet de justifier la forme prédominante.',
      '13-ex04-cor':'Vue de dessus. Les longueurs des flèches de vitesse et d’accélération utilisent des échelles distinctes.',
      '13-ex08-cor':'La pente de la droite vaut $g$ pour l’axe vertical orienté vers le bas.',
      '13-ex09-cor':'L’accélération est la somme de ses composantes tangentielle et normale.',
      '13-ex11-cor':'La différence seconde donne un vecteur dirigé vers le centre du cercle.',
      '14-ex03-cor':'La vitesse indique le mouvement ; elle ne fait pas partie du bilan des forces.',
      '15-ex09-cor':'Points calculés avec les données du programme. Les écarts à la constance viennent des arrondis du pointage.',
      '16-ex07-cor':'Les six planètes du programme sont compatibles avec une droite passant par l’origine.',
      '16-ex12-cor':'Orbite circulaire modélisée ; la vitesse est tangente et l’accélération centripète. Dessin sans échelle.',
      '18-ex08-cor':'Le tracé de $p$ en fonction de $1/V$ permet de tester la proportionnalité.',
      '18-ex09-cor':'La droite est prolongée mathématiquement ; l’air réel ne demeure pas gazeux sur tout ce domaine.',
      '20-ex08-cor':'Le pas de 10 s produit une courbe très proche de la solution exacte ; les deux tracés se superposent presque.',
      '22-ex02-cor':'Le demi-angle correspond à la moitié de la largeur de la tache centrale. Schéma sans échelle.',
      '22-ex08-cor':'Deux signaux de même fréquence déphasés de $\\pi/2$ ; l’amplitude de la somme vaut $\\sqrt2$ unité.',
      '26-ex06-cor':'Sens de décharge choisi : le condensateur fournit de l’énergie à la résistance.',
      '26-ex08-cor':'Charge avec un pas de 0,001 s ; la courbe d’Euler est presque confondue avec l’exponentielle.',
    }
    for name in meta['figures']:
        ch=int(name[:2]);n=int(name[5:7])
        edit(files[ch],'corrige',n,'\\schema[corrige]{rev-'+name+'}\n\\legende{'+captions[name]+'}')
    for ch,n,fig in [(9,15,'09-ex15'),(13,6,'13-ex06'),(15,8,'15-ex08'),(17,4,'17-venturi'),(17,8,'17-venturi')]:
        edit(files[ch],'corrige',n,'\\schema[corrige]{'+fig+'}')
    chapters={int(p.name[:2]):p for p in (ROOT/'chapitres').glob('*.tex')}
    # Documents locaux dans l’énoncé : pas d’aller-retour obligatoire vers le cours.
    for ch,n,fig in [(17,4,'17-venturi'),(17,8,'17-venturi'),(23,2,'23-fronts')]:
        edit(chapters[ch],'exercice',n,'\\schema{'+fig+'}')
    path=files[26];s=path.read_text(encoding='utf-8')
    s=s.replace(r'\demarche{Loi des mailles $u_R+u_C=0$, avec $u_R=R\,i$ et $i=C\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t}$.}',
                r'\demarche{Le courant est orienté dans le sens de la décharge : $u_R=u_C$, $u_R=R\,i$ et $i=-C\,\dfrac{\mathrm{d}u_C}{\mathrm{d}t}$.}')
    s=s.replace(r'\item Circuit formé du condensateur et de la résistance ; en convention récepteur, $u_R+u_C=0$.',
                r'\item Le condensateur alimente la résistance. Sur le schéma, $u_R$ et $u_C$ ont la même orientation : $u_R-u_C=0$. Le courant positif quitte l’armature positive ; sa charge diminue, donc $i=-\mathrm{d}q/\mathrm{d}t=-C\,\mathrm{d}u_C/\mathrm{d}t$.')
    path.write_text(s,encoding='utf-8')
    # Le doigt reste couplé capacitivement à travers une couche isolante.
    s=s.replace(r"Le plastique et le gant sont \res{\text{isolants}} : ils ne forment pas de condensateur avec l'électrode.",
                r'Un gant peut réduire la variation de capacité détectable en augmentant la séparation entre le doigt et l’électrode. Une couche isolante n’empêche pas, à elle seule, un couplage capacitif ; l’écran est déjà recouvert d’un isolant.')
    path.write_text(s,encoding='utf-8')
    print('Révision des figures intégrée aux sources.')

if __name__=='__main__':main()
