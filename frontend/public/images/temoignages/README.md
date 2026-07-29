# Captures des témoignages WhatsApp / SMS

Les captures affichées sur la page `/avis` se déposent ici.

La page n'affiche **que de vraies captures**. Il n'y a volontairement aucune
conversation reconstituée : un faux chat se repère immédiatement et détruit
la confiance qu'on cherche justement à construire.

## Comment ajouter une capture

1. **Demandez l'accord de la famille** avant toute publication. Un simple message
   « Est-ce que je peux publier votre retour sur mon site ? » suffit, mais gardez-en une trace.
2. **Anonymisez la capture** avant de l'enregistrer :
   - masquez le numéro de téléphone (en haut de l'écran WhatsApp) ;
   - masquez la photo de profil ;
   - remplacez le nom complet par le prénom + initiale (ex. « Sandra M. ») ;
   - supprimez tout ce qui permettrait d'identifier l'enfant (nom de l'établissement, adresse…).
3. **Recadrez sur les messages qui comptent.** Inutile de garder la barre de statut ou
   le clavier : plus la capture est resserrée sur la conversation, plus elle est lisible
   dans la vignette.
4. **Enregistrez le fichier ici** avec un nom explicite, en minuscules et sans accent :
   `whatsapp-sandra.png`, `sms-karim.png`…
5. **Optimisez le poids** : largeur max ~900 px, format `.png` ou `.webp`, idéalement < 250 Ko.
   Une capture trop lourde ralentit la page et fait fuir les visiteurs mobiles.
6. **Déclarez la capture** dans `src/config/bioLandingContent.js`, tableau `TESTIMONIALS` :

```js
export const TESTIMONIALS = [
  {
    id: 'sandra',
    channel: 'whatsapp',              // 'whatsapp' ou 'sms'
    author: 'Sandra M.',              // prénom + initiale, jamais le nom complet
    role: 'Maman de Léa · Terminale',
    src: '/images/temoignages/whatsapp-sandra.png',
    alt: "Message WhatsApp d'une maman : sa fille est passée de 8 à 14 de moyenne",
    featured: true                    // sur UNE seule entrée : s'affiche aussi dans le hero
  }
]
```

## Ce qui se passe automatiquement

- **Les vignettes sont toutes à la même hauteur.** Le cadrage est à ratio fixe (3/4),
  donc une capture très haute et une capture très large donnent la même carte.
  Aucun effet « escalier », quelles que soient les dimensions de vos images.
- **Le clic ouvre la capture en entier**, non recadrée, dans une visionneuse
  (flèches gauche/droite pour naviguer, Échap pour fermer).
- **Les filtres WhatsApp / SMS apparaissent tout seuls** dès que vous avez au moins
  une capture de chaque type.
- **`featured: true`** fait remonter la capture dans le hero, visible sans scroller.

## Tant que ce dossier est vide

La section témoignages est **entièrement masquée en production** — mieux vaut pas de
section qu'une section vide. En développement, un guide s'affiche à la place pour
vous rappeler la marche à suivre.

## Rappel

Ne publiez jamais une capture non anonymisée : c'est une donnée personnelle (RGPD).
