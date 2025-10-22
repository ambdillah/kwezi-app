# 🚀 Guide Render.com - Déploiement Backend Kwezi

## Option A : Déploiement depuis GitHub (Recommandé)

### Étape 1 : Préparer le dépôt GitHub

Si vous n'avez pas encore de dépôt GitHub pour ce projet :

1. Créez un nouveau dépôt sur https://github.com/new
2. Nom du dépôt : `kwezi-backend`
3. Visibilité : **Private** (ou Public selon votre choix)
4. Cliquez sur "Create repository"

### Étape 2 : Pousser le code backend

Depuis votre environnement Emergent ou local :

```bash
cd /app/backend
git init
git add .
git commit -m "Initial commit - Kwezi backend"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/kwezi-backend.git
git push -u origin main
```

### Étape 3 : Connecter Render à GitHub

1. Allez sur https://render.com/
2. Cliquez sur "New +" → "Web Service"
3. Sélectionnez "Build and deploy from a Git repository"
4. Connectez votre compte GitHub
5. Autorisez Render à accéder à votre dépôt `kwezi-backend`

### Étape 4 : Configuration du service

**Informations du service :**
- **Name** : `kwezi-backend`
- **Region** : `Frankfurt (EU Central)` (ou le plus proche de vos utilisateurs)
- **Branch** : `main`
- **Root Directory** : laisser vide (ou `.` si demandé)

**Build Settings :**
- **Runtime** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Étape 5 : Variables d'environnement

Cliquez sur "Advanced" puis ajoutez ces variables :

| Key | Value |
|-----|-------|
| `MONGO_URL` | `mongodb+srv://kwezi_user:VOTRE_MOT_DE_PASSE@kwezi-cluster.xxxxx.mongodb.net/mayotte_app?retryWrites=true&w=majority` |
| `DB_NAME` | `mayotte_app` |
| `STRIPE_SECRET_KEY` | `sk_test_51NE6WPCOUjCnz53N66xEX0NZq3zFOGJiPGR3jlcSPWkPKCvhQSQ9qgRh4C6tUmfZHBCCW` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_BZMfbZbZ48rvUQHdjKvdU5A0z9u2NVJy` |
| `PYTHON_VERSION` | `3.11.0` |

⚠️ **Important** : Remplacez `VOTRE_MOT_DE_PASSE` et l'URL MongoDB par les vôtres !

### Étape 6 : Déployer

1. Cliquez sur "Create Web Service"
2. Render va automatiquement :
   - Cloner votre dépôt
   - Installer les dépendances Python
   - Démarrer le serveur FastAPI
3. ⏰ Durée : ~5-10 minutes

### Étape 7 : Obtenir l'URL

Une fois le déploiement terminé, vous verrez l'URL de votre backend :

```
https://kwezi-backend.onrender.com
```

📝 **Notez cette URL ! Vous en aurez besoin pour configurer l'APK.**

### Étape 8 : Tester le backend

Ouvrez dans votre navigateur :

```
https://kwezi-backend.onrender.com/api/words?limit=5
```

Vous devriez voir 5 mots en JSON ! ✅

---

## Option B : Déploiement manuel (Sans GitHub)

### Étape 1 : Créer une archive du backend

Depuis votre environnement Emergent :

```bash
cd /app
tar -czf kwezi-backend.tar.gz backend/
```

### Étape 2 : Upload sur Render

Render ne support pas le déploiement manuel direct. Vous devrez utiliser **Option A (GitHub)** ou un service de stockage temporaire comme :

1. Upload `kwezi-backend.tar.gz` sur Google Drive/Dropbox
2. Créer un dépôt GitHub minimal avec juste les fichiers essentiels
3. Suivre Option A

---

##  Configuration HTTPS et CORS

Render fournit automatiquement un certificat SSL (HTTPS). Votre backend sera accessible via :

```
https://kwezi-backend.onrender.com
```

Si vous avez des problèmes CORS, ajoutez cette variable d'environnement dans Render :

```
CORS_ORIGINS=*
```

Ou mieux, listez uniquement les origines autorisées :

```
CORS_ORIGINS=https://mayotte-learn-4.preview.emergentagent.com,https://app.emergent.sh
```

---

## 🔍 Monitoring et Logs

### Voir les logs

1. Dans le dashboard Render, sélectionnez votre service `kwezi-backend`
2. Cliquez sur l'onglet "Logs"
3. Vous verrez tous les logs en temps réel

### Vérifier l'état du service

Dans "Events", vous verrez :
- **Live** : Le service fonctionne ✅
- **Failed** : Erreur de déploiement ❌

### Redéployer

Si vous faites des changements dans votre code GitHub :

1. Pushez les changements : `git push`
2. Render redéploie automatiquement ! 🎉

Ou manuellement :
1. Dans Render, cliquez sur "Manual Deploy" → "Deploy latest commit"

---

## ⚠️ Limitations du Plan Gratuit

Render offre un plan gratuit avec quelques limitations :

- ✅ **750 heures/mois** (suffisant pour un service 24/7)
- ✅ **Bande passante illimitée**
- ⚠️ **Le service s'endort après 15 min d'inactivité** (redémarre à la prochaine requête, ~30s de délai)
- ⚠️ **CPU/RAM limités** (suffisant pour Kwezi)

**Pour éviter l'endormissement** :
- Utilisez un service de "ping" comme UptimeRobot (gratuit)
- Ou passez au plan payant ($7/mois) pour avoir un service always-on

---

## 🆘 Problèmes Courants

### "Application failed to start"

1. Vérifiez les logs dans Render
2. Problème fréquent : `requirements.txt` manquant ou incorrect
3. Solution : Assurez-vous que `requirements.txt` est à la racine

### "MongoDB connection failed"

1. Vérifiez que `MONGO_URL` est correct
2. Vérifiez que l'IP `0.0.0.0/0` est autorisée dans MongoDB Atlas
3. Vérifiez que l'utilisateur MongoDB existe

### "502 Bad Gateway"

1. Le service est en cours de démarrage (attendez 1-2 min)
2. Ou le service a crashé (vérifiez les logs)

### Temps de réponse lent

1. C'est normal si le service vient de se réveiller (plan gratuit)
2. La première requête prend ~30 secondes
3. Les suivantes sont rapides

---

## 📚 Ressources Utiles

- [Documentation Render](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/deploy-fastapi)
- [Render Status](https://status.render.com/)

---

✅ **Une fois déployé, votre backend est accessible 24/7 depuis n'importe où dans le monde !**
