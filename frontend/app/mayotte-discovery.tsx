import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  TouchableOpacity,
  StatusBar,
  ScrollView,
  Modal,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MAYOTTE_VILLAGES, Village, QuizQuestion } from '../data/mayotteVillages';
import Svg, { Path, Circle, Text as SvgText, G } from 'react-native-svg';

const MayotteDiscoveryGame: React.FC = () => {
  const [villages, setVillages] = useState<Village[]>(MAYOTTE_VILLAGES);
  const [selectedVillage, setSelectedVillage] = useState<Village | null>(null);
  const [showQuiz, setShowQuiz] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [totalScore, setTotalScore] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [makiPosition, setMakiPosition] = useState({ x: 55, y: 50 }); // Commence à Mamoudzou
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const savedProgress = await AsyncStorage.getItem('mayotte_discovery_progress');
      if (savedProgress) {
        const { villages: savedVillages, totalScore: savedScore } = JSON.parse(savedProgress);
        setVillages(savedVillages);
        setTotalScore(savedScore);
      }
    } catch (error) {
      console.error('Erreur chargement progression:', error);
    }
  };

  const saveProgress = async (updatedVillages: Village[], newTotalScore: number) => {
    try {
      await AsyncStorage.setItem('mayotte_discovery_progress', JSON.stringify({
        villages: updatedVillages,
        totalScore: newTotalScore,
      }));
    } catch (error) {
      console.error('Erreur sauvegarde progression:', error);
    }
  };

  const animateMakiTo = (targetX: number, targetY: number) => {
    setIsAnimating(true);
    const startX = makiPosition.x;
    const startY = makiPosition.y;
    const duration = 1000;
    const steps = 30;
    let step = 0;

    const interval = setInterval(() => {
      step++;
      const progress = step / steps;
      const newX = startX + (targetX - startX) * progress;
      const newY = startY + (targetY - startY) * progress;
      setMakiPosition({ x: newX, y: newY });

      if (step >= steps) {
        clearInterval(interval);
        setIsAnimating(false);
      }
    }, duration / steps);
  };

  const handleVillagePress = (villageId: string) => {
    const village = villages.find(v => v.id === villageId);
    if (!village || !village.unlocked || isAnimating) return;

    // Animer le maki vers le village
    animateMakiTo(village.x, village.y);

    // Attendre la fin de l'animation avant d'afficher le quiz
    setTimeout(() => {
      setSelectedVillage(village);
      setCurrentQuestionIndex(0);
      setScore(0);
      setShowQuiz(true);
      setSelectedAnswer(null);
      setShowFeedback(false);
    }, 1000);
  };

  const handleAnswerSelect = (answerIndex: number) => {
    if (showFeedback || !selectedVillage) return;

    const currentQuestion = selectedVillage.quiz[currentQuestionIndex];
    const correct = answerIndex === currentQuestion.correct;

    setSelectedAnswer(answerIndex);
    setIsCorrect(correct);
    setShowFeedback(true);

    if (correct) {
      setScore(score + 10);
    }

    // Passer à la question suivante après 2 secondes
    setTimeout(() => {
      if (currentQuestionIndex < selectedVillage.quiz.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        setSelectedAnswer(null);
        setShowFeedback(false);
      } else {
        // Quiz terminé
        completeVillage();
      }
    }, 2000);
  };

  const completeVillage = () => {
    if (!selectedVillage) return;

    const updatedVillages = villages.map(v => {
      if (v.id === selectedVillage.id) {
        return { ...v, completed: true };
      }
      // Débloquer le prochain village
      const currentIndex = villages.findIndex(vil => vil.id === selectedVillage.id);
      const nextVillage = villages[currentIndex + 1];
      if (nextVillage && v.id === nextVillage.id) {
        return { ...v, unlocked: true };
      }
      return v;
    });

    const newTotalScore = totalScore + score;
    setVillages(updatedVillages);
    setTotalScore(newTotalScore);
    saveProgress(updatedVillages, newTotalScore);

    setTimeout(() => {
      setShowQuiz(false);
      setSelectedVillage(null);
    }, 2500);
  };

  const resetProgress = async () => {
    const resetVillages = MAYOTTE_VILLAGES.map((v, index) => ({
      ...v,
      unlocked: index === 0,
      completed: false,
    }));
    setVillages(resetVillages);
    setTotalScore(0);
    setMakiPosition({ x: 55, y: 50 });
    await saveProgress(resetVillages, 0);
  };

  const renderMap = () => {
    return (
      <View style={styles.mapContainer}>
        <Svg width="100%" height="100%" viewBox="0 0 100 100">
          {/* Forme simplifiée de Mayotte */}
          <Path
            d="M 40,20 Q 50,15 60,20 L 65,30 Q 70,40 65,50 L 60,65 Q 55,75 45,77 L 35,75 Q 25,70 22,60 L 20,50 Q 18,40 20,30 L 25,22 Q 30,18 40,20 Z"
            fill="#4CAF50"
            stroke="#2E7D32"
            strokeWidth="0.5"
          />
          
          {/* Petite-Terre */}
          <Path
            d="M 85,60 Q 88,58 91,60 L 93,65 Q 93,70 91,72 L 88,73 Q 85,73 83,72 L 81,67 Q 81,62 83,60 L 85,60 Z"
            fill="#66BB6A"
            stroke="#388E3C"
            strokeWidth="0.3"
          />

          {/* Villages */}
          {villages.map((village) => {
            let fillColor = '#9E9E9E';
            if (village.completed) {
              fillColor = '#FFD700';
            } else if (village.unlocked) {
              fillColor = '#FF5722';
            }

            return (
              <G key={village.id}>
                <Circle
                  cx={village.x}
                  cy={village.y}
                  r="3"
                  fill={fillColor}
                  stroke="#fff"
                  strokeWidth="0.5"
                  onPress={() => handleVillagePress(village.id)}
                />
                {!village.unlocked && (
                  <SvgText
                    x={village.x}
                    y={village.y + 1.5}
                    fontSize="3"
                    fill="#fff"
                    textAnchor="middle"
                  >
                    🔒
                  </SvgText>
                )}
                {village.completed && (
                  <SvgText
                    x={village.x}
                    y={village.y + 1.5}
                    fontSize="3"
                    fill="#fff"
                    textAnchor="middle"
                  >
                    ✓
                  </SvgText>
                )}
              </G>
            );
          })}

          {/* Maki */}
          <G>
            <Circle cx={makiPosition.x} cy={makiPosition.y} r="2.5" fill="#8D6E63" stroke="#5D4037" strokeWidth="0.3" />
            <Circle cx={makiPosition.x - 0.8} cy={makiPosition.y - 0.5} r="0.5" fill="#000" />
            <Circle cx={makiPosition.x + 0.8} cy={makiPosition.y - 0.5} r="0.5" fill="#000" />
          </G>
        </Svg>
      </View>
    );
  };

  const renderQuiz = () => {
    if (!selectedVillage) return null;

    const currentQuestion = selectedVillage.quiz[currentQuestionIndex];

    return (
      <Modal visible={showQuiz} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.quizContainer}>
            <LinearGradient colors={['#2E7D32', '#4CAF50']} style={styles.quizHeader}>
              <Text style={styles.quizVillageName}>{selectedVillage.name}</Text>
              <Text style={styles.quizVillageNameLocal}>
                {selectedVillage.nameShimaore} / {selectedVillage.nameKibouchi}
              </Text>
              <Text style={styles.quizProgress}>
                Question {currentQuestionIndex + 1}/{selectedVillage.quiz.length}
              </Text>
            </LinearGradient>

            <ScrollView style={styles.quizContent}>
              <Text style={styles.questionText}>{currentQuestion.question}</Text>

              {currentQuestion.options.map((option, index) => {
                let backgroundColor = '#FFFFFF';
                if (showFeedback) {
                  if (index === currentQuestion.correct) {
                    backgroundColor = '#C8E6C9';
                  } else if (index === selectedAnswer && !isCorrect) {
                    backgroundColor = '#FFCDD2';
                  }
                }

                return (
                  <TouchableOpacity
                    key={index}
                    style={[styles.optionButton, { backgroundColor }]}
                    onPress={() => handleAnswerSelect(index)}
                    disabled={showFeedback}
                  >
                    <Text style={styles.optionText}>{option}</Text>
                    {showFeedback && index === currentQuestion.correct && (
                      <Ionicons name="checkmark-circle" size={24} color="#4CAF50" />
                    )}
                    {showFeedback && index === selectedAnswer && !isCorrect && (
                      <Ionicons name="close-circle" size={24} color="#F44336" />
                    )}
                  </TouchableOpacity>
                );
              })}

              {showFeedback && (
                <View style={[styles.feedback, isCorrect ? styles.feedbackCorrect : styles.feedbackIncorrect]}>
                  <Ionicons
                    name={isCorrect ? 'happy' : 'sad'}
                    size={32}
                    color={isCorrect ? '#4CAF50' : '#F44336'}
                  />
                  <Text style={styles.feedbackText}>
                    {isCorrect ? 'Bravo! 🎉' : 'Essaie encore! 💪'}
                  </Text>
                  <Text style={styles.explanationText}>{currentQuestion.explanation}</Text>
                </View>
              )}

              {currentQuestionIndex === selectedVillage.quiz.length - 1 && showFeedback && (
                <View style={styles.scoreContainer}>
                  <Text style={styles.scoreText}>Score: {score} / {selectedVillage.quiz.length * 10}</Text>
                  <Text style={styles.completionText}>Village complété! ✨</Text>
                </View>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>
    );
  };

  const completedCount = villages.filter(v => v.completed).length;
  const unlockedCount = villages.filter(v => v.unlocked).length;

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
            <Text style={styles.headerSubtitle}>🐒 Explore avec le maki!</Text>
          </View>

          <TouchableOpacity onPress={resetProgress} style={styles.resetButton}>
            <Ionicons name="refresh" size={20} color="#FFFFFF" />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content}>
        {/* Statistiques */}
        <View style={styles.statsContainer}>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{completedCount}/10</Text>
            <Text style={styles.statLabel}>Villages</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{totalScore}</Text>
            <Text style={styles.statLabel}>Points</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{unlockedCount}/10</Text>
            <Text style={styles.statLabel}>Débloqués</Text>
          </View>
        </View>

        {/* Instructions */}
        <View style={styles.instructionsContainer}>
          <Ionicons name="information-circle" size={20} color="#4CAF50" />
          <Text style={styles.instructionsText}>
            Clique sur les villages débloqués pour découvrir Mayotte et apprendre le Shimaoré et le Kibouchi!
          </Text>
        </View>

        {/* Carte */}
        {renderMap()}

        {/* Légende */}
        <View style={styles.legendContainer}>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#FF5722' }]} />
            <Text style={styles.legendText}>Débloqué</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#FFD700' }]} />
            <Text style={styles.legendText}>Complété</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#9E9E9E' }]} />
            <Text style={styles.legendText}>Verrouillé</Text>
          </View>
        </View>

        {/* Liste des villages */}
        <View style={styles.villageListContainer}>
          <Text style={styles.villageListTitle}>Les 10 villages à découvrir:</Text>
          {villages.map((village, index) => (
            <TouchableOpacity
              key={village.id}
              style={[
                styles.villageListItem,
                !village.unlocked && styles.villageListItemLocked,
                village.completed && styles.villageListItemCompleted,
              ]}
              onPress={() => handleVillagePress(village.id)}
              disabled={!village.unlocked}
            >
              <View style={styles.villageListNumber}>
                <Text style={styles.villageListNumberText}>{index + 1}</Text>
              </View>
              <View style={styles.villageListInfo}>
                <Text style={styles.villageListName}>{village.name}</Text>
                <Text style={styles.villageListLocal}>
                  {village.nameShimaore} / {village.nameKibouchi}
                </Text>
                <Text style={styles.villageListDesc}>{village.description}</Text>
              </View>
              <View style={styles.villageListStatus}>
                {village.completed && <Ionicons name="checkmark-circle" size={24} color="#FFD700" />}
                {village.unlocked && !village.completed && <Ionicons name="play-circle" size={24} color="#FF5722" />}
                {!village.unlocked && <Ionicons name="lock-closed" size={24} color="#9E9E9E" />}
              </View>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      {renderQuiz()}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8F5E9',
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
  resetButton: {
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
  content: {
    flex: 1,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
  },
  statBox: {
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    minWidth: 80,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  instructionsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#C8E6C9',
    padding: 12,
    marginHorizontal: 20,
    marginBottom: 15,
    borderRadius: 10,
    gap: 10,
  },
  instructionsText: {
    flex: 1,
    fontSize: 13,
    color: '#2E7D32',
  },
  mapContainer: {
    height: 300,
    backgroundColor: '#81D4FA',
    marginHorizontal: 20,
    borderRadius: 15,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  legendContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 15,
    marginHorizontal: 20,
    marginTop: 15,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: '#FFFFFF',
  },
  legendText: {
    fontSize: 12,
    color: '#666',
  },
  villageListContainer: {
    padding: 20,
  },
  villageListTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 15,
  },
  villageListItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    gap: 12,
  },
  villageListItemLocked: {
    opacity: 0.6,
  },
  villageListItemCompleted: {
    backgroundColor: '#FFF9C4',
  },
  villageListNumber: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
  },
  villageListNumberText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 14,
  },
  villageListInfo: {
    flex: 1,
  },
  villageListName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  villageListLocal: {
    fontSize: 12,
    color: '#4CAF50',
    marginTop: 2,
  },
  villageListDesc: {
    fontSize: 11,
    color: '#666',
    marginTop: 4,
  },
  villageListStatus: {
    marginLeft: 10,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'flex-end',
  },
  quizContainer: {
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 25,
    borderTopRightRadius: 25,
    maxHeight: '85%',
    overflow: 'hidden',
  },
  quizHeader: {
    padding: 20,
    alignItems: 'center',
  },
  quizVillageName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  quizVillageNameLocal: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    marginTop: 4,
  },
  quizProgress: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.8,
    marginTop: 8,
  },
  quizContent: {
    padding: 20,
  },
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 20,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 15,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 2,
    borderColor: '#E0E0E0',
  },
  optionText: {
    fontSize: 16,
    color: '#333',
    flex: 1,
  },
  feedback: {
    alignItems: 'center',
    padding: 20,
    borderRadius: 12,
    marginTop: 10,
    gap: 10,
  },
  feedbackCorrect: {
    backgroundColor: '#C8E6C9',
  },
  feedbackIncorrect: {
    backgroundColor: '#FFCDD2',
  },
  feedbackText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  explanationText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  scoreContainer: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#FFF9C4',
    borderRadius: 12,
    marginTop: 20,
  },
  scoreText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#F57C00',
  },
  completionText: {
    fontSize: 16,
    color: '#4CAF50',
    marginTop: 10,
  },
});

export default MayotteDiscoveryGame;