import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Modal,
  ScrollView,
  TouchableOpacity,
  Dimensions,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { BlurView } from 'expo-blur';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { Village } from '../utils/mayotteGameEngine';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

interface VillageDiscoveryPanelProps {
  village: Village | null;
  isVisible: boolean;
  onClose: () => void;
  onQuizComplete?: (success: boolean) => void;
}

const VillageDiscoveryPanel: React.FC<VillageDiscoveryPanelProps> = ({
  village,
  isVisible,
  onClose,
  onQuizComplete,
}) => {
  const [showQuiz, setShowQuiz] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [quizResult, setQuizResult] = useState<boolean | null>(null);

  // Animations
  const scale = useSharedValue(0);
  const opacity = useSharedValue(0);

  React.useEffect(() => {
    if (isVisible && village) {
      opacity.value = withTiming(1, { duration: 300 });
      scale.value = withSpring(1, { damping: 15, stiffness: 150 });
      setShowQuiz(false);
      setQuizCompleted(false);
      setQuizResult(null);
      setSelectedAnswer(null);
    } else {
      opacity.value = withTiming(0, { duration: 200 });
      scale.value = withTiming(0, { duration: 200 });
    }
  }, [isVisible, village]);

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ scale: scale.value }],
      opacity: opacity.value,
    };
  });

  const handleQuizStart = () => {
    setShowQuiz(true);
  };

  const handleQuizSubmit = () => {
    if (selectedAnswer === null) {
      Alert.alert('Attention', 'Veuillez sélectionner une réponse !');
      return;
    }

    const isCorrect = selectedAnswer === village?.meta.quiz?.correct;
    setQuizResult(isCorrect);
    setQuizCompleted(true);
    
    if (onQuizComplete) {
      onQuizComplete(isCorrect);
    }
  };

  const getLanguageFlag = (langue: string) => {
    switch (langue) {
      case 'shimaoré':
        return '🇰🇲'; // Comores flag pour shimaoré
      case 'kibouchi':
        return '🏝️'; // Île pour kibouchi
      default:
        return '🇫🇷'; // Français
    }
  };

  if (!village) return null;

  return (
    <Modal
      visible={isVisible}
      transparent
      animationType="none"
      onRequestClose={onClose}
    >
      <BlurView intensity={50} style={styles.modalOverlay}>
        <Animated.View style={[styles.panelContainer, animatedStyle]}>
          <LinearGradient
            colors={['#E8F5E8', '#F1F8E9', '#E8F5E8']}
            style={styles.panel}
          >
            {/* Header */}
            <View style={styles.header}>
              <View style={styles.headerLeft}>
                <Text style={styles.villageType}>
                  {village.type === 'prefecture' ? '🏛️' : '🏘️'} 
                  {village.type === 'prefecture' ? 'Préfecture' : 'Commune'}
                </Text>
                <Text style={styles.villageName}>{village.name}</Text>
              </View>
              <TouchableOpacity onPress={onClose} style={styles.closeButton}>
                <Ionicons name="close" size={24} color="#2E7D32" />
              </TouchableOpacity>
            </View>

            <ScrollView showsVerticalScrollIndicator={false} style={styles.content}>
              {/* Informations générales */}
              <View style={styles.section}>
                <View style={styles.sectionHeader}>
                  <Ionicons name="information-circle" size={20} color="#4CAF50" />
                  <Text style={styles.sectionTitle}>Informations</Text>
                </View>
                
                <View style={styles.infoCard}>
                  <Text style={styles.specialite}>🌟 {village.meta.specialite}</Text>
                  <Text style={styles.description}>{village.meta.description}</Text>
                  
                  {village.meta.population && (
                    <View style={styles.statRow}>
                      <Ionicons name="people" size={16} color="#666" />
                      <Text style={styles.statText}>
                        {village.meta.population.toLocaleString()} habitants
                      </Text>
                    </View>
                  )}
                  
                  {village.meta.langue_locale && (
                    <View style={styles.statRow}>
                      <Text style={styles.flag}>
                        {getLanguageFlag(village.meta.langue_locale)}
                      </Text>
                      <Text style={styles.statText}>
                        Langue locale: {village.meta.langue_locale}
                      </Text>
                    </View>
                  )}
                </View>
              </View>

              {/* Histoire */}
              {village.meta.histoire && (
                <View style={styles.section}>
                  <View style={styles.sectionHeader}>
                    <Ionicons name="book" size={20} color="#4CAF50" />
                    <Text style={styles.sectionTitle}>Histoire</Text>
                  </View>
                  <View style={styles.infoCard}>
                    <Text style={styles.historyText}>{village.meta.histoire}</Text>
                  </View>
                </View>
              )}

              {/* Quiz Section */}
              {village.meta.quiz && (
                <View style={styles.section}>
                  <View style={styles.sectionHeader}>
                    <Ionicons name="help-circle" size={20} color="#4CAF50" />
                    <Text style={styles.sectionTitle}>Quiz Découverte</Text>
                  </View>
                  
                  {!showQuiz ? (
                    <TouchableOpacity
                      style={styles.quizStartButton}
                      onPress={handleQuizStart}
                    >
                      <Ionicons name="play-circle" size={24} color="#FFFFFF" />
                      <Text style={styles.quizStartText}>
                        Tester mes connaissances
                      </Text>
                    </TouchableOpacity>
                  ) : (
                    <View style={styles.quizContainer}>
                      <Text style={styles.quizQuestion}>
                        {village.meta.quiz.question}
                      </Text>
                      
                      {village.meta.quiz.options.map((option, index) => (
                        <TouchableOpacity
                          key={index}
                          style={[
                            styles.quizOption,
                            selectedAnswer === index && styles.selectedOption,
                            quizCompleted && index === village.meta.quiz?.correct && styles.correctOption,
                            quizCompleted && selectedAnswer === index && index !== village.meta.quiz?.correct && styles.incorrectOption,
                          ]}
                          onPress={() => !quizCompleted && setSelectedAnswer(index)}
                          disabled={quizCompleted}
                        >
                          <Text style={[
                            styles.optionText,
                            selectedAnswer === index && styles.selectedOptionText,
                          ]}>
                            {String.fromCharCode(65 + index)}. {option}
                          </Text>
                          
                          {quizCompleted && index === village.meta.quiz?.correct && (
                            <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                          )}
                          {quizCompleted && selectedAnswer === index && index !== village.meta.quiz?.correct && (
                            <Ionicons name="close-circle" size={20} color="#F44336" />
                          )}
                        </TouchableOpacity>
                      ))}
                      
                      {!quizCompleted ? (
                        <TouchableOpacity
                          style={[
                            styles.quizSubmitButton,
                            selectedAnswer === null && styles.disabledButton,
                          ]}
                          onPress={handleQuizSubmit}
                          disabled={selectedAnswer === null}
                        >
                          <Text style={styles.quizSubmitText}>Valider</Text>
                        </TouchableOpacity>
                      ) : (
                        <View style={styles.quizResultContainer}>
                          <Ionicons
                            name={quizResult ? "trophy" : "ribbon"}
                            size={32}
                            color={quizResult ? "#FFD700" : "#FFA726"}
                          />
                          <Text style={styles.quizResultText}>
                            {quizResult 
                              ? "Bravo ! Excellente réponse !" 
                              : "Pas mal ! Continuez à explorer pour apprendre !"
                            }
                          </Text>
                          <Text style={styles.pointsText}>
                            +{quizResult ? 20 : 5} points
                          </Text>
                        </View>
                      )}
                    </View>
                  )}
                </View>
              )}
            </ScrollView>

            {/* Footer Actions */}
            <View style={styles.footer}>
              <TouchableOpacity style={styles.exploreButton} onPress={onClose}>
                <Ionicons name="map" size={20} color="#FFFFFF" />
                <Text style={styles.exploreButtonText}>Continuer l'exploration</Text>
              </TouchableOpacity>
            </View>
          </LinearGradient>
        </Animated.View>
      </BlurView>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.4)',
  },
  panelContainer: {
    width: screenWidth * 0.9,
    maxHeight: screenHeight * 0.85,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.25,
    shadowRadius: 20,
    elevation: 10,
  },
  panel: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    padding: 20,
    paddingBottom: 15,
  },
  headerLeft: {
    flex: 1,
  },
  villageType: {
    fontSize: 14,
    color: '#4CAF50',
    fontWeight: '600',
    marginBottom: 4,
  },
  villageName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  closeButton: {
    padding: 8,
    borderRadius: 20,
    backgroundColor: 'rgba(46, 125, 50, 0.1)',
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  section: {
    marginBottom: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginLeft: 8,
  },
  infoCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  specialite: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FF6B35',
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
    marginBottom: 12,
  },
  statRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  statText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
  },
  flag: {
    fontSize: 16,
  },
  historyText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
    fontStyle: 'italic',
  },
  quizStartButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#4CAF50',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  quizStartText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  quizContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  quizQuestion: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 16,
    textAlign: 'center',
  },
  quizOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  selectedOption: {
    backgroundColor: '#E8F5E8',
    borderColor: '#4CAF50',
  },
  correctOption: {
    backgroundColor: '#E8F5E8',
    borderColor: '#4CAF50',
  },
  incorrectOption: {
    backgroundColor: '#FFEBEE',
    borderColor: '#F44336',
  },
  optionText: {
    fontSize: 14,
    color: '#333',
    flex: 1,
  },
  selectedOptionText: {
    color: '#2E7D32',
    fontWeight: '600',
  },
  quizSubmitButton: {
    backgroundColor: '#4CAF50',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
    marginTop: 8,
  },
  disabledButton: {
    backgroundColor: '#CCCCCC',
  },
  quizSubmitText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  quizResultContainer: {
    alignItems: 'center',
    padding: 16,
    marginTop: 8,
  },
  quizResultText: {
    fontSize: 16,
    color: '#2E7D32',
    textAlign: 'center',
    marginTop: 8,
    marginBottom: 4,
  },
  pointsText: {
    fontSize: 14,
    color: '#FF6B35',
    fontWeight: 'bold',
  },
  footer: {
    padding: 20,
    paddingTop: 0,
  },
  exploreButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#2E7D32',
    borderRadius: 12,
    padding: 16,
  },
  exploreButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});

export default VillageDiscoveryPanel;