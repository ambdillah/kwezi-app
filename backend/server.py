import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import conjugation engine for sentence generation
from conjugation_engine import create_sentence_database

# Import database protection system
from database_protection import protect_database, db_protector, check_database_integrity

app = FastAPI(title="Mayotte Language Learning API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
# Use the correct database name from environment variable
DB_NAME = os.getenv("DB_NAME", "shimaoré_app")
db = client[DB_NAME]

# Collections
words_collection = db.words
exercises_collection = db.exercises
user_progress_collection = db.user_progress
sentences_collection = db.sentences
users_collection = db.users

# Debug: Test database connection
try:
    print(f"Connected to database: {DB_NAME}")
    print(f"Collections: {db.list_collection_names()}")
    count = words_collection.count_documents({})
    print(f"Total words in collection: {count}")
except Exception as e:
    print(f"Database connection error: {e}")

# Pydantic models
class Word(BaseModel):
    id: Optional[str] = None
    french: str
    shimaore: str
    kibouchi: str
    category: str  # famille, couleurs, animaux, salutations, nombres
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=3)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Anciens champs audio authentiques (maintenant compatibilité)
    audio_filename: Optional[str] = None
    audio_pronunciation_lang: Optional[str] = None
    audio_note: Optional[str] = None
    audio_source: Optional[str] = None
    has_authentic_audio: Optional[bool] = False
    audio_updated_at: Optional[datetime] = None
    # Nouveaux champs audio duaux - Système restructuré
    shimoare_audio_filename: Optional[str] = None
    kibouchi_audio_filename: Optional[str] = None
    shimoare_has_audio: Optional[bool] = False
    kibouchi_has_audio: Optional[bool] = False
    dual_audio_system: Optional[bool] = False
    audio_restructured_at: Optional[datetime] = None

class WordCreate(BaseModel):
    french: str
    shimaore: str
    kibouchi: str
    category: str
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=3)

class Exercise(BaseModel):
    id: Optional[str] = None
    type: str  # "match_word_image", "quiz", "memory"
    content: dict
    difficulty: int = Field(default=1, ge=1, le=3)
    points: int = 10
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserProgress(BaseModel):
    id: Optional[str] = None
    user_name: str
    exercise_id: str
    score: int
    completed_at: datetime = Field(default_factory=datetime.utcnow)

# Modèles pour le système premium
class User(BaseModel):
    id: Optional[str] = None
    user_id: str  # Identifiant unique généré côté client
    email: Optional[str] = None
    is_premium: bool = False
    premium_expires_at: Optional[datetime] = None
    subscription_type: Optional[str] = None  # "monthly", "yearly"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    words_learned: int = 0
    total_score: int = 0
    streak_days: int = 0
    last_activity_date: Optional[datetime] = None

class UserCreate(BaseModel):
    user_id: str
    email: Optional[str] = None

class UpgradeRequest(BaseModel):
    user_id: str
    subscription_type: str = "monthly"  # "monthly" ou "yearly"

def dict_to_word(word_dict):
    """Convert MongoDB document to Word model"""
    if '_id' in word_dict:
        word_dict['id'] = str(word_dict['_id'])
        del word_dict['_id']
    return Word(**word_dict)

def dict_to_exercise(exercise_dict):
    """Convert MongoDB document to Exercise model"""
    if '_id' in exercise_dict:
        exercise_dict['id'] = str(exercise_dict['_id'])
        del exercise_dict['_id']
    return Exercise(**exercise_dict)

@app.get("/")
async def root():
    return {"message": "Mayotte Language Learning API", "status": "running"}

@app.get("/test-audio")
async def test_audio_page():
    """Page de test des audios authentiques"""
    from fastapi.responses import FileResponse
    return FileResponse("/app/backend/test_audio.html")

@app.get("/api/vocabulary")
async def get_vocabulary(section: str = Query(None, description="Filter by section")):
    """Get vocabulary by section"""
    try:
        # Build query based on section parameter
        query = {}
        if section:
            query["section"] = section
        
        # Execute query
        cursor = words_collection.find(query)
        words = []
        for word_doc in cursor:
            # Convert MongoDB document to dictionary
            word_dict = dict(word_doc)
            if '_id' in word_dict:
                word_dict['id'] = str(word_dict['_id'])
                del word_dict['_id']
            words.append(word_dict)
        
        return words
    except Exception as e:
        print(f"Error in get_vocabulary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vocabulary/sections")
async def get_vocabulary_sections():
    """Get all available vocabulary sections"""
    try:
        # Get distinct sections from the vocabulary collection
        sections = words_collection.distinct("section")
        return {"sections": sections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vocabulary/{word_id}")
async def get_word(word_id: str):
    """Get a specific word by ID"""
    try:
        word_doc = words_collection.find_one({"_id": ObjectId(word_id)})
        if not word_doc:
            raise HTTPException(status_code=404, detail="Word not found")
        
        # Convert to dict and replace _id
        word_dict = dict(word_doc)
        word_dict['id'] = str(word_dict['_id'])
        del word_dict['_id']
        
        return word_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/words")
async def get_words(category: str = Query(None, description="Filter by category")):
    """Get words (compatible with frontend expectations)"""
    try:
        # Build query based on category parameter
        query = {}
        if category:
            query["category"] = category
        
        # Execute query
        cursor = words_collection.find(query)
        words = []
        for word_doc in cursor:
            # Convert MongoDB document to dictionary
            word_dict = dict(word_doc)
            if '_id' in word_dict:
                word_dict['id'] = str(word_dict['_id'])
                del word_dict['_id']
            
            words.append(word_dict)
        
        return words
    except Exception as e:
        print(f"Error in get_words: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audio/{section}/{filename}")
async def get_audio(section: str, filename: str):
    """Serve audio files from assets/audio directory"""
    try:
        from fastapi.responses import FileResponse
        import os
        
        # Construct the file path
        audio_path = f"/app/frontend/assets/audio/{section}/{filename}"
        
        # Check if file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail=f"Audio file not found: {filename}")
        
        # Return the file
        return FileResponse(
            path=audio_path,
            media_type="audio/m4a",
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/init-base-content")
async def init_base_content():
    """Initialize the database with base vocabulary and exercises"""
    
    # CRITICAL: Commented out destructive operations to prevent data loss
    # Clear existing data
    # words_collection.delete_many({})  # DISABLED - CAUSES DATA LOSS
    # exercises_collection.delete_many({})  # DISABLED - CAUSES DATA LOSS
    
    # Base vocabulary avec traductions authentiques de Mayotte
    base_words = [
        # Salutations (8 mots)
        {"french": "Au revoir", "shimaore": "Djalabé", "kibouchi": "Djalabé", "category": "salutations", "image_url": "👋", "difficulty": 1},
        {"french": "Bonjour", "shimaore": "Kwezi", "kibouchi": "Kwezi", "category": "salutations", "image_url": "☀️", "difficulty": 1},
        {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori", "category": "salutations", "image_url": "❓", "difficulty": 1},
        {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara", "category": "salutations", "image_url": "😊", "difficulty": 1},
        {"french": "Oui", "shimaore": "Ewa", "kibouchi": "Iya", "category": "salutations", "image_url": "✅", "difficulty": 1},
        {"french": "Non", "shimaore": "Anha", "kibouchi": "Anha", "category": "salutations", "image_url": "❌", "difficulty": 1},
        {"french": "Excuse-moi", "shimaore": "Soimahani", "kibouchi": "Soimahani", "category": "salutations", "image_url": "🙏", "difficulty": 1},
        {"french": "Merci", "shimaore": "Marahaba", "kibouchi": "Misara", "category": "salutations", "image_url": "🙏", "difficulty": 1},

        # Famille (21 mots) - avec correction Maman et mot Famille ajouté
        {"french": "Enfant", "shimaore": "Mwana", "kibouchi": "Zaza", "category": "famille", "image_url": "👶", "difficulty": 1},
        {"french": "Famille", "shimaore": "Mdjamaza", "kibouchi": "Havagna", "category": "famille", "image_url": "👨‍👩‍👧‍👦", "difficulty": 1},
        {"french": "Fille", "shimaore": "Mwana mtroub", "kibouchi": "Anabavi zaza", "category": "famille", "image_url": "👧", "difficulty": 1},
        {"french": "Frère", "shimaore": "Mwanagna mtroun", "kibouchi": "Anadahi", "category": "famille", "image_url": "👦", "difficulty": 1, "audio_url": "https://example.com/audio/anadahi.m4a"},
        {"french": "Garçon", "shimaore": "Mwana mtroun", "kibouchi": "Anamalé zaza", "category": "famille", "image_url": "👦", "difficulty": 1},
        {"french": "Grand-mère", "shimaore": "Bibi", "kibouchi": "Rénéni", "category": "famille", "image_url": "👵", "difficulty": 1},
        {"french": "Grand-père", "shimaore": "Babu", "kibouchi": "Dadavé", "category": "famille", "image_url": "👴", "difficulty": 1},
        {"french": "Maman", "shimaore": "Mama", "kibouchi": "Baba", "category": "famille", "image_url": "👩", "difficulty": 1},
        {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille", "image_url": "👨", "difficulty": 1, "audio_url": "https://example.com/audio/baba_shimaore.m4a"},
        {"french": "Sœur", "shimaore": "Mwanagna mtroub", "kibouchi": "Anabavi", "category": "famille", "image_url": "👧", "difficulty": 1, "audio_url": "https://example.com/audio/anabavi.m4a"},
        {"french": "Tante", "shimaore": "Shangadja", "kibouchi": "Voulantiti", "category": "famille", "image_url": "👩", "difficulty": 2},
        {"french": "Oncle", "shimaore": "Baba mdjé", "kibouchi": "Baba héli", "category": "famille", "image_url": "👨", "difficulty": 2},
        {"french": "Cousin", "shimaore": "Mwanagna wamdjamaza", "kibouchi": "Voualantiri", "category": "famille", "image_url": "👦", "difficulty": 2},
        {"french": "Cousine", "shimaore": "Mwanagna wamdjamaza", "kibouchi": "Voualantiti", "category": "famille", "image_url": "👧", "difficulty": 2},
        {"french": "Époux", "shimaore": "Moutrou", "kibouchi": "Anamalé", "category": "famille", "image_url": "🤵", "difficulty": 2},
        {"french": "Épouse", "shimaore": "Mtroub", "kibouchi": "Anabavi", "category": "famille", "image_url": "👰", "difficulty": 2},
        {"french": "Ami", "shimaore": "Chaba", "kibouchi": "Tsi", "category": "famille", "image_url": "👫", "difficulty": 1},
        {"french": "Amie", "shimaore": "Chaba", "kibouchi": "Tsi", "category": "famille", "image_url": "👭", "difficulty": 1},
        {"french": "Voisin", "shimaore": "Djranyi", "kibouchi": "Mpiaouatagna", "category": "famille", "image_url": "🏠", "difficulty": 2},
        {"french": "Bébé", "shimaore": "Kahé", "kibouchi": "Bébé", "category": "famille", "image_url": "👶", "difficulty": 1},
        {"french": "Jumeau", "shimaore": "Mataou", "kibouchi": "Kambana", "category": "famille", "image_url": "👶👶", "difficulty": 2},

        # Couleurs (8 mots)
        {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs", "image_url": "⚪", "difficulty": 1},
        {"french": "Bleu", "shimaore": "🔵", "kibouchi": "Bilé", "category": "couleurs", "image_url": "🔵", "difficulty": 1},
        {"french": "Gris", "shimaore": "Kibou", "kibouchi": "Mavou", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "couleurs", "image_url": "🟡", "difficulty": 1},
        {"french": "Marron", "shimaore": "Bouné", "kibouchi": "Haintonga", "category": "couleurs", "image_url": "🟤", "difficulty": 1},
        {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "Rouge", "shimaore": "🔴", "kibouchi": "Mena", "category": "couleurs", "image_url": "🔴", "difficulty": 1},
        {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs", "image_url": "🟢", "difficulty": 1},
        {"french": "Bonjour", "shimaore": "Kwezi", "kibouchi": "Salama", "category": "salutations", "difficulty": 1},
        {"french": "Bonsoir", "shimaore": "Massimu laïmwé", "kibouchi": "Massimu", "category": "salutations", "difficulty": 1},
        {"french": "Bonne nuit", "shimaore": "Ulala hazi", "kibouchi": "Mandri soa", "category": "salutations", "difficulty": 1},
        {"french": "Au revoir", "shimaore": "Twana", "kibouchi": "Veloma", "category": "salutations", "difficulty": 1},
        {"french": "Merci", "shimaore": "Marahaba", "kibouchi": "Misaotra", "category": "salutations", "difficulty": 1},
        {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori iaou", "category": "salutations", "difficulty": 1},
        {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara", "category": "salutations", "difficulty": 1},
        {"french": "Je m'appelle", "shimaore": "Dzina yangou", "kibouchi": "Anakou hoe", "category": "salutations", "difficulty": 2},

        # Famille (vocabulaire familial étendu)
        {"french": "Ami", "shimaore": "Mwandzani", "kibouchi": "Mwandzani", "category": "famille", "difficulty": 1},
        {"french": "Enfant", "shimaore": "Mwana", "kibouchi": "Mwana", "category": "famille", "image_url": "👶", "difficulty": 1},
        {"french": "Famille", "shimaore": "Mdjamaza", "kibouchi": "Havagna", "category": "famille", "difficulty": 1},
        {"french": "Fille", "shimaore": "Mtroumama", "kibouchi": "Viavi", "category": "famille", "difficulty": 1},
        {"french": "Frère", "shimaore": "Mwanagna mtroubaba", "kibouchi": "Anadahi", "category": "famille", "audio_url": "https://customer-assets.emergentagent.com/job_mayotalk/artifacts/8n7qk8tu_Anadahi.m4a", "difficulty": 1},
        {"french": "Garçon", "shimaore": "Mtroubaba", "kibouchi": "Lalahi", "category": "famille", "difficulty": 1},
        {"french": "Grand frère", "shimaore": "Zouki", "kibouchi": "Zoki", "category": "famille", "difficulty": 1},
        {"french": "Grand-mère", "shimaore": "Coco", "kibouchi": "Dadi", "category": "famille", "difficulty": 1},
        {"french": "Grand-père", "shimaore": "Bacoco", "kibouchi": "Dadayi", "category": "famille", "difficulty": 1},
        {"french": "Grande sœur", "shimaore": "Zouki", "kibouchi": "Zoki", "category": "famille", "difficulty": 1},
        {"french": "Madame", "shimaore": "Bwéni", "kibouchi": "Viavi", "category": "famille", "difficulty": 1},
        {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", "category": "famille", "difficulty": 1},
        {"french": "Monsieur", "shimaore": "Mogné", "kibouchi": "Lalahi", "category": "famille", "difficulty": 1},
        {"french": "Oncle maternel", "shimaore": "Zama", "kibouchi": "Zama", "category": "famille", "difficulty": 2},
        {"french": "Oncle paternel", "shimaore": "Baba titi", "kibouchi": "Baba héli", "category": "famille", "audio_url": "https://customer-assets.emergentagent.com/job_mayotalk/artifacts/8n7qk8tu_Baba héli-bé.m4a", "difficulty": 2},
        {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille", "audio_url": "https://customer-assets.emergentagent.com/job_mayotalk/artifacts/8n7qk8tu_Baba s.m4a", "difficulty": 1},
        {"french": "Petit frère", "shimaore": "Moinagna mtroum", "kibouchi": "Zandri", "category": "famille", "difficulty": 1},
        {"french": "Petite sœur", "shimaore": "Moinagna mtrouba", "kibouchi": "Zandri", "category": "famille", "difficulty": 1},
        {"french": "Sœur", "shimaore": "Mwanagna", "kibouchi": "Anabavi", "category": "famille", "audio_url": "https://customer-assets.emergentagent.com/job_mayotalk/artifacts/8n7qk8tu_Anabavi.m4a", "difficulty": 1},
        {"french": "Tante", "shimaore": "Mama titi", "kibouchi": "Nindri heli", "category": "famille", "difficulty": 2},
        {"french": "Épouse oncle maternel", "shimaore": "Zena", "kibouchi": "Zena", "category": "famille", "difficulty": 2},

        # Couleurs (palette complète avec emojis)
        {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs", "image_url": "⚪", "difficulty": 1},
        {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs", "image_url": "🔵", "difficulty": 1},
        {"french": "Gris", "shimaore": "Djifou", "kibouchi": "Dzofou", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "couleurs", "image_url": "🟡", "difficulty": 1},
        {"french": "Marron", "shimaore": "Trotro", "kibouchi": "Fotafotaka", "category": "couleurs", "image_url": "🟤", "difficulty": 1},
        {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs", "image_url": "⚫", "difficulty": 1},
        {"french": "Rouge", "shimaore": "Ndzoukoundrou", "kibouchi": "Mena", "category": "couleurs", "image_url": "🔴", "difficulty": 1},
        {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs", "image_url": "🟢", "difficulty": 1},

        # Animaux (liste complète mise à jour avec emojis)
        {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Araignée", "shimaore": "Shitrandrabwibwi", "kibouchi": "Bibi amparamani massou", "category": "animaux", "image_url": "🕷️", "difficulty": 1},
        {"french": "Baleine", "shimaore": "Droujou", "kibouchi": "Fésoutrou", "category": "animaux", "image_url": "🐋", "difficulty": 2},
        {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou", "category": "animaux", "image_url": "🐚", "difficulty": 1},
        {"french": "Bouc", "shimaore": "Béwé", "kibouchi": "Bébéroué", "category": "animaux", "image_url": "🐐", "difficulty": 1},
        {"french": "Bourdon", "shimaore": "Voungo voungo", "kibouchi": "Madjaoumbi", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou", "category": "animaux", "image_url": "🪳", "difficulty": 1},
        {"french": "Caméléon", "shimaore": "Tarundru", "kibouchi": "Tarondru", "category": "animaux", "image_url": "🦎", "difficulty": 2},
        {"french": "Chameau", "shimaore": "Ngamia", "kibouchi": "Angamia", "category": "animaux", "image_url": "🐪", "difficulty": 2},
        {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "category": "animaux", "image_url": "🐱", "difficulty": 1},
        {"french": "Chauve-souris", "shimaore": "Drema", "kibouchi": "Fanihi", "category": "animaux", "image_url": "🦇", "difficulty": 1},
        {"french": "Chenille", "shimaore": "Bazi", "kibouchi": "Bibimanguidi", "category": "animaux", "image_url": "🐛", "difficulty": 1},
        {"french": "Cheval", "shimaore": "Poundra", "kibouchi": "Farassi", "category": "animaux", "image_url": "🐴", "difficulty": 1},
        {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "category": "animaux", "image_url": "🐕", "difficulty": 1},
        {"french": "Chèvre", "shimaore": "Mbouzi", "kibouchi": "Bengui", "category": "animaux", "image_url": "🐐", "difficulty": 1},
        {"french": "Civette", "shimaore": "Founga", "kibouchi": "Angava", "category": "animaux", "image_url": "🦝", "difficulty": 1},
        {"french": "Cochon", "shimaore": "Pouroukou", "kibouchi": "Lambou", "category": "animaux", "image_url": "🐷", "difficulty": 1},
        {"french": "Cône de mer", "shimaore": "Tsipoui", "kibouchi": "Tsimtipaka", "category": "animaux", "image_url": "🐚", "difficulty": 2},
        {"french": "Crabe", "shimaore": "Dradraka", "kibouchi": "Dakatra", "category": "animaux", "image_url": "🦀", "difficulty": 1},
        {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba", "category": "animaux", "image_url": "🦐", "difficulty": 1},
        {"french": "Crocodile", "shimaore": "Vwai", "kibouchi": "Vwai", "category": "animaux", "image_url": "🐊", "difficulty": 2},
        {"french": "Dauphin", "shimaore": "Camba", "kibouchi": "Fésoutrou", "category": "animaux", "image_url": "🐬", "difficulty": 2},
        {"french": "Escargot", "shimaore": "Kouéya", "kibouchi": "Ancora", "category": "animaux", "image_url": "🐌", "difficulty": 1},
        {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou", "category": "animaux", "image_url": "🐗", "difficulty": 2},
        {"french": "Fourmis", "shimaore": "Tsutsuhu", "kibouchi": "Visiki", "category": "animaux", "image_url": "🐜", "difficulty": 1},
        {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Grenouille", "shimaore": "Shiwatrotro", "kibouchi": "Sahougnou", "category": "animaux", "image_url": "🐸", "difficulty": 1},
        {"french": "Guêpe", "shimaore": "Movou", "kibouchi": "Fanintri", "category": "animaux", "image_url": "🐝", "difficulty": 1},
        {"french": "Hérisson/Tangue", "shimaore": "Landra", "kibouchi": "Trandraka", "category": "animaux", "image_url": "🦔", "difficulty": 2},
        {"french": "Lambis", "shimaore": "Komba", "kibouchi": "Mahombi", "category": "animaux", "image_url": "🐚", "difficulty": 2},
        {"french": "Lion", "shimaore": "Simba", "kibouchi": "Simba", "category": "animaux", "image_url": "🦁", "difficulty": 2},
        {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "category": "animaux", "image_url": "🦎", "difficulty": 1},
        {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba", "category": "animaux", "image_url": "🐒", "difficulty": 1},
        {"french": "Margouillat", "shimaore": "Kasangwe", "kibouchi": "Kitsatsaka", "category": "animaux", "image_url": "🦎", "difficulty": 1},
        {"french": "Mille pattes", "shimaore": "Mjongo", "kibouchi": "Ancoudavitri", "category": "animaux", "image_url": "🐛", "difficulty": 1},
        {"french": "Mouche", "shimaore": "Ndzi", "kibouchi": "Lalitri", "category": "animaux", "image_url": "🪰", "difficulty": 1},
        {"french": "Moustique", "shimaore": "Manundi", "kibouchi": "Mokou", "category": "animaux", "image_url": "🦟", "difficulty": 1},
        {"french": "Mouton", "shimaore": "Baribari", "kibouchi": "Baribari", "category": "animaux", "image_url": "🐑", "difficulty": 1},
        {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou", "category": "animaux", "image_url": "🐦", "difficulty": 1},
        {"french": "Papillon", "shimaore": "Pelapelaka", "kibouchi": "Tsipelapelaka", "category": "animaux", "image_url": "🦋", "difficulty": 1},
        {"french": "Perroquet", "shimaore": "Kasuku", "kibouchi": "Kararokou", "category": "animaux", "image_url": "🦜", "difficulty": 2},
        {"french": "Pigeon", "shimaore": "Ndiwa", "kibouchi": "Ndiwa", "category": "animaux", "image_url": "🕊️", "difficulty": 1},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "animaux", "image_url": "🐟", "difficulty": 1},
        {"french": "Poule", "shimaore": "Kouhou", "kibouchi": "Akohou", "category": "animaux", "image_url": "🐔", "difficulty": 1},
        {"french": "Poulpe", "shimaore": "Pwedza", "kibouchi": "Pwedza", "category": "animaux", "image_url": "🐙", "difficulty": 1},
        {"french": "Puce", "shimaore": "Ndra", "kibouchi": "Howou", "category": "animaux", "image_url": "🦟", "difficulty": 1},
        {"french": "Rat", "shimaore": "Pouhou", "kibouchi": "Voilavou", "category": "animaux", "image_url": "🐀", "difficulty": 1},
        {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankiou", "category": "animaux", "image_url": "🦈", "difficulty": 2},
        {"french": "Scorpion", "shimaore": "Hala", "kibouchi": "Hala", "category": "animaux", "image_url": "🦂", "difficulty": 1},
        {"french": "Scolopandre", "shimaore": "Trambwi", "kibouchi": "Trambougnou", "category": "animaux", "image_url": "🐛", "difficulty": 1},
        {"french": "Serpent", "shimaore": "Nyoha", "kibouchi": "Bibi lava", "category": "animaux", "image_url": "🐍", "difficulty": 2},
        {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi", "category": "animaux", "image_url": "🐒", "difficulty": 1},
        {"french": "Souris", "shimaore": "Shikwetse", "kibouchi": "Voilavou", "category": "animaux", "image_url": "🐭", "difficulty": 1},
        {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow", "category": "animaux", "image_url": "🐂", "difficulty": 1},
        {"french": "Tortue", "shimaore": "Nyamba", "kibouchi": "Katsa/Fanou", "category": "animaux", "image_url": "🐢", "difficulty": 1},
        {"french": "Ver de terre", "shimaore": "Lingoui lingoui", "kibouchi": "Bibi fotaka", "category": "animaux", "image_url": "🪱", "difficulty": 1},
        {"french": "Zébu", "shimaore": "Nyombe", "kibouchi": "Aoumbi", "category": "animaux", "image_url": "🐄", "difficulty": 1},
        {"french": "Âne", "shimaore": "Pundra", "kibouchi": "Ampundra", "category": "animaux", "image_url": "🫏", "difficulty": 1},
        {"french": "Éléphant", "shimaore": "Ndovu", "kibouchi": "Ndovu", "category": "animaux", "image_url": "🐘", "difficulty": 2},

        # Nombres (organisés de 1 à 20 avec emojis)
        {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "category": "nombres", "image_url": "1️⃣", "difficulty": 1},
        {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Aroyi", "category": "nombres", "image_url": "2️⃣", "difficulty": 1},
        {"french": "Trois", "shimaore": "Trarou", "kibouchi": "Telou", "category": "nombres", "image_url": "3️⃣", "difficulty": 1},
        {"french": "Quatre", "shimaore": "Nhé", "kibouchi": "Efatra", "category": "nombres", "image_url": "4️⃣", "difficulty": 1},
        {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimi", "category": "nombres", "image_url": "5️⃣", "difficulty": 1},
        {"french": "Six", "shimaore": "Sita", "kibouchi": "Tchouta", "category": "nombres", "image_url": "6️⃣", "difficulty": 1},
        {"french": "Sept", "shimaore": "Saba", "kibouchi": "Fitou", "category": "nombres", "image_url": "7️⃣", "difficulty": 1},
        {"french": "Huit", "shimaore": "Nané", "kibouchi": "Valou", "category": "nombres", "image_url": "8️⃣", "difficulty": 1},
        {"french": "Neuf", "shimaore": "Chendra", "kibouchi": "Civi", "category": "nombres", "image_url": "9️⃣", "difficulty": 1},
        {"french": "Dix", "shimaore": "Koumi", "kibouchi": "Foulou", "category": "nombres", "image_url": "🔟", "difficulty": 1},
        {"french": "Onze", "shimaore": "Koumi na moja", "kibouchi": "Foulou Areki Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Douze", "shimaore": "Koumi na mbili", "kibouchi": "Foulou Aroyi Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Treize", "shimaore": "Koumi na trarou", "kibouchi": "Foulou Telou Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Quatorze", "shimaore": "Koumi na nhé", "kibouchi": "Foulou Efatra Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Quinze", "shimaore": "Koumi na tsano", "kibouchi": "Foulou Dimi Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Seize", "shimaore": "Koumi na sita", "kibouchi": "Foulou Tchouta Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Dix-sept", "shimaore": "Koumi na saba", "kibouchi": "Foulou Fitou Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Dix-huit", "shimaore": "Koumi na nané", "kibouchi": "Foulou Valou Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Dix-neuf", "shimaore": "Koumi na chendra", "kibouchi": "Foulou Civi Ambi", "category": "nombres", "difficulty": 2},
        {"french": "Vingt", "shimaore": "Chirini", "kibouchi": "Arompoulou", "category": "nombres", "difficulty": 2},

        # Corps humain (vocabulaire corporel mis à jour avec emojis)
        {"french": "Arrière du crâne", "shimaore": "Komoi", "kibouchi": "Kitoika", "category": "corps", "difficulty": 1},
        {"french": "Barbe", "shimaore": "Ndrévou", "kibouchi": "Somboutrou", "category": "corps", "difficulty": 1},
        {"french": "Bouche", "shimaore": "Hangno", "kibouchi": "Vava", "category": "corps", "image_url": "👄", "difficulty": 1},
        {"french": "Cheville", "shimaore": "Dzitso la pwédza", "kibouchi": "Dzitso la pwédza", "category": "corps", "difficulty": 1},
        {"french": "Cheveux", "shimaore": "Ngnélé", "kibouchi": "Fagnéva", "category": "corps", "difficulty": 1},
        {"french": "Cils", "shimaore": "Kové", "kibouchi": "Rambou faninti", "category": "corps", "difficulty": 1},
        {"french": "Cou", "shimaore": "Tsingo", "kibouchi": "Vouzougnou", "category": "corps", "difficulty": 1},
        {"french": "Côtes", "shimaore": "Bavou", "kibouchi": "Mbavou", "category": "corps", "difficulty": 1},
        {"french": "Dent", "shimaore": "Magno", "kibouchi": "Hifi", "category": "corps", "image_url": "🦷", "difficulty": 1},
        {"french": "Doigts", "shimaore": "Cha", "kibouchi": "Tondrou", "category": "corps", "difficulty": 1},
        {"french": "Dos", "shimaore": "Mengo", "kibouchi": "Vohou", "category": "corps", "difficulty": 1},
        {"french": "Fesses", "shimaore": "Shidze", "kibouchi": "Mvoumo/Fouri", "category": "corps", "difficulty": 1},
        {"french": "Front", "shimaore": "Housso", "kibouchi": "Lahara", "category": "corps", "difficulty": 1},
        {"french": "Hanche", "shimaore": "Trenga", "kibouchi": "Tahezagna", "category": "corps", "difficulty": 1},
        {"french": "Joue", "shimaore": "Savou", "kibouchi": "Fifi", "category": "corps", "difficulty": 1},
        {"french": "Langue", "shimaore": "Oulimé", "kibouchi": "Léla", "category": "corps", "difficulty": 1},
        {"french": "Lèvre", "shimaore": "Dhomo", "kibouchi": "Soungni", "category": "corps", "difficulty": 1},
        {"french": "Main", "shimaore": "Mhono", "kibouchi": "Tagnana", "category": "corps", "image_url": "✋", "difficulty": 1},
        {"french": "Menton", "shimaore": "Shlévou", "kibouchi": "Sokou", "category": "corps", "difficulty": 1},
        {"french": "Nez", "shimaore": "Poua", "kibouchi": "Horougnou", "category": "corps", "image_url": "👃", "difficulty": 1},
        {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou", "category": "corps", "difficulty": 1},
        {"french": "Oreille", "shimaore": "Kiyo", "kibouchi": "Soufigni", "category": "corps", "image_url": "👂", "difficulty": 1},
        {"french": "Peau", "shimaore": "Ngwezi", "kibouchi": "Ngwezi", "category": "corps", "difficulty": 1},
        {"french": "Pied", "shimaore": "Mindrou", "kibouchi": "Viti", "category": "corps", "image_url": "🦶", "difficulty": 1},
        {"french": "Pénis", "shimaore": "Mbo", "kibouchi": "Kaboudzi", "category": "corps", "difficulty": 1},
        {"french": "Sourcil", "shimaore": "Tsi", "kibouchi": "Ankwéssi", "category": "corps", "difficulty": 1},
        {"french": "Testicules", "shimaore": "Kwendzé", "kibouchi": "Vouancarou", "category": "corps", "difficulty": 1},
        {"french": "Tête", "shimaore": "Shitsoi", "kibouchi": "Louha", "category": "corps", "image_url": "🗣️", "difficulty": 1},
        {"french": "Vagin", "shimaore": "Ndzigni", "kibouchi": "Tingui", "category": "corps", "difficulty": 1},
        {"french": "Ventre", "shimaore": "Mimba", "kibouchi": "Kibou", "category": "corps", "difficulty": 1},
        {"french": "Œil", "shimaore": "Matso", "kibouchi": "Faninti", "category": "corps", "image_url": "👁️", "difficulty": 1},
        {"french": "Épaule", "shimaore": "Béga", "kibouchi": "Haveyi", "category": "corps", "difficulty": 1},

        # Grammaire (pronoms personnels et possessifs)
        {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi", "category": "grammaire", "difficulty": 1},
        {"french": "Ils/Elles", "shimaore": "Wawo", "kibouchi": "Réou", "category": "grammaire", "difficulty": 1},
        {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou", "category": "grammaire", "difficulty": 1},
        {"french": "Le leur", "shimaore": "Yawo", "kibouchi": "Nindréou", "category": "grammaire", "difficulty": 2},
        {"french": "Le mien", "shimaore": "Yangou", "kibouchi": "Ninakahi", "category": "grammaire", "difficulty": 2},
        {"french": "Le nôtre", "shimaore": "Yatrou", "kibouchi": "Nintsika", "category": "grammaire", "difficulty": 2},
        {"french": "Le sien", "shimaore": "Yahé", "kibouchi": "Ninazi", "category": "grammaire", "difficulty": 2},
        {"french": "Le tien", "shimaore": "Yaho", "kibouchi": "Ninaou", "category": "grammaire", "difficulty": 2},
        {"french": "Le vôtre", "shimaore": "Yagnou", "kibouchi": "Ninéyi", "category": "grammaire", "difficulty": 2},
        {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika", "category": "grammaire", "difficulty": 1},
        {"french": "Tu", "shimaore": "Wawé", "kibouchi": "Anaou", "category": "grammaire", "difficulty": 1},
        {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anaréou", "category": "grammaire", "difficulty": 1},

        # Objets de la maison avec emojis
        {"french": "Assiette", "shimaore": "Saani", "kibouchi": "Saani", "category": "maison", "image_url": "🍽️", "difficulty": 1},
        {"french": "Balai", "shimaore": "Sanga", "kibouchi": "Famafo", "category": "maison", "image_url": "🧹", "difficulty": 1},
        {"french": "Banga", "shimaore": "Banga", "kibouchi": "Banga", "category": "maison", "difficulty": 1},
        {"french": "Bassine", "shimaore": "Karahi", "kibouchi": "Karahi", "category": "maison", "image_url": "🥄", "difficulty": 1},
        {"french": "Buffet", "shimaore": "Biffé", "kibouchi": "Biffé", "category": "maison", "difficulty": 1},
        {"french": "Cartable/Malette", "shimaore": "Mkoba", "kibouchi": "Mkoba", "category": "maison", "image_url": "🎒", "difficulty": 1},
        {"french": "Case", "shimaore": "Banga", "kibouchi": "Banga", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "Chaise", "shimaore": "Chiri", "kibouchi": "Chiri", "category": "maison", "image_url": "🪑", "difficulty": 1},
        {"french": "Clôture", "shimaore": "Mraba", "kibouchi": "Mraba", "category": "maison", "difficulty": 1},
        {"french": "Coupe coupe", "shimaore": "Chombo", "kibouchi": "Chombou", "category": "maison", "difficulty": 1},
        {"french": "Cour", "shimaore": "Mraba", "kibouchi": "Lacourou", "category": "maison", "difficulty": 1},
        {"french": "Couteau", "shimaore": "Souli", "kibouchi": "Mounrou", "category": "maison", "image_url": "🔪", "difficulty": 1},
        {"french": "Cuillère", "shimaore": "Kiyio", "kibouchi": "Soutchanau", "category": "maison", "image_url": "🥄", "difficulty": 1},
        {"french": "Fenêtre", "shimaore": "Fénétri", "kibouchi": "Lafoumétara", "category": "maison", "image_url": "🪟", "difficulty": 1},
        {"french": "Fondation", "shimaore": "Houra", "kibouchi": "Koura", "category": "maison", "difficulty": 1},
        {"french": "Hache", "shimaore": "Soha", "kibouchi": "Famaki", "category": "maison", "difficulty": 1},
        {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani", "category": "maison", "image_url": "🛏️", "difficulty": 1},
        {"french": "Louche", "shimaore": "Paou", "kibouchi": "Pow", "category": "maison", "difficulty": 1},
        {"french": "Lumière", "shimaore": "Mwengué", "kibouchi": "Mwengué", "category": "maison", "image_url": "💡", "difficulty": 1},
        {"french": "Machette", "shimaore": "M'panga", "kibouchi": "Ampanga", "category": "maison", "difficulty": 1},
        {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou", "category": "maison", "image_url": "🏠", "difficulty": 1},
        {"french": "Marmite", "shimaore": "Safiou", "kibouchi": "Vilogo", "category": "maison", "image_url": "🍲", "difficulty": 1},
        {"french": "Matelas", "shimaore": "Godoro", "kibouchi": "Godoro", "category": "maison", "difficulty": 1},
        {"french": "Mortier", "shimaore": "Moukaou", "kibouchi": "Lamoya", "category": "maison", "difficulty": 1},
        {"french": "Nappe", "shimaore": "Kilemba", "kibouchi": "Lambo", "category": "maison", "difficulty": 1},
        {"french": "Pilon", "shimaore": "Moukondzi", "kibouchi": "Moudéssi", "category": "maison", "difficulty": 1},
        {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavaragena", "category": "maison", "image_url": "🚪", "difficulty": 1},
        {"french": "Sac", "shimaore": "Gouni", "kibouchi": "Gouni", "category": "maison", "image_url": "🎒", "difficulty": 1},
        {"french": "Seau", "shimaore": "Siyo", "kibouchi": "Siyo", "category": "maison", "image_url": "🪣", "difficulty": 1},
        {"french": "Table", "shimaore": "Latabou", "kibouchi": "Latabou", "category": "maison", "image_url": "🪑", "difficulty": 1},
        {"french": "Toilette", "shimaore": "Mrabani", "kibouchi": "Mraba", "category": "maison", "image_url": "🚽", "difficulty": 1},
        {"french": "Toiture", "shimaore": "Outro", "kibouchi": "Vovougnou", "category": "maison", "difficulty": 1},
        {"french": "Torche", "shimaore": "Gandilé", "kibouchi": "Gandili", "category": "maison", "image_url": "🔦", "difficulty": 1},
        {"french": "Verre", "shimaore": "Taça", "kibouchi": "Taça", "category": "maison", "image_url": "🥤", "difficulty": 1},

        # Transport
        {"french": "Avion", "shimaore": "Ndégé", "kibouchi": "Ndégé", "category": "transport", "image_url": "✈️", "difficulty": 1},
        {"french": "Bateau", "shimaore": "Mashua", "kibouchi": "Sambo", "category": "transport", "image_url": "🚢", "difficulty": 1},

        # Vêtements avec emojis
        {"french": "Chemise", "shimaore": "Kamiza", "kibouchi": "Kamiza", "category": "vetements", "image_url": "👔", "difficulty": 1},
        {"french": "Pantalon", "shimaore": "Pantalon", "kibouchi": "Pantalon", "category": "vetements", "image_url": "👖", "difficulty": 1},
        {"french": "Salouva", "shimaore": "Salouva", "kibouchi": "Salouva", "category": "vetements", "image_url": "👗", "difficulty": 1},

        # Nourriture (alimentation locale) avec emojis
        {"french": "Ananas", "shimaore": "Nanassi", "kibouchi": "Mananassi", "category": "nourriture", "image_url": "🍍", "difficulty": 1},
        {"french": "Banane", "shimaore": "Trovi", "kibouchi": "Hountsi", "category": "nourriture", "image_url": "🍌", "difficulty": 1},
        {"french": "Brèdes", "shimaore": "Féliki", "kibouchi": "Féliki", "category": "nourriture", "image_url": "🥬", "difficulty": 1},
        {"french": "Café", "shimaore": "Karawa", "kibouchi": "Kaoua", "category": "nourriture", "image_url": "☕", "difficulty": 1},
        {"french": "Ciboulette", "shimaore": "Chouroungou", "kibouchi": "Chiboulette", "category": "nourriture", "image_url": "🌿", "difficulty": 2},
        {"french": "Coco", "shimaore": "Nazi", "kibouchi": "Voiniou", "category": "nourriture", "image_url": "🥥", "difficulty": 1},
        {"french": "Coriandre", "shimaore": "Koriangou", "kibouchi": "Koriangou", "category": "nourriture", "image_url": "🌿", "difficulty": 2},
        {"french": "Crevettes", "shimaore": "Camba", "kibouchi": "Ancamba", "category": "nourriture", "image_url": "🦐", "difficulty": 1},
        {"french": "Curcuma", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "nourriture", "image_url": "🌿", "difficulty": 2},
        {"french": "Eau", "shimaore": "Maji", "kibouchi": "Ranou", "category": "nourriture", "image_url": "💧", "difficulty": 1},
        {"french": "Farine", "shimaore": "Unga", "kibouchi": "Lafarinna", "category": "nourriture", "image_url": "🌾", "difficulty": 1},
        {"french": "Fruit à pain", "shimaore": "Fwrampé", "kibouchi": "Frampé", "category": "nourriture", "image_url": "🍞", "difficulty": 1},
        {"french": "Gingembre", "shimaore": "Sakayi", "kibouchi": "Sakéyi", "category": "nourriture", "image_url": "🫚", "difficulty": 2},
        {"french": "Huile", "shimaore": "Mahoutou", "kibouchi": "Mahoutou", "category": "nourriture", "image_url": "🫒", "difficulty": 1},
        {"french": "Lait", "shimaore": "Dzia", "kibouchi": "Rounounou", "category": "nourriture", "image_url": "🥛", "difficulty": 1},
        {"french": "Langouste", "shimaore": "Camba diva", "kibouchi": "Ancamba diva", "category": "nourriture", "image_url": "🦞", "difficulty": 2},
        {"french": "Mangue", "shimaore": "Manga", "kibouchi": "Manga", "category": "nourriture", "image_url": "🥭", "difficulty": 1},
        {"french": "Noix de coco", "shimaore": "Nazi", "kibouchi": "Voiniou", "category": "nourriture", "image_url": "🥥", "difficulty": 1},
        {"french": "Nourriture", "shimaore": "Chaoula", "kibouchi": "Hanigni", "category": "nourriture", "image_url": "🍽️", "difficulty": 1},
        {"french": "Œuf", "shimaore": "Bayi", "kibouchi": "Atoudou", "category": "nourriture", "image_url": "🥚", "difficulty": 1},
        {"french": "Pain", "shimaore": "Dipé", "kibouchi": "Dipé", "category": "nourriture", "image_url": "🍞", "difficulty": 1},
        {"french": "Patate douce", "shimaore": "Batata", "kibouchi": "Batata", "category": "nourriture", "image_url": "🍠", "difficulty": 1},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "nourriture", "image_url": "🐟", "difficulty": 1},
        {"french": "Pois d'angole", "shimaore": "Tsouzi", "kibouchi": "Ambatri", "category": "nourriture", "image_url": "🫘", "difficulty": 1},
        {"french": "Poivre", "shimaore": "Bvilibvili manga", "kibouchi": "Vilivili", "category": "nourriture", "image_url": "🌶️", "difficulty": 2},
        {"french": "Poulet", "shimaore": "Bawa", "kibouchi": "Akohou", "category": "nourriture", "image_url": "🐔", "difficulty": 1},
        {"french": "Riz", "shimaore": "Tsoholé", "kibouchi": "Vari", "category": "nourriture", "image_url": "🍚", "difficulty": 1},
        {"french": "Sel", "shimaore": "Chavi", "kibouchi": "Soui", "category": "nourriture", "image_url": "🧂", "difficulty": 1},
        {"french": "Sucre", "shimaore": "Sikar", "kibouchi": "Sikar", "category": "nourriture", "image_url": "🍯", "difficulty": 1},
        {"french": "Tamarin", "shimaore": "Ouhajou", "kibouchi": "Madirou kakazou", "category": "nourriture", "image_url": "🌰", "difficulty": 1},
        {"french": "Thé", "shimaore": "Trayi", "kibouchi": "Rayi", "category": "nourriture", "image_url": "🍵", "difficulty": 1},
        {"french": "Vanille", "shimaore": "Lavani", "kibouchi": "Lavani", "category": "nourriture", "image_url": "🌿", "difficulty": 1},
        {"french": "Viande", "shimaore": "Nhyama", "kibouchi": "Amboumati", "category": "nourriture", "image_url": "🥩", "difficulty": 1},
        {"french": "Yaourt", "shimaore": "Roba nani", "kibouchi": "Roba nani", "category": "nourriture", "image_url": "🍸", "difficulty": 1},

        # Adjectifs (descripteurs)
        {"french": "Beau/Jolie", "shimaore": "Mzouri", "kibouchi": "Zatovou", "category": "adjectifs", "image_url": "😍", "difficulty": 1},
        {"french": "Bon", "shimaore": "Mwéma", "kibouchi": "Tsara", "category": "adjectifs", "image_url": "👍", "difficulty": 1},
        {"french": "Chaud", "shimaore": "Moro", "kibouchi": "Méyi", "category": "adjectifs", "image_url": "🔥", "difficulty": 1},
        {"french": "Content", "shimaore": "Oujiviwa", "kibouchi": "Ravou", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "Dur", "shimaore": "Mangavou", "kibouchi": "Mahéri", "category": "adjectifs", "difficulty": 1},
        {"french": "Fort", "shimaore": "Ouna ngouvou", "kibouchi": "Missi ngouvou", "category": "adjectifs", "image_url": "💪", "difficulty": 1},
        {"french": "Froid", "shimaore": "Baridi", "kibouchi": "Manintsi", "category": "adjectifs", "image_url": "🧊", "difficulty": 1},
        {"french": "Gentil", "shimaore": "Mwéma", "kibouchi": "Tsara rohou", "category": "adjectifs", "image_url": "😊", "difficulty": 1},
        {"french": "Grand", "shimaore": "Bole", "kibouchi": "Bé", "category": "adjectifs", "image_url": "📏", "difficulty": 1},
        {"french": "Gros", "shimaore": "Mtronga", "kibouchi": "Tronga/Bé", "category": "adjectifs", "difficulty": 1},
        {"french": "Jeune", "shimaore": "Nrétsa", "kibouchi": "Zaza", "category": "adjectifs", "image_url": "👶", "difficulty": 1},
        {"french": "Laid", "shimaore": "Tsi ndzouzouri", "kibouchi": "Ratsi sora", "category": "adjectifs", "image_url": "😖", "difficulty": 1},
        {"french": "Maigre", "shimaore": "Tsala", "kibouchi": "Mahia", "category": "adjectifs", "difficulty": 1},
        {"french": "Mauvais", "shimaore": "Mbovou", "kibouchi": "Mwadéli", "category": "adjectifs", "image_url": "👎", "difficulty": 1},
        {"french": "Méchant", "shimaore": "Mbovou", "kibouchi": "Ratsi rohou", "category": "adjectifs", "image_url": "😠", "difficulty": 1},
        {"french": "Mou", "shimaore": "Tremboivou", "kibouchi": "Malémi", "category": "adjectifs", "difficulty": 1},
        {"french": "Petit", "shimaore": "Tsi", "kibouchi": "Tsi", "category": "adjectifs", "image_url": "🤏", "difficulty": 1},
        {"french": "Triste", "shimaore": "Ouna hamo", "kibouchi": "Malahélou", "category": "adjectifs", "image_url": "😢", "difficulty": 1},
        {"french": "Vieux", "shimaore": "Dhouha", "kibouchi": "Héla", "category": "adjectifs", "image_url": "👴", "difficulty": 1},

        # Nature et environnement avec emojis
        {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Arbre à pain", "shimaore": "M'frampé", "kibouchi": "Voudi ni frampé", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Bambou", "shimaore": "M'banbo", "kibouchi": "Valiha", "category": "nature", "image_url": "🎋", "difficulty": 1},
        {"french": "Baobab", "shimaore": "M'bouyou", "kibouchi": "Voudi ni bouyou", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Barrière de corail", "shimaore": "Caléni", "kibouchi": "Caléni", "category": "nature", "image_url": "🪸", "difficulty": 1},
        {"french": "Canne à sucre", "shimaore": "Moua", "kibouchi": "Fari", "category": "nature", "image_url": "🌾", "difficulty": 1},
        {"french": "Cocotier", "shimaore": "M'hadzi", "kibouchi": "Voudi ni vwaniou", "category": "nature", "image_url": "🌴", "difficulty": 1},
        {"french": "Corail", "shimaore": "Soiyi", "kibouchi": "Soiyi", "category": "nature", "image_url": "🪸", "difficulty": 1},
        {"french": "École", "shimaore": "Licoli", "kibouchi": "Licoli", "category": "nature", "image_url": "🏫", "difficulty": 1},
        {"french": "École coranique", "shimaore": "Shioni", "kibouchi": "Kioni", "category": "nature", "image_url": "🕌", "difficulty": 1},
        {"french": "Fagot", "shimaore": "Kouni", "kibouchi": "Azoumati", "category": "nature", "image_url": "🪵", "difficulty": 1},
        {"french": "Inondé", "shimaore": "Ourora", "kibouchi": "Dobou", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "Jacquier", "shimaore": "M'fénéssi", "kibouchi": "Voudi ni finéssi", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Lune", "shimaore": "Mwézi", "kibouchi": "Fandzava", "category": "nature", "image_url": "🌙", "difficulty": 1},
        {"french": "Mangrove", "shimaore": "Mhonko", "kibouchi": "Honkou", "category": "nature", "image_url": "🌿", "difficulty": 1},
        {"french": "Manguier", "shimaore": "M'manga", "kibouchi": "Voudi ni manga", "category": "nature", "image_url": "🌳", "difficulty": 1},
        {"french": "Marée basse", "shimaore": "Maji yavo", "kibouchi": "Ranou méki", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "Marée haute", "shimaore": "Maji yamalé", "kibouchi": "Ranou fénou", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "Pente/Colline/Mont", "shimaore": "Mlima", "kibouchi": "Boungou", "category": "nature", "image_url": "⛰️", "difficulty": 1},
        {"french": "Pirogue", "shimaore": "Laka", "kibouchi": "Lakana", "category": "nature", "image_url": "🛶", "difficulty": 1},
        {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni", "category": "nature", "image_url": "🏖️", "difficulty": 1},
        {"french": "Pluie", "shimaore": "Vhoua", "kibouchi": "Mahaléni", "category": "nature", "image_url": "🌧️", "difficulty": 1},
        {"french": "Rivière", "shimaore": "Mouro", "kibouchi": "Mouroni", "category": "nature", "image_url": "🏞️", "difficulty": 1},
        {"french": "Sable", "shimaore": "Mtsanga", "kibouchi": "Fasigni", "category": "nature", "image_url": "🏖️", "difficulty": 1},
        {"french": "Sauvage", "shimaore": "Nyéha", "kibouchi": "Di", "category": "nature", "difficulty": 1},
        {"french": "Sol", "shimaore": "Tsi", "kibouchi": "Tani", "category": "nature", "image_url": "🌍", "difficulty": 1},
        {"french": "Soleil", "shimaore": "Mwézi", "kibouchi": "Zouva", "category": "nature", "image_url": "☀️", "difficulty": 1},
        {"french": "Tempête", "shimaore": "Darouba", "kibouchi": "Tsikou", "category": "nature", "image_url": "⛈️", "difficulty": 1},
        {"french": "Terre", "shimaore": "Trotro", "kibouchi": "Fotaka", "category": "nature", "image_url": "🌍", "difficulty": 1},
        {"french": "Vague", "shimaore": "Dhouja", "kibouchi": "Houndza/Riaka", "category": "nature", "image_url": "🌊", "difficulty": 1},
        {"french": "Vedette", "shimaore": "Kwassa kwassa", "kibouchi": "Vidéti", "category": "nature", "image_url": "🚤", "difficulty": 1},
        {"french": "Vent", "shimaore": "Pévo", "kibouchi": "Tsikou", "category": "nature", "image_url": "💨", "difficulty": 1},
        {"french": "Érosion", "shimaore": "Padza", "kibouchi": "Padza", "category": "nature", "difficulty": 1},
        {"french": "Étoile", "shimaore": "Gnora", "kibouchi": "Lakintagna", "category": "nature", "image_url": "⭐", "difficulty": 1},

        # Expressions courantes avec emojis
        {"french": "Aller bien", "shimaore": "Oufa heri", "kibouchi": "Mandeha tsara", "category": "expressions", "image_url": "😊", "difficulty": 1},
        {"french": "Aller quelque part", "shimaore": "Ouzndra mahali", "kibouchi": "Mandeha mbi", "category": "expressions", "difficulty": 2},
        {"french": "Avoir faim", "shimaore": "Ouna ndjaa", "kibouchi": "Hanoanoa", "category": "expressions", "image_url": "😋", "difficulty": 1},
        {"french": "Avoir mal", "shimaore": "Ouna maumivu", "kibouchi": "Maharevi", "category": "expressions", "image_url": "😖", "difficulty": 1},
        {"french": "Avoir peur", "shimaore": "Ouna hofu", "kibouchi": "Hatahoura", "category": "expressions", "image_url": "😨", "difficulty": 1},
        {"french": "Avoir soif", "shimaore": "Ouna kio", "kibouchi": "Magndrangerani", "category": "expressions", "image_url": "🥤", "difficulty": 1},
        {"french": "Avoir sommeil", "shimaore": "Ouna usingidzi", "kibouchi": "Matouri", "category": "expressions", "image_url": "😴", "difficulty": 1},
        {"french": "Beaucoup", "shimaore": "Mutru/Wengi", "kibouchi": "Betsaka", "category": "expressions", "difficulty": 1},
        {"french": "C'est bon", "shimaore": "Ni heri", "kibouchi": "Tsara", "category": "expressions", "image_url": "👍", "difficulty": 1},
        {"french": "C'est fini", "shimaore": "Ni kamalé", "kibouchi": "Vita", "category": "expressions", "image_url": "✅", "difficulty": 1},
        {"french": "Comment tu t'appelles", "shimaore": "Dzina laho nani", "kibouchi": "Oviaou anaou", "category": "expressions", "difficulty": 2},
        {"french": "De rien", "shimaore": "Poulia mbali", "kibouchi": "Tsi misi", "category": "expressions", "image_url": "🤷", "difficulty": 1},
        {"french": "Excuse-moi", "shimaore": "Soimahani", "kibouchi": "Soimahani", "category": "expressions", "image_url": "🙏", "difficulty": 1},
        {"french": "Faire attention", "shimaore": "Ouangalia heri", "kibouchi": "Mitandré", "category": "expressions", "image_url": "⚠️", "difficulty": 2},
        {"french": "Il n'y a pas", "shimaore": "Hawana", "kibouchi": "Tsi misi", "category": "expressions", "difficulty": 1},
        {"french": "Il y a", "shimaore": "Yana/Ana", "kibouchi": "Misi", "category": "expressions", "difficulty": 1},
        {"french": "J'ai mal compris", "shimaore": "Tsi waandjé", "kibouchi": "Tsi nahalé", "category": "expressions", "image_url": "🤔", "difficulty": 2},
        {"french": "J'ai oublié", "shimaore": "Wasaha", "kibouchi": "Hadinovi", "category": "expressions", "image_url": "🤦", "difficulty": 2},
        {"french": "Je ne comprends pas", "shimaore": "Tsi pvanandré", "kibouchi": "Tsi takatré", "category": "expressions", "image_url": "😕", "difficulty": 2},
        {"french": "Je ne sais pas", "shimaore": "Tsi pvadjioua", "kibouchi": "Tsi fantarové", "category": "expressions", "image_url": "🤷", "difficulty": 2},
        {"french": "Je suis désolé", "shimaore": "Soimahani tru", "kibouchi": "Soimahani loatse", "category": "expressions", "image_url": "😔", "difficulty": 2},
        {"french": "Non", "shimaore": "Anha", "kibouchi": "Anha", "category": "expressions", "image_url": "❌", "difficulty": 1},
        {"french": "Oui", "shimaore": "Ewa", "kibouchi": "Iya", "category": "expressions", "image_url": "✅", "difficulty": 1},
        {"french": "Pardon", "shimaore": "Soimahani", "kibouchi": "Soimahani", "category": "expressions", "image_url": "🙏", "difficulty": 1},
        {"french": "Pas grave", "shimaore": "Hapana taba", "kibouchi": "Tsi mavendou", "category": "expressions", "image_url": "🤷", "difficulty": 1},
        {"french": "Peut-être", "shimaore": "Huenda", "kibouchi": "Angamba", "category": "expressions", "image_url": "🤔", "difficulty": 2},
        {"french": "Peu", "shimaore": "Kadiri", "kibouchi": "Keli", "category": "expressions", "difficulty": 1},
        {"french": "Qu'est-ce qu'il y a", "shimaore": "Nini hayo", "kibouchi": "Inoni lé", "category": "expressions", "image_url": "❓", "difficulty": 2},
        {"french": "Qu'est-ce que c'est", "shimaore": "Nini hao", "kibouchi": "Inoni lé", "category": "expressions", "image_url": "❓", "difficulty": 2},
        {"french": "S'il vous plaît", "shimaore": "Parafadhali", "kibouchi": "Aza falia", "category": "expressions", "image_url": "🙏", "difficulty": 2},
        {"french": "Très bien", "shimaore": "Fétré tru", "kibouchi": "Tsara loatse", "category": "expressions", "image_url": "👌", "difficulty": 1},
        {"french": "Un peu", "shimaore": "Kidari", "kibouchi": "Kelibe", "category": "expressions", "difficulty": 1},
        {"french": "Venir", "shimaore": "Oudja", "kibouchi": "Miavi", "category": "expressions", "difficulty": 1},
        {"french": "Être fatigué", "shimaore": "Oushindoa", "kibouchi": "Sarahi", "category": "expressions", "image_url": "😴", "difficulty": 1},
        {"french": "Être pressé", "shimaore": "Ouna haraka", "kibouchi": "Maikatse", "category": "expressions", "image_url": "🏃", "difficulty": 2},

        # Verbes (actions essentielles) avec emojis
        {"french": "Abîmer", "shimaore": "Oumengna", "kibouchi": "Mandroubaka", "category": "verbes", "image_url": "💥", "difficulty": 1},
        {"french": "Acheter", "shimaore": "Ounuwa", "kibouchi": "Mividi", "category": "verbes", "image_url": "💰", "difficulty": 1},
        {"french": "Aider", "shimaore": "Ousaidia", "kibouchi": "Manampy", "category": "verbes", "image_url": "🤝", "difficulty": 1},
        {"french": "Aimer", "shimaore": "Oupenda", "kibouchi": "Tia", "category": "verbes", "image_url": "❤️", "difficulty": 1},
        {"french": "Aller", "shimaore": "Ouzndra", "kibouchi": "Mandeha", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Apporter", "shimaore": "Ouleta", "kibouchi": "Mitondra", "category": "verbes", "image_url": "📦", "difficulty": 1},
        {"french": "Apprendre", "shimaore": "Ourfoundrana", "kibouchi": "Midzorou", "category": "verbes", "image_url": "📚", "difficulty": 1},
        {"french": "Arrêter", "shimaore": "Ousimamisha", "kibouchi": "Mampitsahatra", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "Arriver", "shimaore": "Oufika", "kibouchi": "Mitongava", "category": "verbes", "image_url": "🏁", "difficulty": 1},
        {"french": "Attendre", "shimaore": "Oungodjea", "kibouchi": "Miandri", "category": "verbes", "image_url": "⏰", "difficulty": 1},
        {"french": "Balayer", "shimaore": "Ouhoundza", "kibouchi": "Mamafa", "category": "verbes", "image_url": "🧹", "difficulty": 1},
        {"french": "Boire", "shimaore": "Ounzoa", "kibouchi": "Mitsiratra", "category": "verbes", "image_url": "🥤", "difficulty": 1},
        {"french": "Casser", "shimaore": "Ouvoundja", "kibouchi": "Mandrava", "category": "verbes", "image_url": "💥", "difficulty": 1},
        {"french": "Chanter", "shimaore": "Ouimba", "kibouchi": "Mihira", "category": "verbes", "image_url": "🎵", "difficulty": 1},
        {"french": "Chercher", "shimaore": "Outafouta", "kibouchi": "Hitadi", "category": "verbes", "image_url": "🔍", "difficulty": 1},
        {"french": "Commencer", "shimaore": "Ouzandzea", "kibouchi": "Manomboka", "category": "verbes", "image_url": "▶️", "difficulty": 1},
        {"french": "Comprendre", "shimaore": "Ouéléwa", "kibouchi": "Kouéléwa", "category": "verbes", "image_url": "💡", "difficulty": 1},
        {"french": "Connaître", "shimaore": "Oujoua", "kibouchi": "Méhéyi", "category": "verbes", "image_url": "🧠", "difficulty": 1},
        {"french": "Construire", "shimaore": "Oudjenga", "kibouchi": "Manao", "category": "verbes", "image_url": "🏗️", "difficulty": 1},
        {"french": "Couper", "shimaore": "Oukatra", "kibouchi": "Manapaka", "category": "verbes", "image_url": "✂️", "difficulty": 1},
        {"french": "Couper du bois", "shimaore": "Oupasouha kuni", "kibouchi": "Mamaki azoumati", "category": "verbes", "image_url": "🪓", "difficulty": 2},
        {"french": "Courir", "shimaore": "Wendra mbiyo", "kibouchi": "Miloumeyi", "category": "verbes", "image_url": "🏃", "difficulty": 1},
        {"french": "Creuser", "shimaore": "Outsimba", "kibouchi": "Mangadi", "category": "verbes", "image_url": "⛏️", "difficulty": 1},
        {"french": "Cuisiner", "shimaore": "Oupiha", "kibouchi": "Mahandrou", "category": "verbes", "image_url": "👨‍🍳", "difficulty": 1},
        {"french": "Cultiver", "shimaore": "Oulima", "kibouchi": "Mikapa", "category": "verbes", "image_url": "🌱", "difficulty": 1},
        {"french": "Danser", "shimaore": "Oucheza", "kibouchi": "Mandihy", "category": "verbes", "image_url": "💃", "difficulty": 1},
        {"french": "Demander", "shimaore": "Oodzisa", "kibouchi": "Magndoutani", "category": "verbes", "image_url": "❓", "difficulty": 1},
        {"french": "Descendre", "shimaore": "Ouhidra", "kibouchi": "Miritrka", "category": "verbes", "image_url": "⬇️", "difficulty": 1},
        {"french": "Devenir", "shimaore": "Ouwa", "kibouchi": "Manjari", "category": "verbes", "difficulty": 1},
        {"french": "Dire", "shimaore": "Ourenguissa", "kibouchi": "Mangataka", "category": "verbes", "image_url": "💬", "difficulty": 1},
        {"french": "Donner", "shimaore": "Ouhapa", "kibouchi": "Manomé", "category": "verbes", "image_url": "🤲", "difficulty": 1},
        {"french": "Dormir", "shimaore": "Oulala", "kibouchi": "Mandri", "category": "verbes", "image_url": "😴", "difficulty": 1},
        {"french": "Emmener", "shimaore": "Ouchukuwa", "kibouchi": "Mitondra", "category": "verbes", "image_url": "👫", "difficulty": 1},
        {"french": "Entendre", "shimaore": "Ouwoulkia", "kibouchi": "Mandré", "category": "verbes", "image_url": "👂", "difficulty": 1},
        {"french": "Entrer", "shimaore": "Oughulya", "kibouchi": "Midiri", "category": "verbes", "image_url": "🚪", "difficulty": 1},
        {"french": "Essayer", "shimaore": "Oudjaribu", "kibouchi": "Mizaha", "category": "verbes", "image_url": "🎯", "difficulty": 1},
        {"french": "Faire", "shimaore": "Oufa", "kibouchi": "Manao", "category": "verbes", "image_url": "🔨", "difficulty": 1},
        {"french": "Faire sécher", "shimaore": "Ouhoumisa", "kibouchi": "Manapi", "category": "verbes", "image_url": "☀️", "difficulty": 1},
        {"french": "Faire ses besoins", "shimaore": "Oukoza", "kibouchi": "Manibi", "category": "verbes", "difficulty": 1},
        {"french": "Fermer", "shimaore": "Oufungua", "kibouchi": "Manidy", "category": "verbes", "image_url": "🔒", "difficulty": 1},
        {"french": "Finir", "shimaore": "Oukamalisha", "kibouchi": "Mamarana", "category": "verbes", "image_url": "✅", "difficulty": 1},
        {"french": "Frapper", "shimaore": "Oupiga", "kibouchi": "Mikapoka", "category": "verbes", "image_url": "👊", "difficulty": 1},
        {"french": "Garder", "shimaore": "Ouhifadzi", "kibouchi": "Mitandri", "category": "verbes", "image_url": "🛡️", "difficulty": 1},
        {"french": "Jeter", "shimaore": "Outupa", "kibouchi": "Manilatsou", "category": "verbes", "image_url": "🗑️", "difficulty": 1},
        {"french": "Jouer", "shimaore": "Oupaguedza", "kibouchi": "Misoma", "category": "verbes", "image_url": "🎮", "difficulty": 1},
        {"french": "Laver", "shimaore": "Ouhowa", "kibouchi": "Miséki", "category": "verbes", "image_url": "🧽", "difficulty": 1},
        {"french": "Lever", "shimaore": "Ouinuka", "kibouchi": "Mitsangan", "category": "verbes", "image_url": "⬆️", "difficulty": 1},
        {"french": "Lire", "shimaore": "Ousoma", "kibouchi": "Midzorou", "category": "verbes", "image_url": "📖", "difficulty": 1},
        {"french": "Manger", "shimaore": "Oudhya", "kibouchi": "Mihinagna", "category": "verbes", "image_url": "🍽️", "difficulty": 1},
        {"french": "Marcher", "shimaore": "Ouzndra", "kibouchi": "Mandeha", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Monter", "shimaore": "Oupangua", "kibouchi": "Mitreza", "category": "verbes", "image_url": "⬆️", "difficulty": 1},
        {"french": "Montrer", "shimaore": "Ouonesa", "kibouchi": "Masegou", "category": "verbes", "image_url": "👉", "difficulty": 1},
        {"french": "Mourir", "shimaore": "Oufwa", "kibouchi": "Mati", "category": "verbes", "image_url": "💀", "difficulty": 2},
        {"french": "Naître", "shimaore": "Ouzalywa", "kibouchi": "Mate lahatra", "category": "verbes", "image_url": "👶", "difficulty": 1},
        {"french": "Oublier", "shimaore": "Ousaha", "kibouchi": "Hadinovi", "category": "verbes", "image_url": "🤦", "difficulty": 1},
        {"french": "Ouvrir", "shimaore": "Oufunguwa", "kibouchi": "Misohi", "category": "verbes", "image_url": "🔓", "difficulty": 1},
        {"french": "Parler", "shimaore": "Oujagous", "kibouchi": "Mivoulgma", "category": "verbes", "image_url": "💬", "difficulty": 1},
        {"french": "Partir", "shimaore": "Ouzndra", "kibouchi": "Mandeha", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Passer", "shimaore": "Oupita", "kibouchi": "Mande", "category": "verbes", "image_url": "➡️", "difficulty": 1},
        {"french": "Payer", "shimaore": "Oulipia", "kibouchi": "Mandoa", "category": "verbes", "image_url": "💰", "difficulty": 1},
        {"french": "Penser", "shimaore": "Oufikiria", "kibouchi": "Mieritréri", "category": "verbes", "image_url": "🤔", "difficulty": 1},
        {"french": "Perdre", "shimaore": "Oupotea", "kibouchi": "Mamvi", "category": "verbes", "image_url": "😞", "difficulty": 1},
        {"french": "Planter", "shimaore": "Outabou", "kibouchi": "Mamboli", "category": "verbes", "image_url": "🌱", "difficulty": 1},
        {"french": "Porter", "shimaore": "Oushika", "kibouchi": "Mitondra", "category": "verbes", "image_url": "🎒", "difficulty": 1},
        {"french": "Pouvoir", "shimaore": "Ouchindra", "kibouchi": "Mahaléou", "category": "verbes", "image_url": "💪", "difficulty": 1},
        {"french": "Prendre", "shimaore": "Ouchukuwa", "kibouchi": "Makate", "category": "verbes", "image_url": "🤏", "difficulty": 1},
        {"french": "Préparer", "shimaore": "Ousoudra", "kibouchi": "Mamouana", "category": "verbes", "image_url": "👨‍🍳", "difficulty": 1},
        {"french": "Prier", "shimaore": "Ousouala", "kibouchi": "Mivavi", "category": "verbes", "image_url": "🙏", "difficulty": 1},
        {"french": "Ramasser", "shimaore": "Oukusania", "kibouchi": "Mangala", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "Ranger/Arranger", "shimaore": "Ourenguélédza", "kibouchi": "Magnadzari", "category": "verbes", "image_url": "📦", "difficulty": 1},
        {"french": "Rappeler", "shimaore": "Oukumbuka", "kibouchi": "Mitadidy", "category": "verbes", "image_url": "📞", "difficulty": 1},
        {"french": "Regarder", "shimaore": "Ouangalia", "kibouchi": "Mijéri", "category": "verbes", "image_url": "👀", "difficulty": 1},
        {"french": "Remplir", "shimaore": "Oudjaza", "kibouchi": "Mafeno", "category": "verbes", "image_url": "🪣", "difficulty": 1},
        {"french": "Rencontrer", "shimaore": "Oukutunga", "kibouchi": "Mahita", "category": "verbes", "image_url": "🤝", "difficulty": 1},
        {"french": "Rentrer", "shimaore": "Ougilia", "kibouchi": "Miverimé", "category": "verbes", "image_url": "🏠", "difficulty": 1},
        {"french": "Récolter", "shimaore": "Ouvouna", "kibouchi": "Mampoka", "category": "verbes", "image_url": "🌾", "difficulty": 1},
        {"french": "Répondre", "shimaore": "Oudjibou", "kibouchi": "Mikoudjibou", "category": "verbes", "image_url": "💬", "difficulty": 1},
        {"french": "Réveiller", "shimaore": "Ouamsha", "kibouchi": "Mamohamoha", "category": "verbes", "image_url": "⏰", "difficulty": 1},
        {"french": "Rire", "shimaore": "Oucheka", "kibouchi": "Mihomé", "category": "verbes", "image_url": "😂", "difficulty": 1},
        {"french": "S'asseoir", "shimaore": "Ouzina", "kibouchi": "Mitsindza", "category": "verbes", "image_url": "🪑", "difficulty": 1},
        {"french": "Savoir", "shimaore": "Oujoua", "kibouchi": "Méhéyi", "category": "verbes", "image_url": "🧠", "difficulty": 1},
        {"french": "Se baigner", "shimaore": "Ouhowa", "kibouchi": "Misséki", "category": "verbes", "image_url": "🛁", "difficulty": 1},
        {"french": "Se laver", "shimaore": "Ouhowa", "kibouchi": "Miséki", "category": "verbes", "image_url": "🧼", "difficulty": 1},
        {"french": "Se laver le derrière", "shimaore": "Outsamba", "kibouchi": "Mambouyï", "category": "verbes", "difficulty": 1},
        {"french": "Se rappeler", "shimaore": "Oumadzi", "kibouchi": "Koutanamou", "category": "verbes", "image_url": "💭", "difficulty": 1},
        {"french": "Se raser", "shimaore": "Oumea ndrevu", "kibouchi": "Manapaka somboutrou", "category": "verbes", "image_url": "🪒", "difficulty": 1},
        {"french": "Suivre", "shimaore": "Oufwata", "kibouchi": "Manampy", "category": "verbes", "image_url": "👥", "difficulty": 1},
        {"french": "Tomber", "shimaore": "Ouanguka", "kibouchi": "Milatsou", "category": "verbes", "image_url": "🤕", "difficulty": 1},
        {"french": "Toucher", "shimaore": "Ougusa", "kibouchi": "Mikatsa", "category": "verbes", "image_url": "✋", "difficulty": 1},
        {"french": "Travailler", "shimaore": "Oufagnia", "kibouchi": "Miazi", "category": "verbes", "image_url": "💼", "difficulty": 1},
        {"french": "Tremper", "shimaore": "Oulodza", "kibouchi": "Mandzoubougnou", "category": "verbes", "image_url": "💧", "difficulty": 1},
        {"french": "Tresser", "shimaore": "Oussouká", "kibouchi": "Mitali/Mandrari", "category": "verbes", "image_url": "💇", "difficulty": 1},
        {"french": "Trouver", "shimaore": "Oupata", "kibouchi": "Mahita", "category": "verbes", "image_url": "🔍", "difficulty": 1},
        {"french": "Tuer", "shimaore": "Ouwa", "kibouchi": "Mamono", "category": "verbes", "image_url": "💀", "difficulty": 2},
        {"french": "Uriner", "shimaore": "Ouraviha", "kibouchi": "Mandouwya", "category": "verbes", "difficulty": 1},
        {"french": "Vendre", "shimaore": "Ouuza", "kibouchi": "Mivarou", "category": "verbes", "image_url": "💰", "difficulty": 1},
        {"french": "Venir", "shimaore": "Oudja", "kibouchi": "Miavi", "category": "verbes", "image_url": "🚶", "difficulty": 1},
        {"french": "Voir", "shimaore": "Ourubona", "kibouchi": "Mahita", "category": "verbes", "image_url": "👀", "difficulty": 1},
        {"french": "Voler (dérober)", "shimaore": "Ouiwa", "kibouchi": "Mangalatra", "category": "verbes", "image_url": "🕴️", "difficulty": 2},
        {"french": "Voler (dans le ciel)", "shimaore": "Oupaa", "kibouchi": "Manidine", "category": "verbes", "image_url": "🦅", "difficulty": 1},
        {"french": "Vomir", "shimaore": "Outakéa", "kibouchi": "Mampétraka", "category": "verbes", "image_url": "🤮", "difficulty": 1},
        {"french": "Vouloir", "shimaore": "Outrlaho", "kibouchi": "Irokou", "category": "verbes", "image_url": "❤️", "difficulty": 1},
        {"french": "Écouter", "shimaore": "Ouwoulkia", "kibouchi": "Mitandréngni", "category": "verbes", "image_url": "👂", "difficulty": 1},
        {"french": "Écrire", "shimaore": "Ouhangidina", "kibouchi": "Soukouadika", "category": "verbes", "image_url": "✏️", "difficulty": 1},
    ]
    
    # Insert words into database
    for word_data in base_words:
        words_collection.insert_one(word_data)
    
    # Base exercises
    base_exercises = [
        {
            "type": "match_word_image",
            "content": {
                "word": "Chat",
                "options": ["Chat", "Chien", "Oiseau", "Poisson"],
                "correct": "Chat"
            },
            "difficulty": 1,
            "points": 10
        },
        {
            "type": "quiz",
            "content": {
                "question": "Comment dit-on 'Bonjour' en shimaoré ?",
                "options": ["Kwezi", "Twana", "Marahaba", "Jéjé"],
                "correct": "Kwezi"
            },
            "difficulty": 1,
            "points": 10
        }
    ]
    
    # Insert exercises into database
    for exercise_data in base_exercises:
        exercises_collection.insert_one(exercise_data)
    
    return {"message": "Base content initialized successfully", "words_count": len(base_words), "exercises_count": len(base_exercises)}

# Words endpoints
@app.get("/api/words")
async def get_words(category: Optional[str] = Query(None)):
    """Get all words or filter by category"""
    query = {}
    if category:
        query["category"] = category
    
    words = list(words_collection.find(query))
    return [dict_to_word(word).dict() for word in words]

@app.get("/api/words/{word_id}")
async def get_word(word_id: str):
    """Get a specific word by ID"""
    try:
        word = words_collection.find_one({"_id": ObjectId(word_id)})
        if word:
            return dict_to_word(word).dict()
        raise HTTPException(status_code=404, detail="Word not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid word ID")

@app.get("/api/sentences")
async def get_sentences(difficulty: int = None, tense: str = None, limit: int = 20):
    """Récupère les phrases pour le jeu 'construire des phrases'"""
    try:
        import random
        
        # Construire le filtre
        filter_query = {}
        if difficulty:
            filter_query["difficulty"] = difficulty
        if tense:
            filter_query["tense"] = tense
        
        # Récupérer toutes les phrases correspondantes puis mélanger
        all_sentences = list(sentences_collection.find(filter_query))
        
        # Mélanger les phrases pour plus de variété
        random.shuffle(all_sentences)
        
        # Appliquer la limite après le mélange
        sentences = all_sentences[:limit]
        
        # Convertir ObjectId en string
        for sentence in sentences:
            sentence["_id"] = str(sentence["_id"])
        
        return sentences
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/init-sentences")
async def initialize_sentences():
    """Initialize sentences database for the 'Construire des phrases' game"""
    try:
        # Exécuter la création de phrases dans un thread séparé pour éviter les problèmes d'async
        import asyncio
        await asyncio.get_event_loop().run_in_executor(None, create_sentence_database)
        count = sentences_collection.count_documents({})
        return {"message": f"Sentences database initialized successfully with {count} sentences"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/database-status")
async def get_database_status():
    """Get database integrity status and statistics"""
    try:
        is_healthy, message = db_protector.is_database_healthy()
        stats = db_protector.get_database_stats()
        
        return {
            "healthy": is_healthy,
            "message": message,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create-backup")
async def create_database_backup():
    """Create a manual backup of the database"""
    try:
        backup_path = db_protector.create_backup("manual_api_call")
        if backup_path:
            return {"message": "Backup created successfully", "backup_path": backup_path}
        else:
            raise HTTPException(status_code=500, detail="Failed to create backup")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emergency-restore")
async def emergency_database_restore():
    """Emergency restore of the authentic database"""
    try:
        if db_protector.emergency_restore():
            return {"message": "Emergency restore completed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Emergency restore failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/words")
async def create_word(word: WordCreate):
    """Create a new word"""
    word_dict = word.dict()
    word_dict["created_at"] = datetime.utcnow()
    result = words_collection.insert_one(word_dict)
    word_dict["id"] = str(result.inserted_id)
    return word_dict

@app.put("/api/words/{word_id}")
async def update_word(word_id: str, word: WordCreate):
    """Update a word"""
    try:
        word_dict = word.dict()
        result = words_collection.update_one(
            {"_id": ObjectId(word_id)},
            {"$set": word_dict}
        )
        if result.matched_count:
            updated_word = words_collection.find_one({"_id": ObjectId(word_id)})
            return dict_to_word(updated_word).dict()
        raise HTTPException(status_code=404, detail="Word not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid word ID")

@app.delete("/api/words/{word_id}")
async def delete_word(word_id: str):
    """Delete a word"""
    try:
        result = words_collection.delete_one({"_id": ObjectId(word_id)})
        if result.deleted_count:
            return {"message": "Word deleted successfully"}
        raise HTTPException(status_code=404, detail="Word not found")
    except:
        raise HTTPException(status_code=400, detail="Invalid word ID")

# Exercises endpoints
@app.get("/api/exercises")
async def get_exercises():
    """Get all exercises"""
    exercises = list(exercises_collection.find())
    return [dict_to_exercise(exercise).dict() for exercise in exercises]

@app.post("/api/exercises")
async def create_exercise(exercise: Exercise):
    """Create a new exercise"""
    exercise_dict = exercise.dict(exclude={"id"})
    exercise_dict["created_at"] = datetime.utcnow()
    result = exercises_collection.insert_one(exercise_dict)
    exercise_dict["id"] = str(result.inserted_id)
    return exercise_dict

# User progress endpoints
@app.get("/api/progress/{user_name}")
async def get_user_progress(user_name: str):
    """Get progress for a specific user"""
    try:
        progress = list(user_progress_collection.find({"user_name": user_name}))
        for p in progress:
            p["id"] = str(p["_id"])
            del p["_id"]
            # Convert datetime to string for JSON serialization
            if "completed_at" in p:
                p["completed_at"] = p["completed_at"].isoformat()
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/progress")
async def create_progress(progress: UserProgress):
    """Record user progress"""
    try:
        progress_dict = progress.dict(exclude={"id"})
        progress_dict["completed_at"] = datetime.utcnow()
        result = user_progress_collection.insert_one(progress_dict)
        
        # Create a clean response dict for JSON serialization
        response_dict = {
            "id": str(result.inserted_id),
            "user_name": progress_dict["user_name"],
            "exercise_id": progress_dict["exercise_id"],
            "score": progress_dict["score"],
            "completed_at": progress_dict["completed_at"].isoformat()
        }
        return response_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Badge system endpoints
@app.get("/api/badges/{user_name}")
async def get_user_badges(user_name: str):
    """Get badges for a specific user"""
    try:
        badges_collection = db.user_badges
        user_badges = badges_collection.find_one({"user_name": user_name})
        
        if user_badges:
            user_badges["id"] = str(user_badges["_id"])
            del user_badges["_id"]
            return user_badges.get("badges", [])
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/badges/{user_name}/unlock/{badge_id}")
async def unlock_badge(user_name: str, badge_id: str):
    """Unlock a badge for a user"""
    try:
        badges_collection = db.user_badges
        
        # Check if user already has badges record
        user_badges = badges_collection.find_one({"user_name": user_name})
        
        if user_badges:
            # User exists, add badge if not already unlocked
            if badge_id not in user_badges.get("badges", []):
                badges_collection.update_one(
                    {"user_name": user_name},
                    {
                        "$push": {"badges": badge_id},
                        "$set": {"updated_at": datetime.utcnow()}
                    }
                )
                return {"message": f"Badge {badge_id} unlocked for {user_name}"}
            else:
                return {"message": f"Badge {badge_id} already unlocked"}
        else:
            # Create new user badges record
            badges_collection.insert_one({
                "user_name": user_name,
                "badges": [badge_id],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
            return {"message": f"Badge {badge_id} unlocked for {user_name}"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/{user_name}")
async def get_user_stats(user_name: str):
    """Get comprehensive stats for a user for badge calculations"""
    try:
        # Get user progress
        progress = list(user_progress_collection.find({"user_name": user_name}))
        
        # Calculate basic stats
        total_score = sum(p.get("score", 0) for p in progress)
        completed_exercises = len(progress)
        average_score = total_score / completed_exercises if completed_exercises > 0 else 0
        best_score = max((p.get("score", 0) for p in progress), default=0)
        perfect_scores = len([p for p in progress if p.get("score", 0) >= 100])
        
        # Calculate learning streaks (simplified)
        learning_days = len(set(p.get("completed_at", datetime.utcnow()).date() for p in progress))
        
        return {
            "user_name": user_name,
            "total_score": total_score,
            "completed_exercises": completed_exercises,
            "average_score": round(average_score, 1),
            "best_score": best_score,
            "perfect_scores": perfect_scores,
            "learning_days": learning_days,
            "words_learned": completed_exercises  # Simplified assumption
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes audio authentiques
@app.get("/api/audio/famille/{filename}")
async def get_famille_audio(filename: str):
    """Sert un fichier audio famille"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/famille", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio famille non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/nature/{filename}")
async def get_nature_audio(filename: str):
    """Sert un fichier audio nature"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/nature", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio nature non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/nombres/{filename}")
async def get_nombres_audio(filename: str):
    """Sert un fichier audio nombres"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/nombres", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio nombres non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/animaux/{filename}")
async def get_animaux_audio(filename: str):
    """Sert un fichier audio animaux"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/animaux", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio animaux non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/vetements/{filename}")
async def get_vetements_audio(filename: str):
    """Sert un fichier audio vetements"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/vetements", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio vetements non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/maison/{filename}")
async def get_maison_audio(filename: str):
    """Sert un fichier audio maison"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/maison", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio maison non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/tradition/{filename}")
async def get_tradition_audio(filename: str):
    """Sert un fichier audio tradition"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/tradition", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio tradition non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/transport/{filename}")
async def get_transport_audio(filename: str):
    """Sert un fichier audio transport"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/transport", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio transport non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/adjectifs/{filename}")
async def get_adjectifs_audio(filename: str):
    """Sert un fichier audio adjectifs"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/adjectifs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio adjectifs non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/expressions/{filename}")
async def get_expressions_audio(filename: str):
    """Sert un fichier audio expressions"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/expressions", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio expressions non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/verbes/{filename}")
async def get_verbes_audio(filename: str):
    """Sert un fichier audio verbes"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/verbes", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio verbes non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/salutations/{filename}")
async def get_salutations_audio(filename: str):
    """Sert un fichier audio salutations"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/salutations", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio salutations non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/couleurs/{filename}")
async def get_couleurs_audio(filename: str):
    """Sert un fichier audio couleurs"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/couleurs", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio couleurs non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/grammaire/{filename}")
async def get_grammaire_audio(filename: str):
    """Sert un fichier audio grammaire"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/grammaire", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio grammaire non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/nourriture/{filename}")
async def get_nourriture_audio(filename: str):
    """Sert un fichier audio nourriture"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/nourriture", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio nourriture non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/corps/{filename}")
async def get_corps_audio(filename: str):
    """Sert un fichier audio corps"""
    import os
    from fastapi.responses import FileResponse
    
    file_path = os.path.join("/app/frontend/assets/audio/corps", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier audio corps non trouvé: {filename}")
    
    if not filename.endswith('.m4a'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers .m4a sont supportés")
    
    return FileResponse(
        file_path,
        media_type="audio/mp4",
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )

@app.get("/api/audio/info")
async def get_audio_info():
    """Information sur les fichiers audio disponibles"""
    import os
    
    famille_dir = "/app/frontend/assets/audio/famille"
    nature_dir = "/app/frontend/assets/audio/nature"
    nombres_dir = "/app/frontend/assets/audio/nombres"
    animaux_dir = "/app/frontend/assets/audio/animaux"
    corps_dir = "/app/frontend/assets/audio/corps"
    salutations_dir = "/app/frontend/assets/audio/salutations"
    couleurs_dir = "/app/frontend/assets/audio/couleurs"
    grammaire_dir = "/app/frontend/assets/audio/grammaire"
    nourriture_dir = "/app/frontend/assets/audio/nourriture"
    verbes_dir = "/app/frontend/assets/audio/verbes"
    expressions_dir = "/app/frontend/assets/audio/expressions"
    adjectifs_dir = "/app/frontend/assets/audio/adjectifs"
    vetements_dir = "/app/frontend/assets/audio/vetements"
    maison_dir = "/app/frontend/assets/audio/maison"
    tradition_dir = "/app/frontend/assets/audio/tradition"
    transport_dir = "/app/frontend/assets/audio/transport"
    
    famille_files = []
    nature_files = []
    nombres_files = []
    animaux_files = []
    corps_files = []
    salutations_files = []
    couleurs_files = []
    grammaire_files = []
    nourriture_files = []
    verbes_files = []
    expressions_files = []
    adjectifs_files = []
    vetements_files = []
    maison_files = []
    tradition_files = []
    transport_files = []
    
    if os.path.exists(famille_dir):
        famille_files = [f for f in os.listdir(famille_dir) if f.endswith('.m4a')]
    
    if os.path.exists(nature_dir):
        nature_files = [f for f in os.listdir(nature_dir) if f.endswith('.m4a')]
        
    if os.path.exists(nombres_dir):
        nombres_files = [f for f in os.listdir(nombres_dir) if f.endswith('.m4a')]
        
    if os.path.exists(animaux_dir):
        animaux_files = [f for f in os.listdir(animaux_dir) if f.endswith('.m4a')]
        
    if os.path.exists(corps_dir):
        corps_files = [f for f in os.listdir(corps_dir) if f.endswith('.m4a')]
        
    if os.path.exists(salutations_dir):
        salutations_files = [f for f in os.listdir(salutations_dir) if f.endswith('.m4a')]
        
    if os.path.exists(couleurs_dir):
        couleurs_files = [f for f in os.listdir(couleurs_dir) if f.endswith('.m4a')]
        
    if os.path.exists(grammaire_dir):
        grammaire_files = [f for f in os.listdir(grammaire_dir) if f.endswith('.m4a')]
        
    if os.path.exists(nourriture_dir):
        nourriture_files = [f for f in os.listdir(nourriture_dir) if f.endswith('.m4a')]
        
    if os.path.exists(verbes_dir):
        verbes_files = [f for f in os.listdir(verbes_dir) if f.endswith('.m4a')]
        
    if os.path.exists(expressions_dir):
        expressions_files = [f for f in os.listdir(expressions_dir) if f.endswith('.m4a')]
        
    if os.path.exists(adjectifs_dir):
        adjectifs_files = [f for f in os.listdir(adjectifs_dir) if f.endswith('.m4a')]
        
    if os.path.exists(vetements_dir):
        vetements_files = [f for f in os.listdir(vetements_dir) if f.endswith('.m4a')]
        
    if os.path.exists(maison_dir):
        maison_files = [f for f in os.listdir(maison_dir) if f.endswith('.m4a')]
        
    if os.path.exists(tradition_dir):
        tradition_files = [f for f in os.listdir(tradition_dir) if f.endswith('.m4a')]
        
    if os.path.exists(transport_dir):
        transport_files = [f for f in os.listdir(transport_dir) if f.endswith('.m4a')]
    
    return {
        "service": "Audio API intégré - Système Dual Étendu",
        "famille": {
            "count": len(famille_files),
            "files": sorted(famille_files)
        },
        "nature": {
            "count": len(nature_files),
            "files": sorted(nature_files)
        },
        "nombres": {
            "count": len(nombres_files),
            "files": sorted(nombres_files)
        },
        "animaux": {
            "count": len(animaux_files),
            "files": sorted(animaux_files)
        },
        "corps": {
            "count": len(corps_files),
            "files": sorted(corps_files)
        },
        "salutations": {
            "count": len(salutations_files),
            "files": sorted(salutations_files)
        },
        "couleurs": {
            "count": len(couleurs_files),
            "files": sorted(couleurs_files)
        },
        "grammaire": {
            "count": len(grammaire_files),
            "files": sorted(grammaire_files)
        },
        "nourriture": {
            "count": len(nourriture_files),
            "files": sorted(nourriture_files)
        },
        "verbes": {
            "count": len(verbes_files),
            "files": sorted(verbes_files)
        },
        "expressions": {
            "count": len(expressions_files),
            "files": sorted(expressions_files)
        },
        "adjectifs": {
            "count": len(adjectifs_files),
            "files": sorted(adjectifs_files)
        },
        "vetements": {
            "count": len(vetements_files),
            "files": sorted(vetements_files)
        },
        "maison": {
            "count": len(maison_files),
            "files": sorted(maison_files)
        },
        "tradition": {
            "count": len(tradition_files),
            "files": sorted(tradition_files)
        },
        "transport": {
            "count": len(transport_files),
            "files": sorted(transport_files)
        },
        "endpoints": {
            "famille": "/api/audio/famille/{filename}",
            "nature": "/api/audio/nature/{filename}",
            "nombres": "/api/audio/nombres/{filename}",
            "animaux": "/api/audio/animaux/{filename}",
            "corps": "/api/audio/corps/{filename}",
            "salutations": "/api/audio/salutations/{filename}",
            "couleurs": "/api/audio/couleurs/{filename}",
            "grammaire": "/api/audio/grammaire/{filename}",
            "nourriture": "/api/audio/nourriture/{filename}",
            "verbes": "/api/audio/verbes/{filename}",
            "expressions": "/api/audio/expressions/{filename}",
            "adjectifs": "/api/audio/adjectifs/{filename}",
            "vetements": "/api/audio/vetements/{filename}",
            "maison": "/api/audio/maison/{filename}",
            "tradition": "/api/audio/tradition/{filename}",
            "transport": "/api/audio/transport/{filename}",
            "dual_system": "/api/words/{word_id}/audio/{lang}"
        },
        "total_categories": 16,
        "total_files": len(famille_files) + len(nature_files) + len(nombres_files) + len(animaux_files) + len(corps_files) + len(salutations_files) + len(couleurs_files) + len(grammaire_files) + len(nourriture_files) + len(verbes_files) + len(expressions_files) + len(adjectifs_files) + len(vetements_files) + len(maison_files) + len(tradition_files) + len(transport_files)
    }

# Nouveaux endpoints pour le système audio dual
@app.get("/api/words/{word_id}/audio/{lang}")
async def get_word_audio_by_language(word_id: str, lang: str):
    """
    Récupère l'audio d'un mot dans une langue spécifique
    lang: 'shimaore' ou 'kibouchi'
    """
    if lang not in ['shimaore', 'kibouchi']:
        raise HTTPException(status_code=400, detail="Langue doit être 'shimaore' ou 'kibouchi'")
    
    try:
        # Récupérer le mot
        word_doc = words_collection.find_one({"_id": ObjectId(word_id)})
        if not word_doc:
            raise HTTPException(status_code=404, detail="Mot non trouvé")
        
        # Vérifier si le système dual est activé
        if not word_doc.get("dual_audio_system", False):
            raise HTTPException(status_code=400, detail="Ce mot n'utilise pas le système audio dual")
        
        # Récupérer le nom du fichier selon la langue
        if lang == "shimaore":
            filename = word_doc.get("shimoare_audio_filename")
            has_audio = word_doc.get("shimoare_has_audio", False)
        else:  # kibouchi
            filename = word_doc.get("kibouchi_audio_filename")
            has_audio = word_doc.get("kibouchi_has_audio", False)
        
        if not has_audio or not filename:
            raise HTTPException(status_code=404, detail=f"Pas d'audio disponible en {lang} pour ce mot")
        
        # Servir le fichier
        import os
        from fastapi.responses import FileResponse
        
        # Détecter automatiquement la catégorie du mot pour utiliser le bon dossier
        word_category = word_doc.get("section") or word_doc.get("category", "famille")
        audio_dirs = {
            "famille": "/app/frontend/assets/audio/famille",
            "nature": "/app/frontend/assets/audio/nature", 
            "nombres": "/app/frontend/assets/audio/nombres",
            "animaux": "/app/frontend/assets/audio/animaux",
            "corps": "/app/frontend/assets/audio/corps",
            "salutations": "/app/frontend/assets/audio/salutations",
            "couleurs": "/app/frontend/assets/audio/couleurs",
            "grammaire": "/app/frontend/assets/audio/grammaire",
            "nourriture": "/app/frontend/assets/audio/nourriture",
            "verbes": "/app/frontend/assets/audio/verbes",
            "expressions": "/app/frontend/assets/audio/expressions",
            "adjectifs": "/app/frontend/assets/audio/adjectifs",
            "vetements": "/app/frontend/assets/audio/vetements",
            "maison": "/app/frontend/assets/audio/maison",
            "tradition": "/app/frontend/assets/audio/traditions",
            "transport": "/app/frontend/assets/audio/transport"
        }
        
        # Utiliser le dossier correspondant à la catégorie, famille par défaut
        audio_dir = audio_dirs.get(word_category, audio_dirs["famille"])
        file_path = os.path.join(audio_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Fichier audio non trouvé: {filename}")
        
        return FileResponse(
            file_path,
            media_type="audio/mp4",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de mot invalide")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/words/{word_id}/audio-info")
async def get_word_audio_info(word_id: str):
    """
    Récupère les informations audio d'un mot (système dual)
    """
    try:
        word_doc = words_collection.find_one({"_id": ObjectId(word_id)})
        if not word_doc:
            raise HTTPException(status_code=404, detail="Mot non trouvé")
        
        return {
            "word": {
                "id": word_id,
                "french": word_doc.get("french"),
                "shimaore": word_doc.get("shimaore"),
                "kibouchi": word_doc.get("kibouchi")
            },
            "dual_audio_system": word_doc.get("dual_audio_system", False),
            "audio": {
                "shimaore": {
                    "has_audio": word_doc.get("has_shimaoré_audio", False),
                    "filename": word_doc.get("audio_shimaoré_filename"),
                    "url": f"/api/words/{word_id}/audio/shimaore" if word_doc.get("has_shimaoré_audio") else None
                },
                "kibouchi": {
                    "has_audio": word_doc.get("has_kibouchi_audio", False),
                    "filename": word_doc.get("audio_kibouchi_filename"),
                    "url": f"/api/words/{word_id}/audio/kibouchi" if word_doc.get("has_kibouchi_audio") else None
                }
            },
            "legacy_audio": {
                "has_authentic_audio": word_doc.get("has_authentic_audio", False),
                "audio_filename": word_doc.get("audio_filename"),
                "audio_pronunciation_lang": word_doc.get("audio_pronunciation_lang")
            }
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de mot invalide")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

@app.get("/api/debug/audio/{word_id}/{lang}")
async def debug_audio_route(word_id: str, lang: str):
    """Route de debug pour l'audio"""
    try:
        from bson import ObjectId
        import os
        
        # Log de debug
        print(f"DEBUG: word_id={word_id}, lang={lang}")
        
        # Connexion DB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        collection = db['vocabulary']
        
        # Récupérer document
        try:
            obj_id = ObjectId(word_id)
        except Exception as e:
            return {"error": f"Invalid ObjectId: {e}"}
            
        word_doc = collection.find_one({"_id": obj_id})
        if not word_doc:
            return {"error": "Document not found"}
        
        # Récupérer filename
        if lang == "shimaore":
            filename = word_doc.get("audio_shimaoré_filename")
            has_audio = word_doc.get("has_shimaoré_audio", False)
        else:
            filename = word_doc.get("audio_kibouchi_filename") 
            has_audio = word_doc.get("has_kibouchi_audio", False)
        
        if not filename or not has_audio:
            return {"error": "No audio configured", "filename": filename, "has_audio": has_audio}
        
        # Vérifier fichier
        file_path = f"/app/frontend/assets/audio/verbes/{filename}"
        file_exists = os.path.exists(file_path)
        file_size = os.path.getsize(file_path) if file_exists else 0
        
        return {
            "word_id": word_id,
            "lang": lang,
            "filename": filename,
            "has_audio": has_audio,
            "file_path": file_path,
            "file_exists": file_exists,
            "file_size": file_size,
            "word_doc": {
                "french": word_doc.get("french"),
                "section": word_doc.get("section")
            }
        }
        
    except Exception as e:
        import traceback
        return {"error": f"Exception: {e}", "traceback": traceback.format_exc()}


@app.get("/api/audio/{word_id}/{lang}")
async def get_audio_file(word_id: str, lang: str):
    """Route audio simplifiée et fonctionnelle"""
    try:
        from pymongo import MongoClient
        from bson import ObjectId
        from fastapi.responses import FileResponse
        from fastapi import HTTPException
        import os
        
        # Validation langue
        if lang not in ["shimaore", "kibouchi"]:
            raise HTTPException(status_code=400, detail="Langue non supportée")
        
        # Connexion DB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_url)
        db = client['shimaoré_app']
        collection = db['vocabulary']
        
        # Récupérer le mot
        try:
            obj_id = ObjectId(word_id)
        except:
            raise HTTPException(status_code=400, detail="ID invalide")
            
        word_doc = collection.find_one({"_id": obj_id})
        if not word_doc:
            raise HTTPException(status_code=404, detail="Mot non trouvé")
        
        # Récupérer le fichier audio
        if lang == "shimaore":
            filename = word_doc.get("audio_shimaoré_filename")
            has_audio = word_doc.get("has_shimaoré_audio", False)
        else:


# ============================================
# SYSTÈME PREMIUM - Endpoints Utilisateurs
# ============================================

from premium_system import (
    create_user, get_user, upgrade_to_premium,
    get_words_for_user, update_user_activity, get_user_stats
)

@app.post("/api/users/register")
async def register_user(user_data: UserCreate):
    """Créer un nouvel utilisateur gratuit"""
    try:
        user = create_user(user_data.user_id, user_data.email)
        # Convertir ObjectId en string
        user["id"] = str(user["_id"])
        del user["_id"]
        return {"success": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}")
async def get_user_info(user_id: str):
    """Récupérer les informations d'un utilisateur"""
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Convertir ObjectId en string
        user["id"] = str(user["_id"])
        del user["_id"]
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users/{user_id}/upgrade")
async def upgrade_user_premium(user_id: str, upgrade_data: UpgradeRequest):
    """Simuler l'achat Premium (POUR TESTS - À remplacer par Stripe en production)"""
    try:
        user = upgrade_to_premium(user_id, upgrade_data.subscription_type)
        # Convertir ObjectId en string
        user["id"] = str(user["_id"])
        del user["_id"]
        
        return {
            "success": True,
            "message": "Upgrade Premium réussi! Bienvenue dans la communauté Premium Kwezi 🎉",
            "user": user
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}/stats")
async def get_user_statistics(user_id: str):
    """Récupérer les statistiques d'un utilisateur"""
    try:
        stats = get_user_stats(user_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users/{user_id}/activity")
async def update_activity(user_id: str, words_learned: int = 0, score: int = 0):
    """Mettre à jour l'activité d'un utilisateur"""
    try:
        user = update_user_activity(user_id, words_learned, score)
        # Convertir ObjectId en string
        user["id"] = str(user["_id"])
        del user["_id"]
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modifier l'endpoint /api/words pour supporter le système premium
@app.get("/api/words/premium")
async def get_words_premium(user_id: Optional[str] = None, category: Optional[str] = None):
    """Récupérer les mots avec limitation selon le statut premium"""
    try:
        result = get_words_for_user(user_id, category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

            filename = word_doc.get("audio_kibouchi_filename")
            has_audio = word_doc.get("has_kibouchi_audio", False)
        
        if not filename or not has_audio:
            raise HTTPException(status_code=404, detail=f"Pas d\'audio {lang}")
        
        # Chemin du fichier
        section = word_doc.get("section", "verbes")
        file_path = f"/app/frontend/assets/audio/{section}/{filename}"
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        return FileResponse(
            file_path,
            media_type="audio/mp4",
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

    uvicorn.run(app, host="0.0.0.0", port=8001)