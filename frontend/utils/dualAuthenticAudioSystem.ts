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
  // Système dual - DEUX formats possibles
  dual_audio_system?: boolean;
  // Format 1 (nouveaux verbes/expressions)
  audio_filename_shimaore?: string;
  audio_filename_kibouchi?: string;
  // Format 2 (anciennes catégories)
  shimoare_audio_filename?: string;
  kibouchi_audio_filename?: string;
  shimoare_has_audio?: boolean;
  kibouchi_has_audio?: boolean;
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
    // CORRECTION CRITIQUE: Utiliser assets locaux au lieu de l'API backend
    // Les fichiers audio sont bundlés dans /assets/audio/
    const audioPath = language === 'shimaore' ? word.audio_shimaore : word.audio_kibouchi;
    
    if (!audioPath) {
      console.log(`⚠️ Pas de fichier audio pour ${language}`);
      return false;
    }
    
    // Construire le chemin asset complet avec Asset.fromModule
    // audioPath est comme "animaux/Papa.m4a"
    const fullPath = `../../assets/audio/${audioPath}`;
    
    console.log(`🎵 Chargement audio local: ${language} - ${audioPath}`);
    console.log(`🔗 Asset path: ${fullPath}`);
    
    // Arrêter l'audio précédent
    await stopCurrentAudio();
    
    // Configurer l'audio
    await Audio.setAudioModeAsync({
      allowsRecordingIOS: false,
      playsInSilentModeIOS: true,
      staysActiveInBackground: false,
      shouldDuckAndroid: true,
    });
    
    // CORRECTION CRITIQUE: Attendre la fin de l'audio avec une Promise
    return new Promise<boolean>((resolve) => {
      let timeoutId: NodeJS.Timeout;
      
      // Charger et jouer l'audio via l'API dual
      Audio.Sound.createAsync(
        { uri: audioUrl },
        { 
          shouldPlay: true,
          volume: 1.0,
          isLooping: false 
        }
      ).then(({ sound }) => {
        currentAudio.sound = sound;
        currentAudio.isPlaying = true;
        
        onStart?.();
        
        // Écouter la fin de la lecture
        sound.setOnPlaybackStatusUpdate((status) => {
          if (status.isLoaded && status.didJustFinish) {
            // CORRECTION: Nettoyer le timeout avant de résoudre
            if (timeoutId) {
              clearTimeout(timeoutId);
            }
            
            currentAudio.isPlaying = false;
            sound.unloadAsync();
            currentAudio.sound = null;
            onComplete?.();
            console.log(`✅ Audio dual ${language} terminé naturellement`);
            resolve(true);
          }
        });
        
        // Timeout de sécurité étendu (30 secondes au lieu de 10)
        // Ne s'active QUE si l'audio ne se termine pas naturellement
        timeoutId = setTimeout(() => {
          if (currentAudio.isPlaying) {
            console.log(`⚠️ Timeout audio ${language} après 30s, arrêt de sécurité`);
            stopCurrentAudio().then(() => {
              resolve(false); // false car timeout = problème
            });
          }
        }, 30000);
        
      }).catch((error) => {
        console.log(`❌ Erreur lors du chargement audio dual ${language}:`, error);
        resolve(false);
      });
    });
    
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
    // CORRECTION CRITIQUE: Arrêter TOUTE synthèse vocale en cours AVANT de jouer un audio authentique
    try {
      const Speech = await import('./safeSpeech');
      if (Speech && Speech.isSpeakingAsync) {
        const isSpeaking = await Speech.isSpeakingAsync();
        if (isSpeaking) {
          console.log('🛑 Arrêt de la synthèse vocale en cours avant audio authentique');
          await Speech.stop();
        }
      }
    } catch (error) {
      // Ignorer les erreurs expo-speech (incompatibilité APK)
      console.log('Note: Impossible de vérifier/arrêter la synthèse vocale:', error);
    }
    
    // PRIORITÉ 1: Vérifier le système dual (DEUX formats possibles)
    if (word.dual_audio_system && word.id) {
      // Vérifier les DEUX formats de nommage possibles
      const hasAudioForLanguage = language === 'shimaore' 
        ? !!(word.audio_filename_shimaore || word.shimoare_audio_filename)
        : !!(word.audio_filename_kibouchi || word.kibouchi_audio_filename);
      
      if (hasAudioForLanguage) {
        console.log(`🎯 SYSTÈME DUAL pour "${word.french}" en ${language}`);
        console.log(`   Fichier: ${language === 'shimaore' ? word.audio_filename_shimaore : word.audio_filename_kibouchi}`);
        
        const success = await playDualAudioFromAPI(
          word.id,
          language,
          onStart,
          onComplete
        );
        
        if (success) {
          console.log(`✅ AUDIO DUAL joué: ${word.french} (${language})`);
          return; // RETOUR IMMÉDIAT - PAS DE SYNTHÈSE
        }
        
        console.log(`⚠️ Audio dual échoué, essai ancien système...`);
      }
    }
    
    // PRIORITÉ 2: Essayer l'ancien système audio (audio_filename)
    if (word.has_authentic_audio && word.audio_filename) {
      console.log(`🎯 ANCIEN SYSTÈME pour "${word.french}" (${word.audio_filename})`);
      console.log(`   audio_pronunciation_lang: ${word.audio_pronunciation_lang}`);
      
      // CORRECTION: Accepter "dual_system" pour les anciens audios
      const shouldUseAuthentic = 
        word.audio_pronunciation_lang === 'both' ||
        word.audio_pronunciation_lang === 'dual_system' ||
        word.audio_pronunciation_lang === language ||
        (word.audio_pronunciation_lang === 'shimaoré' && language === 'shimaore') ||
        (word.audio_pronunciation_lang === 'shimaore' && language === 'shimaore');

      if (shouldUseAuthentic) {
        console.log(`   URL: /api/audio/${word.category}/${word.audio_filename}`);
        
        // Utiliser l'ancien système via l'API catégorie
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
    
    // Fallback vers la synthèse vocale UNIQUEMENT si AUCUN audio authentique n'existe
    const hasAnyAudio = word.dual_audio_system && (
      word.audio_filename_shimaore || 
      word.shimoare_audio_filename || 
      word.audio_filename_kibouchi || 
      word.kibouchi_audio_filename ||
      word.has_authentic_audio
    );
    
    if (!hasAnyAudio) {
      // Seulement si vraiment AUCUN audio authentique n'existe
      const textToSpeak = language === 'shimaore' ? word.shimaore : word.kibouchi;
      console.log(`🔊 Pas d'audio authentique, synthèse vocale pour "${textToSpeak}" en ${language}`);
      
      onStart?.();
      await speakText(textToSpeak, language);
      onComplete?.();
    } else {
      // Audio authentique existe mais a échoué - NE PAS utiliser la synthèse
      console.log(`⚠️ Audio authentique existe pour "${word.french}" mais échec de lecture - Pas de fallback synthèse`);
      onComplete?.(); // Appeler onComplete quand même pour débloquer l'UI
    }
    
  } catch (error) {
    console.log('Erreur générale dans playWordWithDualAudio:', error);
    
    // PAS de dernier fallback automatique vers synthèse si audio authentique existe
    const hasAnyAudio = word.dual_audio_system && (
      word.audio_filename_shimaore || 
      word.shimoare_audio_filename || 
      word.audio_filename_kibouchi || 
      word.kibouchi_audio_filename ||
      word.has_authentic_audio
    );
    
    if (!hasAnyAudio) {
      // Seulement si vraiment AUCUN audio
      try {
        const textToSpeak = language === 'shimaore' ? word.shimaore : word.kibouchi;
        await speakText(textToSpeak, language);
      } catch (fallbackError) {
        console.log('Erreur fallback synthèse:', fallbackError);
      }
    } else {
      console.log(`⚠️ Échec lecture mais audio authentique existe - Pas de synthèse de remplacement`);
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
    // Gérer les DEUX formats de nommage
    return language === 'shimaore' 
      ? !!(word.audio_filename_shimaore || word.shimoare_audio_filename)
      : !!(word.audio_filename_kibouchi || word.kibouchi_audio_filename);
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
    // Gérer les DEUX formats de nommage
    return !!(
      word.audio_filename_shimaore || 
      word.audio_filename_kibouchi || 
      word.shimoare_audio_filename || 
      word.kibouchi_audio_filename
    );
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
      hasAudio: !!(word.audio_filename_shimaore || word.shimoare_audio_filename),
      filename: word.audio_filename_shimaore || word.shimoare_audio_filename
    },
    kibouchi: {
      hasAudio: !!(word.audio_filename_kibouchi || word.kibouchi_audio_filename),
      filename: word.audio_filename_kibouchi || word.kibouchi_audio_filename
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