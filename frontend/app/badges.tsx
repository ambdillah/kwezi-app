import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  requirement: string;
  unlocked: boolean;
  unlockedAt?: Date;
}

const AVAILABLE_BADGES: Omit<Badge, 'unlocked' | 'unlockedAt'>[] = [
  {
    id: 'first-word',
    name: 'Premier Mot',
    description: 'Tu as appris ton premier mot en shimaoré!',
    icon: 'school',
    color: '#4ECDC4',
    requirement: 'Apprendre 1 mot'
  },
  {
    id: 'word-collector',
    name: 'Collectionneur de Mots',
    description: 'Tu connais 10 mots dans les langues de Mayotte!',
    icon: 'library',
    color: '#45B7D1',
    requirement: 'Apprendre 10 mots'
  },
  {
    id: 'maki-friend',
    name: 'Ami des Makis',
    description: 'Tu as complété tous les exercices sur les animaux!',
    icon: 'paw',
    color: '#96CEB4',
    requirement: 'Finir catégorie animaux'
  },
  {
    id: 'ylang-ylang-master',
    name: 'Maître Ylang-Ylang',
    description: 'Tu as obtenu 100 points au total!',
    icon: 'flower',
    color: '#FECA57',
    requirement: '100 points totaux'
  },
  {
    id: 'family-expert',
    name: 'Expert Famille',
    description: 'Tu maîtrises tous les mots de la famille!',
    icon: 'people',
    color: '#FF6B6B',
    requirement: 'Maîtriser catégorie famille'
  },
  {
    id: 'polyglot-kid',
    name: 'Petit Polyglotte',
    description: 'Tu connais des mots dans les 3 langues!',
    icon: 'language',
    color: '#9B59B6',
    requirement: 'Utiliser français, shimaoré, kibouchi'
  },
  {
    id: 'game-master',
    name: 'Maître des Jeux',
    description: 'Tu as joué à tous les types de jeux!',
    icon: 'game-controller',
    color: '#E67E22',
    requirement: 'Jouer à tous les jeux'
  },
  {
    id: 'perfect-score',
    name: 'Score Parfait',
    description: 'Tu as obtenu 100% à un exercice!',
    icon: 'trophy',
    color: '#FFD700',
    requirement: 'Score parfait'
  },
  {
    id: 'daily-learner',
    name: 'Apprenant Quotidien',
    description: 'Tu apprends tous les jours pendant une semaine!',
    icon: 'calendar',
    color: '#1ABC9C',
    requirement: '7 jours consécutifs'
  },
  {
    id: 'mayotte-champion',
    name: 'Champion de Mayotte',
    description: 'Tu es devenu expert dans toutes les catégories!',
    icon: 'medal',
    color: '#C0392B',
    requirement: 'Niveau expert'
  }
];

export default function BadgesScreen() {
  const [badges, setBadges] = useState<Badge[]>([]);
  const [unlockedCount, setUnlockedCount] = useState(0);
  const [userName, setUserName] = useState('');

  useEffect(() => {
    loadBadges();
    loadUserName();
  }, []);

  const loadUserName = async () => {
    try {
      const stored = await AsyncStorage.getItem('userName');
      if (stored) {
        setUserName(stored);
      }
    } catch (error) {
      console.log('Error loading user name:', error);
    }
  };

  const loadBadges = async () => {
    try {
      const stored = await AsyncStorage.getItem('userBadges');
      const unlockedBadges = stored ? JSON.parse(stored) : [];
      
      const badgesWithStatus = AVAILABLE_BADGES.map(badge => ({
        ...badge,
        unlocked: unlockedBadges.includes(badge.id),
        unlockedAt: unlockedBadges.includes(badge.id) ? new Date() : undefined
      }));

      setBadges(badgesWithStatus);
      setUnlockedCount(unlockedBadges.length);
    } catch (error) {
      console.log('Error loading badges:', error);
      // Initialize with default badges
      const defaultBadges = AVAILABLE_BADGES.map(badge => ({
        ...badge,
        unlocked: false
      }));
      setBadges(defaultBadges);
    }
  };

  const unlockBadge = async (badgeId: string) => {
    try {
      const stored = await AsyncStorage.getItem('userBadges');
      const unlockedBadges = stored ? JSON.parse(stored) : [];
      
      if (!unlockedBadges.includes(badgeId)) {
        unlockedBadges.push(badgeId);
        await AsyncStorage.setItem('userBadges', JSON.stringify(unlockedBadges));
        
        const badge = badges.find(b => b.id === badgeId);
        if (badge) {
          Alert.alert(
            '🎉 Nouveau Badge!',
            `Tu as débloqué: ${badge.name}\n${badge.description}`,
            [{ text: 'Super!', onPress: loadBadges }]
          );
        }
      }
    } catch (error) {
      console.log('Error unlocking badge:', error);
    }
  };

  const simulateUnlock = () => {
    const lockedBadges = badges.filter(b => !b.unlocked);
    if (lockedBadges.length > 0) {
      const randomBadge = lockedBadges[Math.floor(Math.random() * lockedBadges.length)];
      unlockBadge(randomBadge.id);
    } else {
      Alert.alert('Bravo!', 'Tu as déjà tous les badges! 🏆');
    }
  };

  const resetBadges = async () => {
    Alert.alert(
      'Réinitialiser les badges',
      'Es-tu sûr de vouloir remettre à zéro tes badges?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Réinitialiser',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('userBadges');
              loadBadges();
              Alert.alert('Badges réinitialisés', 'Tu peux maintenant les débloquer à nouveau!');
            } catch (error) {
              Alert.alert('Erreur', 'Impossible de réinitialiser les badges');
            }
          }
        }
      ]
    );
  };

  return (
    <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <Text style={styles.title}>Mes Badges 🏆</Text>
          <TouchableOpacity onPress={simulateUnlock} style={styles.testButton}>
            <Ionicons name="gift" size={24} color="#000" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Progress Overview */}
          <View style={styles.progressContainer}>
            <LinearGradient colors={['#4ECDC4', '#45B7D1']} style={styles.progressGradient}>
              <Text style={styles.progressTitle}>
                Salut {userName || 'petit mahorais'}! 🌺
              </Text>
              <Text style={styles.progressText}>
                Tu as débloqué {unlockedCount} badge{unlockedCount !== 1 ? 's' : ''} sur {badges.length}
              </Text>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { width: `${(unlockedCount / badges.length) * 100}%` }
                  ]} 
                />
              </View>
              <Text style={styles.progressPercentage}>
                {Math.round((unlockedCount / badges.length) * 100)}% complété
              </Text>
            </LinearGradient>
          </View>

          {/* Badges Grid */}
          <Text style={styles.sectionTitle}>Collection de badges 🏅</Text>
          
          <View style={styles.badgesGrid}>
            {badges.map((badge) => (
              <View
                key={badge.id}
                style={[
                  styles.badgeCard,
                  { backgroundColor: badge.unlocked ? badge.color : '#E0E0E0' }
                ]}
              >
                <View style={styles.badgeIconContainer}>
                  <Ionicons
                    name={badge.icon as any}
                    size={32}
                    color={badge.unlocked ? '#fff' : '#999'}
                  />
                  {badge.unlocked && (
                    <View style={styles.unlockedIndicator}>
                      <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
                    </View>
                  )}
                </View>
                
                <Text style={[
                  styles.badgeName,
                  { color: badge.unlocked ? '#fff' : '#999' }
                ]}>
                  {badge.name}
                </Text>
                
                <Text style={[
                  styles.badgeDescription,
                  { color: badge.unlocked ? '#fff' : '#666' }
                ]}>
                  {badge.description}
                </Text>
                
                <Text style={[
                  styles.badgeRequirement,
                  { color: badge.unlocked ? 'rgba(255,255,255,0.8)' : '#888' }
                ]}>
                  {badge.requirement}
                </Text>
                
                {!badge.unlocked && (
                  <View style={styles.lockedOverlay}>
                    <Ionicons name="lock-closed" size={24} color="#999" />
                  </View>
                )}
              </View>
            ))}
          </View>

          {/* Achievement Tips */}
          <View style={styles.tipsContainer}>
            <Text style={styles.tipsTitle}>💡 Comment débloquer plus de badges :</Text>
            <Text style={styles.tipText}>🎮 Continue à jouer aux jeux éducatifs</Text>
            <Text style={styles.tipText}>📚 Apprends de nouveaux mots chaque jour</Text>
            <Text style={styles.tipText}>⭐ Essaie d'obtenir des scores parfaits</Text>
            <Text style={styles.tipText}>🌺 Explore toutes les catégories</Text>
          </View>

          {/* Admin Controls */}
          <View style={styles.adminContainer}>
            <TouchableOpacity onPress={resetBadges} style={styles.resetButton}>
              <Text style={styles.resetButtonText}>Réinitialiser les badges (Admin)</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 15,
  },
  backButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 20,
    padding: 8,
  },
  testButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 20,
    padding: 8,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  progressContainer: {
    marginBottom: 25,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 8,
  },
  progressGradient: {
    padding: 25,
    alignItems: 'center',
  },
  progressTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  progressText: {
    fontSize: 16,
    color: '#fff',
    marginBottom: 15,
    textAlign: 'center',
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderRadius: 4,
    marginBottom: 10,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#fff',
    borderRadius: 4,
  },
  progressPercentage: {
    fontSize: 14,
    color: '#fff',
    fontWeight: 'bold',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
    textAlign: 'center',
  },
  badgesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  badgeCard: {
    width: '48%',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    alignItems: 'center',
    minHeight: 180,
    position: 'relative',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  badgeIconContainer: {
    position: 'relative',
    marginBottom: 15,
  },
  unlockedIndicator: {
    position: 'absolute',
    top: -5,
    right: -5,
    backgroundColor: '#fff',
    borderRadius: 10,
  },
  badgeName: {
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
  },
  badgeDescription: {
    fontSize: 12,
    textAlign: 'center',
    marginBottom: 8,
    lineHeight: 16,
  },
  badgeRequirement: {
    fontSize: 10,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  lockedOverlay: {
    position: 'absolute',
    top: 10,
    right: 10,
  },
  tipsContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 20,
  },
  tipsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  tipText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
    lineHeight: 20,
  },
  adminContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  resetButton: {
    backgroundColor: 'rgba(255, 107, 107, 0.8)',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  resetButtonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
});