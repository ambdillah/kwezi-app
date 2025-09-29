/**
 * UTILITAIRES DE TEST DE VOIX
 * ===========================
 * Fonctions pour tester différentes configurations de voix
 */

import { speakWithFeminineVoice, selectBestFeminineVoice } from './feminineSpeechUtils';

/**
 * Teste plusieurs configurations de voix avec des phrases d'exemple
 */
export const runVoiceDemo = async () => {
  const testSentences = [
    "Bonjour ! Je suis votre assistant pour apprendre le shimaoré et le kibouchi.",
    "Cette voix vous convient-elle pour l'apprentissage ?",
    "Essayons maintenant avec un mot en shimaoré : wami nisnguadza",
    "Et en kibouchi : zahou za msoma"
  ];

  console.log('🎙️ === DÉMONSTRATION DES VOIX ===');
  
  try {
    // Test 1: Voix féminine énergique (recommandée)
    console.log('\n🎯 Test 1: Voix féminine énergique (RECOMMANDÉE)');
    for (let i = 0; i < testSentences.length; i++) {
      console.log(`🗣️ Phrase ${i + 1}: "${testSentences[i]}"`);
      await speakWithEnhancedVoice(
        testSentences[i], 
        i < 2 ? 'fr' : (i === 2 ? 'shimaore' : 'kibouchi'), 
        'feminine', 
        'energetic'
      );
      await new Promise(resolve => setTimeout(resolve, 2000)); // Pause entre les phrases
    }
    
    await new Promise(resolve => setTimeout(resolve, 3000)); // Pause plus longue
    
    // Test 2: Voix masculine conteur
    console.log('\n📚 Test 2: Voix masculine conteur (ALTERNATIVE)');
    await speakWithEnhancedVoice(
      "Voici une voix plus douce, parfaite pour raconter des histoires en shimaoré et kibouchi.", 
      'fr', 
      'masculine', 
      'storyteller'
    );
    
    await new Promise(resolve => setTimeout(resolve, 4000));
    
    // Test 3: Voix masculine calme
    console.log('\n😌 Test 3: Voix masculine calme (RELAXANTE)');
    await speakWithEnhancedVoice(
      "Cette voix est plus calme et posée, idéale pour les moments de concentration.", 
      'fr', 
      'masculine', 
      'calm'
    );
    
    await new Promise(resolve => setTimeout(resolve, 4000));
    
    // Test final avec question
    console.log('\n❓ Test final: Question utilisateur');
    await speakWithEnhancedVoice(
      "Quelle voix préférez-vous pour l'apprentissage du shimaoré et du kibouchi ?", 
      'fr', 
      'masculine', 
      'energetic'
    );
    
    console.log('✅ Démonstration terminée !');
    
  } catch (error) {
    console.log('❌ Erreur lors de la démonstration:', error);
  }
};

/**
 * Affiche les informations sur les voix disponibles
 */
export const showAvailableVoices = async () => {
  try {
    console.log('🔍 Recherche des voix disponibles...');
    const voices = await getAvailableVoices();
    
    console.log(`\n📊 ${voices.length} voix françaises trouvées:`);
    voices.forEach((voice, index) => {
      console.log(`${index + 1}. ${voice.name} (${voice.language}) - ${voice.gender || 'Genre inconnu'}`);
    });
    
    // Identifier les meilleures voix masculines
    const masculineVoices = voices.filter(voice =>
      voice.gender === 'male' || 
      voice.name.toLowerCase().includes('thomas') ||
      voice.name.toLowerCase().includes('daniel') ||
      voice.name.toLowerCase().includes('male')
    );
    
    if (masculineVoices.length > 0) {
      console.log(`\n🎭 ${masculineVoices.length} voix masculines recommandées:`);
      masculineVoices.forEach((voice, index) => {
        console.log(`⭐ ${index + 1}. ${voice.name} - ${voice.language}`);
      });
    } else {
      console.log('\n⚠️ Aucune voix masculine spécifique détectée, utilisation des paramètres de pitch');
    }
    
  } catch (error) {
    console.log('❌ Erreur lors de la récupération des voix:', error);
  }
};

/**
 * Test rapide d'une phrase avec la voix masculine optimisée
 */
export const quickVoiceTest = async (text: string = "Test de la voix masculine pour Mayotte") => {
  console.log(`🧪 Test rapide: "${text}"`);
  
  try {
    await speakWithEnhancedVoice(text, 'fr', 'masculine', 'energetic');
    console.log('✅ Test rapide terminé');
  } catch (error) {
    console.log('❌ Erreur lors du test rapide:', error);
  }
};

/**
 * Teste spécifiquement les corrections phonétiques avec la nouvelle voix
 */
export const testPhoneticCorrections = async () => {
  console.log('🔧 Test des corrections phonétiques avec voix masculine...');
  
  const testWords = [
    { text: "mtsounga", language: 'shimaore' as const, meaning: "éleveur" },
    { text: "ampitsounga", language: 'kibouchi' as const, meaning: "éleveur" },
    { text: "wami nisnguadza", language: 'shimaore' as const, meaning: "je joue" },
    { text: "zahou za msoma", language: 'kibouchi' as const, meaning: "je joue" }
  ];
  
  for (const word of testWords) {
    console.log(`🗣️ Test: "${word.text}" (${word.language}) = ${word.meaning}`);
    await speakWithEnhancedVoice(word.text, word.language, 'masculine', 'energetic');
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  console.log('✅ Test des corrections phonétiques terminé');
};

// Fonction de commodité pour les développeurs
export const devTestVoices = () => {
  console.log('🛠️ Mode développeur: Tests de voix disponibles');
  console.log('Commandes disponibles:');
  console.log('- runVoiceDemo() : Démonstration complète');
  console.log('- showAvailableVoices() : Liste des voix système');
  console.log('- quickVoiceTest("votre texte") : Test rapide');
  console.log('- testPhoneticCorrections() : Test corrections phonétiques');
};