# 🚀 GUIDE DÉPLOIEMENT KWEZI - ÉTAPE PAR ÉTAPE

## 📦 ÉTAPE 1 : EXTRACTION DES FICHIERS

Sur votre machine locale (Windows/Mac/Linux) :

```bash
# 1. Créer un dossier de travail
mkdir kwezi-deployment
cd kwezi-deployment

# 2. Placer vos 2 fichiers téléchargés dans ce dossier
# - kwezi-code.tar.gz (ou kwezi-frontend-code-final.tar.gz)
# - kwezi-audio.tar.gz (ou kwezi-audio-final.tar.gz)

# 3. Extraire le code
tar -xzf kwezi-*code*.tar.gz

# 4. Extraire les audios (crée automatiquement assets/audio/)
tar -xzf kwezi-*audio*.tar.gz

# 5. Vérifier que tout est là
ls -la
```

**Structure attendue après extraction :**
```
kwezi-deployment/
├── app/
├── assets/
│   └── audio/          ← 1254 fichiers audio
├── components/
├── contexts/
├── data/
├── utils/
├── app.json
├── eas.json
├── package.json
├── tsconfig.json
└── .env
```

---

## 🔧 ÉTAPE 2 : INSTALLATION DES OUTILS NÉCESSAIRES

### A. Node.js (si pas déjà installé)

**Vérifier la version :**
```bash
node --version
```

Si < 18.x, télécharger depuis : https://nodejs.org/

### B. Yarn (recommandé) ou NPM

```bash
# Vérifier Yarn
yarn --version

# Si non installé :
npm install -g yarn
```

### C. Expo CLI & EAS CLI

```bash
# Installer les outils Expo
npm install -g expo-cli eas-cli

# Vérifier l'installation
expo --version
eas --version
```

---

## 📝 ÉTAPE 3 : INSTALLATION DES DÉPENDANCES

```bash
# Dans le dossier kwezi-deployment
yarn install

# ou avec npm
npm install

# Attendre la fin (peut prendre 2-5 minutes)
```

---

## ⚙️ ÉTAPE 4 : CONFIGURATION DU BACKEND

### Modifier le fichier .env

```bash
# Ouvrir le fichier .env
nano .env
# ou
code .env    # Si vous utilisez VS Code
```

**Modifier cette ligne :**
```env
# AVANT (exemple)
EXPO_PUBLIC_BACKEND_URL=https://votre-backend.com

# APRÈS (votre URL réelle)
EXPO_PUBLIC_BACKEND_URL=https://kwezi-api.votredomaine.com
```

**⚠️ IMPORTANT :** Remplacez par l'URL de votre backend déployé

**Si vous n'avez pas encore de backend déployé :**
- Option 1 : Déployer sur Render.com, Railway.app, ou Heroku
- Option 2 : Utiliser l'URL actuelle temporairement (session Emergent)

---

## 🔐 ÉTAPE 5 : CRÉER UN COMPTE EXPO

Si vous n'avez pas encore de compte :

```bash
# Se connecter à Expo
eas login

# Entrer email et mot de passe
# Si pas de compte : Créer sur https://expo.dev/signup
```

---

## 📱 ÉTAPE 6 : CONFIGURER LE PROJET EXPO

```bash
# Initialiser le projet avec EAS (si demandé)
eas build:configure

# Vérifier app.json (déjà configuré)
cat app.json
```

**Vérifier ces paramètres dans app.json :**
```json
{
  "expo": {
    "name": "Kwezi",
    "slug": "kwezi",
    "version": "1.0.0",
    "android": {
      "package": "com.mahoraiseducation.kwezi",
      "versionCode": 1
    }
  }
}
```

---

## 🏗️ ÉTAPE 7 : BUILDER L'APK ANDROID

### Option A : Build APK (pour test direct)

```bash
# Lancer le build APK
eas build --platform android --profile production

# Suivre les instructions à l'écran :
# - Confirmer le build
# - Sélectionner "Build an APK"
# - Attendre 10-20 minutes
```

### Option B : Build AAB (pour Google Play Store)

```bash
# Modifier eas.json pour AAB
nano eas.json

# Changer "apk" en "aab" :
{
  "build": {
    "production": {
      "android": {
        "buildType": "aab"
      }
    }
  }
}

# Lancer le build
eas build --platform android --profile production
```

**⚠️ Pour Google Play Store, utilisez AAB (Android App Bundle)**

---

## 📥 ÉTAPE 8 : TÉLÉCHARGER L'APK/AAB

Une fois le build terminé :

```bash
# Vous recevrez un lien dans le terminal :
✓ Build completed!
URL: https://expo.dev/accounts/[votre-compte]/builds/[build-id]
```

**Cliquez sur le lien pour :**
1. Voir le status du build
2. Télécharger l'APK/AAB
3. Voir les logs si erreur

---

## 🧪 ÉTAPE 9 : TESTER L'APPLICATION

### Test sur appareil physique (APK)

```bash
# Transférer l'APK sur votre téléphone Android
# Installer et tester toutes les fonctionnalités :
- ✅ Apprentissage des mots
- ✅ Lecture audio authentique
- ✅ Jeux éducatifs
- ✅ Système freemium
- ✅ Boutique PDF
```

### Test sur émulateur

```bash
# Installer Android Studio avec émulateur
# Glisser-déposer l'APK sur l'émulateur
```

---

## 🏪 ÉTAPE 10 : PUBLIER SUR GOOGLE PLAY STORE

### A. Créer un compte développeur Google Play

1. Aller sur : https://play.google.com/console/signup
2. Payer les frais one-time : $25
3. Compléter le profil développeur

### B. Créer l'application

1. **Dans Google Play Console :**
   - Cliquer "Créer une application"
   - Nom : **Kwezi - Apprendre le Shimaoré**
   - Langue par défaut : Français
   - App gratuite

2. **Uploader l'AAB :**
   - Aller dans "Production" → "Créer une version"
   - Uploader le fichier .aab
   - Définir le nom de version : 1.0.0

3. **Remplir la fiche Play Store :**
   - Description courte (80 caractères max)
   - Description complète
   - Screenshots (au moins 2)
   - Icône haute résolution (512x512)
   - Bannière (1024x500)

4. **Contenu et classification :**
   - Catégorie : Éducation
   - Public cible : Tout public
   - Contenu approprié pour les enfants : Oui

5. **Politique de confidentialité :**
   - URL de votre landing page : https://votredomaine.com/privacy-policy

6. **Soumettre pour review :**
   - Vérifier tous les onglets (✅ verts)
   - Cliquer "Publier"
   - Attente review : 1-3 jours

---

## 📋 CHECKLIST FINALE

Avant de publier, vérifier :

- [ ] ✅ Backend configuré et déployé
- [ ] ✅ URL backend correcte dans .env
- [ ] ✅ Build AAB réussi
- [ ] ✅ Tests effectués sur appareil réel
- [ ] ✅ Compte développeur Google créé ($25 payés)
- [ ] ✅ Screenshots préparés (2 minimum)
- [ ] ✅ Icône haute résolution prête
- [ ] ✅ Description de l'app rédigée
- [ ] ✅ Politique de confidentialité accessible
- [ ] ✅ Landing page en ligne

---

## 🆘 DÉPANNAGE COMMUN

### Erreur : "Command not found: eas"

```bash
# Réinstaller EAS CLI
npm install -g eas-cli

# Redémarrer le terminal
```

### Erreur : "Build failed"

```bash
# Voir les logs détaillés
eas build:list

# Reconstruire avec cache nettoyé
eas build --platform android --profile production --clear-cache
```

### Erreur : "Cannot find module"

```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules
yarn install
```

### L'APK ne s'installe pas sur Android

```bash
# Activer "Sources inconnues" sur Android :
# Paramètres → Sécurité → Autoriser sources inconnues
```

---

## 📞 RESSOURCES ET SUPPORT

### Documentation officielle
- Expo : https://docs.expo.dev/
- EAS Build : https://docs.expo.dev/build/introduction/
- Google Play : https://support.google.com/googleplay/android-developer/

### Outils utiles
- Tester sur émulateur : https://developer.android.com/studio
- Créer screenshots : https://screenshots.pro/
- Icônes app : https://easyappicon.com/

### Votre documentation
- Guide complet : `GUIDE_DEPLOIEMENT_FINAL.md` (dans l'archive)
- Rapports techniques : Consultables dans `/app/`

---

## ✨ FÉLICITATIONS !

Une fois ces étapes complétées, votre application Kwezi sera :
- ✅ Compilée en APK/AAB
- ✅ Testée et fonctionnelle
- ✅ Publiée sur Google Play Store
- ✅ Accessible à des millions d'utilisateurs

**Bon déploiement ! 🚀**
