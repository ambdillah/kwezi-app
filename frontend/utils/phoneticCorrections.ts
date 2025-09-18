/**
 * CORRECTIONS PHONÉTIQUES POUR SHIMAORÉ ET KIBOUCHI
 * =================================================
 * Améliore la prononciation TTS en appliquant des règles spécifiques
 */

export interface PhoneticRule {
  pattern: RegExp;
  replacement: string;
  description: string;
}

/**
 * Règles phonétiques pour le Shimaoré
 */
export const shimaoreePhoneticRules: PhoneticRule[] = [
  // Règles pour les consonnes groupées avec "m"
  {
    pattern: /\bmts/gi,
    replacement: 'm-ts',
    description: 'Séparation m+ts avec liaison'
  },
  {
    pattern: /\bmb([aeiou])/gi,
    replacement: 'm-b$1',
    description: 'Séparation m+b avec voyelle'
  },
  {
    pattern: /\bmp([aeiou])/gi,
    replacement: 'm-p$1',
    description: 'Séparation m+p avec voyelle'
  },
  {
    pattern: /\bmn([aeiou])/gi,
    replacement: 'm-n$1',
    description: 'Séparation m+n avec voyelle'
  },
  
  // Règles pour les combinaisons spécifiques
  {
    pattern: /ts/gi,
    replacement: 'tss',
    description: 'Accentuation du son ts'
  },
  {
    pattern: /dz/gi,
    replacement: 'dzz',
    description: 'Accentuation du son dz'
  },
  {
    pattern: /ng/gi,
    replacement: 'ngg',
    description: 'Accentuation du son ng'
  },
  
  // Règles pour les voyelles
  {
    pattern: /ou([aeiou])/gi,
    replacement: 'ou-$1',
    description: 'Séparation ou+voyelle'
  },
  
  // Règles spéciales pour certains mots courants
  {
    pattern: /\bwami\b/gi,
    replacement: 'oua-mi',
    description: 'Prononciation correcte de "wami" (je)'
  },
  {
    pattern: /\bwawe\b/gi,
    replacement: 'oua-wé',
    description: 'Prononciation correcte de "wawe" (tu)'
  }
];

/**
 * Règles phonétiques pour le Kibouchi
 */
export const kibouchiPhoneticRules: PhoneticRule[] = [
  // Règles similaires au Shimaoré pour la cohérence
  {
    pattern: /ts/gi,
    replacement: 'tss',
    description: 'Accentuation du son ts (cohérent avec Shimaoré)'
  },
  {
    pattern: /dz/gi,
    replacement: 'dzz',
    description: 'Accentuation du son dz (cohérent avec Shimaoré)'
  },
  
  // Règles spécifiques au Kibouchi
  {
    pattern: /\bampi/gi,
    replacement: 'am-pi',
    description: 'Séparation am+pi'
  },
  {
    pattern: /\bandro/gi,
    replacement: 'an-dro',
    description: 'Séparation an+dro'
  },
  {
    pattern: /\bangala/gi,
    replacement: 'an-ga-la',
    description: 'Décomposition syllabique angala'
  },
  
  // Règles pour les sons malgaches
  {
    pattern: /tr([aeiou])/gi,
    replacement: 'ttr$1',
    description: 'Accentuation tr+voyelle'
  },
  {
    pattern: /dr([aeiou])/gi,
    replacement: 'ddr$1',
    description: 'Accentuation dr+voyelle'
  },
  
  // Règles spéciales pour certains mots courants
  {
    pattern: /\bzahou\b/gi,
    replacement: 'za-hou',
    description: 'Prononciation correcte de "zahou" (je)'
  },
  {
    pattern: /\banaou\b/gi,
    replacement: 'a-na-ou',
    description: 'Prononciation correcte de "anaou" (tu)'
  }
];

/**
 * Applique les corrections phonétiques à un texte
 */
export const applyPhoneticCorrections = (
  text: string,
  language: 'shimaore' | 'kibouchi'
): string => {
  let correctedText = text;
  const rules = language === 'shimaore' ? shimaoreePhoneticRules : kibouchiPhoneticRules;
  
  rules.forEach(rule => {
    const beforeCorrection = correctedText;
    correctedText = correctedText.replace(rule.pattern, rule.replacement);
    
    if (beforeCorrection !== correctedText) {
      console.log(`🔧 Correction phonétique (${language}): "${beforeCorrection}" → "${correctedText}" (${rule.description})`);
    }
  });
  
  return correctedText;
};

/**
 * Exemples de corrections pour tester
 */
export const phoneticExamples = {
  shimaore: [
    { original: 'mtsounga', corrected: applyPhoneticCorrections('mtsounga', 'shimaore') },
    { original: 'wami', corrected: applyPhoneticCorrections('wami', 'shimaore') },
    { original: 'outsésa', corrected: applyPhoneticCorrections('outsésa', 'shimaore') }
  ],
  kibouchi: [
    { original: 'ampitsounga', corrected: applyPhoneticCorrections('ampitsounga', 'kibouchi') },
    { original: 'zahou', corrected: applyPhoneticCorrections('zahou', 'kibouchi') },
    { original: 'angala', corrected: applyPhoneticCorrections('angala', 'kibouchi') }
  ]
};