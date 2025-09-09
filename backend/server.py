from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import base64
from bson import ObjectId

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models pour l'application éducative Mayotte
class Word(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    french: str
    shimaore: str
    kibouchi: str
    category: str  # famille, couleurs, animaux, salutations, nombres
    image_base64: Optional[str] = None
    audio_url: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=3)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WordCreate(BaseModel):
    french: str
    shimaore: str
    kibouchi: str
    category: str
    image_base64: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=3)

class Exercise(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # match_word_image, build_sentence, memory_game, quiz
    title: str
    description: str
    words: List[str]  # IDs des mots utilisés
    difficulty: int = Field(default=1, ge=1, le=3)
    points: int = Field(default=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExerciseCreate(BaseModel):
    type: str
    title: str
    description: str
    words: List[str]
    difficulty: int = Field(default=1, ge=1, le=3)
    points: int = Field(default=10)

class UserProgress(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str
    exercise_id: str
    score: int
    completed_at: datetime = Field(default_factory=datetime.utcnow)

class UserProgressCreate(BaseModel):
    user_name: str
    exercise_id: str
    score: int

# Routes pour les mots
@api_router.post("/words", response_model=Word)
async def create_word(word: WordCreate):
    word_dict = word.dict()
    word_obj = Word(**word_dict)
    await db.words.insert_one(word_obj.dict())
    return word_obj

@api_router.get("/words", response_model=List[Word])
async def get_words(category: Optional[str] = None):
    query = {}
    if category:
        query["category"] = category
    words = await db.words.find(query).to_list(1000)
    return [Word(**word) for word in words]

@api_router.get("/words/{word_id}", response_model=Word)
async def get_word(word_id: str):
    word = await db.words.find_one({"id": word_id})
    if not word:
        raise HTTPException(status_code=404, detail="Mot non trouvé")
    return Word(**word)

@api_router.put("/words/{word_id}", response_model=Word)
async def update_word(word_id: str, word: WordCreate):
    word_dict = word.dict()
    result = await db.words.update_one({"id": word_id}, {"$set": word_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Mot non trouvé")
    updated_word = await db.words.find_one({"id": word_id})
    return Word(**updated_word)

@api_router.delete("/words/{word_id}")
async def delete_word(word_id: str):
    result = await db.words.delete_one({"id": word_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Mot non trouvé")
    return {"message": "Mot supprimé avec succès"}

# Routes pour les exercices
@api_router.post("/exercises", response_model=Exercise)
async def create_exercise(exercise: ExerciseCreate):
    exercise_dict = exercise.dict()
    exercise_obj = Exercise(**exercise_dict)
    await db.exercises.insert_one(exercise_obj.dict())
    return exercise_obj

@api_router.get("/exercises", response_model=List[Exercise])
async def get_exercises(difficulty: Optional[int] = None):
    query = {}
    if difficulty:
        query["difficulty"] = difficulty
    exercises = await db.exercises.find(query).to_list(1000)
    return [Exercise(**exercise) for exercise in exercises]

@api_router.get("/exercises/{exercise_id}", response_model=Exercise)
async def get_exercise(exercise_id: str):
    exercise = await db.exercises.find_one({"id": exercise_id})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercice non trouvé")
    return Exercise(**exercise)

# Routes pour le progrès utilisateur
@api_router.post("/progress", response_model=UserProgress)
async def create_progress(progress: UserProgressCreate):
    progress_dict = progress.dict()
    progress_obj = UserProgress(**progress_dict)
    await db.user_progress.insert_one(progress_obj.dict())
    return progress_obj

@api_router.get("/progress/{user_name}", response_model=List[UserProgress])
async def get_user_progress(user_name: str):
    progress_list = await db.user_progress.find({"user_name": user_name}).to_list(1000)
    return [UserProgress(**progress) for progress in progress_list]

# Route pour uploader des images
@api_router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Lire le fichier et le convertir en base64
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode('utf-8')
        
        return {
            "success": True,
            "image_base64": f"data:{file.content_type};base64,{base64_image}",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

# Route pour initialiser du contenu de base
@api_router.post("/init-base-content")
async def init_base_content():
    # Contenu authentique complet en shimaoré et kibouchi basé sur les tableaux fournis (version finale)
    base_words = [
        # Corps humain  
        {"french": "Bouche", "shimaore": "Hangno", "kibouchi": "Vava", "category": "corps", "difficulty": 1},
        
        # Salutations et expressions courantes
        {"french": "Bonjour", "shimaore": "Kwezi", "kibouchi": "Kwezi", "category": "salutations", "difficulty": 1},
        {"french": "Comment ça va", "shimaore": "Jéjé", "kibouchi": "Akori", "category": "salutations", "difficulty": 1},
        {"french": "Ça va bien", "shimaore": "Fétré", "kibouchi": "Tsara", "category": "salutations", "difficulty": 1},
        {"french": "Merci", "shimaore": "Marahaba", "kibouchi": "Marahaba", "category": "salutations", "difficulty": 1},
        {"french": "Au revoir", "shimaore": "Kwaheri", "kibouchi": "Maeva", "category": "salutations", "difficulty": 1},
        {"french": "Oui", "shimaore": "Ewa", "kibouchi": "Iya", "category": "salutations", "difficulty": 1},
        {"french": "Non", "shimaore": "Anha", "kibouchi": "Anha", "category": "salutations", "difficulty": 1},
        {"french": "Excuse-moi", "shimaore": "Soimahani", "kibouchi": "Soimahani", "category": "salutations", "difficulty": 1},
        
        # Grammaire complète : Pronoms personnels et possessifs
        # Pronoms personnels
        {"french": "Je", "shimaore": "Wami", "kibouchi": "Zahou", "category": "grammaire", "difficulty": 1},
        {"french": "Tu", "shimaore": "Wawé", "kibouchi": "Anaou", "category": "grammaire", "difficulty": 1},
        {"french": "Il/Elle", "shimaore": "Wayé", "kibouchi": "Izi", "category": "grammaire", "difficulty": 1},
        {"french": "Nous", "shimaore": "Wassi", "kibouchi": "Atsika", "category": "grammaire", "difficulty": 1},
        {"french": "Ils/Elles", "shimaore": "Wawo", "kibouchi": "Réou", "category": "grammaire", "difficulty": 1},
        {"french": "Vous", "shimaore": "Wagnou", "kibouchi": "Anaréou", "category": "grammaire", "difficulty": 1},
        
        # Pronoms possessifs
        {"french": "Le mien", "shimaore": "Yangou", "kibouchi": "Ninakahi", "category": "grammaire", "difficulty": 2},
        {"french": "Le tien", "shimaore": "Yaho", "kibouchi": "Ninaou", "category": "grammaire", "difficulty": 2},
        {"french": "Le sien", "shimaore": "Yahé", "kibouchi": "Ninazi", "category": "grammaire", "difficulty": 2},
        {"french": "Le leur", "shimaore": "Yawo", "kibouchi": "Nindréou", "category": "grammaire", "difficulty": 2},
        {"french": "Le nôtre", "shimaore": "Yatrou", "kibouchi": "Nintsika", "category": "grammaire", "difficulty": 2},
        {"french": "Le vôtre", "shimaore": "Yagnou", "kibouchi": "Ninéyi", "category": "grammaire", "difficulty": 2},
        
        # Famille (vocabulaire familial étendu selon le tableau)
        # Parents directs
        {"french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", "category": "famille", "difficulty": 1},
        {"french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", "category": "famille", "difficulty": 1},
        {"french": "Enfant", "shimaore": "Mwana", "kibouchi": "Mwana", "category": "famille", "difficulty": 1},
        
        # Tantes et oncles
        {"french": "Tante", "shimaore": "Mama titi", "kibouchi": "Nindri heli", "category": "famille", "difficulty": 1},
        {"french": "Oncle maternel", "shimaore": "Zama", "kibouchi": "Zama", "category": "famille", "difficulty": 2},
        {"french": "Oncle paternel", "shimaore": "Baba titi", "kibouchi": "Baba héli", "category": "famille", "difficulty": 2},
        {"french": "Épouse oncle maternel", "shimaore": "Zena", "kibouchi": "Zena", "category": "famille", "difficulty": 2},
        
        # Frères et sœurs (avec nuances d'âge)
        {"french": "Petite sœur", "shimaore": "Moinagna mtroum", "kibouchi": "Zandri", "category": "famille", "difficulty": 1},
        {"french": "Petit frère", "shimaore": "Moinagna mtrouba", "kibouchi": "Zandri", "category": "famille", "difficulty": 1},
        {"french": "Grande sœur", "shimaore": "Zouki", "kibouchi": "Zoki", "category": "famille", "difficulty": 1},
        {"french": "Grand frère", "shimaore": "Zouki", "kibouchi": "Zoki", "category": "famille", "difficulty": 1},
        {"french": "Frère", "shimaore": "Mwanagna", "kibouchi": "Anadahi", "category": "famille", "difficulty": 1},
        {"french": "Sœur", "shimaore": "Mwanagna", "kibouchi": "Anabavi", "category": "famille", "difficulty": 1},
        
        # Relations sociales et genres
        {"french": "Ami", "shimaore": "Mwandzani", "kibouchi": "Mwandzani", "category": "famille", "difficulty": 1},
        {"french": "Fille", "shimaore": "Mtroumama", "kibouchi": "Viavi", "category": "famille", "difficulty": 1},
        {"french": "Garçon", "shimaore": "Mtroubaba", "kibouchi": "Lalahi", "category": "famille", "difficulty": 1},
        {"french": "Monsieur", "shimaore": "Mogné", "kibouchi": "Lalahi", "category": "famille", "difficulty": 1},
        {"french": "Madame", "shimaore": "Bwéni", "kibouchi": "Viavi", "category": "famille", "difficulty": 1},
        
        # Grands-parents
        {"french": "Grand-père", "shimaore": "Bacoco", "kibouchi": "Dadayi", "category": "famille", "difficulty": 1},
        {"french": "Grand-mère", "shimaore": "Coco", "kibouchi": "Dadi", "category": "famille", "difficulty": 1},
        
        # Couleurs (palette complète selon le tableau final)
        {"french": "Bleu", "shimaore": "Bilé", "kibouchi": "Bilé", "category": "couleurs", "difficulty": 1},
        {"french": "Vert", "shimaore": "Dhavou", "kibouchi": "Mayitsou", "category": "couleurs", "difficulty": 1},
        {"french": "Noir", "shimaore": "Nzidhou", "kibouchi": "Mayintigni", "category": "couleurs", "difficulty": 1},
        {"french": "Blanc", "shimaore": "Ndjéou", "kibouchi": "Malandi", "category": "couleurs", "difficulty": 1},
        {"french": "Rouge", "shimaore": "Ndzoukoundrou", "kibouchi": "Mena", "category": "couleurs", "difficulty": 1},
        {"french": "Jaune", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "couleurs", "difficulty": 1},
        {"french": "Marron", "shimaore": "Trotro", "kibouchi": "Fotafotaka", "category": "couleurs", "difficulty": 1},
        {"french": "Gris", "shimaore": "Djifou", "kibouchi": "Dzofou", "category": "couleurs", "difficulty": 1},
        
        # Animaux (liste complète mise à jour selon le nouveau tableau)
        {"french": "Abeille", "shimaore": "Niochi", "kibouchi": "Antéli", "category": "animaux", "difficulty": 1},
        {"french": "Margouillat", "shimaore": "Kasangwe", "kibouchi": "Kitsatsaka", "category": "animaux", "difficulty": 1},
        {"french": "Chat", "shimaore": "Paha", "kibouchi": "Moirou", "category": "animaux", "difficulty": 1},
        {"french": "Rat", "shimaore": "Pouhou", "kibouchi": "Voilavou", "category": "animaux", "difficulty": 1},
        {"french": "Escargot", "shimaore": "Kouéya", "kibouchi": "Ancora", "category": "animaux", "difficulty": 1},
        {"french": "Lion", "shimaore": "Simba", "kibouchi": "Simba", "category": "animaux", "difficulty": 2},
        {"french": "Grenouille", "shimaore": "Shiwatrotro", "kibouchi": "Sahougnou", "category": "animaux", "difficulty": 1},
        {"french": "Oiseau", "shimaore": "Gnougni", "kibouchi": "Vorougnou", "category": "animaux", "difficulty": 1},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "animaux", "difficulty": 1},
        {"french": "Maki", "shimaore": "Komba", "kibouchi": "Ankoumba", "category": "animaux", "difficulty": 1},
        {"french": "Chèvre", "shimaore": "Mbouzi", "kibouchi": "Bengui", "category": "animaux", "difficulty": 1},
        {"french": "Moustique", "shimaore": "Manundi", "kibouchi": "Mokou", "category": "animaux", "difficulty": 1},
        {"french": "Mouche", "shimaore": "Ndzi", "kibouchi": "Lalitri", "category": "animaux", "difficulty": 1},
        {"french": "Chauve-souris", "shimaore": "Drema", "kibouchi": "Fanihi", "category": "animaux", "difficulty": 1},
        {"french": "Serpent", "shimaore": "Nyoha", "kibouchi": "Bibi lava", "category": "animaux", "difficulty": 2},
        {"french": "Lapin", "shimaore": "Sungura", "kibouchi": "Shoungoura", "category": "animaux", "difficulty": 1},
        {"french": "Mouton", "shimaore": "Baribari", "kibouchi": "Baribari", "category": "animaux", "difficulty": 1},
        {"french": "Crocodile", "shimaore": "Vwai", "kibouchi": "Vwai", "category": "animaux", "difficulty": 2},
        {"french": "Caméléon", "shimaore": "Tarundru", "kibouchi": "Tarondru", "category": "animaux", "difficulty": 2},
        {"french": "Zébu", "shimaore": "Nyombe", "kibouchi": "Aoumbi", "category": "animaux", "difficulty": 1},
        {"french": "Âne", "shimaore": "Pundra", "kibouchi": "Ampundra", "category": "animaux", "difficulty": 1},
        {"french": "Poule", "shimaore": "Kouhou", "kibouchi": "Akohou", "category": "animaux", "difficulty": 1},
        {"french": "Fourmis", "shimaore": "Tsutsuhu", "kibouchi": "Visiki", "category": "animaux", "difficulty": 1},
        {"french": "Chien", "shimaore": "Mbwa", "kibouchi": "Fadroka", "category": "animaux", "difficulty": 1},
        {"french": "Papillon", "shimaore": "Pelapelaka", "kibouchi": "Tsipelapelaka", "category": "animaux", "difficulty": 1},
        {"french": "Ver de terre", "shimaore": "Njengwe", "kibouchi": "Bibi fotaka", "category": "animaux", "difficulty": 1},
        {"french": "Criquet", "shimaore": "Furudji", "kibouchi": "Kidzedza", "category": "animaux", "difficulty": 1},
        {"french": "Cochon", "shimaore": "Pouroukou", "kibouchi": "Lambou", "category": "animaux", "difficulty": 1},
        {"french": "Facochère", "shimaore": "Pouroukou nyeha", "kibouchi": "Lambou", "category": "animaux", "difficulty": 2},
        {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "category": "animaux", "difficulty": 1},
        {"french": "Chameau", "shimaore": "Ngamia", "kibouchi": "Angamia", "category": "animaux", "difficulty": 2},
        {"french": "Hérisson/Tangue", "shimaore": "Landra", "kibouchi": "Trandraka", "category": "animaux", "difficulty": 1},
        {"french": "Corbeau", "shimaore": "Gawa", "kibouchi": "Goika", "category": "animaux", "difficulty": 1},
        {"french": "Civette", "shimaore": "Foungo", "kibouchi": "Angava", "category": "animaux", "difficulty": 1},
        {"french": "Dauphin", "shimaore": "Camba", "kibouchi": "Fésoutrou", "category": "animaux", "difficulty": 1},
        {"french": "Baleine", "shimaore": "Droujou", "kibouchi": "Fesoutrou", "category": "animaux", "difficulty": 1},
        {"french": "Crevette", "shimaore": "Camba", "kibouchi": "Ancamba", "category": "animaux", "difficulty": 1},
        {"french": "Frelon", "shimaore": "Chonga", "kibouchi": "Faraka", "category": "animaux", "difficulty": 1},
        {"french": "Guêpe", "shimaore": "Movou", "kibouchi": "Fanintri", "category": "animaux", "difficulty": 1},
        {"french": "Bourdon", "shimaore": "Voungo voungo", "kibouchi": "Madjaoumbi", "category": "animaux", "difficulty": 1},
        {"french": "Puce", "shimaore": "Ndra", "kibouchi": "Howou", "category": "animaux", "difficulty": 1},
        {"french": "Bouc", "shimaore": "Béwé", "kibouchi": "Bébéroué", "category": "animaux", "difficulty": 1},
        {"french": "Taureau", "shimaore": "Kondzo", "kibouchi": "Dzow", "category": "animaux", "difficulty": 1},
        {"french": "Bigorneau", "shimaore": "Trondro", "kibouchi": "Trondrou", "category": "animaux", "difficulty": 1},
        {"french": "Lambis", "shimaore": "Komba", "kibouchi": "Mahombi", "category": "animaux", "difficulty": 1},
        {"french": "Cône de mer", "shimaore": "Tsipoui", "kibouchi": "Tsimtipaka", "category": "animaux", "difficulty": 1},
        {"french": "Mille pattes", "shimaore": "Mjongo", "kibouchi": "Ancoudavitri", "category": "animaux", "difficulty": 1},
        
        # Nombres (corrigés selon le tableau final)
        {"french": "Un", "shimaore": "Moja", "kibouchi": "Areki", "category": "nombres", "difficulty": 1},
        {"french": "Deux", "shimaore": "Mbili", "kibouchi": "Aroyi", "category": "nombres", "difficulty": 1},
        {"french": "Trois", "shimaore": "Trarou", "kibouchi": "Telou", "category": "nombres", "difficulty": 1},
        {"french": "Quatre", "shimaore": "Nhé", "kibouchi": "Efatra", "category": "nombres", "difficulty": 1},
        {"french": "Cinq", "shimaore": "Tsano", "kibouchi": "Dimi", "category": "nombres", "difficulty": 1},
        {"french": "Six", "shimaore": "Sita", "kibouchi": "Tchouta", "category": "nombres", "difficulty": 1},
        {"french": "Sept", "shimaore": "Saba", "kibouchi": "Fitou", "category": "nombres", "difficulty": 1},
        {"french": "Huit", "shimaore": "Nané", "kibouchi": "Valou", "category": "nombres", "difficulty": 1},
        {"french": "Neuf", "shimaore": "Chendra", "kibouchi": "Civi", "category": "nombres", "difficulty": 1},
        {"french": "Dix", "shimaore": "Koumi", "kibouchi": "Foulou", "category": "nombres", "difficulty": 1},
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
        
        # Corps humain (mise à jour complète selon le nouveau tableau)
        {"french": "Œil", "shimaore": "Matso", "kibouchi": "Faninti", "category": "corps", "difficulty": 1},
        {"french": "Nez", "shimaore": "Poua", "kibouchi": "Horougnou", "category": "corps", "difficulty": 1},
        {"french": "Oreille", "shimaore": "Kiyo", "kibouchi": "Soufigni", "category": "corps", "difficulty": 1},
        {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou", "category": "corps", "difficulty": 1},
        {"french": "Front", "shimaore": "Housso", "kibouchi": "Lahara", "category": "corps", "difficulty": 1},
        {"french": "Joue", "shimaore": "Savou", "kibouchi": "Fifi", "category": "corps", "difficulty": 1},
        {"french": "Dos", "shimaore": "Mengo", "kibouchi": "Vohou", "category": "corps", "difficulty": 1},
        {"french": "Épaule", "shimaore": "Béga", "kibouchi": "Haveyi", "category": "corps", "difficulty": 1},
        {"french": "Hanche", "shimaore": "Trenga", "kibouchi": "Tahezagna", "category": "corps", "difficulty": 1},
        {"french": "Fesses", "shimaore": "Shidze/Mvoumo", "kibouchi": "Fouri", "category": "corps", "difficulty": 1},
        {"french": "Main", "shimaore": "Mhono", "kibouchi": "Tagnana", "category": "corps", "difficulty": 1},
        {"french": "Tête", "shimaore": "Shitsoi", "kibouchi": "Louha", "category": "corps", "difficulty": 1},
        {"french": "Ventre", "shimaore": "Mimba", "kibouchi": "Kibou", "category": "corps", "difficulty": 1},
        {"french": "Dent", "shimaore": "Magno", "kibouchi": "Hifi", "category": "corps", "difficulty": 1},
        {"french": "Langue", "shimaore": "Oulimé", "kibouchi": "Léla", "category": "corps", "difficulty": 1},
        {"french": "Pied", "shimaore": "Mindrou", "kibouchi": "Viti", "category": "corps", "difficulty": 1},
        {"french": "Lèvre", "shimaore": "Dhomo", "kibouchi": "Soungni", "category": "corps", "difficulty": 1},
        {"french": "Peau", "shimaore": "Ngwezi", "kibouchi": "Ngwezi", "category": "corps", "difficulty": 1},
        {"french": "Cheveux", "shimaore": "Ngnélé", "kibouchi": "Fagnéva", "category": "corps", "difficulty": 1},
        {"french": "Doigts", "shimaore": "Cha", "kibouchi": "Tondrou", "category": "corps", "difficulty": 1},
        {"french": "Barbe", "shimaore": "Ndrévou", "kibouchi": "Somboutrou", "category": "corps", "difficulty": 1},
        {"french": "Vagin", "shimaore": "Ndzigni", "kibouchi": "Tingui", "category": "corps", "difficulty": 1},
        {"french": "Testicules", "shimaore": "Kwendzé", "kibouchi": "Vouancarou", "category": "corps", "difficulty": 1},
        {"french": "Pénis", "shimaore": "Mbo", "kibouchi": "Kaboudzi", "category": "corps", "difficulty": 1},
        {"french": "Menton", "shimaore": "Shlévou", "kibouchi": "Sokou", "category": "corps", "difficulty": 1},
        {"french": "Bouche", "shimaore": "Hangno", "kibouchi": "Vava", "category": "corps", "difficulty": 1},
        {"french": "Côtes", "shimaore": "Bavou", "kibouchi": "Mbavou", "category": "corps", "difficulty": 1},
        {"french": "Sourcil", "shimaore": "Tsi", "kibouchi": "Ankwéssi", "category": "corps", "difficulty": 1},
        {"french": "Cheville", "shimaore": "Dzitso la pwédza", "kibouchi": "Dzitso la pwédza", "category": "corps", "difficulty": 1},
        {"french": "Cou", "shimaore": "Tsingo", "kibouchi": "Vouzougnou", "category": "corps", "difficulty": 1},
        {"french": "Cils", "shimaore": "Kové", "kibouchi": "Rambou faninti", "category": "corps", "difficulty": 1},
        {"french": "Arrière du crâne", "shimaore": "Komoi", "kibouchi": "Kitoika", "category": "corps", "difficulty": 1},
        
        # Nourriture (mises à jour selon le nouveau tableau)
        
        # Verbes supplémentaires des tableaux 4 et 5
        {"french": "Faire sécher", "shimaore": "Ouhoumisa", "kibouchi": "Manapi", "category": "verbes", "difficulty": 1},
        {"french": "Balayer", "shimaore": "Ouhoundza", "kibouchi": "Mamafa", "category": "verbes", "difficulty": 1},
        {"french": "Couper", "shimaore": "Oukatra", "kibouchi": "Manapaka", "category": "verbes", "difficulty": 1},
        {"french": "Tremper", "shimaore": "Oulodza", "kibouchi": "Mandzoubougnou", "category": "verbes", "difficulty": 1},
        {"french": "Se raser", "shimaore": "Oumea ndrevu", "kibouchi": "Manapaka somboutrou", "category": "verbes", "difficulty": 1},
        {"french": "Abîmer", "shimaore": "Oumengna", "kibouchi": "Mandroubaka", "category": "verbes", "difficulty": 1},
        {"french": "Acheter", "shimaore": "Ounounoua", "kibouchi": "Mivanga", "category": "verbes", "difficulty": 1},
        {"french": "Griller", "shimaore": "Ouwoha", "kibouchi": "Mitonou", "category": "verbes", "difficulty": 1},
        {"french": "Allumer", "shimaore": "Oupatsa", "kibouchi": "Mikoupatsa", "category": "verbes", "difficulty": 1},
        {"french": "Se peigner", "shimaore": "Oupengné", "kibouchi": "Mipéngni", "category": "verbes", "difficulty": 1},
        {"french": "Cuisiner", "shimaore": "Oupiha", "kibouchi": "Mahandrou", "category": "verbes", "difficulty": 1},
        {"french": "Ranger/Arranger", "shimaore": "Ourenguélédza", "kibouchi": "Magnadzari", "category": "verbes", "difficulty": 1},
        {"french": "Tresser", "shimaore": "Oussouká", "kibouchi": "Mitali/Mandrari", "category": "verbes", "difficulty": 1},
        {"french": "Peindre", "shimaore": "Ouvaha", "kibouchi": "Magnossoutrou", "category": "verbes", "difficulty": 1},
        {"french": "Essuyer", "shimaore": "Ouvangouha", "kibouchi": "Mamitri", "category": "verbes", "difficulty": 1},
        {"french": "Amener/Apporter", "shimaore": "Ouvinga", "kibouchi": "Mandéyi", "category": "verbes", "difficulty": 1},
        {"french": "Éteindre", "shimaore": "Ouzima", "kibouchi": "Mamounou", "category": "verbes", "difficulty": 1},
        {"french": "Tuer", "shimaore": "Ouwoula", "kibouchi": "Mamounou", "category": "verbes", "difficulty": 1},
        {"french": "Combler", "shimaore": "Oufitsiya", "kibouchi": "Mankahampi", "category": "verbes", "difficulty": 2},
        {"french": "Cultiver", "shimaore": "Oulima", "kibouchi": "Mikapa", "category": "verbes", "difficulty": 1},
        {"french": "Couper du bois", "shimaore": "Oupasouha kuni", "kibouchi": "Mamaki azoumati", "category": "verbes", "difficulty": 2},
        {"french": "Cueillir", "shimaore": "Oupoua", "kibouchi": "Mampoka", "category": "verbes", "difficulty": 1},
        {"french": "Eau", "shimaore": "Madji", "kibouchi": "Rano", "category": "nourriture", "difficulty": 1},
        {"french": "Riz", "shimaore": "Tsohole", "kibouchi": "Vari", "category": "nourriture", "difficulty": 1},
        {"french": "Nourriture", "shimaore": "Chaoula", "kibouchi": "Hanigni", "category": "nourriture", "difficulty": 1},
        {"french": "Pain", "shimaore": "Dipé", "kibouchi": "Dipé", "category": "nourriture", "difficulty": 1},
        {"french": "Gâteau", "shimaore": "Mharé", "kibouchi": "Moukari", "category": "nourriture", "difficulty": 1},
        {"french": "Banane", "shimaore": "Danassi", "kibouchi": "Fouhi", "category": "nourriture", "difficulty": 1},
        {"french": "Mangue", "shimaore": "Kouweya", "kibouchi": "Ankora", "category": "nourriture", "difficulty": 1},
        {"french": "Coco", "shimaore": "Nazi", "kibouchi": "Vounia", "category": "nourriture", "difficulty": 1},
        {"french": "Lait", "shimaore": "Maziwa", "kibouchi": "Roungoua", "category": "nourriture", "difficulty": 1},
        {"french": "Viande", "shimaore": "Hanyama", "kibouchi": "Saloha", "category": "nourriture", "difficulty": 1},
        {"french": "Poisson", "shimaore": "Samana", "kibouchi": "Lakou", "category": "nourriture", "difficulty": 1},
        
        # Maison (mises à jour selon le nouveau tableau)
        {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou", "category": "maison", "difficulty": 1},
        {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavarangna", "category": "maison", "difficulty": 1},
        {"french": "Fenêtre", "shimaore": "Dirisha", "kibouchi": "Varavaragnouhou", "category": "maison", "difficulty": 1},
        {"french": "Toit", "shimaore": "Kapu", "kibouchi": "Tafo", "category": "maison", "difficulty": 1},
        {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani", "category": "maison", "difficulty": 1},
        
        # Vêtements
        {"french": "Vêtement", "shimaore": "Nguo", "kibouchi": "Lamban", "category": "vetements", "difficulty": 1},
        {"french": "Chemise", "shimaore": "Shati", "kibouchi": "Pataloha", "category": "vetements", "difficulty": 1},
        {"french": "Pantalon", "shimaore": "Suruali", "kibouchi": "Pataloha", "category": "vetements", "difficulty": 1},
        
        # Verbes d'action complets (basés exactement sur les 5 tableaux fournis)
        # Tableau 1 - Verbes fondamentaux
        {"french": "Jouer", "shimaore": "Ounguadza", "kibouchi": "Msoma", "category": "verbes", "difficulty": 1},
        {"french": "Courir", "shimaore": "Wendra mbiyo", "kibouchi": "Miloumeyi", "category": "verbes", "difficulty": 1},
        {"french": "Dire", "shimaore": "Ourongoa", "kibouchi": "Mangnabara", "category": "verbes", "difficulty": 1},
        {"french": "Pouvoir", "shimaore": "Ouchindra", "kibouchi": "Mahaléou", "category": "verbes", "difficulty": 1},
        {"french": "Vouloir", "shimaore": "Outsaha", "kibouchi": "Chokou", "category": "verbes", "difficulty": 1},
        {"french": "Savoir", "shimaore": "Oujoua", "kibouchi": "Méhéyi", "category": "verbes", "difficulty": 1},
        {"french": "Voir", "shimaore": "Ouona", "kibouchi": "Mahita", "category": "verbes", "difficulty": 1},
        {"french": "Devoir", "shimaore": "Oulazimou", "kibouchi": "Tokoutrou", "category": "verbes", "difficulty": 1},
        {"french": "Venir", "shimaore": "Ouja", "kibouchi": "Havi", "category": "verbes", "difficulty": 1},
        {"french": "Rapprocher", "shimaore": "Outsengueléya", "kibouchi": "Magnatougnou", "category": "verbes", "difficulty": 2},
        {"french": "Prendre", "shimaore": "Ourenga", "kibouchi": "Mangala", "category": "verbes", "difficulty": 1},
        {"french": "Donner", "shimaore": "Ouva", "kibouchi": "Magnamiya", "category": "verbes", "difficulty": 1},
        {"french": "Parler", "shimaore": "Oulagoua", "kibouchi": "Mivoulangna", "category": "verbes", "difficulty": 1},
        {"french": "Mettre", "shimaore": "Outria", "kibouchi": "Mangnanou", "category": "verbes", "difficulty": 1},
        {"french": "Passer", "shimaore": "Ouvira", "kibouchi": "Mihomba", "category": "verbes", "difficulty": 1},
        {"french": "Trouver", "shimaore": "Oupara", "kibouchi": "Mahazou", "category": "verbes", "difficulty": 1},
        {"french": "Aimer", "shimaore": "Ouvendza", "kibouchi": "Mitiya", "category": "verbes", "difficulty": 1},
        {"french": "Croire", "shimaore": "Ouamini", "kibouchi": "Koimini", "category": "verbes", "difficulty": 1},
        {"french": "Penser", "shimaore": "Oufikiri", "kibouchi": "Midzéri", "category": "verbes", "difficulty": 1},
        {"french": "Connaître", "shimaore": "Oujoua", "kibouchi": "Méhéyi", "category": "verbes", "difficulty": 1},
        {"french": "Demander", "shimaore": "Oudzissa", "kibouchi": "Magnoutani", "category": "verbes", "difficulty": 1},
        {"french": "Répondre", "shimaore": "Oudjibou", "kibouchi": "Mikoudjibou", "category": "verbes", "difficulty": 1},
        {"french": "Laisser", "shimaore": "Oulicha", "kibouchi": "Mangnambéla", "category": "verbes", "difficulty": 1},
        {"french": "Manger", "shimaore": "Oudhya", "kibouchi": "Mihinagna", "category": "verbes", "difficulty": 1},
        {"french": "Boire", "shimaore": "Ounnoua", "kibouchi": "Mindranou", "category": "verbes", "difficulty": 1},
        {"french": "Lire", "shimaore": "Ousoma", "kibouchi": "Midzorou", "category": "verbes", "difficulty": 1},
        {"french": "Écrire", "shimaore": "Ouhanguiha", "kibouchi": "Mikouandika", "category": "verbes", "difficulty": 1},
        
        # Tableau 2 - Verbes d'action suite
        {"french": "Écouter", "shimaore": "Ouvoulkia", "kibouchi": "Mitangréngni", "category": "verbes", "difficulty": 1},
        {"french": "Apprendre", "shimaore": "Oufoundriha", "kibouchi": "Midzorou", "category": "verbes", "difficulty": 1},
        {"french": "Comprendre", "shimaore": "Ouéléwa", "kibouchi": "Kouéléwa", "category": "verbes", "difficulty": 1},
        {"french": "Jouer", "shimaore": "Ounguadza", "kibouchi": "Missoma", "category": "verbes", "difficulty": 1},
        {"french": "Marcher", "shimaore": "Ouendra", "kibouchi": "Mandéha", "category": "verbes", "difficulty": 1},
        {"french": "Entrer", "shimaore": "Ounguiya", "kibouchi": "Miditri", "category": "verbes", "difficulty": 1},
        {"french": "Sortir", "shimaore": "Oulawa", "kibouchi": "Miboka", "category": "verbes", "difficulty": 1},
        {"french": "Rester", "shimaore": "Ouketsi", "kibouchi": "Mipétraka", "category": "verbes", "difficulty": 1},
        {"french": "Vivre", "shimaore": "Ouyinchi", "kibouchi": "Mikouénchi", "category": "verbes", "difficulty": 1},
        {"french": "Dormir", "shimaore": "Oulala", "kibouchi": "Mandri", "category": "verbes", "difficulty": 1},
        {"french": "Attendre", "shimaore": "Oulindra", "kibouchi": "Mandigni", "category": "verbes", "difficulty": 1},
        {"french": "Suivre", "shimaore": "Oulounga", "kibouchi": "Mangnaraka", "category": "verbes", "difficulty": 1},
        {"french": "Tenir", "shimaore": "Oussika", "kibouchi": "Mitana", "category": "verbes", "difficulty": 1},
        {"french": "Ouvrir", "shimaore": "Ouboua", "kibouchi": "Mampibiyangna", "category": "verbes", "difficulty": 1},
        {"french": "Fermer", "shimaore": "Oubala", "kibouchi": "Migadra", "category": "verbes", "difficulty": 1},
        {"french": "Sembler", "shimaore": "Oufana", "kibouchi": "Mampihiragna", "category": "verbes", "difficulty": 1},
        {"french": "Paraître", "shimaore": "Ouwonéhoua", "kibouchi": "", "category": "verbes", "difficulty": 1},
        {"french": "Devenir", "shimaore": "Ougawouha", "kibouchi": "Mivadiki", "category": "verbes", "difficulty": 2},
        {"french": "Tomber", "shimaore": "Oupouliha", "kibouchi": "Latsaka", "category": "verbes", "difficulty": 1},
        {"french": "Se rappeler", "shimaore": "Oumaézi", "kibouchi": "Koufahamou", "category": "verbes", "difficulty": 2},
        {"french": "Commencer", "shimaore": "Ouhandrissa", "kibouchi": "Mitaponou", "category": "verbes", "difficulty": 1},
        {"french": "Finir", "shimaore": "Oumalidza", "kibouchi": "Mankéfa", "category": "verbes", "difficulty": 1},
        {"french": "Réussir", "shimaore": "Ouchindra", "kibouchi": "Mahaléou", "category": "verbes", "difficulty": 1},
        
        # Tableau 3 - Verbes d'action complexes
        {"french": "Essayer", "shimaore": "Oudjérébou", "kibouchi": "Mikoudjérébou", "category": "verbes", "difficulty": 1},
        {"french": "Attraper", "shimaore": "Oubara", "kibouchi": "Missamboutrou", "category": "verbes", "difficulty": 1},
        {"french": "Flatuler", "shimaore": "Oujamba", "kibouchi": "Manguétoutrou", "category": "verbes", "difficulty": 2},
        {"french": "Traverser", "shimaore": "Ouchiya", "kibouchi": "Mitsaka", "category": "verbes", "difficulty": 1},
        {"french": "Sauter", "shimaore": "Ouarouka", "kibouchi": "Mivongna", "category": "verbes", "difficulty": 1},
        {"french": "Frapper", "shimaore": "Ourema", "kibouchi": "Mamangou", "category": "verbes", "difficulty": 1},
        {"french": "Faire caca", "shimaore": "Ougna madzi", "kibouchi": "Manguéri", "category": "verbes", "difficulty": 1},
        {"french": "Faire pipi", "shimaore": "Ougna kojo", "kibouchi": "Mamani", "category": "verbes", "difficulty": 1},
        {"french": "Vomir", "shimaore": "Ouraviha", "kibouchi": "Mandouwya", "category": "verbes", "difficulty": 1},
        {"french": "S'asseoir", "shimaore": "Ouketsi", "kibouchi": "Mipétraka", "category": "verbes", "difficulty": 1},
        {"french": "Danser", "shimaore": "Ouzina", "kibouchi": "Mitsindzaka", "category": "verbes", "difficulty": 1},
        {"french": "Arrêter", "shimaore": "Ouziya", "kibouchi": "Mitsahatra", "category": "verbes", "difficulty": 1},
        {"french": "Vendre", "shimaore": "Ouhoudza", "kibouchi": "Mandafou", "category": "verbes", "difficulty": 1},
        {"french": "Cracher", "shimaore": "Outra marré", "kibouchi": "Mandrora", "category": "verbes", "difficulty": 1},
        {"french": "Mordre", "shimaore": "Ouka magno", "kibouchi": "Mangnékitri", "category": "verbes", "difficulty": 1},
        {"french": "Gratter", "shimaore": "Oukouwa", "kibouchi": "Mihotrou", "category": "verbes", "difficulty": 1},
        {"french": "Embrasser", "shimaore": "Ounouka", "kibouchi": "Mihoroukou", "category": "verbes", "difficulty": 1},
        {"french": "Jeter", "shimaore": "Ouvoutsa", "kibouchi": "Manopi", "category": "verbes", "difficulty": 1},
        {"french": "Avertir", "shimaore": "Outahadaricha", "kibouchi": "Mampahéyi", "category": "verbes", "difficulty": 2},
        {"french": "Informer", "shimaore": "Oujoudza", "kibouchi": "Mangnabara", "category": "verbes", "difficulty": 2},
        {"french": "Se laver le derrière", "shimaore": "Outsamba", "kibouchi": "Mambouyi", "category": "verbes", "difficulty": 1},
        {"french": "Se laver", "shimaore": "Ouhowa", "kibouchi": "Misséki", "category": "verbes", "difficulty": 1},
        {"french": "Piler", "shimaore": "Oudoudoua", "kibouchi": "Mandissa", "category": "verbes", "difficulty": 1},
        {"french": "Changer", "shimaore": "Ougaoudza", "kibouchi": "Mamadiki", "category": "verbes", "difficulty": 1},
        
        # Tableau 4 - Verbes domestiques et techniques
        {"french": "Étendre au soleil", "shimaore": "Ouaniha", "kibouchi": "Manapi", "category": "verbes", "difficulty": 2},
        {"french": "Réchauffer", "shimaore": "Ouhelesedza", "kibouchi": "Mamana", "category": "verbes", "difficulty": 1},
        {"french": "Se baigner", "shimaore": "Ouhowa", "kibouchi": "Misséki", "category": "verbes", "difficulty": 1},
        {"french": "Faire le lit", "shimaore": "Ouhodza", "kibouchi": "Mandzari koubani", "category": "verbes", "difficulty": 1},
        {"french": "Faire sécher", "shimaore": "Ouhoumisa", "kibouchi": "Manapi", "category": "verbes", "difficulty": 1},
        {"french": "Balayer", "shimaore": "Ouhoundza", "kibouchi": "Mamafa", "category": "verbes", "difficulty": 1},
        {"french": "Couper", "shimaore": "Oukatra", "kibouchi": "Manapaka", "category": "verbes", "difficulty": 1},
        {"french": "Tremper", "shimaore": "Oulodza", "kibouchi": "Mandzoubougnou", "category": "verbes", "difficulty": 1},
        {"french": "Se raser", "shimaore": "Oumea ndrevu", "kibouchi": "Manapaka somboutrou", "category": "verbes", "difficulty": 1},
        {"french": "Abîmer", "shimaore": "Oumengna", "kibouchi": "Mandroubaka", "category": "verbes", "difficulty": 1},
        {"french": "Entrer", "shimaore": "Ounguiya", "kibouchi": "Mihiditri", "category": "verbes", "difficulty": 1},
        {"french": "Acheter", "shimaore": "Ounounoua", "kibouchi": "Mivanga", "category": "verbes", "difficulty": 1},
        {"french": "Griller", "shimaore": "Ouwoha", "kibouchi": "Mitonou", "category": "verbes", "difficulty": 1},
        {"french": "Allumer", "shimaore": "Oupatsa", "kibouchi": "Mikoupatsa", "category": "verbes", "difficulty": 1},
        {"french": "Se peigner", "shimaore": "Oupengné", "kibouchi": "Mipéngni", "category": "verbes", "difficulty": 1},
        {"french": "Cuisiner", "shimaore": "Oupiha", "kibouchi": "Mahandrou", "category": "verbes", "difficulty": 1},
        {"french": "Ranger/Arranger", "shimaore": "Ourenguélédza", "kibouchi": "Magnadzari", "category": "verbes", "difficulty": 1},
        {"french": "Tresser", "shimaore": "Oussouká", "kibouchi": "Mitali/Mandrari", "category": "verbes", "difficulty": 1},
        {"french": "Peindre", "shimaore": "Ouvaha", "kibouchi": "Magnossoutrou", "category": "verbes", "difficulty": 1},
        {"french": "Essuyer", "shimaore": "Ouvangouha", "kibouchi": "Mamitri", "category": "verbes", "difficulty": 1},
        {"french": "Amener/Apporter", "shimaore": "Ouvinga", "kibouchi": "Mandéyi", "category": "verbes", "difficulty": 1},
        {"french": "Éteindre", "shimaore": "Ouzima", "kibouchi": "Mamounou", "category": "verbes", "difficulty": 1},
        {"french": "Tuer", "shimaore": "Ouwoula", "kibouchi": "Mamounou", "category": "verbes", "difficulty": 1},
        {"french": "Combler", "shimaore": "Oufitsiya", "kibouchi": "Mankahampi", "category": "verbes", "difficulty": 2},
        {"french": "Cultiver", "shimaore": "Oulima", "kibouchi": "Mikapa", "category": "verbes", "difficulty": 1},
        {"french": "Couper du bois", "shimaore": "Oupasouha kuni", "kibouchi": "Mamaki azoumati", "category": "verbes", "difficulty": 2},
        {"french": "Cueillir", "shimaore": "Oupoua", "kibouchi": "Mampoka", "category": "verbes", "difficulty": 1},
        
        # Tableau 5 - Verbes agricoles et artisanaux
        {"french": "Planter", "shimaore": "Outabou", "kibouchi": "Mamboli", "category": "verbes", "difficulty": 1},
        {"french": "Creuser", "shimaore": "Outsimba", "kibouchi": "Mangadi", "category": "verbes", "difficulty": 1},
        {"french": "Récolter", "shimaore": "Ouvouna", "kibouchi": "Mampouka", "category": "verbes", "difficulty": 1},
        {"french": "Bouger", "shimaore": "Outsengueléya", "kibouchi": "Mitéki", "category": "verbes", "difficulty": 1},
        
        # Nature (mises à jour selon le nouveau tableau)
        {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou", "category": "nature", "difficulty": 1},
        {"french": "Fleur", "shimaore": "Uwa", "kibouchi": "Vonindro", "category": "nature", "difficulty": 1},
        {"french": "Soleil", "shimaore": "Djuwa", "kibouchi": "Kouva", "category": "nature", "difficulty": 1},
        {"french": "Lune", "shimaore": "Mwezi", "kibouchi": "Volana", "category": "nature", "difficulty": 1},
        {"french": "Étoile", "shimaore": "Nyota", "kibouchi": "Kintana", "category": "nature", "difficulty": 1},
        {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari", "category": "nature", "difficulty": 1},
        {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni", "category": "nature", "difficulty": 1},
        {"french": "Montagne", "shimaore": "Mlima", "kibouchi": "Tendromby", "category": "nature", "difficulty": 1},
        {"french": "Pierre", "shimaore": "Jiwe", "kibouchi": "Vato", "category": "nature", "difficulty": 1},
        {"french": "Sable", "shimaore": "Mshanga", "kibouchi": "Fasika", "category": "nature", "difficulty": 1},
        
        # Transport
        {"french": "Voiture", "shimaore": "Galou", "kibouchi": "Tselatra", "category": "transport", "difficulty": 1},
        {"french": "Bateau", "shimaore": "Galawa", "kibouchi": "Sambo", "category": "transport", "difficulty": 1},
        
        # Reptiles et autres animaux
        {"french": "Lézard", "shimaore": "Ngwizi", "kibouchi": "Kitsatsaka", "category": "animaux", "difficulty": 2},
        {"french": "Renard", "shimaore": "Mbwa nyeha", "kibouchi": "Fandroka", "category": "animaux", "difficulty": 2},

        {"french": "Hérisson", "shimaore": "Landra", "kibouchi": "Trandraka", "category": "animaux", "difficulty": 2},
        {"french": "Ongle", "shimaore": "Kofou", "kibouchi": "Angofou", "category": "corps", "difficulty": 2}
    ]
    
    # Vérifier si le contenu existe déjà
    existing_count = await db.words.count_documents({})
    if existing_count > 0:
        return {"message": "Le contenu de base existe déjà", "count": existing_count}
    
    # Insérer le contenu de base
    for word_data in base_words:
        word_obj = Word(**word_data)
        await db.words.insert_one(word_obj.dict())
    
    # Créer quelques exercices de base
    base_exercises = [
        {
            "type": "match_word_image",
            "title": "Apprendre la famille",
            "description": "Associe les mots français avec leur traduction",
            "words": [],  # Sera rempli avec les IDs des mots de famille
            "difficulty": 1,
            "points": 10
        },
        {
            "type": "quiz",
            "title": "Quiz des salutations",
            "description": "Teste tes connaissances sur les salutations",
            "words": [],
            "difficulty": 1,
            "points": 15
        }
    ]
    
    for exercise_data in base_exercises:
        exercise_obj = Exercise(**exercise_data)
        await db.exercises.insert_one(exercise_obj.dict())
    
    return {"message": "Contenu de base initialisé avec succès", "words_added": len(base_words)}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()