# 🎯 Guide Build EAS - Étape par Étape
## Création du build AAB pour Kwezi

**Statut :** En cours  
**Package name :** com.mahoraiseducation.kwezi

---

## ✅ ÉTAPE 1 : Créer un compte Expo

### Ce que vous devez faire :

1. **Ouvrez un nouvel onglet et allez sur :** https://expo.dev
2. **Cliquez sur "Sign up"** (en haut à droite)
3. **Choisissez une méthode d'inscription :**
   - Avec votre email
   - Ou avec GitHub
   - Ou avec Google

4. **Complétez l'inscription**
5. **Vérifiez votre email** (si demandé)

### Informations à me communiquer :

Une fois votre compte créé, dites-moi :
- ✅ "J'ai créé mon compte Expo"
- ✅ Votre email Expo (pour la connexion)

---

## ⏳ ÉTAPE 2 : Se connecter à Expo (JE M'EN OCCUPE)

**Je vais exécuter :** `eas login`

**Deux options :**

### Option A : Vous me donnez vos identifiants temporairement
- Email Expo
- Mot de passe

Je me connecte pour vous, puis vous changez votre mot de passe après.

### Option B : Connexion manuelle (plus sécurisé)
Je vous donne les commandes à exécuter sur votre machine locale.

**Quelle option préférez-vous ?**

---

## ⏳ ÉTAPE 3 : Initialiser le projet EAS (JE M'EN OCCUPE)

Une fois connecté, je vais exécuter :

```bash
cd /app/frontend
eas build:configure
```

Cela va :
- Créer un projet EAS
- Lier votre app à votre compte Expo
- Configurer le build

**Temps estimé :** 2 minutes

---

## ⏳ ÉTAPE 4 : Lancer le build de production (JE M'EN OCCUPE)

```bash
eas build --platform android --profile production
```

**Ce qui va se passer :**

1. EAS analyse votre code
2. Upload vers les serveurs Expo (peut prendre 2-5 minutes)
3. Build sur les serveurs Expo (**10-20 minutes**)
4. Vous recevez un email quand c'est terminé
5. Le fichier AAB sera téléchargeable

**Pendant le build, vous pouvez :**
- Fermer cette page (le build continue sur les serveurs)
- Suivre l'avancement sur https://expo.dev (dans votre compte)

---

## ⏳ ÉTAPE 5 : Télécharger le AAB (ENSEMBLE)

Une fois le build terminé :

```bash
eas build:download --platform android --profile production
```

Ou téléchargez depuis le dashboard Expo.

**Vous obtiendrez :** `kwezi-1.0.0.aab` (environ 30-50 MB)

---

## ⏳ ÉTAPE 6 : Uploader sur Play Console (VOUS)

1. Allez sur https://play.google.com/console
2. Créez votre application "Kwezi"
3. Uploadez le fichier AAB
4. Remplissez la fiche (textes fournis dans les guides)
5. Soumettez pour review

---

## 📊 PROGRESSION ACTUELLE

- [x] ✅ EAS CLI installé
- [x] ✅ Configuration app.json prête
- [x] ✅ Configuration eas.json prête
- [ ] ⏳ Compte Expo créé → **VOUS ÊTES ICI** 👈
- [ ] ⏳ Connexion à Expo
- [ ] ⏳ Initialisation projet EAS
- [ ] ⏳ Build lancé
- [ ] ⏳ Build terminé (10-20 min)
- [ ] ⏳ AAB téléchargé
- [ ] ⏳ Upload sur Play Console

---

## ⏱️ TEMPS TOTAL ESTIMÉ

- Création compte Expo : **3 minutes** → MAINTENANT
- Connexion : **1 minute**
- Initialisation : **2 minutes**
- Lancement build : **1 minute**
- **Build sur serveurs : 10-20 minutes** ⏱️
- Téléchargement : **1 minute**

**TOTAL : ~20-30 minutes**

---

## 🆘 EN CAS DE PROBLÈME

### Erreur de connexion
- Vérifiez votre email/mot de passe
- Vérifiez que votre compte Expo est activé

### Build échoue
- Je vérifierai les logs
- Je corrigerai si nécessaire
- On relancera le build

### Timeout
- Le build peut prendre jusqu'à 30 minutes
- C'est normal pour un premier build

---

## 📞 PROCHAINE ACTION

**👉 CRÉEZ VOTRE COMPTE EXPO MAINTENANT : https://expo.dev**

Dites-moi quand c'est fait et comment vous voulez procéder pour la connexion (Option A ou B).

---

*Guide créé le 15 octobre 2025*
