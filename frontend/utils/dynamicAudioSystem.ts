/**
 * SYSTÈME AUDIO DYNAMIQUE
 * ========================
 * Utilise les métadonnées de la base de données pour jouer
 * les enregistrements audio authentiques ou la synthèse vocale
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
 * Mapping des fichiers audio locaux
 * Ces fichiers sont maintenant stockés dans /assets/audio/famille/
 */
const LOCAL_AUDIO_FILES: { [key: string]: any } = {
  'Anabavi.m4a': require('../assets/audio/famille/Anabavi.m4a'),
  'Anadahi.m4a': require('../assets/audio/famille/Anadahi.m4a'),
  'Baba héli-bé.m4a': require('../assets/audio/famille/Baba héli-bé.m4a'),
  'Baba k.m4a': require('../assets/audio/famille/Baba k.m4a'),
  'Baba s.m4a': require('../assets/audio/famille/Baba s.m4a'),
  'Baba titi-bolé.m4a': require('../assets/audio/famille/Baba titi-bolé.m4a'),
  'Bacoco.m4a': require('../assets/audio/famille/Bacoco.m4a'),
  'Bweni.m4a': require('../assets/audio/famille/Bweni.m4a'),
  'Coco.m4a': require('../assets/audio/famille/Coco.m4a'),
  'Dadayi.m4a': require('../assets/audio/famille/Dadayi.m4a'),
  'Dadi.m4a': require('../assets/audio/famille/Dadi.m4a'),
  'Havagna.m4a': require('../assets/audio/famille/Havagna.m4a'),
  'Lalahi.m4a': require('../assets/audio/famille/Lalahi.m4a'),
  'Mama titi-bolé.m4a': require('../assets/audio/famille/Mama titi-bolé.m4a'),
  'Mama.m4a': require('../assets/audio/famille/Mama.m4a'),
  'Mdjamaza.m4a': require('../assets/audio/famille/Mdjamaza.m4a'),
  'Moina boueni.m4a': require('../assets/audio/famille/Moina boueni.m4a'),
  'Moina.m4a': require('../assets/audio/famille/Moina.m4a'),
  'Moinagna mtroubaba.m4a': require('../assets/audio/famille/Moinagna mtroubaba.m4a'),
  'Moinagna mtroumama.m4a': require('../assets/audio/famille/Moinagna mtroumama.m4a'),
  'Mongné.m4a': require('../assets/audio/famille/Mongné.m4a'),
  'Mtroubaba.m4a': require('../assets/audio/famille/Mtroubaba.m4a'),
  'Mtroumama.m4a': require('../assets/audio/famille/Mtroumama.m4a'),
  'Mwandzani.m4a': require('../assets/audio/famille/Mwandzani.m4a'),
  'Ninfndri héli-bé.m4a': require('../assets/audio/famille/Ninfndri héli-bé.m4a'),
  'Tseki lalahi.m4a': require('../assets/audio/famille/Tseki lalahi.m4a'),
  'Viavi.m4a': require('../assets/audio/famille/Viavi.m4a'),
  'Zama.m4a': require('../assets/audio/famille/Zama.m4a'),
  'Zena.m4a': require('../assets/audio/famille/Zena.m4a'),
  'Zoki lalahi.m4a': require('../assets/audio/famille/Zoki lalahi.m4a'),
  'Zoki viavi.m4a': require('../assets/audio/famille/Zoki viavi.m4a'),
  'Zouki mtroubaba.m4a': require('../assets/audio/famille/Zouki mtroubaba.m4a'),
  'Zouki mtroumché.m4a': require('../assets/audio/famille/Zouki mtroumché.m4a'),
  'Zouki.m4a': require('../assets/audio/famille/Zouki.m4a'),
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
 * Joue un enregistrement audio authentique local
 */
export const playLocalAuthenticAudio = async (
  audioFilename: string,
  onStart?: () => void,
  onComplete?: () => void
): Promise<boolean> => {
  try {
    // Vérifier si le fichier existe
    const audioAsset = LOCAL_AUDIO_FILES[audioFilename];
    if (!audioAsset) {
      console.log(`⚠️ Fichier audio non trouvé: ${audioFilename}`);
      return false;
    }

    // Arrêter l'audio précédent
    await stopCurrentAudio();
    
    console.log(`🎵 Chargement audio authentique local: ${audioFilename}`);
    
    // Configurer l'audio
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });
    
    // Charger et jouer l'audio
    const { sound } = await Audio.Sound.createAsync(
      audioAsset,
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
    return false;
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
  return !!(word.has_authentic_audio && word.audio_filename && LOCAL_AUDIO_FILES[word.audio_filename]);
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