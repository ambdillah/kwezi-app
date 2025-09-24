/**
 * PANNEAU DE TEST DE VOIX
 * =======================
 * Composant pour tester différentes configurations de voix
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { speakWithFeminineVoice, testFeminineVoice } from '../utils/feminineSpeechUtils';
import { runVoiceDemo, quickVoiceTest, showAvailableVoices } from '../utils/voiceTestUtils';

interface VoiceTestPanelProps {
  visible?: boolean;
  onClose?: () => void;
}

export const VoiceTestPanel: React.FC<VoiceTestPanelProps> = ({ 
  visible = false, 
  onClose 
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  if (!visible) return null;

  const testVoice = async (type: string, description: string) => {
    if (isPlaying) return;
    
    setIsPlaying(true);
    
    try {
      const testText = `Bonjour ! Voici la voix ${description}. Est-ce que cette voix vous convient pour apprendre le shimaoré et le kibouchi ?`;
      
      switch (type) {
        case 'energetic':
          await speakWithFeminineVoice(testText, 'fr', 'feminine', 'warm');
          break;
        case 'storyteller':
          await speakWithFeminineVoice(testText, 'fr', 'feminine', 'gentle');
          break;
        case 'calm':
          await speakWithFeminineVoice(testText, 'fr', 'feminine', 'calm');
          break;
        case 'demo':
          await runVoiceDemo();
          break;
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de tester la voix');
      console.log('Erreur test voix:', error);
    } finally {
      setIsPlaying(false);
    }
  };

  const testPhonetics = async () => {
    if (isPlaying) return;
    
    setIsPlaying(true);
    try {
      await speakWithEnhancedVoice("Test des corrections phonétiques", 'fr', 'masculine', 'energetic');
      await new Promise(resolve => setTimeout(resolve, 1000));
      await speakWithEnhancedVoice("wami nisnguadza", 'shimaore', 'masculine', 'energetic');
      await new Promise(resolve => setTimeout(resolve, 1000));
      await speakWithEnhancedVoice("zahou za msoma", 'kibouchi', 'masculine', 'energetic');
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de tester la phonétique');
    } finally {
      setIsPlaying(false);
    }
  };

  return (
    <View style={styles.overlay}>
      <View style={styles.panel}>
        <View style={styles.header}>
          <Text style={styles.title}>🎙️ Test des Voix Féminines</Text>
          <TouchableOpacity onPress={onClose} style={styles.closeButton}>
            <Ionicons name="close" size={24} color="#333" />
          </TouchableOpacity>
        </View>
        
        <Text style={styles.subtitle}>
          Testez différentes voix pour choisir la plus charismatique
        </Text>
        
        <View style={styles.buttonsContainer}>
          <TouchableOpacity
            style={[styles.testButton, styles.energeticButton]}
            onPress={() => testVoice('energetic', 'masculine énergique')}
            disabled={isPlaying}
          >
            <Ionicons name="flash" size={20} color="white" />
            <Text style={styles.buttonText}>Voix Énergique</Text>
            <Text style={styles.buttonSubtext}>Recommandée ⭐</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.testButton, styles.storytellerButton]}
            onPress={() => testVoice('storyteller', 'masculine conteur')}
            disabled={isPlaying}
          >
            <Ionicons name="book" size={20} color="white" />
            <Text style={styles.buttonText}>Voix Conteur</Text>
            <Text style={styles.buttonSubtext}>Pour les histoires</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.testButton, styles.calmButton]}
            onPress={() => testVoice('calm', 'masculine calme')}
            disabled={isPlaying}
          >
            <Ionicons name="leaf" size={20} color="white" />
            <Text style={styles.buttonText}>Voix Calme</Text>
            <Text style={styles.buttonSubtext}>Relaxante</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.testButton, styles.phoneticButton]}
            onPress={testPhonetics}
            disabled={isPlaying}
          >
            <Ionicons name="language" size={20} color="white" />
            <Text style={styles.buttonText}>Test Phonétique</Text>
            <Text style={styles.buttonSubtext}>Shimaoré & Kibouchi</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.testButton, styles.demoButton]}
            onPress={() => testVoice('demo', 'démonstration complète')}
            disabled={isPlaying}
          >
            <Ionicons name="play-circle" size={20} color="white" />
            <Text style={styles.buttonText}>Démonstration</Text>
            <Text style={styles.buttonSubtext}>Test complet</Text>
          </TouchableOpacity>
        </View>
        
        {isPlaying && (
          <View style={styles.playingIndicator}>
            <Ionicons name="volume-high" size={16} color="#4ECDC4" />
            <Text style={styles.playingText}>Test en cours...</Text>
          </View>
        )}
        
        <Text style={styles.instructions}>
          💡 Conseil : Testez chaque voix et choisissez celle qui rend l'apprentissage plus agréable !
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 1000,
    justifyContent: 'center',
    alignItems: 'center',
  },
  panel: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    margin: 20,
    maxWidth: 400,
    width: '90%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 10,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  closeButton: {
    padding: 5,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
    textAlign: 'center',
  },
  buttonsContainer: {
    gap: 12,
  },
  testButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderRadius: 12,
    gap: 10,
  },
  energeticButton: {
    backgroundColor: '#FF6B6B',
  },
  storytellerButton: {
    backgroundColor: '#4ECDC4',
  },
  calmButton: {
    backgroundColor: '#96CEB4',
  },
  phoneticButton: {
    backgroundColor: '#FECA57',
  },
  demoButton: {
    backgroundColor: '#6C5CE7',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
    flex: 1,
  },
  buttonSubtext: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: 12,
  },
  playingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 15,
    gap: 8,
  },
  playingText: {
    color: '#4ECDC4',
    fontWeight: '500',
  },
  instructions: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
    marginTop: 15,
    fontStyle: 'italic',
  },
});

export default VoiceTestPanel;