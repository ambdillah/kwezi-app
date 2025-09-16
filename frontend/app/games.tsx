import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as Speech from 'expo-speech';

const { width } = Dimensions.get('window');

interface Word {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  difficulty?: number;
  image_url?: string;
}

interface GameCard {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  difficulty: number;
}

const GAMES: GameCard[] = [
  {
    id: 'match-words',
    title: 'Associer les mots',
    description: 'Trouve la bonne traduction avec les makis! 🐒',
    icon: 'link',
    color: '#FF6B6B',
    difficulty: 1,
  },
  {
    id: 'memory-game',
    title: 'Mémoire des fleurs',
    description: 'Retourne les cartes ylang-ylang 🌺',
    icon: 'flower',
    color: '#4ECDC4',
    difficulty: 2,
  },
  {
    id: 'quiz-time',
    title: 'Quiz Mayotte',
    description: 'Réponds aux questions sur les langues',
    icon: 'help-circle',
    color: '#45B7D1',
    difficulty: 2,
  },
  {
    id: 'build-sentence',
    title: 'Construire des phrases',
    description: 'Assemble les mots pour faire des phrases',
    icon: 'text',
    color: '#96CEB4',
    difficulty: 3,
  },
];

export default function GamesScreen() {
  const [words, setWords] = useState<Word[]>([]);
  const [currentGame, setCurrentGame] = useState<string | null>(null);
  const [gameWords, setGameWords] = useState<Word[]>([]);
  const [selectedWords, setSelectedWords] = useState<string[]>([]);
  const [score, setScore] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);

  useEffect(() => {
    fetchWords();
  }, []);

  const fetchWords = async () => {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`);
      if (response.ok) {
        const data = await response.json();
        setWords(data);
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger les mots');
    }
  };

  const startGame = (gameId: string) => {
    const shuffled = [...words].sort(() => Math.random() - 0.5).slice(0, 6);
    setGameWords(shuffled);
    setCurrentGame(gameId);
    setGameStarted(true);
    setScore(0);
    setSelectedWords([]);
    
    Speech.speak("C'est parti pour le jeu! Bonne chance!", {
      language: 'fr-FR',
      pitch: 1.2,
    });
  };

  // États pour le nouveau jeu de traduction
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState<any>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [questionsGenerated, setQuestionsGenerated] = useState<any[]>([]);

  // Générer une question de traduction
  const generateQuestion = (words: Word[], questionIndex: number) => {
    if (questionIndex >= words.length) return null;
    
    const currentWord = words[questionIndex];
    const otherWords = words.filter(w => w.id !== currentWord.id);
    
    // Choisir aléatoirement entre shimaoré et kibouchi
    const languages = ['shimaore', 'kibouchi'] as const;
    const selectedLanguage = languages[Math.floor(Math.random() * languages.length)];
    
    // Obtenir la bonne traduction
    const correctTranslation = currentWord[selectedLanguage];
    
    // Choisir une mauvaise traduction d'un autre mot dans la même langue
    const wrongWord = otherWords[Math.floor(Math.random() * otherWords.length)];
    const wrongTranslation = wrongWord[selectedLanguage];
    
    // Mélanger les positions
    const options = [
      { text: correctTranslation, isCorrect: true },
      { text: wrongTranslation, isCorrect: false }
    ];
    
    // Mélanger l'ordre des options
    const shuffledOptions = Math.random() > 0.5 ? options : [options[1], options[0]];
    
    return {
      french: currentWord.french,
      language: selectedLanguage,
      languageLabel: selectedLanguage === 'shimaore' ? 'Shimaoré' : 'Kibouchi',
      options: shuffledOptions,
      correctAnswer: correctTranslation
    };
  };

  // Générer toutes les questions au début du jeu
  const generateAllQuestions = (words: Word[]) => {
    const questions = [];
    const shuffledWords = [...words].sort(() => Math.random() - 0.5);
    
    for (let i = 0; i < Math.min(10, shuffledWords.length); i++) {
      const question = generateQuestion(shuffledWords, i);
      if (question) questions.push(question);
    }
    
    setQuestionsGenerated(questions);
    setCurrentQuestion(questions[0]);
    setCurrentQuestionIndex(0);
  };

  const checkAnswer = (selectedOption: any) => {
    setSelectedAnswer(selectedOption.text);
    setIsCorrect(selectedOption.isCorrect);
    setShowResult(true);
    
    if (selectedOption.isCorrect) {
      setScore(prev => prev + 10);
      Speech.speak('Bravo! Très bien!', { language: 'fr-FR', pitch: 1.3 });
    } else {
      Speech.speak('Oups! Ce n\'est pas la bonne réponse.', { language: 'fr-FR' });
    }
    
    // Passer à la question suivante après 2 secondes
    setTimeout(() => {
      nextQuestion();
    }, 2000);
  };

  const nextQuestion = () => {
    setShowResult(false);
    setSelectedAnswer(null);
    
    if (currentQuestionIndex + 1 < questionsGenerated.length) {
      const nextIndex = currentQuestionIndex + 1;
      setCurrentQuestionIndex(nextIndex);
      setCurrentQuestion(questionsGenerated[nextIndex]);
    } else {
      // Fin du jeu
      setTimeout(() => {
        Speech.speak(`Félicitations! Tu as terminé avec ${score} points!`, { 
          language: 'fr-FR', 
          pitch: 1.2 
        });
        Alert.alert('🎉 Jeu terminé!', `Tu as obtenu ${score} points sur ${questionsGenerated.length * 10} possibles!`);
        setGameStarted(false);
      }, 500);
    }
  };

  const renderMatchGame = () => (
    <View style={styles.gameContainer}>
      <View style={styles.gameHeader}>
        <Text style={styles.gameTitle}>Associer les mots 🐒</Text>
        <Text style={styles.scoreText}>Score: {score}</Text>
      </View>
      
      <ScrollView style={styles.gameContent}>
        {gameWords.map((word) => (
          <View key={word.id} style={styles.matchCard}>
            <TouchableOpacity 
              style={styles.frenchCard}
              onPress={() => Speech.speak(word.french, { language: 'fr-FR' })}
            >
              <Text style={styles.frenchText}>{word.french}</Text>
              <Ionicons name="volume-high" size={20} color="#4ECDC4" />
            </TouchableOpacity>
            
            <View style={styles.optionsContainer}>
              <TouchableOpacity 
                style={styles.optionButton}
                onPress={() => checkMatch(word.french, word.shimaore, 'shimaore')}
              >
                <Text style={styles.optionText}>Shimaoré: {word.shimaore}</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.optionButton}
                onPress={() => checkMatch(word.french, word.kibouchi, 'kibouchi')}
              >
                <Text style={styles.optionText}>Kibouchi: {word.kibouchi}</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );

  const renderMemoryGame = () => (
    <View style={styles.gameContainer}>
      <Text style={styles.gameTitle}>Jeu de mémoire 🌺</Text>
      <Text style={styles.comingSoon}>Bientôt disponible! En cours de développement...</Text>
    </View>
  );

  const renderQuizGame = () => (
    <View style={styles.gameContainer}>
      <Text style={styles.gameTitle}>Quiz Mayotte 🏝️</Text>
      <Text style={styles.comingSoon}>Bientôt disponible! En cours de développement...</Text>
    </View>
  );

  const renderBuildSentenceGame = () => (
    <View style={styles.gameContainer}>
      <Text style={styles.gameTitle}>Construire des phrases 📝</Text>
      <Text style={styles.comingSoon}>Bientôt disponible! En cours de développement...</Text>
    </View>
  );

  const renderGame = () => {
    switch (currentGame) {
      case 'match-words':
        return renderMatchGame();
      case 'memory-game':
        return renderMemoryGame();
      case 'quiz-time':
        return renderQuizGame();
      case 'build-sentence':
        return renderBuildSentenceGame();
      default:
        return null;
    }
  };

  if (gameStarted && currentGame) {
    return (
      <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.header}>
            <TouchableOpacity 
              onPress={() => {
                setGameStarted(false);
                setCurrentGame(null);
              }} 
              style={styles.backButton}
            >
              <Ionicons name="arrow-back" size={24} color="#000" />
            </TouchableOpacity>
            <Text style={styles.title}>Jeux</Text>
            <TouchableOpacity 
              onPress={() => startGame(currentGame)}
              style={styles.refreshButton}
            >
              <Ionicons name="refresh" size={24} color="#000" />
            </TouchableOpacity>
          </View>
          {renderGame()}
        </SafeAreaView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <Text style={styles.title}>Jeux 🎮</Text>
          <View style={styles.placeholder} />
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          <Text style={styles.sectionTitle}>Choisir un jeu amusant! 🌺</Text>
          
          {GAMES.map((game) => (
            <TouchableOpacity
              key={game.id}
              style={[styles.gameCard, { backgroundColor: game.color }]}
              onPress={() => startGame(game.id)}
            >
              <View style={styles.gameCardContent}>
                <View style={styles.gameInfo}>
                  <Text style={styles.gameCardTitle}>{game.title}</Text>
                  <Text style={styles.gameCardDescription}>{game.description}</Text>
                  
                  <View style={styles.difficultyContainer}>
                    <Text style={styles.difficultyText}>Difficulté: </Text>
                    {[...Array(game.difficulty)].map((_, i) => (
                      <Ionicons key={i} name="star" size={16} color="#FFD700" />
                    ))}
                  </View>
                </View>
                
                <View style={styles.gameIcon}>
                  <Ionicons name={game.icon as any} size={40} color="#fff" />
                </View>
              </View>
            </TouchableOpacity>
          ))}
          
          <View style={styles.encouragementContainer}>
            <Text style={styles.encouragementText}>
              🐒 Les makis de Mayotte t'encouragent! 🌺
            </Text>
            <Text style={styles.encouragementSubtext}>
              Apprends en t'amusant avec le Shimaoré et le Kibouchi
            </Text>
          </View>
        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 15,
  },
  backButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 20,
    padding: 8,
  },
  refreshButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 20,
    padding: 8,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  placeholder: {
    width: 40,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 20,
    textAlign: 'center',
  },
  gameCard: {
    borderRadius: 15,
    marginBottom: 15,
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  gameCardContent: {
    flexDirection: 'row',
    padding: 20,
    alignItems: 'center',
  },
  gameInfo: {
    flex: 1,
  },
  gameCardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  gameCardDescription: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
    marginBottom: 10,
  },
  difficultyContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  difficultyText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  gameIcon: {
    marginLeft: 20,
  },
  encouragementContainer: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    marginTop: 20,
    marginBottom: 30,
  },
  encouragementText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 8,
  },
  encouragementSubtext: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  // Game specific styles
  gameContainer: {
    flex: 1,
    padding: 20,
  },
  gameHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  gameTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#000',
  },
  scoreText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
  },
  gameContent: {
    flex: 1,
  },
  matchCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
  },
  frenchCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#4ECDC4',
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
  },
  frenchText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  optionsContainer: {
    gap: 10,
  },
  optionButton: {
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    padding: 15,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  optionText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    textAlign: 'center',
  },
  comingSoon: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    padding: 20,
    borderRadius: 15,
    marginTop: 50,
  },
});