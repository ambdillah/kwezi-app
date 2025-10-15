# 🚀 Après extraction : Créer le build Android

## Guide étape par étape pour obtenir le fichier AAB

**Temps estimé total : 30-40 minutes**

---

## ✅ VÉRIFICATION PRÉALABLE

Avant de commencer, assurez-vous d'avoir :
- ✅ Extrait `kwezi-frontend-code.tar.gz` dans un dossier (ex: `C:\Kwezi\frontend\`)
- ✅ Extrait `kwezi-audio.tar.gz` dans le sous-dossier `assets/`

**Structure attendue :**
```
C:\Kwezi\frontend\
├── app.json ✅
├── eas.json ✅
├── package.json ✅
├── app/
├── assets/
│   └── audio/ (tous les fichiers audio)
├── components/
├── contexts/
└── utils/
```

---

## 📥 ÉTAPE 1 : Installer Node.js (Si pas déjà fait)

### Vérifier si Node.js est installé :

**Ouvrez un terminal :**
- Windows : Appuyez sur `Win + R`, tapez `cmd`, Entrée
- Mac : Ouvrez "Terminal" depuis Applications
- Linux : Ouvrez votre terminal

**Tapez cette commande :**
```bash
node --version
```

**Si vous voyez un numéro de version (ex: v20.x.x) :**
✅ Node.js est déjà installé → Passez à l'étape 2

**Si vous voyez "command not found" ou une erreur :**
❌ Node.js n'est pas installé → Suivez les instructions ci-dessous

### Installer Node.js :

1. **Allez sur :** https://nodejs.org
2. **Téléchargez la version LTS** (recommandée, bouton vert)
3. **Installez le fichier téléchargé**
4. **Redémarrez votre terminal**
5. **Vérifiez l'installation :**
   ```bash
   node --version
   npm --version
   ```

**Temps estimé : 5 minutes**

---

## ⚙️ ÉTAPE 2 : Installer EAS CLI

**Ouvrez un terminal** (ou utilisez le même que l'étape 1)

**Tapez cette commande :**
```bash
npm install -g eas-cli
```

**Attendez que l'installation se termine** (2-3 minutes)

**Vérifiez l'installation :**
```bash
eas --version
```

Vous devriez voir : `eas-cli/16.x.x` ou similaire

**Temps estimé : 3 minutes**

---

## 📂 ÉTAPE 3 : Naviguer vers votre projet

**Dans le terminal, allez dans le dossier où vous avez extrait les fichiers :**

**Windows :**
```bash
cd C:\Kwezi\frontend
```

**Mac/Linux :**
```bash
cd ~/Kwezi/frontend
```

**Vérifiez que vous êtes au bon endroit :**
```bash
dir        # Windows
ls         # Mac/Linux
```

Vous devriez voir : `app.json`, `eas.json`, `package.json`, etc.

---

## 🔐 ÉTAPE 4 : Se connecter à Expo

**Tapez cette commande :**
```bash
eas login
```

**Le terminal va vous demander :**

```
? Email or username:
```
**Tapez :** `ambdi97@hotmail.fr`
**Appuyez sur Entrée**

```
? Password:
```
**Tapez votre mot de passe** (les caractères ne s'affichent pas, c'est normal)
**Appuyez sur Entrée**

**Vous devriez voir :**
```
✔ Logged in as ambdi97@hotmail.fr
```

**Temps estimé : 1 minute**

---

## 📦 ÉTAPE 5 : Installer les dépendances du projet

**Tapez cette commande :**
```bash
npm install
```

**Ce qui va se passer :**
- Le terminal va télécharger tous les packages nécessaires
- Vous verrez beaucoup de lignes défiler
- Cela peut prendre 3-5 minutes

**Attendez que vous voyiez :**
```
added XXX packages in XXs
```

**⚠️ Si vous voyez des "warnings" en jaune :** C'est normal, ignorez-les

**Temps estimé : 5 minutes**

---

## 🛠️ ÉTAPE 6 : Configurer EAS Build

**Tapez cette commande :**
```bash
eas build:configure
```

**Le terminal va vous poser des questions. Répondez comme suit :**

**Question 1 :**
```
? Would you like to automatically create an EAS project for @ambdi97/kwezi?
```
**Réponse :** Tapez `Y` puis Entrée

**Question 2 :**
```
? Generate a new Android Keystore?
```
**Réponse :** Tapez `Y` puis Entrée

**Vous devriez voir :**
```
✔ Created a new project: @ambdi97/kwezi
✔ Generated a new Android Keystore
```

**Temps estimé : 2 minutes**

---

## 🚀 ÉTAPE 7 : Lancer le build de production !

**C'est l'étape finale ! Tapez cette commande :**
```bash
eas build --platform android --profile production
```

**Ce qui va se passer :**

### Phase 1 : Analyse (1 minute)
```
✔ Checking project configuration
✔ Validating credentials
```

### Phase 2 : Upload (3-5 minutes selon votre connexion)
```
✔ Compressing project files
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%
✔ Uploading to EAS Build
```

**⚠️ NE FERMEZ PAS LE TERMINAL pendant cette phase !**

### Phase 3 : Build sur les serveurs Expo (15-25 minutes)
```
✔ Build started!
📱 Build details: https://expo.dev/accounts/ambdi97/projects/kwezi/builds/...

Build in progress...
⏳ This usually takes 15-25 minutes
```

**À ce stade, vous POUVEZ fermer le terminal.**

Le build continue sur les serveurs Expo. Vous recevrez un **email** quand c'est terminé.

---

## 📧 ÉTAPE 8 : Attendre l'email de confirmation

**Pendant que le build se fait :**
- ☕ Prenez un café
- 🎮 Faites autre chose
- 📧 Surveillez votre email **ambdi97@hotmail.fr**

**Vous recevrez un email d'Expo avec :**
- ✅ "Your build is complete!" (si réussi)
- ❌ "Your build failed" (si échec)

**Si réussi, l'email contiendra :**
- Un lien pour télécharger le fichier AAB
- Les détails du build

**Temps estimé : 15-25 minutes**

---

## 📥 ÉTAPE 9 : Télécharger le fichier AAB

### Méthode A : Via l'email
1. Ouvrez l'email d'Expo
2. Cliquez sur le lien de téléchargement
3. Le fichier `kwezi-1.0.0-xxx.aab` se télécharge

### Méthode B : Via le terminal
```bash
eas build:download --platform android --profile production
```

Le fichier sera téléchargé dans le dossier actuel.

### Méthode C : Via le dashboard Expo
1. Allez sur https://expo.dev
2. Connectez-vous
3. Cliquez sur votre projet "kwezi"
4. Allez dans "Builds"
5. Cliquez sur "Download" pour le dernier build

**Vous obtiendrez un fichier :**
```
kwezi-1.0.0-[build-id].aab
Taille : ~40-60 MB
```

---

## 🎉 ÉTAPE 10 : Vous avez le fichier AAB !

**Félicitations ! Vous avez maintenant le fichier nécessaire pour publier sur Play Store !**

**Prochaines étapes :**
1. ✅ Uploadez ce fichier AAB sur Google Play Console
2. ✅ Remplissez la fiche de l'application (guide fourni)
3. ✅ Ajoutez des captures d'écran
4. ✅ Soumettez pour review
5. ⏳ Attendez 1-7 jours
6. 🎊 Publication !

---

## 📋 RÉSUMÉ DES COMMANDES (Dans l'ordre)

```bash
# 1. Vérifier Node.js
node --version

# 2. Installer EAS CLI
npm install -g eas-cli

# 3. Aller dans le dossier
cd C:\Kwezi\frontend

# 4. Se connecter à Expo
eas login

# 5. Installer les dépendances
npm install

# 6. Configurer EAS
eas build:configure

# 7. Lancer le build
eas build --platform android --profile production

# 8. (Optionnel) Télécharger le AAB
eas build:download --platform android --profile production
```

---

## 🆘 PROBLÈMES COURANTS

### Problème 1 : "npm: command not found"
**Solution :** Node.js n'est pas installé. Installez-le depuis nodejs.org

### Problème 2 : "eas: command not found"
**Solution :** 
```bash
npm install -g eas-cli
# Redémarrez votre terminal
```

### Problème 3 : "Authentication failed"
**Solution :**
```bash
eas logout
eas login
```

### Problème 4 : "Build failed"
**Causes possibles :**
- Connexion internet coupée pendant l'upload
- Fichiers manquants

**Solution :**
- Relancez : `eas build --platform android --profile production`
- Si ça échoue encore, partagez-moi le message d'erreur

### Problème 5 : "Cannot find module..."
**Solution :**
```bash
cd C:\Kwezi\frontend
npm install
```

---

## ⏱️ TIMELINE COMPLÈTE

| Étape | Action | Temps |
|-------|--------|-------|
| 1 | Installer Node.js | 5 min |
| 2 | Installer EAS CLI | 3 min |
| 3 | Naviguer vers projet | 1 min |
| 4 | Se connecter Expo | 1 min |
| 5 | Installer dépendances | 5 min |
| 6 | Configurer EAS | 2 min |
| 7 | Upload vers Expo | 5 min |
| 8 | **Build sur serveurs** | **15-25 min** |
| 9 | Télécharger AAB | 2 min |
| **TOTAL** | | **~40-50 minutes** |

---

## 📞 BESOIN D'AIDE ?

**Partagez-moi :**
- À quelle étape vous êtes bloqué
- Le message d'erreur exact (copier-coller)
- Une capture d'écran si possible

**Je vous aiderai immédiatement !**

---

**🎯 COMMENCEZ MAINTENANT PAR L'ÉTAPE 1 !**

**Dites-moi quand vous êtes prêt à commencer et je vous guiderai en temps réel !** 🚀
