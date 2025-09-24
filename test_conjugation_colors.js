#!/usr/bin/env node
/**
 * Test simple pour vérifier le système de coloration des préfixes de conjugaison
 */

// Import des fonctions (simulation)
const SHIMAORE_PREFIXES = {
  present: ['nis', 'ous', 'as', 'ris', 'mous', 'was'],
  past: ['naco', 'waco', 'aco', 'raco', 'mwaco'],
  future: ['nitso', 'outso', 'atso', 'ritso', 'moutso', 'watso']
};

const KIBOUCHI_PREFIXES = {
  present: ['za', 'ana', 'izi', 'zeheyi', 'anarou', 'rou'],
  past: ['ni'], 
  future: ['bou']
};

const TENSE_COLORS = {
  present: '#28A745',    // Vert 
  past: '#FF6B35',       // Orange
  future: '#007BFF',     // Bleu
  default: '#6C757D'     // Gris
};

function separatePrefixAndRoot(word, language) {
  if (!word) return { prefix: '', root: word, tense: 'default' };
  
  const lowerWord = word.toLowerCase();
  const prefixes = language === 'shimaore' ? SHIMAORE_PREFIXES : KIBOUCHI_PREFIXES;
  
  for (const [tense, prefixList] of Object.entries(prefixes)) {
    for (const prefix of prefixList) {
      if (lowerWord.startsWith(prefix)) {
        const originalPrefix = word.substring(0, prefix.length);
        const originalRoot = word.substring(prefix.length);
        
        return {
          prefix: originalPrefix,
          root: originalRoot,
          tense: tense
        };
      }
    }
  }
  
  return {
    prefix: '',
    root: word,
    tense: 'default'
  };
}

// Tests
console.log('🧪 TEST DU SYSTÈME DE COLORATION DES PRÉFIXES DE CONJUGAISON');
console.log('=' * 60);

// Mots de test shimaoré
const shimaoréWords = ['nisrenga', 'acorenga', 'atsorenga', 'Wami', 'oudzya'];
console.log('\n📝 Tests Shimaoré:');
shimaoréWords.forEach(word => {
  const result = separatePrefixAndRoot(word, 'shimaore');
  const color = TENSE_COLORS[result.tense];
  console.log(`  - "${word}": préfixe="${result.prefix}" (${result.tense}, ${color}) + racine="${result.root}"`);
});

// Mots de test kibouchi  
const kibouchiWords = ['za mihinagna', 'ana misoma', 'ni hinagna', 'bou misoma'];
console.log('\n📝 Tests Kibouchi:');
kibouchiWords.forEach(word => {
  const result = separatePrefixAndRoot(word, 'kibouchi');
  const color = TENSE_COLORS[result.tense];
  console.log(`  - "${word}": préfixe="${result.prefix}" (${result.tense}, ${color}) + racine="${result.root}"`);
});

console.log('\n✅ Tests terminés - Le système de coloration devrait fonctionner!');
console.log('\nLégende des couleurs:');
Object.entries(TENSE_COLORS).forEach(([tense, color]) => {
  const name = tense === 'present' ? 'Présent' : tense === 'past' ? 'Passé' : tense === 'future' ? 'Futur' : 'Défaut';
  console.log(`  🎨 ${name}: ${color}`);
});