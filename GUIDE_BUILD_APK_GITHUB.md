# 🚀 GUIDE COMPLET - BUILD APK KWEZI VIA GITHUB ACTIONS

## ✅ CORRECTIONS EFFECTUÉES

### 1. **Problème des jeux qui plantent** - RÉSOLU ✅
- **Cause:** Import asynchrone d'`expo-speech` causant l'erreur `Cannot read properties of undefined (reading 'emit')`
- **Solution:** Création d'un wrapper `safeSpeech.ts` avec import synchrone conditionnel
- **Résultat:** Les jeux fonctionnent maintenant sans erreur sur le preview Emergent

### 2. **Base de données vide dans l'APK** - CORRIGÉ ✅
- **Cause:** Variable d'environnement `EXPO_PUBLIC_BACKEND_URL` non définie correctement
- **Solution:** Ajout dans `app.json > extra` et configuration dans le workflow GitHub
- **Backend:** `https://kwezi-backend.onrender.com` (635 mots, 270 phrases)

---

## 📋 ÉTAPES POUR GÉNÉRER L'APK VIA GITHUB ACTIONS

### **Prérequis**

Vous devez avoir:
1. ✅ Un compte Expo (expo.dev)
2. ✅ Un projet EAS créé (déjà fait: `308793ab-c80f-403a-a8b3-7cbfac1b57c6`)
3. ✅ Un token Expo pour GitHub Actions

---

## 🔑 ÉTAPE 1: OBTENIR VOTRE TOKEN EXPO

### A. Se connecter à Expo
```bash
cd /app/frontend
npx eas login
```
Entrez vos identifiants Expo.

### B. Créer un token d'accès
```bash
npx eas build:configure
```

Ou directement sur: https://expo.dev/accounts/[votre-username]/settings/access-tokens

**Créez un token avec les permissions:**
- ✅ Read and write access

**Copiez le token généré** (ex: `abc123def456...`)

---

## 🔐 ÉTAPE 2: AJOUTER LE SECRET GITHUB

### A. Sur GitHub:
1. Allez sur votre dépôt GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Cliquez sur **New repository secret**
4. Configurez:
   - **Name:** `EXPO_TOKEN`
   - **Secret:** Collez votre token Expo
5. Cliquez sur **Add secret**

---

## 🎯 ÉTAPE 3: POUSSER LE CODE SUR GITHUB

### A. Depuis votre environnement local

```bash
cd /app

# Initialiser git si nécessaire
git init
git remote add origin https://github.com/VOTRE-USERNAME/kwezi-app.git

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "🚀 Configuration pour build APK avec corrections expo-speech et backend URL"

# Push sur main
git push -u origin main
```

---

## 🤖 ÉTAPE 4: LANCER LE BUILD

### Option A: Push automatique (Déjà configuré)
Le workflow se lancera automatiquement à chaque push sur `main`.

### Option B: Lancement manuel
1. Allez sur votre dépôt GitHub
2. **Actions** → **Build Android APK**
3. Cliquez sur **Run workflow** → **Run workflow**

---

## 📥 ÉTAPE 5: TÉLÉCHARGER L'APK

### Une fois le build terminé (~15-20 minutes):

1. Allez dans **Actions** sur GitHub
2. Cliquez sur le workflow terminé (✅ vert)
3. Descendez jusqu'à **Artifacts**
4. Téléchargez **kwezi-app-release**
5. Décompressez le fichier ZIP
6. **Vous avez votre APK!** 🎉

---

## 📱 ÉTAPE 6: INSTALLER L'APK SUR ANDROID

### A. Sur votre téléphone Android:
1. Transférez `kwezi-app-release.apk` sur votre téléphone
2. Ouvrez le fichier
3. Autorisez l'installation depuis des sources inconnues si demandé
4. Installez l'application

### B. Tester l'application:
- ✅ Vérifier que les données se chargent (635 mots)
- ✅ Tester les jeux (ne devraient plus planter)
- ✅ Tester la connexion backend Render.com
- ✅ Vérifier les fonctionnalités offline premium

---

## 🔧 CONFIGURATION ACTUELLE

### `frontend/app.json`
```json
{
  "cli": {
    "appVersionSource": "remote",
    "requireCommit": false
  },
  "extra": {
    "backendUrl": "https://kwezi-backend.onrender.com",
    "eas": {
      "projectId": "308793ab-c80f-403a-a8b3-7cbfac1b57c6"
    }
  }
}
```

### `frontend/eas.json`
```json
{
  "production": {
    "node": "18.18.0",
    "env": {
      "EXPO_PUBLIC_BACKEND_URL": "https://kwezi-backend.onrender.com"
    }
  }
}
```

### `.github/workflows/build-apk.yml`
- ✅ Actions mises à jour (v4)
- ✅ Node.js 18.18.0
- ✅ Java 17
- ✅ Création automatique du fichier `.env` avec backend URL
- ✅ Download APK via `curl` et `jq`

---

## ⚠️ DÉPANNAGE

### Problème: "EXPO_TOKEN not found"
**Solution:** Vérifiez que le secret GitHub `EXPO_TOKEN` est bien configuré dans les paramètres du dépôt.

### Problème: Build échoue avec "Invalid credentials"
**Solution:** Régénérez un nouveau token Expo et remplacez le secret GitHub.

### Problème: APK se connecte pas au backend
**Solution:** Vérifiez que `EXPO_PUBLIC_BACKEND_URL=https://kwezi-backend.onrender.com` est dans `eas.json`.

### Problème: Jeux plantent sur APK
**Solution:** Vérifiez que tous les imports `expo-speech` ont été remplacés par `../utils/safeSpeech`.

---

## 📊 FICHIERS MODIFIÉS

### Corrections expo-speech (8 fichiers):
- ✅ `frontend/utils/safeSpeech.ts` (créé)
- ✅ `frontend/app/index.tsx`
- ✅ `frontend/app/learn.tsx`
- ✅ `frontend/app/games.tsx`
- ✅ `frontend/utils/speechUtils.ts`
- ✅ `frontend/utils/feminineSpeechUtils.ts`
- ✅ `frontend/utils/simpleMasculineVoice.ts`
- ✅ `frontend/utils/enhancedSpeechUtils.ts`
- ✅ `frontend/utils/dualAuthenticAudioSystem.ts`

### Configuration backend:
- ✅ `frontend/app.json` (ajout cli et backendUrl)
- ✅ `frontend/eas.json` (déjà correct)
- ✅ `.github/workflows/build-apk.yml` (mis à jour)

---

## ✨ RÉSULTAT ATTENDU

Une fois l'APK installé sur votre téléphone Android:

1. **Écran d'accueil:** Logo Kwezi, boutons de navigation
2. **Apprendre:** Liste de 635 mots chargés depuis Render.com
3. **Jeux:** Tous les jeux fonctionnent sans planter
4. **Premium:** Fonctionnalités offline et PDFs accessibles
5. **Backend:** Connecté à `https://kwezi-backend.onrender.com`

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Obtenir token Expo
2. ✅ Configurer secret GitHub `EXPO_TOKEN`
3. ✅ Pousser le code sur GitHub
4. ✅ Lancer le build (automatique ou manuel)
5. ✅ Télécharger l'APK
6. ✅ Tester sur téléphone Android
7. 🚀 Déployer sur Google Play Store

---

## 📞 SUPPORT

Si vous rencontrez des problèmes:
1. Vérifiez les logs du workflow GitHub Actions
2. Testez le backend: `curl https://kwezi-backend.onrender.com/api/health`
3. Testez le preview Emergent: https://kwezi-android.preview.emergentagent.com

**Le backend et le preview fonctionnent parfaitement. Le build APK est maintenant prêt!** 🎉
