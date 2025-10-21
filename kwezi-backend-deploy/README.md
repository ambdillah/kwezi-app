# Kwezi Backend API

Application backend pour Kwezi - Application d'apprentissage des langues Shimaoré et Kibouchi de Mayotte.

## Technologies

- **Framework**: FastAPI (Python)
- **Base de données**: MongoDB Atlas
- **Paiements**: Stripe
- **Déploiement**: Render.com

## Variables d'Environnement Requises

```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/mayotte_app?retryWrites=true&w=majority
DB_NAME=mayotte_app
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Installation Locale

```bash
pip install -r requirements.txt
python server.py
```

## Déploiement sur Render.com

1. Créez un nouveau Web Service
2. Connectez ce dépôt GitHub
3. Configurez les variables d'environnement
4. Déployez !

## API Endpoints

- `GET /api/words` - Liste des mots
- `GET /api/sentences` - Phrases pour les jeux
- `GET /api/categories` - Catégories disponibles
- `POST /api/users/register` - Inscription utilisateur
- Et bien plus...

## Base de Données

- **635 mots** en Shimaoré et Kibouchi
- **270 phrases** pour le jeu "Construire des phrases"
- **10 exercices** pédagogiques

## Auteur

Développé pour l'apprentissage des langues authentiques de Mayotte 🇾🇹
