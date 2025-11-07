# 🏠 GUIDE COMPLET - À FAIRE CHEZ VOUS

**Date** : 7 Novembre 2025  
**Durée estimée** : 1h (première fois)  
**Prérequis** : Ordinateur avec navigateur web

---

## 📋 RÉCAPITULATIF : TOUT EST PRÊT !

### ✅ CE QUI EST DÉJÀ FAIT (Sur Emergent)

1. ✅ **Application Kwezi complète** développée et testée
2. ✅ **635 mots** avec traductions shimaoré/kibouchi
3. ✅ **100% audio** vérifié et corrigé
4. ✅ **72 phrases** pour le jeu (3 temps : présent, passé, futur)
5. ✅ **4 jeux interactifs** fonctionnels
6. ✅ **Système premium** avec Stripe
7. ✅ **Backend FastAPI** prêt à déployer
8. ✅ **Frontend web build** créé (dossier `dist/`)
9. ✅ **Base MongoDB** exportée en JSON (6 fichiers)
10. ✅ **Tous les guides** de déploiement rédigés

### 📦 FICHIERS À TÉLÉCHARGER DEPUIS EMERGENT

| Fichier/Dossier | Chemin Emergent | Taille | Usage |
|-----------------|-----------------|--------|-------|
| **Backend complet** | `/app/backend/` | ~5 MB | À pousser sur GitHub |
| **Frontend build** | `/app/kwezi-app/dist/` | ~2 MB | À déployer sur Vercel |
| **MongoDB JSON** (6 fichiers) | `/app/kwezi_backup/mayotte_app/*.json` | 473 KB | À importer dans Atlas |
| **Guides** | `/app/*.md` | ~200 KB | Documentation |

---

## 🎯 PLAN D'ACTION CHEZ VOUS (4 Étapes)

### ÉTAPE 1 : Télécharger les Fichiers depuis Emergent (15 min)

#### Comment télécharger depuis Emergent ?

**Option A : Via l'interface Emergent File Manager**

1. Dans l'interface Emergent, cherchez **"Files"**, **"Explorer"**, ou un **icône de dossier** 📁
2. Naviguez vers les dossiers suivants et téléchargez-les

**Option B : Via Terminal Emergent (Créer un ZIP)**

Si vous avez accès au terminal Emergent, copiez ces commandes :

```bash
# Créer un ZIP avec tout ce dont vous avez besoin
cd /app
zip -r kwezi_deploy_package.zip \
  backend/ \
  kwezi-app/dist/ \
  kwezi_backup/mayotte_app/*.json \
  *.md \
  -x "*/node_modules/*" "*/.*" "*/__pycache__/*"

# Le fichier sera dans /app/kwezi_deploy_package.zip
```

**Option C : Demander à l'équipe Emergent**

Contactez le support Emergent pour télécharger :
- `/app/backend/`
- `/app/kwezi-app/dist/`
- `/app/kwezi_backup/mayotte_app/*.json`

---

### ÉTAPE 2 : Importer dans MongoDB Atlas (30 min)

#### 2.1 Se Connecter à Atlas

1. Allez sur https://cloud.mongodb.com
2. Connectez-vous avec votre compte
3. Sélectionnez votre cluster **"Ambdi"**

#### 2.2 Créer la Base de Données

1. Cliquez **"Browse Collections"**
2. Cliquez **"+ Create Database"**
3. **Database Name** : `mayotte_app`
4. **Collection Name** : `words`
5. Cliquez **"Create"**

#### 2.3 Importer les 6 Collections

**Pour chaque fichier JSON** :

1. Dans la base `mayotte_app`, créez la collection si elle n'existe pas
2. Cliquez sur la collection
3. Cliquez **"Insert Document"** → **"Import JSON or CSV file"**
4. Sélectionnez le fichier JSON correspondant
5. Cliquez **"Import"**

**Ordre d'import** :
1. `words.json` → Collection `words` (635 documents)
2. `sentences.json` → Collection `sentences` (72 documents)
3. `users.json` → Collection `users` (12 documents)
4. `exercises.json` → Collection `exercises` (10 documents)
5. `user_progress.json` → Collection `user_progress` (7 documents)
6. `user_badges.json` → Collection `user_badges` (1 document)

#### 2.4 Configurer l'Accès Réseau

**Security → Network Access** :
1. Cliquez **"Add IP Address"**
2. Sélectionnez **"Allow Access from Anywhere"** (`0.0.0.0/0`)
3. Cliquez **"Confirm"**

#### 2.5 Récupérer la Connection String

1. Cliquez **"Connect"** sur votre cluster
2. **"Connect your application"**
3. Copiez la connection string :
   ```
   mongodb+srv://<username>:<password>@ambdi.xxxxx.mongodb.net/
   ```
4. **Modifiez-la** :
   - Remplacez `<username>` par votre username
   - Remplacez `<password>` par votre mot de passe
   - Ajoutez `/mayotte_app` après `.net`

**Format final** :
```
mongodb+srv://votre_user:votre_pass@ambdi.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority
```

⚠️ **SAUVEGARDEZ cette connection string** (vous en aurez besoin pour Render)

---

### ÉTAPE 3 : Déployer le Backend sur Render (20 min)

#### 3.1 Créer un Repo GitHub

**Option Simple (Via Web)** :
1. Allez sur https://github.com/new
2. Nom du repo : `kwezi-backend`
3. Laissez en Public ou Private
4. **NE cochez PAS** "Initialize with README"
5. Cliquez **"Create repository"**

**Upload les fichiers** :
1. Dans le repo vide, cliquez **"uploading an existing file"**
2. Glissez tous les fichiers du dossier `backend/` que vous avez téléchargé
3. Commit : "Initial commit - Kwezi backend"
4. Cliquez **"Commit changes"**

**Option Git (Si Git installé)** :
```bash
cd /chemin/vers/backend
git init
git add .
git commit -m "Kwezi backend ready for production"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/kwezi-backend.git
git push -u origin main
```

#### 3.2 Déployer sur Render

1. Allez sur https://dashboard.render.com
2. Cliquez **"New +"** → **"Web Service"**
3. **Connectez votre repo GitHub** `kwezi-backend`
4. **Configuration** :

| Champ | Valeur |
|-------|--------|
| Name | `kwezi-backend` |
| Region | Europe (Frankfurt) |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn server:app --host 0.0.0.0 --port $PORT` |
| Instance Type | **Free** |

5. **Variables d'Environnement** (CRITIQUE - Cliquez "Advanced") :

| Key | Value |
|-----|-------|
| `MONGO_URL` | Votre connection string Atlas (celle sauvegardée à l'étape 2.5) |
| `PYTHON_VERSION` | `3.11.0` |
| `DB_NAME` | `mayotte_app` |

6. Cliquez **"Create Web Service"**

7. **Attendez 2-3 minutes** (installation des dépendances)

8. Statut devrait passer à **"Live"** (vert)

#### 3.3 Tester le Backend

Votre backend sera sur : `https://kwezi-backend-xxxx.onrender.com`

**Testez ces URLs dans votre navigateur** :

1. **Health check** : `https://kwezi-backend-xxxx.onrender.com/`
   - Devrait afficher : `{"message":"Mayotte Language Learning API","status":"running"}`

2. **API Words** : `https://kwezi-backend-xxxx.onrender.com/api/words?limit=5`
   - Devrait afficher 5 mots en JSON

3. **API Sentences** : `https://kwezi-backend-xxxx.onrender.com/api/sentences?limit=5`
   - Devrait afficher 5 phrases en JSON

✅ Si tout fonctionne, passez à l'étape suivante !

⚠️ **SAUVEGARDEZ l'URL de votre backend** (ex: `https://kwezi-backend-xxxx.onrender.com`)

---

### ÉTAPE 4 : Déployer le Frontend sur Vercel (15 min)

#### 4.1 Mettre à Jour l'URL Backend

**Dans le dossier `dist/` que vous avez téléchargé** :

1. Ouvrez le fichier `dist/_expo/static/js/web/entry-[hash].js` avec un éditeur de texte
2. Cherchez : `EXPO_PUBLIC_BACKEND_URL`
3. Remplacez l'ancienne URL par votre nouvelle URL Render
4. Sauvegardez

**OU** (Plus simple) : Configurez la variable d'environnement directement dans Vercel (voir 4.3)

#### 4.2 Créer un Compte Vercel

1. Allez sur https://vercel.com
2. Cliquez **"Sign Up"**
3. Connectez-vous avec GitHub (recommandé)

#### 4.3 Déployer via Drag & Drop

1. Une fois connecté, cliquez **"Add New"** → **"Project"**
2. **Glissez le dossier `dist/`** dans la zone de dépôt
3. **Project Name** : `kwezi`
4. **Framework Preset** : Other (ou Vite)
5. **Environment Variables** :
   - Cliquez "Add Environment Variable"
   - Key : `EXPO_PUBLIC_BACKEND_URL`
   - Value : `https://kwezi-backend-xxxx.onrender.com` (votre URL Render)
6. Cliquez **"Deploy"**

7. **Attendez 1-2 minutes** (déploiement)

8. Votre app sera sur : `https://kwezi-xxxx.vercel.app`

#### 4.4 Tester l'Application Web

**Ouvrez** : `https://kwezi-xxxx.vercel.app`

**Testez** :
- ✅ Page d'accueil s'affiche
- ✅ Onglet "Apprendre" charge les mots
- ✅ Audio fonctionne (cliquez sur 🔊)
- ✅ Jeux sont accessibles
- ✅ Boutique affiche les fiches
- ✅ Premium affiche la page d'abonnement

---

## 🎉 FÉLICITATIONS !

Si tout fonctionne :
- ✅ Backend déployé sur Render
- ✅ Frontend déployé sur Vercel
- ✅ Application accessible publiquement
- ✅ MongoDB Atlas connecté

**Votre application Kwezi est LIVE !** 🚀

---

## 📊 CHECKLIST FINALE

Avant de dire que c'est terminé :

- [ ] MongoDB Atlas : 6 collections importées (737 documents)
- [ ] MongoDB Atlas : Network Access configuré (0.0.0.0/0)
- [ ] Backend Render : Déployé et "Live"
- [ ] Backend Render : URL testée et fonctionnelle
- [ ] Frontend Vercel : Déployé et accessible
- [ ] Frontend Vercel : Connecté au bon backend
- [ ] Application web : Tous les écrans fonctionnels
- [ ] Audio : Se jouent correctement
- [ ] Jeux : Fonctionnent (tester au moins 1)

---

## 🔧 TROUBLESHOOTING

### "Cannot connect to MongoDB" sur Render

**Solution** :
1. Vérifiez que Network Access est configuré (0.0.0.0/0)
2. Vérifiez que la connection string est correcte (username, password)
3. Dans MongoDB Atlas, vérifiez que le user a les bonnes permissions

### "Application failed to respond" sur Render

**Solution** :
1. Vérifiez les logs Render (onglet "Logs")
2. Vérifiez que la commande de démarrage utilise `$PORT`
3. Attendez 1-2 minutes (première requête peut être lente)

### "Mots ne s'affichent pas" sur Vercel

**Solution** :
1. Vérifiez que `EXPO_PUBLIC_BACKEND_URL` est correctement configurée
2. Ouvrez la console navigateur (F12) et vérifiez les erreurs
3. Testez que le backend répond : `https://votre-backend.onrender.com/api/words`

### "Backend s'endort après 15 min" (Plan gratuit Render)

**Comportement normal** avec le plan gratuit Render.

**Solutions** :
- Acceptez le délai de réveil (15-30 secondes)
- Passez au plan payant Render (7$/mois)
- Utilisez un service de "keep alive" (ping toutes les 10 min)

---

## 📱 PROCHAINE ÉTAPE : APK ANDROID (Optionnel)

Une fois l'application web testée et validée, vous pourrez :
1. Build l'APK Android via EAS Build
2. Publier sur Google Play Store

**Mais validez d'abord le web !**

---

## 📞 BESOIN D'AIDE ?

**Guides disponibles sur Emergent** :
- `/app/IMPORT_ATLAS_WEB.md` - Import MongoDB Atlas détaillé
- `/app/GUIDE_DEPLOIEMENT_RENDER.md` - Render avec troubleshooting
- `/app/CHECKLIST_DEPLOIEMENT_WEB.md` - Checklist complète

**Si vous êtes bloqué** :
- Revenez vers moi avec le message d'erreur exact
- Envoyez des captures d'écran si possible

---

## ⏱️ TIMELINE COMPLÈTE

| Étape | Temps | Statut |
|-------|-------|--------|
| Télécharger fichiers depuis Emergent | 15 min | ⏳ |
| Importer dans MongoDB Atlas | 30 min | ⏳ |
| Déployer backend sur Render | 20 min | ⏳ |
| Déployer frontend sur Vercel | 15 min | ⏳ |
| **TOTAL** | **~1h20** | |

---

**Bon courage ! Vous êtes à quelques heures d'avoir votre application en ligne !** 🚀

*Guide créé le 7 Novembre 2025*  
*Tout est prêt pour le déploiement*
