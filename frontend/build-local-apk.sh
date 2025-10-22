#!/bin/bash

echo "🚀 KWEZI - Build APK Local Script"
echo "=================================="
echo ""
echo "Ce script va créer un APK Android en local sans utiliser EAS Build"
echo ""

# Vérifier si Android SDK est installé
if [ -z "$ANDROID_HOME" ]; then
    echo "❌ ERREUR: Android SDK n'est pas installé ou ANDROID_HOME n'est pas défini"
    echo ""
    echo "📋 INSTRUCTIONS D'INSTALLATION:"
    echo "1. Télécharger Android Studio depuis: https://developer.android.com/studio"
    echo "2. Installer Android Studio"
    echo "3. Ouvrir Android Studio > Tools > SDK Manager"
    echo "4. Installer Android SDK Platform 33 (minimum)"
    echo "5. Ajouter ANDROID_HOME à votre PATH:"
    echo "   export ANDROID_HOME=$HOME/Android/Sdk"
    echo "   export PATH=$PATH:$ANDROID_HOME/emulator"
    echo "   export PATH=$PATH:$ANDROID_HOME/platform-tools"
    echo ""
    exit 1
fi

echo "✅ Android SDK trouvé: $ANDROID_HOME"
echo ""

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
yarn install

# Créer le build
echo ""
echo "🔨 Création du build APK..."
echo "Ceci peut prendre 10-15 minutes la première fois..."
echo ""

npx expo run:android --variant release

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 BUILD RÉUSSI!"
    echo ""
    echo "📱 L'APK se trouve dans:"
    echo "   android/app/build/outputs/apk/release/app-release.apk"
    echo ""
    echo "Pour installer sur votre appareil:"
    echo "   adb install android/app/build/outputs/apk/release/app-release.apk"
    echo ""
else
    echo ""
    echo "❌ Le build a échoué. Vérifiez les logs ci-dessus."
    echo ""
fi
