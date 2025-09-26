#!/usr/bin/env python3
"""
Script auto-généré pour appliquer 771 correspondances audio
basé sur l'analyse case-insensitive de la structure réelle de la base
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_database():
    mongo_url = os.getenv('MONGO_URL')
    client = MongoClient(mongo_url)
    return client['shimaoré_app']

def apply_audio_correspondences():
    db = connect_to_database()
    collection = db['vocabulary']
    
    # Correspondances trouvées automatiquement
    correspondences = [
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille_backup_20250925_073453/Zoki lalahi.m4a',
            'audio_filename': 'Zoki lalahi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/famille_backup_20250925_073453/Mama titi-bolé.m4a',
            'audio_filename': 'Mama titi-bolé.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille_backup_20250925_073453/Coco.m4a',
            'audio_filename': 'Coco.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille_backup_20250925_073453/Mama.m4a',
            'audio_filename': 'Mama.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c22'),
            'french': 'famille',
            'audio_path': 'audio/famille_backup_20250925_073453/Havagna.m4a',
            'audio_filename': 'Havagna.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille_backup_20250925_073453/Zouki.m4a',
            'audio_filename': 'Zouki.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/famille_backup_20250925_073453/Baba héli-bé.m4a',
            'audio_filename': 'Baba héli-bé.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c30'),
            'french': 'tante paternelle',
            'audio_path': 'audio/famille_backup_20250925_073453/Zena.m4a',
            'audio_filename': 'Zena.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c29'),
            'french': 'petit frère',
            'audio_path': 'audio/famille_backup_20250925_073453/Moina.m4a',
            'audio_filename': 'Moina.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250925_073453/Baba s.m4a',
            'audio_filename': 'Baba s.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille_backup_20250925_073453/Zoki viavi.m4a',
            'audio_filename': 'Zoki viavi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/famille_backup_20250925_073453/Baba titi-bolé.m4a',
            'audio_filename': 'Baba titi-bolé.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250925_073453/Zouki mtroubaba.m4a',
            'audio_filename': 'Zouki mtroubaba.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250925_073453/Baba k.m4a',
            'audio_filename': 'Baba k.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille_backup_20250925_073453/Dadayi.m4a',
            'audio_filename': 'Dadayi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250925_073453/Moinagna mtroubaba.m4a',
            'audio_filename': 'Moinagna mtroubaba.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2d'),
            'french': 'oncle maternel',
            'audio_path': 'audio/famille_backup_20250925_073453/Zama.m4a',
            'audio_filename': 'Zama.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille_backup_20250925_073453/Lalahi.m4a',
            'audio_filename': 'Lalahi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250925_073453/Mtroubaba.m4a',
            'audio_filename': 'Mtroubaba.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3a'),
            'french': 'ami',
            'audio_path': 'audio/famille_backup_20250925_073453/Mwandzani.m4a',
            'audio_filename': 'Mwandzani.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c26'),
            'french': 'sœur',
            'audio_path': 'audio/famille_backup_20250925_073453/Anabavi.m4a',
            'audio_filename': 'Anabavi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2c'),
            'french': 'grand-mère',
            'audio_path': 'audio/famille_backup_20250925_073453/Dadi.m4a',
            'audio_filename': 'Dadi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/famille_backup_20250925_073453/Ninfndri héli-bé.m4a',
            'audio_filename': 'Ninfndri héli-bé.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille_backup_20250925_073453/Bacoco.m4a',
            'audio_filename': 'Bacoco.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c22'),
            'french': 'famille',
            'audio_path': 'audio/famille_backup_20250925_073453/Mdjamaza.m4a',
            'audio_filename': 'Mdjamaza.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c31'),
            'french': 'garçon',
            'audio_path': 'audio/famille_backup_20250925_073453/Tseki lalahi.m4a',
            'audio_filename': 'Tseki lalahi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille_backup_20250925_073453/Mtroumama.m4a',
            'audio_filename': 'Mtroumama.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille_backup_20250925_073453/Zouki mtroumché.m4a',
            'audio_filename': 'Zouki mtroumché.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille_backup_20250925_073453/Moinagna mtroumama.m4a',
            'audio_filename': 'Moinagna mtroumama.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c25'),
            'french': 'frère',
            'audio_path': 'audio/famille_backup_20250925_073453/Anadahi.m4a',
            'audio_filename': 'Anadahi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille_backup_20250925_073453/Viavi.m4a',
            'audio_filename': 'Viavi.m4a',
            'category': 'famille_backup_20250925_073453',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/verbes/Mamadiki.m4a',
            'audio_filename': 'Mamadiki.m4a',
            'category': 'verbes',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ca5'),
            'french': 'croire',
            'audio_path': 'audio/verbes/Koimini.m4a',
            'audio_filename': 'Koimini.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/verbes/Mamafa.m4a',
            'audio_filename': 'Mamafa.m4a',
            'category': 'verbes',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79caa'),
            'french': 'laisser',
            'audio_path': 'audio/verbes/Mangnambéla.m4a',
            'audio_filename': 'Mangnambéla.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb3'),
            'french': 'cent',
            'audio_path': 'audio/verbes/Magnamiya.m4a',
            'audio_filename': 'Magnamiya.m4a',
            'category': 'verbes',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c96'),
            'french': 'dire',
            'audio_path': 'audio/verbes/Mangnabara.m4a',
            'audio_filename': 'Mangnabara.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cc0'),
            'french': 'se rappeler',
            'audio_path': 'audio/verbes/Koufahamou.m4a',
            'audio_filename': 'Koufahamou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cbd'),
            'french': 'sembler',
            'audio_path': 'audio/verbes/Mampihiragna.m4a',
            'audio_filename': 'Mampihiragna.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/verbes/Mamangou.m4a',
            'audio_filename': 'Mamangou.m4a',
            'category': 'verbes',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4a'),
            'french': 'mangue',
            'audio_path': 'audio/verbes/Mangala.m4a',
            'audio_filename': 'Mangala.m4a',
            'category': 'verbes',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cb1'),
            'french': 'comprendre',
            'audio_path': 'audio/verbes/Kouéléwa.m4a',
            'audio_filename': 'Kouéléwa.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cd5'),
            'french': 'cuisiner',
            'audio_path': 'audio/verbes/Mahandrou.m4a',
            'audio_filename': 'Mahandrou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cdc'),
            'french': 'tuer',
            'audio_path': 'audio/verbes/Ouwoula.m4a',
            'audio_filename': 'Ouwoula.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cd6'),
            'french': 'ranger',
            'audio_path': 'audio/verbes/Magnadzari.m4a',
            'audio_filename': 'Magnadzari.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388883'),
            'french': 'ancien',
            'audio_path': 'audio/verbes/Mahaléou.m4a',
            'audio_filename': 'Mahaléou.m4a',
            'category': 'verbes',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cc8'),
            'french': 'vendre',
            'audio_path': 'audio/verbes/Mandafou.m4a',
            'audio_filename': 'Mandafou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c9a'),
            'french': 'voir',
            'audio_path': 'audio/verbes/Mahita.m4a',
            'audio_filename': 'Mahita.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4a'),
            'french': 'mangue',
            'audio_path': 'audio/verbes/Mangalatra.m4a',
            'audio_filename': 'Mangalatra.m4a',
            'category': 'verbes',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cb2'),
            'french': 'marcher',
            'audio_path': 'audio/verbes/Mandéha.m4a',
            'audio_filename': 'Mandéha.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c76'),
            'french': 'cuillère',
            'audio_path': 'audio/verbes/Magnossoutrou.m4a',
            'audio_filename': 'Magnossoutrou.m4a',
            'category': 'verbes',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/verbes/Mamana.m4a',
            'audio_filename': 'Mamana.m4a',
            'category': 'verbes',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c9d'),
            'french': 'approcher',
            'audio_path': 'audio/verbes/Magnatougnou.m4a',
            'audio_filename': 'Magnatougnou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cb8'),
            'french': 'attendre',
            'audio_path': 'audio/verbes/Mandigni.m4a',
            'audio_filename': 'Mandigni.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cda'),
            'french': 'apporter',
            'audio_path': 'audio/verbes/Mandèyi.m4a',
            'audio_filename': 'Mandèyi.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ccc'),
            'french': 'piler',
            'audio_path': 'audio/verbes/Mandissa.m4a',
            'audio_filename': 'Mandissa.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ca3'),
            'french': 'trouver',
            'audio_path': 'audio/verbes/Mahazou.m4a',
            'audio_filename': 'Mahazou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c72'),
            'french': 'lit',
            'audio_path': 'audio/verbes/Mandzari koubani.m4a',
            'audio_filename': 'Mandzari koubani.m4a',
            'category': 'verbes',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/verbes/Mamani.m4a',
            'audio_filename': 'Mamani.m4a',
            'category': 'verbes',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cd9'),
            'french': 'essuyer',
            'audio_path': 'audio/verbes/Mamitri.m4a',
            'audio_filename': 'Mamitri.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8b'),
            'french': 'sol',
            'audio_path': 'audio/verbes/Magnoutani.m4a',
            'audio_filename': 'Magnoutani.m4a',
            'category': 'verbes',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c86'),
            'french': 'toiture',
            'audio_path': 'audio/verbes/Manapaka somboutrou.m4a',
            'audio_filename': 'Manapaka somboutrou.m4a',
            'category': 'verbes',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/verbes/Mamaki azoumati.m4a',
            'audio_filename': 'Mamaki azoumati.m4a',
            'category': 'verbes',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cd0'),
            'french': 'couper',
            'audio_path': 'audio/verbes/Manapaka.m4a',
            'audio_filename': 'Manapaka.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cde'),
            'french': 'cueillir',
            'audio_path': 'audio/verbes/Mampoka.m4a',
            'audio_filename': 'Mampoka.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c9c'),
            'french': 'venir',
            'audio_path': 'audio/verbes/Havi.m4a',
            'audio_filename': 'Havi.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c98'),
            'french': 'vouloir',
            'audio_path': 'audio/verbes/Chokou.m4a',
            'audio_filename': 'Chokou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cbf'),
            'french': 'casser',
            'audio_path': 'audio/verbes/Latsaka.m4a',
            'audio_filename': 'Latsaka.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cdb'),
            'french': 'éteindre',
            'audio_path': 'audio/verbes/Mamounou.m4a',
            'audio_filename': 'Mamounou.m4a',
            'category': 'verbes',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c42'),
            'french': 'marron',
            'audio_path': 'audio/couleurs/Fotafotaka.m4a',
            'audio_filename': 'Fotafotaka.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c41'),
            'french': 'gris',
            'audio_path': 'audio/couleurs/Djifou.m4a',
            'audio_filename': 'Djifou.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c41'),
            'french': 'gris',
            'audio_path': 'audio/couleurs/Dzofou.m4a',
            'audio_filename': 'Dzofou.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388881'),
            'french': 'sale',
            'audio_path': 'audio/couleurs/Trotro.m4a',
            'audio_filename': 'Trotro.m4a',
            'category': 'couleurs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3b'),
            'french': 'bleu',
            'audio_path': 'audio/couleurs/Mayitsou.m4a',
            'audio_filename': 'Mayitsou.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3f'),
            'french': 'jaune',
            'audio_path': 'audio/couleurs/Tamoutamou.m4a',
            'audio_filename': 'Tamoutamou.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3e'),
            'french': 'blanc',
            'audio_path': 'audio/couleurs/Malandi.m4a',
            'audio_filename': 'Malandi.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3f'),
            'french': 'jaune',
            'audio_path': 'audio/couleurs/Dzindzano.m4a',
            'audio_filename': 'Dzindzano.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3b'),
            'french': 'bleu',
            'audio_path': 'audio/couleurs/Mayitsou bilé.m4a',
            'audio_filename': 'Mayitsou bilé.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c40'),
            'french': 'rouge',
            'audio_path': 'audio/couleurs/Mena.m4a',
            'audio_filename': 'Mena.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3d'),
            'french': 'noir',
            'audio_path': 'audio/couleurs/Mayintigni.m4a',
            'audio_filename': 'Mayintigni.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc2'),
            'french': 'mouche',
            'audio_path': 'audio/couleurs/Ndzidhou.m4a',
            'audio_filename': 'Ndzidhou.m4a',
            'category': 'couleurs',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3e'),
            'french': 'blanc',
            'audio_path': 'audio/couleurs/Ndjéou.m4a',
            'audio_filename': 'Ndjéou.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3b'),
            'french': 'bleu',
            'audio_path': 'audio/couleurs/Bilé.m4a',
            'audio_filename': 'Bilé.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3c'),
            'french': 'vert',
            'audio_path': 'audio/couleurs/Dhavou.m4a',
            'audio_filename': 'Dhavou.m4a',
            'category': 'couleurs',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c19'),
            'french': 'au revoir',
            'audio_path': 'audio/grammaire/Kwaheri.m4a',
            'audio_filename': 'Kwaheri.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c19'),
            'french': 'au revoir',
            'audio_path': 'audio/grammaire/Kwaheri(1).m4a',
            'audio_filename': 'Kwaheri(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388870'),
            'french': 'gentil',
            'audio_path': 'audio/grammaire/Tsara.m4a',
            'audio_filename': 'Tsara.m4a',
            'category': 'grammaire',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1f'),
            'french': 'bienvenue',
            'audio_path': 'audio/grammaire/Maeva.m4a',
            'audio_filename': 'Maeva.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c21'),
            'french': 'salut',
            'audio_path': 'audio/grammaire/Kwezi(1).m4a',
            'audio_filename': 'Kwezi(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887a'),
            'french': 'bon',
            'audio_path': 'audio/grammaire/Haligni tsara.m4a',
            'audio_filename': 'Haligni tsara.m4a',
            'category': 'grammaire',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1d'),
            'french': 'oui',
            'audio_path': 'audio/grammaire/Ewa.m4a',
            'audio_filename': 'Ewa.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c20'),
            'french': 'excusez-moi',
            'audio_path': 'audio/grammaire/Jéjé(1).m4a',
            'audio_filename': 'Jéjé(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c17'),
            'french': 'bonjour',
            'audio_path': 'audio/grammaire/Akori(1).m4a',
            'audio_filename': 'Akori(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1f'),
            'french': 'bienvenue',
            'audio_path': 'audio/grammaire/Maeva(1).m4a',
            'audio_filename': 'Maeva(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c21'),
            'french': 'salut',
            'audio_path': 'audio/grammaire/Kwezi.m4a',
            'audio_filename': 'Kwezi.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1a'),
            'french': 'comment ça va',
            'audio_path': 'audio/grammaire/Oukou wa hairi(1).m4a',
            'audio_filename': 'Oukou wa hairi(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c17'),
            'french': 'bonjour',
            'audio_path': 'audio/grammaire/Marahaba.m4a',
            'audio_filename': 'Marahaba.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c20'),
            'french': 'excusez-moi',
            'audio_path': 'audio/grammaire/Jéjé.m4a',
            'audio_filename': 'Jéjé.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c17'),
            'french': 'bonjour',
            'audio_path': 'audio/grammaire/Marahaba(1).m4a',
            'audio_filename': 'Marahaba(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887a'),
            'french': 'bon',
            'audio_path': 'audio/grammaire/Haligni tsara(1).m4a',
            'audio_filename': 'Haligni tsara(1).m4a',
            'category': 'grammaire',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1c'),
            'french': 'merci',
            'audio_path': 'audio/grammaire/Iya.m4a',
            'audio_filename': 'Iya.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1b'),
            'french': 'ça va bien',
            'audio_path': 'audio/grammaire/Fétré.m4a',
            'audio_filename': 'Fétré.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1b'),
            'french': 'ça va bien',
            'audio_path': 'audio/grammaire/Fétré(1).m4a',
            'audio_filename': 'Fétré(1).m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1a'),
            'french': 'comment ça va',
            'audio_path': 'audio/grammaire/Oukou wa hairi.m4a',
            'audio_filename': 'Oukou wa hairi.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c17'),
            'french': 'bonjour',
            'audio_path': 'audio/grammaire/Akori.m4a',
            'audio_filename': 'Akori.m4a',
            'category': 'grammaire',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887a'),
            'french': 'bon',
            'audio_path': 'audio/grammaire/Tsara(1).m4a',
            'audio_filename': 'Tsara(1).m4a',
            'category': 'grammaire',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7c'),
            'french': 'clôture',
            'audio_path': 'audio/maison/Vala k.m4a',
            'audio_filename': 'Vala k.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c70'),
            'french': 'porte',
            'audio_path': 'audio/maison/Mlango.m4a',
            'audio_filename': 'Mlango.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c70'),
            'french': 'porte',
            'audio_path': 'audio/maison/Varavaragna.m4a',
            'audio_filename': 'Varavaragna.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c88'),
            'french': 'lumière',
            'audio_path': 'audio/maison/Mwengué.m4a',
            'audio_filename': 'Mwengué.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8c'),
            'french': 'coupe-coupe',
            'audio_path': 'audio/maison/Chombo.m4a',
            'audio_filename': 'Chombo.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c74'),
            'french': 'vaisselle',
            'audio_path': 'audio/maison/Ziya.m4a',
            'audio_filename': 'Ziya.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c90'),
            'french': 'mortier',
            'audio_path': 'audio/maison/Chino.m4a',
            'audio_filename': 'Chino.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c82'),
            'french': 'oreiller',
            'audio_path': 'audio/maison/Mtsao.m4a',
            'audio_filename': 'Mtsao.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8e'),
            'french': 'sac',
            'audio_path': 'audio/maison/Gouni s.m4a',
            'audio_filename': 'Gouni s.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c84'),
            'french': 'mur',
            'audio_path': 'audio/maison/Péssi.m4a',
            'audio_filename': 'Péssi.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c73'),
            'french': 'marmite',
            'audio_path': 'audio/maison/Gnoungou.m4a',
            'audio_filename': 'Gnoungou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c77'),
            'french': 'fenêtre',
            'audio_path': 'audio/maison/Lafoumètara.m4a',
            'audio_filename': 'Lafoumètara.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8a'),
            'french': 'hache',
            'audio_path': 'audio/maison/Famaki.m4a',
            'audio_filename': 'Famaki.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c91'),
            'french': 'assiette',
            'audio_path': 'audio/maison/Sahani.m4a',
            'audio_filename': 'Sahani.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c86'),
            'french': 'toiture',
            'audio_path': 'audio/maison/Gandili-poutroumax.m4a',
            'audio_filename': 'Gandili-poutroumax.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c72'),
            'french': 'lit',
            'audio_path': 'audio/maison/Koubani.m4a',
            'audio_filename': 'Koubani.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c92'),
            'french': 'fondation',
            'audio_path': 'audio/maison/Houra.m4a',
            'audio_filename': 'Houra.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c86'),
            'french': 'toiture',
            'audio_path': 'audio/maison/Vovougnou.m4a',
            'audio_filename': 'Vovougnou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c75'),
            'french': 'bol',
            'audio_path': 'audio/maison/Chicombé.m4a',
            'audio_filename': 'Chicombé.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be9'),
            'french': 'dauphin',
            'audio_path': 'audio/maison/Soutrou.m4a',
            'audio_filename': 'Soutrou.m4a',
            'category': 'maison',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7a'),
            'french': 'miroir',
            'audio_path': 'audio/maison/Kitarafa.m4a',
            'audio_filename': 'Kitarafa.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c74'),
            'french': 'vaisselle',
            'audio_path': 'audio/maison/Hintagna.m4a',
            'audio_filename': 'Hintagna.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c76'),
            'french': 'cuillère',
            'audio_path': 'audio/maison/Sotrou.m4a',
            'audio_filename': 'Sotrou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c86'),
            'french': 'toiture',
            'audio_path': 'audio/maison/Gandilé-poutroumax.m4a',
            'audio_filename': 'Gandilé-poutroumax.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7a'),
            'french': 'miroir',
            'audio_path': 'audio/maison/Chido.m4a',
            'audio_filename': 'Chido.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c92'),
            'french': 'fondation',
            'audio_path': 'audio/maison/Koura.m4a',
            'audio_filename': 'Koura.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/maison/Chtrandra.m4a',
            'audio_filename': 'Chtrandra.m4a',
            'category': 'maison',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7b'),
            'french': 'cour',
            'audio_path': 'audio/maison/Mrabani.m4a',
            'audio_filename': 'Mrabani.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8b'),
            'french': 'machette',
            'audio_path': 'audio/maison/Ampanga.m4a',
            'audio_filename': 'Ampanga.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c90'),
            'french': 'mortier',
            'audio_path': 'audio/maison/Légnou.m4a',
            'audio_filename': 'Légnou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7b'),
            'french': 'cour',
            'audio_path': 'audio/maison/Mraba s.m4a',
            'audio_filename': 'Mraba s.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c89'),
            'french': 'torche',
            'audio_path': 'audio/maison/Pongi.m4a',
            'audio_filename': 'Pongi.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c79'),
            'french': 'table',
            'audio_path': 'audio/maison/Latabou.m4a',
            'audio_filename': 'Latabou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be9'),
            'french': 'dauphin',
            'audio_path': 'audio/maison/Outro.m4a',
            'audio_filename': 'Outro.m4a',
            'category': 'maison',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c75'),
            'french': 'bol',
            'audio_path': 'audio/maison/Bacouli.m4a',
            'audio_filename': 'Bacouli.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c89'),
            'french': 'torche',
            'audio_path': 'audio/maison/Pongé.m4a',
            'audio_filename': 'Pongé.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8d'),
            'french': 'cartable',
            'audio_path': 'audio/maison/Mkoba.m4a',
            'audio_filename': 'Mkoba.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c77'),
            'french': 'fenêtre',
            'audio_path': 'audio/maison/Fénétri.m4a',
            'audio_filename': 'Fénétri.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6f'),
            'french': 'maison',
            'audio_path': 'audio/maison/Nyoumba.m4a',
            'audio_filename': 'Nyoumba.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7c'),
            'french': 'clôture',
            'audio_path': 'audio/maison/Vala s.m4a',
            'audio_filename': 'Vala s.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c78'),
            'french': 'chaise',
            'audio_path': 'audio/maison/Chiri k.m4a',
            'audio_filename': 'Chiri k.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c78'),
            'french': 'chaise',
            'audio_path': 'audio/maison/Chiri s.m4a',
            'audio_filename': 'Chiri s.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c80'),
            'french': 'couteau',
            'audio_path': 'audio/maison/Méssou.m4a',
            'audio_filename': 'Méssou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7e'),
            'french': 'seau',
            'audio_path': 'audio/maison/Siyo.m4a',
            'audio_filename': 'Siyo.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8a'),
            'french': 'hache',
            'audio_path': 'audio/maison/Soha.m4a',
            'audio_filename': 'Soha.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6f'),
            'french': 'maison',
            'audio_path': 'audio/maison/Tragnou.m4a',
            'audio_filename': 'Tragnou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c80'),
            'french': 'couteau',
            'audio_path': 'audio/maison/Sembéya.m4a',
            'audio_filename': 'Sembéya.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c85'),
            'french': 'véranda',
            'audio_path': 'audio/maison/Baraza.m4a',
            'audio_filename': 'Baraza.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c82'),
            'french': 'oreiller',
            'audio_path': 'audio/maison/Hondagna.m4a',
            'audio_filename': 'Hondagna.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c71'),
            'french': 'case',
            'audio_path': 'audio/maison/Banga.m4a',
            'audio_filename': 'Banga.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8f'),
            'french': 'balai',
            'audio_path': 'audio/maison/Famafa.m4a',
            'audio_filename': 'Famafa.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8c'),
            'french': 'coupe-coupe',
            'audio_path': 'audio/maison/Chombou.m4a',
            'audio_filename': 'Chombou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c81'),
            'french': 'matelas',
            'audio_path': 'audio/maison/Goudorou.m4a',
            'audio_filename': 'Goudorou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c87'),
            'french': 'ampoule',
            'audio_path': 'audio/maison/Lalampou.m4a',
            'audio_filename': 'Lalampou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8f'),
            'french': 'balai',
            'audio_path': 'audio/maison/Péou.m4a',
            'audio_filename': 'Péou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c83'),
            'french': 'buffet',
            'audio_path': 'audio/maison/Biffé.m4a',
            'audio_filename': 'Biffé.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7b'),
            'french': 'cour',
            'audio_path': 'audio/maison/Mraba.m4a',
            'audio_filename': 'Mraba.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7b'),
            'french': 'cour',
            'audio_path': 'audio/maison/Lacourou.m4a',
            'audio_filename': 'Lacourou.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7f'),
            'french': 'louche',
            'audio_path': 'audio/maison/Chiwi.m4a',
            'audio_filename': 'Chiwi.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c81'),
            'french': 'matelas',
            'audio_path': 'audio/maison/Godoro.m4a',
            'audio_filename': 'Godoro.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c73'),
            'french': 'marmite',
            'audio_path': 'audio/maison/Vilangni.m4a',
            'audio_filename': 'Vilangni.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7b'),
            'french': 'cour',
            'audio_path': 'audio/maison/Mraba k.m4a',
            'audio_filename': 'Mraba k.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc7'),
            'french': 'mouton',
            'audio_path': 'audio/maison/Riba.m4a',
            'audio_filename': 'Riba.m4a',
            'category': 'maison',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c7f'),
            'french': 'louche',
            'audio_path': 'audio/maison/Pow.m4a',
            'audio_filename': 'Pow.m4a',
            'category': 'maison',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille_backup_20250923_052952/Zoki lalahi.m4a',
            'audio_filename': 'Zoki lalahi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/famille_backup_20250923_052952/Mama titi-bolé.m4a',
            'audio_filename': 'Mama titi-bolé.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille_backup_20250923_052952/Coco.m4a',
            'audio_filename': 'Coco.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille_backup_20250923_052952/Mama.m4a',
            'audio_filename': 'Mama.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c22'),
            'french': 'famille',
            'audio_path': 'audio/famille_backup_20250923_052952/Havagna.m4a',
            'audio_filename': 'Havagna.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille_backup_20250923_052952/Zouki.m4a',
            'audio_filename': 'Zouki.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/famille_backup_20250923_052952/Baba héli-bé.m4a',
            'audio_filename': 'Baba héli-bé.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c30'),
            'french': 'tante paternelle',
            'audio_path': 'audio/famille_backup_20250923_052952/Zena.m4a',
            'audio_filename': 'Zena.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c29'),
            'french': 'petit frère',
            'audio_path': 'audio/famille_backup_20250923_052952/Moina.m4a',
            'audio_filename': 'Moina.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250923_052952/Baba s.m4a',
            'audio_filename': 'Baba s.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille_backup_20250923_052952/Zoki viavi.m4a',
            'audio_filename': 'Zoki viavi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/famille_backup_20250923_052952/Baba titi-bolé.m4a',
            'audio_filename': 'Baba titi-bolé.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250923_052952/Zouki mtroubaba.m4a',
            'audio_filename': 'Zouki mtroubaba.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250923_052952/Baba k.m4a',
            'audio_filename': 'Baba k.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille_backup_20250923_052952/Dadayi.m4a',
            'audio_filename': 'Dadayi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250923_052952/Moinagna mtroubaba.m4a',
            'audio_filename': 'Moinagna mtroubaba.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2d'),
            'french': 'oncle maternel',
            'audio_path': 'audio/famille_backup_20250923_052952/Zama.m4a',
            'audio_filename': 'Zama.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille_backup_20250923_052952/Lalahi.m4a',
            'audio_filename': 'Lalahi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille_backup_20250923_052952/Mtroubaba.m4a',
            'audio_filename': 'Mtroubaba.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3a'),
            'french': 'ami',
            'audio_path': 'audio/famille_backup_20250923_052952/Mwandzani.m4a',
            'audio_filename': 'Mwandzani.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c26'),
            'french': 'sœur',
            'audio_path': 'audio/famille_backup_20250923_052952/Anabavi.m4a',
            'audio_filename': 'Anabavi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2c'),
            'french': 'grand-mère',
            'audio_path': 'audio/famille_backup_20250923_052952/Dadi.m4a',
            'audio_filename': 'Dadi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/famille_backup_20250923_052952/Ninfndri héli-bé.m4a',
            'audio_filename': 'Ninfndri héli-bé.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille_backup_20250923_052952/Bacoco.m4a',
            'audio_filename': 'Bacoco.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c22'),
            'french': 'famille',
            'audio_path': 'audio/famille_backup_20250923_052952/Mdjamaza.m4a',
            'audio_filename': 'Mdjamaza.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c31'),
            'french': 'garçon',
            'audio_path': 'audio/famille_backup_20250923_052952/Tseki lalahi.m4a',
            'audio_filename': 'Tseki lalahi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille_backup_20250923_052952/Mtroumama.m4a',
            'audio_filename': 'Mtroumama.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille_backup_20250923_052952/Zouki mtroumché.m4a',
            'audio_filename': 'Zouki mtroumché.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille_backup_20250923_052952/Moinagna mtroumama.m4a',
            'audio_filename': 'Moinagna mtroumama.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c25'),
            'french': 'frère',
            'audio_path': 'audio/famille_backup_20250923_052952/Anadahi.m4a',
            'audio_filename': 'Anadahi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille_backup_20250923_052952/Viavi.m4a',
            'audio_filename': 'Viavi.m4a',
            'category': 'famille_backup_20250923_052952',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bca'),
            'french': 'zébu',
            'audio_path': 'audio/tradition/Ngoma ya nyombé.m4a',
            'audio_filename': 'Ngoma ya nyombé.m4a',
            'category': 'tradition',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bca'),
            'french': 'zébu',
            'audio_path': 'audio/tradition/Vala naoumbi.m4a',
            'audio_filename': 'Vala naoumbi.m4a',
            'category': 'tradition',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c18'),
            'french': 'bonsoir',
            'audio_path': 'audio/expressions/Hali.m4a',
            'audio_filename': 'Hali.m4a',
            'category': 'expressions',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf7'),
            'french': 'oursin',
            'audio_path': 'audio/expressions/Hari.m4a',
            'audio_filename': 'Hari.m4a',
            'category': 'expressions',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b98'),
            'french': 'un',
            'audio_path': 'audio/expressions/Hotri inou haligni areki.m4a',
            'audio_filename': 'Hotri inou haligni areki.m4a',
            'category': 'expressions',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888c'),
            'french': 'content',
            'audio_path': 'audio/expressions/Aravouagna.m4a',
            'audio_filename': 'Aravouagna.m4a',
            'category': 'expressions',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c42'),
            'french': 'marron',
            'audio_path': 'audio/nourriture/Fotafotaka.m4a',
            'audio_filename': 'Fotafotaka.m4a',
            'category': 'nourriture',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b75'),
            'french': 'chemin',
            'audio_path': 'audio/nourriture/Dzia.m4a',
            'audio_filename': 'Dzia.m4a',
            'category': 'nourriture',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4d'),
            'french': 'lait',
            'audio_path': 'audio/nourriture/Rounounou.m4a',
            'audio_filename': 'Rounounou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c43'),
            'french': 'riz',
            'audio_path': 'audio/nourriture/Tsoholé.m4a',
            'audio_filename': 'Tsoholé.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c43'),
            'french': 'riz',
            'audio_path': 'audio/nourriture/Vari.m4a',
            'audio_filename': 'Vari.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c63'),
            'french': 'sel',
            'audio_path': 'audio/nourriture/Chingo.m4a',
            'audio_filename': 'Chingo.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c41'),
            'french': 'gris',
            'audio_path': 'audio/nourriture/Djifou.m4a',
            'audio_filename': 'Djifou.m4a',
            'category': 'nourriture',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4b'),
            'french': 'noix de coco',
            'audio_path': 'audio/nourriture/Voiniou.m4a',
            'audio_filename': 'Voiniou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c49'),
            'french': 'gâteau',
            'audio_path': 'audio/nourriture/Moukari.m4a',
            'audio_filename': 'Moukari.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b84'),
            'french': 'cocotier',
            'audio_path': 'audio/nourriture/Nadzi.m4a',
            'audio_filename': 'Nadzi.m4a',
            'category': 'nourriture',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5c'),
            'french': 'oignon',
            'audio_path': 'audio/nourriture/Doungoulou.m4a',
            'audio_filename': 'Doungoulou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c47'),
            'french': 'banane',
            'audio_path': 'audio/nourriture/Trovi ya nadzi.m4a',
            'audio_filename': 'Trovi ya nadzi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c66'),
            'french': 'cumin',
            'audio_path': 'audio/nourriture/Massala.m4a',
            'audio_filename': 'Massala.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4c'),
            'french': 'noix de coco fraîche',
            'audio_path': 'audio/nourriture/Chijavou.m4a',
            'audio_filename': 'Chijavou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c48'),
            'french': 'pain',
            'audio_path': 'audio/nourriture/Dipé.m4a',
            'audio_filename': 'Dipé.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5a'),
            'french': 'œuf',
            'audio_path': 'audio/nourriture/Antoudi.m4a',
            'audio_filename': 'Antoudi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6d'),
            'french': 'nourriture',
            'audio_path': 'audio/nourriture/Chaoula.m4a',
            'audio_filename': 'Chaoula.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c47'),
            'french': 'banane',
            'audio_path': 'audio/nourriture/Hountsi an voiniou.m4a',
            'audio_filename': 'Hountsi an voiniou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c43'),
            'french': 'riz',
            'audio_path': 'audio/nourriture/Tsoholé ya nadzi.m4a',
            'audio_filename': 'Tsoholé ya nadzi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bda'),
            'french': 'requin',
            'audio_path': 'audio/nourriture/Papaya.m4a',
            'audio_filename': 'Papaya.m4a',
            'category': 'nourriture',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5c'),
            'french': 'oignon',
            'audio_path': 'audio/nourriture/Chouroungou voudjé.m4a',
            'audio_filename': 'Chouroungou voudjé.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4c'),
            'french': 'noix de coco fraîche',
            'audio_path': 'audio/nourriture/Kidjavou.m4a',
            'audio_filename': 'Kidjavou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c41'),
            'french': 'gris',
            'audio_path': 'audio/nourriture/Dzofou.m4a',
            'audio_filename': 'Dzofou.m4a',
            'category': 'nourriture',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c60'),
            'french': 'manioc',
            'audio_path': 'audio/nourriture/Mhogo.m4a',
            'audio_filename': 'Mhogo.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5f'),
            'french': 'mandarine',
            'audio_path': 'audio/nourriture/Madhandzé.m4a',
            'audio_filename': 'Madhandzé.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388883'),
            'french': 'ancien',
            'audio_path': 'audio/nourriture/Sakèyi.m4a',
            'audio_filename': 'Sakèyi.m4a',
            'category': 'nourriture',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki mafana k.m4a',
            'audio_filename': 'Féliki mafana k.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c69'),
            'french': 'vanille',
            'audio_path': 'audio/nourriture/Lavani.m4a',
            'audio_filename': 'Lavani.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki nyongo.m4a',
            'audio_filename': 'Féliki nyongo.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5b'),
            'french': 'tomate',
            'audio_path': 'audio/nourriture/Tamati.m4a',
            'audio_filename': 'Tamati.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4e'),
            'french': 'viande',
            'audio_path': 'audio/nourriture/Amboumati.m4a',
            'audio_filename': 'Amboumati.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3f'),
            'french': 'jaune',
            'audio_path': 'audio/nourriture/Tamoutamou.m4a',
            'audio_filename': 'Tamoutamou.m4a',
            'category': 'nourriture',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5c'),
            'french': 'oignon',
            'audio_path': 'audio/nourriture/Doungoulou mvoudjou.m4a',
            'audio_filename': 'Doungoulou mvoudjou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7d'),
            'french': 'arbre',
            'audio_path': 'audio/nourriture/Madirou kakazou.m4a',
            'audio_filename': 'Madirou kakazou.m4a',
            'category': 'nourriture',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c56'),
            'french': 'bouillon',
            'audio_path': 'audio/nourriture/Woubou.m4a',
            'audio_filename': 'Woubou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c46'),
            'french': 'pois d'angole',
            'audio_path': 'audio/nourriture/Ambatri.m4a',
            'audio_filename': 'Ambatri.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c8a'),
            'french': 'hache',
            'audio_path': 'audio/nourriture/Tsoha.m4a',
            'audio_filename': 'Tsoha.m4a',
            'category': 'nourriture',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4e'),
            'french': 'viande',
            'audio_path': 'audio/nourriture/Nhyama.m4a',
            'audio_filename': 'Nhyama.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki mafana s.m4a',
            'audio_filename': 'Féliki mafana s.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3f'),
            'french': 'jaune',
            'audio_path': 'audio/nourriture/Dzindzano.m4a',
            'audio_filename': 'Dzindzano.m4a',
            'category': 'nourriture',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c54'),
            'french': 'brèdes patate douce',
            'audio_path': 'audio/nourriture/Batata.m4a',
            'audio_filename': 'Batata.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5a'),
            'french': 'œuf',
            'audio_path': 'audio/nourriture/Joiyi.m4a',
            'audio_filename': 'Joiyi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6a'),
            'french': 'tamarin',
            'audio_path': 'audio/nourriture/Ouhajou.m4a',
            'audio_filename': 'Ouhajou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c45'),
            'french': 'ananas',
            'audio_path': 'audio/nourriture/Nanassi.m4a',
            'audio_filename': 'Nanassi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki batata.m4a',
            'audio_filename': 'Féliki batata.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c40'),
            'french': 'rouge',
            'audio_path': 'audio/nourriture/Mena.m4a',
            'audio_filename': 'Mena.m4a',
            'category': 'nourriture',
            'section': 'couleurs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886a'),
            'french': 'dur',
            'audio_path': 'audio/nourriture/Manga.m4a',
            'audio_filename': 'Manga.m4a',
            'category': 'nourriture',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc2'),
            'french': 'mouche',
            'audio_path': 'audio/nourriture/Tsoha madzandzi.m4a',
            'audio_filename': 'Tsoha madzandzi.m4a',
            'category': 'nourriture',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c61'),
            'french': 'piment',
            'audio_path': 'audio/nourriture/Pilipili.m4a',
            'audio_filename': 'Pilipili.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/nourriture/Féliki angnatsindra.m4a',
            'audio_filename': 'Féliki angnatsindra.m4a',
            'category': 'nourriture',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c52'),
            'french': 'brède manioc',
            'audio_path': 'audio/nourriture/Mouhogou.m4a',
            'audio_filename': 'Mouhogou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/nourriture/Troundra.m4a',
            'audio_filename': 'Troundra.m4a',
            'category': 'nourriture',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c46'),
            'french': 'pois d'angole',
            'audio_path': 'audio/nourriture/Tsouzi.m4a',
            'audio_filename': 'Tsouzi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388890'),
            'french': 'fâché',
            'audio_path': 'audio/nourriture/Sira.m4a',
            'audio_filename': 'Sira.m4a',
            'category': 'nourriture',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c59'),
            'french': 'poulet',
            'audio_path': 'audio/nourriture/Bawa.m4a',
            'audio_filename': 'Bawa.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6e'),
            'french': 'riz non décortiqué',
            'audio_path': 'audio/nourriture/Mélé.m4a',
            'audio_filename': 'Mélé.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5b'),
            'french': 'tomate',
            'audio_path': 'audio/nourriture/Matimati.m4a',
            'audio_filename': 'Matimati.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c52'),
            'french': 'brède manioc',
            'audio_path': 'audio/nourriture/Mataba.m4a',
            'audio_filename': 'Mataba.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6c'),
            'french': 'papaye',
            'audio_path': 'audio/nourriture/Poipoiya.m4a',
            'audio_filename': 'Poipoiya.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887c'),
            'french': 'chaud',
            'audio_path': 'audio/nourriture/Maji ya moro.m4a',
            'audio_filename': 'Maji ya moro.m4a',
            'category': 'nourriture',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4a'),
            'french': 'mangue',
            'audio_path': 'audio/nourriture/Bvilibvili manga.m4a',
            'audio_filename': 'Bvilibvili manga.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c47'),
            'french': 'banane',
            'audio_path': 'audio/nourriture/Trovi.m4a',
            'audio_filename': 'Trovi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c6d'),
            'french': 'nourriture',
            'audio_path': 'audio/nourriture/Hanigni.m4a',
            'audio_filename': 'Hanigni.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b80'),
            'french': 'bananier',
            'audio_path': 'audio/nourriture/Hountsi.m4a',
            'audio_filename': 'Hountsi.m4a',
            'category': 'nourriture',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8d'),
            'french': 'marée basse',
            'audio_path': 'audio/nourriture/Maji.m4a',
            'audio_filename': 'Maji.m4a',
            'category': 'nourriture',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5c'),
            'french': 'oignon',
            'audio_path': 'audio/nourriture/Doungoulou ravigni.m4a',
            'audio_filename': 'Doungoulou ravigni.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki k.m4a',
            'audio_filename': 'Féliki k.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c72'),
            'french': 'lit',
            'audio_path': 'audio/nourriture/Kouba.m4a',
            'audio_filename': 'Kouba.m4a',
            'category': 'nourriture',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887c'),
            'french': 'chaud',
            'audio_path': 'audio/nourriture/Ranou meyi.m4a',
            'audio_filename': 'Ranou meyi.m4a',
            'category': 'nourriture',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki s.m4a',
            'audio_filename': 'Féliki s.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c59'),
            'french': 'poulet',
            'audio_path': 'audio/nourriture/Mabawa.m4a',
            'audio_filename': 'Mabawa.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c64'),
            'french': 'poivre',
            'audio_path': 'audio/nourriture/Vilivili.m4a',
            'audio_filename': 'Vilivili.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c45'),
            'french': 'ananas',
            'audio_path': 'audio/nourriture/Mananassi.m4a',
            'audio_filename': 'Mananassi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c43'),
            'french': 'riz',
            'audio_path': 'audio/nourriture/Vari tsivoidissa.m4a',
            'audio_filename': 'Vari tsivoidissa.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c5c'),
            'french': 'oignon',
            'audio_path': 'audio/nourriture/Chouroungou.m4a',
            'audio_filename': 'Chouroungou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c50'),
            'french': 'brèdes',
            'audio_path': 'audio/nourriture/Féliki mouhogou.m4a',
            'audio_filename': 'Féliki mouhogou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c43'),
            'french': 'riz',
            'audio_path': 'audio/nourriture/Vari an voiniou.m4a',
            'audio_filename': 'Vari an voiniou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c49'),
            'french': 'gâteau',
            'audio_path': 'audio/nourriture/Mharé.m4a',
            'audio_filename': 'Mharé.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c44'),
            'french': 'eau',
            'audio_path': 'audio/nourriture/Majimbi.m4a',
            'audio_filename': 'Majimbi.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c61'),
            'french': 'piment',
            'audio_path': 'audio/nourriture/Poutou.m4a',
            'audio_filename': 'Poutou.m4a',
            'category': 'nourriture',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8d'),
            'french': 'marée basse',
            'audio_path': 'audio/nourriture/Ranou.m4a',
            'audio_filename': 'Ranou.m4a',
            'category': 'nourriture',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf2'),
            'french': 'voile',
            'audio_path': 'audio/vetements/Kichali k.m4a',
            'audio_filename': 'Kichali k.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce4'),
            'french': 'chemise',
            'audio_path': 'audio/vetements/Chimizi.m4a',
            'audio_filename': 'Chimizi.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce8'),
            'french': 'chapeau',
            'audio_path': 'audio/vetements/Kofia.m4a',
            'audio_filename': 'Kofia.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c9f'),
            'french': 'donner',
            'audio_path': 'audio/vetements/Salouvagna.m4a',
            'audio_filename': 'Salouvagna.m4a',
            'category': 'vetements',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf1'),
            'french': 'robe',
            'audio_path': 'audio/vetements/Robo.m4a',
            'audio_filename': 'Robo.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce7'),
            'french': 'sous-vêtement',
            'audio_path': 'audio/vetements/Silipou.m4a',
            'audio_filename': 'Silipou.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce6'),
            'french': 'short',
            'audio_path': 'audio/vetements/Kaliso.m4a',
            'audio_filename': 'Kaliso.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cee'),
            'french': 'baskets',
            'audio_path': 'audio/vetements/Magochi.m4a',
            'audio_filename': 'Magochi.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf0'),
            'french': 'jupe',
            'audio_path': 'audio/vetements/Jipo.m4a',
            'audio_filename': 'Jipo.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf2'),
            'french': 'voile',
            'audio_path': 'audio/vetements/Kichali s.m4a',
            'audio_filename': 'Kichali s.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce2'),
            'french': 'vêtement',
            'audio_path': 'audio/vetements/Ngouwo.m4a',
            'audio_filename': 'Ngouwo.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce2'),
            'french': 'vêtement',
            'audio_path': 'audio/vetements/Kandzou.m4a',
            'audio_filename': 'Kandzou.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce2'),
            'french': 'vêtement',
            'audio_path': 'audio/vetements/Ankandzou.m4a',
            'audio_filename': 'Ankandzou.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/vetements/Kandzou bolé.m4a',
            'audio_filename': 'Kandzou bolé.m4a',
            'category': 'vetements',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cef'),
            'french': 'tongs',
            'audio_path': 'audio/vetements/Sapatri.m4a',
            'audio_filename': 'Sapatri.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ced'),
            'french': 'chaussures',
            'audio_path': 'audio/vetements/Kabwa sapatri.m4a',
            'audio_filename': 'Kabwa sapatri.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ce5'),
            'french': 'pantalon',
            'audio_path': 'audio/vetements/Sourouali.m4a',
            'audio_filename': 'Sourouali.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c9f'),
            'french': 'donner',
            'audio_path': 'audio/vetements/Salouva.m4a',
            'audio_filename': 'Salouva.m4a',
            'category': 'vetements',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ced'),
            'french': 'chaussures',
            'audio_path': 'audio/vetements/Kabwa s.m4a',
            'audio_filename': 'Kabwa s.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf0'),
            'french': 'jupe',
            'audio_path': 'audio/vetements/Jipou.m4a',
            'audio_filename': 'Jipou.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ced'),
            'french': 'chaussures',
            'audio_path': 'audio/vetements/Kabwa k.m4a',
            'audio_filename': 'Kabwa k.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf1'),
            'french': 'robe',
            'audio_path': 'audio/vetements/Robou.m4a',
            'audio_filename': 'Robou.m4a',
            'category': 'vetements',
            'section': 'vetements'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd7'),
            'french': 'scorpion',
            'audio_path': 'audio/nature/Atihala.m4a',
            'audio_filename': 'Atihala.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b69'),
            'french': 'barrière de corail',
            'audio_path': 'audio/nature/Caléni.m4a',
            'audio_filename': 'Caléni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8f'),
            'french': 'marée haute',
            'audio_path': 'audio/nature/Ranou fénou.m4a',
            'audio_filename': 'Ranou fénou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b81'),
            'french': 'feuille',
            'audio_path': 'audio/nature/Mawoini.m4a',
            'audio_filename': 'Mawoini.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b95'),
            'french': 'vedette',
            'audio_path': 'audio/nature/Kwassa kwassa.m4a',
            'audio_filename': 'Kwassa kwassa.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8f'),
            'french': 'marée haute',
            'audio_path': 'audio/nature/Maji yamalé.m4a',
            'audio_filename': 'Maji yamalé.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6f'),
            'french': 'campagne',
            'audio_path': 'audio/nature/Malavouni.m4a',
            'audio_filename': 'Malavouni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b82'),
            'french': 'branche',
            'audio_path': 'audio/nature/Trahi s.m4a',
            'audio_filename': 'Trahi s.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7d'),
            'french': 'arbre',
            'audio_path': 'audio/nature/Mwiri.m4a',
            'audio_filename': 'Mwiri.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b74'),
            'french': 'plateau',
            'audio_path': 'audio/nature/Kètraka.m4a',
            'audio_filename': 'Kètraka.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b88'),
            'french': 'manguier',
            'audio_path': 'audio/nature/Voudi ni manga.m4a',
            'audio_filename': 'Voudi ni manga.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be2'),
            'french': 'phacochère',
            'audio_path': 'audio/nature/Nyéha.m4a',
            'audio_filename': 'Nyéha.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b79'),
            'french': 'fleur',
            'audio_path': 'audio/nature/Foulera.m4a',
            'audio_filename': 'Foulera.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b95'),
            'french': 'vedette',
            'audio_path': 'audio/nature/Vidéti.m4a',
            'audio_filename': 'Vidéti.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b97'),
            'french': 'école coranique',
            'audio_path': 'audio/nature/Shioni.m4a',
            'audio_filename': 'Shioni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6c'),
            'french': 'pont',
            'audio_path': 'audio/nature/Daradja.m4a',
            'audio_filename': 'Daradja.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b71'),
            'french': 'caillou',
            'audio_path': 'audio/nature/Bwé.m4a',
            'audio_filename': 'Bwé.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b89'),
            'french': 'jacquier',
            'audio_path': 'audio/nature/Voudi ni finéssi.m4a',
            'audio_filename': 'Voudi ni finéssi.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8e'),
            'french': 'platier',
            'audio_path': 'audio/nature/Kaléni.m4a',
            'audio_filename': 'Kaléni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b75'),
            'french': 'chemin',
            'audio_path': 'audio/nature/Lalagna.m4a',
            'audio_filename': 'Lalagna.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba0'),
            'french': 'neuf',
            'audio_path': 'audio/nature/Civi.m4a',
            'audio_filename': 'Civi.m4a',
            'category': 'nature',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b93'),
            'french': 'fagot',
            'audio_path': 'audio/nature/Azoumati.m4a',
            'audio_filename': 'Azoumati.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b90'),
            'french': 'inondé',
            'audio_path': 'audio/nature/Ourora.m4a',
            'audio_filename': 'Ourora.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/nature/Bandra.m4a',
            'audio_filename': 'Bandra.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b92'),
            'french': 'canne à sucre',
            'audio_path': 'audio/nature/Fari.m4a',
            'audio_filename': 'Fari.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b80'),
            'french': 'bananier',
            'audio_path': 'audio/nature/Trindri.m4a',
            'audio_filename': 'Trindri.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6b'),
            'french': 'rivière',
            'audio_path': 'audio/nature/Mouroni.m4a',
            'audio_filename': 'Mouroni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b83'),
            'french': 'tornade',
            'audio_path': 'audio/nature/Ouzimouyi.m4a',
            'audio_filename': 'Ouzimouyi.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba0'),
            'french': 'neuf',
            'audio_path': 'audio/nature/Civiampoulou.m4a',
            'audio_filename': 'Civiampoulou.m4a',
            'category': 'nature',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b94'),
            'french': 'pirogue',
            'audio_path': 'audio/nature/Lakana.m4a',
            'audio_filename': 'Lakana.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b91'),
            'french': 'sauvage',
            'audio_path': 'audio/nature/Di.m4a',
            'audio_filename': 'Di.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b64'),
            'french': 'vague',
            'audio_path': 'audio/nature/Houndza_riaka.m4a',
            'audio_filename': 'Houndza_riaka.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd0'),
            'french': 'papillon',
            'audio_path': 'audio/nature/Laka.m4a',
            'audio_filename': 'Laka.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388881'),
            'french': 'sale',
            'audio_path': 'audio/nature/Trotro.m4a',
            'audio_filename': 'Trotro.m4a',
            'category': 'nature',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b62'),
            'french': 'étoile',
            'audio_path': 'audio/nature/Lakintagna.m4a',
            'audio_filename': 'Lakintagna.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b87'),
            'french': 'bambou',
            'audio_path': 'audio/nature/Valiha.m4a',
            'audio_filename': 'Valiha.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b63'),
            'french': 'sable',
            'audio_path': 'audio/nature/Mtsangani.m4a',
            'audio_filename': 'Mtsangani.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7e'),
            'french': 'rue',
            'audio_path': 'audio/nature/Paré s.m4a',
            'audio_filename': 'Paré s.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8d'),
            'french': 'marée basse',
            'audio_path': 'audio/nature/Maji yavo.m4a',
            'audio_filename': 'Maji yavo.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b67'),
            'french': 'mangrove',
            'audio_path': 'audio/nature/Honkou.m4a',
            'audio_filename': 'Honkou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b86'),
            'french': 'baobab',
            'audio_path': 'audio/nature/Voudi ni bouyou.m4a',
            'audio_filename': 'Voudi ni bouyou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7a'),
            'french': 'soleil',
            'audio_path': 'audio/nature/Jouwa.m4a',
            'audio_filename': 'Jouwa.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b62'),
            'french': 'étoile',
            'audio_path': 'audio/nature/Gnora.m4a',
            'audio_filename': 'Gnora.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b65'),
            'french': 'vent',
            'audio_path': 'audio/nature/Tsikou soulaimana.m4a',
            'audio_filename': 'Tsikou soulaimana.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8c'),
            'french': 'érosion',
            'audio_path': 'audio/nature/Padza s.m4a',
            'audio_filename': 'Padza s.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4b'),
            'french': 'noix de coco',
            'audio_path': 'audio/nature/M_nadzi.m4a',
            'audio_filename': 'M_nadzi.m4a',
            'category': 'nature',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc2'),
            'french': 'mouche',
            'audio_path': 'audio/nature/Ndzia.m4a',
            'audio_filename': 'Ndzia.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c4a'),
            'french': 'mangue',
            'audio_path': 'audio/nature/M_manga.m4a',
            'audio_filename': 'M_manga.m4a',
            'category': 'nature',
            'section': 'nourriture'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b96'),
            'french': 'école',
            'audio_path': 'audio/nature/Licoli.m4a',
            'audio_filename': 'Licoli.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7e'),
            'french': 'rue',
            'audio_path': 'audio/nature/Paré k.m4a',
            'audio_filename': 'Paré k.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7d'),
            'french': 'arbre',
            'audio_path': 'audio/nature/Kakazou.m4a',
            'audio_filename': 'Kakazou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b63'),
            'french': 'sable',
            'audio_path': 'audio/nature/Fasigni.m4a',
            'audio_filename': 'Fasigni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6d'),
            'french': 'nuage',
            'audio_path': 'audio/nature/Vingou.m4a',
            'audio_filename': 'Vingou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b84'),
            'french': 'cocotier',
            'audio_path': 'audio/nature/Voudi ni vwaniou.m4a',
            'audio_filename': 'Voudi ni vwaniou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b64'),
            'french': 'vague',
            'audio_path': 'audio/nature/Dhouja.m4a',
            'audio_filename': 'Dhouja.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb0'),
            'french': 'soixante-dix',
            'audio_path': 'audio/nature/Sabouini.m4a',
            'audio_filename': 'Sabouini.m4a',
            'category': 'nature',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b97'),
            'french': 'école coranique',
            'audio_path': 'audio/nature/Kioni.m4a',
            'audio_filename': 'Kioni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b85'),
            'french': 'arbre à pain',
            'audio_path': 'audio/nature/Voudi ni frampé.m4a',
            'audio_filename': 'Voudi ni frampé.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388883'),
            'french': 'ancien',
            'audio_path': 'audio/nature/Mahaléni.m4a',
            'audio_filename': 'Mahaléni.m4a',
            'category': 'nature',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b68'),
            'french': 'corail',
            'audio_path': 'audio/nature/Soiyi s.m4a',
            'audio_filename': 'Soiyi s.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b67'),
            'french': 'mangrove',
            'audio_path': 'audio/nature/Mhonko.m4a',
            'audio_filename': 'Mhonko.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b63'),
            'french': 'sable',
            'audio_path': 'audio/nature/Mtsanga.m4a',
            'audio_filename': 'Mtsanga.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b80'),
            'french': 'bananier',
            'audio_path': 'audio/nature/Voudi ni hountsi.m4a',
            'audio_filename': 'Voudi ni hountsi.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8b'),
            'french': 'sol',
            'audio_path': 'audio/nature/Tani.m4a',
            'audio_filename': 'Tani.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b78'),
            'french': 'herbe',
            'audio_path': 'audio/nature/Haitri.m4a',
            'audio_filename': 'Haitri.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b61'),
            'french': 'lune',
            'audio_path': 'audio/nature/Fandzava.m4a',
            'audio_filename': 'Fandzava.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7a'),
            'french': 'soleil',
            'audio_path': 'audio/nature/Zouva.m4a',
            'audio_filename': 'Zouva.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79beb'),
            'french': 'crevette',
            'audio_path': 'audio/nature/Mcacamba.m4a',
            'audio_filename': 'Mcacamba.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b71'),
            'french': 'caillou',
            'audio_path': 'audio/nature/Vatou.m4a',
            'audio_filename': 'Vatou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd1'),
            'french': 'ver de terre',
            'audio_path': 'audio/nature/Fotaka.m4a',
            'audio_filename': 'Fotaka.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c13'),
            'french': 'sourcil',
            'audio_path': 'audio/nature/Tsi.m4a',
            'audio_filename': 'Tsi.m4a',
            'category': 'nature',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b61'),
            'french': 'lune',
            'audio_path': 'audio/nature/Mwézi.m4a',
            'audio_filename': 'Mwézi.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b68'),
            'french': 'corail',
            'audio_path': 'audio/nature/Soiyi k.m4a',
            'audio_filename': 'Soiyi k.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8c'),
            'french': 'érosion',
            'audio_path': 'audio/nature/Padza k.m4a',
            'audio_filename': 'Padza k.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b5e'),
            'french': 'pente',
            'audio_path': 'audio/nature/Mlima.m4a',
            'audio_filename': 'Mlima.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8d'),
            'french': 'marée basse',
            'audio_path': 'audio/nature/Ranou mèki.m4a',
            'audio_filename': 'Ranou mèki.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6d'),
            'french': 'nuage',
            'audio_path': 'audio/nature/Wingou.m4a',
            'audio_filename': 'Wingou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6a'),
            'french': 'tempête',
            'audio_path': 'audio/nature/Darouba.m4a',
            'audio_filename': 'Darouba.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b90'),
            'french': 'inondé',
            'audio_path': 'audio/nature/Dobou.m4a',
            'audio_filename': 'Dobou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b66'),
            'french': 'pluie',
            'audio_path': 'audio/nature/Vhoua.m4a',
            'audio_filename': 'Vhoua.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b7c'),
            'french': 'plage',
            'audio_path': 'audio/nature/Fassigni.m4a',
            'audio_filename': 'Fassigni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b65'),
            'french': 'vent',
            'audio_path': 'audio/nature/Pévo.m4a',
            'audio_filename': 'Pévo.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b81'),
            'french': 'feuille',
            'audio_path': 'audio/nature/Hayitri.m4a',
            'audio_filename': 'Hayitri.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6f'),
            'french': 'campagne',
            'audio_path': 'audio/nature/Malavou.m4a',
            'audio_filename': 'Malavou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b6b'),
            'french': 'rivière',
            'audio_path': 'audio/nature/Mouro.m4a',
            'audio_filename': 'Mouro.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b5e'),
            'french': 'pente',
            'audio_path': 'audio/nature/Boungou.m4a',
            'audio_filename': 'Boungou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b82'),
            'french': 'branche',
            'audio_path': 'audio/nature/Trahi k.m4a',
            'audio_filename': 'Trahi k.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b8e'),
            'french': 'platier',
            'audio_path': 'audio/nature/Kalé.m4a',
            'audio_filename': 'Kalé.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b93'),
            'french': 'fagot',
            'audio_path': 'audio/nature/Kouni.m4a',
            'audio_filename': 'Kouni.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b65'),
            'french': 'vent',
            'audio_path': 'audio/nature/Tsikou.m4a',
            'audio_filename': 'Tsikou.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b92'),
            'french': 'canne à sucre',
            'audio_path': 'audio/nature/Mouwoi.m4a',
            'audio_filename': 'Mouwoi.m4a',
            'category': 'nature',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf7'),
            'french': 'oursin',
            'audio_path': 'audio/nature/Bahari.m4a',
            'audio_filename': 'Bahari.m4a',
            'category': 'nature',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388890'),
            'french': 'fâché',
            'audio_path': 'audio/adjectifs/Ouja hassira.m4a',
            'audio_filename': 'Ouja hassira.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/adjectifs/Titi.m4a',
            'audio_filename': 'Titi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888b'),
            'french': 'fermé',
            'audio_path': 'audio/adjectifs/Migadra.m4a',
            'audio_filename': 'Migadra.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388898'),
            'french': 'court',
            'audio_path': 'audio/adjectifs/Koutri.m4a',
            'audio_filename': 'Koutri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887e'),
            'french': 'lourd',
            'audio_path': 'audio/adjectifs/Ndziro.m4a',
            'audio_filename': 'Ndziro.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388897'),
            'french': 'long',
            'audio_path': 'audio/adjectifs/Habou.m4a',
            'audio_filename': 'Habou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888c'),
            'french': 'content',
            'audio_path': 'audio/adjectifs/Oufourahi.m4a',
            'audio_filename': 'Oufourahi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887c'),
            'french': 'chaud',
            'audio_path': 'audio/adjectifs/Mèyi.m4a',
            'audio_filename': 'Mèyi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388869'),
            'french': 'fort',
            'audio_path': 'audio/adjectifs/Missi ngouvou.m4a',
            'audio_filename': 'Missi ngouvou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886c'),
            'french': 'beau/jolie',
            'audio_path': 'audio/adjectifs/Mzouri.m4a',
            'audio_filename': 'Mzouri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886a'),
            'french': 'dur',
            'audio_path': 'audio/adjectifs/Mangavou.m4a',
            'audio_filename': 'Mangavou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388883'),
            'french': 'ancien',
            'audio_path': 'audio/adjectifs/Halé.m4a',
            'audio_filename': 'Halé.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388889'),
            'french': 'vrai',
            'audio_path': 'audio/adjectifs/Ankitigni.m4a',
            'audio_filename': 'Ankitigni.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388879'),
            'french': 'nerveux',
            'audio_path': 'audio/adjectifs/Oussikitiha.m4a',
            'audio_filename': 'Oussikitiha.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388870'),
            'french': 'gentil',
            'audio_path': 'audio/adjectifs/Tsara rohou.m4a',
            'audio_filename': 'Tsara rohou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886d'),
            'french': 'laid',
            'audio_path': 'audio/adjectifs/Tsi ndzouzouri(1).m4a',
            'audio_filename': 'Tsi ndzouzouri(1).m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887f'),
            'french': 'léger',
            'audio_path': 'audio/adjectifs/Ndzangou.m4a',
            'audio_filename': 'Ndzangou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886a'),
            'french': 'dur',
            'audio_path': 'audio/adjectifs/Mahéri.m4a',
            'audio_filename': 'Mahéri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887b'),
            'french': 'mauvais',
            'audio_path': 'audio/adjectifs/Mwadéli.m4a',
            'audio_filename': 'Mwadéli.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388886'),
            'french': 'important',
            'audio_path': 'audio/adjectifs/Mouhimou.m4a',
            'audio_filename': 'Mouhimou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886e'),
            'french': 'jeune',
            'audio_path': 'audio/adjectifs/Nrétsa.m4a',
            'audio_filename': 'Nrétsa.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388887'),
            'french': 'inutile',
            'audio_path': 'audio/adjectifs/Kassina mana.m4a',
            'audio_filename': 'Kassina mana.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886f'),
            'french': 'vieux',
            'audio_path': 'audio/adjectifs/Dhouha.m4a',
            'audio_filename': 'Dhouha.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388876'),
            'french': 'sérieux',
            'audio_path': 'audio/adjectifs/Koussoudi.m4a',
            'audio_filename': 'Koussoudi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388870'),
            'french': 'gentil',
            'audio_path': 'audio/adjectifs/Tsara.m4a',
            'audio_filename': 'Tsara.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888a'),
            'french': 'ouvert',
            'audio_path': 'audio/adjectifs/Ouboua.m4a',
            'audio_filename': 'Ouboua.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888e'),
            'french': 'fatigué',
            'audio_path': 'audio/adjectifs/Ouléméwa.m4a',
            'audio_filename': 'Ouléméwa.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388867'),
            'french': 'gros',
            'audio_path': 'audio/adjectifs/Mtronga-tronga.m4a',
            'audio_filename': 'Mtronga-tronga.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388897'),
            'french': 'long',
            'audio_path': 'audio/adjectifs/Drilé.m4a',
            'audio_filename': 'Drilé.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388877'),
            'french': 'drôle',
            'audio_path': 'audio/adjectifs/Outsésa.m4a',
            'audio_filename': 'Outsésa.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388878'),
            'french': 'calme',
            'audio_path': 'audio/adjectifs/Baridi.m4a',
            'audio_filename': 'Baridi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388879'),
            'french': 'nerveux',
            'audio_path': 'audio/adjectifs/Tèhitri.m4a',
            'audio_filename': 'Tèhitri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887f'),
            'french': 'léger',
            'audio_path': 'audio/adjectifs/Mayivagna.m4a',
            'audio_filename': 'Mayivagna.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388872'),
            'french': 'intelligent',
            'audio_path': 'audio/adjectifs/Mstanrabou.m4a',
            'audio_filename': 'Mstanrabou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388873'),
            'french': 'bête',
            'audio_path': 'audio/adjectifs/Dhaba.m4a',
            'audio_filename': 'Dhaba.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886e'),
            'french': 'jeune',
            'audio_path': 'audio/adjectifs/Zaza.m4a',
            'audio_filename': 'Zaza.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388876'),
            'french': 'sérieux',
            'audio_path': 'audio/adjectifs/Kassidi.m4a',
            'audio_filename': 'Kassidi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388879'),
            'french': 'nerveux',
            'audio_path': 'audio/adjectifs/Téhi téhitri.m4a',
            'audio_filename': 'Téhi téhitri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388881'),
            'french': 'sale',
            'audio_path': 'audio/adjectifs/Trotro.m4a',
            'audio_filename': 'Trotro.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/adjectifs/Bé.m4a',
            'audio_filename': 'Bé.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/adjectifs/Bolé.m4a',
            'audio_filename': 'Bolé.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388892'),
            'french': 'inquiet',
            'audio_path': 'audio/adjectifs/Miyéfitri-kouchanga.m4a',
            'audio_filename': 'Miyéfitri-kouchanga.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888d'),
            'french': 'triste',
            'audio_path': 'audio/adjectifs/Ouna hamo.m4a',
            'audio_filename': 'Ouna hamo.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388882'),
            'french': 'nouveau',
            'audio_path': 'audio/adjectifs/Vowou.m4a',
            'audio_filename': 'Vowou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388891'),
            'french': 'amoureux',
            'audio_path': 'audio/adjectifs/Mitiya.m4a',
            'audio_filename': 'Mitiya.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888f'),
            'french': 'colère',
            'audio_path': 'audio/adjectifs/Méloukou.m4a',
            'audio_filename': 'Méloukou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388894'),
            'french': 'honteux',
            'audio_path': 'audio/adjectifs/Ouona haya.m4a',
            'audio_filename': 'Ouona haya.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886d'),
            'french': 'laid',
            'audio_path': 'audio/adjectifs/Ratsi sora.m4a',
            'audio_filename': 'Ratsi sora.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388870'),
            'french': 'gentil',
            'audio_path': 'audio/adjectifs/Mwéma.m4a',
            'audio_filename': 'Mwéma.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887d'),
            'french': 'froid',
            'audio_path': 'audio/adjectifs/Manintsi.m4a',
            'audio_filename': 'Manintsi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388879'),
            'french': 'nerveux',
            'audio_path': 'audio/adjectifs/Téhi tèhitri.m4a',
            'audio_filename': 'Téhi tèhitri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388881'),
            'french': 'sale',
            'audio_path': 'audio/adjectifs/Maloutou.m4a',
            'audio_filename': 'Maloutou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888e'),
            'french': 'fatigué',
            'audio_path': 'audio/adjectifs/Vaha.m4a',
            'audio_filename': 'Vaha.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388891'),
            'french': 'amoureux',
            'audio_path': 'audio/adjectifs/Ouvendza.m4a',
            'audio_filename': 'Ouvendza.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388880'),
            'french': 'propre',
            'audio_path': 'audio/adjectifs/Irahara.m4a',
            'audio_filename': 'Irahara.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388888'),
            'french': 'faux',
            'audio_path': 'audio/adjectifs/Trambo.m4a',
            'audio_filename': 'Trambo.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388898'),
            'french': 'court',
            'audio_path': 'audio/adjectifs/Fohiki.m4a',
            'audio_filename': 'Fohiki.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887c'),
            'french': 'chaud',
            'audio_path': 'audio/adjectifs/Moro.m4a',
            'audio_filename': 'Moro.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886b'),
            'french': 'mou',
            'audio_path': 'audio/adjectifs/Malémi.m4a',
            'audio_filename': 'Malémi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888c'),
            'french': 'content',
            'audio_path': 'audio/adjectifs/Ravou.m4a',
            'audio_filename': 'Ravou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388877'),
            'french': 'drôle',
            'audio_path': 'audio/adjectifs/Mampimohi.m4a',
            'audio_filename': 'Mampimohi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888b'),
            'french': 'fermé',
            'audio_path': 'audio/adjectifs/Oubala.m4a',
            'audio_filename': 'Oubala.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886b'),
            'french': 'mou',
            'audio_path': 'audio/adjectifs/Trémboivou.m4a',
            'audio_filename': 'Trémboivou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388895'),
            'french': 'surpris',
            'audio_path': 'audio/adjectifs/Oumarouha.m4a',
            'audio_filename': 'Oumarouha.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388880'),
            'french': 'propre',
            'audio_path': 'audio/adjectifs/Madiou.m4a',
            'audio_filename': 'Madiou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388884'),
            'french': 'facile',
            'audio_path': 'audio/adjectifs/Mora.m4a',
            'audio_filename': 'Mora.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388875'),
            'french': 'pauvre',
            'audio_path': 'audio/adjectifs/Maskini.m4a',
            'audio_filename': 'Maskini.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388882'),
            'french': 'nouveau',
            'audio_path': 'audio/adjectifs/Piya.m4a',
            'audio_filename': 'Piya.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388871'),
            'french': 'méchant',
            'audio_path': 'audio/adjectifs/Ratsi rohou.m4a',
            'audio_filename': 'Ratsi rohou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/adjectifs/Héli.m4a',
            'audio_filename': 'Héli.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888f'),
            'french': 'colère',
            'audio_path': 'audio/adjectifs/Hadabou.m4a',
            'audio_filename': 'Hadabou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388872'),
            'french': 'intelligent',
            'audio_path': 'audio/adjectifs/Tsara louha.m4a',
            'audio_filename': 'Tsara louha.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388887'),
            'french': 'inutile',
            'audio_path': 'audio/adjectifs/Tsissi fotouni.m4a',
            'audio_filename': 'Tsissi fotouni.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388874'),
            'french': 'riche',
            'audio_path': 'audio/adjectifs/Tadjiri.m4a',
            'audio_filename': 'Tadjiri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388868'),
            'french': 'maigre',
            'audio_path': 'audio/adjectifs/Tsala.m4a',
            'audio_filename': 'Tsala.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388869'),
            'french': 'fort',
            'audio_path': 'audio/adjectifs/Ouna ngouvou.m4a',
            'audio_filename': 'Ouna ngouvou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886d'),
            'french': 'laid',
            'audio_path': 'audio/adjectifs/Tsi ndzouzouri.m4a',
            'audio_filename': 'Tsi ndzouzouri.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886f'),
            'french': 'vieux',
            'audio_path': 'audio/adjectifs/Héla.m4a',
            'audio_filename': 'Héla.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888d'),
            'french': 'triste',
            'audio_path': 'audio/adjectifs/Malahélou.m4a',
            'audio_filename': 'Malahélou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388888'),
            'french': 'faux',
            'audio_path': 'audio/adjectifs/Vandi.m4a',
            'audio_filename': 'Vandi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388871'),
            'french': 'méchant',
            'audio_path': 'audio/adjectifs/Mbovou.m4a',
            'audio_filename': 'Mbovou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388868'),
            'french': 'maigre',
            'audio_path': 'audio/adjectifs/Mahia.m4a',
            'audio_filename': 'Mahia.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388883'),
            'french': 'ancien',
            'audio_path': 'audio/adjectifs/Kèyi.m4a',
            'audio_filename': 'Kèyi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388889'),
            'french': 'vrai',
            'audio_path': 'audio/adjectifs/Kwéli.m4a',
            'audio_filename': 'Kwéli.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cd1'),
            'french': 'abîmer',
            'audio_path': 'audio/adjectifs/Oumengna.m4a',
            'audio_filename': 'Oumengna.m4a',
            'category': 'adjectifs',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388894'),
            'french': 'honteux',
            'audio_path': 'audio/adjectifs/Mampihingnatra.m4a',
            'audio_filename': 'Mampihingnatra.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388880'),
            'french': 'propre',
            'audio_path': 'audio/adjectifs/Irahara(1).m4a',
            'audio_filename': 'Irahara(1).m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887e'),
            'french': 'lourd',
            'audio_path': 'audio/adjectifs/Mavèchatra.m4a',
            'audio_filename': 'Mavèchatra.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888a'),
            'french': 'ouvert',
            'audio_path': 'audio/adjectifs/Zahou bou angala thi.m4a',
            'audio_filename': 'Zahou bou angala thi.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838888a'),
            'french': 'ouvert',
            'audio_path': 'audio/adjectifs/Mibiyangna.m4a',
            'audio_filename': 'Mibiyangna.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388893'),
            'french': 'fier',
            'audio_path': 'audio/adjectifs/Oujiviwa.m4a',
            'audio_filename': 'Oujiviwa.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886c'),
            'french': 'beau/jolie',
            'audio_path': 'audio/adjectifs/Zatovou.m4a',
            'audio_filename': 'Zatovou.m4a',
            'category': 'adjectifs',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf9'),
            'french': 'œil',
            'audio_path': 'audio/corps/Kiyo.m4a',
            'audio_filename': 'Kiyo.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfa'),
            'french': 'bouche',
            'audio_path': 'audio/corps/Cha.m4a',
            'audio_filename': 'Cha.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c00'),
            'french': 'cheveux',
            'audio_path': 'audio/corps/Ngnélé.m4a',
            'audio_filename': 'Ngnélé.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c0c'),
            'french': 'coude',
            'audio_path': 'audio/corps/Kové.m4a',
            'audio_filename': 'Kové.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c0e'),
            'french': 'front',
            'audio_path': 'audio/corps/Hangno.m4a',
            'audio_filename': 'Hangno.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388872'),
            'french': 'intelligent',
            'audio_path': 'audio/corps/Louha.m4a',
            'audio_filename': 'Louha.m4a',
            'category': 'corps',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc2'),
            'french': 'mouche',
            'audio_path': 'audio/corps/Ndzigni.m4a',
            'audio_filename': 'Ndzigni.m4a',
            'category': 'corps',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfe'),
            'french': 'pied',
            'audio_path': 'audio/corps/Mbavou.m4a',
            'audio_filename': 'Mbavou.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c0d'),
            'french': 'cœur',
            'audio_path': 'audio/corps/Soufigni.m4a',
            'audio_filename': 'Soufigni.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfd'),
            'french': 'main',
            'audio_path': 'audio/corps/Rambou faninti.m4a',
            'audio_filename': 'Rambou faninti.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c07'),
            'french': 'cou',
            'audio_path': 'audio/corps/Shitsoi.m4a',
            'audio_filename': 'Shitsoi.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c05'),
            'french': 'bras',
            'audio_path': 'audio/corps/Mbo.m4a',
            'audio_filename': 'Mbo.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdb'),
            'french': 'poulpe',
            'audio_path': 'audio/corps/Dzitso la pwédza.m4a',
            'audio_filename': 'Dzitso la pwédza.m4a',
            'category': 'corps',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c15'),
            'french': 'peau',
            'audio_path': 'audio/corps/Ngwezi.m4a',
            'audio_filename': 'Ngwezi.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c0f'),
            'french': 'joue',
            'audio_path': 'audio/corps/Savou.m4a',
            'audio_filename': 'Savou.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c0b'),
            'french': 'genou',
            'audio_path': 'audio/corps/Trenga.m4a',
            'audio_filename': 'Trenga.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c08'),
            'french': 'épaule',
            'audio_path': 'audio/corps/Bèga.m4a',
            'audio_filename': 'Bèga.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bff'),
            'french': 'tête',
            'audio_path': 'audio/corps/Tsingo.m4a',
            'audio_filename': 'Tsingo.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ca8'),
            'french': 'demander',
            'audio_path': 'audio/corps/Magno.m4a',
            'audio_filename': 'Magno.m4a',
            'category': 'corps',
            'section': 'verbes'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c02'),
            'french': 'langue',
            'audio_path': 'audio/corps/Oulimé.m4a',
            'audio_filename': 'Oulimé.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c04'),
            'french': 'ventre',
            'audio_path': 'audio/corps/Sokou.m4a',
            'audio_filename': 'Sokou.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c03'),
            'french': 'dos',
            'audio_path': 'audio/corps/Shlévou.m4a',
            'audio_filename': 'Shlévou.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c02'),
            'french': 'langue',
            'audio_path': 'audio/corps/Lèla.m4a',
            'audio_filename': 'Lèla.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c09'),
            'french': 'doigt',
            'audio_path': 'audio/corps/Tingui.m4a',
            'audio_filename': 'Tingui.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfd'),
            'french': 'main',
            'audio_path': 'audio/corps/Mhono.m4a',
            'audio_filename': 'Mhono.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c01'),
            'french': 'dent',
            'audio_path': 'audio/corps/Mengo.m4a',
            'audio_filename': 'Mengo.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bff'),
            'french': 'tête',
            'audio_path': 'audio/corps/Dhomo.m4a',
            'audio_filename': 'Dhomo.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfb'),
            'french': 'nez',
            'audio_path': 'audio/corps/Poua.m4a',
            'audio_filename': 'Poua.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfc'),
            'french': 'oreille',
            'audio_path': 'audio/corps/Soungni.m4a',
            'audio_filename': 'Soungni.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c12'),
            'french': 'barbe',
            'audio_path': 'audio/corps/Ndrévou.m4a',
            'audio_filename': 'Ndrévou.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c13'),
            'french': 'sourcil',
            'audio_path': 'audio/corps/Tsi.m4a',
            'audio_filename': 'Tsi.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c13'),
            'french': 'sourcil',
            'audio_path': 'audio/corps/Ankwéssi.m4a',
            'audio_filename': 'Ankwéssi.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c0e'),
            'french': 'front',
            'audio_path': 'audio/corps/Housso.m4a',
            'audio_filename': 'Housso.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfe'),
            'french': 'pied',
            'audio_path': 'audio/corps/Bavou.m4a',
            'audio_filename': 'Bavou.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c86'),
            'french': 'toiture',
            'audio_path': 'audio/corps/Somboutrou.m4a',
            'audio_filename': 'Somboutrou.m4a',
            'category': 'corps',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bfd'),
            'french': 'main',
            'audio_path': 'audio/corps/Faninti.m4a',
            'audio_filename': 'Faninti.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf9'),
            'french': 'œil',
            'audio_path': 'audio/corps/Matso.m4a',
            'audio_filename': 'Matso.m4a',
            'category': 'corps',
            'section': 'corps'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c19'),
            'french': 'au revoir',
            'audio_path': 'audio/salutations/Kwaheri.m4a',
            'audio_filename': 'Kwaheri.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388870'),
            'french': 'gentil',
            'audio_path': 'audio/salutations/Tsara.m4a',
            'audio_filename': 'Tsara.m4a',
            'category': 'salutations',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1f'),
            'french': 'bienvenue',
            'audio_path': 'audio/salutations/Maeva.m4a',
            'audio_filename': 'Maeva.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1f'),
            'french': 'bienvenue',
            'audio_path': 'audio/salutations/Maèva.m4a',
            'audio_filename': 'Maèva.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887a'),
            'french': 'bon',
            'audio_path': 'audio/salutations/Haligni tsara.m4a',
            'audio_filename': 'Haligni tsara.m4a',
            'category': 'salutations',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1d'),
            'french': 'oui',
            'audio_path': 'audio/salutations/Ewa.m4a',
            'audio_filename': 'Ewa.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c21'),
            'french': 'salut',
            'audio_path': 'audio/salutations/Kwezi.m4a',
            'audio_filename': 'Kwezi.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c17'),
            'french': 'bonjour',
            'audio_path': 'audio/salutations/Marahaba.m4a',
            'audio_filename': 'Marahaba.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c20'),
            'french': 'excusez-moi',
            'audio_path': 'audio/salutations/Jéjé.m4a',
            'audio_filename': 'Jéjé.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1c'),
            'french': 'merci',
            'audio_path': 'audio/salutations/Iya.m4a',
            'audio_filename': 'Iya.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1b'),
            'french': 'ça va bien',
            'audio_path': 'audio/salutations/Fétré.m4a',
            'audio_filename': 'Fétré.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c1a'),
            'french': 'comment ça va',
            'audio_path': 'audio/salutations/Oukou wa hairi.m4a',
            'audio_filename': 'Oukou wa hairi.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c17'),
            'french': 'bonjour',
            'audio_path': 'audio/salutations/Akori.m4a',
            'audio_filename': 'Akori.m4a',
            'category': 'salutations',
            'section': 'salutations'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille/Zoki lalahi.m4a',
            'audio_filename': 'Zoki lalahi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/famille/Mama titi-bolé.m4a',
            'audio_filename': 'Mama titi-bolé.m4a',
            'category': 'famille',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille/Coco.m4a',
            'audio_filename': 'Coco.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille/Mama.m4a',
            'audio_filename': 'Mama.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c22'),
            'french': 'famille',
            'audio_path': 'audio/famille/Havagna.m4a',
            'audio_filename': 'Havagna.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille/Zouki.m4a',
            'audio_filename': 'Zouki.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886e'),
            'french': 'jeune',
            'audio_path': 'audio/famille/Zaza lalahi.m4a',
            'audio_filename': 'Zaza lalahi.m4a',
            'category': 'famille',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838886e'),
            'french': 'jeune',
            'audio_path': 'audio/famille/Zaza viavi.m4a',
            'audio_filename': 'Zaza viavi.m4a',
            'category': 'famille',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/famille/Baba héli-bé.m4a',
            'audio_filename': 'Baba héli-bé.m4a',
            'category': 'famille',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c30'),
            'french': 'tante paternelle',
            'audio_path': 'audio/famille/Zena.m4a',
            'audio_filename': 'Zena.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c29'),
            'french': 'petit frère',
            'audio_path': 'audio/famille/Moina.m4a',
            'audio_filename': 'Moina.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille/Baba s.m4a',
            'audio_filename': 'Baba s.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille/Zoki viavi.m4a',
            'audio_filename': 'Zoki viavi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c30'),
            'french': 'tante paternelle',
            'audio_path': 'audio/famille/Zéna.m4a',
            'audio_filename': 'Zéna.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388865'),
            'french': 'grand',
            'audio_path': 'audio/famille/Baba titi-bolé.m4a',
            'audio_filename': 'Baba titi-bolé.m4a',
            'category': 'famille',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille/Zouki mtroubaba.m4a',
            'audio_filename': 'Zouki mtroubaba.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille/Baba k.m4a',
            'audio_filename': 'Baba k.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille/Dadayi.m4a',
            'audio_filename': 'Dadayi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille/Moinagna mtroubaba.m4a',
            'audio_filename': 'Moinagna mtroubaba.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2d'),
            'french': 'oncle maternel',
            'audio_path': 'audio/famille/Zama.m4a',
            'audio_filename': 'Zama.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c27'),
            'french': 'grand frère',
            'audio_path': 'audio/famille/Lalahi.m4a',
            'audio_filename': 'Lalahi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille/Mtroubaba.m4a',
            'audio_filename': 'Mtroubaba.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c3a'),
            'french': 'ami',
            'audio_path': 'audio/famille/Mwandzani.m4a',
            'audio_filename': 'Mwandzani.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c26'),
            'french': 'sœur',
            'audio_path': 'audio/famille/Anabavi.m4a',
            'audio_filename': 'Anabavi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2c'),
            'french': 'grand-mère',
            'audio_path': 'audio/famille/Dadi.m4a',
            'audio_filename': 'Dadi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c29'),
            'french': 'petit frère',
            'audio_path': 'audio/famille/Moinagna.m4a',
            'audio_filename': 'Moinagna.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c23'),
            'french': 'papa',
            'audio_path': 'audio/famille/Moina mtroubaba.m4a',
            'audio_filename': 'Moina mtroubaba.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388866'),
            'french': 'petit',
            'audio_path': 'audio/famille/Ninfndri héli-bé.m4a',
            'audio_filename': 'Ninfndri héli-bé.m4a',
            'category': 'famille',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille/Moina mtroumama.m4a',
            'audio_filename': 'Moina mtroumama.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c2b'),
            'french': 'grand-père',
            'audio_path': 'audio/famille/Bacoco.m4a',
            'audio_filename': 'Bacoco.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c22'),
            'french': 'famille',
            'audio_path': 'audio/famille/Mdjamaza.m4a',
            'audio_filename': 'Mdjamaza.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c31'),
            'french': 'garçon',
            'audio_path': 'audio/famille/Tseki lalahi.m4a',
            'audio_filename': 'Tseki lalahi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille/Mtroumama.m4a',
            'audio_filename': 'Mtroumama.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille/Zouki mtroumché.m4a',
            'audio_filename': 'Zouki mtroumché.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c24'),
            'french': 'maman',
            'audio_path': 'audio/famille/Moinagna mtroumama.m4a',
            'audio_filename': 'Moinagna mtroumama.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c25'),
            'french': 'frère',
            'audio_path': 'audio/famille/Anadahi.m4a',
            'audio_filename': 'Anadahi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c28'),
            'french': 'grande sœur',
            'audio_path': 'audio/famille/Viavi.m4a',
            'audio_filename': 'Viavi.m4a',
            'category': 'famille',
            'section': 'famille'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdf'),
            'french': 'éléphant',
            'audio_path': 'audio/animaux/Ndovu.m4a',
            'audio_filename': 'Ndovu.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf5'),
            'french': 'cône de mer',
            'audio_path': 'audio/animaux/Tsimtipaka.m4a',
            'audio_filename': 'Tsimtipaka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcd'),
            'french': 'pigeon',
            'audio_path': 'audio/animaux/Ndiwa.m4a',
            'audio_filename': 'Ndiwa.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcc'),
            'french': 'poule',
            'audio_path': 'audio/animaux/Akohou.m4a',
            'audio_filename': 'Akohou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb9'),
            'french': 'escargot',
            'audio_path': 'audio/animaux/Ancora.m4a',
            'audio_filename': 'Ancora.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd3'),
            'french': 'cheval',
            'audio_path': 'audio/animaux/Poundra.m4a',
            'audio_filename': 'Poundra.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbe'),
            'french': 'poisson',
            'audio_path': 'audio/animaux/Lokou.m4a',
            'audio_filename': 'Lokou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd0'),
            'french': 'papillon',
            'audio_path': 'audio/animaux/Tsipelapelaka.m4a',
            'audio_filename': 'Tsipelapelaka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec838887e'),
            'french': 'lourd',
            'audio_path': 'audio/animaux/Ndzi.m4a',
            'audio_filename': 'Ndzi.m4a',
            'category': 'animaux',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcc'),
            'french': 'poule',
            'audio_path': 'audio/animaux/Kouhou.m4a',
            'audio_filename': 'Kouhou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be4'),
            'french': 'renard',
            'audio_path': 'audio/animaux/Fandroka.m4a',
            'audio_filename': 'Fandroka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc9'),
            'french': 'caméléon',
            'audio_path': 'audio/animaux/Tarundru.m4a',
            'audio_filename': 'Tarundru.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdc'),
            'french': 'crabe',
            'audio_path': 'audio/animaux/Dradraka.m4a',
            'audio_filename': 'Dradraka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd9'),
            'french': 'thon',
            'audio_path': 'audio/animaux/Mbassi.m4a',
            'audio_filename': 'Mbassi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/animaux/Howou.m4a',
            'audio_filename': 'Howou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb4'),
            'french': 'cochon',
            'audio_path': 'audio/animaux/Pouroukou.m4a',
            'audio_filename': 'Pouroukou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bec'),
            'french': 'frelon',
            'audio_path': 'audio/animaux/Faraka.m4a',
            'audio_filename': 'Faraka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bca'),
            'french': 'zébu',
            'audio_path': 'audio/animaux/Madjaoumbi.m4a',
            'audio_filename': 'Madjaoumbi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc5'),
            'french': 'lapin',
            'audio_path': 'audio/animaux/Shoungoura.m4a',
            'audio_filename': 'Shoungoura.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd1'),
            'french': 'ver de terre',
            'audio_path': 'audio/animaux/Lingoui lingoui.m4a',
            'audio_filename': 'Lingoui lingoui.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bef'),
            'french': 'puce',
            'audio_path': 'audio/animaux/Ancongou.m4a',
            'audio_filename': 'Ancongou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdc'),
            'french': 'crabe',
            'audio_path': 'audio/animaux/Dakatra.m4a',
            'audio_filename': 'Dakatra.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf2'),
            'french': 'taureau',
            'audio_path': 'audio/animaux/Kondzo.m4a',
            'audio_filename': 'Kondzo.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd4'),
            'french': 'perroquet',
            'audio_path': 'audio/animaux/Kassoukou.m4a',
            'audio_filename': 'Kassoukou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bce'),
            'french': 'fourmis',
            'audio_path': 'audio/animaux/Tsoussou.m4a',
            'audio_filename': 'Tsoussou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdb'),
            'french': 'poulpe',
            'audio_path': 'audio/animaux/Pwedza.m4a',
            'audio_filename': 'Pwedza.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc4'),
            'french': 'serpent',
            'audio_path': 'audio/animaux/Bibi lava.m4a',
            'audio_filename': 'Bibi lava.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcb'),
            'french': 'âne',
            'audio_path': 'audio/animaux/Ndra.m4a',
            'audio_filename': 'Ndra.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be8'),
            'french': 'civette',
            'audio_path': 'audio/animaux/Founga.m4a',
            'audio_filename': 'Founga.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd6'),
            'french': 'araignée',
            'audio_path': 'audio/animaux/Bibi ampamani massou.m4a',
            'audio_filename': 'Bibi ampamani massou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd0'),
            'french': 'papillon',
            'audio_path': 'audio/animaux/Pelapelaka.m4a',
            'audio_filename': 'Pelapelaka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf4'),
            'french': 'lambis',
            'audio_path': 'audio/animaux/Kombé.m4a',
            'audio_filename': 'Kombé.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bea'),
            'french': 'baleine',
            'audio_path': 'audio/animaux/Ndroujou.m4a',
            'audio_filename': 'Ndroujou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bed'),
            'french': 'guêpe',
            'audio_path': 'audio/animaux/Movou.m4a',
            'audio_filename': 'Movou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be6'),
            'french': 'hérisson',
            'audio_path': 'audio/animaux/Landra.m4a',
            'audio_filename': 'Landra.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc8'),
            'french': 'crocodile',
            'audio_path': 'audio/animaux/Vwai k.m4a',
            'audio_filename': 'Vwai k.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bce'),
            'french': 'fourmis',
            'audio_path': 'audio/animaux/Vitsiki.m4a',
            'audio_filename': 'Vitsiki.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbd'),
            'french': 'chien',
            'audio_path': 'audio/animaux/Mbwa nyeha.m4a',
            'audio_filename': 'Mbwa nyeha.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbd'),
            'french': 'chien',
            'audio_path': 'audio/animaux/Mbwa.m4a',
            'audio_filename': 'Mbwa.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc2'),
            'french': 'mouche',
            'audio_path': 'audio/animaux/Lalitri.m4a',
            'audio_filename': 'Lalitri.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bda'),
            'french': 'requin',
            'audio_path': 'audio/animaux/Papa.m4a',
            'audio_filename': 'Papa.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcb'),
            'french': 'âne',
            'audio_path': 'audio/animaux/Ampundra.m4a',
            'audio_filename': 'Ampundra.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd4'),
            'french': 'perroquet',
            'audio_path': 'audio/animaux/Kararokou.m4a',
            'audio_filename': 'Kararokou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b89'),
            'french': 'jacquier',
            'audio_path': 'audio/animaux/Fénéssi.m4a',
            'audio_filename': 'Fénéssi.m4a',
            'category': 'animaux',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd2'),
            'french': 'criquet',
            'audio_path': 'audio/animaux/Furudji.m4a',
            'audio_filename': 'Furudji.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be7'),
            'french': 'corbeau',
            'audio_path': 'audio/animaux/Gawa_kwayi.m4a',
            'audio_filename': 'Gawa_kwayi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf1'),
            'french': 'bouc',
            'audio_path': 'audio/animaux/Bébérou.m4a',
            'audio_filename': 'Bébérou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb5'),
            'french': 'margouillat',
            'audio_path': 'audio/animaux/Kasangwe.m4a',
            'audio_filename': 'Kasangwe.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be8'),
            'french': 'civette',
            'audio_path': 'audio/animaux/Angava.m4a',
            'audio_filename': 'Angava.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd3'),
            'french': 'cheval',
            'audio_path': 'audio/animaux/Farassi.m4a',
            'audio_filename': 'Farassi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf8'),
            'french': 'huître',
            'audio_path': 'audio/animaux/Sadza.m4a',
            'audio_filename': 'Sadza.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc1'),
            'french': 'moustique',
            'audio_path': 'audio/animaux/Mokou.m4a',
            'audio_filename': 'Mokou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bef'),
            'french': 'puce',
            'audio_path': 'audio/animaux/Kunguni.m4a',
            'audio_filename': 'Kunguni.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be0'),
            'french': 'singe',
            'audio_path': 'audio/animaux/Djakouayi.m4a',
            'audio_filename': 'Djakouayi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd1'),
            'french': 'ver de terre',
            'audio_path': 'audio/animaux/Bibi fotaka.m4a',
            'audio_filename': 'Bibi fotaka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be5'),
            'french': 'chameau',
            'audio_path': 'audio/animaux/Angamia.m4a',
            'audio_filename': 'Angamia.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd3'),
            'french': 'cheval',
            'audio_path': 'audio/animaux/Poundra(1).m4a',
            'audio_filename': 'Poundra(1).m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcf'),
            'french': 'chenille',
            'audio_path': 'audio/animaux/Bazi.m4a',
            'audio_filename': 'Bazi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc0'),
            'french': 'chèvre',
            'audio_path': 'audio/animaux/Mbouzi.m4a',
            'audio_filename': 'Mbouzi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/animaux/Strandrabwibwi.m4a',
            'audio_filename': 'Strandrabwibwi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc9'),
            'french': 'caméléon',
            'audio_path': 'audio/animaux/Tarondru.m4a',
            'audio_filename': 'Tarondru.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bca'),
            'french': 'zébu',
            'audio_path': 'audio/animaux/Nyombé.m4a',
            'audio_filename': 'Nyombé.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbc'),
            'french': 'oiseau',
            'audio_path': 'audio/animaux/Vorougnou.m4a',
            'audio_filename': 'Vorougnou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc3'),
            'french': 'chauve-souris',
            'audio_path': 'audio/animaux/Fanihi.m4a',
            'audio_filename': 'Fanihi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bda'),
            'french': 'requin',
            'audio_path': 'audio/animaux/Ankiou.m4a',
            'audio_filename': 'Ankiou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf1'),
            'french': 'bouc',
            'audio_path': 'audio/animaux/Béwé.m4a',
            'audio_filename': 'Béwé.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdd'),
            'french': 'tortue',
            'audio_path': 'audio/animaux/Fanou.m4a',
            'audio_filename': 'Fanou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be7'),
            'french': 'corbeau',
            'audio_path': 'audio/animaux/Gawa-kwayi.m4a',
            'audio_filename': 'Gawa-kwayi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf4'),
            'french': 'lambis',
            'audio_path': 'audio/animaux/Mahombi.m4a',
            'audio_filename': 'Mahombi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bdd'),
            'french': 'tortue',
            'audio_path': 'audio/animaux/Nyamba_katsa.m4a',
            'audio_filename': 'Nyamba_katsa.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd7'),
            'french': 'scorpion',
            'audio_path': 'audio/animaux/Hala.m4a',
            'audio_filename': 'Hala.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bed'),
            'french': 'guêpe',
            'audio_path': 'audio/animaux/Fanintri.m4a',
            'audio_filename': 'Fanintri.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be9'),
            'french': 'dauphin',
            'audio_path': 'audio/animaux/Moungoumé.m4a',
            'audio_filename': 'Moungoumé.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf7'),
            'french': 'oursin',
            'audio_path': 'audio/animaux/Gadzassi.m4a',
            'audio_filename': 'Gadzassi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf6'),
            'french': 'mille-pattes',
            'audio_path': 'audio/animaux/Mjongo.m4a',
            'audio_filename': 'Mjongo.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbe'),
            'french': 'poisson',
            'audio_path': 'audio/animaux/Fi.m4a',
            'audio_filename': 'Fi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b89'),
            'french': 'jacquier',
            'audio_path': 'audio/animaux/Finéssi.m4a',
            'audio_filename': 'Finéssi.m4a',
            'category': 'animaux',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be1'),
            'french': 'souris',
            'audio_path': 'audio/animaux/Shikwetse.m4a',
            'audio_filename': 'Shikwetse.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd8'),
            'french': 'scolopendre',
            'audio_path': 'audio/animaux/Trambwi.m4a',
            'audio_filename': 'Trambwi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb7'),
            'french': 'chat',
            'audio_path': 'audio/animaux/Paha.m4a',
            'audio_filename': 'Paha.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be3'),
            'french': 'lézard',
            'audio_path': 'audio/animaux/Ngwizi.m4a',
            'audio_filename': 'Ngwizi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcb'),
            'french': 'âne',
            'audio_path': 'audio/animaux/Pundra.m4a',
            'audio_filename': 'Pundra.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb7'),
            'french': 'chat',
            'audio_path': 'audio/animaux/Moirou.m4a',
            'audio_filename': 'Moirou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc3'),
            'french': 'chauve-souris',
            'audio_path': 'audio/animaux/Drema.m4a',
            'audio_filename': 'Drema.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb8'),
            'french': 'rat',
            'audio_path': 'audio/animaux/Pouhou.m4a',
            'audio_filename': 'Pouhou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388888'),
            'french': 'faux',
            'audio_path': 'audio/animaux/Trambougnou.m4a',
            'audio_filename': 'Trambougnou.m4a',
            'category': 'animaux',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb9'),
            'french': 'escargot',
            'audio_path': 'audio/animaux/Kwa.m4a',
            'audio_filename': 'Kwa.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bcf'),
            'french': 'chenille',
            'audio_path': 'audio/animaux/Bibimanguidi.m4a',
            'audio_filename': 'Bibimanguidi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc0'),
            'french': 'chèvre',
            'audio_path': 'audio/animaux/Bengui.m4a',
            'audio_filename': 'Bengui.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bee'),
            'french': 'bourdon',
            'audio_path': 'audio/animaux/Vungo vungo.m4a',
            'audio_filename': 'Vungo vungo.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc7'),
            'french': 'mouton',
            'audio_path': 'audio/animaux/Baribari.m4a',
            'audio_filename': 'Baribari.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbf'),
            'french': 'maki',
            'audio_path': 'audio/animaux/Komba.m4a',
            'audio_filename': 'Komba.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be5'),
            'french': 'chameau',
            'audio_path': 'audio/animaux/Ngamia.m4a',
            'audio_filename': 'Ngamia.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bde'),
            'french': 'bigorno',
            'audio_path': 'audio/animaux/Trondrou.m4a',
            'audio_filename': 'Trondrou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79beb'),
            'french': 'crevette',
            'audio_path': 'audio/animaux/Camba.m4a',
            'audio_filename': 'Camba.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bba'),
            'french': 'lion',
            'audio_path': 'audio/animaux/Simba.m4a',
            'audio_filename': 'Simba.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc8'),
            'french': 'crocodile',
            'audio_path': 'audio/animaux/Vwai s.m4a',
            'audio_filename': 'Vwai s.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc1'),
            'french': 'moustique',
            'audio_path': 'audio/animaux/Manundri.m4a',
            'audio_filename': 'Manundri.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be9'),
            'french': 'dauphin',
            'audio_path': 'audio/animaux/Fésoutrou.m4a',
            'audio_filename': 'Fésoutrou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bec'),
            'french': 'frelon',
            'audio_path': 'audio/animaux/Chonga.m4a',
            'audio_filename': 'Chonga.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79beb'),
            'french': 'crevette',
            'audio_path': 'audio/animaux/Ancamba.m4a',
            'audio_filename': 'Ancamba.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be6'),
            'french': 'hérisson',
            'audio_path': 'audio/animaux/Trandraka.m4a',
            'audio_filename': 'Trandraka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd5'),
            'french': 'cafard',
            'audio_path': 'audio/animaux/Kalalawi.m4a',
            'audio_filename': 'Kalalawi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d53a01973c2afec8388881'),
            'french': 'sale',
            'audio_path': 'audio/animaux/Shiwatrotro.m4a',
            'audio_filename': 'Shiwatrotro.m4a',
            'category': 'animaux',
            'section': 'adjectifs'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb4'),
            'french': 'cochon',
            'audio_path': 'audio/animaux/Lambou.m4a',
            'audio_filename': 'Lambou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb6'),
            'french': 'abeille',
            'audio_path': 'audio/animaux/Antéli.m4a',
            'audio_filename': 'Antéli.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc6'),
            'french': 'canard',
            'audio_path': 'audio/animaux/Doukitri.m4a',
            'audio_filename': 'Doukitri.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbb'),
            'french': 'grenouille',
            'audio_path': 'audio/animaux/Sahougnou.m4a',
            'audio_filename': 'Sahougnou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf2'),
            'french': 'taureau',
            'audio_path': 'audio/animaux/Dzow.m4a',
            'audio_filename': 'Dzow.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bca'),
            'french': 'zébu',
            'audio_path': 'audio/animaux/Aoumbi.m4a',
            'audio_filename': 'Aoumbi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bde'),
            'french': 'bigorno',
            'audio_path': 'audio/animaux/Trondro.m4a',
            'audio_filename': 'Trondro.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd2'),
            'french': 'criquet',
            'audio_path': 'audio/animaux/Kidzedza.m4a',
            'audio_filename': 'Kidzedza.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf7'),
            'french': 'oursin',
            'audio_path': 'audio/animaux/Vouli vavi.m4a',
            'audio_filename': 'Vouli vavi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf5'),
            'french': 'cône de mer',
            'audio_path': 'audio/animaux/Kwitsi.m4a',
            'audio_filename': 'Kwitsi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf6'),
            'french': 'mille-pattes',
            'audio_path': 'audio/animaux/Ancoudavitri.m4a',
            'audio_filename': 'Ancoudavitri.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be7'),
            'french': 'corbeau',
            'audio_path': 'audio/animaux/Gouaka.m4a',
            'audio_filename': 'Gouaka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc4'),
            'french': 'serpent',
            'audio_path': 'audio/animaux/Nyoha.m4a',
            'audio_filename': 'Nyoha.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd5'),
            'french': 'cafard',
            'audio_path': 'audio/animaux/Kalalowou.m4a',
            'audio_filename': 'Kalalowou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb5'),
            'french': 'margouillat',
            'audio_path': 'audio/animaux/Kitsatsaka.m4a',
            'audio_filename': 'Kitsatsaka.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb8'),
            'french': 'rat',
            'audio_path': 'audio/animaux/Voilavou.m4a',
            'audio_filename': 'Voilavou.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc6'),
            'french': 'canard',
            'audio_path': 'audio/animaux/Guisi.m4a',
            'audio_filename': 'Guisi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bbc'),
            'french': 'oiseau',
            'audio_path': 'audio/animaux/Gnougni.m4a',
            'audio_filename': 'Gnougni.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bc5'),
            'french': 'lapin',
            'audio_path': 'audio/animaux/Sungura.m4a',
            'audio_filename': 'Sungura.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be2'),
            'french': 'phacochère',
            'audio_path': 'audio/animaux/Pouruku nyeha.m4a',
            'audio_filename': 'Pouruku nyeha.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79be0'),
            'french': 'singe',
            'audio_path': 'audio/animaux/Djakwe.m4a',
            'audio_filename': 'Djakwe.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb6'),
            'french': 'abeille',
            'audio_path': 'audio/animaux/Niochi.m4a',
            'audio_filename': 'Niochi.m4a',
            'category': 'animaux',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b98'),
            'french': 'un',
            'audio_path': 'audio/nombres/Areki.m4a',
            'audio_filename': 'Areki.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9f'),
            'french': 'huit',
            'audio_path': 'audio/nombres/Valou.m4a',
            'audio_filename': 'Valou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b98'),
            'french': 'un',
            'audio_path': 'audio/nombres/Moja.m4a',
            'audio_filename': 'Moja.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba1'),
            'french': 'dix',
            'audio_path': 'audio/nombres/Foulou.m4a',
            'audio_filename': 'Foulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b98'),
            'french': 'un',
            'audio_path': 'audio/nombres/Foulou areki ambi.m4a',
            'audio_filename': 'Foulou areki ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b99'),
            'french': 'deux',
            'audio_path': 'audio/nombres/Koumi na mbili.m4a',
            'audio_filename': 'Koumi na mbili.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bad'),
            'french': 'quarante',
            'audio_path': 'audio/nombres/Efampoulou.m4a',
            'audio_filename': 'Efampoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9a'),
            'french': 'trois',
            'audio_path': 'audio/nombres/Téloumpoulou.m4a',
            'audio_filename': 'Téloumpoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9f'),
            'french': 'huit',
            'audio_path': 'audio/nombres/Valoumpoulou.m4a',
            'audio_filename': 'Valoumpoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9a'),
            'french': 'trois',
            'audio_path': 'audio/nombres/Koumi na trarou.m4a',
            'audio_filename': 'Koumi na trarou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9f'),
            'french': 'huit',
            'audio_path': 'audio/nombres/Foulou valou ambi.m4a',
            'audio_filename': 'Foulou valou ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd7'),
            'french': 'scorpion',
            'audio_path': 'audio/nombres/Thalathini.m4a',
            'audio_filename': 'Thalathini.m4a',
            'category': 'nombres',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9b'),
            'french': 'quatre',
            'audio_path': 'audio/nombres/Efatra.m4a',
            'audio_filename': 'Efatra.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/nombres/Chendra.m4a',
            'audio_filename': 'Chendra.m4a',
            'category': 'nombres',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bf0'),
            'french': 'poux',
            'audio_path': 'audio/nombres/Koumi na chendra.m4a',
            'audio_filename': 'Koumi na chendra.m4a',
            'category': 'nombres',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9a'),
            'french': 'trois',
            'audio_path': 'audio/nombres/Trarou.m4a',
            'audio_filename': 'Trarou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9e'),
            'french': 'sept',
            'audio_path': 'audio/nombres/Fitoumpoulou.m4a',
            'audio_filename': 'Fitoumpoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bae'),
            'french': 'cinquante',
            'audio_path': 'audio/nombres/Hamssini.m4a',
            'audio_filename': 'Hamssini.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba1'),
            'french': 'dix',
            'audio_path': 'audio/nombres/Foulou(1).m4a',
            'audio_filename': 'Foulou(1).m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9e'),
            'french': 'sept',
            'audio_path': 'audio/nombres/Saba.m4a',
            'audio_filename': 'Saba.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba1'),
            'french': 'dix',
            'audio_path': 'audio/nombres/Koumi.m4a',
            'audio_filename': 'Koumi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b98'),
            'french': 'un',
            'audio_path': 'audio/nombres/Koumi na moja.m4a',
            'audio_filename': 'Koumi na moja.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9f'),
            'french': 'huit',
            'audio_path': 'audio/nombres/Koumi na nané.m4a',
            'audio_filename': 'Koumi na nané.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9d'),
            'french': 'six',
            'audio_path': 'audio/nombres/Koumi na sita.m4a',
            'audio_filename': 'Koumi na sita.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba0'),
            'french': 'neuf',
            'audio_path': 'audio/nombres/Foulou civi ambi.m4a',
            'audio_filename': 'Foulou civi ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9b'),
            'french': 'quatre',
            'audio_path': 'audio/nombres/Nhé.m4a',
            'audio_filename': 'Nhé.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9b'),
            'french': 'quatre',
            'audio_path': 'audio/nombres/Foulou efatra ambi.m4a',
            'audio_filename': 'Foulou efatra ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9c'),
            'french': 'cinq',
            'audio_path': 'audio/nombres/Foulou dimi ambi.m4a',
            'audio_filename': 'Foulou dimi ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bad'),
            'french': 'quarante',
            'audio_path': 'audio/nombres/Arbahini.m4a',
            'audio_filename': 'Arbahini.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb3'),
            'french': 'cent',
            'audio_path': 'audio/nombres/Zatou.m4a',
            'audio_filename': 'Zatou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb3'),
            'french': 'cent',
            'audio_path': 'audio/nombres/Miya.m4a',
            'audio_filename': 'Miya.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9e'),
            'french': 'sept',
            'audio_path': 'audio/nombres/Koumi na saba.m4a',
            'audio_filename': 'Koumi na saba.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9d'),
            'french': 'six',
            'audio_path': 'audio/nombres/Foulou tchouta ambi.m4a',
            'audio_filename': 'Foulou tchouta ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b99'),
            'french': 'deux',
            'audio_path': 'audio/nombres/Aroyi.m4a',
            'audio_filename': 'Aroyi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9a'),
            'french': 'trois',
            'audio_path': 'audio/nombres/Telou.m4a',
            'audio_filename': 'Telou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9c'),
            'french': 'cinq',
            'audio_path': 'audio/nombres/Koumi na tsano.m4a',
            'audio_filename': 'Koumi na tsano.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9c'),
            'french': 'cinq',
            'audio_path': 'audio/nombres/Dimimpoulou.m4a',
            'audio_filename': 'Dimimpoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb2'),
            'french': 'quatre-vingt-dix',
            'audio_path': 'audio/nombres/Toussuini.m4a',
            'audio_filename': 'Toussuini.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bb1'),
            'french': 'quatre-vingts',
            'audio_path': 'audio/nombres/Thamanini.m4a',
            'audio_filename': 'Thamanini.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9c'),
            'french': 'cinq',
            'audio_path': 'audio/nombres/Tsano.m4a',
            'audio_filename': 'Tsano.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bab'),
            'french': 'vingt',
            'audio_path': 'audio/nombres/Arompoulou.m4a',
            'audio_filename': 'Arompoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9e'),
            'french': 'sept',
            'audio_path': 'audio/nombres/Foulou fitou ambi.m4a',
            'audio_filename': 'Foulou fitou ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9c'),
            'french': 'cinq',
            'audio_path': 'audio/nombres/Dimi.m4a',
            'audio_filename': 'Dimi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9a'),
            'french': 'trois',
            'audio_path': 'audio/nombres/Foulou telou ambi.m4a',
            'audio_filename': 'Foulou telou ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9f'),
            'french': 'huit',
            'audio_path': 'audio/nombres/Nané.m4a',
            'audio_filename': 'Nané.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9e'),
            'french': 'sept',
            'audio_path': 'audio/nombres/Fitou.m4a',
            'audio_filename': 'Fitou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9d'),
            'french': 'six',
            'audio_path': 'audio/nombres/Tchouta.m4a',
            'audio_filename': 'Tchouta.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9d'),
            'french': 'six',
            'audio_path': 'audio/nombres/Sita.m4a',
            'audio_filename': 'Sita.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b9d'),
            'french': 'six',
            'audio_path': 'audio/nombres/Tchoutampoulou.m4a',
            'audio_filename': 'Tchoutampoulou.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b99'),
            'french': 'deux',
            'audio_path': 'audio/nombres/Foulou aroyi ambi.m4a',
            'audio_filename': 'Foulou aroyi ambi.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79ba1'),
            'french': 'dix',
            'audio_path': 'audio/nombres/Koumi na nhé.m4a',
            'audio_filename': 'Koumi na nhé.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79c78'),
            'french': 'chaise',
            'audio_path': 'audio/nombres/Chirini.m4a',
            'audio_filename': 'Chirini.m4a',
            'category': 'nombres',
            'section': 'maison'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79baf'),
            'french': 'soixante',
            'audio_path': 'audio/nombres/Sitini.m4a',
            'audio_filename': 'Sitini.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b99'),
            'french': 'deux',
            'audio_path': 'audio/nombres/Mbili.m4a',
            'audio_filename': 'Mbili.m4a',
            'category': 'nombres',
            'section': 'nombres'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf3'),
            'french': 'bicyclette',
            'audio_path': 'audio/transport/Bicycléti.m4a',
            'audio_filename': 'Bicycléti.m4a',
            'category': 'transport',
            'section': 'transport'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b95'),
            'french': 'vedette',
            'audio_path': 'audio/transport/Kwassa kwassa.m4a',
            'audio_filename': 'Kwassa kwassa.m4a',
            'category': 'transport',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cfa'),
            'french': 'avion',
            'audio_path': 'audio/transport/Roplani.m4a',
            'audio_filename': 'Roplani.m4a',
            'category': 'transport',
            'section': 'transport'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b95'),
            'french': 'vedette',
            'audio_path': 'audio/transport/Vidéti.m4a',
            'audio_filename': 'Vidéti.m4a',
            'category': 'transport',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf8'),
            'french': 'moto',
            'audio_path': 'audio/transport/Monto.m4a',
            'audio_filename': 'Monto.m4a',
            'category': 'transport',
            'section': 'transport'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79b94'),
            'french': 'pirogue',
            'audio_path': 'audio/transport/Lakana.m4a',
            'audio_filename': 'Lakana.m4a',
            'category': 'transport',
            'section': 'nature'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79bd0'),
            'french': 'papillon',
            'audio_path': 'audio/transport/Laka.m4a',
            'audio_filename': 'Laka.m4a',
            'category': 'transport',
            'section': 'animaux'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cfb'),
            'french': 'taxi',
            'audio_path': 'audio/transport/Taxi.m4a',
            'audio_filename': 'Taxi.m4a',
            'category': 'transport',
            'section': 'transport'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf7'),
            'french': 'bateau',
            'audio_path': 'audio/transport/Markabou.m4a',
            'audio_filename': 'Markabou.m4a',
            'category': 'transport',
            'section': 'transport'
        },
        {
            'word_id': ObjectId('68d52eff53dfba3e80a79cf9'),
            'french': 'camion',
            'audio_path': 'audio/transport/Ndrégué.m4a',
            'audio_filename': 'Ndrégué.m4a',
            'category': 'transport',
            'section': 'transport'
        },
    ]
    
    logger.info(f"Application de {len(correspondences)} correspondences...")
    
    updated_count = 0
    for corr in correspondences:
        # Déterminer si c'est shimaoré ou kibouchi selon le nom du fichier
        filename_lower = corr['audio_filename'].lower()
        
        # Mise à jour avec le nouveau système audio authentique
        result = collection.update_one(
            {"_id": corr['word_id']},
            {
                "$set": {
                    "audio_authentic": corr['audio_path'],
                    "has_authentic_audio": True,
                    "audio_format": "m4a",
                    "auto_matched": True,
                    "audio_updated_at": "{}".replace('{}', str(__import__('datetime').datetime.now()))
                }
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
            logger.info(f"✅ {corr['french']} → {corr['audio_path']}")
        else:
            logger.warning(f"❌ Échec mise à jour: {corr['french']}")
    
    logger.info(f"Mises à jour appliquées: {updated_count}/{len(correspondences)}")
    return updated_count

if __name__ == "__main__":
    apply_audio_correspondences()
