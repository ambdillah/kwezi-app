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
        
        # Métiers et professions (complément grammaire)
        {"french": "Professeur", "shimaore": "Foundi", "kibouchi": "Foundi", "category": "grammaire", "difficulty": 1},
        {"french": "Guide spirituel", "shimaore": "Cadhi", "kibouchi": "Cadhi", "category": "grammaire", "difficulty": 1},
        {"french": "Imam", "shimaore": "Imamou", "kibouchi": "Imamou", "category": "grammaire", "difficulty": 1},
        {"french": "Voisin", "shimaore": "Djirani", "kibouchi": "Djirani", "category": "grammaire", "difficulty": 1},
        {"french": "Maire", "shimaore": "Mera", "kibouchi": "Mera", "category": "grammaire", "difficulty": 1},
        {"french": "Élu", "shimaore": "Dhoimana", "kibouchi": "Dhoimana", "category": "grammaire", "difficulty": 1},
        {"french": "Pêcheur", "shimaore": "Mlozi", "kibouchi": "Ampamintagna", "category": "grammaire", "difficulty": 1},
        {"french": "Agriculteur", "shimaore": "Mlimizi", "kibouchi": "Ampikapa", "category": "grammaire", "difficulty": 1},
        {"french": "Éleveur", "shimaore": "Mtsounga", "kibouchi": "Ampitsounga", "category": "grammaire", "difficulty": 1},
        
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
        
        # Animaux supplémentaires du nouveau tableau
        {"french": "Pigeon", "shimaore": "Ndiwa", "kibouchi": "Ndiwa", "category": "animaux", "difficulty": 1},
        {"french": "Chenille", "shimaore": "Bibimangidji", "kibouchi": "Bibimanguidi", "category": "animaux", "difficulty": 1},
        {"french": "Cheval", "shimaore": "Farassi", "kibouchi": "Farassi", "category": "animaux", "difficulty": 1},
        {"french": "Perroquet", "shimaore": "Kasuku", "kibouchi": "Kararokou", "category": "animaux", "difficulty": 2},
        {"french": "Cafard", "shimaore": "Kalalawi", "kibouchi": "Kalalowou", "category": "animaux", "difficulty": 1},
        {"french": "Araignée", "shimaore": "Shitrandrabwibwi", "kibouchi": "Bibi ampamani massou", "category": "animaux", "difficulty": 2},
        {"french": "Scorpion", "shimaore": "Hala", "kibouchi": "Hala", "category": "animaux", "difficulty": 2},
        {"french": "Scolopandre", "shimaore": "Trambwi", "kibouchi": "Trambougnou", "category": "animaux", "difficulty": 2},
        {"french": "Thon", "shimaore": "Mbassi", "kibouchi": "Mbassi", "category": "animaux", "difficulty": 1},
        {"french": "Requin", "shimaore": "Papa", "kibouchi": "Ankiou", "category": "animaux", "difficulty": 2},
        {"french": "Poulpe", "shimaore": "Pwedza", "kibouchi": "Pwedza", "category": "animaux", "difficulty": 1},
        {"french": "Crabe", "shimaore": "Dradraka", "kibouchi": "Dakatra", "category": "animaux", "difficulty": 1},
        {"french": "Tortue", "shimaore": "Nyamba/Katsa", "kibouchi": "Fanou", "category": "animaux", "difficulty": 1},
        {"french": "Éléphant", "shimaore": "Ndovu", "kibouchi": "Ndovu", "category": "animaux", "difficulty": 2},
        {"french": "Singe", "shimaore": "Djakwe", "kibouchi": "Djakouayi", "category": "animaux", "difficulty": 1},
        {"french": "Souris", "shimaore": "Shikwetse", "kibouchi": "Voilavou", "category": "animaux", "difficulty": 1},
        
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
        # Nourriture (mise à jour complète selon le nouveau tableau)
        {"french": "Riz", "shimaore": "Tsoholé", "kibouchi": "Vari", "category": "nourriture", "difficulty": 1},
        {"french": "Eau", "shimaore": "Maji", "kibouchi": "Ranou", "category": "nourriture", "difficulty": 1},
        {"french": "Nourriture", "shimaore": "Chaoula", "kibouchi": "Hanigni", "category": "nourriture", "difficulty": 1},
        {"french": "Ananas", "shimaore": "Nanassi", "kibouchi": "Mananassi", "category": "nourriture", "difficulty": 1},
        {"french": "Pois d'angole", "shimaore": "Tsouzi", "kibouchi": "Ambatri", "category": "nourriture", "difficulty": 1},
        {"french": "Banane", "shimaore": "Trovi", "kibouchi": "Hountsi", "category": "nourriture", "difficulty": 1},
        {"french": "Pain", "shimaore": "Dipé", "kibouchi": "Dipé", "category": "nourriture", "difficulty": 1},
        {"french": "Gâteau", "shimaore": "Mharé", "kibouchi": "Moukari", "category": "nourriture", "difficulty": 1},
        {"french": "Mangue", "shimaore": "Manga", "kibouchi": "Manga", "category": "nourriture", "difficulty": 1},
        {"french": "Noix de coco", "shimaore": "Nazi", "kibouchi": "Voiniou", "category": "nourriture", "difficulty": 1},
        {"french": "Noix de coco fraîche", "shimaore": "Chijavou", "kibouchi": "Kidjavou", "category": "nourriture", "difficulty": 1},
        {"french": "Lait", "shimaore": "Dzia", "kibouchi": "Rounounou", "category": "nourriture", "difficulty": 1},
        {"french": "Viande", "shimaore": "Nhyama", "kibouchi": "Amboumati", "category": "nourriture", "difficulty": 1},
        {"french": "Poisson", "shimaore": "Fi", "kibouchi": "Lokou", "category": "nourriture", "difficulty": 1},
        {"french": "Brèdes", "shimaore": "Féliki", "kibouchi": "Féliki", "category": "nourriture", "difficulty": 1},
        {"french": "Brède mafane", "shimaore": "Féliki mafana", "kibouchi": "Féliki mafana", "category": "nourriture", "difficulty": 1},
        {"french": "Brède manioc", "shimaore": "Mataba", "kibouchi": "Féliki mouhogou", "category": "nourriture", "difficulty": 1},
        {"french": "Brède morelle", "shimaore": "Féliki nyongo", "kibouchi": "Féliki angnatsindra", "category": "nourriture", "difficulty": 1},
        {"french": "Brès patate douce", "shimaore": "Féliki batata", "kibouchi": "Féliki batata", "category": "nourriture", "difficulty": 1},
        {"french": "Patate douce", "shimaore": "Batata", "kibouchi": "Batata", "category": "nourriture", "difficulty": 1},
        {"french": "Bouillon", "shimaore": "Woubou", "kibouchi": "Kouba", "category": "nourriture", "difficulty": 1},
        {"french": "Banane au coco", "shimaore": "Trovi ya nadzi", "kibouchi": "Hountsi an voiniou", "category": "nourriture", "difficulty": 1},
        {"french": "Riz au coco", "shimaore": "Tsoholé ya nadzi", "kibouchi": "Vari an voiniou", "category": "nourriture", "difficulty": 1},
        {"french": "Poulet", "shimaore": "Bawa", "kibouchi": "Mabawa", "category": "nourriture", "difficulty": 1},
        {"french": "Œuf", "shimaore": "Joiyi", "kibouchi": "Antoudi", "category": "nourriture", "difficulty": 1},
        {"french": "Tomate", "shimaore": "Tamati", "kibouchi": "Matimati", "category": "nourriture", "difficulty": 1},
        {"french": "Oignon", "shimaore": "Chouroungou", "kibouchi": "Doungoulou", "category": "nourriture", "difficulty": 1},
        {"french": "Ail", "shimaore": "Chouroungou foudjé", "kibouchi": "Doungoulou mvoudjou", "category": "nourriture", "difficulty": 1},
        {"french": "Orange", "shimaore": "Troundra", "kibouchi": "Tsoha", "category": "nourriture", "difficulty": 1},
        {"french": "Mandarine", "shimaore": "Madhandze", "kibouchi": "Tsoha madzandzi", "category": "nourriture", "difficulty": 1},
        {"french": "Manioc", "shimaore": "Mhogo", "kibouchi": "Mouhogou", "category": "nourriture", "difficulty": 1},
        {"french": "Piment", "shimaore": "Poutou", "kibouchi": "Pilipili", "category": "nourriture", "difficulty": 1},
        {"french": "Taro", "shimaore": "Majimbi", "kibouchi": "Majimbi", "category": "nourriture", "difficulty": 1},
        {"french": "Sel", "shimaore": "Chingo", "kibouchi": "Sira", "category": "nourriture", "difficulty": 1},
        {"french": "Poivre", "shimaore": "Bvilibvili manga", "kibouchi": "Vilivili", "category": "nourriture", "difficulty": 1},
        {"french": "Curcuma", "shimaore": "Dzindzano", "kibouchi": "Tamoutamou", "category": "nourriture", "difficulty": 1},
        {"french": "Cumin", "shimaore": "Massala", "kibouchi": "Massala", "category": "nourriture", "difficulty": 1},
        {"french": "Ciboulette", "shimaore": "Chouroungou", "kibouchi": "Doungoulou ravigni", "category": "nourriture", "difficulty": 1},
        {"french": "Gingembre", "shimaore": "Sakayi", "kibouchi": "Sakéyi", "category": "nourriture", "difficulty": 1},
        {"french": "Vanille", "shimaore": "Lavani", "kibouchi": "Lavani", "category": "nourriture", "difficulty": 1},
        {"french": "Tamarin", "shimaore": "Ouhajou", "kibouchi": "Madirou kakazou", "category": "nourriture", "difficulty": 1},
        
        # Maison (section complète selon le tableau habitation)
        {"french": "Maison", "shimaore": "Nyoumba", "kibouchi": "Tragnou", "category": "maison", "difficulty": 1},
        {"french": "Porte", "shimaore": "Mlango", "kibouchi": "Varavaragena", "category": "maison", "difficulty": 1},
        {"french": "Case", "shimaore": "Banga", "kibouchi": "Banga", "category": "maison", "difficulty": 1},
        {"french": "Lit", "shimaore": "Chtrandra", "kibouchi": "Koubani", "category": "maison", "difficulty": 1},
        {"french": "Marmite", "shimaore": "Gnoungou", "kibouchi": "Vilangni", "category": "maison", "difficulty": 1},
        {"french": "Vaisselle", "shimaore": "Ziya", "kibouchi": "Hintagna", "category": "maison", "difficulty": 1},
        {"french": "Bol", "shimaore": "Bacouli", "kibouchi": "Bacouli", "category": "maison", "difficulty": 1},
        {"french": "Cuillère", "shimaore": "Soutrou", "kibouchi": "Sotrou", "category": "maison", "difficulty": 1},
        {"french": "Fenêtre", "shimaore": "Fénétri", "kibouchi": "Lafoumétara", "category": "maison", "difficulty": 1},
        {"french": "Chaise", "shimaore": "Chiri", "kibouchi": "Chiri", "category": "maison", "difficulty": 1},
        {"french": "Table", "shimaore": "Latabou", "kibouchi": "Latabou", "category": "maison", "difficulty": 1},
        {"french": "Miroir", "shimaore": "Chido", "kibouchi": "Kitarafa", "category": "maison", "difficulty": 1},
        {"french": "Cour", "shimaore": "Lacourou", "kibouchi": "Lacourou", "category": "maison", "difficulty": 1},
        {"french": "Clôture", "shimaore": "Mraba", "kibouchi": "Mraba", "category": "maison", "difficulty": 1},
        {"french": "Toilette", "shimaore": "Mraba", "kibouchi": "Mraba", "category": "maison", "difficulty": 1},
        {"french": "Sot", "shimaore": "Siyo", "kibouchi": "Siyo", "category": "maison", "difficulty": 1},
        {"french": "Louche", "shimaore": "Paou", "kibouchi": "Pow", "category": "maison", "difficulty": 1},
        {"french": "Couteau", "shimaore": "Sembéya", "kibouchi": "Méssou", "category": "maison", "difficulty": 1},
        {"french": "Matelas", "shimaore": "Godoro", "kibouchi": "Goudorou", "category": "maison", "difficulty": 1},
        {"french": "Oreiller", "shimaore": "Mtsao", "kibouchi": "Hondagna", "category": "maison", "difficulty": 1},
        {"french": "Buffet", "shimaore": "Biffé", "kibouchi": "Biffé", "category": "maison", "difficulty": 1},
        {"french": "Mur", "shimaore": "Houra", "kibouchi": "Riba", "category": "maison", "difficulty": 1},
        {"french": "Véranda", "shimaore": "Baraza", "kibouchi": "Baraza", "category": "maison", "difficulty": 1},
        {"french": "Toiture", "shimaore": "Outro", "kibouchi": "Vovougnou", "category": "maison", "difficulty": 1},
        {"french": "Ampoule", "shimaore": "Lalampou", "kibouchi": "Lalampou", "category": "maison", "difficulty": 1},
        {"french": "Lumière", "shimaore": "Mwengué", "kibouchi": "Mwengué", "category": "maison", "difficulty": 1},
        {"french": "Torche", "shimaore": "Gandilé", "kibouchi": "Gandili", "category": "maison", "difficulty": 1},
        {"french": "Hache", "shimaore": "Soha", "kibouchi": "Famaki", "category": "maison", "difficulty": 1},
        {"french": "Machette", "shimaore": "M'panga", "kibouchi": "Ampanga", "category": "maison", "difficulty": 1},
        {"french": "Coupe coupe", "shimaore": "Chombo", "kibouchi": "Chombou", "category": "maison", "difficulty": 1},
        {"french": "Cartable/Malette", "shimaore": "Mkoba", "kibouchi": "Mkoba", "category": "maison", "difficulty": 1},
        {"french": "Sac", "shimaore": "Gouni", "kibouchi": "Gouni", "category": "maison", "difficulty": 1},
        {"french": "Balai", "shimaore": "Péou", "kibouchi": "Famafa", "category": "maison", "difficulty": 1},
        {"french": "Mortier", "shimaore": "Chino", "kibouchi": "Légnou", "category": "maison", "difficulty": 1},
        {"french": "Assiette", "shimaore": "Sahani", "kibouchi": "Sahani", "category": "maison", "difficulty": 1},
        
        # Vêtements (section complète selon le nouveau tableau)
        {"french": "Vêtement", "shimaore": "Ngouwô", "kibouchi": "Ankandzou", "category": "vetements", "difficulty": 1},
        {"french": "Salouva", "shimaore": "Salouva", "kibouchi": "Slouvagna", "category": "vetements", "difficulty": 1},
        {"french": "Chemise", "shimaore": "Chimizi", "kibouchi": "Chimizi", "category": "vetements", "difficulty": 1},
        {"french": "Pantalon", "shimaore": "Sourouali", "kibouchi": "Sourouali", "category": "vetements", "difficulty": 1},
        {"french": "Short", "shimaore": "Kaliso", "kibouchi": "Kaliso", "category": "vetements", "difficulty": 1},
        {"french": "Sous vêtement", "shimaore": "Silipou", "kibouchi": "Silipou", "category": "vetements", "difficulty": 1},
        {"french": "Chapeau", "shimaore": "Kofia", "kibouchi": "Koufia", "category": "vetements", "difficulty": 1},
        {"french": "Kamiss/Boubou", "shimaore": "Candzou bolé", "kibouchi": "Ancandzou bé", "category": "vetements", "difficulty": 1},
        {"french": "Haut de salouva", "shimaore": "Body", "kibouchi": "Body", "category": "vetements", "difficulty": 1},
        {"french": "T shirt", "shimaore": "Kandzou", "kibouchi": "Kandzou", "category": "vetements", "difficulty": 1},
        {"french": "Chaussures", "shimaore": "Kabwa", "kibouchi": "Kabwa", "category": "vetements", "difficulty": 1},
        {"french": "Baskets/Sneakers", "shimaore": "Magochi", "kibouchi": "Magochi", "category": "vetements", "difficulty": 1},
        {"french": "Tongs", "shimaore": "Sapatri", "kibouchi": "Kabwa sapatri", "category": "vetements", "difficulty": 1},
        {"french": "Jupe", "shimaore": "Jipo", "kibouchi": "Jipou", "category": "vetements", "difficulty": 1},
        {"french": "Robe", "shimaore": "Robo", "kibouchi": "Robou", "category": "vetements", "difficulty": 1},
        {"french": "Voile", "shimaore": "Kichali", "kibouchi": "Kichali", "category": "vetements", "difficulty": 1},
        
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
        
        # Nature (mise à jour complète selon le nouveau tableau)
        {"french": "Pente/Colline/Mont", "shimaore": "Mlima", "kibouchi": "Boungou", "category": "nature", "difficulty": 1},
        {"french": "Lune", "shimaore": "Mwézi", "kibouchi": "Fandzava", "category": "nature", "difficulty": 1},
        {"french": "Étoile", "shimaore": "Gnora", "kibouchi": "Lakintagna", "category": "nature", "difficulty": 1},
        {"french": "Sable", "shimaore": "Mtsanga", "kibouchi": "Fasigni", "category": "nature", "difficulty": 1},
        {"french": "Vague", "shimaore": "Dhouja", "kibouchi": "Houndza/Riaka", "category": "nature", "difficulty": 1},
        {"french": "Vent", "shimaore": "Pévo", "kibouchi": "Tsikou", "category": "nature", "difficulty": 1},
        {"french": "Pluie", "shimaore": "Vhoua", "kibouchi": "Mahaléni", "category": "nature", "difficulty": 1},
        {"french": "Mangrove", "shimaore": "Mhonko", "kibouchi": "Honkou", "category": "nature", "difficulty": 1},
        {"french": "Corail", "shimaore": "Soiyi", "kibouchi": "Soiyi", "category": "nature", "difficulty": 1},
        {"french": "Barrière de corail", "shimaore": "Caléni", "kibouchi": "Caléni", "category": "nature", "difficulty": 1},
        {"french": "Tempête", "shimaore": "Darouba", "kibouchi": "Tsikou", "category": "nature", "difficulty": 1},
        {"french": "Rivière", "shimaore": "Mouro", "kibouchi": "Mouroni", "category": "nature", "difficulty": 1},
        {"french": "Pont", "shimaore": "Daradja", "kibouchi": "Daradja", "category": "nature", "difficulty": 1},
        {"french": "Nuage", "shimaore": "Wingou", "kibouchi": "Vingou", "category": "nature", "difficulty": 1},
        {"french": "Campagne/Forêt", "shimaore": "Malayouni", "kibouchi": "Atihala", "category": "nature", "difficulty": 1},
        {"french": "Caillou/Pierre/Rocher", "shimaore": "Bwé", "kibouchi": "Vatou", "category": "nature", "difficulty": 1},
        {"french": "Plateau", "shimaore": "Bandra", "kibouchi": "Kétraka", "category": "nature", "difficulty": 1},
        {"french": "Route", "shimaore": "Parré", "kibouchi": "Parré", "category": "nature", "difficulty": 1},
        {"french": "Chemin/Sentier/Parcours", "shimaore": "Ndzia", "kibouchi": "Lalagna", "category": "nature", "difficulty": 1},
        {"french": "Herbe", "shimaore": "Malavou", "kibouchi": "Hayitri", "category": "nature", "difficulty": 1},
        {"french": "Fleur", "shimaore": "Foulera", "kibouchi": "Foulera", "category": "nature", "difficulty": 1},
        {"french": "Soleil", "shimaore": "Mwézi", "kibouchi": "Zouva", "category": "nature", "difficulty": 1},
        {"french": "Mer", "shimaore": "Bahari", "kibouchi": "Bahari", "category": "nature", "difficulty": 1},
        {"french": "Plage", "shimaore": "Mtsangani", "kibouchi": "Fassigni", "category": "nature", "difficulty": 1},
        {"french": "Arbre", "shimaore": "Mwiri", "kibouchi": "Kakazou", "category": "nature", "difficulty": 1},
        {"french": "Rue/Route", "shimaore": "Paré", "kibouchi": "Paré", "category": "nature", "difficulty": 1},
        {"french": "Bananier", "shimaore": "Trindri", "kibouchi": "Voudini hountsi", "category": "nature", "difficulty": 1},
        {"french": "Feuille", "shimaore": "Mawoini", "kibouchi": "Hayitri", "category": "nature", "difficulty": 1},
        {"french": "Branche", "shimaore": "", "kibouchi": "Trahi", "category": "nature", "difficulty": 1},
        {"french": "Tornade", "shimaore": "Ouzimouyi", "kibouchi": "", "category": "nature", "difficulty": 1},
        
        # Nouveaux éléments nature du tableau supplémentaire
        {"french": "Cocotier", "shimaore": "M'hadzi", "kibouchi": "Voudi ni vwaniou", "category": "nature", "difficulty": 1},
        {"french": "Arbre à pain", "shimaore": "M'frampé", "kibouchi": "Voudi ni frampé", "category": "nature", "difficulty": 1},
        {"french": "Baobab", "shimaore": "M'bouyou", "kibouchi": "Voudi ni bouyou", "category": "nature", "difficulty": 1},
        {"french": "Bambou", "shimaore": "M'banbo", "kibouchi": "Valiha", "category": "nature", "difficulty": 1},
        {"french": "Manguier", "shimaore": "M'manga", "kibouchi": "Voudi ni manga", "category": "nature", "difficulty": 1},
        {"french": "Jacquier", "shimaore": "M'fénéssi", "kibouchi": "Voudi ni finéssi", "category": "nature", "difficulty": 1},
        {"french": "Terre", "shimaore": "Trotro", "kibouchi": "Fotaka", "category": "nature", "difficulty": 1},
        {"french": "Sol", "shimaore": "Tsi", "kibouchi": "Tani", "category": "nature", "difficulty": 1},
        {"french": "Érosion", "shimaore": "Padza", "kibouchi": "Padza", "category": "nature", "difficulty": 1},
        {"french": "Marée basse", "shimaore": "Maji yavo", "kibouchi": "Ranou méki", "category": "nature", "difficulty": 1},
        {"french": "Marée haute", "shimaore": "Maji yamalé", "kibouchi": "Ranou fénou", "category": "nature", "difficulty": 1},
        {"french": "Inondé", "shimaore": "Ourora", "kibouchi": "Dobou", "category": "nature", "difficulty": 1},
        {"french": "Sauvage", "shimaore": "Nyéha", "kibouchi": "Di", "category": "nature", "difficulty": 1},
        {"french": "Canne à sucre", "shimaore": "Moua", "kibouchi": "Fari", "category": "nature", "difficulty": 1},
        {"french": "Fagot", "shimaore": "Kouni", "kibouchi": "Azoumati", "category": "nature", "difficulty": 1},
        {"french": "Pirogue", "shimaore": "Laka", "kibouchi": "Lakana", "category": "nature", "difficulty": 1},
        {"french": "Vedette", "shimaore": "Kwassa kwassa", "kibouchi": "Vidéti", "category": "nature", "difficulty": 1},
        {"french": "École", "shimaore": "Licoli", "kibouchi": "Licoli", "category": "nature", "difficulty": 1},
        {"french": "École coranique", "shimaore": "Shioni", "kibouchi": "Kioni", "category": "nature", "difficulty": 1},
        
        # Adjectifs (nouvelle section complète selon le tableau)
        {"french": "Grand", "shimaore": "Bolé", "kibouchi": "Bé", "category": "adjectifs", "difficulty": 1},
        {"french": "Petit", "shimaore": "Titi", "kibouchi": "Héli", "category": "adjectifs", "difficulty": 1},
        {"french": "Gros", "shimaore": "Mtronga/Tronga", "kibouchi": "Bé", "category": "adjectifs", "difficulty": 1},
        {"french": "Maigre", "shimaore": "Tsala", "kibouchi": "Mahia", "category": "adjectifs", "difficulty": 1},
        {"french": "Fort", "shimaore": "Ouna ngouvou", "kibouchi": "Missi ngouvou", "category": "adjectifs", "difficulty": 1},
        {"french": "Dur", "shimaore": "Mangavou", "kibouchi": "Mahéri", "category": "adjectifs", "difficulty": 1},
        {"french": "Mou", "shimaore": "Tremboivou", "kibouchi": "Malémi", "category": "adjectifs", "difficulty": 1},
        {"french": "Beau/Jolie", "shimaore": "Mzouri", "kibouchi": "Zatovou", "category": "adjectifs", "difficulty": 1},
        {"french": "Laid", "shimaore": "Tsi ndzouzouri", "kibouchi": "Ratsi sora", "category": "adjectifs", "difficulty": 1},
        {"french": "Jeune", "shimaore": "Nrétsa", "kibouchi": "Zaza", "category": "adjectifs", "difficulty": 1},
        {"french": "Vieux", "shimaore": "Dhouha", "kibouchi": "Héla", "category": "adjectifs", "difficulty": 1},
        {"french": "Gentil", "shimaore": "Mwéma", "kibouchi": "Tsara rohou", "category": "adjectifs", "difficulty": 1},
        {"french": "Méchant", "shimaore": "Mbovou", "kibouchi": "Ratsi rohou", "category": "adjectifs", "difficulty": 1},
        {"french": "Intelligent", "shimaore": "", "kibouchi": "Trara louha", "category": "adjectifs", "difficulty": 1},
        {"french": "Bête", "shimaore": "Dhaba", "kibouchi": "Dhaba", "category": "adjectifs", "difficulty": 1},
        {"french": "Riche", "shimaore": "Tadjiri", "kibouchi": "Tadjiri", "category": "adjectifs", "difficulty": 1},
        {"french": "Pauvre", "shimaore": "Maskini", "kibouchi": "Maskini", "category": "adjectifs", "difficulty": 1},
        {"french": "Sérieux", "shimaore": "Kassidi", "kibouchi": "Koussoudi", "category": "adjectifs", "difficulty": 1},
        {"french": "Drôle", "shimaore": "Outsésa", "kibouchi": "Mampimohi", "category": "adjectifs", "difficulty": 1},
        {"french": "Calme", "shimaore": "Baridi", "kibouchi": "Malémi", "category": "adjectifs", "difficulty": 1},
        {"french": "Nerveux", "shimaore": "Hadjarou", "kibouchi": "Tsipi téhitri", "category": "adjectifs", "difficulty": 1},
        {"french": "Bon", "shimaore": "Mwéma", "kibouchi": "Tsara", "category": "adjectifs", "difficulty": 1},
        {"french": "Mauvais", "shimaore": "Mbovou", "kibouchi": "Mwadéli", "category": "adjectifs", "difficulty": 1},
        {"french": "Chaud", "shimaore": "Moro", "kibouchi": "Méyi", "category": "adjectifs", "difficulty": 1},
        {"french": "Froid", "shimaore": "Baridi", "kibouchi": "Manintsi", "category": "adjectifs", "difficulty": 1},
        {"french": "Lourd", "shimaore": "Ndziro", "kibouchi": "Mavéchatra", "category": "adjectifs", "difficulty": 1},
        {"french": "Léger", "shimaore": "Ndzangou", "kibouchi": "Miyivagna", "category": "adjectifs", "difficulty": 1},
        {"french": "Propre", "shimaore": "Irahara", "kibouchi": "Madiou", "category": "adjectifs", "difficulty": 1},
        {"french": "Sale", "shimaore": "Trotro", "kibouchi": "Maloutou", "category": "adjectifs", "difficulty": 1},
        {"french": "Nouveau", "shimaore": "Piya", "kibouchi": "Vowou", "category": "adjectifs", "difficulty": 1},
        {"french": "Ancien", "shimaore": "Hale", "kibouchi": "Keyi", "category": "adjectifs", "difficulty": 1},
        {"french": "Facile", "shimaore": "Ndzangou", "kibouchi": "Mora", "category": "adjectifs", "difficulty": 1},
        {"french": "Difficile", "shimaore": "Ndziro", "kibouchi": "Mahéri", "category": "adjectifs", "difficulty": 1},
        {"french": "Important", "shimaore": "Mouhimou", "kibouchi": "Mouhimou", "category": "adjectifs", "difficulty": 1},
        {"french": "Inutile", "shimaore": "Kassina mana", "kibouchi": "Tsissi fotouni", "category": "adjectifs", "difficulty": 1},
        {"french": "Faux", "shimaore": "Trambo", "kibouchi": "Vandi", "category": "adjectifs", "difficulty": 1},
        {"french": "Vrai", "shimaore": "Kwéli", "kibouchi": "Ankitigni", "category": "adjectifs", "difficulty": 1},
        {"french": "Ouvert", "shimaore": "Ouboua", "kibouchi": "Mibiyangna", "category": "adjectifs", "difficulty": 1},
        {"french": "Fermé", "shimaore": "Oubala", "kibouchi": "Migadra", "category": "adjectifs", "difficulty": 1},
        {"french": "Content", "shimaore": "Oujiviwa", "kibouchi": "Ravou", "category": "adjectifs", "difficulty": 1},
        {"french": "Triste", "shimaore": "Ouna hamo", "kibouchi": "Malahélou", "category": "adjectifs", "difficulty": 1},
        {"french": "Fatigué", "shimaore": "Ouléméwa", "kibouchi": "Vaha", "category": "adjectifs", "difficulty": 1},
        {"french": "En colère", "shimaore": "Hadabou", "kibouchi": "Méloukou", "category": "adjectifs", "difficulty": 1},
        {"french": "Fâché", "shimaore": "Ouja hassira", "kibouchi": "Méloukou", "category": "adjectifs", "difficulty": 1},
        {"french": "Amoureux", "shimaore": "Ouvendza", "kibouchi": "Mitiya", "category": "adjectifs", "difficulty": 1},
        {"french": "Inquiet", "shimaore": "Ouna hamo", "kibouchi": "Miyefitri", "category": "adjectifs", "difficulty": 1},
        {"french": "Fier", "shimaore": "Oujiviwa", "kibouchi": "Ravou", "category": "adjectifs", "difficulty": 1},
        {"french": "Honteux", "shimaore": "Ouona haya", "kibouchi": "Mampihingnatra", "category": "adjectifs", "difficulty": 1},
        {"french": "Surpris", "shimaore": "Oumarouha", "kibouchi": "Téhitri", "category": "adjectifs", "difficulty": 1},
        {"french": "Satisfait", "shimaore": "Oufourahi", "kibouchi": "Ravou", "category": "adjectifs", "difficulty": 1},
        {"french": "Long", "shimaore": "Drilé", "kibouchi": "Hapou", "category": "adjectifs", "difficulty": 1},
        {"french": "Court", "shimaore": "Coutri", "kibouchi": "Fohiki", "category": "adjectifs", "difficulty": 1},
        
        # Transport (section complète selon le nouveau tableau)
        {"french": "Taxis", "shimaore": "Taxi", "kibouchi": "Taxi", "category": "transport", "difficulty": 1},
        {"french": "Motos", "shimaore": "Monto", "kibouchi": "Monto", "category": "transport", "difficulty": 1},
        {"french": "Vélos", "shimaore": "Bicyclèti", "kibouchi": "Bicyclèti", "category": "transport", "difficulty": 1},
        {"french": "Barge", "shimaore": "Markabou", "kibouchi": "Markabou", "category": "transport", "difficulty": 1},
        {"french": "Vedettes", "shimaore": "Kwassa kwassa", "kibouchi": "Vidéti", "category": "transport", "difficulty": 1},
        {"french": "Pirogue", "shimaore": "Laka", "kibouchi": "Lakana", "category": "transport", "difficulty": 1},
        {"french": "Avion", "shimaore": "Ndrègué", "kibouchi": "Roplani", "category": "transport", "difficulty": 1},
        
        # Expressions (petites formules pratiques pour touristes et conversation)
        {"french": "Excuse-moi/pardon", "shimaore": "Soimahani", "kibouchi": "Soimahani", "category": "expressions", "difficulty": 1},
        {"french": "J'ai faim", "shimaore": "Nissi ona ndza", "kibouchi": "Zahou moussari", "category": "expressions", "difficulty": 1},
        {"french": "J'ai soif", "shimaore": "Nissi ona niyora", "kibouchi": "Zahou tindranou", "category": "expressions", "difficulty": 1},
        {"french": "Je voudrais aller à", "shimaore": "Nissi tsaha nendré", "kibouchi": "Zahou chokou andéha", "category": "expressions", "difficulty": 1},
        {"french": "J'arrive de", "shimaore": "Tsi lawa", "kibouchi": "Zahou boka", "category": "expressions", "difficulty": 1},
        {"french": "Je peux avoir des toilettes", "shimaore": "Tnissi miya mraba", "kibouchi": "Zahou mangataka mraba", "category": "expressions", "difficulty": 1},
        {"french": "Je veux manger", "shimaore": "Nissi miya chaoula", "kibouchi": "Zahou mila ihinagna", "category": "expressions", "difficulty": 1},
        {"french": "Où se trouve", "shimaore": "Ouparhanoua havi", "kibouchi": "Aya moi", "category": "expressions", "difficulty": 1},
        {"french": "Où sommes nous", "shimaore": "Ra havi", "kibouchi": "Atsika yétou aya", "category": "expressions", "difficulty": 1},
        {"french": "Je suis perdu", "shimaore": "Tsi latsiha", "kibouchi": "Zahou véri", "category": "expressions", "difficulty": 1},
        {"french": "Bienvenu", "shimaore": "Karibou", "kibouchi": "Karibou", "category": "expressions", "difficulty": 1},
        {"french": "Je t'aime", "shimaore": "Nisouhou vendza", "kibouchi": "Zahou mitia anaou", "category": "expressions", "difficulty": 1},
        {"french": "J'ai mal", "shimaore": "Nissi kodza", "kibouchi": "Zahou marari", "category": "expressions", "difficulty": 1},
        {"french": "Pouvez-vous m'aider ?", "shimaore": "Ni sayidié vanou", "kibouchi": "Zahou mangataka moussada", "category": "expressions", "difficulty": 1},
        {"french": "J'ai compris", "shimaore": "Tsi helewa", "kibouchi": "Zahou kouéléwa", "category": "expressions", "difficulty": 1},
        {"french": "Je ne peux pas", "shimaore": "Tsi chindri", "kibouchi": "Zahou tsi mahaléou", "category": "expressions", "difficulty": 1},
        {"french": "Montre moi", "shimaore": "Néssédzyéyé", "kibouchi": "Ampizaha zahou", "category": "expressions", "difficulty": 1},
        {"french": "S'il vous plaît", "shimaore": "Tafadali", "kibouchi": "Tafadali", "category": "expressions", "difficulty": 1},
        {"french": "Combien ça coûte ?", "shimaore": "Kissajé", "kibouchi": "Hotri inou moi", "category": "expressions", "difficulty": 1},
        {"french": "À gauche", "shimaore": "Potroni", "kibouchi": "Kipotrou", "category": "expressions", "difficulty": 1},
        {"french": "À droite", "shimaore": "Houméni", "kibouchi": "Finana", "category": "expressions", "difficulty": 1},
        {"french": "Tout droit", "shimaore": "Hondzoha", "kibouchi": "Mahitsi", "category": "expressions", "difficulty": 1},
        {"french": "C'est loin ?", "shimaore": "Ya mbali", "kibouchi": "Lavitri", "category": "expressions", "difficulty": 1},
        {"french": "C'est très bon !", "shimaore": "Issi jiva", "kibouchi": "Matavi soifi", "category": "expressions", "difficulty": 1},
        {"french": "Trop cher", "shimaore": "Hali", "kibouchi": "Saroutrou", "category": "expressions", "difficulty": 1},
        {"french": "Moins cher s'il vous plaît", "shimaore": "Nissi miya ouchoukidzé", "kibouchi": "Za mangataka koupoungouza kima", "category": "expressions", "difficulty": 2},
        {"french": "Je prends ça", "shimaore": "Nissi renga ini", "kibouchi": "Zahou bou angala thi", "category": "expressions", "difficulty": 1},
        {"french": "Combien la nuit ?", "shimaore": "Kissagé oukou moja", "kibouchi": "Hotri inou haligni areki", "category": "expressions", "difficulty": 1},
        {"french": "Avec climatisation ?", "shimaore": "Ina climatisation", "kibouchi": "Missi climatisation", "category": "expressions", "difficulty": 1},
        {"french": "Avec petit déjeuner ?", "shimaore": "Ina kéya", "kibouchi": "Missi ankera", "category": "expressions", "difficulty": 1},
        {"french": "Appelez la police !", "shimaore": "Hira sirikali", "kibouchi": "Kahiya sirikali", "category": "expressions", "difficulty": 1},
        {"french": "Appelez une ambulance !", "shimaore": "Hira ambulanci", "kibouchi": "Kahiya ambulanci", "category": "expressions", "difficulty": 1},
        {"french": "J'ai besoin d'un médecin", "shimaore": "Ntsha douktera", "kibouchi": "Zahou mila douktera", "category": "expressions", "difficulty": 1},
        {"french": "Je ne me sens pas bien", "shimaore": "Tsissi fétré", "kibouchi": "Za maharengni nafoussoukou moidéli", "category": "expressions", "difficulty": 2},
        {"french": "Au milieu", "shimaore": "Hari", "kibouchi": "Angnivou", "category": "expressions", "difficulty": 1},
        
        # Nouvelles expressions sociales et culturelles
        {"french": "Respect", "shimaore": "Mastaha", "kibouchi": "Mastaha", "category": "expressions", "difficulty": 1},
        {"french": "Quelqu'un de fiable", "shimaore": "Mwaminifou", "kibouchi": "Mwaminifou", "category": "expressions", "difficulty": 1},
        {"french": "Secret", "shimaore": "Siri", "kibouchi": "Siri", "category": "expressions", "difficulty": 1},
        {"french": "Joie", "shimaore": "Fouraha", "kibouchi": "Aravouangna", "category": "expressions", "difficulty": 1},
        {"french": "Avoir la haine", "shimaore": "Outoukiwa", "kibouchi": "Marari rohou", "category": "expressions", "difficulty": 1},
        {"french": "Convivialité", "shimaore": "Ouvoimoja", "kibouchi": "Ouvoimoja", "category": "expressions", "difficulty": 1},
        {"french": "Entre aide", "shimaore": "Oussayidiyana", "kibouchi": "Moussada", "category": "expressions", "difficulty": 1},
        {"french": "Faire crédit", "shimaore": "Oukopa", "kibouchi": "Midéni", "category": "expressions", "difficulty": 1},
        {"french": "Nounou", "shimaore": "Mlézi", "kibouchi": "Mlézi", "category": "expressions", "difficulty": 1},
        
        # Reptiles et autres animaux
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