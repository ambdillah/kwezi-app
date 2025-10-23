/**
 * Safe wrapper for expo-speech to handle APK compatibility issues
 * Prevents crashes when SyntheticPlatformEmitter is undefined in production builds
<<<<<<< HEAD
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
=======
 */

let Speech: any = null;
let speechAvailable = false;

// Try to import expo-speech safely
(async () => {
  try {
    const module = await import('expo-speech');
    Speech = module;
    speechAvailable = true;
  } catch (error) {
    console.warn('⚠️ expo-speech not available (APK compatibility issue):', error);
    speechAvailable = false;
  }
})();
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1

export const speak = async (text: string, options?: any): Promise<void> => {
  if (!speechAvailable || !Speech) {
    console.log('🔇 TTS not available, skipping speech');
    return;
  }
  
  try {
<<<<<<< HEAD
    if (Speech.speak) {
      Speech.speak(text, options);
    }
=======
    await Speech.speak(text, options);
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
  } catch (error) {
    console.warn('⚠️ Speech.speak failed:', error);
  }
};

export const stop = async (): Promise<void> => {
  if (!speechAvailable || !Speech) return;
  
  try {
<<<<<<< HEAD
    if (Speech.stop) {
      Speech.stop();
    }
=======
    await Speech.stop();
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
  } catch (error) {
    console.warn('⚠️ Speech.stop failed:', error);
  }
};

export const isSpeakingAsync = async (): Promise<boolean> => {
  if (!speechAvailable || !Speech) return false;
  
  try {
<<<<<<< HEAD
    if (Speech.isSpeakingAsync) {
      return await Speech.isSpeakingAsync();
    }
    return false;
=======
    return await Speech.isSpeakingAsync();
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
  } catch (error) {
    console.warn('⚠️ Speech.isSpeakingAsync failed:', error);
    return false;
  }
};

export const pause = async (): Promise<void> => {
  if (!speechAvailable || !Speech || !Speech.pause) return;
  
  try {
<<<<<<< HEAD
    Speech.pause();
=======
    await Speech.pause();
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
  } catch (error) {
    console.warn('⚠️ Speech.pause failed:', error);
  }
};

export const resume = async (): Promise<void> => {
  if (!speechAvailable || !Speech || !Speech.resume) return;
  
  try {
<<<<<<< HEAD
    Speech.resume();
=======
    await Speech.resume();
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
  } catch (error) {
    console.warn('⚠️ Speech.resume failed:', error);
  }
};

<<<<<<< HEAD
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

=======
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
export default {
  speak,
  stop,
  isSpeakingAsync,
  pause,
  resume,
<<<<<<< HEAD
  getAvailableVoicesAsync,
=======
>>>>>>> b00cc3a19d9a27378afe7d74435dadbd4b2e0ad1
  get available() {
    return speechAvailable;
  }
};
