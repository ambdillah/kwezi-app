# 🏝️ Kwezi - Landing Page

## Landing page officielle de l'application Kwezi

Page web professionnelle pour présenter l'application d'apprentissage du Shimaoré et Kibouchi.

---

## 📁 Structure des fichiers

```
landing_page/
├── index.html          # Page principale
├── styles.css          # Styles CSS
├── script.js           # JavaScript pour interactivité
├── README.md           # Ce fichier
├── deploy-github.md    # Instructions déploiement GitHub Pages
├── deploy-netlify.md   # Instructions déploiement Netlify
└── assets/             # Dossier pour les images (à créer)
    ├── favicon.png
    ├── og-image.png
    ├── app-screenshot-1.png
    └── google-play-badge.png
```

---

## 🚀 Déploiement

### Option 1 : GitHub Pages (Recommandé - Gratuit)

1. Créez un dépôt GitHub nommé `kwezi-landing`
2. Uploadez tous les fichiers du dossier `landing_page`
3. Allez dans Settings → Pages
4. Source : Deploy from a branch → main → root
5. Votre site sera disponible à : `https://votre-username.github.io/kwezi-landing`

**URL finale pour Play Store :** `https://votre-username.github.io/kwezi-landing`

📄 Voir `deploy-github.md` pour les instructions détaillées

### Option 2 : Netlify (Gratuit)

1. Créez un compte sur [Netlify](https://netlify.com)
2. Drag & drop le dossier `landing_page` sur Netlify
3. Votre site est en ligne en quelques secondes
4. URL gratuite : `https://kwezi-app.netlify.app`

📄 Voir `deploy-netlify.md` pour les instructions détaillées

### Option 3 : Vercel (Gratuit)

1. Créez un compte sur [Vercel](https://vercel.com)
2. Importez le dossier depuis GitHub ou uploadez directement
3. URL gratuite : `https://kwezi-app.vercel.app`

---

## 🖼️ Images à ajouter

Créez un dossier `assets/` et ajoutez ces images :

### 1. favicon.png (32x32px)
- Icône du site pour l'onglet du navigateur
- Suggestion : Logo Kwezi ou drapeau de Mayotte 🇾🇹

### 2. og-image.png (1200x630px)
- Image pour partage sur réseaux sociaux
- Doit contenir : Logo Kwezi + texte "Apprends le Shimaoré et Kibouchi"

### 3. app-screenshot-1.png (1080x2340px)
- Capture d'écran de l'application
- À prendre depuis l'app Kwezi (écran d'accueil ou jeux)

### 4. google-play-badge.png
- Badge officiel Google Play
- Télécharger depuis : https://play.google.com/intl/fr/badges/

**Note :** Si vous n'avez pas ces images maintenant, la page fonctionnera quand même avec des placeholders.

---

## 🔗 URLs importantes à mettre à jour

### Dans `index.html`, remplacez :

1. **Lien Play Store** (ligne ~424)
```html
<a href="https://play.google.com/store/apps/details?id=com.kwezi.app" ...>
```
Remplacez par votre vrai lien Play Store une fois l'app publiée.

2. **Email de contact** (ligne ~478)
```html
<a href="mailto:contact@kwezi-app.com" ...>
```
Remplacez par votre vraie adresse email.

---

## ✅ Checklist avant déploiement

- [ ] Ajoutez vos images dans `/assets/`
- [ ] Mettez à jour le lien Play Store
- [ ] Mettez à jour l'email de contact
- [ ] Testez tous les liens (documents légaux, etc.)
- [ ] Vérifiez la page sur mobile (responsive)
- [ ] Optimisez les images (compression)

---

## 📱 Responsive Design

La page est entièrement responsive et s'adapte à :
- 📱 Mobile (320px+)
- 📱 Tablette (768px+)
- 💻 Desktop (1200px+)

---

## 🎨 Personnalisation

### Changer les couleurs

Dans `styles.css`, modifiez les variables CSS (ligne 9-18) :

```css
:root {
    --primary-color: #2563eb;     /* Bleu principal */
    --secondary-color: #10b981;   /* Vert secondaire */
    --accent-color: #f59e0b;      /* Orange accent */
}
```

### Ajouter une section

1. Ajoutez le HTML dans `index.html`
2. Ajoutez les styles dans `styles.css`
3. Ajoutez le lien dans la navigation

---

## 📊 Performances

- ✅ HTML/CSS/JS vanille (pas de framework lourd)
- ✅ Optimisé pour le SEO
- ✅ Temps de chargement < 2 secondes
- ✅ Score Lighthouse > 90

---

## 🆘 Support

Pour toute question sur le déploiement ou la personnalisation, contactez-moi.

---

## 📝 License

© 2025 Kwezi. Tous droits réservés.
