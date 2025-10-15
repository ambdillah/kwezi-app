# 🏗️ Instructions pour créer le Build de Production
## Application Kwezi - Build AAB pour Google Play Store

**Date :** 15 octobre 2025  
**Package Name :** `com.mahoraiseducation.kwezi` ✅  
**Version :** 1.0.0 (Version Code: 1)

---

## ✅ CONFIGURATION COMPLÉTÉE

J'ai déjà configuré :
- ✅ Package name : `com.mahoraiseducation.kwezi`
- ✅ Nom de l'app : "Kwezi"
- ✅ Version : 1.0.0
- ✅ Fichier `app.json` mis à jour
- ✅ Fichier `eas.json` créé

---

## 📋 ÉTAPES POUR CRÉER LE BUILD

### Méthode 1 : Build avec EAS (Expo Application Services) - RECOMMANDÉ

Cette méthode est la plus simple et ne nécessite pas de configuration locale complexe.

#### Étape 1 : Créer un compte Expo (si vous n'en avez pas)

1. Allez sur [expo.dev](https://expo.dev)
2. Cliquez sur "Sign up"
3. Créez un compte gratuit avec :
   - Email
   - Ou GitHub
   - Ou Google

**Note :** Le plan gratuit permet de créer des builds Android.

---

#### Étape 2 : Installer EAS CLI sur votre ordinateur

**Sur votre machine locale :**

```bash
# Installer EAS CLI globalement
npm install -g eas-cli

# Vérifier l'installation
eas --version
```

---

#### Étape 3 : Se connecter à Expo

```bash
# Se connecter avec votre compte Expo
eas login

# Entrez votre email et mot de passe
```

---

#### Étape 4 : Télécharger les fichiers du projet

Vous devez télécharger le dossier `/app/frontend/` sur votre ordinateur local.

**Fichiers importants à inclure :**
- `app.json` (configuré)
- `eas.json` (configuré)
- `package.json`
- Tout le dossier `app/`
- Tout le dossier `assets/`
- Tout le dossier `components/`
- Tout le dossier `contexts/`
- Tout le dossier `utils/`

---

#### Étape 5 : Lancer le build de production

**Dans le dossier du projet sur votre machine :**

```bash
# Naviguer vers le dossier frontend
cd /chemin/vers/frontend

# Lancer le build de production Android
eas build --platform android --profile production
```

**Ce qui va se passer :**

1. EAS va analyser votre projet
2. Il va vous demander de configurer le projet (première fois uniquement)
3. Répondez aux questions :
   - **"Would you like to automatically create an EAS project?"** → `Yes`
   - **"Generate a new Android Keystore?"** → `Yes` (EAS gère automatiquement)
4. Le build démarre sur les serveurs Expo (cela prend 10-20 minutes)
5. Vous recevrez un email quand c'est terminé
6. Un lien de téléchargement du fichier AAB sera disponible

---

#### Étape 6 : Télécharger le fichier AAB

Une fois le build terminé :

```bash
# Télécharger le fichier AAB
eas build:download --platform android --profile production
```

Ou cliquez sur le lien dans l'email que vous avez reçu.

**Vous obtiendrez un fichier :** `kwezi-1.0.0-build-xxx.aab`

---

### Méthode 2 : Build local (Plus complexe, pour développeurs expérimentés)

Si vous préférez ne pas utiliser EAS, vous pouvez faire un build local.

**Prérequis :**
- Android Studio installé
- Java JDK 17 installé
- Android SDK configuré
- Variables d'environnement configurées

**Commandes :**

```bash
# Installer les dépendances
cd /app/frontend
yarn install

# Pré-build Expo
npx expo prebuild --platform android --clean

# Build avec Gradle
cd android
./gradlew bundleRelease

# Le fichier AAB sera dans :
# android/app/build/outputs/bundle/release/app-release.aab
```

⚠️ **Note :** Cette méthode est beaucoup plus complexe et sujette à erreurs. Je recommande EAS.

---

## 🔑 GESTION DES CLÉS DE SIGNATURE

### Avec EAS (Automatique) - RECOMMANDÉ

EAS gère automatiquement les keystores pour vous :
- ✅ Génération automatique
- ✅ Stockage sécurisé
- ✅ Gestion des certificats
- ✅ Pas de risque de perte

**Vous n'avez rien à faire !**

### Build local (Manuel)

Si vous faites un build local, vous devrez :
1. Générer un keystore
2. Le protéger (NE JAMAIS LE PERDRE)
3. Le configurer dans `gradle.properties`

---

## 📤 UPLOADER LE AAB SUR PLAY CONSOLE

Une fois que vous avez le fichier AAB :

### Étape 1 : Se connecter à Play Console

1. Allez sur [play.google.com/console](https://play.google.com/console)
2. Cliquez sur votre application Kwezi (ou créez-la si ce n'est pas fait)

---

### Étape 2 : Créer une version de production

1. Dans le menu latéral, cliquez sur **"Production"**
2. Cliquez sur **"Créer une version"**
3. Cliquez sur **"Importer"** pour uploader le fichier AAB
4. Sélectionnez votre fichier `kwezi-1.0.0-build-xxx.aab`
5. Attendez que l'upload soit terminé (peut prendre quelques minutes)

---

### Étape 3 : Remplir les détails de la version

Google va afficher un résumé du fichier uploadé :

```
Package name : com.mahoraiseducation.kwezi ✅
Version code : 1 ✅
Version name : 1.0.0 ✅
```

**Ajoutez les notes de version :**

```
Version 1.0.0 - Première version

🎉 Bienvenue sur Kwezi !

Cette première version inclut :
- 636+ mots en shimaoré et kibouchi
- Plus de 1280 audio authentiques
- 4 jeux d'apprentissage interactifs
- Quiz sur la culture de Mayotte
- Mode gratuit (250 mots) et Premium (accès complet)

Merci de nous faire confiance pour préserver les langues de Mayotte ! 🇾🇹
```

---

### Étape 4 : Vérifier et enregistrer

1. Vérifiez que tout est correct
2. Cliquez sur **"Enregistrer"**
3. Cliquez sur **"Examiner la version"**
4. Google va analyser votre AAB (quelques minutes)

---

### Étape 5 : Passer en revue

Google affichera une checklist de tout ce qui doit être complété avant publication :

**À compléter (si pas déjà fait) :**
- ✅ Description de l'application
- ✅ Captures d'écran
- ✅ Icône 512x512
- ✅ Bannière 1024x500
- ✅ Politique de confidentialité
- ✅ Classification du contenu
- ✅ Tarification

Tout cela est détaillé dans `/app/GUIDE_PUBLICATION_PLAY_STORE.md`

---

## ⚠️ PROBLÈMES COURANTS ET SOLUTIONS

### Problème 1 : "EAS CLI not found"

**Solution :**
```bash
npm install -g eas-cli
# Ou avec yarn
yarn global add eas-cli
```

---

### Problème 2 : "Not logged in"

**Solution :**
```bash
eas login
# Entrez vos identifiants Expo
```

---

### Problème 3 : "Build failed - Missing dependencies"

**Solution :**
```bash
cd /app/frontend
yarn install
# Puis relancez le build
eas build --platform android --profile production
```

---

### Problème 4 : "AAB file is invalid"

**Causes possibles :**
- Package name incorrect
- Version code en doublon
- Signature manquante

**Solution :**
- Vérifiez `app.json`
- Vérifiez que le package name est bien `com.mahoraiseducation.kwezi`
- Relancez le build avec EAS

---

## 🎯 CHECKLIST AVANT BUILD

Avant de lancer le build, vérifiez :

- [ ] ✅ Package name configuré : `com.mahoraiseducation.kwezi`
- [ ] ✅ Version définie : 1.0.0 (code: 1)
- [ ] ✅ Nom de l'app : "Kwezi"
- [ ] ✅ Icône de l'app présente dans `assets/images/icon.png`
- [ ] ✅ Compte Expo créé
- [ ] ✅ EAS CLI installé
- [ ] ✅ Connecté à Expo (`eas login`)
- [ ] ✅ Toutes les dépendances installées (`yarn install`)

---

## 📊 TEMPS ESTIMÉS

| Étape | Temps |
|-------|-------|
| Configuration (déjà faite) | ✅ Complété |
| Installation EAS CLI | 2 minutes |
| Connexion Expo | 1 minute |
| Lancement du build | 1 minute |
| **Build sur serveurs Expo** | **10-20 minutes** ⏱️ |
| Téléchargement AAB | 1 minute |
| Upload sur Play Console | 2-5 minutes |
| **TOTAL** | **~20-30 minutes** |

---

## 🆘 BESOIN D'AIDE ?

### Ressources officielles :

- **Documentation EAS Build :** https://docs.expo.dev/build/introduction/
- **Guide Android :** https://docs.expo.dev/build-reference/android-builds/
- **Forum Expo :** https://forums.expo.dev/

### Problème avec le build ?

Partagez-moi :
1. Le message d'erreur complet
2. Le fichier `eas.json`
3. Le fichier `app.json`
4. Les logs du build

---

## 🎉 PROCHAINE ÉTAPE APRÈS LE BUILD

Une fois que vous avez le fichier AAB :

1. ✅ Uploadez-le sur Play Console
2. ✅ Complétez la fiche du Store (guide fourni)
3. ✅ Ajoutez les captures d'écran
4. ✅ Soumettez pour review
5. ⏳ Attendez 1-7 jours
6. 🎉 Publication !

---

## 📝 RÉSUMÉ DES COMMANDES

```bash
# 1. Installer EAS CLI
npm install -g eas-cli

# 2. Se connecter
eas login

# 3. Naviguer vers le projet
cd /chemin/vers/frontend

# 4. Installer les dépendances
yarn install

# 5. Lancer le build
eas build --platform android --profile production

# 6. Télécharger le AAB (quand terminé)
eas build:download --platform android --profile production
```

---

**Configuration terminée ✅**  
**Package name :** `com.mahoraiseducation.kwezi`  
**Prêt pour le build !** 🚀

---

*Guide créé le 15 octobre 2025 pour l'application Kwezi*
