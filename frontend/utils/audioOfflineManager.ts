/**
 * GESTIONNAIRE AUDIO OFFLINE POUR MODE PREMIUM
 * ============================================
 * Télécharge et cache les fichiers audio pour utilisation offline
 */

import * as FileSystem from 'expo-file-system';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

const AUDIO_CACHE_KEY = 'kwezi_audio_cache';
const AUDIO_CACHE_DIR = `${FileSystem.documentDirectory}audio_cache/`;

interface CachedAudio {
  wordId: string;
  language: 'shimaore' | 'kibouchi';
  localUri: string;
  downloadedAt: number;
}

interface AudioCacheIndex {
  [key: string]: CachedAudio;
}

/**
 * Initialiser le système de cache
 */
export const initializeAudioCache = async (): Promise<void> => {
  try {
    // Créer le dossier de cache s'il n'existe pas
    const dirInfo = await FileSystem.getInfoAsync(AUDIO_CACHE_DIR);
    if (!dirInfo.exists) {
      await FileSystem.makeDirectoryAsync(AUDIO_CACHE_DIR, { intermediates: true });
      console.log('📁 Dossier cache audio créé');
    }
  } catch (error) {
    console.error('❌ Erreur initialisation cache audio:', error);
  }
};

/**
 * Récupérer l'index du cache
 */
const getCacheIndex = async (): Promise<AudioCacheIndex> => {
  try {
    const indexStr = await AsyncStorage.getItem(AUDIO_CACHE_KEY);
    return indexStr ? JSON.parse(indexStr) : {};
  } catch (error) {
    console.error('❌ Erreur lecture index cache:', error);
    return {};
  }
};

/**
 * Sauvegarder l'index du cache
 */
const saveCacheIndex = async (index: AudioCacheIndex): Promise<void> => {
  try {
    await AsyncStorage.setItem(AUDIO_CACHE_KEY, JSON.stringify(index));
  } catch (error) {
    console.error('❌ Erreur sauvegarde index cache:', error);
  }
};

/**
 * Générer une clé unique pour un audio
 */
const getAudioKey = (wordId: string, language: 'shimaore' | 'kibouchi'): string => {
  return `${wordId}_${language}`;
};

/**
 * Vérifier si un audio est déjà en cache
 */
export const isAudioCached = async (
  wordId: string,
  language: 'shimaore' | 'kibouchi'
): Promise<boolean> => {
  try {
    const index = await getCacheIndex();
    const key = getAudioKey(wordId, language);
    const cached = index[key];
    
    if (!cached) return false;
    
    // Vérifier que le fichier existe toujours
    const fileInfo = await FileSystem.getInfoAsync(cached.localUri);
    return fileInfo.exists;
  } catch (error) {
    return false;
  }
};

/**
 * Récupérer l'URI local d'un audio en cache
 */
export const getCachedAudioUri = async (
  wordId: string,
  language: 'shimaore' | 'kibouchi'
): Promise<string | null> => {
  try {
    const index = await getCacheIndex();
    const key = getAudioKey(wordId, language);
    const cached = index[key];
    
    if (!cached) return null;
    
    // Vérifier que le fichier existe
    const fileInfo = await FileSystem.getInfoAsync(cached.localUri);
    if (!fileInfo.exists) {
      // Nettoyer l'index si le fichier n'existe plus
      delete index[key];
      await saveCacheIndex(index);
      return null;
    }
    
    return cached.localUri;
  } catch (error) {
    console.error('❌ Erreur récupération audio cache:', error);
    return null;
  }
};

/**
 * Télécharger et cacher un audio
 */
export const downloadAndCacheAudio = async (
  wordId: string,
  language: 'shimaore' | 'kibouchi',
  audioPath: string
): Promise<string | null> => {
  try {
    const backendUrl = Constants.expoConfig?.extra?.backendUrl || 'https://kwezi-backend.onrender.com';
    const audioUrl = `${backendUrl}/api/words/${wordId}/audio/${language}`;
    
    // Nom du fichier local
    const fileName = audioPath.replace(/\//g, '_'); // Remplacer / par _
    const localUri = `${AUDIO_CACHE_DIR}${fileName}`;
    
    console.log(`⬇️ Téléchargement audio: ${audioPath}`);
    console.log(`📥 Depuis: ${audioUrl}`);
    console.log(`💾 Vers: ${localUri}`);
    
    // Télécharger le fichier
    const downloadResult = await FileSystem.downloadAsync(audioUrl, localUri);
    
    if (downloadResult.status === 200) {
      // Ajouter à l'index
      const index = await getCacheIndex();
      const key = getAudioKey(wordId, language);
      
      index[key] = {
        wordId,
        language,
        localUri: downloadResult.uri,
        downloadedAt: Date.now(),
      };
      
      await saveCacheIndex(index);
      console.log(`✅ Audio téléchargé et caché: ${audioPath}`);
      
      return downloadResult.uri;
    } else {
      console.error(`❌ Échec téléchargement (status ${downloadResult.status})`);
      return null;
    }
  } catch (error) {
    console.error('❌ Erreur téléchargement audio:', error);
    return null;
  }
};

/**
 * Télécharger tous les audios pour un utilisateur premium (mode offline)
 */
export const downloadAllAudiosForOffline = async (
  words: any[],
  onProgress?: (current: number, total: number) => void
): Promise<void> => {
  console.log(`🚀 Début téléchargement de ${words.length} mots pour mode offline`);
  
  let downloaded = 0;
  const total = words.length * 2; // 2 langues par mot
  
  for (const word of words) {
    // Télécharger Shimaoré
    if (word.audio_shimaore) {
      const isCached = await isAudioCached(word._id, 'shimaore');
      if (!isCached) {
        await downloadAndCacheAudio(word._id, 'shimaore', word.audio_shimaore);
      }
      downloaded++;
      onProgress?.(downloaded, total);
    }
    
    // Télécharger Kibouchi
    if (word.audio_kibouchi) {
      const isCached = await isAudioCached(word._id, 'kibouchi');
      if (!isCached) {
        await downloadAndCacheAudio(word._id, 'kibouchi', word.audio_kibouchi);
      }
      downloaded++;
      onProgress?.(downloaded, total);
    }
  }
  
  console.log(`✅ Téléchargement terminé: ${downloaded}/${total} audios`);
};

/**
 * Obtenir les statistiques du cache
 */
export const getCacheStats = async (): Promise<{
  totalFiles: number;
  totalSize: number;
}> => {
  try {
    const index = await getCacheIndex();
    const totalFiles = Object.keys(index).length;
    
    // Calculer la taille totale
    let totalSize = 0;
    for (const cached of Object.values(index)) {
      const fileInfo = await FileSystem.getInfoAsync(cached.localUri);
      if (fileInfo.exists && 'size' in fileInfo) {
        totalSize += fileInfo.size || 0;
      }
    }
    
    return { totalFiles, totalSize };
  } catch (error) {
    console.error('❌ Erreur calcul stats cache:', error);
    return { totalFiles: 0, totalSize: 0 };
  }
};

/**
 * Vider le cache audio
 */
export const clearAudioCache = async (): Promise<void> => {
  try {
    // Supprimer le dossier de cache
    const dirInfo = await FileSystem.getInfoAsync(AUDIO_CACHE_DIR);
    if (dirInfo.exists) {
      await FileSystem.deleteAsync(AUDIO_CACHE_DIR, { idempotent: true });
    }
    
    // Réinitialiser l'index
    await AsyncStorage.removeItem(AUDIO_CACHE_KEY);
    
    // Recréer le dossier
    await initializeAudioCache();
    
    console.log('🗑️ Cache audio vidé');
  } catch (error) {
    console.error('❌ Erreur vidage cache:', error);
  }
};
