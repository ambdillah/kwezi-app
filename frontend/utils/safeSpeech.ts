/**
 * Safe wrapper for expo-speech to handle APK compatibility issues
 * Prevents crashes when SyntheticPlatformEmitter is undefined in production builds
 * SOLUTION: Import synchrone mais avec try-catch pour gérer les erreurs
 */

import { Platform } from 'react-native';

let Speech: any = null;
let speechAvailable = false;

// Essayer d'importer expo-speech de manière synchrone
try {
  // Sur web, ne pas charger expo-speech du tout pour éviter l'erreur
  if (Platform.OS !== 'web') {
    Speech = require('expo-speech');
    speechAvailable = true;
    console.log('✅ expo-speech loaded successfully');
  } else {
    console.log('🌐 Web platform: expo-speech désactivé (pas nécessaire)');
    speechAvailable = false;
  }
} catch (error) {
  console.warn('⚠️ expo-speech not available (APK compatibility issue):', error);
  speechAvailable = false;
  Speech = null;
}

export const speak = async (text: string, options?: any): Promise<void> => {
  if (!speechAvailable || !Speech) {
    console.log('🔇 TTS not available, skipping speech');
    return;
  }
  
  try {
    if (Speech.speak) {
      Speech.speak(text, options);
    }
  } catch (error) {
    console.warn('⚠️ Speech.speak failed:', error);
  }
};

export const stop = async (): Promise<void> => {
  if (!speechAvailable || !Speech) return;
  
  try {
    if (Speech.stop) {
      Speech.stop();
    }
  } catch (error) {
    console.warn('⚠️ Speech.stop failed:', error);
  }
};

export const isSpeakingAsync = async (): Promise<boolean> => {
  if (!speechAvailable || !Speech) return false;
  
  try {
    if (Speech.isSpeakingAsync) {
      return await Speech.isSpeakingAsync();
    }
    return false;
  } catch (error) {
    console.warn('⚠️ Speech.isSpeakingAsync failed:', error);
    return false;
  }
};

export const pause = async (): Promise<void> => {
  if (!speechAvailable || !Speech || !Speech.pause) return;
  
  try {
    Speech.pause();
  } catch (error) {
    console.warn('⚠️ Speech.pause failed:', error);
  }
};

export const resume = async (): Promise<void> => {
  if (!speechAvailable || !Speech || !Speech.resume) return;
  
  try {
    Speech.resume();
  } catch (error) {
    console.warn('⚠️ Speech.resume failed:', error);
  }
};

export const getAvailableVoicesAsync = async (): Promise<any[]> => {
  if (!speechAvailable || !Speech || !Speech.getAvailableVoicesAsync) {
    return [];
  }
  
  try {
    return await Speech.getAvailableVoicesAsync();
  } catch (error) {
    console.warn('⚠️ Speech.getAvailableVoicesAsync failed:', error);
    return [];
  }
};

export default {
  speak,
  stop,
  isSpeakingAsync,
  pause,
  resume,
  getAvailableVoicesAsync,
  get available() {
    return speechAvailable;
  }
};
