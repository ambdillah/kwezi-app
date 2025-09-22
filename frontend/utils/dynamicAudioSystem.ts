/**
 * SYSTÈME AUDIO DYNAMIQUE
 * ========================
 * Utilise les métadonnées de la base de données pour jouer
 * les enregistrements audio authentiques ou la synthèse vocale
 */

import { Audio } from 'expo-av';
import { Asset } from 'expo-asset';
import { speakText } from './speechUtils';

export type AudioLanguage = 'fr' | 'shimaore' | 'kibouchi';

interface WordWithAudio {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  has_authentic_audio?: boolean;
  audio_filename?: string;
  audio_pronunciation_lang?: string;
  audio_source?: string;
}

/**
 * Interface pour le contrôle audio
 */
interface AudioController {
  sound: Audio.Sound | null;
  isPlaying: boolean;
}

let currentAudio: AudioController = {
  sound: null,
  isPlaying: false
};

/**
 * Arrête l'audio en cours s'il y en a un
 */
export const stopCurrentAudio = async (): Promise<void> => {
  try {
    if (currentAudio.sound && currentAudio.isPlaying) {
      await currentAudio.sound.stopAsync();
      await currentAudio.sound.unloadAsync();
      currentAudio.sound = null;
      currentAudio.isPlaying = false;
      console.log('🔇 Audio authentique arrêté');
    }
  } catch (error) {
    console.log('Erreur lors de l\'arrêt de l\'audio:', error);
  }
};

/**
 * Joue un enregistrement audio authentique local via URI
 */
export const playLocalAuthenticAudio = async (
  audioFilename: string,
  onStart?: () => void,
  onComplete?: () => void
): Promise<boolean> => {
  try {
    // Construire le chemin URI vers le fichier audio
    const audioUri = `file:///app/frontend/assets/audio/famille/${audioFilename}`;
    
    // Arrêter l'audio précédent
    await stopCurrentAudio();
    
    console.log(`🎵 Chargement audio authentique: ${audioFilename}`);
    console.log(`📂 URI: ${audioUri}`);
    
    // Configurer l'audio
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });
    
    // Charger et jouer l'audio
    const { sound } = await Audio.Sound.createAsync(
      { uri: audioUri },
      { 
        shouldPlay: true,
        volume: 1.0,
        isLooping: false 
      }
    );
    
    currentAudio.sound = sound;
    currentAudio.isPlaying = true;
    
    onStart?.();
    
    // Écouter la fin de la lecture
    sound.setOnPlaybackStatusUpdate((status) => {
      if (status.isLoaded && status.didJustFinish) {
        currentAudio.isPlaying = false;
        sound.unloadAsync();
        currentAudio.sound = null;
        onComplete?.();
        console.log('✅ Audio authentique local terminé');
      }
    });
    
    return true;
    
  } catch (error) {
    console.log('❌ Erreur lors de la lecture de l\'audio authentique local:', error);
    console.log('🔄 Tentative avec Asset API...');
    
    // Fallback: essayer avec Asset API si disponible
    try {
      const assetUri = Asset.fromModule(require('../assets/adaptive-icon.png')).uri; // Placeholder pour tester
      console.log('⚠️ Utilisation d\'un placeholder pour le test');
      return false; // Forcer le fallback TTS pour le moment
    } catch (assetError) {
      console.log('❌ Asset API aussi échoué:', assetError);
      return false;
    }
  }
};

/**
 * Fonction principale pour jouer un mot avec les nouvelles métadonnées
 */
export const playWordWithMetadata = async (
  word: WordWithAudio,
  language: 'shimaore' | 'kibouchi',
  onStart?: () => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Vérifier s'il existe un audio authentique pour ce mot
    if (word.has_authentic_audio && word.audio_filename) {
      // Vérifier si la langue correspond
      const shouldUseAuthentic = 
        word.audio_pronunciation_lang === 'both' ||
        word.audio_pronunciation_lang === language ||
        (word.audio_pronunciation_lang === 'shimaoré' && language === 'shimaore') ||
        (word.audio_pronunciation_lang === 'shimaore' && language === 'shimaore');

      if (shouldUseAuthentic) {
        console.log(`🎯 Audio authentique trouvé pour "${word.french}" (${word.audio_filename})`);
        
        const success = await playLocalAuthenticAudio(
          word.audio_filename,
          onStart,
          onComplete
        );
        
        if (success) {
          return; // Audio authentique joué avec succès
        }
        
        console.log('⚠️ Audio authentique échoué, utilisation de la synthèse vocale');
      }
    }
    
    // Fallback vers la synthèse vocale
    const textToSpeak = language === 'shimaore' ? word.shimaore : word.kibouchi;
    console.log(`🔊 Utilisation de la synthèse vocale pour "${textToSpeak}" en ${language}`);
    
    onStart?.();
    await speakText(textToSpeak, language);
    onComplete?.();
    
  } catch (error) {
    console.log('Erreur générale dans playWordWithMetadata:', error);
    
    // Dernier fallback : synthèse vocale simple
    try {
      const textToSpeak = language === 'shimaore' ? word.shimaore : word.kibouchi;
      await speakText(textToSpeak, language);
    } catch (fallbackError) {
      console.log('Erreur fallback:', fallbackError);
    }
  }
};

/**
 * Fonction pour jouer un mot dans toutes les langues disponibles
 */
export const playWordAllLanguagesWithMetadata = async (
  word: WordWithAudio,
  onLanguageStart?: (language: string) => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Français
    onLanguageStart?.('français');
    await speakText(word.french, 'fr');
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Shimaoré
    onLanguageStart?.('shimaoré');
    await new Promise<void>((resolve) => {
      playWordWithMetadata(word, 'shimaore', undefined, resolve);
    });
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Kibouchi
    onLanguageStart?.('kibouchi');
    await new Promise<void>((resolve) => {
      playWordWithMetadata(word, 'kibouchi', undefined, resolve);
    });
    
    onComplete?.();
    
  } catch (error) {
    console.log('Erreur lors de la lecture dans toutes les langues:', error);
  }
};

/**
 * Vérifie si un mot a un enregistrement audio authentique
 */
export const hasAuthenticAudioMetadata = (word: WordWithAudio): boolean => {
  return !!(word.has_authentic_audio && word.audio_filename);
};

/**
 * Obtient les informations audio d'un mot
 */
export const getWordAudioInfo = (word: WordWithAudio): {
  hasAuthentic: boolean;
  filename?: string;
  language?: string;
  source?: string;
} => {
  return {
    hasAuthentic: hasAuthenticAudioMetadata(word),
    filename: word.audio_filename,
    language: word.audio_pronunciation_lang,
    source: word.audio_source
  };
};