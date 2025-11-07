# 🎯 GUIDE IMPORT MONGODB ATLAS - KWEZI

**Date**: 7 Novembre 2025  
**Backup créé** : ✅ `/app/kwezi_backup/` (6 collections, 737 documents)  
**Archive** : ✅ `/app/kwezi_mongodb_backup.tar.gz` (47 KB)

---

## 📦 DONNÉES EXPORTÉES

| Collection | Documents | Taille |
|------------|-----------|--------|
| **words** | 635 | 342 KB |
| **sentences** | 72 | 29 KB |
| **users** | 12 | 3.4 KB |
| **exercises** | 10 | 2.1 KB |
| **user_progress** | 7 | 799 B |
| **user_badges** | 1 | 207 B |
| **TOTAL** | **737** | **~420 KB** |

---

## 🚀 ÉTAPE 2 : IMPORTER DANS ATLAS

### Option A : Via MongoDB Compass (RECOMMANDÉ - Interface Graphique)

#### 1. Télécharger MongoDB Compass
- **Windows/Mac/Linux** : https://www.mongodb.com/try/download/compass
- Installez et ouvrez Compass

#### 2. Se Connecter à votre Cluster Atlas

**Dans MongoDB Atlas Dashboard** :
1. Cliquez sur **"Connect"** à côté de votre cluster "Ambdi"
2. Sélectionnez **"Connect using MongoDB Compass"**
3. Copiez la connection string qui ressemble à :
   ```
   mongodb+srv://username:password@ambdi.xxxxx.mongodb.net/
   ```

**Dans MongoDB Compass** :
1. Collez la connection string
2. Remplacez `<password>` par votre mot de passe Atlas
3. Cliquez **"Connect"**

#### 3. Créer la Base de Données

1. Dans Compass, cliquez **"Create Database"**
2. **Database Name** : `mayotte_app`
3. **Collection Name** : `words` (on créera les autres après)
4. Cliquez **"Create Database"**

#### 4. Importer Chaque Collection

**Pour chaque collection** (words, sentences, users, exercises, user_progress, user_badges) :

1. Sélectionnez la base `mayotte_app`
2. Si la collection n'existe pas, créez-la (ex: "sentences")
3. Cliquez sur la collection
4. Cliquez **"Add Data"** → **"Import JSON or CSV"**
5. **Type** : Sélectionnez **"BSON"**
6. Naviguez vers `/app/kwezi_backup/mayotte_app/[nom_collection].bson`
7. Cliquez **"Import"**

**Répétez pour les 6 collections**.

---

### Option B : Via Ligne de Commande (Plus Rapide)

#### 1. Récupérer votre Connection String

**Dans MongoDB Atlas** :
1. Cliquez **"Connect"** → **"Connect your application"**
2. Copiez la connection string
3. Format : `mongodb+srv://username:password@ambdi.xxxxx.mongodb.net/`

#### 2. Importer avec mongorestore

**Sur votre machine locale** (après avoir téléchargé le backup) :

```bash
# Remplacez les valeurs entre <>
mongorestore \
  --uri="mongodb+srv://<username>:<password>@ambdi.xxxxx.mongodb.net/mayotte_app" \
  /chemin/vers/kwezi_backup/mayotte_app
```

**Exemple concret** :
```bash
mongorestore \
  --uri="mongodb+srv://kwezi_user:VotreMotDePasse@ambdi.abc123.mongodb.net/mayotte_app" \
  ./kwezi_backup/mayotte_app
```

**Résultat attendu** :
```
2025-11-07T... finished restoring mayotte_app.words (635 documents, 0 failures)
2025-11-07T... finished restoring mayotte_app.sentences (72 documents, 0 failures)
2025-11-07T... finished restoring mayotte_app.users (12 documents, 0 failures)
...
737 document(s) restored successfully. 0 document(s) failed to restore.
```

---

## ⚙️ ÉTAPE 3 : CONFIGURATION ATLAS (CRITIQUE)

### 3A. Autoriser l'Accès Réseau

**MongoDB Atlas Dashboard** → **Security** → **Network Access** :

1. Cliquez **"Add IP Address"**
2. Sélectionnez **"Allow Access from Anywhere"**
   - IP: `0.0.0.0/0`
   - Description: "Render & Production Access"
3. Cliquez **"Confirm"**

⚠️ **Important** : Cela permet à Render.com de se connecter à votre base.

### 3B. Vérifier l'Utilisateur Base de Données

**Security** → **Database Access** :

1. Vérifiez qu'un utilisateur existe
2. **Permissions** : "Read and write to any database" (ou "Atlas Admin")
3. Si pas d'utilisateur, créez-en un :
   - Username: `kwezi_user`
   - Password: Générez un mot de passe fort (sauvegardez-le !)
   - Database User Privileges: **"Read and write to any database"**

---

## 📋 ÉTAPE 4 : RÉCUPÉRER LA CONNECTION STRING

**Dans MongoDB Atlas** :
1. Cliquez **"Connect"** sur votre cluster
2. **"Connect your application"**
3. **Driver** : Python
4. **Version** : 3.12 or later (peu importe)
5. **Copiez** la connection string :

```
mongodb+srv://<username>:<password>@ambdi.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 📝 Modifiez la Connection String :

**Format pour Render** :
```
mongodb+srv://<username>:<password>@ambdi.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority
```

**Changements** :
1. Remplacez `<username>` par votre username Atlas
2. Remplacez `<password>` par votre mot de passe Atlas
3. Ajoutez `/mayotte_app` après `.net`

**Exemple final** :
```
mongodb+srv://kwezi_user:MonMotDePasse123@ambdi.abc123.mongodb.net/mayotte_app?retryWrites=true&w=majority
```

---

## ✅ ÉTAPE 5 : TESTER LA CONNECTION

**Sur votre machine** ou **dans Emergent**, testez :

```python
import pymongo

# Remplacez par votre connection string
uri = "mongodb+srv://username:password@ambdi.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(uri)
    db = client["mayotte_app"]
    
    # Tester
    word_count = db.words.count_documents({})
    print(f"✅ Connexion réussie !")
    print(f"✅ Mots trouvés : {word_count}")
    
    if word_count == 635:
        print("🎉 Toutes les données sont importées !")
    else:
        print(f"⚠️ Attendu 635 mots, trouvé {word_count}")
        
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
```

---

## 🚀 ÉTAPE 6 : DÉPLOYER SUR RENDER

Une fois Atlas configuré et testé :

### 6A. Push Code sur GitHub

**Si pas encore fait** :

```bash
cd /app/backend
git init
git add .
git commit -m "Kwezi backend - ready for production"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/kwezi-backend.git
git push -u origin main
```

### 6B. Créer Web Service sur Render

1. **Dashboard Render** : https://dashboard.render.com
2. **New** → **Web Service**
3. **Connect Repository** : Sélectionnez `kwezi-backend`
4. **Configuration** :
   - Name: `kwezi-backend`
   - Region: Europe (Frankfurt)
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### 6C. Variables d'Environnement

**Advanced** → **Environment Variables** :

| Key | Value |
|-----|-------|
| `MONGO_URL` | `mongodb+srv://username:password@ambdi.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority` |
| `PYTHON_VERSION` | `3.11.0` |
| `DB_NAME` | `mayotte_app` |

### 6D. Deploy !

1. Cliquez **"Create Web Service"**
2. Attendez 2-3 minutes (installation des dépendances)
3. Statut devrait passer à **"Live"** (vert)

---

## 🧪 ÉTAPE 7 : TESTER LE BACKEND DÉPLOYÉ

Votre backend sera accessible sur :
```
https://kwezi-backend-xxxx.onrender.com
```

**Testez ces endpoints** :

```bash
# 1. Health check
curl https://kwezi-backend-xxxx.onrender.com/

# 2. Words API
curl https://kwezi-backend-xxxx.onrender.com/api/words?limit=5

# 3. Sentences API
curl https://kwezi-backend-xxxx.onrender.com/api/sentences?limit=5
```

**Réponses attendues** :
- Health : `{"message":"Mayotte Language Learning API","status":"running"}`
- Words : JSON array avec 5 mots
- Sentences : JSON array avec 5 phrases

---

## 📝 CHECKLIST FINALE

Avant de continuer vers le frontend :

- [ ] MongoDB Atlas : Données importées (635 mots, 72 phrases)
- [ ] MongoDB Atlas : Network Access configuré (0.0.0.0/0)
- [ ] MongoDB Atlas : Utilisateur DB créé avec permissions
- [ ] Connection string récupérée et testée
- [ ] Code backend poussé sur GitHub
- [ ] Render Web Service créé
- [ ] Variables d'environnement configurées
- [ ] Backend déployé et "Live"
- [ ] Endpoints testés et fonctionnels

---

## 🎯 PROCHAINE ÉTAPE

Une fois le backend sur Render testé et fonctionnel :

**Mettre à jour le frontend** :
```bash
# Dans /app/kwezi-app/.env
EXPO_PUBLIC_BACKEND_URL=https://kwezi-backend-xxxx.onrender.com
```

**Rebuild le frontend** :
```bash
cd /app/kwezi-app
npx expo export --platform web
```

**Déployer sur Vercel** :
```bash
vercel --prod
```

---

*Guide créé le 7 Novembre 2025*  
*Backup MongoDB ready for Atlas import*
