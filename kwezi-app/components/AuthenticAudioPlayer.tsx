import React, { useState } from 'react';
import { TouchableOpacity, View, Text, StyleSheet, Alert } from 'react-native';
import { Audio } from 'expo-av';
import { Ionicons } from '@expo/vector-icons';

interface AuthenticAudioPlayerProps {
  word: {
    french: string;
    shimaore: string;
    kibouchi: string;
    audio_url?: string;
    audio_filename?: string;
    audio_pronunciation_lang?: string;
    has_authentic_audio?: boolean;
  };
  size?: 'small' | 'medium' | 'large';
}

export const AuthenticAudioPlayer: React.FC<AuthenticAudioPlayerProps> = ({
  word,
  size = 'medium'
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [sound, setSound] = useState<Audio.Sound | null>(null);

  const iconSizes = {
    small: 20,
    medium: 24,
    large: 32
  };

  const buttonSizes = {
    small: 32,
    medium: 40,
    large: 48
  };

  const playAuthentic = async () => {
    try {
      if (!word.has_authentic_audio || !word.audio_filename) {
        Alert.alert('Audio non disponible', 'Cette prononciation authentique n\'est pas encore disponible.');
        return;
      }

      if (sound) {
        await sound.unloadAsync();
      }

      setIsPlaying(true);

      console.log('🎵 Lecture audio authentique:', word.french, word.audio_filename);
      
      try {
        // Construire le chemin vers le fichier audio réel
        const audioPath = require(`../assets/audio/famille/${word.audio_filename}`);
        
        const { sound: newSound } = await Audio.Sound.createAsync(
          audioPath,
          {
            shouldPlay: true,
            volume: 1.0,
          }
        );

        setSound(newSound);

        newSound.setOnPlaybackStatusUpdate((status) => {
          if (status.isLoaded && status.didJustFinish) {
            setIsPlaying(false);
          }
        });

        console.log(`✅ Lecture audio authentique réussie: ${word.french}`);

      } catch (audioError) {
        console.log('⚠️ Fichier audio non trouvé, utilisation de la synthèse vocale');
        console.log('Erreur audio:', audioError);
        
        // Fallback vers la synthèse vocale féminine
        const { speakText } = require('../utils/feminineSpeechUtils');
        const textToSpeak = word.audio_pronunciation_lang === 'kibouchi' ? word.kibouchi : word.shimaore;
        const language = word.audio_pronunciation_lang === 'kibouchi' ? 'kibouchi' : 'shimaore';
        
        await speakText(textToSpeak, language);
        
        setTimeout(() => setIsPlaying(false), 2000);
      }

    } catch (error) {
      console.error('❌ Erreur lecture audio:', error);
      setIsPlaying(false);
      Alert.alert('Erreur', 'Impossible de lire l\'audio');
    }
  };

  if (!word.has_authentic_audio) {
    return null; // Ou retourner un bouton TTS classique
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[
          styles.audioButton,
          { 
            width: buttonSizes[size], 
            height: buttonSizes[size],
            backgroundColor: isPlaying ? '#FF6B6B' : '#4ECDC4'
          }
        ]}
        onPress={playAuthentic}
        disabled={isPlaying}
      >
        <Ionicons 
          name={isPlaying ? "stop" : "volume-high"} 
          size={iconSizes[size]} 
          color="white" 
        />
      </TouchableOpacity>
      
      {word.audio_pronunciation_lang && (
        <Text style={[styles.langLabel, { fontSize: size === 'small' ? 10 : 12 }]}>
          {word.audio_pronunciation_lang === 'both' ? 'S+K' : 
           word.audio_pronunciation_lang === 'shimaore' ? 'S' : 'K'}
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginHorizontal: 4,
  },
  audioButton: {
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  langLabel: {
    marginTop: 2,
    fontSize: 10,
    color: '#666',
    fontWeight: '500',
  },
});

export default AuthenticAudioPlayer;