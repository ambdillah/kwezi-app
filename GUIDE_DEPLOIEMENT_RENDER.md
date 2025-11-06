# 🚀 GUIDE DE DÉPLOIEMENT BACKEND RENDER - KWEZI

**Date**: 6 Novembre 2025  
**Backend**: FastAPI + MongoDB  
**Fichiers prêts**: ✅ Tous les fichiers sont configurés

---

## ✅ FICHIERS DÉJÀ PRÉPARÉS

Tous les fichiers nécessaires sont dans `/app/backend/` :
- ✅ `server.py` - Backend FastAPI complet
- ✅ `requirements.txt` - Dépendances Python
- ✅ `render.yaml` - Configuration Render automatique
- ✅ `.env` - Variables d'environnement (ne sera PAS poussé sur Git)

---

## 📋 ÉTAPE PAR ÉTAPE

### ÉTAPE 1 : Créer un repo GitHub pour le backend

**Option A : Via GitHub Web (Plus simple)**

1. Allez sur https://github.com
2. Cliquez sur le bouton "+" en haut à droite → "New repository"
3. Nommez-le : `kwezi-backend`
4. Laissez en **Public** ou **Private** (votre choix)
5. **NE cochez PAS** "Initialize with README"
6. Cliquez "Create repository"

**Option B : Via Git CLI (si vous préférez le terminal)**

```bash
# Sur votre machine locale, créez un nouveau repo sur GitHub puis :
cd /app/backend
git init
git add .
git commit -m "Initial commit - Kwezi backend"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/kwezi-backend.git
git push -u origin main
```

---

### ÉTAPE 2 : Connecter GitHub à Render

1. Allez sur https://dashboard.render.com
2. Connectez-vous avec votre compte Render
3. Cliquez sur **"New +"** en haut à droite
4. Sélectionnez **"Web Service"**

---

### ÉTAPE 3 : Configurer le Web Service

#### A. Connexion au Repo

1. **Connect a repository**
   - Si première fois : Cliquez "Connect account" → Autorisez GitHub
   - Sélectionnez le repo `kwezi-backend`
   - Cliquez "Connect"

#### B. Configuration du Service

Remplissez les champs suivants :

| Champ | Valeur |
|-------|--------|
| **Name** | `kwezi-backend` |
| **Region** | Europe (Frankfurt) ou le plus proche |
| **Branch** | `main` |
| **Root Directory** | (laisser vide) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn server:app --host 0.0.0.0 --port $PORT` |

#### C. Plan (Important)

- Sélectionnez **"Free"** (0$/mois)
- ⚠️ Note : Le plan gratuit s'endort après 15 min d'inactivité, mais se réveille automatiquement

---

### ÉTAPE 4 : Variables d'Environnement (CRITIQUE)

Cliquez sur **"Advanced"** puis ajoutez ces variables :

#### Variables Obligatoires :

1. **MONGO_URL**
   ```
   Nom: MONGO_URL
   Valeur: Votre URL MongoDB Atlas
   Exemple: mongodb+srv://username:password@cluster.mongodb.net/mayotte_app
   ```

2. **PYTHON_VERSION**
   ```
   Nom: PYTHON_VERSION
   Valeur: 3.11.0
   ```

3. **DB_NAME**
   ```
   Nom: DB_NAME
   Valeur: mayotte_app
   ```

#### Variables Optionnelles (pour Stripe - si activé) :

4. **STRIPE_SECRET_KEY**
   ```
   Nom: STRIPE_SECRET_KEY
   Valeur: sk_test_... (votre clé Stripe secrète)
   ```

5. **STRIPE_WEBHOOK_SECRET**
   ```
   Nom: STRIPE_WEBHOOK_SECRET
   Valeur: whsec_... (votre secret webhook Stripe)
   ```

---

### ÉTAPE 5 : Déployer !

1. **Scrollez en bas** et cliquez sur **"Create Web Service"**
2. Render va :
   - Cloner votre repo
   - Installer les dépendances (2-3 minutes)
   - Démarrer le serveur
3. **Attendez** que le statut passe à "Live" (vert)

---

### ÉTAPE 6 : Tester l'URL Déployée

Une fois déployé, vous aurez une URL comme :
```
https://kwezi-backend.onrender.com
```

**Testez ces endpoints** :

1. **Page d'accueil** :
   ```
   https://kwezi-backend.onrender.com/
   ```
   Devrait retourner : `{"message":"Mayotte Language Learning API","status":"running"}`

2. **API Words** :
   ```
   https://kwezi-backend.onrender.com/api/words?limit=5
   ```
   Devrait retourner 5 mots en JSON

3. **API Sentences** :
   ```
   https://kwezi-backend.onrender.com/api/sentences?limit=5
   ```
   Devrait retourner 5 phrases

---

## 🔧 ÉTAPE 7 : Mettre à Jour le Frontend

Une fois le backend déployé, mettez à jour le frontend :

### A. Fichier `.env` dans kwezi-app

```bash
# Dans /app/kwezi-app/.env
EXPO_PUBLIC_BACKEND_URL=https://kwezi-backend.onrender.com
```

### B. Rebuild le Frontend

```bash
cd /app/kwezi-app
npx expo export --platform web
```

### C. Redéployer sur Vercel

Si déjà déployé sur Vercel :
- Allez dans le dashboard Vercel
- Settings → Environment Variables
- Modifiez `EXPO_PUBLIC_BACKEND_URL` avec la nouvelle URL
- Redéployez (Deploy → Redeploy)

---

## ⚠️ PROBLÈMES COURANTS & SOLUTIONS

### 1. "Application failed to respond"

**Cause** : Port non configuré correctement

**Solution** : Vérifiez que la commande de démarrage utilise `$PORT` :
```bash
uvicorn server:app --host 0.0.0.0 --port $PORT
```

### 2. "Cannot connect to MongoDB"

**Cause** : MONGO_URL incorrecte ou MongoDB Atlas n'autorise pas l'IP de Render

**Solution** :
1. Allez sur MongoDB Atlas
2. Network Access → Add IP Address
3. Ajoutez `0.0.0.0/0` (autorise toutes les IPs) ou l'IP de Render

### 3. "Module not found"

**Cause** : Dépendance manquante dans requirements.txt

**Solution** : Ajoutez la dépendance dans requirements.txt et redéployez

### 4. "Service goes to sleep"

**Cause** : Plan gratuit Render

**Solution** : 
- Acceptez le délai de réveil (15-30 secondes)
- OU passez au plan payant (7$/mois)
- OU utilisez un service de "keep alive" (ping toutes les 10 min)

---

## 📊 MONGODB ATLAS (SI VOUS N'AVEZ PAS ENCORE)

Si vous n'avez pas encore de base MongoDB Atlas :

### Configuration Rapide MongoDB Atlas

1. **Créer un compte** : https://www.mongodb.com/cloud/atlas/register
2. **Créer un cluster gratuit** (M0 - Free tier)
3. **Créer un utilisateur** :
   - Database Access → Add New Database User
   - Username: `kwezi_admin`
   - Password: Générez un mot de passe fort
4. **Autoriser l'accès** :
   - Network Access → Add IP Address
   - Entrez `0.0.0.0/0` (ou l'IP de Render)
5. **Récupérer la connection string** :
   - Cliquez "Connect" → "Connect your application"
   - Copiez l'URL : `mongodb+srv://kwezi_admin:PASSWORD@cluster.mongodb.net/`
6. **Importer vos données** :
   - Si vous avez un backup dans `/app/backend/db_backup/`
   - Utilisez `mongorestore` ou MongoDB Compass

---

## ✅ CHECKLIST FINALE

Avant de dire que le backend est déployé, vérifiez :

- [ ] Render Web Service montre "Live" (vert)
- [ ] `https://kwezi-backend.onrender.com/` retourne un JSON
- [ ] `/api/words` retourne 635 mots
- [ ] `/api/sentences` retourne 72 phrases
- [ ] MongoDB est connecté (pas d'erreur dans les logs)
- [ ] Les logs Render ne montrent pas d'erreur critique

---

## 🎯 PROCHAINES ÉTAPES

Une fois le backend déployé sur Render :

1. ✅ Testez tous les endpoints
2. ✅ Mettez à jour l'URL dans le frontend
3. ✅ Redéployez le frontend sur Vercel
4. ✅ Testez l'application web complète
5. 🎉 Lancez l'application !

---

## 📞 AIDE SUPPLÉMENTAIRE

**Logs Render** : 
- Dans le dashboard Render, onglet "Logs"
- Voir les erreurs en temps réel

**MongoDB Atlas Logs** :
- Dans Atlas, onglet "Monitoring"
- Voir les connexions et requêtes

---

*Guide créé le 6 Novembre 2025*  
*Backend Kwezi prêt pour production*
