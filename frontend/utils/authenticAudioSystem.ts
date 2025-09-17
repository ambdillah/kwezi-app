/**
 * SYSTÈME AUDIO AUTHENTIQUE
 * =========================
 * Utilise les enregistrements audio authentiques de l'utilisateur
 * en priorité, avec fallback vers la synthèse vocale
 */

import { Audio } from 'expo-av';
import { speakText } from './speechUtils';

export type AudioLanguage = 'fr' | 'shimaore' | 'kibouchi';

/**
 * Mapping des mots vers leurs enregistrements audio authentiques
 */
const AUTHENTIC_AUDIO_MAPPING = {
  // Papa
  'Papa': {
    shimaore: 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/cr57ryqz_Baba%20s.m4a',
    kibouchi: 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/qdc3kyos_Baba%20k.m4a'
  },
  // Frère
  'Frère': {
    kibouchi: 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/5ppmqe8p_Anadahi.m4a'
  },
  // Sœur
  'Sœur': {
    kibouchi: 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/f5qkf8pn_Anabavi.m4a'
  },
  // Variante famille (à identifier)
  'Baba héli': {
    kibouchi: 'https://customer-assets.emergentagent.com/job_4a14c8f2-84cf-4ceb-96bb-f2064afeeb42/artifacts/hg2eeidx_Baba%20h%C3%A9li-b%C3%A9.m4a'
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
 * Joue un enregistrement audio authentique
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
 * Fonction principale pour jouer un mot avec audio authentique ou synthèse vocale
 */
export const playWordAudio = async (
  frenchWord: string,
  translatedWord: string,
  language: AudioLanguage,
  onStart?: () => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Vérifier s'il existe un audio authentique pour ce mot
    const audioMapping = AUTHENTIC_AUDIO_MAPPING[frenchWord as keyof typeof AUTHENTIC_AUDIO_MAPPING];
    
    if (audioMapping && audioMapping[language]) {
      console.log(`🎯 Audio authentique trouvé pour "${frenchWord}" en ${language}`);
      
      const success = await playAuthenticAudio(
        audioMapping[language]!,
        onStart,
        onComplete
      );
      
      if (success) {
        return; // Audio authentique joué avec succès
      }
    }
    
    // Fallback vers la synthèse vocale
    console.log(`🔊 Utilisation de la synthèse vocale pour "${translatedWord}" en ${language}`);
    
    onStart?.();
    await speakText(translatedWord, language);
    onComplete?.();
    
  } catch (error) {
    console.log('Erreur générale dans playWordAudio:', error);
    
    // Dernier fallback : synthèse vocale simple
    try {
      await speakText(translatedWord, language);
    } catch (fallbackError) {
      console.log('Erreur fallback:', fallbackError);
    }
  }
};

/**
 * Fonction pour jouer un mot dans toutes les langues disponibles
 */
export const playWordAllLanguages = async (
  word: {
    french: string;
    shimaore: string;
    kibouchi: string;
  },
  onLanguageStart?: (language: AudioLanguage) => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Français
    onLanguageStart?.('fr');
    await new Promise<void>((resolve) => {
      playWordAudio(word.french, word.french, 'fr', undefined, resolve);
    });
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Shimaoré
    onLanguageStart?.('shimaore');
    await new Promise<void>((resolve) => {
      playWordAudio(word.french, word.shimaore, 'shimaore', undefined, resolve);
    });
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Kibouchi
    onLanguageStart?.('kibouchi');
    await new Promise<void>((resolve) => {
      playWordAudio(word.french, word.kibouchi, 'kibouchi', undefined, resolve);
    });
    
    onComplete?.();
    
  } catch (error) {
    console.log('Erreur lors de la lecture dans toutes les langues:', error);
  }
};

/**
 * Vérifie si un mot a un enregistrement audio authentique
 */
export const hasAuthenticAudio = (frenchWord: string, language: AudioLanguage): boolean => {
  const audioMapping = AUTHENTIC_AUDIO_MAPPING[frenchWord as keyof typeof AUTHENTIC_AUDIO_MAPPING];
  return !!(audioMapping && audioMapping[language]);
};

/**
 * Obtient la liste des mots avec audio authentique
 */
export const getWordsWithAuthenticAudio = (): Array<{
  french: string;
  languages: AudioLanguage[];
}> => {
  return Object.entries(AUTHENTIC_AUDIO_MAPPING).map(([frenchWord, mapping]) => ({
    french: frenchWord,
    languages: Object.keys(mapping) as AudioLanguage[]
  }));
};