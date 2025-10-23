/**
 * SYSTÈME DE VOIX MASCULINE SIMPLIFIÉ
 * ===================================
 * Version simplifiée qui force réellement la voix masculine
 */

import * as Speech from './safeSpeech';
import { Platform } from 'react-native';
import { applyPhoneticCorrections } from './phoneticCorrections';

export type SupportedLanguage = 'fr' | 'shimaore' | 'kibouchi';

/**
 * Configuration masculine forcée et simplifiée
 */
const getMasculineConfig = (language: SupportedLanguage) => {
  switch (language) {
    case 'fr':
      return {
        language: 'fr-FR',
        pitch: 0.7,        // Très grave pour forcer masculin
        rate: 0.75,        // Légèrement plus lent
        volume: 1.0,
      };
    case 'shimaore':
      return {
        language: 'sw-KE',  // Swahili comme approximation
        pitch: 0.75,       // Grave aussi
        rate: 0.65,
        volume: 1.0,
      };
    case 'kibouchi':
      return {
        language: 'mg-MG',  // Malgache comme approximation
        pitch: 0.75,       // Grave aussi
        rate: 0.65,
        volume: 1.0,
      };
  }
};

/**
 * Force l'utilisation d'une voix masculine avec des paramètres très spécifiques
 */
export const speakWithMasculineVoice = async (
  text: string,
  language: SupportedLanguage = 'fr',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  try {
    // Appliquer les corrections phonétiques
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

    const config = getMasculineConfig(language);
    
    console.log(`🎙️ VOIX MASCULINE FORCÉE - Langue: ${language}, Pitch: ${config.pitch}, Rate: ${config.rate}`);
    console.log(`🗣️ Texte à prononcer: "${correctedText}"`);

    // Récupérer la liste des voix disponibles pour débugger
    try {
      const voices = await Speech.getAvailableVoicesAsync();
      const frenchVoices = voices.filter(v => v.language.startsWith('fr'));
      const masculineVoices = frenchVoices.filter(v => 
        v.gender === 'male' || 
        v.name.toLowerCase().includes('thomas') ||
        v.name.toLowerCase().includes('daniel') ||
        v.name.toLowerCase().includes('male')
      );
      
      console.log(`🔍 Voix disponibles: ${frenchVoices.length} françaises, ${masculineVoices.length} masculines`);
      
      if (masculineVoices.length > 0) {
        console.log(`🎭 Voix masculine trouvée: ${masculineVoices[0].name}`);
      }
    } catch (error) {
      console.log('⚠️ Erreur lors de la récupération des voix:', error);
    }

    return new Promise<void>((resolve, reject) => {
      Speech.speak(correctedText, {
        language: config.language,
        pitch: config.pitch,
        rate: config.rate,
        volume: config.volume,
        onStart: () => {
          console.log(`🎙️ DÉBUT DE LA PRONONCIATION MASCULINE: "${correctedText}"`);
          onStart?.();
        },
        onDone: () => {
          console.log(`✅ FIN DE LA PRONONCIATION MASCULINE`);
          onDone?.();
          resolve();
        },
        onError: (error) => {
          console.log(`❌ ERREUR VOIX MASCULINE:`, error);
          
          // Fallback avec paramètres encore plus masculins
          console.log('🔄 Fallback avec paramètres ultra-masculins...');
          Speech.speak(correctedText, {
            language: config.language,
            pitch: 0.6,  // Encore plus grave
            rate: 0.7,
            volume: 1.0,
            onDone: () => {
              console.log('✅ Fallback terminé');
              resolve();
            },
            onError: (fallbackError) => {
              console.log('❌ Erreur fallback:', fallbackError);
              reject(fallbackError);
            }
          });
        }
      });
    });

  } catch (error) {
    console.log('❌ Erreur critique voix masculine:', error);
    throw error;
  }
};

/**
 * Test simple pour vérifier que la voix masculine fonctionne
 */
export const testMasculineVoice = async () => {
  console.log('🧪 TEST DE LA VOIX MASCULINE SIMPLIFIÉE...');
  
  try {
    await speakWithMasculineVoice(
      "Test de la voix masculine pour Mayotte. Est-ce que vous entendez une voix d'homme ?",
      'fr'
    );
    console.log('✅ Test de voix masculine terminé');
  } catch (error) {
    console.log('❌ Échec du test de voix masculine:', error);
  }
};
