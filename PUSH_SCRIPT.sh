#!/bin/bash

# Script pour pousser les modifications Kwezi sur GitHub
# Exécutez ce script depuis votre machine locale

echo "🚀 Script de push Kwezi vers GitHub"
echo "=================================="
echo ""

# Vérifier si on est dans le bon dépôt
if [ ! -d ".git" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du dépôt Git"
    exit 1
fi

# Vérifier le remote
REMOTE=$(git remote get-url origin 2>/dev/null)
if [[ "$REMOTE" != *"kwezi-app"* ]]; then
    echo "⚠️  Remote actuel: $REMOTE"
    echo "📝 Configuration du remote kwezi-app..."
    git remote set-url origin https://github.com/ambdillah/kwezi-app.git
fi

echo "✅ Remote configuré: https://github.com/ambdillah/kwezi-app.git"
echo ""

# Récupérer les dernières modifications
echo "📥 Récupération des dernières modifications..."
git fetch origin main

# Vérifier s'il y a des fichiers à pousser
if git diff --quiet origin/main; then
    echo "✅ Tout est à jour!"
    echo "🎉 Les modifications sont déjà sur GitHub"
else
    echo "📤 Push des modifications vers GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ PUSH RÉUSSI!"
        echo "🚀 Le build APK va démarrer automatiquement sur GitHub Actions"
        echo "📍 Suivez le build ici: https://github.com/ambdillah/kwezi-app/actions"
    else
        echo ""
        echo "❌ Erreur lors du push"
        echo "Vérifiez vos identifiants GitHub"
    fi
fi

echo ""
echo "📋 Prochaines étapes:"
echo "1. Allez sur: https://github.com/ambdillah/kwezi-app/actions"
echo "2. Vérifiez que le workflow 'Build Android APK' est lancé"
echo "3. Attendez ~15-20 minutes"
echo "4. Téléchargez l'APK dans Artifacts"
echo ""
echo "🔐 N'oubliez pas de configurer le secret EXPO_TOKEN sur GitHub!"
