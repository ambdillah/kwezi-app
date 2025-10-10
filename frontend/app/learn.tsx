import React, { useEffect, useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
  Image,
  Animated,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as Speech from 'expo-speech';
import { speakEducationalContent } from '../utils/feminineSpeechUtils';
import { speakWithMasculineVoice, testMasculineVoice } from '../utils/simpleMasculineVoice';
import { playWordAudio, playWordAllLanguages, hasAuthenticAudio } from '../utils/authenticAudioSystem';
import { playWordWithRealAudio, hasRealAuthenticAudio, getRealAudioInfo } from '../utils/realAuthenticAudioSystem';
import { playWordWithDualAudio, hasDualAudio, hasDualAudioForLanguage, getDualAudioInfo } from '../utils/dualAuthenticAudioSystem';
import YlangYlangFlower from '../components/YlangYlangFlower';

interface Word {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  difficulty: number;
  image_url?: string;
  // Anciens champs audio (compatibilité)
  has_authentic_audio?: boolean;
  audio_filename?: string;
  audio_pronunciation_lang?: string;
  audio_source?: string;
  audio_updated_at?: string;
  // Champs audio - TOUS les formats possibles dans la base
  dual_audio_system?: boolean;
  // Nouveau format (verbes, nouvelles expressions)
  audio_filename_shimaore?: string;
  audio_filename_kibouchi?: string;
  // Ancien format (famille, animaux, nature, etc.)
  shimoare_audio_filename?: string;
  kibouchi_audio_filename?: string;
  shimoare_has_audio?: boolean;
  kibouchi_has_audio?: boolean;
}

const CATEGORIES = [
  { key: 'famille', name: 'Famille', icon: 'people', color: '#FF6B6B' },
  { key: 'salutations', name: 'Salutations', icon: 'hand-left', color: '#4ECDC4' },
  { key: 'grammaire', name: 'Grammaire', icon: 'book', color: '#FF9500' },
  { key: 'couleurs', name: 'Couleurs', icon: 'color-palette', color: '#45B7D1' },
  { key: 'animaux', name: 'Animaux', icon: 'paw', color: '#96CEB4' },
  { key: 'nombres', name: 'Nombres', icon: 'calculator', color: '#FECA57' },
  { key: 'corps', name: 'Corps humain', icon: 'body', color: '#E67E22' },
  { key: 'nourriture', name: 'Nourriture', icon: 'restaurant', color: '#9B59B6' },
  { key: 'maison', name: 'Maison', icon: 'home', color: '#16A085' },
  { key: 'vetements', name: 'Vêtements', icon: 'shirt', color: '#E91E63' },
  { key: 'nature', name: 'Nature', icon: 'leaf', color: '#27AE60' },
  { key: 'transport', name: 'Transport', icon: 'car', color: '#3498DB' },
  { key: 'verbes', name: 'Verbes', icon: 'walk', color: '#8E44AD' },
  { key: 'adjectifs', name: 'Adjectifs', icon: 'text', color: '#F39C12' },
  { key: 'expressions', name: 'Expressions', icon: 'chatbubbles', color: '#FF6347' },
  { key: 'tradition', name: 'Tradition', icon: 'musical-notes', color: '#D63384' },
];

// Composant d'animation de chargement avec le maki
const LoadingAnimation = () => {
  const bounceAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Animation de rebond
    Animated.loop(
      Animated.sequence([
        Animated.timing(bounceAnim, {
          toValue: -20,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.timing(bounceAnim, {
          toValue: 0,
          duration: 500,
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Animation de rotation
    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 2000,
        useNativeDriver: true,
      })
    ).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <View style={styles.loadingContainer}>
      <Animated.View style={{ transform: [{ translateY: bounceAnim }] }}>
        <Text style={styles.makiEmoji}>🐒</Text>
      </Animated.View>
      <Animated.View style={{ transform: [{ rotate }] }}>
        <Ionicons name="flower" size={24} color="#FFD700" />
      </Animated.View>
      <Text style={styles.loadingText}>Chargement des mots...</Text>
      <Text style={styles.loadingSubText}>Le maki prépare ta leçon 📚</Text>
    </View>
  );
};

export default function LearnScreen() {
  const [words, setWords] = useState<Word[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [showAllWords, setShowAllWords] = useState(false);
  const [loadingAllWords, setLoadingAllWords] = useState(false);
  const [totalWordsCount, setTotalWordsCount] = useState(0);
  
  // États pour la recherche
  const [searchVisible, setSearchVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [allWordsForSearch, setAllWordsForSearch] = useState<Word[]>([]);

  const fetchWords = async (category?: string, loadAll: boolean = false) => {
    setLoading(true);
    try {
      const baseUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:3000';
      const url = category 
        ? `${baseUrl}/api/words?category=${category}`
        : `${baseUrl}/api/words`;
      
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setTotalWordsCount(data.length);
        
        // Si on ne charge pas tout et qu'il n'y a pas de catégorie, limiter à 50 mots
        if (!loadAll && !category && data.length > 50) {
          setWords(data.slice(0, 50));
          setShowAllWords(false);
        } else {
          setWords(data);
          setShowAllWords(true);
        }
      } else {
        Alert.alert('Erreur', 'Problème lors du chargement des mots');
      }
    } catch (error) {
      Alert.alert('Erreur', 'Connexion impossible au serveur');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Charger seulement 50 mots au démarrage pour un chargement rapide
    fetchWords('', false);
  }, []);

  const speakWord = async (text: string, language: 'fr' | 'shimaore' | 'kibouchi' = 'fr', word?: Word) => {
    try {
      if (word && language !== 'fr') {
        // Utiliser le nouveau système audio DUAL en priorité
        console.log(`🎯 Tentative prononciation ${language} pour "${word.french}"`);
        console.log(`   Système dual: ${word.dual_audio_system}`);
        console.log(`   Audio filename ${language}: ${language === 'shimaore' ? word.audio_filename_shimaore : word.audio_filename_kibouchi}`);
        console.log(`   Audio ancien système: ${word.audio_filename}`);
        
        await playWordWithDualAudio(word, language);
      } else {
        // Fallback vers la synthèse vocale pour français
        await speakEducationalContent(text, language);
      }
    } catch (error) {
      console.log('Erreur lors de la prononciation:', error);
      Alert.alert('Info', 'La prononciation audio n\'est pas disponible sur cet appareil.');
    }
  };

  const speakAllLanguages = async (word: Word) => {
    try {
      // Français
      await speakEducationalContent(word.french, 'fr');
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Shimaoré avec nouveau système dual
      await playWordWithDualAudio(word, 'shimaore');
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Kibouchi avec nouveau système dual
      await playWordWithDualAudio(word, 'kibouchi');
    } catch (error) {
      console.log('Erreur lors de la lecture de toutes les langues:', error);
      Alert.alert('Info', 'Problème avec la prononciation audio.');
    }
  };

  const selectCategory = (category: string) => {
    setSelectedCategory(category);
    fetchWords(category, false);
  };

  const clearCategory = () => {
    setSelectedCategory('');
    fetchWords('', false);
  };

  const loadAllWords = () => {
    fetchWords('', true);
  };

  return (
    <LinearGradient colors={['#FFD700', '#FFA500', '#000000']} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <Text style={styles.title}>Apprendre 📚</Text>
          <View style={styles.placeholder} />
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Categories */}
          <View style={styles.categoriesContainer}>
            <View style={styles.sectionTitleContainer}>
              <YlangYlangFlower size={24} />
              <Text style={styles.sectionTitle}> Choisir une catégorie</Text>
            </View>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categoriesScroll}>
              {CATEGORIES.map((category) => (
                <TouchableOpacity
                  key={category.key}
                  style={[
                    styles.categoryCard,
                    { backgroundColor: category.color },
                    selectedCategory === category.key && styles.selectedCategory,
                  ]}
                  onPress={() => selectCategory(category.key)}
                >
                  <Ionicons name={category.icon as any} size={32} color="#fff" />
                  <Text style={styles.categoryName}>{category.name}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
            
            {selectedCategory && (
              <TouchableOpacity onPress={clearCategory} style={styles.clearButton}>
                <Text style={styles.clearButtonText}>Voir tout</Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Words List */}
          <View style={styles.wordsContainer}>
            <View style={styles.wordsHeaderContainer}>
              <Text style={styles.sectionTitle}>
                {selectedCategory 
                  ? `Mots de ${CATEGORIES.find(c => c.key === selectedCategory)?.name}` 
                  : 'Tous les mots'} ({words.length}{!showAllWords && totalWordsCount > 50 && !selectedCategory ? `/${totalWordsCount}` : ''})
              </Text>
              
              {!showAllWords && !selectedCategory && totalWordsCount > 50 && (
                <TouchableOpacity onPress={loadAllWords} style={styles.loadAllButton}>
                  <Ionicons name="download" size={16} color="#fff" />
                  <Text style={styles.loadAllButtonText}>Voir tout ({totalWordsCount})</Text>
                </TouchableOpacity>
              )}
            </View>
            
            {loading ? (
              <LoadingAnimation />
            ) : (
              words.map((word) => (
                <View key={word.id} style={styles.wordCard}>
                  <View style={styles.wordHeader}>
                    <View style={styles.frenchWordContainer}>
                      {word.image_url && (
                        <View style={styles.wordImageContainer}>
                          {word.image_url.startsWith('data:image/svg') || word.image_url.startsWith('http') ? (
                            <View 
                              style={[
                                styles.wordImage,
                                { 
                                  backgroundColor: '#f0f0f0',
                                  borderWidth: 1, 
                                  borderColor: '#ddd'
                                }
                              ]}
                            >
                              <Image 
                                source={{ uri: word.image_url }} 
                                style={styles.wordImageInner} 
                                resizeMode="contain"
                                onError={(e) => console.log('Image load error:', e)}
                              />
                            </View>
                          ) : (
                            <View style={styles.emojiContainer}>
                              <Text style={styles.emojiText}>{word.image_url}</Text>
                            </View>
                          )}
                        </View>
                      )}
                      <Text style={styles.frenchWord}>{word.french}</Text>
                    </View>
                    <View style={styles.difficultyContainer}>
                      {[...Array(word.difficulty)].map((_, i) => (
                        <Ionicons key={i} name="star" size={16} color="#FFD700" />
                      ))}
                    </View>
                  </View>
                  
                  <View style={styles.translationsContainer}>
                    <TouchableOpacity 
                      style={styles.translationRow}
                      onPress={() => speakWord(word.shimaore, 'shimaore', word)}
                    >
                      <Text style={styles.languageLabel}>Shimaoré:</Text>
                      <Text style={styles.translationText}>{word.shimaore}</Text>
                      <View style={styles.audioButtonContainer}>
                        {hasDualAudioForLanguage(word, 'shimaore') && (
                          <Ionicons name="musical-notes" size={12} color="#FFD700" />
                        )}
                        <Ionicons name="volume-high" size={20} color="#4ECDC4" />
                      </View>
                    </TouchableOpacity>
                    
                    <TouchableOpacity 
                      style={styles.translationRow}
                      onPress={() => speakWord(word.kibouchi, 'kibouchi', word)}
                    >
                      <Text style={styles.languageLabel}>Kibouchi:</Text>
                      <Text style={styles.translationText}>{word.kibouchi}</Text>
                      <View style={styles.audioButtonContainer}>
                        {hasDualAudioForLanguage(word, 'kibouchi') && (
                          <Ionicons name="musical-notes" size={12} color="#FFD700" />
                        )}
                        <Ionicons name="volume-high" size={20} color="#FF6B6B" />
                      </View>
                    </TouchableOpacity>
                  </View>
                  
                  <View style={styles.pronunciationButtons}>
                    <TouchableOpacity 
                      style={styles.pronounceButton}
                      onPress={() => speakWord(word.french, 'fr')}
                    >
                      <Text style={styles.pronounceButtonText}>🇫🇷 Français</Text>
                      <Ionicons name="play" size={16} color="#fff" />
                    </TouchableOpacity>
                    
                    <TouchableOpacity 
                      style={[styles.pronounceButton, styles.pronounceAllButton]}
                      onPress={() => speakAllLanguages(word)}
                    >
                      <Text style={styles.pronounceButtonText}>🔊 Tout écouter</Text>
                      <Ionicons name="musical-notes" size={16} color="#fff" />
                    </TouchableOpacity>
                  </View>
                </View>
              ))
            )}
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
  categoriesContainer: {
    marginBottom: 30,
  },
  sectionTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  categoriesScroll: {
    marginBottom: 10,
  },
  categoryCard: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 100,
    height: 80,
    borderRadius: 15,
    marginRight: 15,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  selectedCategory: {
    borderWidth: 3,
    borderColor: '#000',
  },
  categoryName: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
    marginTop: 5,
    textAlign: 'center',
  },
  clearButton: {
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
  },
  clearButtonText: {
    color: '#000',
    fontWeight: '600',
  },
  wordsContainer: {
    paddingBottom: 30,
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 50,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 20,
    marginVertical: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  loadingText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginTop: 15,
  },
  wordCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
  },
  wordHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  frenchWordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: 10,
  },
  wordImageContainer: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  wordImage: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  wordImageInner: {
    width: '100%',
    height: '100%',
  },
  emojiContainer: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 8,
  },
  emojiText: {
    fontSize: 24,
    textAlign: 'center',
  },
  frenchWord: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  difficultyContainer: {
    flexDirection: 'row',
  },
  translationsContainer: {
    marginBottom: 15,
  },
  translationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: 'rgba(0, 0, 0, 0.05)',
    borderRadius: 10,
    marginBottom: 8,
  },
  languageLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    width: 80,
  },
  translationText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  pronunciationButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
    marginTop: 10,
  },
  pronounceButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#4ECDC4',
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 20,
    gap: 6,
    flex: 1,
    minHeight: 44, // Taille tactile minimale
  },
  pronounceAllButton: {
    backgroundColor: '#FF6B6B', // Couleur différente pour le bouton "Tout écouter"
  },
  pronounceButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
    textAlign: 'center',
  },
  audioButtonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  wordsHeaderContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
    gap: 10,
  },
  loadAllButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF6B6B',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 5,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  loadAllButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 12,
  },
  makiEmoji: {
    fontSize: 64,
    marginBottom: 15,
  },
  loadingSubText: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
    fontStyle: 'italic',
  },
});