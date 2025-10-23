# 🔧 CORRECTION URL BACKEND POUR APK FONCTIONNEL

## ❌ **PROBLÈME IDENTIFIÉ**

L'APK est vide car il utilise l'**ancienne URL backend** :
```
https://kwezi-android.preview.emergentagent.com
```

Au lieu de la **nouvelle URL Render.com** :
```
https://kwezi-backend.onrender.com
```

---

## ✅ **SOLUTION : Ajouter une variable d'environnement au workflow**

### **Étape 1 : Modifiez le workflow GitHub Actions**

1. Allez sur : https://github.com/ambdillah/kwezi-app/blob/main/.github/workflows/build-apk.yml

2. Cliquez sur le **crayon** ✏️

3. Trouvez la section **"Build APK with EAS"** (vers la ligne 37)

4. **Remplacez** :
```yaml
    - name: Build APK with EAS
      working-directory: ./frontend
      run: |
        echo "🚀 Starting EAS Build..."
        eas build --platform android --profile production --non-interactive --wait
      env:
        EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}
```

**Par** :
```yaml
    - name: Build APK with EAS
      working-directory: ./frontend
      run: |
        echo "🚀 Starting EAS Build..."
        echo "EXPO_PUBLIC_BACKEND_URL=https://kwezi-backend.onrender.com" > .env
        cat .env
        eas build --platform android --profile production --non-interactive --wait
      env:
        EXPO_TOKEN: ${{ secrets.EXPO_TOKEN }}
```

5. **Commitez** : `fix: Set correct backend URL for APK build`

---

## 🚀 **CE QUI VA SE PASSER**

1. Le workflow va créer un fichier `.env` avec la bonne URL
2. Le build EAS va utiliser cette URL
3. L'APK généré se connectera au backend Render.com
4. Vous aurez enfin un APK avec toutes les données ! 🎉

---

## ⏰ **TIMELINE**

- **Maintenant** : Modifier le workflow (2 min)
- **Build** : 20-25 min
- **Test** : 5 min

**TOTAL : ~30 minutes pour un APK fonctionnel !**

---

## 📱 **APRÈS LE BUILD**

1. Téléchargez le nouvel APK depuis Artifacts
2. Installez sur votre téléphone
3. **Cette fois, les 635 mots devraient s'afficher !** ✅

---

**FAITES CETTE MODIFICATION MAINTENANT !** 💪
