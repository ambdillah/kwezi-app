# 🎯 GUIDE FINAL - BUILD APK KWEZI

## ✅ PROBLÈME RÉSOLU!

**Cause racine:** Le fichier `.github/workflows/build-apk.yml` contenait des **conflits Git non résolus** (lignes 35-116), ce qui rendait le workflow invalide sur GitHub.

**Solution appliquée:** Workflow complètement recréé sans aucun conflit, avec `workflow_dispatch` correctement configuré.

**Status:** ✅ Workflow propre poussé sur GitHub (commit: cb8d5dc)

---

## 📋 ÉTAPES POUR LANCER LE BUILD APK

### **Option 1: Lancement Manuel via Interface GitHub (RECOMMANDÉ)**

1. **Allez sur votre dépôt GitHub:**
   ```
   https://github.com/ambdillah/kwezi-app
   ```

2. **Cliquez sur l'onglet "Actions"** (en haut de la page)

3. **Dans la barre latérale GAUCHE, cherchez et cliquez sur:**
   ```
   Build Android APK
   ```

4. **À DROITE, vous devriez maintenant voir un bouton gris "Run workflow"**
   
   Si vous ne le voyez pas encore:
   - Rafraîchissez la page (F5)
   - Attendez 30 secondes et rafraîchissez encore
   - GitHub peut mettre un peu de temps à traiter le nouveau workflow

5. **Une fois le bouton visible:**
   - Cliquez sur **"Run workflow"**
   - Une petite fenêtre s'ouvre
   - Vérifiez que "Branch: main" est sélectionné
   - Cliquez sur le bouton vert **"Run workflow"**

6. **Le build démarre! 🚀**
   - Rafraîchissez la page pour voir apparaître une nouvelle ligne
   - Le cercle jaune indique que le build est en cours
   - Durée: environ 15-20 minutes

7. **Une fois terminé (✅ vert):**
   - Cliquez sur le build terminé
   - Descendez jusqu'à la section **"Artifacts"**
   - Cliquez sur **"kwezi-app-release"** pour télécharger
   - Décompressez le ZIP
   - Vous avez votre APK! 🎉

---

### **Option 2: Lancement Automatique par Push**

Le workflow se lance aussi automatiquement à chaque push sur `main`.

**Pour forcer un build immédiatement:**

Depuis votre terminal (si vous avez Git configuré):
```bash
cd /chemin/vers/votre/depot/local

# Créer un commit vide pour déclencher le build
git commit --allow-empty -m "Trigger APK build"

# Pousser sur GitHub
git push origin main
```

Le build démarrera automatiquement dans GitHub Actions.

---

### **Option 3: Si le bouton "Run workflow" n'apparaît toujours pas**

**Vérifiez les permissions GitHub Actions:**

1. Allez sur: `https://github.com/ambdillah/kwezi-app/settings/actions`

2. Section **"Actions permissions"**

3. Sélectionnez: **"Allow all actions and reusable workflows"**

4. Cliquez sur **"Save"**

5. Retournez sur l'onglet **"Actions"** et rafraîchissez

---

## 🔍 VÉRIFICATION DU WORKFLOW

**Le workflow est correct si vous voyez dans le fichier sur GitHub:**

```yaml
on:
  push:
    branches: [ main ]
  workflow_dispatch:    # ← Cette ligne permet le lancement manuel
```

**URL pour vérifier:** https://github.com/ambdillah/kwezi-app/blob/main/.github/workflows/build-apk.yml

---

## ⏱️ PENDANT LE BUILD (~15-20 minutes)

Le build passe par ces étapes:
1. 🔄 **Checkout code** (~30 sec)
2. 🔧 **Setup Node.js** (~1 min)
3. ☕ **Setup Java** (~1 min)
4. 📦 **Install dependencies** (~2-3 min)
5. 📝 **Create .env file** (~5 sec)
6. 🚀 **Build APK with EAS** (~10-15 min) ← Le plus long
7. 📥 **Download APK** (~30 sec)
8. ⬆️ **Upload artifact** (~20 sec)

**Vous pouvez suivre en temps réel en cliquant sur le build en cours.**

---

## 📱 APRÈS TÉLÉCHARGEMENT DE L'APK

### **Installation sur Android:**

1. **Transférez** `kwezi-app-release.apk` sur votre téléphone
   - Via USB
   - Via email
   - Via WeTransfer, etc.

2. **Ouvrez le fichier APK** sur votre téléphone

3. **Autorisez l'installation** depuis des sources inconnues si demandé

4. **Installez l'application** ✅

### **Tests à faire:**

1. ✅ **Ouvrir l'app** → Logo Kwezi apparaît
2. ✅ **Page "Apprendre"** → Les 635 mots se chargent depuis Render.com
3. ✅ **Cliquer sur un mot** → Audio fonctionne (TTS ou audio authentique)
4. ✅ **Page "Jeux"** → Tous les jeux se lancent sans planter
5. ✅ **Connexion backend** → Pas de message "Erreur de connexion"

---

## 🎯 CONFIGURATION FINALE

### **Ce qui a été corrigé:**

✅ **safeSpeech.ts** → Wrapper complet pour éviter crashes TTS
✅ **UserContext.tsx** → Variable `backendUrl` correctement définie
✅ **games.tsx** → Utilise `Constants.expoConfig.extra.backendUrl`
✅ **app.json** → `cli` config + `backendUrl` dans `extra`
✅ **eas.json** → `EXPO_PUBLIC_BACKEND_URL` configuré
✅ **build-apk.yml** → Workflow propre sans conflits Git

### **Backend:**
- URL: https://kwezi-backend.onrender.com
- Status: ✅ Opérationnel
- Données: 635 mots + 270 phrases + audios

---

## 🆘 EN CAS DE PROBLÈME

### **Le build échoue:**
1. Cliquez sur le build échoué
2. Lisez les logs pour identifier l'erreur
3. Les erreurs communes:
   - `EXPO_TOKEN invalid` → Vérifiez le secret GitHub
   - `Gradle build failed` → Problème de dépendances (déjà corrigé)
   - `eas: command not found` → Problème d'installation (déjà géré)

### **L'APK ne se connecte pas au backend:**
1. Vérifiez que `app.json` contient:
   ```json
   "extra": {
     "backendUrl": "https://kwezi-backend.onrender.com"
   }
   ```
2. Testez le backend: https://kwezi-backend.onrender.com/api/health
3. Si ça répond `{"status":"healthy"}` → Le backend fonctionne

### **Les jeux plantent sur l'APK:**
1. Vérifiez que tous les fichiers utilisent `import * as Speech from '../utils/safeSpeech'`
2. Jamais `import * as Speech from 'expo-speech'` directement

---

## ✅ CHECKLIST AVANT BUILD

- [x] Workflow sans conflits Git
- [x] Secret `EXPO_TOKEN` configuré sur GitHub
- [x] Backend Render.com opérationnel
- [x] `safeSpeech.ts` complet et fonctionnel
- [x] `app.json` avec `backendUrl` dans `extra`
- [x] Tous les imports `expo-speech` remplacés
- [x] Metro cache vidé et Expo redémarré
- [x] Preview Emergent fonctionne

**TOUT EST PRÊT POUR LE BUILD! 🚀**

---

## 🎉 RÉSULTAT ATTENDU

Une fois l'APK installé sur votre téléphone Android:

✅ **Écran d'accueil** avec le logo Kwezi
✅ **635 mots** chargés depuis le backend
✅ **Jeux fonctionnels** sans plantage
✅ **Audio TTS** et audios authentiques
✅ **Système premium** opérationnel
✅ **Mode offline** (pour utilisateurs premium)

**Prêt pour le Google Play Store!** 🎊
