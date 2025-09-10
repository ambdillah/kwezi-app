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
  Modal,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';

interface Word {
  id: string;
  french: string;
  shimaore: string;
  kibouchi: string;
  category: string;
  difficulty: number;
  image_base64?: string;
}

const CATEGORIES = [
  'famille', 'salutations', 'grammaire', 'couleurs', 'animaux', 'nombres', 'corps', 'nourriture', 'maison', 'vetements', 'nature', 'transport', 'verbes', 'adjectifs', 'expressions'
];

export default function AdminScreen() {
  const [words, setWords] = useState<Word[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingWord, setEditingWord] = useState<Word | null>(null);
  const [formData, setFormData] = useState({
    french: '',
    shimaore: '',
    kibouchi: '',
    category: 'famille',
    difficulty: 1,
    image_base64: '',
  });

  useEffect(() => {
    fetchWords();
    initializeContent();
  }, []);

  const initializeContent = async () => {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/init-base-content`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Content initialized:', result);
        fetchWords(); // Refresh the list
      }
    } catch (error) {
      console.log('Error initializing content:', error);
    }
  };

  const fetchWords = async () => {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`);
      if (response.ok) {
        const data = await response.json();
        setWords(data);
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger les mots');
    }
  };

  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    
    if (status !== 'granted') {
      Alert.alert('Permission requise', 'Nous avons besoin d\'accéder à vos photos');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.8,
      base64: true,
    });

    if (!result.canceled && result.assets[0].base64) {
      setFormData(prev => ({
        ...prev,
        image_base64: `data:image/jpeg;base64,${result.assets[0].base64}`
      }));
    }
  };

  const openAddModal = () => {
    setEditingWord(null);
    setFormData({
      french: '',
      shimaore: '',
      kibouchi: '',
      category: 'famille',
      difficulty: 1,
      image_base64: '',
    });
    setModalVisible(true);
  };

  const openEditModal = (word: Word) => {
    setEditingWord(word);
    setFormData({
      french: word.french,
      shimaore: word.shimaore,
      kibouchi: word.kibouchi,
      category: word.category,
      difficulty: word.difficulty,
      image_base64: word.image_base64 || '',
    });
    setModalVisible(true);
  };

  const saveWord = async () => {
    if (!formData.french || !formData.shimaore || !formData.kibouchi) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs obligatoires');
      return;
    }

    try {
      const url = editingWord 
        ? `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words/${editingWord.id}`
        : `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words`;
      
      const method = editingWord ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        Alert.alert('Succès', `Mot ${editingWord ? 'modifié' : 'ajouté'} avec succès!`);
        setModalVisible(false);
        fetchWords();
      } else {
        Alert.alert('Erreur', 'Impossible de sauvegarder le mot');
      }
    } catch (error) {
      Alert.alert('Erreur', 'Problème de connexion');
    }
  };

  const deleteWord = async (wordId: string) => {
    Alert.alert(
      'Confirmer la suppression',
      'Êtes-vous sûr de vouloir supprimer ce mot?',
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: 'Supprimer',
          style: 'destructive',
          onPress: async () => {
            try {
              const response = await fetch(
                `${process.env.EXPO_PUBLIC_BACKEND_URL}/api/words/${wordId}`,
                { method: 'DELETE' }
              );
              
              if (response.ok) {
                Alert.alert('Succès', 'Mot supprimé!');
                fetchWords();
              } else {
                Alert.alert('Erreur', 'Impossible de supprimer le mot');
              }
            } catch (error) {
              Alert.alert('Erreur', 'Problème de connexion');
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
          <Text style={styles.title}>Administration 👨‍💼</Text>
          <TouchableOpacity onPress={openAddModal} style={styles.addButton}>
            <Ionicons name="add" size={24} color="#000" />
          </TouchableOpacity>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          <View style={styles.statsContainer}>
            <Text style={styles.statsText}>Total des mots: {words.length}</Text>
            <Text style={styles.statsText}>
              Catégories: {new Set(words.map(w => w.category)).size}
            </Text>
          </View>

          <Text style={styles.sectionTitle}>Gestion du contenu éducatif 📚</Text>

          {words.map((word) => (
            <View key={word.id} style={styles.wordCard}>
              <View style={styles.wordHeader}>
                <View style={styles.wordInfo}>
                  <Text style={styles.frenchText}>{word.french}</Text>
                  <Text style={styles.categoryText}>📁 {word.category}</Text>
                </View>
                <View style={styles.difficultyContainer}>
                  {[...Array(word.difficulty)].map((_, i) => (
                    <Ionicons key={i} name="star" size={16} color="#FFD700" />
                  ))}
                </View>
              </View>

              <View style={styles.translationsContainer}>
                <Text style={styles.translationText}>
                  🇰🇲 Shimaoré: <Text style={styles.bold}>{word.shimaore}</Text>
                </Text>
                <Text style={styles.translationText}>
                  🏝️ Kibouchi: <Text style={styles.bold}>{word.kibouchi}</Text>
                </Text>
              </View>

              {word.image_base64 && (
                <Image source={{ uri: word.image_base64 }} style={styles.wordImage} />
              )}

              <View style={styles.actionButtons}>
                <TouchableOpacity 
                  onPress={() => openEditModal(word)}
                  style={[styles.actionButton, styles.editButton]}
                >
                  <Ionicons name="pencil" size={16} color="#fff" />
                  <Text style={styles.actionButtonText}>Modifier</Text>
                </TouchableOpacity>

                <TouchableOpacity 
                  onPress={() => deleteWord(word.id)}
                  style={[styles.actionButton, styles.deleteButton]}
                >
                  <Ionicons name="trash" size={16} color="#fff" />
                  <Text style={styles.actionButtonText}>Supprimer</Text>
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </ScrollView>

        {/* Modal for Add/Edit */}
        <Modal
          animationType="slide"
          transparent={true}
          visible={modalVisible}
          onRequestClose={() => setModalVisible(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>
                  {editingWord ? 'Modifier le mot' : 'Ajouter un mot'}
                </Text>
                <TouchableOpacity 
                  onPress={() => setModalVisible(false)}
                  style={styles.closeButton}
                >
                  <Ionicons name="close" size={24} color="#333" />
                </TouchableOpacity>
              </View>

              <ScrollView style={styles.modalScroll}>
                <Text style={styles.inputLabel}>Français *</Text>
                <TextInput
                  style={styles.input}
                  value={formData.french}
                  onChangeText={(text) => setFormData(prev => ({ ...prev, french: text }))}
                  placeholder="Mot en français"
                />

                <Text style={styles.inputLabel}>Shimaoré *</Text>
                <TextInput
                  style={styles.input}
                  value={formData.shimaore}
                  onChangeText={(text) => setFormData(prev => ({ ...prev, shimaore: text }))}
                  placeholder="Traduction en Shimaoré"
                />

                <Text style={styles.inputLabel}>Kibouchi *</Text>
                <TextInput
                  style={styles.input}
                  value={formData.kibouchi}
                  onChangeText={(text) => setFormData(prev => ({ ...prev, kibouchi: text }))}
                  placeholder="Traduction en Kibouchi"
                />

                <Text style={styles.inputLabel}>Catégorie</Text>
                <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                  <View style={styles.categoryButtons}>
                    {CATEGORIES.map((category) => (
                      <TouchableOpacity
                        key={category}
                        style={[
                          styles.categoryButton,
                          formData.category === category && styles.selectedCategoryButton
                        ]}
                        onPress={() => setFormData(prev => ({ ...prev, category }))}
                      >
                        <Text style={[
                          styles.categoryButtonText,
                          formData.category === category && styles.selectedCategoryButtonText
                        ]}>
                          {category}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </ScrollView>

                <Text style={styles.inputLabel}>Difficulté</Text>
                <View style={styles.difficultyButtons}>
                  {[1, 2, 3].map((level) => (
                    <TouchableOpacity
                      key={level}
                      style={[
                        styles.difficultyButton,
                        formData.difficulty === level && styles.selectedDifficultyButton
                      ]}
                      onPress={() => setFormData(prev => ({ ...prev, difficulty: level }))}
                    >
                      <Text style={styles.difficultyButtonText}>{level} ⭐</Text>
                    </TouchableOpacity>
                  ))}
                </View>

                <Text style={styles.inputLabel}>Image (optionnel)</Text>
                <TouchableOpacity onPress={pickImage} style={styles.imageButton}>
                  <Ionicons name="image" size={24} color="#4ECDC4" />
                  <Text style={styles.imageButtonText}>Choisir une image</Text>
                </TouchableOpacity>

                {formData.image_base64 && (
                  <Image source={{ uri: formData.image_base64 }} style={styles.previewImage} />
                )}

                <TouchableOpacity onPress={saveWord} style={styles.saveButton}>
                  <LinearGradient colors={['#4ECDC4', '#45B7D1']} style={styles.saveButtonGradient}>
                    <Text style={styles.saveButtonText}>
                      {editingWord ? 'Modifier' : 'Ajouter'}
                    </Text>
                  </LinearGradient>
                </TouchableOpacity>
              </ScrollView>
            </View>
          </View>
        </Modal>
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
  addButton: {
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
  statsContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 15,
    padding: 15,
    marginBottom: 20,
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statsText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 15,
  },
  wordCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  wordHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 10,
  },
  wordInfo: {
    flex: 1,
  },
  frenchText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  categoryText: {
    fontSize: 14,
    color: '#666',
  },
  difficultyContainer: {
    flexDirection: 'row',
  },
  translationsContainer: {
    marginBottom: 15,
  },
  translationText: {
    fontSize: 16,
    color: '#333',
    marginBottom: 5,
  },
  bold: {
    fontWeight: 'bold',
  },
  wordImage: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    marginBottom: 15,
    resizeMode: 'cover',
  },
  actionButtons: {
    flexDirection: 'row',
    gap: 10,
  },
  actionButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    borderRadius: 8,
    gap: 5,
  },
  editButton: {
    backgroundColor: '#4ECDC4',
  },
  deleteButton: {
    backgroundColor: '#FF6B6B',
  },
  actionButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 20,
    width: '90%',
    maxHeight: '80%',
    overflow: 'hidden',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  closeButton: {
    padding: 5,
  },
  modalScroll: {
    padding: 20,
  },
  inputLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
    marginTop: 15,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  categoryButtons: {
    flexDirection: 'row',
    gap: 10,
  },
  categoryButton: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
  },
  selectedCategoryButton: {
    backgroundColor: '#4ECDC4',
  },
  categoryButtonText: {
    fontSize: 14,
    color: '#666',
  },
  selectedCategoryButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  difficultyButtons: {
    flexDirection: 'row',
    gap: 10,
  },
  difficultyButton: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: '#f0f0f0',
  },
  selectedDifficultyButton: {
    backgroundColor: '#FFD700',
  },
  difficultyButtonText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  imageButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 15,
    borderWidth: 2,
    borderColor: '#4ECDC4',
    borderStyle: 'dashed',
    borderRadius: 10,
    gap: 10,
  },
  imageButtonText: {
    fontSize: 16,
    color: '#4ECDC4',
    fontWeight: '600',
  },
  previewImage: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    marginTop: 15,
    resizeMode: 'cover',
  },
  saveButton: {
    marginTop: 25,
    borderRadius: 15,
    overflow: 'hidden',
  },
  saveButtonGradient: {
    paddingVertical: 15,
    alignItems: 'center',
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});