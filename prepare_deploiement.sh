#!/bin/bash

# Script pour télécharger tous les fichiers nécessaires au déploiement

echo "📦 Préparation des fichiers de déploiement Kwezi..."

# Créer un dossier de déploiement
mkdir -p /app/deploiement_kwezi
cd /app/deploiement_kwezi

echo "✅ Copie de la base de données exportée..."
cp /app/backend/db_export.json ./

echo "✅ Copie du backup MongoDB..."
cp -r /app/backend/db_backup ./

echo "✅ Copie des guides..."
cp /app/GUIDE_DEPLOIEMENT_COMPLET.md ./
cp /app/GUIDE_IMPORT_MONGODB.md ./
cp /app/GUIDE_RENDER_DEPLOIEMENT.md ./
cp /app/DEPLOIEMENT_RECAP.md ./

echo "✅ Copie de la configuration Render..."
cp /app/backend/render.yaml ./

echo "✅ Copie du backend pour référence..."
mkdir -p backend
cp /app/backend/server.py ./backend/
cp /app/backend/requirements.txt ./backend/
cp /app/backend/.env ./backend/.env.example

echo "✅ Création d'une archive..."
cd /app
tar -czf deploiement_kwezi.tar.gz deploiement_kwezi/

echo ""
echo "🎉 Tous les fichiers sont prêts !"
echo ""
echo "📂 Fichiers disponibles dans : /app/deploiement_kwezi/"
echo "📦 Archive complète : /app/deploiement_kwezi.tar.gz"
echo ""
echo "📋 Contenu :"
echo "  - db_export.json (0.66 MB) - Base de données complète"
echo "  - db_backup/ - Backup MongoDB (BSON)"
echo "  - *.md - Guides de déploiement"
echo "  - render.yaml - Configuration Render.com"
echo "  - backend/ - Code source backend"
echo ""
echo "💾 Taille totale de l'archive :"
du -h /app/deploiement_kwezi.tar.gz
echo ""
echo "📥 Pour télécharger :"
echo "  1. Allez sur https://langapp-debug.preview.emergentagent.com/"
echo "  2. Ouvrez la console développeur (F12)"
echo "  3. Entrez cette commande :"
echo "     fetch('/app/deploiement_kwezi.tar.gz').then(r => r.blob()).then(b => {"
echo "       const a = document.createElement('a');"
echo "       a.href = URL.createObjectURL(b);"
echo "       a.download = 'kwezi-deploiement.tar.gz';"
echo "       a.click();"
echo "     });"
echo ""
