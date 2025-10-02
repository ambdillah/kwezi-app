/**
 * Données des fiches d'exercices pour la boutique
 */

export interface ExerciseSheet {
  id: string;
  title: string;
  description: string;
  category: 'vocabulaire' | 'conjugaison' | 'nombres' | 'animaux' | 'ecriture';
  language: 'shimaore' | 'kibouchi' | 'mixte';
  imageUrl: string;
  pdfUrl: string; // URL du PDF (même que l'image pour l'instant)
  price: number; // en euros
  difficulty: 'facile' | 'moyen' | 'difficile';
  ageRange: string;
}

export const EXERCISE_SHEETS: ExerciseSheet[] = [
  {
    id: 'sheet_1',
    title: 'Mancahampi Haroufou',
    description: 'Complète les lettres manquantes - Exercice de vocabulaire illustré',
    category: 'vocabulaire',
    language: 'shimaoré',
    imageUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/y7m0mpzy_1.jpg',
    pdfUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/y7m0mpzy_1.jpg',
    price: 0.99,
    difficulty: 'facile',
    ageRange: '5-8 ans',
  },
  {
    id: 'sheet_2',
    title: 'Mampihiragna - Association',
    description: 'Relie les images aux bons mots - Exercice d\'association',
    category: 'vocabulaire',
    language: 'kibouchi',
    imageUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/wm06m07d_2.jpg',
    pdfUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/wm06m07d_2.jpg',
    price: 0.99,
    difficulty: 'facile',
    ageRange: '5-8 ans',
  },
  {
    id: 'sheet_3',
    title: 'Mampihiragna - Chasse aux mots',
    description: 'Trouve et entoure les mots cachés dans l\'image',
    category: 'vocabulaire',
    language: 'kibouchi',
    imageUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/udvy3vf7_3.jpg',
    pdfUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/udvy3vf7_3.jpg',
    price: 0.99,
    difficulty: 'moyen',
    ageRange: '6-10 ans',
  },
  {
    id: 'sheet_4',
    title: 'Midzorou Magnissaka',
    description: 'Apprends les nombres de 1 à 15 en Kibouchi',
    category: 'nombres',
    language: 'kibouchi',
    imageUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/jixe1ca7_4.jpg',
    pdfUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/jixe1ca7_4.jpg',
    price: 0.99,
    difficulty: 'facile',
    ageRange: '5-8 ans',
  },
  {
    id: 'sheet_5',
    title: 'Foundriha Zignama Chimaoré',
    description: 'Les animaux en Shimaoré - Exercice de vocabulaire',
    category: 'animaux',
    language: 'shimaoré',
    imageUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/blz1k4fz_14.png',
    pdfUrl: 'https://customer-assets.emergentagent.com/job_mayotte-vocab/artifacts/blz1k4fz_14.png',
    price: 0.99,
    difficulty: 'moyen',
    ageRange: '6-10 ans',
  },
];
