import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function TestSimpleGame() {
  const [score, setScore] = useState(0);
  const [currentQuestion] = useState({
    french: "Bonjour",
    options: [
      { text: "Kwezi", isCorrect: true },
      { text: "Mboubou", isCorrect: false }
    ]
  });

  const handleAnswer = (option: any) => {
    if (option.isCorrect) {
      setScore(prev => prev + 10);
      alert("Bravo!");
    } else {
      alert("Oups! La bonne réponse était: Kwezi");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Test Jeu Simple</Text>
      <Text style={styles.score}>Score: {score}</Text>
      
      <View style={styles.questionCard}>
        <Text style={styles.frenchText}>{currentQuestion.french}</Text>
        <Text style={styles.questionText}>Comment dit-on en Shimaoré?</Text>
        
        {currentQuestion.options.map((option, index) => (
          <TouchableOpacity 
            key={index}
            style={styles.optionButton}
            onPress={() => handleAnswer(option)}
          >
            <Text style={styles.optionText}>{option.text}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
  },
  score: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  questionCard: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
  },
  frenchText: {
    fontSize: 22,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  questionText: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
  },
  optionButton: {
    backgroundColor: '#e0e0e0',
    padding: 15,
    marginVertical: 5,
    borderRadius: 8,
  },
  optionText: {
    fontSize: 16,
    textAlign: 'center',
  },
});