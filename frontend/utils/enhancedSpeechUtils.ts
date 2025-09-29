/**
 * SYSTÈME DE PRONONCIATION AMÉLIORÉ - VOIX FÉMININE ET DOUCE
 * ==========================================================
 * Version améliorée avec options de voix féminine, tonalités douces
 * et configurations optimisées pour l'engagement des enfants
 */

import * as Speech from 'expo-speech';
import { Alert, Platform } from 'react-native';
import { applyPhoneticCorrections } from './phoneticCorrections';

export type SupportedLanguage = 'fr' | 'shimaore' | 'kibouchi';
export type VoiceType = 'masculine' | 'feminine' | 'child-friendly';
export type VoiceCharisma = 'standard' | 'energetic' | 'calm' | 'storyteller';

interface VoiceConfig {
  lang: string;
  pitch: number;
  rate: number;
  volume: number;
  quality?: string;
}

/**
 * Configurations de voix masculine et charismatique
 */
const getVoiceConfig = (
  language: SupportedLanguage, 
  voiceType: VoiceType = 'feminine',
  charisma: VoiceCharisma = 'energetic'
): VoiceConfig => {
  
  const baseConfigs = {
    'fr': {
      lang: 'fr-FR',
      baseVoices: Platform.select({
        ios: ['Amelie', 'Thomas'], // Voix féminines iOS en priorité
        android: ['fr-fr-x-frc-network', 'fr-fr-x-frb-network'],
        default: 'fr-FR'
      })
    },
    'shimaore': {
      lang: Platform.select({
        ios: 'sw-KE', // Swahili comme approximation
        android: 'sw-KE',
        default: 'sw-KE'
      })
    },
    'kibouchi': {
      lang: Platform.select({
        ios: 'mg-MG', // Malgache comme approximation
        android: 'mg-MG', 
        default: 'mg-MG'
      })
    }
  };

  // Configurations de base selon le type de voix
  let baseConfig: VoiceConfig;
  
  switch (voiceType) {
    case 'feminine':
      baseConfig = {
        lang: baseConfigs[language].lang,
        pitch: language === 'fr' ? 1.2 : 1.1, // Plus aigu pour féminin
        rate: 0.8,
        volume: 1.0
      };
      break;
    case 'masculine':
      baseConfig = {
        lang: baseConfigs[language].lang,
        pitch: language === 'fr' ? 0.75 : 0.8, // Plus grave pour masculin
        rate: 0.7,
        volume: 1.0
      };
      break;
      
    case 'feminine':
      baseConfig = {
        lang: baseConfigs[language].lang,
        pitch: language === 'fr' ? 1.1 : 1.15, // Plus aigu pour féminin
        rate: 0.7,
        volume: 1.0
      };
      break;
      
    case 'child-friendly':
      baseConfig = {
        lang: baseConfigs[language].lang,
        pitch: 1.2, // Voix joyeuse pour enfants
        rate: 0.6, // Plus lent pour enfants
        volume: 1.0
      };
      break;
  }

  // Ajustements selon le charisme
  switch (charisma) {
    case 'energetic':
      return {
        ...baseConfig,
        pitch: baseConfig.pitch + 0.1,
        rate: baseConfig.rate + 0.1,
        volume: 1.0
      };
      
    case 'calm':
      return {
        ...baseConfig,
        pitch: baseConfig.pitch - 0.05,
        rate: baseConfig.rate - 0.1,
        volume: 0.9
      };
      
    case 'storyteller':
      return {
        ...baseConfig,
        pitch: baseConfig.pitch + 0.05,
        rate: baseConfig.rate - 0.05,
        volume: 0.95
      };
      
    case 'standard':
    default:
      return baseConfig;
  }
};

/**
 * Liste les voix disponibles sur le système
 */
export const getAvailableVoices = async (): Promise<Speech.Voice[]> => {
  try {
    const voices = await Speech.getAvailableVoicesAsync();
    
    // Filtrer pour trouver les meilleures voix masculines françaises
    const frenchVoices = voices.filter(voice => 
      voice.language.startsWith('fr') || voice.language.startsWith('fr-FR')
    );
    
    const masculineVoices = frenchVoices.filter(voice =>
      voice.name.toLowerCase().includes('thomas') ||
      voice.name.toLowerCase().includes('daniel') ||
      voice.name.toLowerCase().includes('bruno') ||
      voice.name.toLowerCase().includes('male') ||
      voice.gender === 'male'
    );
    
    console.log('🎙️ Voix masculines françaises trouvées:', masculineVoices.map(v => v.name));
    return masculineVoices.length > 0 ? masculineVoices : frenchVoices;
  } catch (error) {
    console.log('⚠️ Erreur lors de la récupération des voix:', error);
    return [];
  }
};

/**
 * Sélectionne la meilleure voix masculine disponible
 */
export const selectBestMasculineVoice = async (language: SupportedLanguage): Promise<string | undefined> => {
  if (language !== 'fr') return undefined; // Seulement pour le français pour l'instant
  
  try {
    const voices = await getAvailableVoices();
    
    // Ordre de préférence pour les voix masculines
    const preferredVoices = [
      'Thomas', 'thomas',
      'Daniel', 'daniel', 
      'Bruno', 'bruno',
      'Alain', 'alain'
    ];
    
    for (const preferred of preferredVoices) {
      const voice = voices.find(v => 
        v.name.toLowerCase().includes(preferred.toLowerCase())
      );
      if (voice) {
        console.log(`🎙️ Voix masculine sélectionnée: ${voice.name}`);
        return voice.identifier || voice.name;
      }
    }
    
    // Fallback: première voix masculine trouvée
    const masculineVoice = voices.find(v => 
      v.gender === 'male' || 
      v.name.toLowerCase().includes('male')
    );
    
    if (masculineVoice) {
      console.log(`🎙️ Voix masculine fallback: ${masculineVoice.name}`);
      return masculineVoice.identifier || masculineVoice.name;
    }
    
  } catch (error) {
    console.log('⚠️ Erreur lors de la sélection de voix:', error);
  }
  
  return undefined;
};

/**
 * Prononce un texte avec voix masculine et charismatique
 */
export const speakWithEnhancedVoice = async (
  text: string, 
  language: SupportedLanguage = 'fr',
  voiceType: VoiceType = 'feminine',
  charisma: VoiceCharisma = 'energetic',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  try {
    const config = getVoiceConfig(language, voiceType, charisma);
    
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
    
    // Sélectionner la meilleure voix si disponible
    const selectedVoice = await selectBestMasculineVoice(language);
    
    const speechOptions: Speech.SpeechOptions = {
      language: config.lang,
      pitch: config.pitch,
      rate: config.rate,
      volume: config.volume,
      voice: selectedVoice, // Utiliser la voix masculine sélectionnée
      onStart: () => {
        console.log(`🎙️ Prononciation ${voiceType} ${charisma}: "${correctedText}" (${language})`);
        onStart?.();
      },
      onDone: () => {
        console.log(`✅ Prononciation terminée`);
        onDone?.();
      },
      onError: (error) => {
        console.log(`❌ Erreur de prononciation:`, error);
        
        // Fallback vers configuration standard si erreur
        Speech.speak(correctedText, {
          language: config.lang,
          pitch: config.pitch,
          rate: config.rate,
          onDone: () => onDone?.(),
          onError: (fallbackError) => {
            console.log('❌ Erreur fallback:', fallbackError);
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
        console.log('Erreur Speech:', error);
        onDone?.();
        resolve();
      };
      
      Speech.speak(correctedText, speechOptions);
    });
    
  } catch (error) {
    console.log('Erreur Speech Enhanced:', error);
    throw new Error('La prononciation audio améliorée n\'est pas disponible sur cet appareil.');
  }
};

/**
 * Teste différentes configurations de voix
 */
export const testVoiceConfigurations = async () => {
  const testText = "Bonjour! Je suis ta nouvelle voix pour apprendre le shimaoré et le kibouchi.";
  
  console.log('🧪 Test des configurations de voix...');
  
  // Test voix masculine énergique
  console.log('🎙️ Test: Voix masculine énergique');
  await speakWithEnhancedVoice(testText, 'fr', 'masculine', 'energetic');
  
  await new Promise(resolve => setTimeout(resolve, 3000)); // Pause
  
  // Test voix masculine conteur
  console.log('🎙️ Test: Voix masculine conteur');
  await speakWithEnhancedVoice(testText, 'fr', 'masculine', 'storyteller');
  
  await new Promise(resolve => setTimeout(resolve, 3000)); // Pause
  
  // Test voix masculine calme
  console.log('🎙️ Test: Voix masculine calme');
  await speakWithEnhancedVoice(testText, 'fr', 'masculine', 'calm');
};

/**
 * Configuration recommandée pour l'application éducative
 */
export const speakEducationalContent = async (
  text: string,
  language: SupportedLanguage = 'fr',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  // Configuration optimale pour l'éducation : masculine énergique
  return speakWithEnhancedVoice(text, language, 'masculine', 'energetic', onStart, onDone);
};

// Exporter aussi les fonctions existantes pour compatibilité
export { speakText } from './speechUtils';
export * from './speechUtils';