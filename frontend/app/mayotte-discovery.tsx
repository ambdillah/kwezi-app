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

import RealisticMayotteMap from '../components/RealisticMayotteMap';
import AnimatedMaki from '../components/AnimatedMaki';
import VillageDiscoveryPanel from '../components/VillageDiscoveryPanel';
import MayotteGameEngine, { Village, GameState } from '../utils/mayotteGameEngine';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface CommuneInfo {
  id: string;
  name: string;
  fullName: string;
  description: string;
  specialties: string[];
  history: string;
  legends: string[];
  funFacts: string[];
  quiz: QuizQuestion[];
  price?: number;
  isUnlocked: boolean;
}

interface QuizQuestion {
  id: string;
  question: string;
  answers: string[];
  correctAnswer: number;
  explanation: string;
}

// Données des communes de Mayotte
const MAYOTTE_COMMUNES: CommuneInfo[] = [
  {
    id: 'mamoudzou',
    name: 'Mamoudzou',
    fullName: 'Mamoudzou - La Capitale',
    description: 'Capitale et plus grande ville de Mayotte, centre économique et administratif de l\'île.',
    specialties: ['Marché couvert', 'Port de pêche', 'Artisanat local', 'Ylang-ylang'],
    history: 'Mamoudzou est devenu le chef-lieu de Mayotte en 1977. Son nom signifie "lieu de Mtsambou" en shimaoré.',
    legends: [
      'La légende raconte qu\'un grand sultan y vivait autrefois',
      'Les esprits des ancêtres protègent encore la baie'
    ],
    funFacts: [
      'Plus de 71 000 habitants',
      'Port principal de Mayotte',
      'Siège de la préfecture'
    ],
    quiz: [
      {
        id: 'mamoudzou_q1',
        question: 'Depuis quand Mamoudzou est-il le chef-lieu de Mayotte ?',
        answers: ['1975', '1977', '1980', '1983'],
        correctAnswer: 1,
        explanation: 'Mamoudzou est devenu chef-lieu de Mayotte en 1977, remplaçant Dzaoudzi.'
      },
      {
        id: 'mamoudzou_q2',
        question: 'Que signifie "Mamoudzou" en shimaoré ?',
        answers: ['Grande ville', 'Lieu de Mtsambou', 'Port royal', 'Baie sacrée'],
        correctAnswer: 1,
        explanation: 'Mamoudzou signifie "lieu de Mtsambou" en shimaoré, du nom d\'un ancien chef local.'
      }
    ],
    isUnlocked: true
  },
  {
    id: 'dzaoudzi',
    name: 'Dzaoudzi',
    fullName: 'Dzaoudzi-Labattoir - L\'Ancienne Capitale',
    description: 'Ancienne capitale située sur Petite-Terre, près de l\'aéroport international.',
    specialties: ['Aéroport international', 'Plages de sable blanc', 'Baobabs centenaires'],
    history: 'Ancienne capitale de Mayotte jusqu\'en 1977. Dzaoudzi fut le siège du pouvoir colonial français.',
    legends: [
      'Les baobabs géants seraient les gardiens de l\'île',
      'Un trésor de pirates serait caché dans les grottes'
    ],
    funFacts: [
      'Située sur Petite-Terre',
      'Reliée par barge à Grande-Terre',
      'Aéroport Dzaoudzi-Pamandzi'
    ],
    quiz: [
      {
        id: 'dzaoudzi_q1',
        question: 'Sur quelle île se trouve Dzaoudzi ?',
        answers: ['Grande-Terre', 'Petite-Terre', 'Île aux Makis', 'Îlot de sable'],
        correctAnswer: 1,
        explanation: 'Dzaoudzi se trouve sur Petite-Terre, reliée à Grande-Terre par des barges.'
      }
    ],
    isUnlocked: false
  },
  {
    id: 'sada',
    name: 'Sada',
    fullName: 'Sada - Village des Pêcheurs',
    description: 'Charmant village de pêcheurs sur la côte ouest, réputé pour ses couchers de soleil.',
    specialties: ['Pêche traditionnelle', 'Couchers de soleil', 'Cuisine locale', 'Pirogues'],
    history: 'Sada est l\'un des plus anciens villages de pêcheurs de Mayotte, avec une tradition maritime séculaire.',
    legends: [
      'Les dauphins guident les pêcheurs vers les bancs de poissons',
      'Une sirène protège les marins de Sada'
    ],
    funFacts: [
      'Plus beau coucher de soleil de Mayotte',
      'Tradition de pêche au lamparo',
      'Fabrication artisanale de pirogues'
    ],
    quiz: [
      {
        id: 'sada_q1',
        question: 'Pour quoi Sada est-il particulièrement réputé ?',
        answers: ['Ses montagnes', 'Ses couchers de soleil', 'Ses cascades', 'Ses plantations'],
        correctAnswer: 1,
        explanation: 'Sada est célèbre pour ses magnifiques couchers de soleil sur l\'océan Indien.'
      }
    ],
    isUnlocked: false,
    price: 1.99
  },
  {
    id: 'tsingoni',
    name: 'Tsingoni',
    fullName: 'Tsingoni - Première Mosquée de France',
    description: 'Village historique abritant la plus ancienne mosquée de France (1538).',
    specialties: ['Mosquée historique', 'Architecture traditionnelle', 'Artisanat religieux'],
    history: 'Tsingoni abrite la plus ancienne mosquée de France, construite en 1538. Centre spirituel important.',
    legends: [
      'La mosquée aurait été construite par des anges en une nuit',
      'L\'eau du puits sacré guérit les maux'
    ],
    funFacts: [
      'Mosquée la plus ancienne de France (1538)',
      'Architecture arabo-swahilie unique',
      'Lieu de pèlerinage musulman'
    ],
    quiz: [
      {
        id: 'tsingoni_q1',
        question: 'En quelle année fut construite la mosquée de Tsingoni ?',
        answers: ['1520', '1538', '1550', '1565'],
        correctAnswer: 1,
        explanation: 'La mosquée de Tsingoni fut construite en 1538, en faisant la plus ancienne mosquée de France.'
      }
    ],
    isUnlocked: false,
    price: 2.99
  }
];

export default function MayotteDiscoveryGame() {
  const [currentCommune, setCurrentCommune] = useState<string>('mamoudzou');
  const [unlockedCommunes, setUnlockedCommunes] = useState<string[]>(['mamoudzou']);
  const [showCommuneInfo, setShowCommuneInfo] = useState(false);
  const [selectedCommuneInfo, setSelectedCommuneInfo] = useState<CommuneInfo | null>(null);
  const [showQuiz, setShowQuiz] = useState(false);
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0);
  const [quizScore, setQuizScore] = useState(0);
  const [gameProgress, setGameProgress] = useState(0);

  // Animation pour le maki
  const makiPosition = useRef(new Animated.ValueXY({ x: 200, y: 180 })).current;
  const makiBounce = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    loadGameProgress();
    // Animation de pulsation pour le maki
    Animated.loop(
      Animated.sequence([
        Animated.timing(makiBounce, { toValue: 1.1, duration: 1000, useNativeDriver: true }),
        Animated.timing(makiBounce, { toValue: 1, duration: 1000, useNativeDriver: true })
      ])
    ).start();
  }, []);

  const loadGameProgress = async () => {
    try {
      const savedProgress = await AsyncStorage.getItem('mayotte_game_progress');
      if (savedProgress) {
        const progress = JSON.parse(savedProgress);
        setUnlockedCommunes(progress.unlockedCommunes || ['mamoudzou']);
        setCurrentCommune(progress.currentCommune || 'mamoudzou');
        setGameProgress(progress.gameProgress || 0);
      }
    } catch (error) {
      console.log('Erreur chargement progression:', error);
    }
  };

  const saveGameProgress = async () => {
    try {
      const progress = {
        unlockedCommunes,
        currentCommune,
        gameProgress
      };
      await AsyncStorage.setItem('mayotte_game_progress', JSON.stringify(progress));
    } catch (error) {
      console.log('Erreur sauvegarde progression:', error);
    }
  };

  const animateMakiToCommune = (commune: CommuneData) => {
    Animated.sequence([
      // Animation de saut
      Animated.timing(makiBounce, {
        toValue: 1.3,
        duration: 200,
        useNativeDriver: true
      }),
      // Déplacement vers la nouvelle position
      Animated.timing(makiPosition, {
        toValue: { x: commune.position.x, y: commune.position.y },
        duration: 1500,
        useNativeDriver: false
      }),
      // Atterrissage
      Animated.timing(makiBounce, {
        toValue: 1,
        duration: 200,
        useNativeDriver: true
      })
    ]).start();
  };

  const handleCommunePress = (commune: CommuneData) => {
    const communeInfo = MAYOTTE_COMMUNES.find(c => c.id === commune.id);
    if (!communeInfo) return;

    if (!unlockedCommunes.includes(commune.id)) {
      // Commune verrouillée
      if (communeInfo.price) {
        Alert.alert(
          `🔒 ${communeInfo.name} - Commune Premium`,
          `Débloquez cette commune pour €${communeInfo.price} et découvrez ses secrets !`,
          [
            { text: 'Plus tard', style: 'cancel' },
            { text: `Débloquer €${communeInfo.price}`, onPress: () => handlePurchaseCommune(commune.id) }
          ]
        );
      } else {
        Alert.alert(
          '🔒 Commune verrouillée',
          'Terminez les quiz des communes précédentes pour débloquer celle-ci !',
          [{ text: 'OK' }]
        );
      }
      return;
    }

    // Commune débloquée - afficher les informations
    setSelectedCommuneInfo(communeInfo);
    setCurrentCommune(commune.id);
    animateMakiToCommune(commune);
    setShowCommuneInfo(true);
    
    // Lire le nom de la commune
    speakEducationalContent(`Bienvenue à ${communeInfo.fullName}`, 'fr');
  };

  const handlePurchaseCommune = (communeId: string) => {
    // TODO: Intégrer système de paiement (Stripe)
    Alert.alert(
      '💳 Achat Premium',
      'Fonctionnalité de paiement à venir ! Pour le moment, cette commune est débloquée gratuitement.',
      [
        {
          text: 'Super !',
          onPress: () => {
            setUnlockedCommunes(prev => [...prev, communeId]);
            saveGameProgress();
          }
        }
      ]
    );
  };

  const startQuiz = () => {
    if (!selectedCommuneInfo) return;
    setShowCommuneInfo(false);
    setCurrentQuizIndex(0);
    setQuizScore(0);
    setShowQuiz(true);
  };

  const handleQuizAnswer = (answerIndex: number) => {
    if (!selectedCommuneInfo) return;

    const question = selectedCommuneInfo.quiz[currentQuizIndex];
    const isCorrect = answerIndex === question.correctAnswer;

    if (isCorrect) {
      setQuizScore(prev => prev + 1);
      Alert.alert('✅ Correct !', question.explanation, [
        { text: 'Continuer', onPress: nextQuizQuestion }
      ]);
    } else {
      Alert.alert('❌ Incorrect', question.explanation, [
        { text: 'Continuer', onPress: nextQuizQuestion }
      ]);
    }
  };

  const nextQuizQuestion = () => {
    if (!selectedCommuneInfo) return;

    if (currentQuizIndex < selectedCommuneInfo.quiz.length - 1) {
      setCurrentQuizIndex(prev => prev + 1);
    } else {
      // Quiz terminé
      const scorePercentage = (quizScore / selectedCommuneInfo.quiz.length) * 100;
      
      if (scorePercentage >= 70) {
        // Quiz réussi - débloquer prochaine commune
        unlockNextCommune();
      } else {
        Alert.alert(
          '📚 Pas mal !',
          `Score: ${quizScore}/${selectedCommuneInfo.quiz.length}\nVous pouvez recommencer pour améliorer votre score !`,
          [{ text: 'OK', onPress: () => setShowQuiz(false) }]
        );
      }
    }
  };

  const unlockNextCommune = () => {
    setShowQuiz(false);
    setGameProgress(prev => prev + 1);
    
    Alert.alert(
      '🎉 Quiz réussi !',
      `Félicitations ! Vous avez débloqué de nouvelles communes à explorer !`,
      [
        {
          text: 'Explorer !',
          onPress: () => {
            // Débloquer la prochaine commune disponible
            const nextCommune = MAYOTTE_COMMUNES.find(c => 
              !unlockedCommunes.includes(c.id) && !c.price
            );
            if (nextCommune) {
              setUnlockedCommunes(prev => [...prev, nextCommune.id]);
            }
            saveGameProgress();
          }
        }
      ]
    );
  };

  const getCurrentMakiPosition = () => {
    const commune = MAYOTTE_COMMUNES.find(c => c.id === currentCommune);
    return commune ? { x: commune.quiz[0] ? 285 : 285, y: commune.quiz[0] ? 220 : 220 } : { x: 285, y: 220 }; // Position Mamoudzou par défaut
  };

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={['#E3F2FD', '#BBDEFB', '#90CAF9']}
        style={styles.gradient}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#1565C0" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>🏝️ Découverte de Mayotte</Text>
          <View style={styles.progressContainer}>
            <Text style={styles.progressText}>{gameProgress}/10</Text>
          </View>
        </View>

        {/* Carte principale */}
        <View style={styles.mapContainer}>
          <Animated.View style={{ transform: [{ scale: makiBounce }] }}>
            <MayotteMap
              width={SCREEN_WIDTH - 40}
              height={400}
              onCommunePress={handleCommunePress}
              unlockedCommunes={unlockedCommunes}
              currentCommune={currentCommune}
              makiPosition={getCurrentMakiPosition()}
            />
          </Animated.View>
        </View>

        {/* Instructions */}
        <View style={styles.instructionsContainer}>
          <Text style={styles.instructionsText}>
            🐒 Guidez le maki à travers Mayotte ! Touchez une commune pour découvrir ses secrets.
          </Text>
        </View>

        {/* Modal d'informations sur la commune */}
        <Modal
          visible={showCommuneInfo}
          animationType="slide"
          transparent={true}
          onRequestClose={() => setShowCommuneInfo(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              {selectedCommuneInfo && (
                <ScrollView showsVerticalScrollIndicator={false}>
                  <TouchableOpacity
                    style={styles.closeButton}
                    onPress={() => setShowCommuneInfo(false)}
                  >
                    <Ionicons name="close" size={24} color="#666" />
                  </TouchableOpacity>

                  <Text style={styles.modalTitle}>{selectedCommuneInfo.fullName}</Text>
                  
                  <Text style={styles.modalDescription}>{selectedCommuneInfo.description}</Text>

                  <View style={styles.section}>
                    <Text style={styles.sectionTitle}>🍽️ Spécialités locales</Text>
                    {selectedCommuneInfo.specialties.map((specialty, index) => (
                      <Text key={index} style={styles.listItem}>• {specialty}</Text>
                    ))}
                  </View>

                  <View style={styles.section}>
                    <Text style={styles.sectionTitle}>📚 Histoire</Text>
                    <Text style={styles.sectionText}>{selectedCommuneInfo.history}</Text>
                  </View>

                  <View style={styles.section}>
                    <Text style={styles.sectionTitle}>🌟 Légendes</Text>
                    {selectedCommuneInfo.legends.map((legend, index) => (
                      <Text key={index} style={styles.listItem}>• {legend}</Text>
                    ))}
                  </View>

                  <View style={styles.section}>
                    <Text style={styles.sectionTitle}>🎯 Le saviez-vous ?</Text>
                    {selectedCommuneInfo.funFacts.map((fact, index) => (
                      <Text key={index} style={styles.listItem}>• {fact}</Text>
                    ))}
                  </View>

                  <TouchableOpacity style={styles.quizButton} onPress={startQuiz}>
                    <Text style={styles.quizButtonText}>🧠 Tester mes connaissances</Text>
                  </TouchableOpacity>
                </ScrollView>
              )}
            </View>
          </View>
        </Modal>

        {/* Modal de quiz */}
        <Modal
          visible={showQuiz}
          animationType="fade"
          transparent={true}
          onRequestClose={() => setShowQuiz(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.quizModalContent}>
              {selectedCommuneInfo && selectedCommuneInfo.quiz[currentQuizIndex] && (
                <>
                  <Text style={styles.quizProgress}>
                    Question {currentQuizIndex + 1}/{selectedCommuneInfo.quiz.length}
                  </Text>
                  
                  <Text style={styles.quizQuestion}>
                    {selectedCommuneInfo.quiz[currentQuizIndex].question}
                  </Text>
                  
                  {selectedCommuneInfo.quiz[currentQuizIndex].answers.map((answer, index) => (
                    <TouchableOpacity
                      key={index}
                      style={styles.answerButton}
                      onPress={() => handleQuizAnswer(index)}
                    >
                      <Text style={styles.answerText}>{answer}</Text>
                    </TouchableOpacity>
                  ))}
                  
                  <TouchableOpacity
                    style={styles.quitQuizButton}
                    onPress={() => setShowQuiz(false)}
                  >
                    <Text style={styles.quitQuizText}>Quitter le quiz</Text>
                  </TouchableOpacity>
                </>
              )}
            </View>
          </View>
        </Modal>
      </LinearGradient>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.2)',
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(255,255,255,0.9)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1565C0',
    flex: 1,
    textAlign: 'center',
  },
  progressContainer: {
    backgroundColor: 'rgba(255,255,255,0.9)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
  },
  progressText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#1565C0',
  },
  mapContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  instructionsContainer: {
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: 'rgba(255,255,255,0.9)',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  instructionsText: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    lineHeight: 24,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: SCREEN_WIDTH - 40,
    maxHeight: SCREEN_HEIGHT - 100,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
  },
  closeButton: {
    alignSelf: 'flex-end',
    padding: 5,
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 15,
  },
  modalDescription: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 24,
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 10,
  },
  sectionText: {
    fontSize: 15,
    color: '#666',
    lineHeight: 22,
  },
  listItem: {
    fontSize: 15,
    color: '#666',
    marginBottom: 5,
    lineHeight: 22,
  },
  quizButton: {
    backgroundColor: '#4ECDC4',
    borderRadius: 25,
    paddingVertical: 15,
    paddingHorizontal: 30,
    alignItems: 'center',
    marginTop: 20,
  },
  quizButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
  },
  quizModalContent: {
    width: SCREEN_WIDTH - 40,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 30,
  },
  quizProgress: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  quizQuestion: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 25,
    lineHeight: 26,
  },
  answerButton: {
    backgroundColor: '#F8F9FA',
    borderRadius: 15,
    padding: 15,
    marginBottom: 10,
    borderWidth: 2,
    borderColor: '#E9ECEF',
  },
  answerText: {
    fontSize: 16,
    color: '#2C3E50',
    textAlign: 'center',
  },
  quitQuizButton: {
    marginTop: 20,
    alignItems: 'center',
  },
  quitQuizText: {
    fontSize: 14,
    color: '#666',
  },
});