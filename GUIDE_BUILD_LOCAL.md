# 🖥️ Guide Build Local - Sur votre machine
## Instructions complètes pour créer le build AAB de Kwezi

**Package name :** com.mahoraiseducation.kwezi  
**Version :** 1.0.0

---

## 📥 ÉTAPE 1 : Télécharger le projet

### Sur votre navigateur :

1. **Téléchargez le dossier frontend complet**
   - Tous les fichiers sont dans `/app/frontend/`
   - Vous devez télécharger :
     - `app.json` ✅ (déjà configuré)
     - `eas.json` ✅ (déjà configuré)
     - `package.json`
     - Dossier `app/` (avec tous les écrans)
     - Dossier `assets/` (avec toutes les images et audio)
     - Dossier `components/`
     - Dossier `contexts/`
     - Dossier `utils/`
     - Dossier `data/`
     - `.env`

2. **Créez un dossier sur votre ordinateur**
   ```
   C:/Kwezi/frontend/  (Windows)
   ou
   ~/Kwezi/frontend/   (Mac/Linux)
   ```

3. **Extrayez tous les fichiers dans ce dossier**

---

## 💻 ÉTAPE 2 : Prérequis sur votre machine

### A. Installer Node.js (si pas déjà fait)

1. Allez sur https://nodejs.org
2. Téléchargez la version LTS (recommandée)
3. Installez-la
4. Vérifiez l'installation :
   ```bash
   node --version
   npm --version
   ```

### B. Installer EAS CLI

Ouvrez votre terminal (CMD sur Windows, Terminal sur Mac/Linux) :

```bash
npm install -g eas-cli
```

Vérifiez l'installation :
```bash
eas --version
```

---

## 🔐 ÉTAPE 3 : Se connecter à Expo

Dans votre terminal, naviguez vers le dossier du projet :

```bash
cd C:/Kwezi/frontend
# ou sur Mac/Linux
cd ~/Kwezi/frontend
```

Connectez-vous à Expo :

```bash
eas login
```

**Entrez vos identifiants :**
- Email : ambdi97@hotmail.fr
- Mot de passe : [votre mot de passe]

---

## 📦 ÉTAPE 4 : Installer les dépendances

```bash
npm install
# ou si vous utilisez yarn
yarn install
```

**Temps estimé :** 2-5 minutes

---

## 🏗️ ÉTAPE 5 : Configurer le projet EAS

```bash
eas build:configure
```

**Répondez aux questions :**

1. **"Would you like to automatically create an EAS project for @[votre-username]/kwezi?"**
   → Tapez : `Y` (Yes)

2. **"Generate a new Android Keystore?"**
   → Tapez : `Y` (Yes)

EAS va créer un projet et générer automatiquement une clé de signature.

---

## 🚀 ÉTAPE 6 : Lancer le build de production

```bash
eas build --platform android --profile production
```

**Ce qui va se passer :**

1. **Analyse du projet** (30 secondes)
2. **Upload vers les serveurs Expo** (2-5 minutes selon votre connexion)
   ```
   Uploading...
   [========================================] 100%
   ```

3. **Build sur les serveurs Expo** (10-20 minutes)
   ```
   Build in progress...
   You'll receive an email when it's done
   ```

4. **Notification par email**
   - Expo vous enverra un email quand c'est terminé
   - Le lien de téléchargement sera dans l'email

**Vous pouvez fermer le terminal pendant le build !**

---

## 📥 ÉTAPE 7 : Télécharger le fichier AAB

### Option A : Depuis le terminal

Quand le build est terminé, téléchargez-le :

```bash
eas build:download --platform android --profile production
```

Le fichier sera téléchargé dans le dossier actuel :
```
kwezi-1.0.0-[build-id].aab
```

### Option B : Depuis le dashboard Expo

1. Allez sur https://expo.dev
2. Connectez-vous
3. Cliquez sur votre projet "kwezi"
4. Allez dans "Builds"
5. Cliquez sur "Download" pour le dernier build Android

---

## ✅ VÉRIFICATION DU FICHIER AAB

Vous devriez avoir un fichier :
- **Nom :** `kwezi-1.0.0-[build-id].aab`
- **Taille :** ~30-60 MB
- **Format :** Android App Bundle

**Gardez ce fichier précieusement !**

---

## 🎯 ÉTAPE 8 : Uploader sur Play Console

Maintenant que vous avez le fichier AAB :

1. **Allez sur https://play.google.com/console**
2. **Créez votre application "Kwezi"**
3. **Allez dans Production → Créer une version**
4. **Uploadez le fichier AAB**
5. **Remplissez la fiche** (tous les textes sont dans `/app/GUIDE_PUBLICATION_PLAY_STORE.md`)
6. **Soumettez pour review**

---

## 📋 RÉSUMÉ DES COMMANDES

```bash
# 1. Installer EAS CLI
npm install -g eas-cli

# 2. Naviguer vers le projet
cd C:/Kwezi/frontend

# 3. Se connecter
eas login

# 4. Installer les dépendances
npm install

# 5. Configurer EAS
eas build:configure

# 6. Lancer le build
eas build --platform android --profile production

# 7. Télécharger le AAB (quand terminé)
eas build:download --platform android --profile production
```

---

## ⏱️ TEMPS ESTIMÉS

| Étape | Temps |
|-------|-------|
| Télécharger le projet | 5 min |
| Installer Node.js | 5 min |
| Installer EAS CLI | 2 min |
| Se connecter à Expo | 1 min |
| Installer les dépendances | 3 min |
| Configurer EAS | 2 min |
| Upload vers Expo | 3 min |
| **Build sur serveurs Expo** | **15-25 min** |
| Télécharger AAB | 2 min |
| **TOTAL** | **~40 minutes** |

---

## 🆘 PROBLÈMES COURANTS

### Problème 1 : "Command not found: eas"

**Solution :**
```bash
npm install -g eas-cli
# Redémarrez votre terminal
```

### Problème 2 : "Error: Cannot find module..."

**Solution :**
```bash
cd /chemin/vers/frontend
npm install
```

### Problème 3 : "Build failed"

**Causes possibles :**
- Connexion internet interrompue
- Fichiers manquants

**Solution :**
1. Vérifiez que tous les fichiers sont présents
2. Relancez : `eas build --platform android --profile production`

### Problème 4 : "Authentication error"

**Solution :**
```bash
eas logout
eas login
```

### Problème 5 : "Package name already exists"

C'est normal ! Ça signifie que votre package name est unique.

---

## 📞 SUIVRE L'AVANCEMENT DU BUILD

### Pendant le build :

1. **Dans le terminal :**
   - Vous verrez une barre de progression
   - Un lien vers le dashboard Expo

2. **Sur le dashboard Expo :**
   - Allez sur https://expo.dev
   - Connectez-vous
   - Cliquez sur votre projet
   - Onglet "Builds"
   - Vous verrez le statut en temps réel

3. **Par email :**
   - Vous recevrez un email quand c'est terminé
   - Avec le lien de téléchargement

---

## 🎉 APRÈS LE BUILD

Une fois le fichier AAB téléchargé :

1. ✅ Vous avez le fichier `kwezi-1.0.0.aab`
2. ⏳ Uploadez-le sur Play Console
3. ⏳ Remplissez la fiche (guide fourni)
4. ⏳ Soumettez pour review (1-7 jours)
5. 🎊 Publication !

---

## 📄 FICHIERS IMPORTANTS À VÉRIFIER

Avant de lancer le build, assurez-vous d'avoir ces fichiers :

```
frontend/
├── app.json ✅ (configuré avec package name)
├── eas.json ✅ (configuré pour production)
├── package.json ✅
├── .env ✅
├── app/
│   ├── _layout.tsx
│   ├── index.tsx
│   ├── games.tsx
│   ├── learn.tsx
│   └── ... (tous les autres écrans)
├── assets/
│   └── audio/ (tous les fichiers audio)
├── components/
├── contexts/
└── utils/
```

---

## 🔑 CLÉS DE SIGNATURE

**Important :** EAS génère automatiquement une clé de signature (keystore) et la stocke de manière sécurisée.

Vous n'avez **rien à faire** pour la gestion des clés !

EAS s'occupe de tout :
- ✅ Génération
- ✅ Stockage sécurisé
- ✅ Signature du AAB
- ✅ Gestion pour les futures mises à jour

---

## 💡 CONSEILS

1. **Gardez le terminal ouvert** pendant l'upload (2-5 min)
2. **Pas besoin d'attendre le build** (10-20 min) - vous pouvez fermer
3. **Surveillez votre email** pour la notification
4. **Gardez précieusement le fichier AAB** une fois téléchargé

---

**Guide créé le 15 octobre 2025**  
**Pour l'application Kwezi**  
**Package name : com.mahoraiseducation.kwezi**
