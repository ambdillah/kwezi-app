/**
 * Safe wrapper for expo-speech to handle APK compatibility issues
 * Prevents crashes when SyntheticPlatformEmitter is undefined in production builds
 */

let Speech: any = null;
let speechAvailable: boolean | null = null;
let initPromise: Promise<void> | null = null;

// Lazy initialization of expo-speech
const initSpeech = async (): Promise<void> => {
  if (speechAvailable !== null) return; // Already initialized
  
  if (initPromise) return initPromise; // Initialization in progress
  
  initPromise = (async () => {
    try {
      Speech = await import('expo-speech');
      speechAvailable = true;
      console.log('✅ expo-speech loaded successfully');
    } catch (error) {
      console.warn('⚠️ expo-speech not available (APK compatibility issue):', error);
      speechAvailable = false;
      Speech = null;
    }
  })();
  
  return initPromise;
};

export const speak = async (text: string, options?: any): Promise<void> => {
  await initSpeech();
  
  if (!speechAvailable || !Speech) {
    console.log('🔇 TTS not available, skipping speech');
    return;
  }
  
  try {
    if (Speech.speak) {
      await Speech.speak(text, options);
    }
  } catch (error) {
    console.warn('⚠️ Speech.speak failed:', error);
  }
};

export const stop = async (): Promise<void> => {
  await initSpeech();
  
  if (!speechAvailable || !Speech) return;
  
  try {
    if (Speech.stop) {
      await Speech.stop();
    }
  } catch (error) {
    console.warn('⚠️ Speech.stop failed:', error);
  }
};

export const isSpeakingAsync = async (): Promise<boolean> => {
  await initSpeech();
  
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
  await initSpeech();
  
  if (!speechAvailable || !Speech || !Speech.pause) return;
  
  try {
    await Speech.pause();
  } catch (error) {
    console.warn('⚠️ Speech.pause failed:', error);
  }
};

export const resume = async (): Promise<void> => {
  await initSpeech();
  
  if (!speechAvailable || !Speech || !Speech.resume) return;
  
  try {
    await Speech.resume();
  } catch (error) {
    console.warn('⚠️ Speech.resume failed:', error);
  }
};

export const getAvailableVoicesAsync = async (): Promise<any[]> => {
  await initSpeech();
  
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
    return speechAvailable === true;
  }
};
