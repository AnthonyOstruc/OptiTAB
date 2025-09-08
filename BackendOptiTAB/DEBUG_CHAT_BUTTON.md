# 🔧 Guide de Dépannage - Bouton Chat IA

## 🚨 Problème : "Je n'arrive pas à cliquer pour envoyer une question"

### 📋 Étapes de Diagnostic

#### **1. Test du Bouton d'Urgence**
1. Ouvrez l'interface de chat IA
2. Regardez en bas de la zone de saisie
3. Vous devriez voir un bouton rouge avec "🧪 TESTER LE BOUTON"
4. **Cliquez dessus**
5. Une alerte devrait apparaître avec votre message

**Résultats possibles :**
- ✅ **L'alerte apparaît** → Le problème vient du bouton principal (CSS/événements)
- ❌ **Rien ne se passe** → Problème général avec les événements

#### **2. Vérifications dans la Console**
1. Ouvrez les outils développeur (F12)
2. Allez dans l'onglet "Console"
3. Tapez un message dans la zone de texte
4. Cliquez sur le bouton d'envoi
5. Regardez les messages dans la console

**Messages attendus :**
```
Send button clicked MouseEvent {...}
Sending message: votre message ici
```

#### **3. Vérifications Visuelles**
- Le bouton est-il visible ? (bordure rouge pulsante)
- Le bouton change-t-il de couleur quand vous tapez du texte ?
- Le curseur devient-il une main quand vous survolez le bouton ?

### 🛠️ Solutions par Problème

#### **A. Le Bouton d'Urgence Fonctionne**
Si le bouton rouge fonctionne mais pas le bouton principal :

1. **Vérifiez les Styles CSS**
   - Le bouton pourrait être masqué par d'autres éléments
   - Problème de z-index ou de positionnement

2. **Testez en Mode Simplifié**
   ```javascript
   // Dans la console du navigateur :
   document.querySelector('.send-btn').click()
   ```

#### **B. Aucun Bouton ne Fonctionne**
Si même le bouton d'urgence ne marche pas :

1. **Problème JavaScript**
   - Erreur dans la console ?
   - Problème de chargement du composant Vue

2. **Test Manuel**
   ```javascript
   // Dans la console :
   alert('JavaScript fonctionne')
   ```

### 🔍 Tests Supplémentaires

#### **Test 1 : Zone de Texte**
```javascript
// Tapez dans la console :
document.querySelector('.message-input').value = 'Test message'
```

#### **Test 2 : Événements Clavier**
- Essayez **Enter** au lieu du bouton
- Essayez **Shift + Enter** pour une nouvelle ligne

#### **Test 3 : Souris**
- Cliquez droit sur le bouton → "Inspecter l'élément"
- Vérifiez si des styles CSS bloquent les clics

### 📱 Test Mobile
Si vous êtes sur mobile :
1. Essayez de taper plus fort sur l'écran
2. Vérifiez que le viewport n'est pas zoomé
3. Testez avec un navigateur différent

### 🆘 Solutions d'Urgence

#### **Solution 1 : Mode Texte Simple**
```html
<!-- Remplacez temporairement le bouton par : -->
<button onclick="alert('Message: ' + document.querySelector('.message-input').value)">
  ENVOYER
</button>
```

#### **Solution 2 : Raccourci Clavier**
Utilisez uniquement la touche **Enter** pour envoyer les messages.

#### **Solution 3 : Console Directe**
```javascript
// Pour tester l'envoi direct :
fetch('/api/ai/ask/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
  },
  body: JSON.stringify({
    message: 'Test depuis la console',
    model: 'gpt-3.5-turbo'
  })
}).then(r => r.json()).then(console.log)
```

### 📞 Support

Si le problème persiste :
1. **Capture d'écran** de la console (F12)
2. **Capture d'écran** de l'interface
3. **Description précise** de ce qui se passe

**L'interface est conçue pour fonctionner parfaitement - nous allons identifier et résoudre le problème ensemble !** 🚀
