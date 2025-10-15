# 📘 Déploiement sur GitHub Pages

## Instructions complètes étape par étape

---

## Prérequis

- Un compte GitHub (gratuit)
- Les fichiers de la landing page

---

## Étape 1 : Créer un dépôt GitHub

1. Allez sur [GitHub](https://github.com)
2. Cliquez sur le bouton **"+"** en haut à droite
3. Sélectionnez **"New repository"**
4. Remplissez les informations :
   - **Repository name :** `kwezi-landing` (ou autre nom)
   - **Description :** "Landing page officielle de l'app Kwezi"
   - **Public** (obligatoire pour GitHub Pages gratuit)
   - ✅ Cochez "Add a README file"
5. Cliquez sur **"Create repository"**

---

## Étape 2 : Uploader les fichiers

### Méthode A : Via l'interface web (Plus simple)

1. Sur la page de votre dépôt, cliquez sur **"Add file"** → **"Upload files"**
2. Glissez-déposez tous les fichiers de `landing_page/` :
   - `index.html`
   - `styles.css`
   - `script.js`
   - Dossier `assets/` (si vous l'avez créé)
3. Ajoutez un message de commit : "Initial landing page"
4. Cliquez sur **"Commit changes"**

### Méthode B : Via Git (Pour développeurs)

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/kwezi-landing.git
cd kwezi-landing

# Copier les fichiers de landing_page/
cp -r /chemin/vers/landing_page/* .

# Commiter et pusher
git add .
git commit -m "Initial landing page"
git push origin main
```

---

## Étape 3 : Activer GitHub Pages

1. Dans votre dépôt, allez dans **Settings** (icône engrenage)
2. Dans le menu latéral gauche, cliquez sur **"Pages"**
3. Sous **"Source"** :
   - Sélectionnez **"Deploy from a branch"**
   - Branch : **main**
   - Folder : **/ (root)**
4. Cliquez sur **"Save"**
5. Attendez 1-2 minutes ⏱️

---

## Étape 4 : Obtenir votre URL

Votre site sera disponible à :

```
https://votre-username.github.io/kwezi-landing
```

**Exemple :**
- Si votre username GitHub est `johnmahorais`
- URL : `https://johnmahorais.github.io/kwezi-landing`

---

## Étape 5 : Tester votre site

1. Ouvrez l'URL dans votre navigateur
2. Vérifiez que tout s'affiche correctement
3. Testez sur mobile (ouvrez l'URL sur votre téléphone)
4. Vérifiez tous les liens

---

## ✅ URL à fournir au Play Store

**Copiez cette URL et collez-la dans le formulaire Google Play Store :**

```
https://votre-username.github.io/kwezi-landing
```

---

## 🔄 Mettre à jour votre site

### Si vous modifiez des fichiers :

1. Allez dans votre dépôt GitHub
2. Cliquez sur le fichier à modifier (ex: `index.html`)
3. Cliquez sur l'icône **crayon** (Edit)
4. Faites vos modifications
5. Cliquez sur **"Commit changes"**
6. Attendez 1-2 minutes, les changements seront en ligne

---

## 📌 Domaine personnalisé (Optionnel)

Si vous achetez un domaine (ex: `kwezi-app.com`) :

1. Allez dans **Settings → Pages**
2. Sous **"Custom domain"**, entrez : `kwezi-app.com`
3. Configurez les DNS chez votre registrar (Namecheap, OVH, etc.)
4. Ajoutez ces enregistrements DNS :
   ```
   A     @     185.199.108.153
   A     @     185.199.109.153
   A     @     185.199.110.153
   A     @     185.199.111.153
   CNAME www   votre-username.github.io
   ```

---

## 🆘 Problèmes courants

### Le site ne s'affiche pas
- Attendez 2-5 minutes après activation
- Vérifiez que `index.html` est à la racine du dépôt
- Actualisez la page avec **Ctrl+F5** (vider le cache)

### Erreur 404
- Vérifiez que le dépôt est **public**
- Vérifiez que GitHub Pages est activé dans Settings

### Les images ne s'affichent pas
- Vérifiez les chemins : `./assets/image.png` (avec le `./`)
- Vérifiez que les images sont bien uploadées

---

## 🎉 C'est fait !

Votre landing page est maintenant en ligne et accessible au monde entier !

**URL finale :** `https://votre-username.github.io/kwezi-landing` 🚀
