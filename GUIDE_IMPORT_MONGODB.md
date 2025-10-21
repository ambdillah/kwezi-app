# 🚀 Guide Rapide - Import MongoDB Atlas

## Étape 1 : Préparation des données

Téléchargez le fichier `/app/backend/db_export.json` depuis votre environnement Emergent.

Ce fichier contient :
- **635 mots** en Shimaoré et Kibouchi
- **270 phrases** pour le jeu "Construire des phrases"
- **10 exercices** pédagogiques

## Étape 2 : Import via MongoDB Compass (Recommandé)

### 2.1 Télécharger MongoDB Compass

1. Allez sur https://www.mongodb.com/try/download/compass
2. Téléchargez et installez MongoDB Compass (client gratuit)

### 2.2 Connexion à MongoDB Atlas

1. Ouvrez MongoDB Compass
2. Collez votre URL de connexion MongoDB Atlas :
   ```
   mongodb+srv://kwezi_user:VOTRE_MOT_DE_PASSE@kwezi-cluster.xxxxx.mongodb.net/
   ```
3. Cliquez sur "Connect"

### 2.3 Import des données

1. Créez la base de données `mayotte_app` (si pas déjà fait)
2. Pour chaque collection (`words`, `sentences`, `exercises`) :
   - Sélectionnez la collection
   - Cliquez sur "ADD DATA" → "Import JSON or CSV file"
   - Sélectionnez le fichier `db_export.json`
   - Choisissez la section correspondante (ex: pour `words`, sélectionnez le tableau `words`)
   - Cliquez sur "Import"

## Étape 3 : Import via mongoimport (Alternative CLI)

Si vous préférez la ligne de commande :

```bash
# Pour la collection words
mongoimport --uri "mongodb+srv://kwezi_user:VOTRE_MOT_DE_PASSE@kwezi-cluster.xxxxx.mongodb.net/mayotte_app" \
  --collection words \
  --file db_export.json \
  --jsonArray \
  --mode insert

# Pour la collection sentences
mongoimport --uri "mongodb+srv://kwezi_user:VOTRE_MOT_DE_PASSE@kwezi-cluster.xxxxx.mongodb.net/mayotte_app" \
  --collection sentences \
  --file db_export.json \
  --jsonArray \
  --mode insert

# Pour la collection exercises
mongoimport --uri "mongodb+srv://kwezi_user:VOTRE_MOT_DE_PASSE@kwezi-cluster.xxxxx.mongodb.net/mayotte_app" \
  --collection exercises \
  --file db_export.json \
  --jsonArray \
  --mode insert
```

## Étape 4 : Vérification

Dans MongoDB Atlas ou Compass :

1. Allez dans la collection `words`
2. Vous devriez voir **635 documents**
3. Vérifiez qu'un mot contient bien les champs : `french`, `shimaore`, `kibouchi`, `category`

✅ **Import terminé !** Vous pouvez maintenant utiliser cette URL dans Render.com.

---

## 🆘 Problèmes courants

**Erreur "Authentication failed"**
→ Vérifiez que le mot de passe dans l'URL est correct (sans `<>`)

**Erreur "Network timeout"**
→ Vérifiez que vous avez autorisé l'accès réseau (0.0.0.0/0) dans MongoDB Atlas

**Import lent ou qui échoue**
→ Importez collection par collection plutôt que tout en une fois
