# 🔧 CORRECTIONS BACKEND URL - À FAIRE SUR GITHUB

## ✅ DÉJÀ CORRIGÉS (dans Emergent):
- ✅ UserContext.tsx
- ✅ learn.tsx  
- ✅ games.tsx

## 🔴 À CORRIGER SUR GITHUB (5 fichiers):

---

### **1. frontend/app/offline.tsx** (3 endroits)

**Ajoutez en haut (après les imports):**
```typescript
import Constants from 'expo-constants';
```

**Ligne ~74, remplacez:**
```typescript
const wordsResponse = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`);
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const wordsResponse = await fetch(`${backendUrl}/api/words`);
```

**Ligne ~78, remplacez:**
```typescript
const exercisesResponse = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/exercises`);
```
**Par:**
```typescript
const exercisesResponse = await fetch(`${backendUrl}/api/exercises`);
```

**Ligne ~86, remplacez:**
```typescript
`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress/${encodeURIComponent(userName)}`
```
**Par:**
```typescript
`${backendUrl}/api/progress/${encodeURIComponent(userName)}`
```

---

### **2. frontend/app/progress.tsx** (2 endroits)

**Ajoutez en haut (après les imports):**
```typescript
import Constants from 'expo-constants';
```

**Ligne ~78, remplacez:**
```typescript
`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress/${encodeURIComponent(currentUser)}`
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const response = await fetch(
  `${backendUrl}/api/progress/${encodeURIComponent(currentUser)}`
```

**Ligne ~118, remplacez:**
```typescript
`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress`,
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const response = await fetch(
  `${backendUrl}/api/progress`,
```

---

### **3. frontend/app/admin.tsx** (4 endroits)

**Ajoutez en haut (après les imports):**
```typescript
import Constants from 'expo-constants';
```

**Ligne ~54, remplacez:**
```typescript
const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/init-base-content`, {
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const response = await fetch(`${backendUrl}/api/init-base-content`, {
```

**Ligne ~70, remplacez:**
```typescript
const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`);
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const response = await fetch(`${backendUrl}/api/words`);
```

**Lignes ~138-139, remplacez:**
```typescript
? `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words/${editingWord.id}`
: `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`;
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const url = editingWord
  ? `${backendUrl}/api/words/${editingWord.id}`
  : `${backendUrl}/api/words`;
```

**Ligne ~173, remplacez:**
```typescript
`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words/${wordId}`,
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const response = await fetch(
  `${backendUrl}/api/words/${wordId}`,
```

---

### **4. frontend/app/export.tsx** (1 endroit)

**Ajoutez en haut (après les imports):**
```typescript
import Constants from 'expo-constants';
```

**Ligne ~72, remplacez:**
```typescript
`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress/${encodeURIComponent(userName)}`
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
const response = await fetch(
  `${backendUrl}/api/progress/${encodeURIComponent(userName)}`
```

---

### **5. frontend/app/premium.tsx** (1 endroit - déjà partiellement corrigé)

**Ligne ~24, remplacez:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';
```
**Par:**
```typescript
const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
```

---

## ✅ VÉRIFICATION FINALE

Après avoir fait toutes les corrections sur GitHub, vérifiez qu'AUCUN fichier ne contient plus:
```
process.env.EXPO_PUBLIC_BACKEND_URL
```

**Recherche rapide sur GitHub:**
Allez dans votre dépôt → Utilisez la barre de recherche → Tapez: `process.env.EXPO_PUBLIC_BACKEND_URL`

Il ne devrait y avoir **AUCUN résultat** dans les fichiers `/app/` !

---

## 🚀 APRÈS LES CORRECTIONS

1. ✅ Toutes les modifications commitées sur GitHub
2. 🚀 Lancer le build: GitHub → Actions → Build Android APK → Run workflow
3. ⏱️ Attendre 15-20 minutes
4. 📥 Télécharger l'APK
5. 📱 Tester sur Android - **LES DONNÉES DEVRAIENT SE CHARGER!**
