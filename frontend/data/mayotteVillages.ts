/**
 * Données des villages de Mayotte pour le jeu de découverte
 */

export interface Village {
  id: string;
  name: string;
  nameShimaore: string;
  nameKibouchi: string;
  x: number; // Position X sur la carte (pourcentage)
  y: number; // Position Y sur la carte (pourcentage)
  description: string;
  difficulty: number; // 1-3
  quiz: QuizQuestion[];
  unlocked: boolean;
  completed: boolean;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct: number; // Index de la bonne réponse
  explanation: string;
  language?: 'shimaore' | 'kibouchi'; // Question sur la langue
}

export const MAYOTTE_VILLAGES: Village[] = [
  {
    id: 'mamoudzou',
    name: 'Mamoudzou',
    nameShimaore: 'Momoju',
    nameKibouchi: 'Mamuzu',
    x: 55,
    y: 50,
    description: 'La capitale économique de Mayotte',
    difficulty: 1,
    unlocked: true,
    completed: false,
    quiz: [
      {
        question: 'Mamoudzou est la capitale de Mayotte depuis:',
        options: ['1977', '1987', '1997', '2007'],
        correct: 0,
        explanation: 'Mamoudzou est devenue la capitale de Mayotte en 1977, remplaçant Dzaoudzi.',
      },
      {
        question: 'Comment dit-on "Bonjour" en Shimaoré?',
        options: ['Kwezi', 'Salama', 'Mbou marahaba', 'Bariza'],
        correct: 0,
        explanation: 'On dit "Kwezi" pour dire bonjour en Shimaoré!',
        language: 'shimaore',
      },
      {
        question: 'Quel est le marché principal de Mamoudzou?',
        options: ['Marché de Kaweni', 'Marché couvert', 'Marché de Doujani', 'Marché de Mtsapéré'],
        correct: 1,
        explanation: 'Le marché couvert de Mamoudzou est le principal marché de l\'île.',
      },
    ],
  },
  {
    id: 'dzaoudzi',
    name: 'Dzaoudzi',
    nameShimaore: 'Jausi',
    nameKibouchi: 'Dzawuzi',
    x: 85,
    y: 65,
    description: 'L\'ancienne capitale administrative',
    difficulty: 1,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Dzaoudzi se trouve sur quelle île?',
        options: ['Grande-Terre', 'Petite-Terre', 'Bandrélé', 'M\'Tzamboro'],
        correct: 1,
        explanation: 'Dzaoudzi est située sur Petite-Terre, reliée à Grande-Terre par une barge.',
      },
      {
        question: 'Comment dit-on "Merci" en Shimaoré?',
        options: ['Bariza', 'Asante', 'Marahaba', 'Kwezi'],
        correct: 2,
        explanation: '"Marahaba" signifie merci en Shimaoré.',
        language: 'shimaore',
      },
      {
        question: 'Quel monument important se trouve à Dzaoudzi?',
        options: ['Le Rocher', 'La Préfecture', 'Le Fort', 'La Mosquée'],
        correct: 0,
        explanation: 'Le Rocher de Dzaoudzi est un site emblématique qui domine la ville.',
      },
    ],
  },
  {
    id: 'koungou',
    name: 'Koungou',
    nameShimaore: 'Koungou',
    nameKibouchi: 'Kungu',
    x: 45,
    y: 25,
    description: 'La deuxième commune la plus peuplée',
    difficulty: 2,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Koungou est connue pour:',
        options: ['Ses plages', 'Sa mangrove', 'Son aéroport', 'Ses montagnes'],
        correct: 0,
        explanation: 'Koungou possède de magnifiques plages comme Majicavo.',
      },
      {
        question: 'Comment dit-on "Tortue" en Kibouchi?',
        options: ['Fara', 'Fanou', 'Vouli', 'Mamba'],
        correct: 1,
        explanation: '"Fanou" signifie tortue en Kibouchi.',
        language: 'kibouchi',
      },
      {
        question: 'Quelle activité est populaire à Koungou?',
        options: ['La randonnée', 'La plongée', 'Le ski', 'L\'escalade'],
        correct: 1,
        explanation: 'La plongée est très populaire grâce aux magnifiques fonds marins.',
      },
    ],
  },
  {
    id: 'bandrele',
    name: 'Bandrélé',
    nameShimaore: 'Bandrele',
    nameKibouchi: 'Bandrele',
    x: 40,
    y: 75,
    description: 'Village du sud réputé pour sa plage',
    difficulty: 2,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'La plage de Bandrélé est célèbre pour:',
        options: ['Le surf', 'Les tortues', 'La pêche', 'Les dauphins'],
        correct: 1,
        explanation: 'La plage de Bandrélé est un site de ponte des tortues marines.',
      },
      {
        question: 'Comment dit-on "Mer" en Shimaoré?',
        options: ['Bahari', 'Maji', 'Pwani', 'Mvua'],
        correct: 0,
        explanation: '"Bahari" signifie mer en Shimaoré.',
        language: 'shimaore',
      },
      {
        question: 'Quel animal peut-on observer à Bandrélé?',
        options: ['Des makis', 'Des baleines', 'Des éléphants', 'Des ours'],
        correct: 1,
        explanation: 'On peut observer des baleines à bosse pendant la saison migratoire.',
      },
    ],
  },
  {
    id: 'sada',
    name: 'Sada',
    nameShimaore: 'Sada',
    nameKibouchi: 'Sada',
    x: 25,
    y: 55,
    description: 'Village traditionnel de l\'ouest',
    difficulty: 2,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Sada est située sur quelle côte?',
        options: ['Est', 'Ouest', 'Nord', 'Sud'],
        correct: 1,
        explanation: 'Sada se trouve sur la côte ouest de Mayotte.',
      },
      {
        question: 'Comment dit-on "Maison" en Shimaoré?',
        options: ['Nyumba', 'Mlango', 'Dirisha', 'Dari'],
        correct: 0,
        explanation: '"Nyumba" signifie maison en Shimaoré.',
        language: 'shimaore',
      },
      {
        question: 'Quelle tradition est importante à Sada?',
        options: ['Le carnaval', 'Le grand mariage', 'La fête de la musique', 'Halloween'],
        correct: 1,
        explanation: 'Le grand mariage (Manzaraka) est une tradition très importante à Mayotte.',
      },
    ],
  },
  {
    id: 'chiconi',
    name: 'Chiconi',
    nameShimaore: 'Shikoni',
    nameKibouchi: 'Shikoni',
    x: 15,
    y: 40,
    description: 'Village de pêcheurs au nord-ouest',
    difficulty: 2,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Chiconi est réputée pour:',
        options: ['L\'agriculture', 'La pêche', 'L\'industrie', 'Le tourisme'],
        correct: 1,
        explanation: 'Chiconi est un village de pêcheurs traditionnel.',
      },
      {
        question: 'Comment dit-on "Poisson" en Kibouchi?',
        options: ['Samaki', 'Lokou', 'Dagaa', 'Kamba'],
        correct: 1,
        explanation: '"Lokou" signifie poisson en Kibouchi.',
        language: 'kibouchi',
      },
      {
        question: 'Quelle embarcation traditionnelle utilise-t-on?',
        options: ['Le pirogue', 'Le bateau à moteur', 'Le kayak', 'Le voilier'],
        correct: 0,
        explanation: 'La pirogue traditionnelle est encore utilisée par les pêcheurs.',
      },
    ],
  },
  {
    id: 'tsingoni',
    name: 'Tsingoni',
    nameShimaore: 'Tsingoni',
    nameKibouchi: 'Tsingoni',
    x: 30,
    y: 35,
    description: 'L\'ancienne capitale historique',
    difficulty: 3,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Tsingoni fut la capitale de Mayotte jusqu\'en:',
        options: ['1841', '1871', '1901', '1931'],
        correct: 1,
        explanation: 'Tsingoni fut la capitale jusqu\'en 1871.',
      },
      {
        question: 'Comment dit-on "Histoire" en Shimaoré?',
        options: ['Haba', 'Taréhi', 'Mwezi', 'Wakati'],
        correct: 1,
        explanation: '"Taréhi" signifie histoire en Shimaoré.',
        language: 'shimaore',
      },
      {
        question: 'Quel monument historique trouve-t-on à Tsingoni?',
        options: ['Un fort', 'Une mosquée ancienne', 'Un château', 'Un temple'],
        correct: 1,
        explanation: 'La mosquée de Tsingoni est la plus ancienne de France, datant du 16e siècle.',
      },
    ],
  },
  {
    id: 'mtsamboro',
    name: 'M\'Tsangamouji',
    nameShimaore: 'Mtsamuji',
    nameKibouchi: 'Mtsamuji',
    x: 20,
    y: 15,
    description: 'Village du nord avec ses îlots',
    difficulty: 3,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Près de M\'Tsangamouji se trouve:',
        options: ['Le Mont Choungui', 'L\'îlot M\'Tzamboro', 'Le lac Dziani', 'Le Rocher'],
        correct: 1,
        explanation: 'L\'îlot M\'Tzamboro est un site naturel protégé proche de M\'Tsangamouji.',
      },
      {
        question: 'Comment dit-on "Île" en Shimaoré?',
        options: ['Bahari', 'Kissiwa', 'Maji', 'Pwani'],
        correct: 1,
        explanation: '"Kissiwa" signifie île en Shimaoré.',
        language: 'shimaore',
      },
      {
        question: 'Quelle réserve naturelle se trouve au nord?',
        options: ['Parc Marin', 'Réserve de Saziley', 'Forêt de Majimbini', 'Mont Bénara'],
        correct: 0,
        explanation: 'Le Parc Marin de Mayotte protège les récifs et la biodiversité marine.',
      },
    ],
  },
  {
    id: 'acoua',
    name: 'Acoua',
    nameShimaore: 'Akoua',
    nameKibouchi: 'Akua',
    x: 40,
    y: 10,
    description: 'Village du nord-est',
    difficulty: 3,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Acoua est proche de:',
        options: ['La barrière de corail', 'Le lac Dziani', 'Le Mont Choungui', 'Mamoudzou'],
        correct: 0,
        explanation: 'Acoua est proche de la barrière de corail, une des plus belles de Mayotte.',
      },
      {
        question: 'Comment dit-on "Corail" en Kibouchi?',
        options: ['Matumbawe', 'Pweza', 'Kasa', 'Nyota'],
        correct: 0,
        explanation: '"Matumbawe" désigne le corail en Kibouchi.',
        language: 'kibouchi',
      },
      {
        question: 'Quelle activité pratiquer à Acoua?',
        options: ['Ski nautique', 'Snorkeling', 'Alpinisme', 'Parapente'],
        correct: 1,
        explanation: 'Le snorkeling (palmes-masque-tuba) est idéal pour découvrir les fonds marins.',
      },
    ],
  },
  {
    id: 'pamandzi',
    name: 'Pamandzi',
    nameShimaore: 'Pamandzi',
    nameKibouchi: 'Pamandzi',
    x: 90,
    y: 70,
    description: 'Commune de Petite-Terre avec l\'aéroport',
    difficulty: 1,
    unlocked: false,
    completed: false,
    quiz: [
      {
        question: 'Pamandzi accueille:',
        options: ['Le port', 'L\'aéroport', 'La préfecture', 'Le marché'],
        correct: 1,
        explanation: 'L\'aéroport de Mayotte se trouve à Pamandzi sur Petite-Terre.',
      },
      {
        question: 'Comment dit-on "Avion" en Shimaoré?',
        options: ['Ndege', 'Gari', 'Boti', 'Pikipiki'],
        correct: 0,
        explanation: '"Ndege" signifie avion en Shimaoré.',
        language: 'shimaore',
      },
      {
        question: 'Comment voyager entre Petite-Terre et Grande-Terre?',
        options: ['Pont', 'Barge', 'Hélicoptère', 'Tunnel'],
        correct: 1,
        explanation: 'On utilise une barge (bateau) pour traverser entre les deux îles.',
      },
    ],
  },
];
