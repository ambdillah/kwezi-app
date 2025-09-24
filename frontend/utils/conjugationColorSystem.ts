/**
 * SYSTÈME DE COLORATION DES PRÉFIXES DE CONJUGAISON
 * Colorie automatiquement les préfixes selon les temps grammaticaux
 */

// Schéma de couleurs pédagogiques pour les temps
export const TENSE_COLORS = {
  present: '#28A745',    // Vert - Présent (actuel)
  past: '#FF6B35',       // Orange - Passé (derrière nous)
  future: '#007BFF',     // Bleu - Futur (devant nous)
  default: '#6C757D'     // Gris - Non identifié
};

// Préfixes de conjugaison Shimaoré
export const SHIMAORE_PREFIXES = {
  present: ['nis', 'ous', 'as', 'ris', 'mous', 'was'],
  past: ['naco', 'waco', 'aco', 'raco', 'mwaco'],
  future: ['nitso', 'outso', 'atso', 'ritso', 'moutso', 'watso']
};

// Préfixes de conjugaison Kibouchi
export const KIBOUCHI_PREFIXES = {
  present: ['za', 'ana', 'izi', 'zéheyi', 'anaréou', 'réou'],
  past: ['ni'], // Préfixe ajouté pour le passé
  future: ['bou'] // Préfixe ajouté pour le futur
};

/**
 * Identifie le temps d'un mot basé sur ses préfixes
 */
export const identifyTense = (word: string, language: 'shimaore' | 'kibouchi'): string => {
  if (!word) return 'default';
  
  const lowerWord = word.toLowerCase();
  const prefixes = language === 'shimaore' ? SHIMAORE_PREFIXES : KIBOUCHI_PREFIXES;
  
  // Vérifier chaque temps
  for (const [tense, prefixList] of Object.entries(prefixes)) {
    for (const prefix of prefixList) {
      if (lowerWord.startsWith(prefix)) {
        return tense;
      }
    }
  }
  
  return 'default';
};

/**
 * Sépare un mot en préfixe et racine pour la coloration
 */
export const separatePrefixAndRoot = (word: string, language: 'shimaore' | 'kibouchi'): {
  prefix: string;
  root: string;
  tense: string;
} => {
  if (!word) return { prefix: '', root: word, tense: 'default' };
  
  const lowerWord = word.toLowerCase();
  const prefixes = language === 'shimaore' ? SHIMAORE_PREFIXES : KIBOUCHI_PREFIXES;
  
  // Rechercher le préfixe correspondant
  for (const [tense, prefixList] of Object.entries(prefixes)) {
    for (const prefix of prefixList) {
      if (lowerWord.startsWith(prefix)) {
        // Préserver la casse originale
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
  
  // Si aucun préfixe trouvé, tout le mot est la racine
  return {
    prefix: '',
    root: word,
    tense: 'default'
  };
};

/**
 * Obtient la couleur d'un temps spécifique
 */
export const getTenseColor = (tense: string): string => {
  return TENSE_COLORS[tense as keyof typeof TENSE_COLORS] || TENSE_COLORS.default;
};

/**
 * Créé des informations de coloration pour une liste de mots
 */
export const createColoredWordsList = (words: string[], language: 'shimaore' | 'kibouchi') => {
  return words.map(word => {
    const { prefix, root, tense } = separatePrefixAndRoot(word, language);
    return {
      originalWord: word,
      prefix,
      root,
      tense,
      color: getTenseColor(tense),
      hasPrefix: prefix.length > 0
    };
  });
};

/**
 * Génère les explications pédagogiques des couleurs
 */
export const getTenseExplanations = () => {
  return {
    present: {
      color: TENSE_COLORS.present,
      name: 'Présent',
      description: 'Action qui se passe maintenant',
      examples: {
        shimaore: ['nis-renga (je parle)', 'ous-renga (tu parles)', 'as-renga (il parle)'],
        kibouchi: ['za mihinagna (je mange)', 'ana misoma (tu joues)']
      }
    },
    past: {
      color: TENSE_COLORS.past,
      name: 'Passé',
      description: 'Action qui s\'est déjà passée',
      examples: {
        shimaore: ['naco-renga (j\'ai parlé)', 'waco-renga (tu as parlé)', 'aco-renga (il a parlé)'],
        kibouchi: ['za ni-hinagna (j\'ai mangé)', 'ana ni-soma (tu as joué)']
      }
    },
    future: {
      color: TENSE_COLORS.future,
      name: 'Futur',
      description: 'Action qui va se passer plus tard',
      examples: {
        shimaore: ['nitso-renga (je parlerai)', 'outso-renga (tu parleras)', 'atso-renga (il parlera)'],
        kibouchi: ['za bou mihinagna (je mangerai)', 'ana bou misoma (tu joueras)']
      }
    }
  };
};

/**
 * Vérifie si un mot contient un préfixe temporel
 */
export const hasTemporalPrefix = (word: string, language: 'shimaore' | 'kibouchi'): boolean => {
  const { tense } = separatePrefixAndRoot(word, language);
  return tense !== 'default';
};