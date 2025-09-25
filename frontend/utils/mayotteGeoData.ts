// Données géographiques réelles de Mayotte basées sur OpenStreetMap
// Coordonnées GPS réelles des communes et coastline

export interface GeoCoordinate {
  latitude: number;
  longitude: number;
}

export interface VillageGeoData {
  id: string;
  name: string;
  coordinates: GeoCoordinate;
  type: 'prefecture' | 'commune';
  unlocked: boolean;
  meta: {
    population?: number;
    specialite: string;
    description: string;
    histoire?: string;
    langue_locale?: string;
    quiz?: {
      question: string;
      options: string[];
      correct: number;
    };
  };
}

// Coordonnées GPS réelles des villages de Mayotte (source OpenStreetMap)
export const MAYOTTE_VILLAGES: VillageGeoData[] = [
  {
    id: 'mamoudzou',
    name: 'Mamoudzou',
    coordinates: { latitude: -12.7822, longitude: 45.2281 },
    type: 'prefecture',
    unlocked: true,
    meta: {
      population: 57281,
      specialite: 'Centre économique de Mayotte',
      description: 'Plus grande ville et préfecture de Mayotte, centre des affaires et du commerce.',
      histoire: 'Ancienne capitale administrative, Mamoudzou est le cœur économique moderne de l\'île.',
      langue_locale: 'shimaoré',
      quiz: {
        question: 'Quelle est la spécialité de Mamoudzou ?',
        options: ['Pêche', 'Commerce', 'Agriculture', 'Artisanat'],
        correct: 1
      }
    }
  },
  {
    id: 'dzaoudzi',
    name: 'Dzaoudzi',
    coordinates: { latitude: -12.7903, longitude: 45.2614 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 15339,
      specialite: 'Aéroport et transport maritime',
      description: 'Porte d\'entrée de Mayotte avec l\'aéroport international Roland Garros.',
      histoire: 'Ancienne capitale de Mayotte, siège de l\'aéroport principal de l\'île.',
      langue_locale: 'shimaoré',
      quiz: {
        question: 'Que trouve-t-on à Dzaoudzi ?',
        options: ['Port de pêche', 'Aéroport', 'Université', 'Marché'],
        correct: 1
      }
    }
  },
  {
    id: 'koungou',
    name: 'Koungou',
    coordinates: { latitude: -12.7336, longitude: 45.2036 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 26444,
      specialite: 'Agriculture et élevage',
      description: 'Commune agricole réputée pour ses cultures de manioc et ses élevages.',
      histoire: 'Village traditionnel devenu commune moderne, gardienne des traditions agricoles mahoraises.',
      langue_locale: 'shimaoré',
      quiz: {
        question: 'Quelle est la principale activité de Koungou ?',
        options: ['Tourisme', 'Agriculture', 'Industrie', 'Pêche'],
        correct: 1
      }
    }
  },
  {
    id: 'dembeni',
    name: 'Dembéni',
    coordinates: { latitude: -12.8267, longitude: 45.1681 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 10141,
      specialite: 'Artisanat traditionnel',
      description: 'Village réputé pour son artisanat local et ses traditions ancestrales.',
      histoire: 'L\'un des plus anciens villages de Mayotte, conservant les savoir-faire traditionnels.',
      langue_locale: 'kibouchi',
      quiz: {
        question: 'Dembéni est connu pour quoi ?',
        options: ['Pêche', 'Artisanat', 'Agriculture', 'Commerce'],
        correct: 1
      }
    }
  },
  {
    id: 'tsingoni',
    name: 'Tsingoni',
    coordinates: { latitude: -12.7847, longitude: 45.1119 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 11165,
      specialite: 'Première mosquée de France',
      description: 'Village historique abritant la plus ancienne mosquée de France, datée de 1538.',
      histoire: 'Ancienne capitale spirituelle de Mayotte, lieu de pèlerinage musulman.',
      langue_locale: 'kibouchi',
      quiz: {
        question: 'Que trouve-t-on à Tsingoni ?',
        options: ['Plus ancienne mosquée de France', 'Plus ancien port', 'Plus ancien marché', 'Plus ancienne école'],
        correct: 0
      }
    }
  },
  {
    id: 'sada',
    name: 'Sada',
    coordinates: { latitude: -12.8347, longitude: 45.1300 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 10612,
      specialite: 'Plages et lagon',
      description: 'Commune côtière aux magnifiques plages et récifs coralliens.',
      histoire: 'Village de pêcheurs traditionnel, gardien des techniques de pêche ancestrales.',
      langue_locale: 'shimaoré',
      quiz: {
        question: 'Sada est réputé pour ses ?',
        options: ['Montagnes', 'Plages', 'Forêts', 'Rivières'],
        correct: 1
      }
    }
  },
  {
    id: 'boueni',
    name: 'Bouéni',
    coordinates: { latitude: -12.9075, longitude: 45.1456 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 7135,
      specialite: 'Culture de l\'ylang-ylang',
      description: 'Village parfumé par ses plantations d\'ylang-ylang, fleur emblématique de Mayotte.',
      histoire: 'Centre historique de la production d\'ylang-ylang, parfum exporté dans le monde entier.',
      langue_locale: 'kibouchi',
      quiz: {
        question: 'Bouéni est célèbre pour sa culture de ?',
        options: ['Vanille', 'Ylang-ylang', 'Café', 'Canne à sucre'],
        correct: 1
      }
    }
  },
  {
    id: 'kani_keli',
    name: 'Kani-Kéli',
    coordinates: { latitude: -12.9683, longitude: 45.1919 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 5382,
      specialite: 'Plage de sable blanc de Sakouli',
      description: 'Village du sud aux plages paradisiaques, dont la célèbre plage de Sakouli.',
      histoire: 'Point le plus au sud de Mayotte, lieu de contemplation et de sérénité.',
      langue_locale: 'kibouchi',
      quiz: {
        question: 'Kani-Kéli abrite quelle plage célèbre ?',
        options: ['Plage de Moya', 'Plage de Sakouli', 'Plage de N\'Gouja', 'Plage de Soulou'],
        correct: 1
      }
    }
  },
  {
    id: 'bandrele',
    name: 'Bandrélé',
    coordinates: { latitude: -12.9089, longitude: 45.1958 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 8900,
      specialite: 'Plage de Saziley et tortues marines',
      description: 'Village côtier où viennent pondre les tortues marines sur la plage de Saziley.',
      histoire: 'Site de reproduction des tortues vertes, lieu de conservation marine important.',
      langue_locale: 'shimaoré',
      quiz: {
        question: 'Bandrélé est connu pour ses ?',
        options: ['Oiseaux rares', 'Tortues marines', 'Dauphins', 'Baleines'],
        correct: 1
      }
    }
  },
  {
    id: 'mtsamboro',
    name: 'Mtsamboro',
    coordinates: { latitude: -12.6717, longitude: 45.1025 },
    type: 'commune',
    unlocked: false,
    meta: {
      population: 6556,
      specialite: 'Mont Choungui et randonnées',
      description: 'Village au pied du Mont Choungui, paradis des randonneurs et amoureux de nature.',
      histoire: 'Village de montagne préservé, gardien des traditions de l\'intérieur de l\'île.',
      langue_locale: 'kibouchi',
      quiz: {
        question: 'Mtsamboro est situé près du ?',
        options: ['Mont Bénara', 'Mont Choungui', 'Mont Mtsapéré', 'Mont Combani'],
        correct: 1
      }
    }
  }
];

// Coastline de Mayotte (coordonnées GPS simplifiées basées sur OSM)
export const MAYOTTE_COASTLINE = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: { name: 'Grande-Terre' },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [45.1025, -12.6717], // Nord-Ouest (Mtsamboro)
          [45.1300, -12.6800], // Nord-Est
          [45.2036, -12.7336], // Est (Koungou)
          [45.2281, -12.7822], // Centre-Est (Mamoudzou)
          [45.2200, -12.8200], // Sud-Est
          [45.1958, -12.9089], // Sud (Bandrélé)
          [45.1919, -12.9683], // Sud (Kani-Kéli)
          [45.1456, -12.9075], // Sud-Ouest (Bouéni)
          [45.1300, -12.8347], // Ouest (Sada)
          [45.1119, -12.7847], // Ouest (Tsingoni)
          [45.1681, -12.8267], // Centre-Ouest (Dembéni)
          [45.1200, -12.7500], // Nord-Ouest
          [45.1025, -12.6717]  // Fermeture (Mtsamboro)
        ]]
      }
    },
    {
      type: 'Feature',
      properties: { name: 'Petite-Terre' },
      geometry: {
        type: 'Polygon',
        coordinates: [[
          [45.2614, -12.7903], // Dzaoudzi centre
          [45.2700, -12.7850], // Nord-Est
          [45.2750, -12.7950], // Sud-Est
          [45.2650, -12.8000], // Sud-Ouest
          [45.2550, -12.7950], // Nord-Ouest
          [45.2614, -12.7903]  // Fermeture
        ]]
      }
    }
  ]
};

// Chemins entre villages avec coordonnées GPS réelles
export interface GeoPath {
  from: string;
  to: string;
  coordinates: GeoCoordinate[];
  distance: number; // en km
  transport: 'route' | 'barge' | 'sentier';
  unlock_requirement: {
    type: string;
    village?: string;
    count?: number;
  };
}

export const MAYOTTE_PATHS: GeoPath[] = [
  {
    from: 'mamoudzou',
    to: 'dzaoudzi',
    coordinates: [
      { latitude: -12.7822, longitude: 45.2281 }, // Mamoudzou
      { latitude: -12.7850, longitude: 45.2400 }, // Point intermédiaire (barge)
      { latitude: -12.7903, longitude: 45.2614 }  // Dzaoudzi
    ],
    distance: 4.2,
    transport: 'barge',
    unlock_requirement: { type: 'visit', village: 'mamoudzou' }
  },
  {
    from: 'mamoudzou',
    to: 'koungou',
    coordinates: [
      { latitude: -12.7822, longitude: 45.2281 }, // Mamoudzou
      { latitude: -12.7600, longitude: 45.2200 }, // Point intermédiaire
      { latitude: -12.7336, longitude: 45.2036 }  // Koungou
    ],
    distance: 6.8,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'mamoudzou' }
  },
  {
    from: 'mamoudzou',
    to: 'dembeni',
    coordinates: [
      { latitude: -12.7822, longitude: 45.2281 }, // Mamoudzou
      { latitude: -12.8000, longitude: 45.2000 }, // Point intermédiaire
      { latitude: -12.8267, longitude: 45.1681 }  // Dembéni
    ],
    distance: 8.5,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'mamoudzou' }
  },
  {
    from: 'dembeni',
    to: 'tsingoni',
    coordinates: [
      { latitude: -12.8267, longitude: 45.1681 }, // Dembéni
      { latitude: -12.8050, longitude: 45.1400 }, // Point intermédiaire
      { latitude: -12.7847, longitude: 45.1119 }  // Tsingoni
    ],
    distance: 7.2,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'dembeni' }
  },
  {
    from: 'koungou',
    to: 'sada',
    coordinates: [
      { latitude: -12.7336, longitude: 45.2036 }, // Koungou
      { latitude: -12.7800, longitude: 45.1700 }, // Point intermédiaire
      { latitude: -12.8347, longitude: 45.1300 }  // Sada
    ],
    distance: 12.3,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'koungou' }
  },
  {
    from: 'tsingoni',
    to: 'boueni',
    coordinates: [
      { latitude: -12.7847, longitude: 45.1119 }, // Tsingoni
      { latitude: -12.8500, longitude: 45.1300 }, // Point intermédiaire
      { latitude: -12.9075, longitude: 45.1456 }  // Bouéni
    ],
    distance: 14.1,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'tsingoni' }
  },
  {
    from: 'boueni',
    to: 'kani_keli',
    coordinates: [
      { latitude: -12.9075, longitude: 45.1456 }, // Bouéni
      { latitude: -12.9300, longitude: 45.1700 }, // Point intermédiaire
      { latitude: -12.9683, longitude: 45.1919 }  // Kani-Kéli
    ],
    distance: 8.7,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'boueni' }
  },
  {
    from: 'kani_keli',
    to: 'bandrele',
    coordinates: [
      { latitude: -12.9683, longitude: 45.1919 }, // Kani-Kéli
      { latitude: -12.9400, longitude: 45.1950 }, // Point intermédiaire
      { latitude: -12.9089, longitude: 45.1958 }  // Bandrélé
    ],
    distance: 6.6,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'kani_keli' }
  },
  {
    from: 'sada',
    to: 'mtsamboro',
    coordinates: [
      { latitude: -12.8347, longitude: 45.1300 }, // Sada
      { latitude: -12.7500, longitude: 45.1200 }, // Point intermédiaire
      { latitude: -12.6717, longitude: 45.1025 }  // Mtsamboro
    ],
    distance: 18.9,
    transport: 'sentier',
    unlock_requirement: { type: 'visit', village: 'sada' }
  },
  {
    from: 'bandrele',
    to: 'mamoudzou',
    coordinates: [
      { latitude: -12.9089, longitude: 45.1958 }, // Bandrélé
      { latitude: -12.8500, longitude: 45.2100 }, // Point intermédiaire
      { latitude: -12.8200, longitude: 45.2200 }, // Point intermédiaire 2
      { latitude: -12.7822, longitude: 45.2281 }  // Mamoudzou
    ],
    distance: 16.4,
    transport: 'route',
    unlock_requirement: { type: 'visit', village: 'bandrele' }
  }
];

// Bounding box de Mayotte pour centrer la carte
export const MAYOTTE_BOUNDS = {
  southwest: { latitude: -13.0000, longitude: 45.0500 },
  northeast: { latitude: -12.6500, longitude: 45.3000 }
};

// Centre géographique de Mayotte
export const MAYOTTE_CENTER: GeoCoordinate = {
  latitude: -12.8333,
  longitude: 45.1667
};