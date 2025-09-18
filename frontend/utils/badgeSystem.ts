/**
 * SYSTÈME DE BADGES AUTOMATIQUE
 * ==============================
 * Gestion automatique du déblocage de badges basé sur les statistiques utilisateur
 */

export interface UserStats {
  user_name: string;
  total_score: number;
  completed_exercises: number;
  average_score: number;
  best_score: number;
  perfect_scores: number;
  learning_days: number;
  words_learned: number;
}

export interface BadgeRule {
  id: string;
  name: string;
  description: string;
  condition: (stats: UserStats) => boolean;
}

// Règles de déblocage des badges
export const BADGE_RULES: BadgeRule[] = [
  {
    id: 'first-word',
    name: 'Premier Mot',
    description: 'Tu as appris ton premier mot en shimaoré!',
    condition: (stats) => stats.words_learned >= 1
  },
  {
    id: 'word-collector',
    name: 'Collectionneur de Mots',
    description: 'Tu connais 10 mots dans les langues de Mayotte!',
    condition: (stats) => stats.words_learned >= 10
  },
  {
    id: 'ylang-ylang-master',
    name: 'Maître Ylang-Ylang',
    description: 'Tu as obtenu 100 points au total!',
    condition: (stats) => stats.total_score >= 100
  },
  {
    id: 'perfect-score',
    name: 'Score Parfait',
    description: 'Tu as obtenu 100% à un exercice!',
    condition: (stats) => stats.perfect_scores >= 1
  },
  {
    id: 'game-master',
    name: 'Maître des Jeux',
    description: 'Tu as joué à tous les types de jeux!',
    condition: (stats) => stats.completed_exercises >= 5
  },
  {
    id: 'daily-learner',
    name: 'Apprenant Quotidien',
    description: 'Tu apprends tous les jours pendant une semaine!',
    condition: (stats) => stats.learning_days >= 7
  },
  {
    id: 'polyglot-kid',
    name: 'Petit Polyglotte',
    description: 'Tu connais des mots dans les 3 langues!',
    condition: (stats) => stats.words_learned >= 5 && stats.completed_exercises >= 3
  },
  {
    id: 'mayotte-champion',
    name: 'Champion de Mayotte',
    description: 'Tu es devenu expert dans toutes les catégories!',
    condition: (stats) => stats.average_score >= 80 && stats.words_learned >= 50
  }
];

/**
 * Vérifie et débloque automatiquement les badges pour un utilisateur
 */
export const checkAndUnlockBadges = async (userName: string): Promise<string[]> => {
  try {
    // Récupérer les statistiques utilisateur
    const statsResponse = await fetch(
      `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/stats/${encodeURIComponent(userName)}`
    );
    
    if (!statsResponse.ok) {
      console.log('Erreur lors de la récupération des stats');
      return [];
    }
    
    const stats: UserStats = await statsResponse.json();
    
    // Récupérer les badges actuels
    const badgesResponse = await fetch(
      `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/badges/${encodeURIComponent(userName)}`
    );
    
    if (!badgesResponse.ok) {
      console.log('Erreur lors de la récupération des badges');
      return [];
    }
    
    const currentBadges: string[] = await badgesResponse.json();
    const newlyUnlocked: string[] = [];
    
    // Vérifier chaque règle de badge
    for (const rule of BADGE_RULES) {
      // Si le badge n'est pas déjà débloqué et que la condition est remplie
      if (!currentBadges.includes(rule.id) && rule.condition(stats)) {
        try {
          // Débloquer le badge
          const unlockResponse = await fetch(
            `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/badges/${encodeURIComponent(userName)}/unlock/${rule.id}`,
            { method: 'POST' }
          );
          
          if (unlockResponse.ok) {
            newlyUnlocked.push(rule.id);
            console.log(`🎉 Badge débloqué: ${rule.name}`);
          }
        } catch (error) {
          console.log(`Erreur lors du déblocage du badge ${rule.id}:`, error);
        }
      }
    }
    
    return newlyUnlocked;
    
  } catch (error) {
    console.log('Erreur lors de la vérification des badges:', error);
    return [];
  }
};

/**
 * Affiche une notification pour les nouveaux badges
 */
export const showBadgeNotification = (badgeIds: string[], onPress?: () => void) => {
  if (badgeIds.length === 0) return;
  
  const { Alert } = require('react-native');
  
  const badges = BADGE_RULES.filter(rule => badgeIds.includes(rule.id));
  
  if (badges.length === 1) {
    Alert.alert(
      '🎉 Nouveau Badge!',
      `Tu as débloqué: ${badges[0].name}\n${badges[0].description}`,
      [
        { text: 'Super!', onPress },
        { text: 'Voir mes badges', onPress: () => {
          // Navigation vers l'écran badges
          const { router } = require('expo-router');
          router.push('/badges');
        }}
      ]
    );
  } else {
    Alert.alert(
      '🎉 Nouveaux Badges!',
      `Tu as débloqué ${badges.length} nouveaux badges!\n\n${badges.map(b => `• ${b.name}`).join('\n')}`,
      [
        { text: 'Génial!', onPress },
        { text: 'Voir mes badges', onPress: () => {
          const { router } = require('expo-router');
          router.push('/badges');
        }}
      ]
    );
  }
};

/**
 * Enregistre un progrès et vérifie automatiquement les badges
 */
export const recordProgressAndCheckBadges = async (
  userName: string, 
  exerciseId: string, 
  score: number
): Promise<void> => {
  try {
    // Enregistrer le progrès
    const progressResponse = await fetch(
      `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_name: userName,
          exercise_id: exerciseId,
          score: score
        })
      }
    );
    
    if (progressResponse.ok) {
      console.log(`✅ Progrès enregistré: ${score} points pour ${exerciseId}`);
      
      // Vérifier les badges avec un délai pour permettre à la base de données de se mettre à jour
      setTimeout(async () => {
        const newBadges = await checkAndUnlockBadges(userName);
        if (newBadges.length > 0) {
          showBadgeNotification(newBadges);
        }
      }, 1000);
    } else {
      console.log('Erreur lors de l\'enregistrement du progrès');
    }
    
  } catch (error) {
    console.log('Erreur lors de l\'enregistrement du progrès:', error);
  }
};

/**
 * Obtient le niveau d'un utilisateur basé sur ses statistiques
 */
export const getUserLevel = (stats: UserStats) => {
  if (stats.average_score >= 80 && stats.words_learned >= 50) {
    return { level: 'Expert', emoji: '🏆', color: '#FFD700' };
  }
  if (stats.average_score >= 60 && stats.words_learned >= 25) {
    return { level: 'Avancé', emoji: '🌟', color: '#4ECDC4' };
  }
  if (stats.average_score >= 40 && stats.words_learned >= 10) {
    return { level: 'Bon', emoji: '👍', color: '#96CEB4' };
  }
  return { level: 'Débutant', emoji: '🌱', color: '#FF6B6B' };
};