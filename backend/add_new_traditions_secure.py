#!/usr/bin/env python3
"""
Script sécurisé pour ajouter 8 nouvelles traditions à la section tradition
avec leurs fichiers audio authentiques
"""

from pymongo import MongoClient
import os
import shutil
from datetime import datetime

# Connexion MongoDB
mongo_url = "mongodb://localhost:27017/"
client = MongoClient(mongo_url)
db = client['mayotte_app']
words_collection = db['words']

# Répertoires des audios
AUDIO_SOURCE_DIR = "/tmp"
AUDIO_DEST_DIR = "/app/frontend/assets/audio/tradition"

# Nouvelles traditions avec données exactes et correspondances audio
NEW_TRADITIONS = [
    {
        'french': 'Dieu',
        'shimaore': 'moungou',
        'kibouchi': 'dragnahari',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🙏',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Moungou.m4a',
        'audio_filename_kibouchi': 'Dragnahari.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Faire la prière',
        'shimaore': 'ousoili',
        'kibouchi': 'mikousoili',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🕌',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Ousoili.m4a',
        'audio_filename_kibouchi': 'Mikousoili.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Tambour',
        'shimaore': 'ngoma',
        'kibouchi': 'azoulahi',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🥁',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Ngoma.m4a',
        'audio_filename_kibouchi': 'Azoulahi.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Tambourin',
        'shimaore': 'tari',
        'kibouchi': 'tari',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '🪘',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Tari s.m4a',
        'audio_filename_kibouchi': 'Tari k.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Ballon',
        'shimaore': 'boulou',
        'kibouchi': 'boulou',
        'category': 'tradition',
        'difficulty': 1,
        'image_url': '⚽',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Boulou.m4a',
        'audio_filename_kibouchi': 'Boulou.m4a',  # Même fichier
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Ligne de pêche',
        'shimaore': 'missi',
        'kibouchi': 'mouchipi',
        'category': 'tradition',
        'difficulty': 2,
        'image_url': '🎣',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Missi.m4a',
        'audio_filename_kibouchi': 'Mouchipi.m4a',
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Filet de pêche',
        'shimaore': 'wavou/chamiya',
        'kibouchi': 'wavou/chamiya',
        'category': 'tradition',
        'difficulty': 2,
        'image_url': '🪝',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Wavou_chamiya.m4a',
        'audio_filename_kibouchi': 'Wavou_chamiya.m4a',  # Même fichier
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    },
    {
        'french': 'Voile de pêche',
        'shimaore': 'djarifa',
        'kibouchi': 'djarifa',
        'category': 'tradition',
        'difficulty': 2,
        'image_url': '⛵',
        'dual_audio_system': True,
        'audio_filename_shimaore': 'Djarifa.m4a',
        'audio_filename_kibouchi': 'Djarifa.m4a',  # Même fichier
        'shimoare_has_audio': True,
        'kibouchi_has_audio': True,
        'audio_source': 'Authentic recording - User provided',
        'audio_updated_at': datetime.utcnow()
    }
]

# Fichiers audio à copier (unique) - 13 fichiers
AUDIO_FILES = [
    'Moungou.m4a',
    'Dragnahari.m4a',
    'Ousoili.m4a',
    'Mikousoili.m4a',
    'Ngoma.m4a',
    'Azoulahi.m4a',
    'Tari s.m4a',
    'Tari k.m4a',
    'Boulou.m4a',
    'Missi.m4a',
    'Mouchipi.m4a',
    'Wavou_chamiya.m4a',
    'Djarifa.m4a'
]

def main():
    print("=" * 80)
    print("