# 🚀 GUIDE COMPLET - Déploiement APK via GitHub Actions

## ✅ **STATUT : TOUT EST PRÊT POUR LE DÉPLOIEMENT**

---

## 📋 **CE QUI A DÉJÀ ÉTÉ FAIT**

✅ **Workflow GitHub Actions créé** : `.github/workflows/build-apk.yml`
✅ **Code optimisé** : Expo SDK 50, React Native 0.73.6
✅ **Backend configuré** : https://kwezi-backend.onrender.com
✅ **Toutes dépendances alignées**
✅ **Configuration EAS prête**

---

## 🎯 **ÉTAPES À SUIVRE (20 MINUTES MAX)**

### **ÉTAPE 1 : Pousser le code sur GitHub** ⏱️ 3 min

**Via l'interface Emergent** :

1. Dans l'interface Emergent, cherchez le bouton **GitHub** (icône en haut)
2. Cliquez dessus
3. **Connectez votre compte GitHub** si pas déjà fait
4. **Créez un nouveau repository** :
   - Nom : `kwezi-app`
   - Visibilité : Privé (recommandé) ou Public
5. **Poussez le code** (bouton "Push to GitHub")

**OU via ligne de commande** (si vous préférez) :

```bash
# Créez d'abord un repo sur github.com
# Puis :
cd /app
git remote add origin https://github.com/VOTRE_USERNAME/kwezi-app.git
git push -u origin main
```

---

### **ÉTAPE 2 : Obtenir un Token Expo** ⏱️ 5 min

**IMPORTANT** : La page tokens Expo est bugée dans certains navigateurs.

**Solutions (par ordre de préférence)** :

#### **Solution A : Autre navigateur/mode incognito** ⭐

1. Ouvrez un **nouveau navigateur** (Chrome, Firefox, Safari, Edge)
2. Allez en **mode Incognito/Privé**
3. Allez sur : https://expo.dev/login
4. Connectez-vous avec : **ambd97** / votre mot de passe
5. Allez sur : https://expo.dev/accounts/ambd97/settings/access-tokens
6. Cliquez sur **"Create Token"**
7. Nom du token : `GitHub Actions Build`
8. **COPIEZ LE TOKEN** (vous ne pourrez plus le revoir !)

#### **Solution B : Nouveau compte Expo**

Si la Solution A ne marche toujours pas :

1. Allez sur : https://expo.dev/signup
2. Créez un **nouveau compte** (utilisez un autre email)
3. Une fois connecté, allez dans **Settings** → **Access Tokens**
4. Créez un token : `GitHub Actions Build`
5. **COPIEZ LE TOKEN**

**SI vous créez un nouveau compte** :
- Vous devrez créer un nouveau projet Expo
- Exécutez dans le terminal :
  ```bash
  cd /app/frontend
  npx eas init
  ```
- Cela générera un nouveau `projectId`
- Copiez ce `projectId` et mettez à jour `app.json`

---

### **ÉTAPE 3 : Configurer le Secret GitHub** ⏱️ 2 min

1. Allez sur votre repo GitHub : `https://github.com/VOTRE_USERNAME/kwezi-app`
2. Cliquez sur **Settings** (onglet en haut)
3. Dans le menu de gauche : **Secrets and variables** → **Actions**
4. Cliquez sur **"New repository secret"** (bouton vert)
5. Remplissez :
   - **Name** : `EXPO_TOKEN`
   - **Secret** : *[Collez le token Expo que vous avez copié]*
6. Cliquez sur **"Add secret"**

✅ **Le secret est maintenant configuré !**

---

### **ÉTAPE 4 : Lancer le Build GitHub Actions** ⏱️ 1 min + 10-15 min d'attente

1. Sur votre repo GitHub, allez dans l'onglet **Actions**
2. Vous verrez le workflow **"Build Android APK"**
3. Cliquez dessus
4. Cliquez sur **"Run workflow"** (bouton bleu à droite)
5. Sélectionnez la branche **"main"**
6. Cliquez sur **"Run workflow"** (bouton vert)

**Le build démarre !** 🚀

⏰ **Attendez 10-15 minutes** pendant que GitHub Actions :
- Installe Node.js, Java, Android SDK
- Installe toutes les dépendances
- Build l'APK avec EAS
- Upload l'APK comme artifact

---

### **ÉTAPE 5 : Télécharger votre APK** ⏱️ 2 min

Une fois le build terminé (vous verrez une ✅ verte) :

1. Cliquez sur le **workflow terminé**
2. Scrollez vers le bas jusqu'à la section **"Artifacts"**
3. Vous verrez **"kwezi-app"** avec l'icône de téléchargement
4. **Cliquez pour télécharger** (fichier ZIP)
5. **Décompressez le ZIP**
6. **Votre APK est là !** 🎉

Le fichier s'appelle : `app-release.apk` ou similaire

---

### **ÉTAPE 6 : Installer sur Android** ⏱️ 3 min

**Transférer l'APK sur votre téléphone** :

**Méthode 1 : Email**
1. Envoyez l'APK par email à vous-même
2. Ouvrez l'email sur votre téléphone Android
3. Téléchargez l'APK

**Méthode 2 : USB**
1. Connectez votre téléphone à l'ordinateur via USB
2. Copiez l'APK vers le dossier Downloads de votre téléphone
3. Déconnectez

**Méthode 3 : Google Drive / Dropbox**
1. Uploadez l'APK sur Drive/Dropbox
2. Téléchargez depuis votre téléphone

**Installer l'APK** :

1. Sur votre téléphone, ouvrez **Fichiers** ou **Gestionnaire de fichiers**
2. Trouvez l'APK téléchargé
3. Tapez dessus pour l'installer
4. Si demandé, **autorisez l'installation depuis des sources inconnues** :
   - Paramètres → Sécurité → Sources inconnues → Activer
5. **Installez l'application**
6. **Ouvrez et testez !** 🎉

---

## ✅ **VÉRIFICATION POST-INSTALLATION**

Une fois l'app installée, vérifiez :

- [ ] L'application démarre sans crash
- [ ] Vous voyez l'écran d'accueil avec les 4 boutons
- [ ] Navigation fonctionne (Learn, Games, Shop, Premium)
- [ ] Page **Learn** affiche les mots (au moins 250 en gratuit)
- [ ] **Recherche** de mots fonctionne
- [ ] **Audio** se joue quand vous tapez sur les mots
- [ ] Page **Games** montre les 4 jeux
- [ ] Les jeux se lancent correctement
- [ ] Page **Premium** affiche le prix (€2.90/mois)
- [ ] **Pas d'erreurs de connexion backend**

**Si tout fonctionne : FÉLICITATIONS ! 🎊**

---

## 🆘 **TROUBLESHOOTING**

### ❌ Le workflow GitHub Actions échoue

**Vérifiez** :
1. Le secret `EXPO_TOKEN` est bien configuré
2. Le token Expo est valide (pas expiré)
3. Le `projectId` dans `app.json` correspond à votre compte Expo
4. Consultez les **logs du workflow** pour voir l'erreur exacte

**Solutions** :
- Recréez le token Expo
- Vérifiez que le compte Expo est actif
- Assurez-vous que le `projectId` est correct

---

### ❌ Impossible de créer un token Expo

**Essayez** :
1. **Autre navigateur** (Chrome, Firefox, Safari, Edge)
2. **Mode Incognito/Privé**
3. **Autre appareil** (téléphone, tablette)
4. **Autre connexion Internet** (4G/5G au lieu de WiFi)
5. **Créer un nouveau compte Expo** avec un autre email

---

### ❌ L'APK ne s'installe pas sur Android

**Vérifiez** :
1. **Sources inconnues** autorisées dans Paramètres → Sécurité
2. **Espace de stockage** suffisant (au moins 100 MB libres)
3. **Version Android** compatible (minimum Android 5.0)

**Solutions** :
- Redémarrez votre téléphone
- Supprimez l'ancienne version de l'app si présente
- Essayez d'installer depuis un autre emplacement

---

### ❌ L'app crash au démarrage

**Causes possibles** :
1. Connexion Internet requise (vérifiez WiFi/4G)
2. Backend inaccessible (testez : https://kwezi-backend.onrender.com/api/health)
3. Permissions manquantes

**Solutions** :
- Activez la connexion Internet
- Redémarrez l'app
- Donnez toutes les permissions demandées
- Consultez les logs Android (adb logcat)

---

### ❌ Les mots ne s'affichent pas

**Vérifiez** :
1. **Connexion Internet** active
2. **Backend accessible** : https://kwezi-backend.onrender.com/api/health
3. Pas de pare-feu bloquant

**Solutions** :
- Changez de réseau (WiFi → 4G ou inverse)
- Attendez quelques secondes (chargement initial)
- Redémarrez l'app

---

## 📞 **RESSOURCES & SUPPORT**

### **Documentation locale**
- `/app/INSTRUCTIONS_GITHUB_BUILD.md` : Instructions complètes
- `/app/DIAGNOSTIC_COMPLET.md` : Analyse technique
- `/app/DEPLOIEMENT_APK_INSTRUCTIONS.md` : Options de déploiement

### **Backend API**
- Health : https://kwezi-backend.onrender.com/api/health
- Words : https://kwezi-backend.onrender.com/api/words

### **Support externe**
- Expo Docs : https://docs.expo.dev
- GitHub Actions : https://docs.github.com/en/actions
- Expo Forums : https://forums.expo.dev

---

## 🎯 **RÉSUMÉ - CHECKLIST FINALE**

Avant de lancer le build, assurez-vous que :

- [ ] Code poussé sur GitHub
- [ ] Workflow `.github/workflows/build-apk.yml` est présent dans le repo
- [ ] Token Expo créé et copié
- [ ] Secret `EXPO_TOKEN` configuré sur GitHub
- [ ] `projectId` correct dans `app.json` (si nouveau compte)
- [ ] Workflow lancé manuellement via interface GitHub Actions

**Si tous ces points sont ✅, le build devrait réussir !**

---

## 🎉 **APRÈS LE BUILD RÉUSSI**

Vous aurez un **APK Android fonctionnel** avec :

✅ Application complète Kwezi
✅ 635 mots Shimaoré et Kibouchi
✅ 4 jeux d'apprentissage interactifs
✅ Système audio dual authentique
✅ Backend connecté à Render.com
✅ Système freemium (250 mots gratuits)
✅ Paiement Stripe (€2.90/mois)
✅ Documents légaux intégrés

**PRÊT POUR VOTRE PRÉSENTATION DEMAIN ! 🚀🎊**

---

**Temps total estimé : 20-30 minutes (incluant l'attente du build)**

**Bonne chance pour votre présentation ! 💪**
