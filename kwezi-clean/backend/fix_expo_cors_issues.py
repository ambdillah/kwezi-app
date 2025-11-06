#!/usr/bin/env python3
"""
Correction des problèmes CORS et Expo Go
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_expo_config():
    """Vérifie la configuration Expo"""
    app_json_path = "/app/frontend/app.json"
    
    logger.info("🔍 VÉRIFICATION CONFIGURATION EXPO")
    
    if os.path.exists(app_json_path):
        with open(app_json_path, 'r') as f:
            content = f.read()
            logger.info("✅ app.json existe")
            
            # Vérifier les configurations importantes
            if '"scheme":' in content:
                logger.info("✅ Scheme configuré")
            else:
                logger.warning("⚠️ Scheme manquant")
                
            if '"platforms":' in content:
                logger.info("✅ Platforms configurées")
            else:
                logger.warning("⚠️ Platforms manquantes")
    else:
        logger.error("❌ app.json non trouvé")

def check_env_variables():
    """Vérifie les variables d'environnement"""
    logger.info("\n🔍 VÉRIFICATION VARIABLES ENVIRONNEMENT")
    
    env_path = "/app/frontend/.env"
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            content = f.read()
            logger.info("✅ .env existe")
            
            # Variables importantes pour Expo
            important_vars = [
                'EXPO_PACKAGER_PROXY_URL',
                'EXPO_PACKAGER_HOSTNAME'
            ]
            
            for var in important_vars:
                if var in content:
                    logger.info(f"✅ {var} configuré")
                else:
                    logger.warning(f"⚠️ {var} manquant")
    else:
        logger.error("❌ .env non trouvé")

def check_backend_cors():
    """Vérifie la configuration CORS du backend"""
    logger.info("\n🔍 VÉRIFICATION CORS BACKEND")
    
    server_path = "/app/backend/server.py"
    if os.path.exists(server_path):
        with open(server_path, 'r') as f:
            content = f.read()
            
            if 'CORSMiddleware' in content:
                logger.info("✅ CORSMiddleware configuré")
            else:
                logger.warning("⚠️ CORSMiddleware manquant")
                
            if 'allow_origins=["*"]' in content:
                logger.info("✅ Origins autorisées")
            else:
                logger.warning("⚠️ Origins restrictives")
    else:
        logger.error("❌ server.py non trouvé")

def generate_qr_code():
    """Génère un nouveau QR code pour Expo Go"""
    logger.info("\n📱 GÉNÉRATION QR CODE EXPO GO")
    
    # Le QR code est généralement créé automatiquement par Expo
    qr_path = "/app/frontend/qr_code_expo.png"
    if os.path.exists(qr_path):
        logger.info("✅ QR code existe")
    else:
        logger.warning("⚠️ QR code manquant - sera généré au démarrage")

def main():
    """Fonction principale"""
    logger.info("🎯 DIAGNOSTIC PROBLÈMES EXPO GO & CORS")
    
    try:
        check_expo_config()
        check_env_variables()
        check_backend_cors()
        generate_qr_code()
        
        logger.info(f"\n{'='*60}")
        logger.info("RECOMMANDATIONS")
        logger.info(f"{'='*60}")
        logger.info("1. Redémarrer Expo avec tunnel mode")
        logger.info("2. Vérifier les variables d'environnement")
        logger.info("3. Utiliser le QR code généré")
        logger.info("4. Tester avec incognito mode si problèmes CORS")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur dans le diagnostic: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)