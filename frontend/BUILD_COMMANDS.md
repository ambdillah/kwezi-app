# 🚀 COMMANDES DE BUILD APK - Kwezi Application

## ✅ ÉTAT ACTUEL: PRÊT POUR BUILD

Toutes les corrections ont été appliquées avec succès:
- ✅ Expo SDK 50 installé
- ✅ React Native 0.73.6
- ✅ URL Backend: https://kwezi-backend.onrender.com
- ✅ Configuration optimisée

---

## 🎯 OPTION 1: BUILD EAS (RECOMMANDÉ - 10-15 MINUTES)

### Méthode A: Avec Compte Expo (Gratuit)

```bash
# 1. Se positionner dans le dossier frontend
cd /app/frontend

# 2. Se connecter à Expo (créer un compte sur expo.dev si nécessaire)
eas login

# 3. Lancer le build Android
eas build --platform android --profile production

# 4. Attendre 10-15 minutes
# Vous recevrez un lien pour télécharger l'APK
```

### Méthode B: Avec Token Expo (Pour CI/CD)

Si vous avez un token Expo (depuis expo.dev/settings/access-tokens):

```bash
cd /app/frontend

# Définir le token
export EXPO_TOKEN=votre_token_ici

# Lancer le build
eas build --platform android --profile production --non-interactive
```

---

## 🛠️ OPTION 2: BUILD LOCAL (20-30 MINUTES)

### Prérequis:
- Android Studio installé
- Android SDK configuré
- Variables d'environnement:
  ```bash
  export ANDROID_HOME=$HOME/Library/Android/sdk  # ou ~/Android/Sdk sur Linux
  export PATH=$PATH:$ANDROID_HOME/emulator
  export PATH=$PATH:$ANDROID_HOME/platform-tools
  ```

### Commandes:

```bash
cd /app/frontend

# Option A: Avec le script fourni
chmod +x build-local-apk.sh
./build-local-apk.sh

# Option B: Manuel
npx expo prebuild --clean
npx expo run:android --variant release
```

**L'APK sera créé dans**:
```
/app/frontend/android/app/build/outputs/apk/release/app-release.apk
```

---

## 📦 TÉLÉCHARGER ET INSTALLER L'APK

### Sur votre ordinateur:

```bash
# Si build local
cp /app/frontend/android/app/build/outputs/apk/release/app-release.apk ~/Downloads/kwezi-app.apk
```

### Sur votre appareil Android:

**Méthode 1: Via USB**
```bash
# Activer le mode développeur et le débogage USB sur votre téléphone
# Connecter le téléphone via USB
adb devices  # Vérifier que l'appareil est détecté
adb install app-release.apk
```

**Méthode 2: Via Email/Cloud**
- Envoyer l'APK par email à vous-même
- Télécharger sur le téléphone
- Autoriser l'installation d'apps inconnues
- Installer l'APK

**Méthode 3: Via Build EAS**
- EAS vous donne un lien de téléchargement direct
- Scanner le QR code avec votre téléphone
- Télécharger et installer

---

## 🧪 VÉRIFIER LE BUILD AVANT DE LANCER

```bash
cd /app/frontend

# Vérifier la version SDK
grep '"expo"' package.json
# Attendu: "expo": "50"

# Vérifier React Native
grep '"react-native"' package.json
# Attendu: "react-native": "0.73.6"

# Vérifier l'URL backend
grep EXPO_PUBLIC_BACKEND_URL .env
# Attendu: EXPO_PUBLIC_BACKEND_URL=https://kwezi-backend.onrender.com

# Tester le backend
curl https://kwezi-backend.onrender.com/api/health
# Attendu: {"status":"healthy","database":"connected"}

# Vérifier la configuration EAS
cat eas.json
# Node version doit être "18.x"

# Vérifier app.json
grep -A 5 "android" app.json
# Doit contenir: "package": "com.mahoraiseducation.kwezi"
```

---

## 🔍 DIAGNOSTICS SI PROBLÈMES

### Problème: "No credentials found"
```bash
# Solution: Se connecter d'abord
eas login
```

### Problème: "Gradle build failed"
```bash
# Solution: Nettoyer et reconstruire
cd /app/frontend
rm -rf android/build android/app/build
npx expo prebuild --clean
eas build --platform android --profile production --clear-cache
```

### Problème: "SDK location not found"
```bash
# Solution: Créer local.properties
echo "sdk.dir=$ANDROID_HOME" > android/local.properties
```

### Problème: "Node version mismatch"
```bash
# Solution: Utiliser nvm
nvm install 18
nvm use 18
```

---

## 📊 MONITORING DU BUILD

### Build EAS:
```bash
# Voir les builds en cours
eas build:list

# Voir les détails d'un build spécifique
eas build:view [BUILD_ID]

# Annuler un build
eas build:cancel [BUILD_ID]
```

### Build Local:
Les logs s'affichent directement dans le terminal pendant le build.

---

## ✅ CHECKLIST POST-BUILD

Après avoir installé l'APK sur votre appareil, vérifier:

- [ ] L'application démarre sans crash
- [ ] Écran d'accueil s'affiche avec les 4 boutons
- [ ] Navigation fonctionne (Learn, Games, Shop, Premium)
- [ ] Page Learn affiche les mots (au moins 250 en gratuit)
- [ ] Recherche de mots fonctionne
- [ ] Audio se joue correctement
- [ ] Page Games affiche les 4 jeux
- [ ] Jeu "Construire des phrases" se lance
- [ ] Quiz Mayotte fonctionne
- [ ] Page Shop accessible
- [ ] Page Premium affiche €2.90/mois
- [ ] Documents légaux accessibles (Privacy, Terms, Mentions)
- [ ] Pas d'erreurs de connexion backend

---

## 🎉 BUILD RÉUSSI!

Une fois l'APK fonctionnel:

1. **Garder une copie de sauvegarde** de l'APK
2. **Documenter** ce qui fonctionne et ce qui ne fonctionne pas
3. **Préparer** pour la présentation de demain
4. **Optionnel**: Préparer le déploiement sur Google Play Store

---

## 🚑 SUPPORT D'URGENCE

Si vous rencontrez des problèmes critiques:

1. Vérifier `/app/DIAGNOSTIC_COMPLET.md`
2. Vérifier `/app/DEPLOIEMENT_APK_INSTRUCTIONS.md`
3. Consulter les logs EAS: https://expo.dev/accounts/[votre-compte]/builds
4. Forum Expo: https://forums.expo.dev
5. Discord Expo: https://chat.expo.dev

---

**Tout est prêt pour le build ! Bonne chance pour votre présentation demain ! 🚀**
