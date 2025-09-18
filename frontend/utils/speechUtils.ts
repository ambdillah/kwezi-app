/**
 * UTILITAIRES AUDIO - SYSTÈME DE PRONONCIATION AMÉLIORÉ
 * =====================================================
 * Fonctions réutilisables pour la synthèse vocale avec corrections phonétiques
 */

import * as Speech from 'expo-speech';
import { Alert } from 'react-native';
import { applyPhoneticCorrections } from './phoneticCorrections';

export type SupportedLanguage = 'fr' | 'shimaore' | 'kibouchi';

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
 * Configuration des langues pour la synthèse vocale
 */
const getLanguageConfig = (language: SupportedLanguage) => {
  switch (language) {
    case 'fr':
      return {
        lang: 'fr-FR',
        pitch: 1.0,
        rate: 0.7, // Plus lent pour les enfants
      };
    case 'shimaore':
      // Approximation avec swahili
      return {
        lang: 'sw-KE',
        pitch: 1.1,
        rate: 0.6, // Encore plus lent pour les langues locales
      };
    case 'kibouchi':
      // Approximation avec malgache
      return {
        lang: 'mg-MG',
        pitch: 1.1,
        rate: 0.6,
      };
  }
};

/**
 * Prononce un mot ou une phrase dans la langue spécifiée
 */
export const speakText = async (
  text: string, 
  language: SupportedLanguage = 'fr',
  onStart?: () => void,
  onDone?: () => void
): Promise<void> => {
  try {
    const config = getLanguageConfig(language);
    
    // Appliquer les corrections phonétiques pour Shimaoré et Kibouchi
    let correctedText = text;
    if (language === 'shimaore' || language === 'kibouchi') {
      correctedText = applyPhoneticCorrections(text, language);
      console.log(`🎯 Correction phonétique ${language}: "${text}" → "${correctedText}"`);
    }
    
    // Vérifier si une synthèse est en cours
    const isCurrentlySpeaking = await Speech.isSpeakingAsync();
    if (isCurrentlySpeaking) {
      await Speech.stop();
    }
    
    return new Promise((resolve, reject) => {
      Speech.speak(correctedText, {
        language: config.lang,
        pitch: config.pitch,
        rate: config.rate,
        volume: 1.0,
        onStart: () => {
          console.log(`🔊 Prononciation: "${correctedText}" (${language})`);
          onStart?.();
        },
        onDone: () => {
          console.log(`✅ Prononciation terminée`);
          onDone?.();
          resolve();
        },
        onError: (error) => {
          console.log(`❌ Erreur de prononciation:`, error);
          
          // Fallback vers le français si la langue n'est pas supportée
          if (language !== 'fr') {
            Speech.speak(correctedText, {
              language: 'fr-FR',
              pitch: 1.0,
              rate: 0.7,
              onDone: () => resolve(),
              onError: () => reject(error)
            });
          } else {
            reject(error);
          }
        }
      });
    });
    
  } catch (error) {
    console.log('Erreur Speech:', error);
    throw new Error('La prononciation audio n\'est pas disponible sur cet appareil.');
  }
};

/**
 * Prononce un mot dans toutes les langues avec des pauses
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

/**
 * Arrête toute synthèse vocale en cours
 */
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

/**
 * Vérifie si la synthèse vocale est en cours
 */
export const isSpeechActive = async (): Promise<boolean> => {
  try {
    return await Speech.isSpeakingAsync();
  } catch (error) {
    console.log('Erreur lors de la vérification de la synthèse:', error);
    return false;
  }
};

/**
 * Prononce une phrase conjuguée avec indication du temps
 */
export const speakConjugatedSentence = async (
  sentence: string,
  tense: 'present' | 'past' | 'future',
  language: SupportedLanguage = 'fr'
): Promise<void> => {
  try {
    // Ajouter une introduction pour le temps (optionnel)
    let introduction = '';
    if (language === 'fr') {
      switch (tense) {
        case 'present':
          introduction = 'Au présent: ';
          break;
        case 'past':
          introduction = 'Au passé: ';
          break;
        case 'future':
          introduction = 'Au futur: ';
          break;
      }
    }
    
    const textToSpeak = introduction + sentence;
    await speakText(textToSpeak, language);
    
  } catch (error) {
    console.log('Erreur lors de la prononciation de la phrase conjuguée:', error);
  }
};