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
import { speakText, speakEducationalContent } from '../utils/feminineSpeechUtils';
import YlangYlangFlower from '../components/YlangYlangFlower';
import MakiMayotte from '../components/MakiMayotte';
import ColoredConjugationWord from '../components/ColoredConjugationWord';
import ConjugationColorLegend from '../components/ConjugationColorLegend';

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

interface Sentence {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  tense: string;
  difficulty: number;
  shimaore_words: string[];
  kibouchi_words: string[];
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
    description: 'Remets les mots dans le bon ordre! 📝',
    icon: 'construct',
    color: '#96CEB4',
    difficulty: 2,
  },
  {
    id: 'mayotte-discovery',
    title: 'Découverte de Mayotte',
    description: 'Explore l\'île avec le maki aventurier! 🗺️',
    icon: 'map',
    color: '#F39C12',
    difficulty: 1,
  },
];

export default function GamesScreen() {
  const [words, setWords] = useState<Word[]>([]);
  const [currentGame, setCurrentGame] = useState<string | null>(null);
  const [gameWords, setGameWords] = useState<Word[]>([]);
  const [selectedWords, setSelectedWords] = useState<string[]>([]);
  const [score, setScore] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  
  // États pour le jeu de construction de phrases
  const [sentences, setSentences] = useState<Sentence[]>([]);
  const [currentSentence, setCurrentSentence] = useState<Sentence | null>(null);
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState<'shimaore' | 'kibouchi'>('shimaore');
  const [availableWords, setAvailableWords] = useState<string[]>([]);
  const [builtSentence, setBuiltSentence] = useState<string[]>([]);
  const [sentenceScore, setSentenceScore] = useState(0);
  const [showSentenceFeedback, setShowSentenceFeedback] = useState(false);
  const [sentenceFeedbackType, setSentenceFeedbackType] = useState<'success' | 'error'>('success');

  const speakTextLocal = async (text: string, lang: 'shimaore' | 'kibouchi') => {
    // Utiliser le système de voix féminine
    await speakText(text, lang);
  };
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

  const fetchSentences = async (difficulty: number = 1) => {
    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/sentences?difficulty=${difficulty}&limit=5`
      );
      if (response.ok) {
        const data = await response.json();
        setSentences(data);
        if (data.length > 0) {
          setCurrentSentence(data[0]);
          setCurrentSentenceIndex(0);
          // Mélanger les mots de la phrase pour le jeu
          const wordsToShuffle = selectedLanguage === 'shimaore' 
            ? data[0].shimaore_words 
            : data[0].kibouchi_words;
          setAvailableWords([...wordsToShuffle].sort(() => Math.random() - 0.5));
          setBuiltSentence([]);
        }
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger les phrases');
    }
  };

  const startGame = (gameId: string) => {
    // Navigation spéciale pour le jeu de découverte de Mayotte
    if (gameId === 'mayotte-discovery') {
      router.push('/mayotte-discovery');
      return;
    }
    
    setCurrentGame(gameId);
    setGameStarted(true);
    setScore(0);
    setSelectedWords([]);
    
    if (gameId === 'build-sentence') {
      // Pour le jeu de construction de phrases
      setSentenceScore(0);
      setCurrentSentenceIndex(0);
      setBuiltSentence([]);
      fetchSentences(1); // Commencer par difficulté 1
    } else {
      // Pour les autres jeux
      const shuffled = [...words].sort(() => Math.random() - 0.5).slice(0, 6);
      setGameWords(shuffled);
      
      if (gameId === 'match-words') {
        generateAllQuestions(shuffled);
      }
    }
    
    // Utiliser la voix féminine pour l'encouragement
    speakEducationalContent("C'est parti pour le jeu! Bonne chance!", 'fr');
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
    // S'assurer que la mauvaise traduction est vraiment différente de la bonne
    let wrongTranslation = '';
    let attempts = 0;
    const maxAttempts = 10;
    
    do {
      const wrongWord = otherWords[Math.floor(Math.random() * otherWords.length)];
      wrongTranslation = wrongWord[selectedLanguage];
      attempts++;
    } while (
      wrongTranslation === correctTranslation && 
      attempts < maxAttempts
    );
    
    // Si après plusieurs tentatives on n'a pas trouvé de traduction différente,
    // essayer avec l'autre langue pour créer une fausse option évidente
    if (wrongTranslation === correctTranslation) {
      const otherLanguage = selectedLanguage === 'shimaore' ? 'kibouchi' : 'shimaore';
      const randomWrongWord = otherWords[Math.floor(Math.random() * otherWords.length)];
      wrongTranslation = randomWrongWord[otherLanguage];
    }
    
    // Vérification finale : s'assurer qu'on a bien une traduction différente
    if (wrongTranslation === correctTranslation) {
      // En dernier recours, utiliser une traduction inventée évidente
      wrongTranslation = selectedLanguage === 'shimaore' ? 'Traduction inventée' : 'Fausse traduction';
    }
    
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
      speakEducationalContent('Bravo! Très bien!', 'fr');
    } else {
      speakEducationalContent('Oups! Ce n\'est pas la bonne réponse.', 'fr');
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
        speakEducationalContent(`Félicitations! Tu as terminé avec ${score} points!`, 'fr');
        Alert.alert('🎉 Jeu terminé!', `Tu as obtenu ${score} points sur ${questionsGenerated.length * 10} possibles!`);
        setGameStarted(false);
      }, 500);
    }
  };

  const renderMatchGame = () => {
    if (!currentQuestion) {
      return (
        <View style={styles.gameContainer}>
          <Text style={styles.gameTitle}>Chargement...</Text>
        </View>
      );
    }

    return (
      <View style={styles.gameContainer}>
        <View style={styles.gameHeader}>
          <Text style={styles.gameTitle}>Associer les mots 🐒</Text>
        </View>
        
        <View style={styles.gameProgressBar}>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Question</Text>
            <Text style={styles.progressValue}>
              {currentQuestionIndex + 1} / {questionsGenerated.length}
            </Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Score</Text>
            <Text style={styles.progressValue}>{score}</Text>
          </View>
        </View>
        
        <View style={styles.questionContainer}>
          
          <View style={styles.questionCard}>
            <TouchableOpacity 
              style={styles.frenchCard}
              onPress={() => speakEducationalContent(currentQuestion.french, 'fr')}
            >
              <Text style={styles.frenchText}>{currentQuestion.french}</Text>
              <Ionicons name="volume-high" size={20} color="#4ECDC4" />
            </TouchableOpacity>
            
            <Text style={styles.questionText}>
              Comment dit-on en {currentQuestion.languageLabel} ?
            </Text>
            
            <View style={styles.optionsContainer}>
              {currentQuestion.options.map((option: any, index: number) => (
                <TouchableOpacity 
                  key={index}
                  style={[
                    styles.optionButton,
                    showResult && option.isCorrect && styles.correctOption,
                    showResult && selectedAnswer === option.text && !option.isCorrect && styles.wrongOption,
                    showResult && styles.disabledOption
                  ]}
                  onPress={() => !showResult && checkAnswer(option)}
                  disabled={showResult}
                >
                  <Text style={[
                    styles.optionText,
                    showResult && option.isCorrect && styles.correctOptionText,
                    showResult && selectedAnswer === option.text && !option.isCorrect && styles.wrongOptionText
                  ]}>
                    {option.text}
                  </Text>
                  {showResult && option.isCorrect && (
                    <Ionicons name="checkmark-circle" size={24} color="#4CAF50" />
                  )}
                  {showResult && selectedAnswer === option.text && !option.isCorrect && (
                    <Ionicons name="close-circle" size={24} color="#F44336" />
                  )}
                </TouchableOpacity>
              ))}
            </View>
            
            {showResult && (
              <View style={styles.resultContainer}>
                <Text style={[
                  styles.resultText,
                  isCorrect ? styles.correctText : styles.wrongText
                ]}>
                  {isCorrect ? '🎉 Bravo!' : '❌ Oups!'}
                </Text>
                {!isCorrect && (
                  <Text style={styles.correctAnswerText}>
                    La bonne réponse était: {currentQuestion.correctAnswer}
                  </Text>
                )}
              </View>
            )}
          </View>
        </View>
      </View>
    );
  };

  // États pour le jeu de mémoire
  const [memoryCards, setMemoryCards] = useState<any[]>([]);
  const [flippedCards, setFlippedCards] = useState<number[]>([]);
  const [matchedPairs, setMatchedPairs] = useState<number[]>([]);
  const [canFlip, setCanFlip] = useState(true);
  const [memoryScore, setMemoryScore] = useState(0);
  const [moves, setMoves] = useState(0);

  // Créer les paires de cartes pour le jeu de mémoire
  const createMemoryCards = (words: Word[]) => {
    // Sélectionner 6 mots aléatoirement
    const selectedWords = words.sort(() => Math.random() - 0.5).slice(0, 6);
    
    const cards: any[] = [];
    
    selectedWords.forEach((word, index) => {
      // Choisir aléatoirement entre shimaoré et kibouchi
      const useShimaore = Math.random() > 0.5;
      const translation = useShimaore ? word.shimaore : word.kibouchi;
      const language = useShimaore ? 'shimaoré' : 'kibouchi';
      
      // Carte française
      cards.push({
        id: index * 2,
        text: word.french,
        type: 'french',
        pairId: index,
        word: word
      });
      
      // Carte traduction
      cards.push({
        id: index * 2 + 1,
        text: translation,
        type: 'translation',
        language: language,
        pairId: index,
        word: word
      });
    });
    
    // Mélanger les cartes
    return cards.sort(() => Math.random() - 0.5);
  };

  // Initialiser le jeu de mémoire
  const initMemoryGame = () => {
    const cards = createMemoryCards(words);
    setMemoryCards(cards);
    setFlippedCards([]);
    setMatchedPairs([]);
    setCanFlip(true);
    setMemoryScore(0);
    setMoves(0);
  };

  // Gérer le clic sur une carte
  const handleCardFlip = (cardId: number) => {
    if (!canFlip || flippedCards.includes(cardId) || matchedPairs.includes(cardId)) {
      return;
    }

    const newFlippedCards = [...flippedCards, cardId];
    setFlippedCards(newFlippedCards);

    if (newFlippedCards.length === 2) {
      setCanFlip(false);
      setMoves(prev => prev + 1);
      
      const [firstCardId, secondCardId] = newFlippedCards;
      const firstCard = memoryCards.find(card => card.id === firstCardId);
      const secondCard = memoryCards.find(card => card.id === secondCardId);
      
      // Vérifier si c'est une paire
      if (firstCard.pairId === secondCard.pairId) {
        // Paire trouvée !
        setTimeout(() => {
          setMatchedPairs(prev => [...prev, firstCardId, secondCardId]);
          setFlippedCards([]);
          setCanFlip(true);
          setMemoryScore(prev => prev + (moves === 0 ? 30 : 20));
          
          // Prononcer les deux mots avec voix féminine
          speakEducationalContent(`${firstCard.text}. ${secondCard.text}`, 'fr');
          
          // Vérifier si le jeu est terminé
          if (matchedPairs.length + 2 === memoryCards.length) {
            setTimeout(() => {
              const finalScore = memoryScore + (moves === 0 ? 30 : 20);
              const bonus = moves <= 8 ? 50 : 0;
              setMemoryScore(finalScore + bonus);
              
              speakEducationalContent(`Bravo! Jeu terminé avec ${finalScore + bonus} points!`, 'fr');
              
              Alert.alert(
                '🌺 Félicitations!', 
                `Tu as terminé en ${moves + 1} coups!\nScore final: ${finalScore + bonus} points!` +
                (bonus > 0 ? '\n🏆 Bonus rapidité: +50 points!' : ''),
                [{ text: 'Rejouer', onPress: initMemoryGame }]
              );
            }, 1000);
          }
        }, 1000);
      } else {
        // Pas une paire
        setTimeout(() => {
          setFlippedCards([]);
          setCanFlip(true);
          speakEducationalContent('Oups, essaie encore!', 'fr');
        }, 1500);
      }
    }
  };

  const renderMemoryGame = () => {
    if (memoryCards.length === 0) {
      return (
        <View style={styles.gameContainer}>
          <View style={styles.memoryStartScreen}>
            <Text style={styles.memoryStartTitle}>Mémoire des fleurs 🌺</Text>
            <Text style={styles.memoryStartDescription}>
              Retourne les cartes ylang-ylang et trouve les paires ! 
            </Text>
            <TouchableOpacity 
              style={styles.startMemoryButton}
              onPress={initMemoryGame}
            >
              <Text style={styles.startButtonText}>🌸 Commencer le jeu</Text>
            </TouchableOpacity>
          </View>
        </View>
      );
    }

    return (
      <View style={styles.gameContainer}>
        <View style={styles.gameHeader}>
          <Text style={styles.gameTitle}>Mémoire des fleurs 🌺</Text>
        </View>
        
        <View style={styles.gameProgressBar}>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Score</Text>
            <Text style={styles.progressValue}>{memoryScore}</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Coups</Text>
            <Text style={styles.progressValue}>{moves}</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Paires</Text>
            <Text style={styles.progressValue}>
              {matchedPairs.length / 2} / {memoryCards.length / 2}
            </Text>
          </View>
        </View>
        
        <View style={styles.memoryGrid}>
          {memoryCards.map((card) => (
            <TouchableOpacity
              key={card.id}
              style={[
                styles.memoryCard,
                flippedCards.includes(card.id) && styles.memoryCardFlipped,
                matchedPairs.includes(card.id) && styles.memoryCardMatched
              ]}
              onPress={() => handleCardFlip(card.id)}
              disabled={!canFlip && !flippedCards.includes(card.id)}
            >
              {flippedCards.includes(card.id) || matchedPairs.includes(card.id) ? (
                <View style={styles.memoryCardContent}>
                  <Text style={[
                    styles.memoryCardText,
                    card.type === 'french' ? styles.frenchCardText : styles.translationCardText
                  ]}>
                    {card.text}
                  </Text>
                  {card.type === 'translation' && (
                    <Text style={styles.languageLabel}>
                      {card.language}
                    </Text>
                  )}
                  {matchedPairs.includes(card.id) && (
                    <YlangYlangFlower size={32} />
                  )}
                </View>
              ) : (
                <View style={styles.memoryCardBack}>
                  <YlangYlangFlower size={28} />
                  <Text style={styles.cardBackText}>ylang-ylang</Text>
                </View>
              )}
            </TouchableOpacity>
          ))}
        </View>
        
        <TouchableOpacity 
          style={styles.restartButton}
          onPress={initMemoryGame}
        >
          <Text style={styles.restartButtonText}>🌺 Nouvelle partie</Text>
        </TouchableOpacity>
      </View>
    );
  };

  // États pour le quiz Mayotte
  const [quizQuestions, setQuizQuestions] = useState<any[]>([]);
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0);
  const [quizScore, setQuizScore] = useState(0);
  const [selectedQuizAnswer, setSelectedQuizAnswer] = useState<string | null>(null);
  const [showQuizResult, setShowQuizResult] = useState(false);
  const [quizStarted, setQuizStarted] = useState(false);

  // Questions du quiz Mayotte
  const createQuizQuestions = (words: Word[]) => {
    const quizData = [
      // Questions sur les langues
      {
        question: "Quelle est la langue principale parlée à Mayotte avec le français ?",
        options: ["Créole", "Shimaoré", "Swahili", "Malgache"],
        correct: "Shimaoré",
        explanation: "Le shimaoré est la langue locale principale de Mayotte, parlée par la majorité de la population.",
        category: "langue"
      },
      {
        question: "Le kibouchi est parlé principalement dans quelle partie de Mayotte ?",
        options: ["Petite-Terre", "Mamoudzou", "Grande-Terre", "Partout"],
        correct: "Grande-Terre",
        explanation: "Le kibouchi est traditionnellement parlé surtout à Grande-Terre (ouangani, chirongui, acoua etc).",
        category: "géographie"
      },
      {
        question: "Quelle est la fleur emblématique de Mayotte ?",
        options: ["Hibiscus", "Ylang-ylang", "Frangipane", "Bougainvillier"],
        correct: "Ylang-ylang",
        explanation: "L'ylang-ylang est la fleur emblématique de Mayotte, utilisée en parfumerie.",
        category: "culture"
      },
      {
        question: "Quel animal est le symbole de Mayotte ?",
        options: ["Tortue", "Dauphin", "Maki", "Requin"],
        correct: "Maki",
        explanation: "Le maki est l'animal emblématique de Mayotte, un lémurien endémique des Comores.",
        category: "culture"
      },
      {
        question: "Mayotte fait partie de quel archipel ?",
        options: ["Comores", "Seychelles", "Mascareignes", "Maldives"],
        correct: "Comores",
        explanation: "Mayotte fait géographiquement partie de l'archipel des Comores dans l'océan Indien.",
        category: "géographie"
      },
      {
        question: "Quelle est la danse traditionnelle de Mayotte ?",
        options: ["Shigoma", "Sega", "Maloya", "Quadrille"],
        correct: "Shigoma",
        explanation: "Le shigoma est une danse traditionnelle importante de Mayotte.",
        category: "tradition"
      },
      {
        question: "Le lagon de Mayotte est l'un des plus grands du monde ?",
        options: ["Vrai", "Faux", "Seulement en hiver", "Uniquement la nuit"],
        correct: "Vrai",
        explanation: "Mayotte possède effectivement l'un des plus grands lagons fermés au monde.",
        category: "géographie"
      },
      // Nouvelles questions basées sur l'image fournie
      {
        question: "Quelle est la capitale de Mayotte ?",
        options: ["Dzaoudzi", "Sada", "Mamoudzou", "Koungou"],
        correct: "Mamoudzou",
        explanation: "Mamoudzou est la capitale administrative et économique de Mayotte.",
        category: "géographie"
      },
      {
        question: "Comment s'appelle le lagon qui entoure Mayotte ?",
        options: ["Lagon de Zanzibar", "Lagon de Mayotte", "Lagon des Comores", "Lagon de Madagascar"],
        correct: "Lagon de Mayotte",
        explanation: "Le lagon de Mayotte est l'un des plus grands et beaux lagons fermés du monde, avec une barrière de corail presque complète.",
        category: "géographie"
      },
      {
        question: "Quelle fête religieuse est la plus célébrée à Mayotte ?",
        options: ["Noël", "Le Ramadan", "Diwali", "Pâques"],
        correct: "Le Ramadan",
        explanation: "La majorité de la population mahoraise est musulmane, et le Ramadan est une période très importante.",
        category: "culture"
      },
      {
        question: "Quel animal marin emblématique peut être observé à Mayotte ?",
        options: ["La tortue marine", "Le dauphin", "Le crocodile", "Le manchot"],
        correct: "La tortue marine",
        explanation: "Mayotte est célèbre pour ses plages où viennent pondre les tortues marines.",
        category: "nature"
      },
      {
        question: "Quel est le plat traditionnel à base de manioc et de coco ?",
        options: ["Le mataba", "Le rougail", "Le couscous", "Le mafé"],
        correct: "Le mataba",
        explanation: "Le mataba est préparé avec des feuilles de manioc pilées, cuites avec du lait de coco.",
        category: "cuisine"
      },
      {
        question: "Quelle boisson locale se prépare avec du sucre de canne et des fruits ?",
        options: ["Le punch mahorais", "Le café glacé", "Le thé vert", "Le bissap"],
        correct: "Le punch mahorais",
        explanation: "Le punch mahorais est une boisson festive préparée avec du rhum ou sans alcool pour les enfants, aromatisée aux fruits tropicaux.",
        category: "cuisine"
      },
      {
        question: "Quelle langue est également parlée dans certaines familles mahoraises ?",
        options: ["Le créole réunionnais", "Le swahili", "Le malgache", "L'arabe"],
        correct: "Le malgache",
        explanation: "Le malgache est parlé dans certaines familles mahoraises, en raison des liens historiques avec Madagascar.",
        category: "langue"
      },
      {
        question: "Quel est le statut administratif de Mayotte ?",
        options: ["Département français", "Territoire d'outre-mer", "Collectivité", "Région autonome"],
        correct: "Département français",
        explanation: "Mayotte est devenue le 101ème département français en 2011.",
        category: "politique"
      },
      {
        question: "Quelle est la monnaie utilisée à Mayotte ?",
        options: ["Le franc CFA", "Le dollar", "L'euro", "Le franc comorien"],
        correct: "L'euro",
        explanation: "Depuis que Mayotte est département français, la monnaie officielle est l'euro.",
        category: "économie"
      }
    ];

    // Ajouter des questions dynamiques basées sur le vocabulaire
    const vocabularyQuestions = words.slice(0, 5).map(word => ({
      question: `Comment dit-on "${word.french}" en shimaoré ?`,
      options: [
        word.shimaore,
        words[Math.floor(Math.random() * words.length)].shimaore,
        words[Math.floor(Math.random() * words.length)].shimaore,
        words[Math.floor(Math.random() * words.length)].shimaore
      ].filter((option, index, arr) => arr.indexOf(option) === index).slice(0, 4),
      correct: word.shimaore,
      explanation: `"${word.french}" se dit "${word.shimaore}" en shimaoré.`,
      category: "vocabulaire"
    }));

    // Mélanger et prendre 10 questions
    const allQuestions = [...quizData, ...vocabularyQuestions];
    return allQuestions.sort(() => Math.random() - 0.5).slice(0, 10);
  };

  // Initialiser le quiz
  const startQuiz = () => {
    const questions = createQuizQuestions(words);
    setQuizQuestions(questions);
    setCurrentQuizIndex(0);
    setQuizScore(0);
    setSelectedQuizAnswer(null);
    setShowQuizResult(false);
    setQuizStarted(true);
  };

  // Gérer la réponse du quiz
  const handleQuizAnswer = (selectedAnswer: string) => {
    const currentQuestion = quizQuestions[currentQuizIndex];
    setSelectedQuizAnswer(selectedAnswer);
    setShowQuizResult(true);

    const isCorrect = selectedAnswer === currentQuestion.correct;
    if (isCorrect) {
      setQuizScore(prev => prev + 10);
      speakEducationalContent('Bravo! Bonne réponse!', 'fr');
    } else {
      speakEducationalContent('Oups! Mauvaise réponse.', 'fr');
    }

    // Passer à la question suivante après 3 secondes
    setTimeout(() => {
      if (currentQuizIndex + 1 < quizQuestions.length) {
        setCurrentQuizIndex(prev => prev + 1);
        setSelectedQuizAnswer(null);
        setShowQuizResult(false);
      } else {
        // Fin du quiz
        setTimeout(() => {
          const finalScore = quizScore + (isCorrect ? 10 : 0);
          let message = '';
          if (finalScore >= 80) {
            message = `Excellent! Tu es un expert de Mayotte avec ${finalScore} points!`;
          } else if (finalScore >= 60) {
            message = `Très bien! Tu connais bien Mayotte avec ${finalScore} points!`;
          } else {
            message = `Continue à apprendre! Tu as ${finalScore} points. N'abandonne pas!`;
          }
          
          speakEducationalContent(message, 'fr');
          Alert.alert(
            '🏝️ Quiz Mayotte terminé!',
            message,
            [
              { text: 'Rejouer', onPress: startQuiz },
              { text: 'Retour', onPress: () => setQuizStarted(false) }
            ]
          );
        }, 1000);
      }
    }, 3000);
  };

  const renderQuizGame = () => {
    if (!quizStarted) {
      return (
        <View style={styles.gameContainer}>
          <View style={styles.quizStartScreen}>
            <Text style={styles.quizStartTitle}>Quiz Mayotte 🏝️</Text>
            <Text style={styles.quizStartDescription}>
              Teste tes connaissances sur les langues et la culture de Mayotte !
            </Text>
            <TouchableOpacity 
              style={styles.startQuizButton}
              onPress={startQuiz}
            >
              <Text style={styles.startButtonText}>🌺 Commencer le quiz</Text>
            </TouchableOpacity>
          </View>
        </View>
      );
    }

    if (quizQuestions.length === 0) {
      return (
        <View style={styles.gameContainer}>
          <Text style={styles.gameTitle}>Chargement du quiz...</Text>
        </View>
      );
    }

    const currentQuestion = quizQuestions[currentQuizIndex];

    return (
      <View style={styles.gameContainer}>
        <View style={styles.gameHeader}>
          <Text style={styles.gameTitle}>Quiz Mayotte 🏝️</Text>
        </View>
        
        <View style={styles.quizProgressBar}>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Question</Text>
            <Text style={styles.progressValue}>
              {currentQuizIndex + 1} / {quizQuestions.length}
            </Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Score</Text>
            <Text style={styles.progressValue}>{quizScore}</Text>
          </View>
        </View>

        <View style={styles.quizCard}>
          <View style={styles.categoryBadge}>
            <Text style={styles.categoryText}>{currentQuestion.category}</Text>
          </View>
          
          <Text style={styles.quizQuestion}>{currentQuestion.question}</Text>
          
          <View style={styles.quizOptionsContainer}>
            {currentQuestion.options.map((option: string, index: number) => (
              <TouchableOpacity
                key={index}
                style={[
                  styles.quizOptionButton,
                  showQuizResult && option === currentQuestion.correct && styles.correctQuizOption,
                  showQuizResult && selectedQuizAnswer === option && option !== currentQuestion.correct && styles.wrongQuizOption,
                  showQuizResult && styles.disabledQuizOption
                ]}
                onPress={() => !showQuizResult && handleQuizAnswer(option)}
                disabled={showQuizResult}
              >
                <Text style={[
                  styles.quizOptionText,
                  showQuizResult && option === currentQuestion.correct && styles.correctQuizOptionText,
                  showQuizResult && selectedQuizAnswer === option && option !== currentQuestion.correct && styles.wrongQuizOptionText
                ]}>
                  {option}
                </Text>
                {showQuizResult && option === currentQuestion.correct && (
                  <Ionicons name="checkmark-circle" size={24} color="#4CAF50" />
                )}
                {showQuizResult && selectedQuizAnswer === option && option !== currentQuestion.correct && (
                  <Ionicons name="close-circle" size={24} color="#F44336" />
                )}
              </TouchableOpacity>
            ))}
          </View>

          {showQuizResult && (
            <View style={styles.quizExplanation}>
              <Text style={styles.explanationTitle}>
                {selectedQuizAnswer === currentQuestion.correct ? '🎉 Bravo!' : '📚 À retenir :'}
              </Text>
              <Text style={styles.explanationText}>
                {currentQuestion.explanation}
              </Text>
            </View>
          )}
        </View>
      </View>
    );
  };

  const renderBuildSentenceGame = () => {
    // Fonctions pour gérer les mots
    const addWordToSentence = (word: string) => {
      setBuiltSentence([...builtSentence, word]);
      setAvailableWords(availableWords.filter(w => w !== word));
    };

    const removeWordFromSentence = (index: number) => {
      const word = builtSentence[index];
      setBuiltSentence(builtSentence.filter((_, i) => i !== index));
      setAvailableWords([...availableWords, word]);
    };

    const checkSentence = async () => {
      if (!currentSentence) return;
      
      const correctWords = selectedLanguage === 'shimaore' 
        ? currentSentence.shimaore_words 
        : currentSentence.kibouchi_words;
      
      const isCorrect = builtSentence.length === correctWords.length &&
        builtSentence.every((word, index) => word === correctWords[index]);
      
      if (isCorrect) {
        setSentenceScore(sentenceScore + 10);
        setSentenceFeedbackType('success');
        setShowSentenceFeedback(true);
        
        // Prononcer d'abord le français avec voix féminine
        await speakEducationalContent(currentSentence.french, 'fr');
        await new Promise(resolve => setTimeout(resolve, 800));
        
        // Puis prononcer la phrase correcte en langue locale avec voix féminine
        const correctSentence = selectedLanguage === 'shimaore' 
          ? currentSentence.shimaore 
          : currentSentence.kibouchi;
        await speakText(correctSentence, selectedLanguage);
        
        // Passer automatiquement à la phrase suivante après 2 secondes
        setTimeout(() => {
          setShowSentenceFeedback(false);
          nextSentence();
        }, 2000);
      } else {
        setSentenceFeedbackType('error');
        setShowSentenceFeedback(true);
        
        // Prononcer le français pour rappeler la phrase à traduire
        await speakEducationalContent(currentSentence.french, 'fr');
        
        // Cacher le feedback d'erreur après 2 secondes
        setTimeout(() => {
          setShowSentenceFeedback(false);
        }, 2000);
      }
    };

    const nextSentence = () => {
      if (currentSentenceIndex < sentences.length - 1) {
        const nextIndex = currentSentenceIndex + 1;
        const nextSent = sentences[nextIndex];
        setCurrentSentenceIndex(nextIndex);
        setCurrentSentence(nextSent);
        
        const wordsToShuffle = selectedLanguage === 'shimaore' 
          ? nextSent.shimaore_words 
          : nextSent.kibouchi_words;
        setAvailableWords([...wordsToShuffle].sort(() => Math.random() - 0.5));
        setBuiltSentence([]);
      } else {
        Alert.alert('Félicitations! 🎊', `Jeu terminé! Score final: ${sentenceScore + 10}`, [
          { text: 'Recommencer', onPress: () => startGame('build-sentence') },
          { text: 'Retour', onPress: () => { setGameStarted(false); setCurrentGame(null); } }
        ]);
      }
    };

    const switchLanguage = () => {
      if (!currentSentence) return;
      
      const newLanguage = selectedLanguage === 'shimaore' ? 'kibouchi' : 'shimaore';
      setSelectedLanguage(newLanguage);
      
      const wordsToShuffle = newLanguage === 'shimaore' 
        ? currentSentence.shimaore_words 
        : currentSentence.kibouchi_words;
      setAvailableWords([...wordsToShuffle].sort(() => Math.random() - 0.5));
      setBuiltSentence([]);
    };

    if (!currentSentence) {
      return (
        <View style={styles.gameContainer}>
          <Text style={styles.loadingText}>Chargement des phrases...</Text>
        </View>
      );
    }

    return (
      <ScrollView style={styles.gameContainer}>
        <View style={styles.gameHeader}>
          <Text style={styles.gameTitle}>Construire des phrases 📝</Text>
        </View>
        
        <View style={styles.gameProgressBar}>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Question</Text>
            <Text style={styles.progressValue}>
              {currentSentenceIndex + 1} / {sentences.length}
            </Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Score</Text>
            <Text style={styles.progressValue}>{sentenceScore}</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressLabel}>Langue</Text>
            <TouchableOpacity onPress={switchLanguage}>
              <Text style={[styles.progressValue, styles.languageButton]}>
                {selectedLanguage === 'shimaore' ? 'SH' : 'KI'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Légende des couleurs de conjugaison */}
        <ConjugationColorLegend language={selectedLanguage} compact={true} />

        {/* Phrase française à traduire */}
        <View style={styles.sentenceTarget}>
          <View style={styles.sentenceTargetHeader}>
            <Text style={styles.sentenceTargetLabel}>Phrase à traduire :</Text>
            <TouchableOpacity 
              style={styles.sentenceAudioButton}
              onPress={() => speakEducationalContent(currentSentence.french, 'fr')}
            >
              <Ionicons name="volume-high" size={20} color="#4ECDC4" />
            </TouchableOpacity>
          </View>
          <Text style={styles.sentenceTargetText}>{currentSentence.french}</Text>
        </View>

        {/* Zone de construction de la phrase */}
        <View style={styles.sentenceBuilder}>
          <Text style={styles.sentenceBuilderLabel}>
            Votre phrase en {selectedLanguage === 'shimaore' ? 'Shimaoré' : 'Kibouchi'} :
          </Text>
          <View style={styles.sentenceBuilderZone}>
            {builtSentence.length === 0 ? (
              <Text style={styles.sentenceBuilderPlaceholder}>
                Sélectionnez les mots ci-dessous...
              </Text>
            ) : (
              builtSentence.map((word, index) => (
                <ColoredConjugationWord
                  key={index}
                  word={word}
                  language={selectedLanguage}
                  onPress={() => removeWordFromSentence(index)}
                  style={styles.builtWordButton}
                  textStyle={styles.builtWordText}
                  showTenseIndicator={false}
                />
              ))
            )}
          </View>
        </View>

        {/* Mots disponibles */}
        <View style={styles.availableWords}>
          <Text style={styles.availableWordsLabel}>Mots disponibles :</Text>
          <View style={styles.availableWordsZone}>
            {availableWords.map((word, index) => (
              <ColoredConjugationWord
                key={index}
                word={word}
                language={selectedLanguage}
                onPress={() => addWordToSentence(word)}
                style={styles.availableWordButton}
                textStyle={styles.availableWordText}
                showTenseIndicator={true}
              />
            ))}
          </View>
        </View>

        {/* Boutons d'action */}
        <View style={styles.gameActionButtons}>
          <TouchableOpacity 
            onPress={checkSentence}
            style={[styles.checkButton, builtSentence.length === 0 && styles.checkButtonDisabled]}
            disabled={builtSentence.length === 0}
          >
            <Text style={styles.checkButtonText}>Vérifier la phrase</Text>
          </TouchableOpacity>
          
          {builtSentence.length > 0 && (
            <TouchableOpacity 
              style={styles.listenButton}
              onPress={async () => {
                const builtSentenceText = builtSentence.join(' ');
                await speakTextLocal(builtSentenceText, selectedLanguage);
              }}
            >
              <Ionicons name="headset" size={18} color="#fff" />
              <Text style={styles.listenButtonText}>Écouter</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Feedback visuel */}
        {showSentenceFeedback && (
          <View style={[
            styles.sentenceFeedback,
            sentenceFeedbackType === 'success' ? styles.sentenceFeedbackSuccess : styles.sentenceFeedbackError
          ]}>
            <Ionicons 
              name={sentenceFeedbackType === 'success' ? 'checkmark-circle' : 'close-circle'} 
              size={32} 
              color="#fff" 
            />
            <Text style={styles.sentenceFeedbackText}>
              {sentenceFeedbackType === 'success' ? 'Bravo! Phrase correcte! 🎉' : 'Essaie encore! L\'ordre n\'est pas correct. 🤔'}
            </Text>
          </View>
        )}

        {/* Bouton d'aide */}
        <TouchableOpacity 
          onPress={() => {
            const correctSentence = selectedLanguage === 'shimaore' 
              ? currentSentence.shimaore 
              : currentSentence.kibouchi;
            Alert.alert('Aide 💡', `Phrase correcte :\n${correctSentence}`);
          }}
          style={styles.helpButton}
        >
          <Text style={styles.helpButtonText}>💡 Aide</Text>
        </TouchableOpacity>
      </ScrollView>
    );
  };

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
            <View style={styles.encouragementRow}>
              <MakiMayotte size={24} />
              <Text style={styles.encouragementText}> Les makis de Mayotte t'encouragent! </Text>
              <YlangYlangFlower size={24} />
            </View>
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
  encouragementRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  encouragementText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
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
    paddingHorizontal: 16,
    paddingTop: 10,
  },
  gameHeader: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  gameTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 8,
  },
  scoreText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: '#4ECDC4',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    textAlign: 'center',
    minWidth: 80,
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
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#E9ECEF', 
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginVertical: 6,
    minHeight: 48, // Taille minimum pour les doigts
  },
  optionText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#2C3E50',
    flex: 1,
    textAlign: 'left',
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
  // Nouveaux styles pour le jeu de questions
  questionContainer: {
    flex: 1,
    padding: 20,
  },
  questionCounter: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    backgroundColor: '#FFE135',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 15,
    alignSelf: 'center',
  },
  questionCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
  },
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    textAlign: 'center',
    marginVertical: 20,
  },
  correctOption: {
    backgroundColor: '#E8F5E8',
    borderColor: '#4CAF50',
  },
  wrongOption: {
    backgroundColor: '#FFEBEE',
    borderColor: '#F44336',
  },
  disabledOption: {
    opacity: 0.8,
  },
  correctOptionText: {
    color: '#2E7D32',
  },
  wrongOptionText: {
    color: '#C62828',
  },
  resultContainer: {
    alignItems: 'center',
    marginTop: 20,
    padding: 15,
    backgroundColor: 'rgba(0, 0, 0, 0.05)',
    borderRadius: 10,
  },
  resultText: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  correctText: {
    color: '#4CAF50',
  },
  wrongText: {
    color: '#F44336',
  },

  // Styles pour le jeu de mémoire (Mémoire des fleurs)
  memoryStartScreen: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  memoryStartTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 20,
  },
  memoryStartDescription: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 40,
    paddingHorizontal: 10,
    lineHeight: 24,
    maxWidth: 320,
  },
  startMemoryButton: {
    backgroundColor: '#4ECDC4',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 25,
    minWidth: 250,
    alignItems: 'center',
  },
  startButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  // Anciens styles supprimés - remplacés par gameProgressBar
  movesText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
    backgroundColor: '#FFE135',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    textAlign: 'center',
    minWidth: 80,
  },
  memoryGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    alignItems: 'center',
    paddingHorizontal: 8,
    marginVertical: 10,
  },
  memoryCard: {
    width: Math.min(width * 0.28, 110),
    height: Math.min(width * 0.20, 85),
    margin: 4,
    borderRadius: 12,
    backgroundColor: '#FFF8DC', // Couleur ylang-ylang (jaune clair)
    borderWidth: 2,
    borderColor: '#FFD700', // Bordure dorée
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 3,
  },
  memoryCardFlipped: {
    backgroundColor: '#FFFFFF',
    borderColor: '#4ECDC4',
  },
  memoryCardMatched: {
    backgroundColor: '#E8F8F5',
    borderColor: '#4ECDC4',
    borderWidth: 4,
  },
  memoryCardContent: {
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
  },
  memoryCardText: {
    fontSize: 12,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 2,
    flexShrink: 1,
  },
  frenchCardText: {
    color: '#2C3E50',
    fontSize: 13,
  },
  translationCardText: {
    color: '#8E44AD',
    fontSize: 12,
  },
  languageLabel: {
    fontSize: 9,
    color: '#7F8C8D',
    fontStyle: 'italic',
    marginTop: 1,
  },
  flowerEmoji: {
    fontSize: 20,
    position: 'absolute',
    top: 5,
    right: 8,
  },
  memoryCardBack: {
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '100%',
  },
  cardBackEmoji: {
    fontSize: 18,
    marginBottom: 2,
  },
  cardBackText: {
    fontSize: 9,
    color: '#B8860B',
    fontStyle: 'italic',
    textAlign: 'center',
  },
  restartButton: {
    backgroundColor: '#E74C3C',
    paddingHorizontal: 25,
    paddingVertical: 12,
    borderRadius: 20,
    marginTop: 20,
    alignSelf: 'center',
  },
  restartButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  correctAnswerText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    fontStyle: 'italic',
  },

  // Styles pour le Quiz Mayotte
  quizStartScreen: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  quizStartTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 20,
  },
  quizStartDescription: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 40,
    paddingHorizontal: 10,
    lineHeight: 24,
    maxWidth: 320,
  },
  quizDescription: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
    paddingHorizontal: 20,
    lineHeight: 24,
  },
  startQuizButton: {
    backgroundColor: '#45B7D1',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 25,
    minWidth: 250,
    alignItems: 'center',
  },
  // Barre de progression unifiée pour tous les jeux - disposition verticale
  gameProgressBar: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  progressItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 6,
  },
  progressLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
    flex: 1,
  },
  progressValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2C3E50',
    backgroundColor: '#FFE135',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    textAlign: 'center',
    minWidth: 60,
  },
  quizCard: {
    backgroundColor: 'white',
    margin: 15,
    padding: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  categoryBadge: {
    backgroundColor: '#FFE135', // Couleur jaune de Mayotte
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    alignSelf: 'flex-start',
    marginBottom: 15,
  },
  categoryText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#8B4513',
    textTransform: 'uppercase',
  },
  quizQuestion: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 20,
    lineHeight: 26,
    textAlign: 'center',
  },
  quizOptionsContainer: {
    marginBottom: 20,
  },
  quizOptionButton: {
    backgroundColor: '#F8F9FA',
    paddingVertical: 14,
    paddingHorizontal: 16,
    marginVertical: 6,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#E9ECEF',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    minHeight: 50, // Taille minimum tactile
  },
  correctQuizOption: {
    backgroundColor: '#D4F8D4',
    borderColor: '#4CAF50',
  },
  wrongQuizOption: {
    backgroundColor: '#FFE6E6',
    borderColor: '#F44336',
  },
  disabledQuizOption: {
    opacity: 0.8,
  },
  quizOptionText: {
    fontSize: 16,
    color: '#495057',
    fontWeight: '500',
    flex: 1,
  },
  correctQuizOptionText: {
    color: '#2E7D32',
    fontWeight: 'bold',
  },
  wrongQuizOptionText: {
    color: '#C62828',
    fontWeight: 'bold',
  },
  quizExplanation: {
    backgroundColor: '#F0F8FF',
    padding: 15,
    borderRadius: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#45B7D1',
  },
  explanationTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 8,
  },
  explanationText: {
    fontSize: 14,
    color: '#5A6C7D',
    lineHeight: 20,
  },

  // Styles pour le jeu "Construire des phrases"
  loadingText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginTop: 20,
  },
  languageButton: {
    backgroundColor: '#3498DB',
    color: '#fff',
  },
  sentenceTarget: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  sentenceTargetLabel: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#7F8C8D',
    textTransform: 'uppercase',
    marginBottom: 8,
  },
  sentenceTargetText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    textAlign: 'center',
  },
  sentenceBuilder: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 16,
    marginBottom: 16,
    minHeight: 100,
  },
  sentenceBuilderLabel: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#7F8C8D',
    textTransform: 'uppercase',
    marginBottom: 8,
  },
  sentenceBuilderZone: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    minHeight: 60,
    borderWidth: 2,
    borderColor: '#E9ECEF',
    borderStyle: 'dashed',
    borderRadius: 10,
    padding: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sentenceBuilderPlaceholder: {
    color: '#ADB5BD',
    fontSize: 14,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  builtWordButton: {
    backgroundColor: '#4ECDC4',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    margin: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  builtWordText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  availableWords: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 16,
    marginBottom: 16,
  },
  availableWordsLabel: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#7F8C8D',
    textTransform: 'uppercase',
    marginBottom: 8,
  },
  availableWordsZone: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  availableWordButton: {
    backgroundColor: '#F8F9FA',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    margin: 4,
    borderWidth: 2,
    borderColor: '#E9ECEF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  availableWordText: {
    color: '#495057',
    fontSize: 14,
    fontWeight: '600',
  },
  checkButton: {
    backgroundColor: '#28A745',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 25,
    marginBottom: 16,
    alignSelf: 'center',
    minWidth: 200,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  checkButtonDisabled: {
    backgroundColor: '#ADB5BD',
    opacity: 0.6,
  },
  checkButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  helpButton: {
    backgroundColor: '#FFC107',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 20,
    alignSelf: 'center',
    marginBottom: 20,
  },
  helpButtonText: {
    color: '#212529',
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',
  },

  // Styles pour l'audio et la prononciation
  sentenceTargetHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  sentenceAudioButton: {
    backgroundColor: 'rgba(78, 205, 196, 0.1)',
    borderRadius: 20,
    padding: 8,
    borderWidth: 1,
    borderColor: '#4ECDC4',
  },
  gameActionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 10,
    marginBottom: 16,
  },
  listenButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#9B59B6',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 20,
    gap: 6,
    minHeight: 44,
  },
  listenButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  
  // Styles pour le feedback visuel
  sentenceFeedback: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    marginTop: 16,
    gap: 12,
  },
  sentenceFeedbackSuccess: {
    backgroundColor: '#28A745',
  },
  sentenceFeedbackError: {
    backgroundColor: '#DC3545',
  },
  sentenceFeedbackText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    flex: 1,
  },
});