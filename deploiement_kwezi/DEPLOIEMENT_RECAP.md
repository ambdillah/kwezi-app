# 📦 Fichiers de Déploiement Kwezi - Récapitulatif

## 📁 Fichiers Exportés

### 1. Base de Données
- **Fichier** : `/app/backend/db_export.json` (0.66 MB)
- **Contenu** : 
  - 635 mots (Shimaoré + Kibouchi)
  - 270 phrases pour le jeu
  - 10 exercices pédagogiques
- **Utilisation** : Import dans MongoDB Atlas

### 2. Backup MongoDB (Format BSON)
- **Dossier** : `/app/backend/db_backup/mayotte_app/`
- **Fichiers** :
  - `words.bson` (635 documents)
  - `sentences.bson` (270 documents)
  - `exercises.bson` (10 documents)
  - `users.bson` (6 documents)
  - `user_progress.bson` (7 documents)
  - `user_badges.bson` (1 document)
- **Utilisation** : Restauration via `mongorestore`

### 3. Configuration Render.com
- **Fichier** : `/app/backend/render.yaml`
- **Utilisation** : Configuration automatique du déploiement

## 📖 Guides Créés

### 1. Guide Principal
- **Fichier** : `/app/GUIDE_DEPLOIEMENT_COMPLET.md`
- **Contenu** : Guide complet étape par étape pour :
  - Configuration MongoDB Atlas
  - Déploiement sur Render.com
  - Reconfiguration de l'APK
  - Tests complets

### 2. Guide Import MongoDB
- **Fichier** : `/app/GUIDE_IMPORT_MONGODB.md`
- **Contenu** : Instructions détaillées pour importer les données avec MongoDB Compass ou mongoimport

### 3. Guide Render
- **Fichier** : `/app/GUIDE_RENDER_DEPLOIEMENT.md`
- **Contenu** : Guide complet pour déployer le backend sur Render.com

## 🔑 Informations Importantes

### Clés Stripe (Mode Test)
```
STRIPE_SECRET_KEY=sk_test_51NE6WPCOUjCnz53N66xEX0NZq3zFOGJiPGR3jlcSPWkPKCvhQSQ9qgRh4C6tUmfZHBCCW
STRIPE_WEBHOOK_SECRET=whsec_BZMfbZbZ48rvUQHdjKvdU5A0z9u2NVJy
```

### Configuration MongoDB Locale
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=mayotte_app
```

### Configuration à mettre dans Render.com
```
MONGO_URL=mongodb+srv://kwezi_user:VOTRE_MOT_DE_PASSE@cluster.mongodb.net/mayotte_app
DB_NAME=mayotte_app
STRIPE_SECRET_KEY=sk_test_51NE6WPCOUjCnz53N66xEX0NZq3zFOGJiPGR3jlcSPWkPKCvhQSQ9qgRh4C6tUmfZHBCCW
STRIPE_WEBHOOK_SECRET=whsec_BZMfbZbZ48rvUQHdjKvdU5A0z9u2NVJy
```

## 📋 Checklist de Déploiement

### Phase 1 : MongoDB Atlas (15-20 min)
- [ ] Créer un compte MongoDB Atlas
- [ ] Créer un cluster gratuit (M0)
- [ ] Configurer l'accès réseau (0.0.0.0/0)
- [ ] Créer un utilisateur de base de données
- [ ] Obtenir l'URL de connexion
- [ ] Importer les données (635 mots + 270 phrases + 10 exercices)
- [ ] Vérifier que les données sont bien présentes

### Phase 2 : Déploiement Render.com (20-30 min)
- [ ] Créer un compte Render.com
- [ ] Préparer le code backend (GitHub ou manuel)
- [ ] Créer un nouveau Web Service
- [ ] Configurer les variables d'environnement
- [ ] Lancer le déploiement
- [ ] Attendre la fin du build (~5-10 min)
- [ ] Noter l'URL du backend (ex: https://kwezi-backend.onrender.com)
- [ ] Tester l'API : /api/words

### Phase 3 : Reconfiguration APK (15-20 min)
- [ ] Mettre à jour EXPO_BACKEND_URL dans /app/frontend/.env
- [ ] Rebuilder l'APK avec EAS
- [ ] Attendre la fin du build (~15-20 min)
- [ ] Télécharger le nouvel APK

### Phase 4 : Tests Complets (20-30 min)
- [ ] Tester les API backend dans le navigateur
- [ ] Installer l'APK sur Android
- [ ] Vérifier que les 635 mots s'affichent
- [ ] Tester l'audio Shimaoré/Kibouchi
- [ ] Tester les jeux (Quiz, Construire des phrases)
- [ ] Tester la navigation
- [ ] Tester le système premium (si activé)

## ⏱️ Durée Totale Estimée

- **Minimum** : 1h30
- **Moyenne** : 2h00
- **Maximum** : 2h30 (avec résolution de problèmes)

## 🆘 Support

Si vous rencontrez des problèmes à n'importe quelle étape :

1. **Consultez les guides** : Chaque guide contient une section "Problèmes courants"
2. **Vérifiez les logs** :
   - MongoDB Atlas : Database → Collections
   - Render : Dashboard → Logs
3. **Testez les URLs** :
   - Backend : https://VOTRE-URL.onrender.com/api/words
   - MongoDB : Utilisez MongoDB Compass pour vous connecter

## 📚 Ressources

- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Render.com](https://render.com/)
- [Expo EAS Build](https://docs.expo.dev/build/introduction/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## ✅ Résultat Final

Après avoir complété toutes les étapes :

✅ **Base de données cloud** accessible 24/7  
✅ **Backend API** déployé et fonctionnel  
✅ **APK Android** configuré pour utiliser le backend cloud  
✅ **Application complète** prête pour le Google Play Store  

---

**Bonne chance avec le déploiement ! 🚀**

Si vous avez des questions, n'hésitez pas à revenir vers moi pour assistance.
