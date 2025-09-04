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
    # Contenu de base en shimaoré et kibouchi
    base_words = [
        {
            "french": "Maman", "shimaore": "Mama", "kibouchi": "Mama", 
            "category": "famille", "difficulty": 1
        },
        {
            "french": "Papa", "shimaore": "Baba", "kibouchi": "Baba", 
            "category": "famille", "difficulty": 1
        },
        {
            "french": "Enfant", "shimaore": "Mwana", "kibouchi": "Mwana", 
            "category": "famille", "difficulty": 1
        },
        {
            "french": "Bonjour", "shimaore": "Bari", "kibouchi": "Bariza", 
            "category": "salutations", "difficulty": 1
        },
        {
            "french": "Merci", "shimaore": "Marahaba", "kibouchi": "Marahaba", 
            "category": "salutations", "difficulty": 1
        },
        {
            "french": "Rouge", "shimaore": "Mera", "kibouchi": "Mera", 
            "category": "couleurs", "difficulty": 1
        },
        {
            "french": "Jaune", "shimaore": "Manjano", "kibouchi": "Manjano", 
            "category": "couleurs", "difficulty": 1
        },
        {
            "french": "Maki", "shimaore": "Maki", "kibouchi": "Maki", 
            "category": "animaux", "difficulty": 1
        },
        {
            "french": "Un", "shimaore": "Moja", "kibouchi": "Raike", 
            "category": "nombres", "difficulty": 1
        },
        {
            "french": "Deux", "shimaore": "Mbili", "kibouchi": "Rou", 
            "category": "nombres", "difficulty": 1
        }
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