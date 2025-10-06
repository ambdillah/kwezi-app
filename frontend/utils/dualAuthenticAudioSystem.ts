/**
 * SYSTÈME AUDIO AUTHENTIQUE DUAL
 * ==============================
 * Gère les prononciations authentiques séparées pour Shimaoré et Kibouchi
 * Utilise la nouvelle structure de base de données restructurée
 */

import { Audio } from 'expo-av';
import { speakText } from './speechUtils';

export type AudioLanguage = 'fr' | 'shimaore' | 'kibouchi';

interface WordWithDualAudio {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  // Nouveau système dual - NOMS DE CHAMPS CORRECTS
  dual_audio_system?: boolean;
  audio_filename_shimaore?: string;  // Nom correct dans la base
  audio_filename_kibouchi?: string;  // Nom correct dans la base
  // Anciens champs pour compatibilité
  has_authentic_audio?: boolean;
  audio_filename?: string;
  audio_pronunciation_lang?: string;
}

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
      console.log('🔇 Audio dual arrêté');
    }
  } catch (error) {
    console.log('Erreur lors de l\'arrêt de l\'audio dual:', error);
  }
};

/**
 * Joue l'audio d'un mot dans une langue spécifique via la nouvelle API dual
 */
const playDualAudioFromAPI = async (
  wordId: string,
  language: 'shimaore' | 'kibouchi',
  onStart?: () => void,
  onComplete?: () => void
): Promise<boolean> => {
  try {
    const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';
    const audioUrl = `${backendUrl}/api/words/${wordId}/audio/${language}`;
    
    console.log(`🎵 Chargement audio dual via nouvelle API: ${language} pour mot ${wordId}`);
    console.log(`🔗 URL: ${audioUrl}`);
    
    // Arrêter l'audio précédent
    await stopCurrentAudio();
    
    // Configurer l'audio
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });
    
    // Charger et jouer l'audio via l'API dual
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
        console.log(`✅ Audio dual ${language} terminé`);
      }
    });
    
    return true;
    
  } catch (error) {
    console.log(`❌ Erreur lors de la lecture audio dual ${language}:`, error);
    return false;
  }
};

/**
 * Fonction principale pour jouer un mot avec le système dual
 */
export const playWordWithDualAudio = async (
  word: WordWithDualAudio,
  language: 'shimaore' | 'kibouchi',
  onStart?: () => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Vérifier si le mot utilise le nouveau système dual
    if (word.dual_audio_system && word.id) {
      // CORRECTION: Utiliser les bons noms de champs
      const hasAudioForLanguage = language === 'shimaore' 
        ? !!word.audio_filename_shimaore 
        : !!word.audio_filename_kibouchi;
      
      if (hasAudioForLanguage) {
        console.log(`🎯 UTILISATION SYSTÈME DUAL pour "${word.french}" en ${language}`);
        console.log(`   Fichier audio: ${language === 'shimaore' ? word.audio_filename_shimaore : word.audio_filename_kibouchi}`);
        
        const success = await playDualAudioFromAPI(
          word.id,
          language,
          onStart,
          onComplete
        );
        
        if (success) {
          console.log(`✅ AUDIO DUAL joué avec succès: ${word.french} (${language})`);
          return; // Audio dual joué avec succès
        }
        
        console.log(`⚠️ Audio dual ${language} échoué, utilisation de la synthèse vocale`);
      } else {
        console.log(`⚠️ Pas d'audio ${language} disponible pour ${word.french} dans le système dual`);
      }
    } else {
      // Fallback vers l'ancien système pour compatibilité
      console.log(`⚠️ Mot "${word.french}" n'utilise pas le système dual, utilisation de l'ancien système`);
      
      // Vérifier l'ancien système audio
      if (word.has_authentic_audio && word.audio_filename) {
        const shouldUseAuthentic = 
          word.audio_pronunciation_lang === 'both' ||
          word.audio_pronunciation_lang === language ||
          (word.audio_pronunciation_lang === 'shimaoré' && language === 'shimaore') ||
          (word.audio_pronunciation_lang === 'shimaore' && language === 'shimaore');

        if (shouldUseAuthentic) {
          console.log(`🎯 UTILISATION ANCIEN SYSTÈME pour "${word.french}" (${word.audio_filename})`);
          
          // Utiliser l'ancien système via l'API famille/nature
          const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';
          const audioUrl = `${backendUrl}/api/audio/${word.category}/${word.audio_filename}`;
          
          try {
            await stopCurrentAudio();
            
            await Audio.setAudioModeAsync({
              allowsRecordingIOS: false,
              playsInSilentModeIOS: true,
              staysActiveInBackground: false,
              shouldDuckAndroid: true,
            });
            
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
            
            sound.setOnPlaybackStatusUpdate((status) => {
              if (status.isLoaded && status.didJustFinish) {
                currentAudio.isPlaying = false;
                sound.unloadAsync();
                currentAudio.sound = null;
                onComplete?.();
                console.log('✅ Audio ancien système terminé');
              }
            });
            
            return; // Audio ancien système joué avec succès
            
          } catch (error) {
            console.log('❌ Ancien système audio échoué:', error);
          }
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
    console.log('Erreur générale dans playWordWithDualAudio:', error);
    
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
 * Vérifie si un mot a un enregistrement audio authentique dans une langue spécifique
 */
export const hasDualAudioForLanguage = (
  word: WordWithDualAudio, 
  language: 'shimaore' | 'kibouchi'
): boolean => {
  if (word.dual_audio_system) {
    return language === 'shimaore' 
      ? !!(word.shimoare_has_audio) 
      : !!(word.kibouchi_has_audio);
  }
  
  // Fallback vers l'ancien système
  if (word.has_authentic_audio && word.audio_filename) {
    const shouldUseAuthentic = 
      word.audio_pronunciation_lang === 'both' ||
      word.audio_pronunciation_lang === language ||
      (word.audio_pronunciation_lang === 'shimaoré' && language === 'shimaore') ||
      (word.audio_pronunciation_lang === 'shimaore' && language === 'shimaore');
    
    return shouldUseAuthentic;
  }
  
  return false;
};

/**
 * Vérifie si un mot a un enregistrement audio authentique (toutes langues confondues)
 */
export const hasDualAudio = (word: WordWithDualAudio): boolean => {
  if (word.dual_audio_system) {
    return !!(word.shimoare_has_audio || word.kibouchi_has_audio);
  }
  
  // Fallback vers l'ancien système
  return !!(word.has_authentic_audio && word.audio_filename);
};

/**
 * Obtient les informations audio détaillées d'un mot
 */
export const getDualAudioInfo = (word: WordWithDualAudio): {
  isDualSystem: boolean;
  shimaore: { hasAudio: boolean; filename?: string };
  kibouchi: { hasAudio: boolean; filename?: string };
  legacy: { hasAudio: boolean; filename?: string; language?: string };
} => {
  return {
    isDualSystem: !!(word.dual_audio_system),
    shimaore: {
      hasAudio: !!(word.shimoare_has_audio),
      filename: word.shimoare_audio_filename
    },
    kibouchi: {
      hasAudio: !!(word.kibouchi_has_audio),
      filename: word.kibouchi_audio_filename
    },
    legacy: {
      hasAudio: !!(word.has_authentic_audio),
      filename: word.audio_filename,
      language: word.audio_pronunciation_lang
    }
  };
};

/**
 * Récupère les informations audio d'un mot via l'API
 */
export const fetchWordAudioInfo = async (wordId: string): Promise<any> => {
  try {
    const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';
    const response = await fetch(`${backendUrl}/api/words/${wordId}/audio-info`);
    
    if (response.ok) {
      const audioInfo = await response.json();
      console.log(`📊 Info audio récupérée pour mot ${wordId}:`, audioInfo);
      return audioInfo;
    } else {
      console.log(`⚠️ Impossible de récupérer les infos audio pour mot ${wordId}`);
      return null;
    }
  } catch (error) {
    console.log(`❌ Erreur lors de la récupération des infos audio:`, error);
    return null;
  }
};

export default {
  playWordWithDualAudio,
  hasDualAudioForLanguage,
  hasDualAudio,
  getDualAudioInfo,
  fetchWordAudioInfo,
  stopCurrentAudio
};