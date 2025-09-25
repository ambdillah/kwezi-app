import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  Alert,
  StatusBar,
  Dimensions,
  Vibration,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSequence,
  interpolate,
  runOnJS,
} from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';

import MapLibreMayotteMap from '../components/MapLibreMayotteMap';
import VillageDiscoveryPanel from '../components/VillageDiscoveryPanel';
import GeoMayotteGameEngine, { VillageGeoData, GeoGameState, GeoCoordinate } from '../utils/geoMayotteGameEngine';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

const MayotteDiscoveryGame: React.FC = () => {
  // Game Engine géolocalisé
  const gameEngine = GeoMayotteGameEngine.getInstance();
  
  // State
  const [gameState, setGameState] = useState<GeoGameState>(gameEngine.getGameState());
  const [selectedVillage, setSelectedVillage] = useState<VillageGeoData | null>(null);
  const [showDiscoveryPanel, setShowDiscoveryPanel] = useState(false);
  const [makiPosition, setMakiPosition] = useState<GeoCoordinate>({ latitude: -12.7822, longitude: 45.2281 }); // Mamoudzou
  const [isMoving, setIsMoving] = useState(false);
  const [showStats, setShowStats] = useState(false);

  // Animations
  const statsScale = useSharedValue(0);
  const celebrationScale = useSharedValue(0);
  const movementProgress = useSharedValue(0);

  useEffect(() => {
    // Initialiser le jeu géolocalisé
    const initGame = async () => {
      await gameEngine.initializeGame();
    };

    initGame();
    
    const unsubscribe = gameEngine.subscribe((newState: GeoGameState) => {
      setGameState(newState);
      
      // Mettre à jour la position GPS du maki
      setMakiPosition(newState.progress.currentPosition);
    });

    return unsubscribe;
  }, []);

  // Animation styles
  const statsStyle = useAnimatedStyle(() => {
    return {
      transform: [{ scale: statsScale.value }],
    };
  });

  const celebrationStyle = useAnimatedStyle(() => {
    const scale = celebrationScale.value;
    const opacity = interpolate(scale, [0, 0.5, 1], [0, 1, 0]);
    
    return {
      transform: [{ scale }],
      opacity,
    };
  });

  // Handlers
  const handleVillagePress = async (villageId: string) => {
    const village = gameState.villages.find(v => v.id === villageId);
    if (!village || !village.unlocked) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      Alert.alert(
        'Village verrouillé', 
        'Explorez d\'abord les villages voisins pour débloquer celui-ci !'
      );
      return;
    }

    // Vérifier s'il y a un chemin disponible
    const availableDestinations = gameEngine.getAvailableDestinations(gameState.progress.currentVillage);
    const isAccessible = availableDestinations.some(dest => dest.id === villageId);
    
    if (!isAccessible && villageId !== gameState.progress.currentVillage) {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
      Alert.alert(
        'Chemin non disponible', 
        'Vous ne pouvez pas vous rendre directement dans ce village depuis votre position actuelle.'
      );
      return;
    }

    if (villageId === gameState.progress.currentVillage) {
      // Déjà dans ce village, ouvrir le panneau de découverte
      setSelectedVillage(village);
      setShowDiscoveryPanel(true);
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    } else {
      // Voyager vers le village avec animation GPS
      await animateGPSMovement(village);
    }
  };

  const animateGPSMovement = async (targetVillage: VillageGeoData) => {
    setIsMoving(true);
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    
    // Obtenir le chemin GPS réel
    const travelResult = await gameEngine.travelToVillage(targetVillage.id);
    
    if (travelResult.success && travelResult.path) {
      // Animer le maki le long du chemin GPS
      const animationDuration = Math.max(2000, travelResult.distance! * 200); // 200ms par km
      
      movementProgress.value = withTiming(1, 
        { duration: animationDuration },
        (finished) => {
          if (finished) {
            runOnJS(() => {
              setIsMoving(false);
              
              // Animation de célébration
              celebrationScale.value = withSequence(
                withTiming(1.2, { duration: 300 }),
                withTiming(0, { duration: 300 })
              );
              
              Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
              Vibration.vibrate([100, 50, 100]);
              
              // Ouvrir automatiquement le panneau de découverte
              setTimeout(() => {
                setSelectedVillage(targetVillage);
                setShowDiscoveryPanel(true);
              }, 600);
            })();
          }
        }
      );

      // Mise à jour de la position en temps réel pendant l'animation
      const intervalId = setInterval(() => {
        const currentProgress = movementProgress.value;
        const interpolatedPosition = gameEngine.interpolateAlongPath(travelResult.path!, currentProgress);
        setMakiPosition(interpolatedPosition);
        
        if (currentProgress >= 1) {
          clearInterval(intervalId);
          movementProgress.value = 0;
        }
      }, 50); // Mise à jour toutes les 50ms
    } else {
      setIsMoving(false);
      Alert.alert('Erreur', 'Impossible de se rendre dans ce village.');
    }
  };

  const handleQuizComplete = (success: boolean) => {
    if (selectedVillage) {
      gameEngine.completeQuiz(selectedVillage.id, success);
      
      if (success) {
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      } else {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
      }
    }
  };

  const toggleStats = () => {
    setShowStats(!showStats);
    statsScale.value = withTiming(showStats ? 0 : 1, { duration: 300 });
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const handleResetGame = () => {
    Alert.alert(
      'Réinitialiser le jeu',
      'Êtes-vous sûr de vouloir recommencer votre exploration de Mayotte ? Toute votre progression sera perdue.',
      [
        { text: 'Annuler', style: 'cancel' },
        { 
          text: 'Réinitialiser', 
          style: 'destructive',
          onPress: async () => {
            await gameEngine.resetGame();
            Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
          }
        },
      ]
    );
  };

  const getStats = () => gameEngine.getGameStats();
  const stats = getStats();

  // Adapter les données pour VillageDiscoveryPanel
  const adaptVillageForPanel = (village: VillageGeoData) => {
    return {
      id: village.id,
      name: village.name,
      pos: { x: 0, y: 0 }, // Non utilisé avec GPS
      type: village.type,
      unlocked: village.unlocked,
      assets: {},
      meta: village.meta
    };
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1B5E20" />
      
      <LinearGradient colors={['#2E7D32', '#388E3C', '#4CAF50']} style={styles.header}>
        <View style={styles.headerContent}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#FFFFFF" />
          </TouchableOpacity>
          
          <View style={styles.headerCenter}>
            <Text style={styles.headerTitle}>Découverte de Mayotte</Text>
            <Text style={styles.headerSubtitle}>
              {gameState.villages.find(v => v.id === gameState.progress.currentVillage)?.name || 'Mamoudzou'}
            </Text>
          </View>
          
          <View style={styles.headerRight}>
            <TouchableOpacity onPress={toggleStats} style={styles.statsButton}>
              <Ionicons name="stats-chart" size={20} color="#FFFFFF" />
              <Text style={styles.scoreText}>{stats.score}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </LinearGradient>

      {/* Panneau des statistiques GPS */}
      {showStats && (
        <Animated.View style={[styles.statsPanel, statsStyle]}>
          <LinearGradient colors={['#E8F5E8', '#F1F8E9']} style={styles.statsContent}>
            <Text style={styles.statsTitle}>📊 Statistiques GPS</Text>
            
            <View style={styles.statsGrid}>
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{stats.villagesVisited}</Text>
                <Text style={styles.statLabel}>Villages visités</Text>
                <Text style={styles.statTotal}>sur {stats.totalVillages}</Text>
              </View>
              
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{stats.quizCompleted}</Text>
                <Text style={styles.statLabel}>Quiz réussis</Text>
                <Text style={styles.statTotal}>sur {stats.totalQuiz}</Text>
              </View>
              
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{stats.badges}</Text>
                <Text style={styles.statLabel}>Badges obtenus</Text>
                <Text style={styles.statTotal}>sur {stats.totalBadges}</Text>
              </View>
              
              <View style={styles.statItem}>
                <Text style={styles.statValue}>{stats.totalDistance}km</Text>
                <Text style={styles.statLabel}>Distance parcourue</Text>
                <Text style={styles.statTotal}>🛣️</Text>
              </View>
            </View>

            <View style={styles.statsActions}>
              <TouchableOpacity onPress={handleResetGame} style={styles.resetButton}>
                <Ionicons name="refresh" size={16} color="#F44336" />
                <Text style={styles.resetText}>Recommencer</Text>
              </TouchableOpacity>
            </View>
          </LinearGradient>
        </Animated.View>
      )}

      {/* Carte MapLibre GL avec vraies données GPS */}
      <View style={styles.mapContainer}>
        <MapLibreMayotteMap
          villages={gameState.villages}
          currentVillage={gameState.progress.currentVillage}
          onVillagePress={handleVillagePress}
          makiPosition={makiPosition}
          isMoving={isMoving}
        />
        
        {/* Animation de célébration */}
        <Animated.View style={[styles.celebrationContainer, celebrationStyle]}>
          <Text style={styles.celebrationText}>🎉</Text>
        </Animated.View>
      </View>

      {/* Panneau de découverte des villages */}
      <VillageDiscoveryPanel
        village={selectedVillage ? adaptVillageForPanel(selectedVillage) : null}
        isVisible={showDiscoveryPanel}
        onClose={() => setShowDiscoveryPanel(false)}
        onQuizComplete={handleQuizComplete}
      />

      {/* Instructions GPS pour nouveaux joueurs */}
      {gameState.progress.visitedVillages.length === 1 && (
        <View style={styles.instructionsContainer}>
          <LinearGradient colors={['#FFF3E0', '#FFE0B2']} style={styles.instructions}>
            <Ionicons name="navigate" size={20} color="#FF8F00" />
            <Text style={styles.instructionsText}>
              Touchez un village voisin pour commencer votre exploration GPS ! 🗺️
            </Text>
          </LinearGradient>
        </View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E3F2FD',
  },
  header: {
    paddingTop: 10,
    paddingBottom: 15,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  backButton: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  headerCenter: {
    flex: 1,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    marginTop: 2,
  },
  headerRight: {
    alignItems: 'flex-end',
  },
  statsButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    borderRadius: 16,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  scoreText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: 'bold',
    marginLeft: 4,
  },
  statsPanel: {
    position: 'absolute',
    top: 100,
    right: 20,
    zIndex: 20,
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 10,
  },
  statsContent: {
    padding: 16,
    minWidth: 250,
  },
  statsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
    textAlign: 'center',
    marginBottom: 12,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statItem: {
    width: '48%',
    alignItems: 'center',
    marginBottom: 12,
    padding: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
  },
  statTotal: {
    fontSize: 10,
    color: '#999',
  },
  statsActions: {
    alignItems: 'center',
    marginTop: 8,
  },
  resetButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#FFEBEE',
  },
  resetText: {
    color: '#F44336',
    fontSize: 12,
    marginLeft: 4,
  },
  mapContainer: {
    flex: 1,
    position: 'relative',
  },
  celebrationContainer: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{ translateX: -25 }, { translateY: -25 }],
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 15,
  },
  celebrationText: {
    fontSize: 32,
  },
  instructionsContainer: {
    position: 'absolute',
    bottom: 30,
    left: 20,
    right: 20,
    zIndex: 10,
  },
  instructions: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 5,
  },
  instructionsText: {
    flex: 1,
    fontSize: 14,
    color: '#E65100',
    marginLeft: 8,
    fontWeight: '500',
  },
});

export default MayotteDiscoveryGame;