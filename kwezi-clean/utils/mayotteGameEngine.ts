import AsyncStorage from '@react-native-async-storage/async-storage';
import mayotteWorldData from '../assets/data/mayotte-world.json';

export interface Village {
  id: string;
  name: string;
  pos: { x: number; y: number };
  type: string;
  unlocked: boolean;
  assets: {
    bg?: string;
    audio?: string;
  };
  meta: {
    population?: number;
    specialite: string;
    description: string;
    histoire?: string;
    langue_locale?: string;
    quiz?: {
      question: string;
      options: string[];
      correct: number;
    };
  };
}

export interface Path {
  from: string;
  to: string;
  path: Array<{ x: number; y: number }>;
  distance: number;
  transport: string;
  unlock_requirement: {
    type: string;
    village?: string;
    count?: number;
  };
}

export interface PlayerProgress {
  currentVillage: string;
  visitedVillages: string[];
  unlockedVillages: string[];
  completedQuiz: string[];
  score: number;
  badges: string[];
  lastPlayTime: string;
}

export interface GameState {
  villages: Village[];
  paths: Path[];
  progress: PlayerProgress;
  isLoaded: boolean;
}

class MayotteGameEngine {
  private static instance: MayotteGameEngine;
  private gameState: GameState;
  private listeners: Array<(state: GameState) => void> = [];

  private constructor() {
    this.gameState = {
      villages: [],
      paths: [],
      progress: {
        currentVillage: 'mamoudzou',
        visitedVillages: ['mamoudzou'],
        unlockedVillages: ['mamoudzou'],
        completedQuiz: [],
        score: 0,
        badges: [],
        lastPlayTime: new Date().toISOString(),
      },
      isLoaded: false,
    };
  }

  public static getInstance(): MayotteGameEngine {
    if (!MayotteGameEngine.instance) {
      MayotteGameEngine.instance = new MayotteGameEngine();
    }
    return MayotteGameEngine.instance;
  }

  // Initialiser le jeu
  public async initializeGame(): Promise<void> {
    try {
      // Charger les données du monde
      const worldData = mayotteWorldData as any;
      
      // Charger la progression sauvegardée
      const savedProgress = await this.loadProgress();
      
      // Créer l'état du jeu
      this.gameState = {
        villages: worldData.villages.map((village: any) => ({
          ...village,
          unlocked: savedProgress.unlockedVillages.includes(village.id),
        })),
        paths: worldData.paths,
        progress: savedProgress,
        isLoaded: true,
      };
      
      // Vérifier et débloquer de nouveaux villages
      this.checkUnlockConditions();
      
      this.notifyListeners();
    } catch (error) {
      console.error('Erreur lors de l\'initialisation du jeu:', error);
    }
  }

  // Écouter les changements d'état
  public subscribe(listener: (state: GameState) => void): () => void {
    this.listeners.push(listener);
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  private notifyListeners(): void {
    this.listeners.forEach(listener => listener(this.gameState));
  }

  // Obtenir l'état actuel
  public getGameState(): GameState {
    return this.gameState;
  }

  // Voyager vers un village
  public async travelToVillage(villageId: string): Promise<boolean> {
    const village = this.gameState.villages.find(v => v.id === villageId);
    if (!village || !village.unlocked) {
      return false;
    }

    // Vérifier s'il y a un chemin depuis le village actuel
    const hasPath = this.hasPathBetween(this.gameState.progress.currentVillage, villageId);
    if (!hasPath) {
      return false;
    }

    // Mettre à jour la progression
    this.gameState.progress.currentVillage = villageId;
    
    if (!this.gameState.progress.visitedVillages.includes(villageId)) {
      this.gameState.progress.visitedVillages.push(villageId);
      this.gameState.progress.score += 10; // Points pour nouvelle visite
    }
    
    this.gameState.progress.lastPlayTime = new Date().toISOString();
    
    // Vérifier déblocages
    this.checkUnlockConditions();
    
    // Sauvegarder et notifier
    await this.saveProgress();
    this.notifyListeners();
    
    return true;
  }

  // Vérifier s'il y a un chemin entre deux villages
  private hasPathBetween(fromId: string, toId: string): boolean {
    return this.gameState.paths.some(path => 
      (path.from === fromId && path.to === toId) ||
      (path.from === toId && path.to === fromId)
    );
  }

  // Obtenir les villages adjacents disponibles
  public getAvailableDestinations(fromVillageId: string): Village[] {
    const availablePaths = this.gameState.paths.filter(path => 
      path.from === fromVillageId || path.to === fromVillageId
    );

    const destinationIds = availablePaths.map(path => 
      path.from === fromVillageId ? path.to : path.from
    );

    return this.gameState.villages.filter(village => 
      destinationIds.includes(village.id) && village.unlocked
    );
  }

  // Obtenir le chemin pour l'animation
  public getPathBetween(fromId: string, toId: string): Path | null {
    return this.gameState.paths.find(path => 
      (path.from === fromId && path.to === toId) ||
      (path.from === toId && path.to === fromId)
    ) || null;
  }

  // Compléter un quiz
  public async completeQuiz(villageId: string, success: boolean): Promise<void> {
    if (!this.gameState.progress.completedQuiz.includes(villageId)) {
      this.gameState.progress.completedQuiz.push(villageId);
      
      if (success) {
        this.gameState.progress.score += 20; // Points pour quiz réussi
      } else {
        this.gameState.progress.score += 5; // Points de consolation
      }
    }
    
    this.checkBadges();
    await this.saveProgress();
    this.notifyListeners();
  }

  // Vérifier les conditions de déblocage
  private checkUnlockConditions(): void {
    const worldData = mayotteWorldData as any;
    
    for (const path of worldData.paths) {
      const requirement = path.unlock_requirement;
      let shouldUnlock = false;
      
      switch (requirement.type) {
        case 'visit':
          shouldUnlock = this.gameState.progress.visitedVillages.includes(requirement.village);
          break;
        case 'visit_count':
          shouldUnlock = this.gameState.progress.visitedVillages.length >= requirement.count;
          break;
        case 'quiz_success':
          shouldUnlock = this.gameState.progress.completedQuiz.length >= requirement.count;
          break;
      }
      
      if (shouldUnlock) {
        const targetVillage = this.gameState.villages.find(v => v.id === path.to);
        if (targetVillage && !targetVillage.unlocked) {
          targetVillage.unlocked = true;
          if (!this.gameState.progress.unlockedVillages.includes(path.to)) {
            this.gameState.progress.unlockedVillages.push(path.to);
            this.gameState.progress.score += 15; // Points pour déblocage
          }
        }
      }
    }
  }

  // Vérifier les badges
  private checkBadges(): void {
    const worldData = mayotteWorldData as any;
    
    for (const badge of worldData.progression.badges) {
      if (this.gameState.progress.badges.includes(badge.id)) {
        continue;
      }
      
      let earned = false;
      
      switch (badge.requirement.type) {
        case 'visit_count':
          earned = this.gameState.progress.visitedVillages.length >= badge.requirement.count;
          break;
        case 'quiz_success':
          earned = this.gameState.progress.completedQuiz.length >= badge.requirement.count;
          break;
        case 'visit_all':
          earned = this.gameState.progress.visitedVillages.length >= worldData.villages.length;
          break;
      }
      
      if (earned) {
        this.gameState.progress.badges.push(badge.id);
        this.gameState.progress.score += 50; // Points bonus pour badge
      }
    }
  }

  // Charger la progression sauvegardée
  private async loadProgress(): Promise<PlayerProgress> {
    try {
      const savedData = await AsyncStorage.getItem('mayotte_game_progress');
      if (savedData) {
        return JSON.parse(savedData);
      }
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    }
    
    // Progression par défaut
    return {
      currentVillage: 'mamoudzou',
      visitedVillages: ['mamoudzou'],
      unlockedVillages: ['mamoudzou'],
      completedQuiz: [],
      score: 0,
      badges: [],
      lastPlayTime: new Date().toISOString(),
    };
  }

  // Sauvegarder la progression
  private async saveProgress(): Promise<void> {
    try {
      const progressData = JSON.stringify(this.gameState.progress);
      await AsyncStorage.setItem('mayotte_game_progress', progressData);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
    }
  }

  // Réinitialiser le jeu
  public async resetGame(): Promise<void> {
    await AsyncStorage.removeItem('mayotte_game_progress');
    await this.initializeGame();
  }

  // Obtenir les statistiques
  public getGameStats(): {
    villagesVisited: number;
    totalVillages: number;
    quizCompleted: number;
    totalQuiz: number;
    badges: number;
    totalBadges: number;
    score: number;
  } {
    const worldData = mayotteWorldData as any;
    
    return {
      villagesVisited: this.gameState.progress.visitedVillages.length,
      totalVillages: worldData.villages.length,
      quizCompleted: this.gameState.progress.completedQuiz.length,
      totalQuiz: worldData.villages.filter((v: any) => v.meta.quiz).length,
      badges: this.gameState.progress.badges.length,
      totalBadges: worldData.progression.badges.length,
      score: this.gameState.progress.score,
    };
  }
}

export default MayotteGameEngine;