# 🟢 Déploiement sur Netlify

## La méthode la plus rapide (2 minutes)

---

## Pourquoi Netlify ?

- ✅ **Gratuit** (pas de carte bancaire requise)
- ✅ **Ultra rapide** : Déploiement en 30 secondes
- ✅ **HTTPS automatique**
- ✅ **URL personnalisable** : `kwezi-app.netlify.app`
- ✅ **CDN global** (chargement rapide partout dans le monde)
- ✅ **Mises à jour simples** (drag & drop)

---

## Méthode 1 : Drag & Drop (Plus simple)

### Étape 1 : Créer un compte Netlify

1. Allez sur [Netlify](https://www.netlify.com)
2. Cliquez sur **"Sign up"**
3. Inscrivez-vous avec :
   - GitHub (recommandé)
   - GitLab
   - Bitbucket
   - Ou email

### Étape 2 : Déployer votre site

1. Une fois connecté, vous verrez la page d'accueil Netlify
2. Faites **glisser-déposer** le dossier `landing_page/` directement sur la zone indiquée
   - Ou cliquez sur **"Add new site"** → **"Deploy manually"**
3. Attendez 10-30 secondes ⏱️
4. ✅ **C'est en ligne !**

### Étape 3 : Votre URL

Netifly vous donne automatiquement une URL :

```
https://random-name-123456.netlify.app
```

**Personnalisez-la :**

1. Cliquez sur **"Site settings"**
2. Sous **"Site details"**, cliquez sur **"Change site name"**
3. Entrez : `kwezi-app` (si disponible)
4. Votre URL devient : `https://kwezi-app.netlify.app` 🎉

---

## Méthode 2 : Via GitHub (Pour mises à jour automatiques)

### Étape 1 : Créer un dépôt GitHub

1. Créez un dépôt sur GitHub avec les fichiers de `landing_page/`
2. (Voir `deploy-github.md` pour les détails)

### Étape 2 : Connecter à Netlify

1. Sur Netlify, cliquez sur **"Add new site"** → **"Import an existing project"**
2. Sélectionnez **"GitHub"**
3. Autorisez Netlify à accéder à votre compte GitHub
4. Sélectionnez votre dépôt `kwezi-landing`
5. Configuration du build :
   - **Build command :** (Laissez vide)
   - **Publish directory :** (Laissez vide ou mettez `/`)
6. Cliquez sur **"Deploy site"**
7. Attendez 1-2 minutes ⏱️
8. ✅ **C'est en ligne !**

**Avantage :** Chaque fois que vous modifiez un fichier sur GitHub, Netlify met à jour automatiquement votre site.

---

## ✅ URL à fournir au Play Store

**Copiez cette URL et collez-la dans le formulaire Google Play Store :**

```
https://kwezi-app.netlify.app
```

(Ou votre nom personnalisé)

---

## 🔄 Mettre à jour votre site

### Si vous avez déployé via Drag & Drop :

1. Allez sur votre dashboard Netlify
2. Cliquez sur votre site
3. Allez dans **"Deploys"**
4. Glissez-déposez le nouveau dossier `landing_page/` mis à jour
5. ✅ Mis à jour en 30 secondes

### Si vous avez connecté GitHub :

1. Modifiez vos fichiers sur GitHub
2. Commitez les changements
3. Netlify déploie automatiquement en 1-2 minutes

---

## 📌 Domaine personnalisé (Optionnel)

Si vous achetez un domaine (ex: `kwezi-app.com`) :

### Étape 1 : Ajouter le domaine sur Netlify

1. Dans votre site Netlify, allez dans **"Domain settings"**
2. Cliquez sur **"Add custom domain"**
3. Entrez : `kwezi-app.com`
4. Netlify vous donne les serveurs DNS à configurer

### Étape 2 : Configurer les DNS

Chez votre registrar (Namecheap, OVH, Google Domains, etc.) :

1. Trouvez la section **"DNS Management"** ou **"Name Servers"**
2. Remplacez les serveurs DNS par ceux de Netlify :
   ```
   dns1.p01.nsone.net
   dns2.p01.nsone.net
   dns3.p01.nsone.net
   dns4.p01.nsone.net
   ```
3. Attendez 24-48h pour la propagation DNS

### Étape 3 : Activer HTTPS

1. Netlify active automatiquement HTTPS avec Let's Encrypt
2. Votre site sera accessible en `https://kwezi-app.com` 🔒

---

## 🎯 Fonctionnalités bonus de Netlify

### Formulaires

Ajoutez un formulaire de contact facilement :

```html
<form name="contact" method="POST" data-netlify="true">
  <input type="text" name="name" placeholder="Nom" />
  <input type="email" name="email" placeholder="Email" />
  <textarea name="message" placeholder="Message"></textarea>
  <button type="submit">Envoyer</button>
</form>
```

Netlify gère automatiquement les soumissions.

### Analytics (Optionnel - Payant)

Voir le trafic de votre site directement dans Netlify.

---

## 🆘 Problèmes courants

### Le site ne se met pas à jour
- Videz le cache : **Ctrl+F5** (ou Cmd+Shift+R sur Mac)
- Allez dans **Deploys** → **Trigger deploy** → **Deploy site**

### Erreur de déploiement
- Vérifiez que `index.html` est à la racine du dossier
- Vérifiez qu'il n'y a pas de fichiers corrompus

### Les images ne s'affichent pas
- Vérifiez les chemins : utilisez `./assets/image.png`
- Assurez-vous que le dossier `assets/` est inclus

---

## 🎉 C'est fait !

Votre landing page est maintenant en ligne sur Netlify !

**URL finale :** `https://kwezi-app.netlify.app` 🚀

---

## 📊 Comparaison GitHub Pages vs Netlify

| Critère | GitHub Pages | Netlify |
|---------|--------------|----------|
| Vitesse de déploiement | 1-2 min | 30 sec |
| Mise à jour | Via Git | Drag & Drop ou Git |
| Domaine personnalisé | ✅ | ✅ |
| HTTPS | ✅ | ✅ |
| Formulaires | ❌ | ✅ |
| CDN Global | ✅ | ✅ ✅ (meilleur) |
| Interface | Basique | Très intuitive |

**Recommandation :** Netlify pour la simplicité, GitHub Pages si vous préférez tout sur GitHub.
