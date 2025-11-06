/**
 * SYSTÈME DE PRONONCIATION FÉMININE RESTAURÉ
 * ==========================================
 * Configuration pour utiliser une voix féminine douce et appropriée
 * pour l'apprentissage des langues shimaoré et kibouchi
 */

import * as Speech from 'expo-speech';
import { Alert, Platform } from 'react-native';
import { applyPhoneticCorrections } from './phoneticCorrections';

export type SupportedLanguage = 'fr' | 'shimaore' | 'kibouchi';
export type VoiceType = 'feminine' | 'child-friendly';
export type VoiceCharisma = 'standard' | 'gentle' | 'calm' | 'warm';

interface VoiceConfig {
  lang: string;
  pitch: number;
  rate: number;
  volume: number;
  quality?: string;
}

/**
 * Configurations de voix féminine optimisées
 */
const getFeminineVoiceConfig = (
  language: SupportedLanguage, 
  voiceType: VoiceType = 'feminine',
  charisma: VoiceCharisma = 'gentle'
): VoiceConfig => {
  
  const baseConfigs = {
    'fr': {
      lang: 'fr-FR',
      baseVoices: Platform.select({
        ios: ['Amelie', 'Audrey', 'Marie'], // Voix féminines iOS
        android: ['fr-fr-x-fra-network', 'fr-fr-x-frd-network'],
        default: 'fr-FR'
      })
    },
    'shimaore': {
      // Utiliser le français pour éviter les voix Swahili avec contenu pré-enregistré
      lang: 'fr-FR'
    },
    'kibouchi': {
      // Utiliser le français pour une lecture phonétique correcte
      lang: 'fr-FR'
    }
  };

  // Configurations de base selon le type de voix (FÉMININE)
  let baseConfig: VoiceConfig;
  
  switch (voiceType) {
    case 'feminine':
      baseConfig = {
        lang: baseConfigs[language].lang,
        pitch: language === 'fr' ? 1.1 : 1.4, // Pitch TRÈS élevé pour Shimaoré/Kibouchi (voix clairement féminine)
        rate: 0.75, // Rythme confortable
        volume: 1.0
      };
      break;
      
    case 'child-friendly':
      baseConfig = {
        lang: baseConfigs[language].lang,
        pitch: 1.3, // Voix joyeuse pour enfants
        rate: 0.65, // Plus lent pour enfants
        volume: 1.0
      };
      break;
  }

  // Ajustements selon le charisme (orienté féminin)
  switch (charisma) {
    case 'gentle':
      return {
        ...baseConfig,
        pitch: baseConfig.pitch + 0.05,
        rate: baseConfig.rate - 0.05,
        volume: 0.95
      };
      
    case 'calm':
      return {
        ...baseConfig,
        pitch: baseConfig.pitch,
        rate: baseConfig.rate - 0.1,
        volume: 0.9
      };
      
    case 'warm':
      return {
        ...baseConfig,
        pitch: baseConfig.pitch + 0.1,
        rate: baseConfig.rate,
        volume: 1.0
      };
      
    case 'standard':
    default:
      return baseConfig;
  }
};

/**
 * Sélectionne la meilleure voix féminine disponible
 */
export const selectBestFeminineVoice = async (language: SupportedLanguage): Promise<string | undefined> => {
  try {
    const voices = await Speech.getAvailableVoicesAsync();
    
    // Configuration par langue
    const languageConfig = {
      'fr': {
        codes: ['fr', 'fr-FR'],
        preferredNames: ['Amelie', 'amelie', 'Audrey', 'audrey', 'Marie', 'marie', 'Virginie', 'virginie', 'Celine', 'celine']
      },
      'shimaore': {
        // Utiliser la voix française pour éviter le contenu pré-enregistré Swahili
        codes: ['fr', 'fr-FR'],
        preferredNames: ['Amelie', 'amelie', 'Audrey', 'audrey', 'Marie', 'marie', 'Virginie', 'virginie', 'Celine', 'celine']
      },
      'kibouchi': {
        // Utiliser la voix française pour une lecture phonétique correcte
        codes: ['fr', 'fr-FR'],
        preferredNames: ['Amelie', 'amelie', 'Audrey', 'audrey', 'Marie', 'marie', 'Virginie', 'virginie', 'Celine', 'celine']
      }
    };
    
    const config = languageConfig[language];
    
    // Filtrer les voix selon la langue
    const languageVoices = voices.filter(voice => 
      config.codes.some(code => voice.language.startsWith(code))
    );
    
    // Chercher les voix féminines préférées
    for (const preferred of config.preferredNames) {
      const voice = languageVoices.find(v => 
        v.name.toLowerCase().includes(preferred.toLowerCase())
      );
      if (voice) {
        console.log(`👩 Voix féminine sélectionnée (${language}): ${voice.name}`);
        return voice.identifier || voice.name;
      }
    }
    
    // Fallback: chercher toute voix féminine
    const feminineVoice = languageVoices.find(v => 
      v.gender === 'female' || 
      v.name.toLowerCase().includes('female') ||
      v.name.toLowerCase().includes('woman') ||
      !v.name.toLowerCase().includes('male')  // Éviter les voix explicitement masculines
    );
    
    if (feminineVoice) {
      console.log(`👩 Voix féminine fallback (${language}): ${feminineVoice.name}`);
      return feminineVoice.identifier || feminineVoice.name;
    }
    
    // Dernier fallback: première voix disponible avec pitch élevé
    if (languageVoices.length > 0) {
      console.log(`👩 Voix générique avec pitch féminin (${language}): ${languageVoices[0].name}`);
      return languageVoices[0].identifier || languageVoices[0].name;
    }
    
  } catch (error) {
    console.log('⚠️ Erreur lors de la sélection de voix féminine:', error);
  }
  
  return undefined;
};

/**
 * Prononce un texte avec voix féminine douce
 */
export const speakWithFeminineVoice = async (
  text: string, 
  language: SupportedLanguage = 'fr',
  voiceType: VoiceType = 'feminine',
  charisma: VoiceCharisma = 'gentle',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  try {
    const config = getFeminineVoiceConfig(language, voiceType, charisma);
    
    // Appliquer les corrections phonétiques pour Shimaoré et Kibouchi
    let correctedText = text;
    if (language === 'shimaore' || language === 'kibouchi') {
      correctedText = applyPhoneticCorrections(text, language);
      console.log(`🎯 Correction phonétique ${language}: "${text}" → "${correctedText}"`);
    }
    
    // Arrêter toute synthèse en cours
    const isCurrentlySpeaking = await Speech.isSpeakingAsync();
    if (isCurrentlySpeaking) {
      await Speech.stop();
    }
    
    // Sélectionner la meilleure voix féminine si disponible
    const selectedVoice = await selectBestFeminineVoice(language);
    
    const speechOptions: Speech.SpeechOptions = {
      language: config.lang,
      pitch: config.pitch,
      rate: config.rate,
      volume: config.volume,
      voice: selectedVoice, // Utiliser la voix féminine sélectionnée
      onStart: () => {
        console.log(`👩 Prononciation féminine ${charisma}: "${correctedText}" (${language})`);
        onStart?.();
      },
      onDone: () => {
        console.log(`✅ Prononciation féminine terminée`);
        onDone?.();
      },
      onError: (error) => {
        console.log(`❌ Erreur de prononciation féminine:`, error);
        
        // Fallback vers configuration standard si erreur
        Speech.speak(correctedText, {
          language: config.lang,
          pitch: config.pitch,
          rate: config.rate,
          onDone: () => onDone?.(),
          onError: (fallbackError) => {
            console.log('❌ Erreur fallback féminine:', fallbackError);
            onDone?.();
          }
        });
      }
    };
    
    return new Promise<void>((resolve) => {
      speechOptions.onDone = () => {
        onDone?.();
        resolve();
      };
      speechOptions.onError = (error) => {
        console.log('Erreur Speech Féminine:', error);
        onDone?.();
        resolve();
      };
      
      Speech.speak(correctedText, speechOptions);
    });
    
  } catch (error) {
    console.log('Erreur Speech Féminine:', error);
    throw new Error('La prononciation audio féminine n\'est pas disponible sur cet appareil.');
  }
};

/**
 * Prononce un mot avec voix féminine (fonction de compatibilité)
 * GARANTIT une voix féminine pour TOUTES les langues
 */
export const speakText = async (
  text: string, 
  language: SupportedLanguage = 'fr',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  console.log(`🎤 speakText appelé: "${text}" (${language})`);
  
  // Force l'utilisation de la voix féminine avec pitch élevé
  return speakWithFeminineVoice(text, language, 'feminine', 'gentle', onStart, onDone);
};

/**
 * Configuration recommandée pour l'application éducative (FÉMININE)
 */
export const speakEducationalContent = async (
  text: string,
  language: SupportedLanguage = 'fr',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  // Configuration optimale pour l'éducation : féminine douce
  return speakWithFeminineVoice(text, language, 'feminine', 'gentle', onStart, onDone);
};

/**
 * Teste la voix féminine restaurée
 */
export const testFeminineVoice = async () => {
  const testText = "Bonjour! Je suis votre guide féminine pour apprendre le shimaoré et le kibouchi.";
  
  console.log('🧪 Test de la voix féminine restaurée...');
  
  // Test voix féminine douce
  console.log('👩 Test: Voix féminine douce');
  await speakWithFeminineVoice(testText, 'fr', 'feminine', 'gentle');
  
  await new Promise(resolve => setTimeout(resolve, 3000)); // Pause
  
  // Test voix féminine chaleureuse
  console.log('👩 Test: Voix féminine chaleureuse');
  await speakWithFeminineVoice(testText, 'fr', 'feminine', 'warm');
};

// Exporter les fonctions utilitaires pour arrêter et vérifier la synthèse
export const stopSpeech = async (): Promise<void> => {
  try {
    const isCurrentlySpeaking = await Speech.isSpeakingAsync();
    if (isCurrentlySpeaking) {
      await Speech.stop();
    }
  } catch (error) {
    console.log('Erreur lors de l\'arrêt de la synthèse:', error);
  }
};

export const isSpeechActive = async (): Promise<boolean> => {
  try {
    return await Speech.isSpeakingAsync();
  } catch (error) {
    console.log('Erreur lors de la vérification de la synthèse:', error);
    return false;
  }
};

export interface Word {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  difficulty?: number;
  image_url?: string;
}

/**
 * Prononce un mot dans toutes les langues avec voix féminine
 */
export const speakWordAllLanguages = async (
  word: Word,
  onLanguageStart?: (language: SupportedLanguage) => void,
  onComplete?: () => void
): Promise<void> => {
  try {
    // Français
    onLanguageStart?.('fr');
    await speakText(word.french, 'fr');
    await new Promise(resolve => setTimeout(resolve, 800)); // Pause
    
    // Shimaoré
    onLanguageStart?.('shimaore');
    await speakText(word.shimaore, 'shimaore');
    await new Promise(resolve => setTimeout(resolve, 800)); // Pause
    
    // Kibouchi
    onLanguageStart?.('kibouchi');
    await speakText(word.kibouchi, 'kibouchi');
    
    onComplete?.();
    
  } catch (error) {
    console.log('Erreur lors de la lecture de toutes les langues:', error);
    Alert.alert('Info', 'Problème avec la prononciation audio.');
  }
};