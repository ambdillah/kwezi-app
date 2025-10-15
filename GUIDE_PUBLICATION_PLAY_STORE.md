# 🚀 Guide de Publication sur Google Play Store
## Application Kwezi - Étapes complètes

**Date :** 15 octobre 2025  
**Statut compte développeur :** ✅ Créé  
**Prochaine étape :** Publier l'application

---

## 📋 TABLE DES MATIÈRES

1. [Préparer l'application](#1-préparer-lapplication)
2. [Créer la fiche sur Play Console](#2-créer-la-fiche-sur-play-console)
3. [Informations de l'application](#3-informations-de-lapplication)
4. [Captures d'écran et assets visuels](#4-captures-décran-et-assets-visuels)
5. [Configuration de l'application](#5-configuration-de-lapplication)
6. [Classification du contenu](#6-classification-du-contenu)
7. [Tarification et disponibilité](#7-tarification-et-disponibilité)
8. [Soumission pour review](#8-soumission-pour-review)

---

## 1. PRÉPARER L'APPLICATION

### Étape 1.1 : Build de production (APK/AAB)

**Nous allons créer un fichier AAB (Android App Bundle) - format requis par Google.**

#### Configuration préalable :

1. **Package name** (identifiant unique de votre app)
   - Format : `com.votreorganisation.kwezi`
   - Exemple : `com.mahoraiseducation.kwezi`
   - ⚠️ **Important :** Une fois choisi, il ne peut plus être changé !

2. **Version de l'app**
   - Version code : 1 (numéro interne)
   - Version name : "1.0.0" (version visible par les utilisateurs)

3. **Nom de l'app**
   - "Kwezi - Shimaoré & Kibouchi"
   - Maximum 30 caractères

---

### Étape 1.2 : Créer le build

**Nous devons exécuter ces commandes :**

```bash
# 1. Configurer le package name dans app.json
# 2. Installer EAS CLI (Expo Application Services)
npm install -g eas-cli

# 3. Se connecter à Expo
eas login

# 4. Configurer EAS
eas build:configure

# 5. Créer le build Android production
eas build --platform android --profile production
```

⚠️ **IMPORTANT :** Avant d'exécuter ces commandes, vous aurez besoin de :
- Un compte Expo (gratuit)
- Configurer le keystore (clé de signature)

**Voulez-vous que je vous aide à créer ce build maintenant ?**

---

## 2. CRÉER LA FICHE SUR PLAY CONSOLE

### Étape 2.1 : Accéder à Play Console

1. Allez sur [Google Play Console](https://play.google.com/console)
2. Cliquez sur **"Créer une application"**
3. Remplissez les informations de base :

**Informations de base :**
```
Nom de l'application : Kwezi - Shimaoré & Kibouchi
Langue par défaut : Français (France)
Type d'application : Application
Gratuite ou payante : Gratuite (avec achats intégrés)
```

4. Acceptez les conditions :
   - ✅ Déclarations relatives au contenu de l'application
   - ✅ Lois américaines sur le contrôle des exportations

5. Cliquez sur **"Créer l'application"**

---

## 3. INFORMATIONS DE L'APPLICATION

### Étape 3.1 : Fiche du Store (Description)

**Allez dans : "Présence sur le Store" → "Fiche du Store principale"**

#### Titre de l'application (30 caractères max)
```
Kwezi - Shimaoré & Kibouchi
```

#### Description courte (80 caractères max)
```
Apprends le shimaoré et le kibouchi, les langues authentiques de Mayotte 🇾🇹
```

#### Description complète (4000 caractères max)
```
🏝️ Kwezi - Apprends le Shimaoré et le Kibouchi

Découvre les langues authentiques de Mayotte avec Kwezi, l'application éducative conçue pour préserver et promouvoir le shimaoré et le kibouchi.

✨ FONCTIONNALITÉS PRINCIPALES

📚 636+ Mots Authentiques
• 16 catégories : animaux, famille, nourriture, traditions, nature, et plus
• Traductions complètes en shimaoré et kibouchi
• Vocabulaire vérifié par des locuteurs natifs

🔊 Plus de 1280 Audio Authentiques
• Enregistrements réalisés par des locuteurs natifs
• Prononciation correcte garantie
• Audio de qualité professionnelle

🎮 4 Jeux d'Apprentissage
• Quiz Vocabulaire : teste tes connaissances
• Construire des Phrases : apprends la grammaire
• Quiz Mayotte : découvre la culture mahoraise
• Conjugaison : maîtrise les verbes

🏝️ Culture Mahoraise
• Découvre les villages de Mayotte
• Apprends les traditions authentiques
• Explore l'histoire de l'île

📚 Fiches d'Exercices
• Télécharge des fiches PDF pour pratiquer
• Exercices adaptés à tous les niveaux
• Contenu pédagogique de qualité

💎 GRATUIT & PREMIUM

Version Gratuite :
• 250 mots de vocabulaire
• Accès aux jeux éducatifs
• Audio authentique
• Quiz Mayotte

Version Premium (2,90€/mois) :
• Accès complet à 636+ mots
• Toutes les catégories débloquées
• Fiches d'exercices PDF
• Support prioritaire

🎯 POUR QUI ?

✅ Mahorais souhaitant renouer avec leurs racines
✅ Parents voulant transmettre la langue à leurs enfants
✅ Étudiants apprenant le shimaoré ou kibouchi
✅ Curieux de découvrir la culture de Mayotte
✅ Tous les âges (recommandé 7+)

🌟 POURQUOI KWEZI ?

Notre mission est de préserver les langues de Mayotte et de les rendre accessibles à tous. Chaque mot, chaque audio, chaque jeu a été conçu avec soin pour offrir une expérience d'apprentissage authentique et immersive.

📱 COMMENCE TON AVENTURE

Télécharge Kwezi maintenant et rejoins des centaines d'apprenants qui découvrent les richesses linguistiques de Mayotte !

---

⚠️ Note aux parents : Cette application est conçue pour un usage éducatif. Nous recommandons la supervision parentale pour les enfants de moins de 13 ans.

🇾🇹 Fait avec ❤️ pour Mayotte
```

---

## 4. CAPTURES D'ÉCRAN ET ASSETS VISUELS

### Étape 4.1 : Captures d'écran requises

**Google exige au minimum :**

#### 📱 Téléphone (OBLIGATOIRE)
- **Minimum :** 2 captures d'écran
- **Maximum :** 8 captures d'écran
- **Dimensions :** 
  - Largeur : 1080px
  - Hauteur : 1920px (portrait) ou 1080px (paysage)
- **Format :** PNG ou JPEG

**Captures à prendre :**
1. Écran d'accueil (catégories de vocabulaire)
2. Page d'apprentissage (mot avec audio)
3. Jeu "Construire des phrases"
4. Quiz Mayotte
5. Écran Premium (optionnel)

#### 📱 Tablette 7 pouces (OPTIONNEL)
- Dimensions : 1024 x 600

#### 📱 Tablette 10 pouces (OPTIONNEL)
- Dimensions : 1920 x 1200

---

### Étape 4.2 : Icône de l'application

**OBLIGATOIRE**

- **Dimensions :** 512 x 512 pixels
- **Format :** PNG (32 bits)
- **Pas de transparence**
- **Contenu :** Logo Kwezi ou 🏝️

---

### Étape 4.3 : Bannière (Feature Graphic)

**OBLIGATOIRE**

- **Dimensions :** 1024 x 500 pixels
- **Format :** PNG ou JPEG
- **Contenu suggéré :**
  - Logo Kwezi au centre
  - Texte : "Apprends le Shimaoré et le Kibouchi"
  - Drapeau de Mayotte 🇾🇹
  - Couleurs : violet/bleu (comme la landing page)

---

### 🎨 CRÉATION DES ASSETS

**Option A : Je peux vous aider à créer des templates**
- Je peux générer des fichiers HTML/CSS pour créer les visuels
- Vous les prenez en capture d'écran

**Option B : Outils en ligne gratuits**
- Canva : https://www.canva.com
- Figma : https://www.figma.com
- Snappa : https://snappa.com

**Option C : Prendre des screenshots depuis l'app**
- Utilisez l'émulateur Android ou votre téléphone
- Prenez des captures d'écran de l'app
- Redimensionnez avec https://www.iloveimg.com/resize-image

---

## 5. CONFIGURATION DE L'APPLICATION

### Étape 5.1 : Informations de contact

**Allez dans : "Croissance" → "Coordonnées"**

```
E-mail : votre-email@exemple.com
Site Web : https://kwezi-app.netlify.app (ou votre URL)
Téléphone : +262 XXX XXX XXX (optionnel)
```

---

### Étape 5.2 : Politique de confidentialité

**OBLIGATOIRE**

**URL :** `https://kwezi-edu.preview.emergentagent.com/privacy-policy`

(Ou votre URL Netlify une fois déployée)

---

### Étape 5.3 : Catégorie de l'application

**Allez dans : "Présence sur le Store" → "Catégorie du Store"**

```
Catégorie : Éducation
Tags : 
  - Apprentissage des langues
  - Langues locales
  - Éducation culturelle
```

---

## 6. CLASSIFICATION DU CONTENU

### Étape 6.1 : Questionnaire de classification

**Allez dans : "Stratégie" → "Classification du contenu"**

**Répondez au questionnaire :**

1. **Votre application contient-elle de la violence ?**
   - ❌ Non

2. **Contenu sexuel ou nudité ?**
   - ❌ Non

3. **Langage injurieux ?**
   - ❌ Non

4. **Drogues, alcool, tabac ?**
   - ❌ Non

5. **Contenu effrayant ?**
   - ❌ Non

6. **Jeux d'argent ?**
   - ❌ Non

7. **Partage de localisation ?**
   - ❌ Non

8. **Achats intégrés ?**
   - ✅ Oui (abonnement Premium 2,90€/mois)

**Âge recommandé :** 7+ (Éducatif, adapté aux enfants avec supervision)

---

## 7. TARIFICATION ET DISPONIBILITÉ

### Étape 7.1 : Tarification

**Allez dans : "Stratégie" → "Tarification et disponibilité"**

```
Type : Gratuite
Contient des achats intégrés : Oui
  - Premium mensuel : 2,90€
```

---

### Étape 7.2 : Pays de distribution

**Sélectionnez les pays :**

**Recommandé pour Kwezi :**
- ✅ France (y compris Mayotte)
- ✅ Comores
- ✅ Madagascar
- ✅ Maurice
- ✅ Réunion
- ✅ Autres pays francophones (optionnel)

**Ou sélectionnez "Tous les pays" si vous voulez une portée mondiale.**

---

## 8. SOUMISSION POUR REVIEW

### Étape 8.1 : Vérifier la checklist

Avant de soumettre, vérifiez que vous avez complété :

#### Configuration du Store
- ✅ Titre de l'application
- ✅ Description courte
- ✅ Description complète
- ✅ Captures d'écran (min 2)
- ✅ Icône 512x512
- ✅ Bannière 1024x500
- ✅ Catégorie de l'app
- ✅ E-mail de contact
- ✅ URL politique de confidentialité

#### Configuration technique
- ✅ Fichier AAB uploadé
- ✅ Package name configuré
- ✅ Version code et name

#### Classification
- ✅ Questionnaire de contenu complété
- ✅ Âge recommandé défini

#### Tarification
- ✅ Type (gratuit) défini
- ✅ Achats intégrés déclarés
- ✅ Pays de distribution sélectionnés

---

### Étape 8.2 : Soumettre pour review

1. Allez dans **"Publication" → "Aperçu de la version"**
2. Vérifiez toutes les sections (tout doit être vert ✅)
3. Cliquez sur **"Envoyer pour examen"**

**Délai de review :**
- ⏱️ En général : 1-3 jours
- ⏱️ Première soumission : jusqu'à 7 jours

**Google vous enverra un email à chaque étape :**
- 📧 Review en cours
- 📧 Approuvé (publication automatique)
- 📧 Rejeté (avec raisons et corrections à apporter)

---

## 🎯 RÉSUMÉ DES ÉTAPES

1. ✅ **Compte développeur créé** (FAIT)
2. ⏳ **Créer le build AAB** (À FAIRE)
3. ⏳ **Créer la fiche sur Play Console** (À FAIRE)
4. ⏳ **Remplir les informations** (À FAIRE)
5. ⏳ **Créer les captures d'écran** (À FAIRE)
6. ⏳ **Uploader le AAB** (À FAIRE)
7. ⏳ **Classification du contenu** (À FAIRE)
8. ⏳ **Soumettre pour review** (À FAIRE)
9. ⏳ **Attendre l'approbation** (1-7 jours)
10. 🎉 **Publication !**

---

## ⚠️ POINTS IMPORTANTS

### 1. Package Name
**Choisissez bien votre package name maintenant !**

Format : `com.votreorganisation.kwezi`

Suggestions :
- `com.mahoraiseducation.kwezi`
- `com.kwezi.app`
- `com.mayotte.kwezi`

**Une fois publié, vous ne pourrez PLUS le changer.**

### 2. Keystore (Clé de signature)
Google générera automatiquement une clé de signature pour vous.

⚠️ **NE PERDEZ JAMAIS CETTE CLÉ !** Sinon vous ne pourrez plus mettre à jour votre app.

### 3. Politique de confidentialité
**Obligatoire depuis 2022.**

Vous avez déjà ce document :
- URL actuelle : `https://kwezi-edu.preview.emergentagent.com/privacy-policy`
- URL future : `https://kwezi-app.netlify.app/privacy-policy` (une fois déployée)

---

## 🆘 AIDE SUPPLÉMENTAIRE

### Besoin d'aide pour :

**1. Créer le build AAB ?**
- Je peux vous guider étape par étape
- Nous devons configurer EAS Build

**2. Créer les captures d'écran ?**
- Je peux générer des templates
- Ou vous guider pour les prendre depuis l'app

**3. Créer l'icône et la bannière ?**
- Je peux vous donner des templates HTML/CSS
- Ou des recommandations pour Canva

**4. Remplir la fiche Play Store ?**
- Tout le texte est fourni ci-dessus
- Copiez-collez directement

---

## 📞 CONTACT GOOGLE

En cas de problème pendant la review :
- Centre d'aide : https://support.google.com/googleplay/android-developer
- Forum communautaire : https://support.google.com/googleplay/android-developer/community

---

## 🎉 FÉLICITATIONS !

Vous êtes sur le point de publier Kwezi sur le Play Store !

**Prochaine étape immédiate :** Créer le build de production (fichier AAB)

**Voulez-vous que je vous aide à créer le build maintenant ?**

---

**Document créé le :** 15 octobre 2025  
**Pour :** Application Kwezi  
**Statut :** Prêt pour publication
