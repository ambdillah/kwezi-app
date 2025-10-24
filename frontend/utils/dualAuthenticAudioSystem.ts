/**
 * SYSTÈME AUDIO AUTHENTIQUE DUAL - SHIMAORÉ ET KIBOUCHI
 * VERSION SIMPLIFIÉE APK-COMPATIBLE
 * ==============================
 * Tente audio authentique, fallback TTS si échec
 */

import { Audio } from 'expo-av';
import Constants from 'expo-constants';
import { speakText } from './safeSpeech';

export type AudioLanguage = 'fr' | 'shimaore' | 'kibouchi';

interface WordWithDualAudio {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  dual_audio_system?: boolean;
  audio_shimaore?: string;
  audio_kibouchi?: string;
  audio_filename_shimaore?: string;
  audio_filename_kibouchi?: string;
  shimoare_audio_filename?: string;
  kibouchi_audio_filename?: string;
  shimoare_has_audio?: boolean;
  kibouchi_has_audio?: boolean;
  has_authentic_audio?: boolean;
  audio_filename?: string;
  audio_pronunciation_lang?: string;
}

/**
 * Joue l'audio d'un mot dans une langue spécifique
 * SIMPLIFIÉ: Tente expo-av, fallback immédiat vers TTS
 */
const playAudioSimple = async (
  audioUrl: string,
  fallbackText: string,
  language: 'shimaore' | 'kibouchi'
): Promise<boolean> => {
  console.log(`🎵 Lecture audio: ${audioUrl}`);
  
  // TENTATIVE 1: Audio authentique via expo-av
  try {
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      shouldDuckAndroid: true,
    });
    
    const { sound } = await Audio.Sound.createAsync(
      { uri: audioUrl },
      { shouldPlay: true, volume: 1.0 }
    );
    
    console.log(`✅ Audio authentique joué`);
    
    // Attendre la fin
    await new Promise<void>((resolve) => {
      sound.setOnPlaybackStatusUpdate((status) => {
        if ('didJustFinish' in status && status.didJustFinish) {
          sound.unloadAsync();
          resolve();
        }
      });
      
      // Timeout 30s
      setTimeout(() => {
        sound.unloadAsync();
        resolve();
      }, 30000);
    });
    
    return true;
  } catch (error) {
    console.log(`⚠️ Audio authentique échoué, fallback TTS`);
    
    // TENTATIVE 2: Synthèse vocale
    try {
      await speakText(fallbackText, language);
      console.log(`✅ TTS joué: ${fallbackText}`);
      return true;
    } catch (ttsError) {
      console.error(`❌ TTS échoué:`, ttsError);
      return false;
    }
  }
};

/**
 * Joue le mot avec audio dual (Shimaoré ou Kibouchi)
 */
export const playWordWithDualAudio = async (
  word: WordWithDualAudio,
  language: AudioLanguage,
  onStart?: () => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    console.log(`🎯 playWordWithDualAudio: "${word.french}" en ${language}`);
    
    onStart?.();
    
    // FRANÇAIS: Synthèse vocale uniquement
    if (language === 'fr') {
      await speakText(word.french, 'fr');
      onComplete?.();
      return;
    }
    
    // SHIMAORÉ/KIBOUCHI: Audio authentique ou TTS
    const audioPath = language === 'shimaore' ? word.audio_shimaore : word.audio_kibouchi;
    const fallbackText = language === 'shimaore' ? word.shimaore : word.kibouchi;
    
    if (audioPath && word.id) {
      const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
      const audioUrl = `${backendUrl}/api/words/${word.id}/audio/${language}`;
      
      await playAudioSimple(audioUrl, fallbackText, language);
    } else {
      // Pas d'audio authentique, TTS direct
      console.log(`🔊 Pas d'audio authentique, TTS: ${fallbackText}`);
      await speakText(fallbackText, language);
    }
    
    onComplete?.();
  } catch (error) {
    console.error(`❌ Erreur playWordWithDualAudio:`, error);
    onComplete?.();
  }
};

/**
 * Vérifie si un mot a un audio authentique
 */
export const hasDualAudioForLanguage = (
  word: WordWithDualAudio,
  language: 'shimaore' | 'kibouchi'
): boolean => {
  if (word.dual_audio_system) {
    return language === 'shimaore'
      ? !!(word.audio_shimaore || word.audio_filename_shimaore || word.shimoare_audio_filename)
      : !!(word.audio_kibouchi || word.audio_filename_kibouchi || word.kibouchi_audio_filename);
  }
  return false;
};

export const hasDualAudio = (word: WordWithDualAudio): boolean => {
  return !!(
    word.audio_shimaore ||
    word.audio_kibouchi ||
    word.audio_filename_shimaore ||
    word.audio_filename_kibouchi ||
    word.shimoare_audio_filename ||
    word.kibouchi_audio_filename
  );
};

export const getDualAudioInfo = (word: WordWithDualAudio) => {
  return {
    isDualSystem: !!(word.dual_audio_system),
    shimaore: {
      hasAudio: !!(word.audio_shimaore || word.audio_filename_shimaore || word.shimoare_audio_filename),
      filename: word.audio_shimaore || word.audio_filename_shimaore || word.shimoare_audio_filename
    },
    kibouchi: {
      hasAudio: !!(word.audio_kibouchi || word.audio_filename_kibouchi || word.kibouchi_audio_filename),
      filename: word.audio_kibouchi || word.audio_filename_kibouchi || word.kibouchi_audio_filename
    },
    legacy: {
      hasAudio: !!(word.has_authentic_audio),
      filename: word.audio_filename,
      language: word.audio_pronunciation_lang
    }
  };
};
