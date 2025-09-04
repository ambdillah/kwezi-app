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
import NetInfo from '@react-native-netinfo/netinfo';

interface OfflineData {
  words: any[];
  exercises: any[];
  userProgress: any[];
  lastSync: string;
}

export default function OfflineScreen() {
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [offlineData, setOfflineData] = useState<OfflineData | null>(null);
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'success' | 'error'>('idle');
  const [dataSize, setDataSize] = useState<string>('0 KB');

  useEffect(() => {
    checkNetworkStatus();
    loadOfflineData();
  }, []);

  const checkNetworkStatus = () => {
    NetInfo.fetch().then(state => {
      setIsConnected(state.isConnected);
    });

    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected);
    });

    return unsubscribe;
  };

  const loadOfflineData = async () => {
    try {
      const stored = await AsyncStorage.getItem('offlineData');
      if (stored) {
        const data = JSON.parse(stored);
        setOfflineData(data);
        
        // Calculate data size
        const sizeInBytes = new Blob([stored]).size;
        const sizeInKB = (sizeInBytes / 1024).toFixed(1);
        setDataSize(`${sizeInKB} KB`);
      }
    } catch (error) {
      console.log('Error loading offline data:', error);
    }
  };

  const downloadOfflineData = async () => {
    if (!isConnected) {
      Alert.alert('Pas de connexion', 'Connecte-toi à internet pour télécharger les données');
      return;
    }

    setSyncStatus('syncing');
    
    try {
      // Download words
      const wordsResponse = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`);
      const words = wordsResponse.ok ? await wordsResponse.json() : [];

      // Download exercises
      const exercisesResponse = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/exercises`);
      const exercises = exercisesResponse.ok ? await exercisesResponse.json() : [];

      // Get user progress
      const userName = await AsyncStorage.getItem('userName');
      let userProgress = [];
      if (userName) {
        const progressResponse = await fetch(
          `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/progress/${encodeURIComponent(userName)}`
        );
        userProgress = progressResponse.ok ? await progressResponse.json() : [];
      }

      const offlineData: OfflineData = {
        words,
        exercises,
        userProgress,
        lastSync: new Date().toISOString()
      };

      await AsyncStorage.setItem('offlineData', JSON.stringify(offlineData));
      setOfflineData(offlineData);
      
      // Calculate and update data size
      const sizeInBytes = new Blob([JSON.stringify(offlineData)]).size;
      const sizeInKB = (sizeInBytes / 1024).toFixed(1);
      setDataSize(`${sizeInKB} KB`);

      setSyncStatus('success');
      Alert.alert('Succès!', 'Données téléchargées pour une utilisation hors-ligne! 🎉');
      
      setTimeout(() => setSyncStatus('idle'), 3000);
    } catch (error) {
      setSyncStatus('error');
      Alert.alert('Erreur', 'Impossible de télécharger les données');
      setTimeout(() => setSyncStatus('idle'), 3000);
    }
  };

  const clearOfflineData = async () => {
    Alert.alert(
      'Supprimer les données hors-ligne',
      'Es-tu sûr de vouloir supprimer toutes les données téléchargées?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Supprimer',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('offlineData');
              setOfflineData(null);
              setDataSize('0 KB');
              Alert.alert('Données supprimées', 'Les données hors-ligne ont été effacées');
            } catch (error) {
              Alert.alert('Erreur', 'Impossible de supprimer les données');
            }
          }
        }
      ]
    );
  };

  const getConnectionIcon = () => {
    if (isConnected === null) return 'help-circle';
    return isConnected ? 'wifi' : 'wifi-off';
  };

  const getConnectionColor = () => {
    if (isConnected === null) return '#FFA500';
    return isConnected ? '#4CAF50' : '#F44336';
  };

  const getConnectionText = () => {
    if (isConnected === null) return 'Vérification...';
    return isConnected ? 'Connecté à Internet' : 'Hors ligne';
  };

  const getSyncButtonText = () => {
    switch (syncStatus) {
      case 'syncing': return 'Téléchargement...';
      case 'success': return 'Téléchargé! ✅';
      case 'error': return 'Erreur ❌';
      default: return 'Télécharger pour hors-ligne';
    }
  };

  return (
    <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <Text style={styles.title}>Mode Hors-ligne 📡</Text>
          <View style={styles.placeholder} />
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Connection Status */}
          <View style={styles.statusContainer}>
            <LinearGradient 
              colors={[getConnectionColor(), '#fff']} 
              style={styles.statusGradient}
            >
              <Ionicons 
                name={getConnectionIcon() as any} 
                size={40} 
                color="#fff" 
              />
              <Text style={styles.statusTitle}>{getConnectionText()}</Text>
              <Text style={styles.statusSubtitle}>
                {isConnected 
                  ? 'Tu peux utiliser toutes les fonctionnalités' 
                  : 'Utilise les données téléchargées'
                }
              </Text>
            </LinearGradient>
          </View>

          {/* Offline Data Status */}
          <View style={styles.dataContainer}>
            <Text style={styles.sectionTitle}>Données hors-ligne 💾</Text>
            
            {offlineData ? (
              <View style={styles.dataCard}>
                <View style={styles.dataHeader}>
                  <Ionicons name="download-done" size={32} color="#4CAF50" />
                  <Text style={styles.dataTitle}>Données disponibles</Text>
                </View>
                
                <View style={styles.dataStats}>
                  <View style={styles.statItem}>
                    <Text style={styles.statNumber}>{offlineData.words.length}</Text>
                    <Text style={styles.statLabel}>Mots</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Text style={styles.statNumber}>{offlineData.exercises.length}</Text>
                    <Text style={styles.statLabel}>Exercices</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Text style={styles.statNumber}>{offlineData.userProgress.length}</Text>
                    <Text style={styles.statLabel}>Progrès</Text>
                  </View>
                </View>
                
                <Text style={styles.dataSize}>Taille: {dataSize}</Text>
                <Text style={styles.lastSync}>
                  Dernière sync: {new Date(offlineData.lastSync).toLocaleDateString('fr-FR')}
                </Text>
              </View>
            ) : (
              <View style={styles.noDataCard}>
                <Ionicons name="cloud-download" size={48} color="#999" />
                <Text style={styles.noDataTitle}>Aucune donnée hors-ligne</Text>
                <Text style={styles.noDataText}>
                  Télécharge les données pour utiliser l'app sans connexion
                </Text>
              </View>
            )}
          </View>

          {/* Actions */}
          <View style={styles.actionsContainer}>
            <TouchableOpacity 
              onPress={downloadOfflineData} 
              style={[
                styles.actionButton,
                { backgroundColor: '#4ECDC4' },
                syncStatus === 'syncing' && styles.disabledButton
              ]}
              disabled={syncStatus === 'syncing'}
            >
              <Ionicons 
                name={syncStatus === 'syncing' ? 'download' : 'cloud-download'} 
                size={24} 
                color="#fff" 
              />
              <Text style={styles.actionButtonText}>
                {getSyncButtonText()}
              </Text>
            </TouchableOpacity>

            {offlineData && (
              <TouchableOpacity 
                onPress={clearOfflineData} 
                style={[styles.actionButton, { backgroundColor: '#FF6B6B' }]}
              >
                <Ionicons name="trash" size={24} color="#fff" />
                <Text style={styles.actionButtonText}>Effacer les données</Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Offline Features */}
          <View style={styles.featuresContainer}>
            <Text style={styles.sectionTitle}>Fonctionnalités hors-ligne 🌟</Text>
            
            <View style={styles.featureItem}>
              <Ionicons name="book" size={24} color="#4ECDC4" />
              <View style={styles.featureText}>
                <Text style={styles.featureTitle}>Apprentissage</Text>
                <Text style={styles.featureDescription}>
                  Consulte tous les mots en shimaoré et kibouchi
                </Text>
              </View>
              <Ionicons 
                name={offlineData ? 'checkmark-circle' : 'close-circle'} 
                size={24} 
                color={offlineData ? '#4CAF50' : '#999'} 
              />
            </View>

            <View style={styles.featureItem}>
              <Ionicons name="game-controller" size={24} color="#4ECDC4" />
              <View style={styles.featureText}>
                <Text style={styles.featureTitle}>Jeux</Text>
                <Text style={styles.featureDescription}>
                  Joue aux jeux d'association avec tes mots téléchargés
                </Text>
              </View>
              <Ionicons 
                name={offlineData ? 'checkmark-circle' : 'close-circle'} 
                size={24} 
                color={offlineData ? '#4CAF50' : '#999'} 
              />
            </View>

            <View style={styles.featureItem}>
              <Ionicons name="bar-chart" size={24} color="#4ECDC4" />
              <View style={styles.featureText}>
                <Text style={styles.featureTitle}>Progrès</Text>
                <Text style={styles.featureDescription}>
                  Vois tes statistiques même sans connexion
                </Text>
              </View>
              <Ionicons 
                name={offlineData ? 'checkmark-circle' : 'close-circle'} 
                size={24} 
                color={offlineData ? '#4CAF50' : '#999'} 
              />
            </View>
          </View>

          {/* Tips */}
          <View style={styles.tipsContainer}>
            <Text style={styles.tipsTitle}>💡 Conseils pour le mode hors-ligne :</Text>
            <Text style={styles.tipText}>
              📶 Télécharge les données quand tu as du WiFi
            </Text>
            <Text style={styles.tipText}>
              🔄 Met à jour régulièrement pour avoir le dernier contenu
            </Text>
            <Text style={styles.tipText}>
              💾 Les données sont sauvegardées sur ton appareil
            </Text>
            <Text style={styles.tipText}>
              🎮 Tous les jeux fonctionnent hors-ligne une fois téléchargés
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
  statusContainer: {
    marginBottom: 25,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 8,
  },
  statusGradient: {
    padding: 25,
    alignItems: 'center',
  },
  statusTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 10,
    marginBottom: 5,
  },
  statusSubtitle: {
    fontSize: 14,
    color: '#fff',
    textAlign: 'center',
    opacity: 0.9,
  },
  dataContainer: {
    marginBottom: 25,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
  },
  dataCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  dataHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  dataTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 15,
  },
  dataStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 15,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4ECDC4',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  dataSize: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 5,
  },
  lastSync: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  noDataCard: {
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
  noDataTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 15,
    marginBottom: 10,
  },
  noDataText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    lineHeight: 20,
  },
  actionsContainer: {
    marginBottom: 25,
    gap: 15,
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 15,
    borderRadius: 15,
    gap: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  disabledButton: {
    opacity: 0.7,
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  featuresContainer: {
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
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  featureText: {
    flex: 1,
    marginLeft: 15,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
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
});