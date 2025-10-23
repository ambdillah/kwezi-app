/**
 * Safe wrapper for expo-speech to handle APK compatibility issues
 * Prevents crashes when SyntheticPlatformEmitter is undefined in production builds
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

export const speak = async (text: string, options?: any): Promise<void> => {
  if (!speechAvailable || !Speech) {
    console.log('🔇 TTS not available, skipping speech');
    return;
  }
  
  try {
    await Speech.speak(text, options);
  } catch (error) {
    console.warn('⚠️ Speech.speak failed:', error);
  }
};

export const stop = async (): Promise<void> => {
  if (!speechAvailable || !Speech) return;
  
  try {
    await Speech.stop();
  } catch (error) {
    console.warn('⚠️ Speech.stop failed:', error);
  }
};

export const isSpeakingAsync = async (): Promise<boolean> => {
  if (!speechAvailable || !Speech) return false;
  
  try {
    return await Speech.isSpeakingAsync();
  } catch (error) {
    console.warn('⚠️ Speech.isSpeakingAsync failed:', error);
    return false;
  }
};

export const pause = async (): Promise<void> => {
  if (!speechAvailable || !Speech || !Speech.pause) return;
  
  try {
    await Speech.pause();
  } catch (error) {
    console.warn('⚠️ Speech.pause failed:', error);
  }
};

export const resume = async (): Promise<void> => {
  if (!speechAvailable || !Speech || !Speech.resume) return;
  
  try {
    await Speech.resume();
  } catch (error) {
    console.warn('⚠️ Speech.resume failed:', error);
  }
};

export default {
  speak,
  stop,
  isSpeakingAsync,
  pause,
  resume,
  get available() {
    return speechAvailable;
  }
};
