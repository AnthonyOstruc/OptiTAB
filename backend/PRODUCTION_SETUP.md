# Configuration Production - Réinitialisation de mot de passe

## Variables d'environnement nécessaires sur Render

Pour que la fonctionnalité de réinitialisation de mot de passe fonctionne en production, vous devez configurer les variables d'environnement suivantes dans votre service Render :

### Variables obligatoires pour les emails :

1. **EMAIL_HOST** - Serveur SMTP (ex: `smtp.gmail.com`, `smtp.sendgrid.com`)
2. **EMAIL_PORT** - Port SMTP (généralement `587` pour TLS)
3. **EMAIL_USE_TLS** - Utiliser TLS (`True` ou `False`)
4. **EMAIL_HOST_USER** - Nom d'utilisateur/email pour l'authentification SMTP
5. **EMAIL_HOST_PASSWORD** - Mot de passe pour l'authentification SMTP
6. **DEFAULT_FROM_EMAIL** - Adresse email expéditrice (ex: `noreply@optitab.net`)

### Variables pour les URLs :

1. **FRONTEND_BASE_URL** - URL complète du frontend en production (ex: `https://www.optitab.net`)

## Configuration des secrets sur Render

Dans votre tableau de bord Render, allez dans :
- **Settings** > **Environment**
- Ajoutez les secrets suivants (ils seront automatiquement utilisés par `fromSecret` dans render.yaml) :

```
email_host: smtp.gmail.com
email_port: 587
email_host_user: votre-email@gmail.com
email_host_password: votre-mot-de-passe-application
default_from_email: contact@optitab.net
```

## Test de la fonctionnalité

Après avoir configuré les variables d'environnement :

1. Déployez votre application sur Render
2. Testez la réinitialisation de mot de passe depuis votre frontend
3. Vérifiez que les emails sont reçus avec les bons liens
4. Assurez-vous que les liens redirigent vers la bonne page de réinitialisation

## Dépannage

### Si les emails ne sont pas envoyés :
- Vérifiez que toutes les variables EMAIL_* sont correctement configurées
- Assurez-vous que le mot de passe d'application est utilisé (pas le mot de passe principal)
- Vérifiez les logs de l'application pour les erreurs SMTP

### Si les liens ne fonctionnent pas :
- Vérifiez que FRONTEND_BASE_URL pointe vers la bonne URL
- Assurez-vous que la route `/password-reset` existe dans votre frontend
- Vérifiez que le token dans l'URL est valide (non expiré)

### Erreurs courantes :
- **Token expiré** : Les tokens expirent par défaut après 24h
- **Lien invalide** : Le token a déjà été utilisé ou est mal formé
- **Erreur SMTP** : Problème de configuration email
