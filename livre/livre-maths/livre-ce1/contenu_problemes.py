from modele import C,E

C('Le tout, les parties et le départ','Problèmes','Dès P1 ; nombres progressifs',
 'Je repère ce qui est connu et ce que je cherche.','Jetons, bandes de papier et ardoise.',
 'Prépare un total de 125 cubes avec le matériel. Cache une partie et laisse 48 visibles. Dessine le tout et les deux parties.',
 ['Je reformule l’histoire et sa question.','Le tout réunit les parties ; une partie peut être inconnue.','Pour retrouver le départ, je reconstruis la situation avant le changement.'],
 'Il y a 245 cartes, dont 128 rouges. Les autres sont bleues. 245 - 128 = 117 cartes bleues.',('bar',[245,128,'?']),
 'J’ai donné 36 cartes et il m’en reste 125. Combien en avais-je ?', '125 + 36 = 161 cartes au départ.',[
 E('Il y a 360 perles en tout, dont 145 vertes. Les autres sont bleues. Combien sont bleues ?','360 - 145 = 215 perles bleues.',('bar',[360,145,'?']),'360-145==215'),
 E('Un bac contient 238 cubes et un autre 174. Combien de cubes au total ?','238 + 174 = 412 cubes.',None,'238+174==412'),
 E('Un album a 500 places et contient 367 photos. Combien de places libres ?','500 - 367 = 133 places libres.',None,'500-367==133'),
 E('J’avais des images. J’en donne 57 et il m’en reste 186. Combien en avais-je ?','186 + 57 = 243 images.',None,'186+57==243'),
 E('J’avais des cartes. J’en reçois 48 et j’en ai maintenant 302. Combien en avais-je ?','302 - 48 = 254 cartes.',None,'302-48==254'),
 E('Un arbre portait 125 fruits. Il en reste 89. Combien ont été cueillis ?','125 - 89 = 36 fruits.',None,'125-89==36'),
 E('Un album peut contenir 350 photos. Lina en a 278 et Noé 85. L’album suffit-il ?','278 + 85 = 363. Non : il manque 13 places.',None,'278+85==363 and 363-350==13'),
 E('Une réserve a perdu 126 feuilles et en contient encore 384. Combien y en avait-il au départ ?','384 + 126 = 510 feuilles.',None,'384+126==510'),
 E('Invente une histoire où l’on donne 25 objets et où la réponse se trouve avec 140 + 25.','Exemple : j’ai donné 25 cartes et il m’en reste 140. J’en avais 165 au départ.',None,'140+25==165')],
 'Nommer le tout, les parties et l’inconnue sur un schéma avant de calculer.', 'Un mot comme « donne » ne suffit pas pour choisir l’opération ; la question détermine ce qu’on cherche.')

C('Comparer deux quantités','Problèmes','P1 puis P2',
 'Je distingue la grande quantité, la petite et leur écart.','Bandes de papier et jetons.',
 'Pose une bande pour 85 cartes et une autre pour 112 cartes avec le même départ. Repère la partie qui dépasse.',
 ['L’écart indique combien il y a de plus ou de moins.','La grande quantité est la petite quantité plus l’écart.','Je vérifie qui doit avoir le plus avant de choisir un calcul.'],
 'Lina a 148 cartes. Noé en a 35 de plus. Noé a 148 + 35 = 183 cartes.',('comparebars',[148,35]),
 'Mina a 96 cartes. Elle en a 18 de plus que Sami. Combien Sami en a-t-il ?', 'Sami en a moins : 96 - 18 = 78 cartes.',[
 E('Lina a 125 cartes. Noé en a 28 de plus. Combien Noé en a-t-il ?','125 + 28 = 153 cartes.',('comparebars',[125,28]),'125+28==153'),
 E('Une école a 238 élèves et une autre 196. Quel est l’écart entre leurs effectifs ?','238 - 196 = 42 élèves.',None,'238-196==42'),
 E('Le bac bleu contient 175 cubes. Il en a 46 de moins que le bac rouge. Combien le bac rouge en contient-il ?','175 + 46 = 221 cubes.',None,'175+46==221'),
 E('Mila a 304 perles, soit 78 de plus que Zoé. Combien Zoé en a-t-elle ?','304 - 78 = 226 perles.',None,'304-78==226'),
 E('Une ficelle mesure 140 cm, une autre 95 cm. De combien la première est-elle plus longue ?','140 - 95 = 45 cm.',None,'140-95==45'),
 E('Lina a 125 cartes. Sami en a 125. Quel est l’écart ?','0 carte : les quantités sont égales.'),
 E('Un jeu coûte 38 €. Il coûte 12 € de moins qu’un autre jeu. Quel est le prix de l’autre jeu ?','38 + 12 = 50 €.',None,'38+12==50'),
 E('Lina dit : « J’ai 63 billes, soit 9 de plus que Noé. Donc Noé en a 72. » Corrige.','Noé en a moins : 63 - 9 = 54 billes.',None,'63-9==54'),
 E('Invente une question de comparaison dont la réponse est 240 - 185.','Exemple : A possède 240 cartes et B 185. Combien A en a-t-il de plus ? Réponse : 55 cartes.',None,'240-185==55')],
 'Aligner deux bandes à la même origine et marquer la partie supplémentaire.', 'Le mot « plus » peut conduire à soustraire lorsqu’on cherche la petite quantité.')

C('Résoudre en deux étapes','Problèmes','Dès P2, puis P3-P5',
 'Je choisis une opération pour chaque étape.','Ardoise et schémas en barres.',
 'Joue une histoire avec 83 livres : on en apporte 25, puis on en prête 46. Note ce qui reste à chaque moment.',
 ['Je repère les étapes et les informations utiles.','Je garde le résultat intermédiaire et son unité.','Un problème peut mêler une multiplication et une addition ou une soustraction.'],
 '83 livres, puis 25 en plus et 46 prêtés : 83 + 25 = 108 ; 108 - 46 = 62 livres.',('story',[83,25,-46]),
 'J’achète 4 cahiers à 3 € chacun. Je donne 20 €. Quelle monnaie me rend-on ?', '4 × 3 = 12 € ; 20 - 12 = 8 €.',[
 E('Il y a 125 livres. On en apporte 38, puis on en prête 47. Combien en reste-t-il ?','125 + 38 = 163 ; 163 - 47 = 116 livres.',('storyblank',[125,38,-47]),'125+38-47==116'),
 E('Une boîte contient 245 perles, dont 86 rouges et 74 bleues. Les autres sont vertes. Combien sont vertes ?','86 + 74 = 160 ; 245 - 160 = 85 perles vertes.',None,'245-86-74==85'),
 E('Un bus contient 43 voyageurs. 18 descendent, puis 27 montent. Combien de voyageurs ?','43 - 18 = 25 ; 25 + 27 = 52 voyageurs.',None,'43-18+27==52'),
 E('Tu achètes 6 crayons à 2 € chacun et un cahier à 5 €. Combien paies-tu ?','6 × 2 = 12 € ; 12 + 5 = 17 €.',None,'6*2+5==17'),
 E('Tu achètes 7 jeux à 4 € chacun et tu donnes 50 €. Combien reçoit-on de monnaie ?','7 × 4 = 28 € ; 50 - 28 = 22 €.',None,'50-7*4==22'),
 E('Pour 8 enfants, il faut un cahier à 3 € et une pochette à 2 € par enfant. Quel est le coût total ?','3 + 2 = 5 € par enfant ; 8 × 5 = 40 €.',None,'8*(3+2)==40'),
 E('On prépare 5 sacs de 6 balles, puis on ajoute 9 balles isolées. Combien de balles ?','5 × 6 = 30 ; 30 + 9 = 39 balles.',None,'5*6+9==39'),
 E('Il y a 260 places. On réserve 135 places le matin et 78 l’après-midi. Combien restent libres ?','135 + 78 = 213 ; 260 - 213 = 47 places.',None,'260-135-78==47'),
 E('Lina reçoit 30 €. Elle achète 4 livres à 5 € chacun. Elle dit qu’il lui reste 26 €. Explique.','Elle doit d’abord calculer 4 × 5 = 20 €. Il reste 30 - 20 = 10 €.',None,'30-4*5==10')],
 'Faire un schéma par étape et conserver les résultats intermédiaires avec leur unité.', 'Les problèmes mixtes comportent une étape additive et une étape multiplicative, sans exiger une division posée.')

C('Grouper et partager','Problèmes','P2 à P5',
 'Je cherche une part ou un nombre de groupes.','Jetons, boîtes et tableaux de recherche.',
 'Partage 24 jetons entre 4 enfants, puis range 24 jetons par paquets de 4. Compare ce que tu cherches dans les deux cas.',
 ['Pour une part égale, je cherche combien chacun reçoit.','Pour des paquets, je cherche combien de groupes je peux former.','Si des objets restent, je relis la question : faut-il un paquet en plus ou seulement des paquets complets ?'],
 '24 cartes pour 4 enfants : 6 cartes chacun. Par paquets de 4, ces 24 cartes font 6 paquets.',('groups',[4,6]),
 'Avec 35 objets, fais des paquets de 5.', '7 paquets, car 7 × 5 = 35.',[
 E('36 cartes sont partagées également entre 4 enfants. Combien chacun reçoit-il ?','9 cartes chacun, car 4 × 9 = 36.',('sharebar',[36,4]),'4*9==36'),
 E('On fait des équipes de 6 avec 54 enfants. Combien d’équipes ?','9 équipes, car 9 × 6 = 54.',None,'9*6==54'),
 E('On partage 80 perles en 10 parts égales. Combien de perles dans chaque part ?','8 perles.',None,'10*8==80'),
 E('On range 120 cartes en paquets de 10. Combien de paquets ?','12 paquets.',None,'12*10==120'),
 E('25 photos doivent être rangées sur des pages de 10 places. Combien de pages faut-il ?','3 pages : deux pages pleines et une page contenant 5 photos.',None,'25//10==2 and 25%10==5'),
 E('On vend seulement des boîtes complètes de 6 œufs. Avec 41 œufs, combien de boîtes peut-on vendre ?','6 boîtes complètes ; il reste 5 œufs.',None,'41//6==6 and 41%6==5'),
 E('La classe partage 150 cartes entre 5 groupes. Combien de cartes par groupe ?','30 cartes par groupe : 5 × 30 = 150.',None,'5*30==150'),
 E('On veut ranger 189 images sur des pages de 10 places. Combien de pages faut-il ?','19 pages : 18 pages pleines et une dernière avec 9 images.',None,'189//10==18 and 189%10==9'),
 E('Pour 75 œufs vendus en boîtes complètes de 6, Noé propose 13 boîtes. Vérifie.','13 boîtes demanderaient 78 œufs. On peut vendre 12 boîtes complètes et il reste 3 œufs.',None,'75//6==12 and 75%6==3 and 13*6==78')],
 'Dessiner les groupes ou utiliser les tables à l’envers ; traiter les restes dans l’histoire.', 'Le symbole de division et un algorithme de division ne sont pas nécessaires pour résoudre ces tâches.')
