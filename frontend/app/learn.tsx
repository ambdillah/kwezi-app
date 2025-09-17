import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as Speech from 'expo-speech';
import { speakText } from '../utils/speechUtils';
import { playWordAudio, playWordAllLanguages, hasAuthenticAudio } from '../utils/authenticAudioSystem';

interface Word {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  difficulty: number;
  image_url?: string;
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

export default function LearnScreen() {
  const [words, setWords] = useState<Word[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const fetchWords = async (category?: string) => {
    setLoading(true);
    try {
      const baseUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:3000';
      const url = category 
        ? `${baseUrl}/api/words?category=${category}`
        : `${baseUrl}/api/words`;
      
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setWords(data);
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
    fetchWords();
  }, []);

  const speakWord = async (text: string, language: 'fr' | 'shimaore' | 'kibouchi' = 'fr') => {
    try {
      await speakText(text, language);
    } catch (error) {
      console.log('Erreur lors de la prononciation:', error);
      Alert.alert('Info', 'La prononciation audio n\'est pas disponible sur cet appareil.');
    }
  };

  const speakAllLanguages = async (word: Word) => {
    try {
      await speakWordAllLanguages(word);
    } catch (error) {
      console.log('Erreur lors de la lecture de toutes les langues:', error);
      Alert.alert('Info', 'Problème avec la prononciation audio.');
    }
  };

  const selectCategory = (category: string) => {
    setSelectedCategory(category);
    fetchWords(category);
  };

  const clearCategory = () => {
    setSelectedCategory('');
    fetchWords();
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
            <Text style={styles.sectionTitle}>Choisir une catégorie 🌺</Text>
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
            <Text style={styles.sectionTitle}>
              {selectedCategory 
                ? `Mots de ${CATEGORIES.find(c => c.key === selectedCategory)?.name}` 
                : 'Tous les mots'} ({words.length})
            </Text>
            
            {loading ? (
              <View style={styles.loadingContainer}>
                <Text style={styles.loadingText}>Chargement... 🐒</Text>
              </View>
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
                      onPress={() => speakWord(word.shimaore, 'shimaore')}
                    >
                      <Text style={styles.languageLabel}>Shimaoré:</Text>
                      <Text style={styles.translationText}>{word.shimaore}</Text>
                      <Ionicons name="volume-high" size={20} color="#4ECDC4" />
                    </TouchableOpacity>
                    
                    <TouchableOpacity 
                      style={styles.translationRow}
                      onPress={() => speakWord(word.kibouchi, 'kibouchi')}
                    >
                      <Text style={styles.languageLabel}>Kibouchi:</Text>
                      <Text style={styles.translationText}>{word.kibouchi}</Text>
                      <Ionicons name="volume-high" size={20} color="#FF6B6B" />
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
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
    padding: 30,
  },
  loadingText: {
    fontSize: 18,
    color: '#333',
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
});