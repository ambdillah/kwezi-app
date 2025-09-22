/**
 * SYSTÈME AUDIO DYNAMIQUE - VERSION CORRIGÉE
 * ============================================
 * Utilise l'ancien système audio fonctionnel avec les nouvelles métadonnées
 */

import { Audio } from 'expo-av';
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
 * Mapping vers l'ancien système audio qui fonctionne
 * Utilise les URLs distantes de l'ancien système qui fonctionnaient
 */
const FAMILLE_AUDIO_MAPPING: { [key: string]: { [key: string]: string } } = {
  'papa': {
    'shimaore': 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/cr57ryqz_Baba%20s.m4a',
    'kibouchi': 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/qdc3kyos_Baba%20k.m4a'
  },
  'frère': {
    'kibouchi': 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/5ppmqe8p_Anadahi.m4a'
  },
  'sœur': {
    'kibouchi': 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/f5qkf8pn_Anabavi.m4a'
  },
  'grand-père': {
    'shimaore': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/vk9s6gu0_Bacoco.m4a',
    'kibouchi': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/k0uxar3d_Dadayi.m4a'
  },
  'grand-mère': {
    'shimaore': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/9kkagt8k_Coco.m4a',
    'kibouchi': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/8zi55srs_Dadi.m4a'
  },
  'madame': {
    'shimaore': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/1q9481sa_Bweni.m4a'
  },
  'famille': {
    'kibouchi': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/rtg5n6mp_Havagna.m4a'
  },
  'homme': {
    'kibouchi': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/cc6ge3l3_Lalahi.m4a'
  },
  'monsieur': {
    'kibouchi': 'https://customer-assets.emergentagent.com/job_c7e31f8c-473e-4b2f-bab2-dc500a14de15/artifacts/cc6ge3l3_Lalahi.m4a'
  }
};

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
 * Joue un enregistrement audio authentique depuis une URL
 */
export const playAuthenticAudio = async (
  audioUrl: string,
  onStart?: () => void,
  onComplete?: () => void
): Promise<boolean> => {
  try {
    // Arrêter l'audio précédent
    await stopCurrentAudio();
    
    console.log(`🎵 Chargement audio authentique: ${audioUrl}`);
    
    // Configurer l'audio
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });
    
    // Charger et jouer l'audio
    const { sound } = await Audio.Sound.createAsync(
      { uri: audioUrl },
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
        console.log('✅ Audio authentique terminé');
      }
    });
    
    return true;
    
  } catch (error) {
    console.log('❌ Erreur lors de la lecture de l\'audio authentique:', error);
    return false;
  }
};

/**
 * Fonction principale pour jouer un mot avec les métadonnées
 */
export const playWordWithMetadata = async (
  word: WordWithAudio,
  language: 'shimaore' | 'kibouchi',
  onStart?: () => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Vérifier d'abord l'ancien système qui fonctionne
    const audioMapping = FAMILLE_AUDIO_MAPPING[word.french.toLowerCase()];
    
    if (audioMapping && audioMapping[language]) {
      console.log(`🎯 Audio authentique trouvé (ancien système) pour "${word.french}" en ${language}`);
      
      const success = await playAuthenticAudio(
        audioMapping[language],
        onStart,
        onComplete
      );
      
      if (success) {
        return; // Audio authentique joué avec succès
      }
    }
    
    // Vérifier le nouveau système avec métadonnées
    if (word.has_authentic_audio && word.audio_filename) {
      const shouldUseAuthentic = 
        word.audio_pronunciation_lang === 'both' ||
        word.audio_pronunciation_lang === language ||
        (word.audio_pronunciation_lang === 'shimaoré' && language === 'shimaore') ||
        (word.audio_pronunciation_lang === 'shimaore' && language === 'shimaore');

      if (shouldUseAuthentic) {
        console.log(`🎯 Audio authentique trouvé (nouveau système) pour "${word.french}" (${word.audio_filename})`);
        
        // Pour le moment, utiliser fallback TTS car les fichiers locaux ne fonctionnent pas encore
        console.log('⚠️ Fichiers locaux pas encore supportés, utilisation TTS');
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
  // Vérifier l'ancien système d'abord
  const audioMapping = FAMILLE_AUDIO_MAPPING[word.french.toLowerCase()];
  if (audioMapping && (audioMapping['shimaore'] || audioMapping['kibouchi'])) {
    return true;
  }
  
  // Vérifier le nouveau système
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