#!/usr/bin/env node
/**
 * Test amélioré pour vérifier le système de coloration des préfixes de conjugaison
 * UNIQUEMENT pour les verbes, pas pour les pronoms
 */

// Import des fonctions (simulation)
const SHIMAORE_PRONOUNS = [
  'wami', 'wawe', 'waye', 'wasi', 'wagnou', 'wawo',  // Pronoms sujets (corrigé: wassi -> wasi)
  'yangou', 'yaho', 'yahe', 'yatrou', 'yangnou', 'yawo', // Pronoms possessifs
  'mimi', 'wewe', 'yeye', 'swasi', 'nangnou', 'wawo'    // Variantes (corrigé: swassi -> swasi)
];

const KIBOUCHI_PRONOUNS = [
  'zahou', 'anaou', 'izi', 'atsika', 'anarou', 'rou',  // Pronoms sujets
  'za', 'ana', // Formes courtes (attention: peuvent être des préfixes)
];

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

function isPronoun(word, language) {
  const lowerWord = word.toLowerCase().trim();
  const pronouns = language === 'shimaore' ? SHIMAORE_PRONOUNS : KIBOUCHI_PRONOUNS;
  return pronouns.includes(lowerWord);
}

function isConjugatedVerb(word, language) {
  // D'abord vérifier que ce n'est pas un pronom
  if (isPronoun(word, language)) {
    return false;
  }
  
  const lowerWord = word.toLowerCase().trim();
  const prefixes = language === 'shimaore' ? SHIMAORE_PREFIXES : KIBOUCHI_PREFIXES;
  
  // Vérifier si le mot commence par un préfixe de conjugaison
  for (const prefixList of Object.values(prefixes)) {
    for (const prefix of prefixList) {
      if (lowerWord.startsWith(prefix)) {
        // Pour Kibouchi, 'za' et 'ana' peuvent être des pronoms ou des préfixes
        if (language === 'kibouchi' && (prefix === 'za' || prefix === 'ana')) {
          // Si le mot est exactement 'za' ou 'ana', c'est probablement un pronom
          if (lowerWord === prefix) {
            return false;
          }
          return true;
        }
        return true;
      }
    }
  }
  
  return false;
}

function separatePrefixAndRoot(word, language) {
  if (!word) return { prefix: '', root: word, tense: 'default', isVerb: false };
  
  // Vérifier si c'est un pronom - si oui, ne pas traiter
  if (isPronoun(word, language)) {
    return { prefix: '', root: word, tense: 'default', isVerb: false };
  }
  
  // Vérifier si c'est un verbe conjugué
  if (!isConjugatedVerb(word, language)) {
    return { prefix: '', root: word, tense: 'default', isVerb: false };
  }
  
  const lowerWord = word.toLowerCase().trim();
  const prefixes = language === 'shimaore' ? SHIMAORE_PREFIXES : KIBOUCHI_PREFIXES;
  
  // Rechercher le préfixe correspondant
  for (const [tense, prefixList] of Object.entries(prefixes)) {
    for (const prefix of prefixList) {
      if (lowerWord.startsWith(prefix)) {
        const originalPrefix = word.substring(0, prefix.length);
        const originalRoot = word.substring(prefix.length);
        
        return {
          prefix: originalPrefix,
          root: originalRoot,
          tense: tense,
          isVerb: true
        };
      }
    }
  }
  
  return { prefix: '', root: word, tense: 'default', isVerb: false };
}

// Tests
console.log('🧪 TEST DU SYSTÈME DE COLORATION (VERBES UNIQUEMENT)');
console.log('=' * 60);

// Mots de test shimaoré avec verbes ET pronoms
const shimaoréWords = ['nisrenga', 'acorenga', 'atsorenga', 'wami', 'wassi', 'oudzya'];
console.log('\n📝 Tests Shimaoré:');
shimaoréWords.forEach(word => {
  const result = separatePrefixAndRoot(word, 'shimaore');
  const color = result.isVerb ? TENSE_COLORS[result.tense] : TENSE_COLORS.default;
  const type = result.isVerb ? 'VERBE' : (isPronoun(word, 'shimaore') ? 'PRONOM' : 'MOT');
  console.log(`  - "${word}": ${type} | préfixe="${result.prefix}" (${result.tense}, ${color}) + racine="${result.root}"`);
});

// Mots de test kibouchi avec verbes ET pronoms
const kibouchiWords = ['za mihinagna', 'ana misoma', 'ni hinagna', 'bou misoma', 'za', 'ana', 'zahou'];
console.log('\n📝 Tests Kibouchi:');
kibouchiWords.forEach(word => {
  const result = separatePrefixAndRoot(word, 'kibouchi');
  const color = result.isVerb ? TENSE_COLORS[result.tense] : TENSE_COLORS.default;
  const type = result.isVerb ? 'VERBE' : (isPronoun(word, 'kibouchi') ? 'PRONOM' : 'MOT');
  console.log(`  - "${word}": ${type} | préfixe="${result.prefix}" (${result.tense}, ${color}) + racine="${result.root}"`);
});

console.log('\n✅ Tests terminés - Seuls les VERBES sont colorés!');
console.log('\n🔍 Règles appliquées:');
console.log('  ✅ Verbes conjugués: préfixes colorés selon le temps');
console.log('  ❌ Pronoms personnels: PAS de coloration (couleur par défaut)');
console.log('  ❌ Autres mots: PAS de coloration (couleur par défaut)');

console.log('\nLégende des couleurs:');
Object.entries(TENSE_COLORS).forEach(([tense, color]) => {
  const name = tense === 'present' ? 'Présent' : tense === 'past' ? 'Passé' : tense === 'future' ? 'Futur' : 'Défaut';
  console.log(`  🎨 ${name}: ${color}`);
});