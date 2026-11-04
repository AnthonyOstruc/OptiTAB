# Construction et actualisation des ressources gratuites

`npm run build` utilise l’export public versionné dans `contenu/ressources/`.
Il ne contacte pas le backend pour construire les pages, les plans du site ou
les redirections : une indisponibilité de Django ne bloque plus le déploiement
du frontend.

L’export comprend les cours, fiches et exercices publics, ainsi que les seuls
identifiants nécessaires au décompte des exercices réservés aux abonnés.
Son manifeste indique sa date, sa source, ses effectifs et son empreinte SHA-256.
Un export absent, corrompu ou incohérent fait échouer la construction.

Après une modification des contenus en base, préparer la prochaine publication :

```sh
npm run ressources:actualiser
node --test scripts/ressources/catalogue.test.mjs scripts/ressources/instantane.test.mjs
npm run build
```

La première commande lit l’API publique, renouvelle l’export et actualise les
fichiers SEO et les redirections. Inclure ces changements dans la publication
Git, après vérification. Elle n’écrit rien dans la base de données.

Pour vérifier uniquement l’export existant :

```sh
node scripts/ressources/instantane.mjs --verifier
```

Les prix, la connexion et les autres fonctions interactives continuent d’utiliser
l’API à l’exécution. Les images des ressources conservent leurs adresses de stockage.
