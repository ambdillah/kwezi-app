import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
  Share,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as FileSystem from 'expo-file-system';

interface ExportData {
  userData: {
    userName: string;
    profileLevel: string;
    unlockedBadges: string[];
    createdAt: string;
  };
  progress: any[];
  offlineData?: any;
  statistics: {
    totalScore: number;
    completedExercises: number;
    averageScore: number;
    bestScore: number;
    badgesCount: number;
  };
  exportDate: string;
  appVersion: string;
}

export default function ExportScreen() {
  const [userData, setUserData] = useState<any>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [dataSize, setDataSize] = useState('0 KB');
  const [lastExport, setLastExport] = useState<string | null>(null);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      // Load user name
      const userName = await AsyncStorage.getItem('userName');
      
      // Load badges
      const badgesData = await AsyncStorage.getItem('userBadges');
      const unlockedBadges = badgesData ? JSON.parse(badgesData) : [];
      
      // Load offline data
      const offlineData = await AsyncStorage.getItem('offlineData');
      const offline = offlineData ? JSON.parse(offlineData) : null;
      
      // Load last export date
      const lastExportDate = await AsyncStorage.getItem('lastExportDate');
      setLastExport(lastExportDate);

      // Get progress from server if user exists
      let progress = [];
      let stats = { totalScore: 0, completedExercises: 0, averageScore: 0, bestScore: 0 };

      if (userName) {
        try {
          const response = await fetch(
            `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress/${encodeURIComponent(userName)}`
          );
          if (response.ok) {
            progress = await response.json();
            
            // Calculate statistics
            if (progress.length > 0) {
              const totalScore = progress.reduce((sum: number, p: any) => sum + p.score, 0);
              stats = {
                totalScore,
                completedExercises: progress.length,
                averageScore: Math.round(totalScore / progress.length),
                bestScore: Math.max(...progress.map((p: any) => p.score))
              };
            }
          }
        } catch (error) {
          console.log('Error fetching progress:', error);
        }
      }

      const data = {
        userName,
        unlockedBadges,
        progress,
        stats,
        offline
      };

      setUserData(data);
      
      // Calculate data size
      const dataString = JSON.stringify(data);
      const sizeInBytes = new Blob([dataString]).size;
      const sizeInKB = (sizeInBytes / 1024).toFixed(1);
      setDataSize(`${sizeInKB} KB`);

    } catch (error) {
      console.log('Error loading user data:', error);
    }
  };

  const createExportData = (): ExportData => {
    const level = getProfileLevel(userData?.stats?.averageScore || 0);
    
    return {
      userData: {
        userName: userData?.userName || 'Utilisateur anonyme',
        profileLevel: level.level,
        unlockedBadges: userData?.unlockedBadges || [],
        createdAt: new Date().toISOString(),
      },
      progress: userData?.progress || [],
      offlineData: userData?.offline,
      statistics: {
        totalScore: userData?.stats?.totalScore || 0,
        completedExercises: userData?.stats?.completedExercises || 0,
        averageScore: userData?.stats?.averageScore || 0,
        bestScore: userData?.stats?.bestScore || 0,
        badgesCount: userData?.unlockedBadges?.length || 0,
      },
      exportDate: new Date().toISOString(),
      appVersion: '1.0.0'
    };
  };

  const getProfileLevel = (averageScore: number) => {
    if (averageScore >= 80) return { level: 'Expert', emoji: '🏆' };
    if (averageScore >= 60) return { level: 'Avancé', emoji: '🌟' };
    if (averageScore >= 40) return { level: 'Bon', emoji: '👍' };
    return { level: 'Débutant', emoji: '🌱' };
  };

  const exportAsJSON = async () => {
    setIsExporting(true);
    
    try {
      const exportData = createExportData();
      const jsonString = JSON.stringify(exportData, null, 2);
      
      // Create file in document directory
      const fileName = `mayotte_app_${userData?.userName || 'user'}_${Date.now()}.json`;
      const filePath = `${FileSystem.documentDirectory}${fileName}`;
      
      await FileSystem.writeAsStringAsync(filePath, jsonString, {
        encoding: FileSystem.EncodingType.UTF8,
      });

      // Save export date
      await AsyncStorage.setItem('lastExportDate', new Date().toISOString());
      setLastExport(new Date().toISOString());

      Alert.alert(
        'Export réussi! 🎉',
        `Tes données ont été exportées vers:\n${fileName}`,
        [
          {
            text: 'Partager',
            onPress: () => shareFile(filePath, fileName)
          },
          { text: 'OK' }
        ]
      );
      
    } catch (error) {
      Alert.alert('Erreur', 'Impossible d\'exporter les données');
      console.log('Export error:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const shareFile = async (filePath: string, fileName: string) => {
    try {
      await Share.share({
        url: filePath,
        title: 'Mes données Mayotte App',
        message: `Voici mes progrès dans l'apprentissage du Shimaoré et Kibouchi! 🌺`
      });
    } catch (error) {
      console.log('Share error:', error);
    }
  };

  const exportAsText = async () => {
    setIsExporting(true);

    try {
      const exportData = createExportData();
      const level = getProfileLevel(exportData.statistics.averageScore);
      
      const textContent = `
🌺 MES PROGRÈS DANS L'APPRENTISSAGE DES LANGUES DE MAYOTTE 🌺

👤 PROFIL UTILISATEUR
Nom: ${exportData.userData.userName}
Niveau: ${level.emoji} ${exportData.userData.profileLevel}
Date d'export: ${new Date(exportData.exportDate).toLocaleDateString('fr-FR')}

📊 STATISTIQUES
Points totaux: ${exportData.statistics.totalScore} ⭐
Exercices complétés: ${exportData.statistics.completedExercises} 📚
Score moyen: ${exportData.statistics.averageScore}% 🎯
Meilleur score: ${exportData.statistics.bestScore} 🏆
Badges débloqués: ${exportData.statistics.badgesCount} 🏅

🎮 HISTORIQUE DES SCORES
${exportData.progress.length > 0 
  ? exportData.progress.map((p: any, i: number) => 
      `${i + 1}. ${p.score} points - ${new Date(p.completed_at).toLocaleDateString('fr-FR')}`
    ).join('\n')
  : 'Aucun exercice complété'}

🏆 BADGES DÉBLOQUÉS
${exportData.userData.unlockedBadges.length > 0
  ? exportData.userData.unlockedBadges.map((badge: string) => `✅ ${badge}`).join('\n')
  : 'Aucun badge débloqué'}

📱 Application: Mayotte - Apprendre Shimaoré & Kibouchi
Version: ${exportData.appVersion}
      `;

      const fileName = `mayotte_rapport_${exportData.userData.userName}_${Date.now()}.txt`;
      const filePath = `${FileSystem.documentDirectory}${fileName}`;
      
      await FileSystem.writeAsStringAsync(filePath, textContent, {
        encoding: FileSystem.EncodingType.UTF8,
      });

      // Save export date
      await AsyncStorage.setItem('lastExportDate', new Date().toISOString());
      setLastExport(new Date().toISOString());

      Alert.alert(
        'Rapport créé! 📄',
        `Ton rapport de progression a été créé:\n${fileName}`,
        [
          {
            text: 'Partager',
            onPress: () => shareFile(filePath, fileName)
          },
          { text: 'OK' }
        ]
      );

    } catch (error) {
      Alert.alert('Erreur', 'Impossible de créer le rapport');
      console.log('Text export error:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const clearExportHistory = async () => {
    Alert.alert(
      'Effacer l\'historique',
      'Veux-tu effacer l\'historique des exports?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Effacer',
          style: 'destructive',
          onPress: async () => {
            await AsyncStorage.removeItem('lastExportDate');
            setLastExport(null);
            Alert.alert('Historique effacé', 'L\'historique des exports a été supprimé');
          }
        }
      ]
    );
  };

  const level = userData ? getProfileLevel(userData.stats?.averageScore || 0) : { level: 'Débutant', emoji: '🌱' };

  return (
    <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <Text style={styles.title}>Export des données 📤</Text>
          <View style={styles.placeholder} />
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* User Summary */}
          <View style={styles.summaryContainer}>
            <LinearGradient colors={['#4ECDC4', '#45B7D1']} style={styles.summaryGradient}>
              <Text style={styles.summaryEmoji}>{level.emoji}</Text>
              <Text style={styles.summaryTitle}>
                {userData?.userName || 'Utilisateur'} - Niveau {level.level}
              </Text>
              <Text style={styles.summaryStats}>
                {userData?.stats?.totalScore || 0} points • {userData?.unlockedBadges?.length || 0} badges
              </Text>
              <Text style={styles.dataSize}>Taille des données: {dataSize}</Text>
            </LinearGradient>
          </View>

          {/* Export Options */}
          <Text style={styles.sectionTitle}>Options d'export 📋</Text>
          
          <View style={styles.exportContainer}>
            <TouchableOpacity 
              onPress={exportAsJSON}
              style={[styles.exportButton, { backgroundColor: '#4ECDC4' }]}
              disabled={isExporting}
            >
              <View style={styles.exportButtonContent}>
                <Ionicons name="code" size={32} color="#fff" />
                <View style={styles.exportButtonText}>
                  <Text style={styles.exportButtonTitle}>Export complet (JSON)</Text>
                  <Text style={styles.exportButtonDescription}>
                    Toutes les données détaillées pour sauvegarde technique
                  </Text>
                </View>
              </View>
            </TouchableOpacity>

            <TouchableOpacity 
              onPress={exportAsText}
              style={[styles.exportButton, { backgroundColor: '#45B7D1' }]}
              disabled={isExporting}
            >
              <View style={styles.exportButtonContent}>
                <Ionicons name="document-text" size={32} color="#fff" />
                <View style={styles.exportButtonText}>
                  <Text style={styles.exportButtonTitle}>Rapport de progression</Text>
                  <Text style={styles.exportButtonDescription}>
                    Résumé lisible de tes progrès à partager
                  </Text>
                </View>
              </View>
            </TouchableOpacity>
          </View>

          {/* Export History */}
          <View style={styles.historyContainer}>
            <Text style={styles.sectionTitle}>Historique d'export 📅</Text>
            
            {lastExport ? (
              <View style={styles.historyCard}>
                <Ionicons name="checkmark-circle" size={24} color="#4CAF50" />
                <View style={styles.historyText}>
                  <Text style={styles.historyTitle}>Dernier export</Text>
                  <Text style={styles.historyDate}>
                    {new Date(lastExport).toLocaleDateString('fr-FR')} à {new Date(lastExport).toLocaleTimeString('fr-FR')}
                  </Text>
                </View>
                <TouchableOpacity onPress={clearExportHistory} style={styles.clearHistoryButton}>
                  <Ionicons name="trash" size={16} color="#FF6B6B" />
                </TouchableOpacity>
              </View>
            ) : (
              <View style={styles.noHistoryCard}>
                <Ionicons name="time" size={32} color="#999" />
                <Text style={styles.noHistoryText}>Aucun export effectué</Text>
              </View>
            )}
          </View>

          {/* What's Included */}
          <View style={styles.includedContainer}>
            <Text style={styles.sectionTitle}>Contenu des exports 📦</Text>
            
            <View style={styles.includedItem}>
              <Ionicons name="person" size={20} color="#4ECDC4" />
              <Text style={styles.includedText}>Informations du profil utilisateur</Text>
            </View>
            
            <View style={styles.includedItem}>
              <Ionicons name="bar-chart" size={20} color="#4ECDC4" />
              <Text style={styles.includedText}>Toutes les statistiques et scores</Text>
            </View>
            
            <View style={styles.includedItem}>
              <Ionicons name="trophy" size={20} color="#4ECDC4" />
              <Text style={styles.includedText}>Badges débloqués et progrès</Text>
            </View>
            
            <View style={styles.includedItem}>
              <Ionicons name="game-controller" size={20} color="#4ECDC4" />
              <Text style={styles.includedText}>Historique des exercices</Text>
            </View>
            
            <View style={styles.includedItem}>
              <Ionicons name="download" size={20} color="#4ECDC4" />
              <Text style={styles.includedText}>Données hors-ligne (si disponibles)</Text>
            </View>
          </View>

          {/* Tips */}
          <View style={styles.tipsContainer}>
            <Text style={styles.tipsTitle}>💡 Conseils d'utilisation :</Text>
            <Text style={styles.tipText}>
              📤 Partage tes progrès avec tes parents ou enseignants
            </Text>
            <Text style={styles.tipText}>
              💾 Sauvegarde régulièrement tes données importantes
            </Text>
            <Text style={styles.tipText}>
              📱 Les fichiers sont sauvés dans le dossier Documents
            </Text>
            <Text style={styles.tipText}>
              🌺 Montre tes progrès en shimaoré et kibouchi!
            </Text>
          </View>

          {isExporting && (
            <View style={styles.loadingContainer}>
              <Text style={styles.loadingText}>Export en cours... 🐒</Text>
            </View>
          )}
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
  summaryContainer: {
    marginBottom: 25,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 8,
  },
  summaryGradient: {
    padding: 25,
    alignItems: 'center',
  },
  summaryEmoji: {
    fontSize: 50,
    marginBottom: 10,
  },
  summaryTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
    textAlign: 'center',
  },
  summaryStats: {
    fontSize: 16,
    color: '#fff',
    marginBottom: 8,
    opacity: 0.9,
  },
  dataSize: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
  },
  exportContainer: {
    marginBottom: 25,
    gap: 15,
  },
  exportButton: {
    borderRadius: 15,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  exportButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  exportButtonText: {
    flex: 1,
    marginLeft: 15,
  },
  exportButtonTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  exportButtonDescription: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
    lineHeight: 18,
  },
  historyContainer: {
    marginBottom: 25,
  },
  historyCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  historyText: {
    flex: 1,
    marginLeft: 15,
  },
  historyTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  historyDate: {
    fontSize: 14,
    color: '#666',
  },
  clearHistoryButton: {
    padding: 8,
  },
  noHistoryCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 30,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  noHistoryText: {
    fontSize: 16,
    color: '#999',
    marginTop: 10,
  },
  includedContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 25,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  includedItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
  },
  includedText: {
    fontSize: 14,
    color: '#333',
    marginLeft: 15,
    flex: 1,
  },
  tipsContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 30,
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
    marginBottom: 8,
    lineHeight: 20,
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    fontSize: 16,
    color: '#333',
    fontWeight: 'bold',
  },
});