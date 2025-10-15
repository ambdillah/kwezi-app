/**
 * SYSTÈME DE COLORATION DES PRÉFIXES DE CONJUGAISON
 * Colorie automatiquement les préfixes selon les temps grammaticaux
 * UNIQUEMENT pour les verbes, pas pour les pronoms
 */

// Schéma de couleurs pédagogiques pour les temps
export const TENSE_COLORS = {
  present: '#28A745',    // Vert - Présent (actuel)
  past: '#FF6B35',       // Orange - Passé (derrière nous)
  future: '#007BFF',     // Bleu - Futur (devant nous)
  default: '#6C757D'     // Gris - Non identifié
};

// Pronoms personnels - NE PAS colorier ces mots
export const SHIMAORE_PRONOUNS = [
  'wami', 'wawe', 'waye', 'wasi', 'wagnou', 'wawo',  // Pronoms sujets (corrigé: wassi -> wasi)
  'yangou', 'yaho', 'yahe', 'yatrou', 'yangnou', 'yawo', // Pronoms possessifs
  'mimi', 'wewe', 'yeye', 'swasi', 'nangnou', 'wawo'    // Variantes (corrigé: swassi -> swasi)
];

export const KIBOUCHI_PRONOUNS = [
  'zahou', 'anaou', 'izi', 'atsika', 'anarou', 'rou',  // Pronoms sujets
  'za', 'ana', // Formes courtes (attention: 'za' et 'ana' peuvent être des préfixes de conjugaison)
];

// Préfixes de conjugaison Shimaoré (UNIQUEMENT pour les verbes)
export const SHIMAORE_PREFIXES = {
  present: ['nis', 'ous', 'as', 'ris', 'mous', 'was', 'wawé', 'wayé'],
  past: ['naco', 'waco', 'aco', 'raco', 'mwaco', 'moico'],
  future: ['nitso', 'outso', 'atso', 'ritso', 'moutso', 'watso']
};

// Préfixes de conjugaison Kibouchi (UNIQUEMENT pour les verbes)
export const KIBOUCHI_PREFIXES = {
  present: ['mi', 'm', 'man', 'miv', 'mit', 'mid', 'mik', 'mal', 'mar', 'mas', 'mat', 'maf', 'map', 'mag', 'mah', 'mam', 'maw'], // Au présent, les verbes gardent l'infinitif (commence par "m")
  past: ['ni', 'nan', 'nam'], // Ajout de 'nan' et 'nam' pour le passé
  future: ['bou', 'mbou'] // Ajout de 'mbou' pour le futur (variante de 'bou')
};

/**
 * Vérifie si un mot est un pronom personnel (à ne pas colorier)
 */
export const isPronoun = (word: string, language: 'shimaore' | 'kibouchi'): boolean => {
  const lowerWord = word.toLowerCase().trim();
  const pronouns = language === 'shimaore' ? SHIMAORE_PRONOUNS : KIBOUCHI_PRONOUNS;
  
  return pronouns.includes(lowerWord);
};

/**
 * Vérifie si un mot semble être un verbe conjugué
 * (a un préfixe de conjugaison ET n'est pas un pronom)
 */
export const isConjugatedVerb = (word: string, language: 'shimaore' | 'kibouchi'): boolean => {
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
          // Si c'est suivi d'un espace ou d'autre chose, c'est probablement un verbe
          return true;
        }
        return true;
      }
    }
  }
  
  return false;
};

/**
 * Identifie le temps d'un mot basé sur ses préfixes
 * UNIQUEMENT si c'est un verbe conjugué
 */
export const identifyTense = (word: string, language: 'shimaore' | 'kibouchi'): string => {
  if (!word || !isConjugatedVerb(word, language)) {
    return 'default';
  }
  
  const lowerWord = word.toLowerCase().trim();
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
 * UNIQUEMENT si c'est un verbe conjugué
 */
export const separatePrefixAndRoot = (word: string, language: 'shimaore' | 'kibouchi'): {
  prefix: string;
  root: string;
  tense: string;
  isVerb: boolean;
} => {
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
        // Préserver la casse originale
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
  
  // Si aucun préfixe trouvé, tout le mot est la racine
  return {
    prefix: '',
    root: word,
    tense: 'default',
    isVerb: false
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
 * UNIQUEMENT les verbes seront colorés
 */
export const createColoredWordsList = (words: string[], language: 'shimaore' | 'kibouchi') => {
  return words.map(word => {
    const { prefix, root, tense, isVerb } = separatePrefixAndRoot(word, language);
    return {
      originalWord: word,
      prefix,
      root,
      tense,
      color: isVerb ? getTenseColor(tense) : TENSE_COLORS.default,
      hasPrefix: prefix.length > 0,
      isVerb: isVerb,
      isPronoun: isPronoun(word, language)
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
 * UNIQUEMENT pour les verbes
 */
export const hasTemporalPrefix = (word: string, language: 'shimaore' | 'kibouchi'): boolean => {
  const { tense, isVerb } = separatePrefixAndRoot(word, language);
  return isVerb && tense !== 'default';
};