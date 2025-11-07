# 🌐 IMPORT MONGODB ATLAS - VIA INTERFACE WEB (Sans Installation)

**Date** : 7 Novembre 2025  
**Fichiers JSON prêts** : ✅ 6 collections converties

---

## 📦 FICHIERS JSON DISPONIBLES

| Fichier | Taille | Documents | Prêt |
|---------|--------|-----------|------|
| `words.json` | 435 KB | 635 | ✅ |
| `sentences.json` | 30 KB | 72 | ✅ |
| `users.json` | 4.9 KB | 12 | ✅ |
| `exercises.json` | 2.2 KB | 10 | ✅ |
| `user_progress.json` | 1.1 KB | 7 | ✅ |
| `user_badges.json` | 251 B | 1 | ✅ |

**Localisation** : `/app/kwezi_backup/mayotte_app/*.json`

---

## 🎯 ÉTAPE PAR ÉTAPE : Import via Atlas Web UI

### ÉTAPE 1 : Télécharger les Fichiers JSON

**Depuis Emergent** :
1. Ouvrez l'explorateur de fichiers Emergent
2. Naviguez vers `/app/kwezi_backup/mayotte_app/`
3. Téléchargez ces 6 fichiers sur votre ordinateur de travail :
   - `words.json`
   - `sentences.json`
   - `users.json`
   - `exercises.json`
   - `user_progress.json`
   - `user_badges.json`

---

### ÉTAPE 2 : Se Connecter à MongoDB Atlas

1. **Allez sur** : https://cloud.mongodb.com
2. **Connectez-vous** avec votre compte
3. Sélectionnez votre organisation/projet
4. Vous devriez voir votre cluster **"Ambdi"**

---

### ÉTAPE 3 : Créer la Base de Données

1. **Cliquez sur "Browse Collections"** sur votre cluster Ambdi
2. **Cliquez "Add My Own Data"** (ou "+ Create Database")
3. **Remplissez** :
   - Database Name : `mayotte_app`
   - Collection Name : `words`
4. **Cliquez "Create"**

---

### ÉTAPE 4 : Importer Chaque Collection

#### 4.1 Collection "words" (635 documents)

1. Dans `mayotte_app`, cliquez sur la collection **"words"**
2. Cliquez **"Insert Document"** → **"Import JSON or CSV file"**
3. **Sélectionnez** le fichier `words.json`
4. Cliquez **"Import"**
5. ✅ Vous devriez voir : "Successfully imported 635 documents"

#### 4.2 Collection "sentences" (72 documents)

1. **Créez une nouvelle collection** :
   - Dans la base `mayotte_app`, cliquez "Create Collection"
   - Nom : `sentences`
   - Cliquez "Create"
2. **Importez** le fichier `sentences.json` (même méthode)
3. ✅ 72 documents importés

#### 4.3 Collection "users" (12 documents)

1. **Créez** la collection `users`
2. **Importez** `users.json`
3. ✅ 12 documents importés

#### 4.4 Collection "exercises" (10 documents)

1. **Créez** la collection `exercises`
2. **Importez** `exercises.json`
3. ✅ 10 documents importés

#### 4.5 Collection "user_progress" (7 documents)

1. **Créez** la collection `user_progress`
2. **Importez** `user_progress.json`
3. ✅ 7 documents importés

#### 4.6 Collection "user_badges" (1 document)

1. **Créez** la collection `user_badges`
2. **Importez** `user_badges.json`
3. ✅ 1 document importé

---

### ÉTAPE 5 : Vérifier l'Import

**Dans MongoDB Atlas**, dans la base `mayotte_app`, vous devriez voir :

```
Collections:
  ✅ words (635 documents)
  ✅ sentences (72 documents)
  ✅ users (12 documents)
  ✅ exercises (10 documents)
  ✅ user_progress (7 documents)
  ✅ user_badges (1 document)

TOTAL: 737 documents
```

---

## ⚙️ CONFIGURATION ATLAS (IMPORTANT)

### Étape 6 : Network Access

**Dans MongoDB Atlas** :
1. Menu gauche → **Security** → **Network Access**
2. Cliquez **"Add IP Address"**
3. Sélectionnez **"Allow Access from Anywhere"**
   - Cliquez le bouton pour `0.0.0.0/0`
   - Description : "Production Access"
4. Cliquez **"Confirm"**

⚠️ **Pourquoi ?** Render.com doit pouvoir se connecter à votre base.

---

### Étape 7 : Database User

**Dans MongoDB Atlas** :
1. Menu gauche → **Security** → **Database Access**
2. **Vérifiez** qu'un utilisateur existe
3. Si aucun utilisateur :
   - Cliquez **"Add New Database User"**
   - **Authentication Method** : Password
   - **Username** : `kwezi_user`
   - **Password** : Générez un mot de passe fort (SAUVEGARDEZ-LE !)
   - **Database User Privileges** : "Read and write to any database"
   - Cliquez **"Add User"**

---

### Étape 8 : Connection String

**Dans MongoDB Atlas** :
1. Retournez sur **Database** (menu gauche)
2. Sur votre cluster Ambdi, cliquez **"Connect"**
3. Sélectionnez **"Connect your application"**
4. **Driver** : Python
5. **Copiez** la connection string :

```
mongodb+srv://<username>:<password>@ambdi.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**Modifiez-la** :
```
mongodb+srv://kwezi_user:VotreMotDePasse@ambdi.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority
```

**Changements** :
- Remplacez `<username>` par votre username
- Remplacez `<password>` par votre mot de passe
- Ajoutez `/mayotte_app` après `.net`

---

## ✅ ÉTAPE 9 : Tester la Connection

**Option A : Via Atlas Data Explorer**

1. Dans Atlas, cliquez **"Browse Collections"**
2. Sélectionnez `mayotte_app` → `words`
3. Vous devriez voir les 635 mots
4. ✅ Si vous voyez les données, l'import est réussi !

**Option B : Test avec Python (si vous voulez)**

Partagez-moi votre connection string et je teste pour vous !

---

## 🚀 PROCHAINE ÉTAPE : Déployer sur Render

Une fois l'import terminé et vérifié :

### Push Backend sur GitHub

**Option Simple** (via GitHub Web) :
1. Allez sur https://github.com/new
2. Créez un repo : `kwezi-backend`
3. Téléchargez le dossier `/app/backend/` depuis Emergent
4. Uploadez les fichiers via l'interface web GitHub

**Option Git** (si Git est installé sur votre ordi) :
```bash
cd /chemin/vers/backend
git init
git add .
git commit -m "Kwezi backend"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/kwezi-backend.git
git push -u origin main
```

### Créer Web Service Render

1. **Render Dashboard** : https://dashboard.render.com
2. **New** → **Web Service**
3. **Connectez** votre repo GitHub `kwezi-backend`
4. **Configuration** :
   - Build : `pip install -r requirements.txt`
   - Start : `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. **Variables d'environnement** :
   - `MONGO_URL` : Votre connection string Atlas
   - `PYTHON_VERSION` : `3.11.0`
   - `DB_NAME` : `mayotte_app`
6. **Deploy !**

---

## 📝 TIMELINE ESTIMÉE

| Tâche | Temps | ✅ |
|-------|-------|-----|
| Télécharger les 6 JSON | 2 min | |
| Créer base + importer collections | 10 min | |
| Configurer Network Access | 2 min | |
| Récupérer connection string | 2 min | |
| Push code sur GitHub | 5 min | |
| Déployer sur Render | 15 min | |
| **TOTAL** | **~35 min** | |

---

## 🎯 RÉSUMÉ : CE QUE VOUS FAITES MAINTENANT

1. ✅ Téléchargez les 6 fichiers JSON depuis `/app/kwezi_backup/mayotte_app/`
2. ✅ Allez sur MongoDB Atlas
3. ✅ Créez la base `mayotte_app`
4. ✅ Importez les 6 collections (via Import JSON)
5. ✅ Configurez Network Access (0.0.0.0/0)
6. ✅ Récupérez la connection string
7. ✅ Push backend sur GitHub
8. ✅ Déployez sur Render

**Tout peut se faire depuis votre ordinateur de travail, via le navigateur ! Aucune installation nécessaire.** 🎉

---

*Guide créé le 7 Novembre 2025*  
*Import MongoDB Atlas sans installation de logiciel*
