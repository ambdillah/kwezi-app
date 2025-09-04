import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  TextInput,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface UserProgress {
  id: string;
  user_name: string;
  exercise_id: string;
  score: number;
  completed_at: string;
}

export default function ProgressScreen() {
  const [userName, setUserName] = useState('');
  const [currentUser, setCurrentUser] = useState('');
  const [progress, setProgress] = useState<UserProgress[]>([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    totalScore: 0,
    completedExercises: 0,
    averageScore: 0,
    bestScore: 0,
  });

  useEffect(() => {
    loadUserName();
  }, []);

  useEffect(() => {
    if (currentUser) {
      fetchProgress();
    }
  }, [currentUser]);

  const loadUserName = async () => {
    try {
      const stored = await AsyncStorage.getItem('userName');
      if (stored) {
        setCurrentUser(stored);
        setUserName(stored);
      }
    } catch (error) {
      console.log('Error loading user name:', error);
    }
  };

  const saveUserName = async () => {
    if (!userName.trim()) {
      Alert.alert('Erreur', 'Entre ton prénom s\'il te plaît');
      return;
    }

    try {
      await AsyncStorage.setItem('userName', userName.trim());
      setCurrentUser(userName.trim());
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de sauvegarder le nom');
    }
  };

  const fetchProgress = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress/${encodeURIComponent(currentUser)}`
      );
      
      if (response.ok) {
        const data = await response.json();
        setProgress(data);
        calculateStats(data);
      }
    } catch (error) {
      console.log('Error fetching progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (progressData: UserProgress[]) => {
    if (progressData.length === 0) {
      setStats({ totalScore: 0, completedExercises: 0, averageScore: 0, bestScore: 0 });
      return;
    }

    const totalScore = progressData.reduce((sum, p) => sum + p.score, 0);
    const completedExercises = progressData.length;
    const averageScore = Math.round(totalScore / completedExercises);
    const bestScore = Math.max(...progressData.map(p => p.score));

    setStats({ totalScore, completedExercises, averageScore, bestScore });
  };

  const addTestProgress = async () => {
    if (!currentUser) return;

    try {
      const testProgress = {
        user_name: currentUser,
        exercise_id: 'test-exercise',
        score: Math.floor(Math.random() * 100) + 1
      };

      const response = await fetch(
        `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(testProgress)
        }
      );

      if (response.ok) {
        fetchProgress(); // Refresh data
        Alert.alert('Super!', 'Nouveau score ajouté! 🎉');
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible d\'ajouter le score');
    }
  };

  const getProgressLevel = () => {
    if (stats.averageScore >= 80) return { level: 'Expert', emoji: '🏆', color: '#FFD700' };
    if (stats.averageScore >= 60) return { level: 'Avancé', emoji: '🌟', color: '#4ECDC4' };
    if (stats.averageScore >= 40) return { level: 'Bon', emoji: '👍', color: '#96CEB4' };
    return { level: 'Débutant', emoji: '🌱', color: '#FF6B6B' };
  };

  if (!currentUser) {
    return (
      <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.header}>
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color="#000" />
            </TouchableOpacity>
            <Text style={styles.title}>Mon profil</Text>
            <View style={styles.placeholder} />
          </View>

          <View style={styles.welcomeContainer}>
            <Text style={styles.welcomeEmoji}>🐒</Text>
            <Text style={styles.welcomeTitle}>Salut petit mahorais!</Text>
            <Text style={styles.welcomeSubtitle}>
              Comment tu t'appelles? Les makis aimeraient te connaître! 🌺
            </Text>

            <View style={styles.inputContainer}>
              <TextInput
                style={styles.nameInput}
                placeholder="Ton prénom..."
                value={userName}
                onChangeText={setUserName}
                autoCapitalize="words"
                returnKeyType="done"
                onSubmitEditing={saveUserName}
              />
              <TouchableOpacity onPress={saveUserName} style={styles.saveButton}>
                <LinearGradient colors={['#4ECDC4', '#45B7D1']} style={styles.saveButtonGradient}>
                  <Text style={styles.saveButtonText}>C'est parti!</Text>
                  <Ionicons name="arrow-forward" size={20} color="#fff" />
                </LinearGradient>
              </TouchableOpacity>
            </View>
          </View>
        </SafeAreaView>
      </LinearGradient>
    );
  }

  const levelInfo = getProgressLevel();

  return (
    <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <Text style={styles.title}>Mes progrès</Text>
          <TouchableOpacity onPress={() => router.push('/admin')} style={styles.adminButton}>
            <Ionicons name="settings" size={24} color="#000" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* User Profile */}
          <View style={styles.profileCard}>
            <LinearGradient colors={[levelInfo.color, '#fff']} style={styles.profileGradient}>
              <Text style={styles.profileEmoji}>{levelInfo.emoji}</Text>
              <Text style={styles.profileName}>Kwezi {currentUser}!</Text>
              <Text style={styles.profileLevel}>Niveau: {levelInfo.level}</Text>
            </LinearGradient>
          </View>

          {/* Stats Cards */}
          <View style={styles.statsContainer}>
            <View style={styles.statCard}>
              <Text style={styles.statNumber}>{stats.totalScore}</Text>
              <Text style={styles.statLabel}>Points totaux</Text>
              <Text style={styles.statEmoji}>⭐</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statNumber}>{stats.completedExercises}</Text>
              <Text style={styles.statLabel}>Exercices</Text>
              <Text style={styles.statEmoji}>📚</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statNumber}>{stats.averageScore}%</Text>
              <Text style={styles.statLabel}>Moyenne</Text>
              <Text style={styles.statEmoji}>🎯</Text>
            </View>

            <View style={styles.statCard}>
              <Text style={styles.statNumber}>{stats.bestScore}</Text>
              <Text style={styles.statLabel}>Meilleur score</Text>
              <Text style={styles.statEmoji}>🏆</Text>
            </View>
          </View>

          {/* Progress History */}
          <View style={styles.historyContainer}>
            <Text style={styles.sectionTitle}>Historique des scores 📊</Text>
            
            {loading ? (
              <Text style={styles.loadingText}>Chargement... 🐒</Text>
            ) : progress.length === 0 ? (
              <View style={styles.emptyContainer}>
                <Text style={styles.emptyEmoji}>🌱</Text>
                <Text style={styles.emptyText}>
                  Tu n'as pas encore joué d'exercices!
                </Text>
                <Text style={styles.emptySubtext}>
                  Va dans "Jeux" pour commencer à apprendre! 🎮
                </Text>
                <TouchableOpacity 
                  onPress={addTestProgress} 
                  style={styles.testButton}
                >
                  <Text style={styles.testButtonText}>Ajouter un score test 🧪</Text>
                </TouchableOpacity>
              </View>
            ) : (
              progress.map((item, index) => (
                <View key={item.id} style={styles.progressItem}>
                  <View style={styles.progressHeader}>
                    <Text style={styles.progressScore}>{item.score} points</Text>
                    <Text style={styles.progressDate}>
                      {new Date(item.completed_at).toLocaleDateString('fr-FR')}
                    </Text>
                  </View>
                  <Text style={styles.progressExercise}>
                    Exercice #{index + 1}
                  </Text>
                </View>
              ))
            )}
          </View>

          {/* Quick Actions */}
          <View style={styles.quickActionsContainer}>
            <Text style={styles.sectionTitle}>Actions rapides 🚀</Text>
            
            <View style={styles.quickActionButtons}>
              <TouchableOpacity 
                style={styles.quickActionButton}
                onPress={() => router.push('/badges')}
              >
                <Ionicons name="trophy" size={24} color="#9B59B6" />
                <Text style={styles.quickActionText}>Badges</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={styles.quickActionButton}
                onPress={() => router.push('/offline')}
              >
                <Ionicons name="download" size={24} color="#4ECDC4" />
                <Text style={styles.quickActionText}>Hors-ligne</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={styles.quickActionButton}
                onPress={() => router.push('/export')}
              >
                <Ionicons name="share" size={24} color="#45B7D1" />
                <Text style={styles.quickActionText}>Exporter</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Encouragement */}
          <View style={styles.encouragementContainer}>
            <Text style={styles.encouragementText}>
              🌺 Continue comme ça! Les langues de Mayotte n'attendent que toi! 🐒
            </Text>
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
  adminButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 20,
    padding: 8,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  placeholder: {
    width: 40,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  welcomeContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 30,
  },
  welcomeEmoji: {
    fontSize: 80,
    marginBottom: 20,
  },
  welcomeTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#000',
    textAlign: 'center',
    marginBottom: 15,
  },
  welcomeSubtitle: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    marginBottom: 40,
    lineHeight: 22,
  },
  inputContainer: {
    width: '100%',
    alignItems: 'center',
  },
  nameInput: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 25,
    paddingHorizontal: 20,
    paddingVertical: 15,
    fontSize: 18,
    textAlign: 'center',
    width: '100%',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  saveButton: {
    width: '100%',
    borderRadius: 25,
    overflow: 'hidden',
  },
  saveButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 15,
    gap: 10,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  profileCard: {
    marginBottom: 25,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 8,
  },
  profileGradient: {
    padding: 25,
    alignItems: 'center',
  },
  profileEmoji: {
    fontSize: 50,
    marginBottom: 10,
  },
  profileName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 5,
  },
  profileLevel: {
    fontSize: 16,
    color: '#333',
    fontWeight: '600',
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  statCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    padding: 20,
    alignItems: 'center',
    width: '48%',
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    marginBottom: 5,
  },
  statEmoji: {
    fontSize: 20,
  },
  historyContainer: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
  },
  loadingText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#333',
    padding: 20,
  },
  emptyContainer: {
    alignItems: 'center',
    padding: 30,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
  },
  emptyEmoji: {
    fontSize: 50,
    marginBottom: 15,
  },
  emptyText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  testButton: {
    backgroundColor: '#4ECDC4',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  testButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  progressItem: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 5,
  },
  progressScore: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4ECDC4',
  },
  progressDate: {
    fontSize: 12,
    color: '#666',
  },
  progressExercise: {
    fontSize: 14,
    color: '#333',
  },
  quickActionsContainer: {
    marginBottom: 25,
  },
  quickActionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    gap: 15,
  },
  quickActionButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    padding: 15,
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  quickActionText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
    textAlign: 'center',
  },
  encouragementContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 30,
    alignItems: 'center',
  },
  encouragementText: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    fontWeight: '600',
    lineHeight: 22,
  },
});