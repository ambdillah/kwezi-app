# 🚀 Guide de Déploiement Complet - Application Kwezi

## 📋 Vue d'ensemble

Ce guide vous permettra de déployer votre application Kwezi sur des services cloud **100% GRATUITS** afin que l'APK Android puisse accéder aux données depuis n'importe où.

**Durée totale estimée** : 1h30 - 2h

---

## PHASE 1 : Configuration MongoDB Atlas (15-20 min)

### Étape 1.1 : Créer un compte MongoDB Atlas

1. Allez sur **https://www.mongodb.com/cloud/atlas/register**
2. Inscrivez-vous avec votre compte Gmail
3. Confirmez votre email
4. Sélectionnez **"M0 Free"** (Cluster gratuit)

### Étape 1.2 : Créer un cluster

1. Choisissez un provider : **AWS** (recommandé)
2. Région : **eu-west-3 (Paris)** ou la plus proche
3. Nom du cluster : `kwezi-cluster` (ou laissez par défaut)
4. Cliquez sur **"Create Cluster"** (création : ~3-5 min)

### Étape 1.3 : Configurer l'accès réseau

1. Dans le menu gauche, cliquez sur **"Network Access"**
2. Cliquez sur **"Add IP Address"**
3. Sélectionnez **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Cliquez sur **"Confirm"**

⚠️ **Important** : En production, vous devriez restreindre l'accès, mais pour débuter c'est acceptable.

### Étape 1.4 : Créer un utilisateur de base de données

1. Dans le menu gauche, cliquez sur **"Database Access"**
2. Cliquez sur **"Add New Database User"**
3. Méthode d'authentification : **Password**
4. Nom d'utilisateur : `kwezi_user`
5. Mot de passe : **Générez un mot de passe sécurisé** (notez-le bien !)
   - Exemple : `Kwezi2025Secure!`
6. Database User Privileges : **"Read and write to any database"**
7. Cliquez sur **"Add User"**

### Étape 1.5 : Obtenir l'URL de connexion

1. Retournez sur **"Database"** dans le menu gauche
2. Cliquez sur **"Connect"** sur votre cluster
3. Choisissez **"Connect your application"**
4. Driver : **Python**, Version : **3.12 or later**
5. Copiez l'URL de connexion qui ressemble à :
   ```
   mongodb+srv://kwezi_user:<password>@kwezi-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **Remplacez `<password>` par votre vrai mot de passe**

📝 **Notez cette URL, vous en aurez besoin plus tard !**

### Étape 1.6 : Importer les données

1. Cliquez sur **"Browse Collections"**
2. Cliquez sur **"Add My Own Data"**
3. Database name : `mayotte_app`
4. Collection name : `words`
5. Cliquez sur **"Create"**

**Option A : Import via l'interface web (recommandé pour débuter)**

1. Dans la collection `words`, cliquez sur **"Insert Document"**
2. Allez sur votre environnement Emergent
3. Téléchargez le fichier `/app/backend/db_export.json`
4. Ouvrez ce fichier, copiez le contenu de `"words"` (les 635 documents)
5. Utilisez la fonction "Import JSON" de MongoDB Atlas

**Option B : Import via mongoimport (plus rapide)**

Si vous avez MongoDB installé localement :
```bash
mongoimport --uri "mongodb+srv://kwezi_user:VotreMotDePasse@kwezi-cluster.xxxxx.mongodb.net/mayotte_app" \
  --collection words \
  --file /app/backend/db_export.json \
  --jsonArray
```

Répétez pour les collections `sentences` et `exercises`.

✅ **Phase 1 Terminée** : Votre base de données cloud est prête avec vos 635 mots !

---

## PHASE 2 : Déploiement Backend sur Render.com (20-30 min)

### Étape 2.1 : Créer un compte Render

1. Allez sur **https://render.com/**
2. Cliquez sur **"Get Started"**
3. Inscrivez-vous avec votre compte Gmail ou GitHub
4. Confirmez votre email

### Étape 2.2 : Préparer les fichiers de déploiement

**Note importante** : L'agent IA va créer ces fichiers pour vous dans l'environnement Emergent.

### Étape 2.3 : Créer un nouveau Web Service

1. Dans le dashboard Render, cliquez sur **"New +"**
2. Sélectionnez **"Web Service"**
3. Choisissez **"Build and deploy from a Git repository"**

**Si vous n'avez pas de dépôt Git :**

Option alternative - **Déploiement manuel** :

1. Sur Render, sélectionnez **"Deploy from GitHub"**
2. Si vous n'avez pas de repo, je vais créer une archive pour vous

⚠️ **À ce stade, revenez me voir pour que je crée les fichiers de déploiement !**

### Étape 2.4 : Configurer le service

Une fois le service créé :

1. **Name** : `kwezi-backend`
2. **Region** : `Frankfurt (EU Central)` ou le plus proche
3. **Branch** : `main` (si vous utilisez Git)
4. **Runtime** : `Python 3`
5. **Build Command** : `pip install -r requirements.txt`
6. **Start Command** : `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Étape 2.5 : Configurer les variables d'environnement

Dans **Environment Variables**, ajoutez :

```
MONGO_URL=mongodb+srv://kwezi_user:VotreMotDePasse@kwezi-cluster.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority
DB_NAME=mayotte_app
STRIPE_SECRET_KEY=sk_test_51NE6WPCOUjCnz53N66xEX0NZq3zFOGJiPGR3jlcSPWkPKCvhQSQ9qgRh4C6tUmfZHBCCW
STRIPE_WEBHOOK_SECRET=whsec_BZMfbZbZ48rvUQHdjKvdU5A0z9u2NVJy
```

⚠️ **Remplacez les valeurs MongoDB par les vôtres !**

### Étape 2.6 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Attendez que le déploiement se termine (~5-10 min)
3. Une fois terminé, vous verrez votre URL :
   ```
   https://kwezi-backend.onrender.com
   ```

### Étape 2.7 : Tester le backend

Ouvrez dans votre navigateur :
```
https://kwezi-backend.onrender.com/api/words?limit=10
```

Vous devriez voir vos mots s'afficher en JSON ! ✅

📝 **Notez cette URL, vous en aurez besoin pour reconfigurer l'APK !**

✅ **Phase 2 Terminée** : Votre backend est en ligne !

---

## PHASE 3 : Reconfiguration et Rebuild de l'APK (15-20 min)

### Étape 3.1 : Mettre à jour la configuration frontend

L'agent IA va mettre à jour le fichier `/app/frontend/.env` avec :

```
EXPO_BACKEND_URL=https://kwezi-backend.onrender.com
```

### Étape 3.2 : Rebuilder l'APK avec EAS

L'agent IA va exécuter :
```bash
cd /app/frontend
eas build --platform android --profile preview
```

⏰ **Durée du build** : ~15-20 minutes

### Étape 3.3 : Télécharger le nouvel APK

Une fois le build terminé, vous recevrez un lien comme :
```
https://expo.dev/accounts/ambdi97/projects/kwezi/builds/xxxxxxxx
```

Téléchargez et installez ce nouvel APK sur votre téléphone !

✅ **Phase 3 Terminée** : L'APK est maintenant configuré pour utiliser votre backend cloud !

---

## PHASE 4 : Tests Complets (20-30 min)

### Tests Backend

1. **Vérifier l'API words** :
   ```
   https://kwezi-backend.onrender.com/api/words
   ```
   → Devrait retourner 635 mots

2. **Vérifier l'API sentences** :
   ```
   https://kwezi-backend.onrender.com/api/sentences
   ```
   → Devrait retourner 270 phrases

3. **Vérifier les catégories** :
   ```
   https://kwezi-backend.onrender.com/api/categories
   ```

### Tests APK sur Android

1. ✅ L'application se lance
2. ✅ Les **635 mots s'affichent** dans les sections d'apprentissage
3. ✅ L'**audio fonctionne** (Shimaoré/Kibouchi)
4. ✅ Les **jeux fonctionnent** (Quiz Mayotte, Construire des phrases, etc.)
5. ✅ La **navigation** entre écrans fonctionne
6. ✅ Le **système premium** fonctionne (si activé)

---

## 🎉 DÉPLOIEMENT TERMINÉ !

Votre application Kwezi est maintenant :
- ✅ **Accessible partout dans le monde**
- ✅ **Connectée à une base de données cloud sécurisée**
- ✅ **Prête pour le Google Play Store**

---

## 🆘 Support

Si vous rencontrez des problèmes à n'importe quelle étape :

1. **Vérifiez les logs Render** : Dashboard → Logs
2. **Vérifiez MongoDB Atlas** : Les données sont bien importées ?
3. **Testez l'URL backend** dans un navigateur
4. **Contactez-moi** pour assistance

---

## 📚 Ressources

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Render Documentation](https://render.com/docs)
- [Expo EAS Build](https://docs.expo.dev/build/introduction/)

---

**Bon déploiement ! 🚀**
