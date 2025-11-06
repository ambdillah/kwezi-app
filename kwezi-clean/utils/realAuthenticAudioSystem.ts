/**
 * SYSTÈME AUDIO AUTHENTIQUE RÉEL
 * ================================
 * Utilise VRAIMENT les fichiers .m4a extraits depuis Google Drive
 * Remplace le système précédent qui ne fonctionnait pas
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
 * Mapping des fichiers audio locaux RÉELS
 * Utilise require() avec les vrais fichiers extraits
 */
const FAMILLE_AUDIO_FILES: { [key: string]: any } = {
  // Famille - les fichiers qui existent vraiment
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

const NATURE_AUDIO_FILES: { [key: string]: any } = {
  // Nature - les fichiers qui existent vraiment
  'Atihala.m4a': require('../assets/audio/nature/Atihala.m4a'),
  'Azoumati.m4a': require('../assets/audio/nature/Azoumati.m4a'),
  'Bahari.m4a': require('../assets/audio/nature/Bahari.m4a'),
  'Bandra.m4a': require('../assets/audio/nature/Bandra.m4a'),
  'Boungou.m4a': require('../assets/audio/nature/Boungou.m4a'),
  'Bwé.m4a': require('../assets/audio/nature/Bwé.m4a'),
  'Caléni.m4a': require('../assets/audio/nature/Caléni.m4a'),
  'Civi.m4a': require('../assets/audio/nature/Civi.m4a'),
  'Civiampoulou.m4a': require('../assets/audio/nature/Civiampoulou.m4a'),
  'Daradja.m4a': require('../assets/audio/nature/Daradja.m4a'),
  'Darouba.m4a': require('../assets/audio/nature/Darouba.m4a'),
  'Dhouja.m4a': require('../assets/audio/nature/Dhouja.m4a'),
  'Di.m4a': require('../assets/audio/nature/Di.m4a'),
  'Dobou.m4a': require('../assets/audio/nature/Dobou.m4a'),
  'Fandzava.m4a': require('../assets/audio/nature/Fandzava.m4a'),
  'Fari.m4a': require('../assets/audio/nature/Fari.m4a'),
  'Fasigni.m4a': require('../assets/audio/nature/Fasigni.m4a'),
  'Fassigni.m4a': require('../assets/audio/nature/Fassigni.m4a'),
  'Fotaka.m4a': require('../assets/audio/nature/Fotaka.m4a'),
  'Foulera.m4a': require('../assets/audio/nature/Foulera.m4a'),
  'Gnora.m4a': require('../assets/audio/nature/Gnora.m4a'),
  'Haitri.m4a': require('../assets/audio/nature/Haitri.m4a'),
  'Hayitri.m4a': require('../assets/audio/nature/Hayitri.m4a'),
  'Honkou.m4a': require('../assets/audio/nature/Honkou.m4a'),
  'Houndza_riaka.m4a': require('../assets/audio/nature/Houndza_riaka.m4a'),
  'Jouwa.m4a': require('../assets/audio/nature/Jouwa.m4a'),
  'Kakazou.m4a': require('../assets/audio/nature/Kakazou.m4a'),
  'Kalé.m4a': require('../assets/audio/nature/Kalé.m4a'),
  'Kaléni.m4a': require('../assets/audio/nature/Kaléni.m4a'),
  'Kioni.m4a': require('../assets/audio/nature/Kioni.m4a'),
  'Kouni.m4a': require('../assets/audio/nature/Kouni.m4a'),
  'Kwassa kwassa.m4a': require('../assets/audio/nature/Kwassa kwassa.m4a'),
  'Kètraka.m4a': require('../assets/audio/nature/Kètraka.m4a'),
  'Laka.m4a': require('../assets/audio/nature/Laka.m4a'),
  'Lakana.m4a': require('../assets/audio/nature/Lakana.m4a'),
  'Lakintagna.m4a': require('../assets/audio/nature/Lakintagna.m4a'),
  'Lalagna.m4a': require('../assets/audio/nature/Lalagna.m4a'),
  'Licoli.m4a': require('../assets/audio/nature/Licoli.m4a'),
  'M_bambo.m4a': require('../assets/audio/nature/M_bambo.m4a'),
  'M_bouyou.m4a': require('../assets/audio/nature/M_bouyou.m4a'),
  'M_frampé.m4a': require('../assets/audio/nature/M_frampé.m4a'),
  'M_fénéssi.m4a': require('../assets/audio/nature/M_fénéssi.m4a'),
  'M_manga.m4a': require('../assets/audio/nature/M_manga.m4a'),
  'M_nadzi.m4a': require('../assets/audio/nature/M_nadzi.m4a'),
  'Mahaléni.m4a': require('../assets/audio/nature/Mahaléni.m4a'),
  'Maji yamalé.m4a': require('../assets/audio/nature/Maji yamalé.m4a'),
  'Maji yavo.m4a': require('../assets/audio/nature/Maji yavo.m4a'),
  'Malavou.m4a': require('../assets/audio/nature/Malavou.m4a'),
  'Malavouni.m4a': require('../assets/audio/nature/Malavouni.m4a'),
  'Mawoini.m4a': require('../assets/audio/nature/Mawoini.m4a'),
  'Mcacamba.m4a': require('../assets/audio/nature/Mcacamba.m4a'),
  'Mhonko.m4a': require('../assets/audio/nature/Mhonko.m4a'),
  'Mlima.m4a': require('../assets/audio/nature/Mlima.m4a'),
  'Mouro.m4a': require('../assets/audio/nature/Mouro.m4a'),
  'Mouroni.m4a': require('../assets/audio/nature/Mouroni.m4a'),
  'Mouwoi.m4a': require('../assets/audio/nature/Mouwoi.m4a'),
  'Mtsanga.m4a': require('../assets/audio/nature/Mtsanga.m4a'),
  'Mtsangani.m4a': require('../assets/audio/nature/Mtsangani.m4a'),
  'Mwiri.m4a': require('../assets/audio/nature/Mwiri.m4a'),
  'Mwézi.m4a': require('../assets/audio/nature/Mwézi.m4a'),
  'Ndzia.m4a': require('../assets/audio/nature/Ndzia.m4a'),
  'Nyéha.m4a': require('../assets/audio/nature/Nyéha.m4a'),
  'Ourora.m4a': require('../assets/audio/nature/Ourora.m4a'),
  'Ouzimouyi.m4a': require('../assets/audio/nature/Ouzimouyi.m4a'),
  'Padza k.m4a': require('../assets/audio/nature/Padza k.m4a'),
  'Padza s.m4a': require('../assets/audio/nature/Padza s.m4a'),
  'Paré k.m4a': require('../assets/audio/nature/Paré k.m4a'),
  'Paré s.m4a': require('../assets/audio/nature/Paré s.m4a'),
  'Pévo.m4a': require('../assets/audio/nature/Pévo.m4a'),
  'Ranou fénou.m4a': require('../assets/audio/nature/Ranou fénou.m4a'),
  'Ranou mèki.m4a': require('../assets/audio/nature/Ranou mèki.m4a'),
  'Sabouini.m4a': require('../assets/audio/nature/Sabouini.m4a'),
  'Shioni.m4a': require('../assets/audio/nature/Shioni.m4a'),
  'Soiyi k.m4a': require('../assets/audio/nature/Soiyi k.m4a'),
  'Soiyi s.m4a': require('../assets/audio/nature/Soiyi s.m4a'),
  'Tani.m4a': require('../assets/audio/nature/Tani.m4a'),
  'Trahi k.m4a': require('../assets/audio/nature/Trahi k.m4a'),
  'Trahi s.m4a': require('../assets/audio/nature/Trahi s.m4a'),
  'Trindri.m4a': require('../assets/audio/nature/Trindri.m4a'),
  'Trotro.m4a': require('../assets/audio/nature/Trotro.m4a'),
  'Tsi.m4a': require('../assets/audio/nature/Tsi.m4a'),
  'Tsikou soulaimana.m4a': require('../assets/audio/nature/Tsikou soulaimana.m4a'),
  'Tsikou.m4a': require('../assets/audio/nature/Tsikou.m4a'),
  'Valiha.m4a': require('../assets/audio/nature/Valiha.m4a'),
  'Vatou.m4a': require('../assets/audio/nature/Vatou.m4a'),
  'Vidéti.m4a': require('../assets/audio/nature/Vidéti.m4a'),
  'Vingou.m4a': require('../assets/audio/nature/Vingou.m4a'),
  'Voua.m4a': require('../assets/audio/nature/Voua.m4a'),
  'Voudi ni bouyou.m4a': require('../assets/audio/nature/Voudi ni bouyou.m4a'),
  'Voudi ni finéssi.m4a': require('../assets/audio/nature/Voudi ni finéssi.m4a'),
  'Voudi ni frampé.m4a': require('../assets/audio/nature/Voudi ni frampé.m4a'),
  'Voudi ni hountsi.m4a': require('../assets/audio/nature/Voudi ni hountsi.m4a'),
  'Voudi ni manga.m4a': require('../assets/audio/nature/Voudi ni manga.m4a'),
  'Voudi ni vwaniou.m4a': require('../assets/audio/nature/Voudi ni vwaniou.m4a'),
  'Wingou.m4a': require('../assets/audio/nature/Wingou.m4a'),
  'Zouva.m4a': require('../assets/audio/nature/Zouva.m4a'),
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
 * Joue un enregistrement audio authentique RÉEL via l'API intégrée
 */
export const playRealAuthenticAudio = async (
  audioFilename: string,
  category: string,
  onStart?: () => void,
  onComplete?: () => void
): Promise<boolean> => {
  try {
    // Utiliser l'API audio intégrée dans le backend principal
    const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';
    const audioUrl = `${backendUrl}/api/audio/${category}/${audioFilename}`;
    
    console.log(`🎵 Chargement RÉEL du fichier authentique via API intégrée: ${audioFilename} (${category})`);
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
    
    // Charger et jouer l'audio via l'API intégrée
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
        console.log('✅ Audio authentique RÉEL API intégrée terminé');
      }
    });
    
    return true;
    
  } catch (error) {
    console.log('❌ Erreur lors de la lecture de l\'audio authentique RÉEL API intégrée:', error);
    return false;
  }
};

/**
 * Fonction principale pour jouer un mot avec les vraies métadonnées
 */
export const playWordWithRealAudio = async (
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
        console.log(`🎯 TENTATIVE AUDIO RÉEL pour "${word.french}" (${word.audio_filename}) - langue: ${language}`);
        
        const success = await playRealAuthenticAudio(
          word.audio_filename,
          word.category,
          onStart,
          onComplete
        );
        
        if (success) {
          console.log(`✅ AUDIO AUTHENTIQUE RÉEL joué avec succès: ${word.french}`);
          return; // Audio authentique joué avec succès
        }
        
        console.log('⚠️ Audio authentique RÉEL échoué, utilisation de la synthèse vocale');
      } else {
        console.log(`⚠️ Langue ${language} ne correspond pas à ${word.audio_pronunciation_lang} pour ${word.french}`);
      }
    } else {
      console.log(`⚠️ Pas d'audio authentique pour ${word.french} (has_audio: ${word.has_authentic_audio}, filename: ${word.audio_filename})`);
    }
    
    // Fallback vers la synthèse vocale
    const textToSpeak = language === 'shimaore' ? word.shimaore : word.kibouchi;
    console.log(`🔊 Utilisation de la synthèse vocale pour "${textToSpeak}" en ${language}`);
    
    onStart?.();
    await speakText(textToSpeak, language);
    onComplete?.();
    
  } catch (error) {
    console.log('Erreur générale dans playWordWithRealAudio:', error);
    
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
 * Vérifie si un mot a un enregistrement audio authentique
 */
export const hasRealAuthenticAudio = (word: WordWithAudio): boolean => {
  // Vérifier simplement les métadonnées de la base de données
  return !!(word.has_authentic_audio && word.audio_filename);
};

/**
 * Obtient les informations audio d'un mot
 */
export const getRealAudioInfo = (word: WordWithAudio): {
  hasAuthentic: boolean;
  filename?: string;
  language?: string;
  source?: string;
  category?: string;
} => {
  return {
    hasAuthentic: hasRealAuthenticAudio(word),
    filename: word.audio_filename,
    language: word.audio_pronunciation_lang,
    source: word.audio_source,
    category: word.category
  };
};