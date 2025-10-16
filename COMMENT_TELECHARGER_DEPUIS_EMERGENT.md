# 📥 Comment télécharger les fichiers depuis Emergent

## Méthode complète étape par étape

---

## 📍 LOCALISATION DES FICHIERS

Les 2 fichiers sont dans le dossier `/tmp/` :

1. **Code :** `/tmp/kwezi-frontend-code.tar.gz` (50 MB)
2. **Audio :** `/tmp/kwezi-audio.tar.gz` (31 MB)

---

## 🎯 MÉTHODE 1 : Via l'explorateur de fichiers Emergent

### Étape 1 : Ouvrir l'explorateur de fichiers

Dans l'interface Emergent, cherchez :
- Un bouton **"Files"** ou **"Explorer"** dans la barre latérale (généralement à gauche)
- Ou un icône de dossier 📁
- Ou un menu avec "Browse Files" / "File Manager"

### Étape 2 : Naviguer vers /tmp

1. Dans l'explorateur de fichiers, vous devriez voir l'arborescence
2. Cliquez sur la racine `/` (ou tapez `/tmp` dans la barre de navigation)
3. Trouvez et ouvrez le dossier **`tmp`**

### Étape 3 : Télécharger les fichiers

Dans le dossier `/tmp`, vous devriez voir :
```
kwezi-frontend-code.tar.gz (50 MB)
kwezi-audio.tar.gz (31 MB)
```

**Pour télécharger chaque fichier :**
- Clic droit sur le fichier → "Download" / "Télécharger"
- OU cliquez sur le fichier et cherchez un bouton de téléchargement ⬇️
- OU sélectionnez le fichier et appuyez sur un bouton d'action

---

## 🎯 MÉTHODE 2 : Via le terminal intégré

Si l'explorateur de fichiers ne fonctionne pas, utilisez le terminal :

### Étape 1 : Ouvrir le terminal

Dans Emergent, trouvez :
- Un onglet **"Terminal"** ou **"Console"**
- Ou un bouton pour ouvrir un terminal

### Étape 2 : Créer un serveur HTTP simple

Dans le terminal, tapez ces commandes :

```bash
# Aller dans le dossier /tmp
cd /tmp

# Démarrer un serveur HTTP sur le port 9000
python3 -m http.server 9000
```

Le terminal affichera :
```
Serving HTTP on 0.0.0.0 port 9000 (http://0.0.0.0:9000/) ...
```

### Étape 3 : Accéder aux fichiers

Dans votre navigateur, allez sur :
```
https://shimakibouchi.preview.emergentagent.com:9000
```

Vous verrez une liste de fichiers. Cliquez sur :
1. `kwezi-frontend-code.tar.gz` pour télécharger
2. `kwezi-audio.tar.gz` pour télécharger

---

## 🎯 MÉTHODE 3 : Utiliser les liens API (Le plus simple)

**J'ai déjà créé des routes API qui fonctionnent !**

Cliquez directement sur ces liens :

### 📥 Code de l'application (50 MB)
```
https://shimakibouchi.preview.emergentagent.com/api/download/code
```

### 📥 Fichiers audio (31 MB)
```
https://shimakibouchi.preview.emergentagent.com/api/download/audio
```

**Ces liens fonctionnent dans n'importe quel navigateur !**

---

## 🎯 MÉTHODE 4 : Si rien ne fonctionne - Commande wget/curl

Si vous avez accès à un terminal sur votre ordinateur local :

```bash
# Télécharger le code
wget https://shimakibouchi.preview.emergentagent.com/api/download/code -O kwezi-frontend-code.tar.gz

# Télécharger l'audio
wget https://shimakibouchi.preview.emergentagent.com/api/download/audio -O kwezi-audio.tar.gz
```

Ou avec curl :

```bash
# Télécharger le code
curl -L https://shimakibouchi.preview.emergentagent.com/api/download/code -o kwezi-frontend-code.tar.gz

# Télécharger l'audio
curl -L https://shimakibouchi.preview.emergentagent.com/api/download/audio -o kwezi-audio.tar.gz
```

---

## ✅ VÉRIFICATION APRÈS TÉLÉCHARGEMENT

Une fois téléchargés, vérifiez les tailles :

- **kwezi-frontend-code.tar.gz** doit faire environ **50 MB**
- **kwezi-audio.tar.gz** doit faire environ **31 MB**

Si les fichiers sont beaucoup plus petits (quelques Ko), c'est que le téléchargement a échoué.

---

## 🔧 EN CAS DE PROBLÈME

### Problème : "Je ne trouve pas l'explorateur de fichiers"

**Solution :** Utilisez la **Méthode 3** (liens API) - c'est la plus simple !

### Problème : "Les liens ne téléchargent pas"

**Solution :** Essayez de :
1. Faire un clic droit → "Enregistrer le lien sous..."
2. Copier le lien et le coller dans un nouvel onglet
3. Utiliser un autre navigateur (Chrome, Firefox, Edge)

### Problème : "Le téléchargement s'arrête"

**Solution :** 
1. Vérifiez votre connexion internet
2. Réessayez le téléchargement
3. Les fichiers restent disponibles pendant plusieurs heures

---

## 📝 RÉSUMÉ - MÉTHODE LA PLUS SIMPLE

**🎯 Utilisez directement ces liens dans votre navigateur :**

1. Cliquez ici pour télécharger le **CODE** :
   ```
   https://shimakibouchi.preview.emergentagent.com/api/download/code
   ```

2. Cliquez ici pour télécharger l'**AUDIO** :
   ```
   https://shimakibouchi.preview.emergentagent.com/api/download/audio
   ```

**C'est tout ! Pas besoin d'explorer l'interface Emergent.**

---

## 🚀 APRÈS TÉLÉCHARGEMENT

Une fois les 2 fichiers téléchargés :

1. **Extrayez-les** (7-Zip sur Windows, tar sur Mac/Linux)
2. **Installez Node.js** : https://nodejs.org
3. **Suivez le guide** `/app/GUIDE_BUILD_LOCAL.md` (inclus dans les fichiers)
4. **Lancez le build** avec les commandes que je vous ai données

---

**La solution la plus simple : CLIQUEZ SUR LES LIENS API ! Ils fonctionnent à 100% !** 🎯
