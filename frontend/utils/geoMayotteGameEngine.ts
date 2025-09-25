import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  MAYOTTE_VILLAGES,
  MAYOTTE_PATHS,
  MAYOTTE_CENTER,
  VillageGeoData,
  GeoPath,
  GeoCoordinate
} from './mayotteGeoData';

export interface GeoPlayerProgress {
  currentVillage: string;
  visitedVillages: string[];
  unlockedVillages: string[];
  completedQuiz: string[];
  score: number;
  badges: string[];
  lastPlayTime: string;
  currentPosition: GeoCoordinate;
}

export interface GeoGameState {
  villages: VillageGeoData[];
  paths: GeoPath[];
  progress: GeoPlayerProgress;
  isLoaded: boolean;
}

/**
 * Moteur de jeu géolocalisé pour Mayotte Discovery
 * Utilise les vraies coordonnées GPS de Mayotte
 */
class GeoMayotteGameEngine {
  private static instance: GeoMayotteGameEngine;
  private gameState: GeoGameState;
  private listeners: Array<(state: GeoGameState) => void> = [];

  private constructor() {
    const initialVillage = MAYOTTE_VILLAGES.find(v => v.id === 'mamoudzou')!;
    
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
        currentPosition: initialVillage.coordinates,
      },
      isLoaded: false,
    };
  }

  public static getInstance(): GeoMayotteGameEngine {
    if (!GeoMayotteGameEngine.instance) {
      GeoMayotteGameEngine.instance = new GeoMayotteGameEngine();
    }
    return GeoMayotteGameEngine.instance;
  }

  /**
   * Initialise le jeu avec les données géographiques
   */
  public async initializeGame(): Promise<void> {
    try {
      // Charger la progression sauvegardée
      const savedProgress = await this.loadProgress();
      
      // Créer l'état du jeu avec les vraies données géographiques
      this.gameState = {
        villages: MAYOTTE_VILLAGES.map((village) => ({
          ...village,
          unlocked: savedProgress.unlockedVillages.includes(village.id),
        })),
        paths: MAYOTTE_PATHS,
        progress: savedProgress,
        isLoaded: true,
      };
      
      // Vérifier et débloquer de nouveaux villages
      this.checkUnlockConditions();
      
      this.notifyListeners();
    } catch (error) {
      console.error('Erreur lors de l\'initialisation du jeu géolocalisé:', error);
    }
  }

  /**
   * S'abonner aux changements d'état
   */
  public subscribe(listener: (state: GeoGameState) => void): () => void {
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

  /**
   * Obtenir l'état actuel du jeu
   */
  public getGameState(): GeoGameState {
    return this.gameState;
  }

  /**
   * Voyager vers un village avec animation GPS
   */
  public async travelToVillage(villageId: string): Promise<{
    success: boolean;
    path?: GeoCoordinate[];
    distance?: number;
  }> {
    const village = this.gameState.villages.find(v => v.id === villageId);
    if (!village || !village.unlocked) {
      return { success: false };
    }

    // Vérifier s'il y a un chemin depuis le village actuel
    const pathData = this.getPathBetween(this.gameState.progress.currentVillage, villageId);
    if (!pathData && villageId !== this.gameState.progress.currentVillage) {
      return { success: false };
    }

    // Mettre à jour la progression
    this.gameState.progress.currentVillage = villageId;
    this.gameState.progress.currentPosition = village.coordinates;
    
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
    
    return {
      success: true,
      path: pathData?.coordinates || [village.coordinates],
      distance: pathData?.distance || 0
    };
  }

  /**
   * Obtenir le chemin GPS entre deux villages
   */
  public getPathBetween(fromId: string, toId: string): GeoPath | null {
    return MAYOTTE_PATHS.find(path => 
      (path.from === fromId && path.to === toId) ||
      (path.from === toId && path.to === fromId)
    ) || null;
  }

  /**
   * Obtenir les villages adjacents disponibles
   */
  public getAvailableDestinations(fromVillageId: string): VillageGeoData[] {
    const availablePaths = MAYOTTE_PATHS.filter(path => 
      path.from === fromVillageId || path.to === fromVillageId
    );

    const destinationIds = availablePaths.map(path => 
      path.from === fromVillageId ? path.to : path.from
    );

    return this.gameState.villages.filter(village => 
      destinationIds.includes(village.id) && village.unlocked
    );
  }

  /**
   * Calculer la distance entre deux coordonnées GPS (en km)
   */
  public calculateDistance(coord1: GeoCoordinate, coord2: GeoCoordinate): number {
    const R = 6371; // Rayon de la Terre en km
    const dLat = this.deg2rad(coord2.latitude - coord1.latitude);
    const dLon = this.deg2rad(coord2.longitude - coord1.longitude);
    
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(this.deg2rad(coord1.latitude)) * Math.cos(this.deg2rad(coord2.latitude)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c; // Distance en km
    
    return Math.round(distance * 100) / 100; // Arrondir à 2 décimales
  }

  private deg2rad(deg: number): number {
    return deg * (Math.PI/180);
  }

  /**
   * Interpoler le long d'un chemin GPS
   */
  public interpolateAlongPath(
    path: GeoCoordinate[], 
    progress: number // 0 à 1
  ): GeoCoordinate {
    if (path.length === 0) return MAYOTTE_CENTER;
    if (path.length === 1) return path[0];
    if (progress <= 0) return path[0];
    if (progress >= 1) return path[path.length - 1];

    // Calculer les distances cumulées
    const distances = [0];
    for (let i = 1; i < path.length; i++) {
      const dist = this.calculateDistance(path[i-1], path[i]);
      distances.push(distances[i-1] + dist);
    }

    const totalDistance = distances[distances.length - 1];
    const targetDistance = totalDistance * progress;

    // Trouver le segment approprié
    for (let i = 1; i < distances.length; i++) {
      if (distances[i] >= targetDistance) {
        const segmentStart = distances[i-1];
        const segmentEnd = distances[i];
        const segmentProgress = (targetDistance - segmentStart) / (segmentEnd - segmentStart);
        
        // Interpolation linéaire entre les deux points
        const startPoint = path[i-1];
        const endPoint = path[i];
        
        return {
          latitude: startPoint.latitude + (endPoint.latitude - startPoint.latitude) * segmentProgress,
          longitude: startPoint.longitude + (endPoint.longitude - startPoint.longitude) * segmentProgress
        };
      }
    }

    return path[path.length - 1];
  }

  /**
   * Compléter un quiz
   */
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

  /**
   * Vérifier les conditions de déblocage
   */
  private checkUnlockConditions(): void {
    for (const path of MAYOTTE_PATHS) {
      const requirement = path.unlock_requirement;
      let shouldUnlock = false;
      
      switch (requirement.type) {
        case 'visit':
          shouldUnlock = this.gameState.progress.visitedVillages.includes(requirement.village!);
          break;
        case 'visit_count':
          shouldUnlock = this.gameState.progress.visitedVillages.length >= requirement.count!;
          break;
        case 'quiz_success':
          shouldUnlock = this.gameState.progress.completedQuiz.length >= requirement.count!;
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

  /**
   * Vérifier les badges
   */
  private checkBadges(): void {
    const badges = [
      {
        id: 'explorateur',
        name: 'Explorateur de Mayotte',
        description: 'Visite 3 villages différents',
        requirement: { type: 'visit_count', count: 3 },
        icon: '🗺️'
      },
      {
        id: 'connaisseur',
        name: 'Connaisseur de Mayotte',
        description: 'Réussis 5 quiz',
        requirement: { type: 'quiz_success', count: 5 },
        icon: '🎓'
      },
      {
        id: 'aventurier',
        name: 'Grand Aventurier',
        description: 'Visite tous les villages',
        requirement: { type: 'visit_all' },
        icon: '🏆'
      }
    ];
    
    for (const badge of badges) {
      if (this.gameState.progress.badges.includes(badge.id)) {
        continue;
      }
      
      let earned = false;
      
      switch (badge.requirement.type) {
        case 'visit_count':
          earned = this.gameState.progress.visitedVillages.length >= badge.requirement.count!;
          break;
        case 'quiz_success':
          earned = this.gameState.progress.completedQuiz.length >= badge.requirement.count!;
          break;
        case 'visit_all':
          earned = this.gameState.progress.visitedVillages.length >= MAYOTTE_VILLAGES.length;
          break;
      }
      
      if (earned) {
        this.gameState.progress.badges.push(badge.id);
        this.gameState.progress.score += 50; // Points bonus pour badge
      }
    }
  }

  /**
   * Charger la progression sauvegardée
   */
  private async loadProgress(): Promise<GeoPlayerProgress> {
    try {
      const savedData = await AsyncStorage.getItem('mayotte_geo_game_progress');
      if (savedData) {
        const loaded = JSON.parse(savedData);
        // S'assurer que currentPosition existe
        if (!loaded.currentPosition) {
          const initialVillage = MAYOTTE_VILLAGES.find(v => v.id === loaded.currentVillage);
          loaded.currentPosition = initialVillage?.coordinates || MAYOTTE_CENTER;
        }
        return loaded;
      }
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    }
    
    // Progression par défaut
    const initialVillage = MAYOTTE_VILLAGES.find(v => v.id === 'mamoudzou')!;
    return {
      currentVillage: 'mamoudzou',
      visitedVillages: ['mamoudzou'],
      unlockedVillages: ['mamoudzou'],
      completedQuiz: [],
      score: 0,
      badges: [],
      lastPlayTime: new Date().toISOString(),
      currentPosition: initialVillage.coordinates,
    };
  }

  /**
   * Sauvegarder la progression
   */
  private async saveProgress(): Promise<void> {
    try {
      const progressData = JSON.stringify(this.gameState.progress);
      await AsyncStorage.setItem('mayotte_geo_game_progress', progressData);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
    }
  }

  /**
   * Réinitialiser le jeu
   */
  public async resetGame(): Promise<void> {
    await AsyncStorage.removeItem('mayotte_geo_game_progress');
    await this.initializeGame();
  }

  /**
   * Obtenir les statistiques du jeu
   */
  public getGameStats(): {
    villagesVisited: number;
    totalVillages: number;
    quizCompleted: number;
    totalQuiz: number;
    badges: number;
    totalBadges: number;
    score: number;
    totalDistance: number;
  } {
    // Calculer la distance totale parcourue
    let totalDistance = 0;
    const visitedVillages = this.gameState.progress.visitedVillages;
    for (let i = 1; i < visitedVillages.length; i++) {
      const fromVillage = MAYOTTE_VILLAGES.find(v => v.id === visitedVillages[i-1]);
      const toVillage = MAYOTTE_VILLAGES.find(v => v.id === visitedVillages[i]);
      if (fromVillage && toVillage) {
        totalDistance += this.calculateDistance(fromVillage.coordinates, toVillage.coordinates);
      }
    }
    
    return {
      villagesVisited: this.gameState.progress.visitedVillages.length,
      totalVillages: MAYOTTE_VILLAGES.length,
      quizCompleted: this.gameState.progress.completedQuiz.length,
      totalQuiz: MAYOTTE_VILLAGES.filter(v => v.meta.quiz).length,
      badges: this.gameState.progress.badges.length,
      totalBadges: 3, // Nombre de badges disponibles
      score: this.gameState.progress.score,
      totalDistance: Math.round(totalDistance * 100) / 100,
    };
  }
}

export default GeoMayotteGameEngine;