import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
  Linking,
  SafeAreaView,
  StatusBar,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { EXERCISE_SHEETS, ExerciseSheet } from '../data/exerciseSheets';
import { useUser } from '../contexts/UserContext';

const ShopScreen = () => {
  const { user } = useUser();
  const [purchasedSheets, setPurchasedSheets] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('tous');

  useEffect(() => {
    loadPurchasedSheets();
  }, []);

  const loadPurchasedSheets = async () => {
    try {
      const saved = await AsyncStorage.getItem('purchased_sheets');
      if (saved) {
        setPurchasedSheets(JSON.parse(saved));
      }
    } catch (error) {
      console.error('Erreur chargement achats:', error);
    }
  };

  const savePurchase = async (sheetId: string) => {
    try {
      const updated = [...purchasedSheets, sheetId];
      await AsyncStorage.setItem('purchased_sheets', JSON.stringify(updated));
      setPurchasedSheets(updated);
    } catch (error) {
      console.error('Erreur sauvegarde achat:', error);
    }
  };

  const handleDownload = async (sheet: ExerciseSheet) => {
    const isPremium = user?.is_premium || false;
    const isAlreadyPurchased = purchasedSheets.includes(sheet.id);

    if (isPremium || isAlreadyPurchased) {
      // Téléchargement direct
      try {
        await Linking.openURL(sheet.pdfUrl);
        Alert.alert(
          '✅ Téléchargement',
          'La fiche d\'exercice est en cours de téléchargement !',
          [{ text: 'OK' }]
        );
      } catch (error) {
        Alert.alert('Erreur', 'Impossible d\'ouvrir le fichier');
      }
    } else {
      // Afficher la modal de paiement
      showPurchaseModal(sheet);
    }
  };

  const showPurchaseModal = (sheet: ExerciseSheet) => {
    Alert.alert(
      '🛒 Achat de fiche',
      `Voulez-vous acheter "${sheet.title}" pour ${sheet.price.toFixed(2)}€ ?\n\n💡 Astuce : Avec l'abonnement Premium, toutes les fiches sont gratuites !`,
      [
        { text: 'Annuler', style: 'cancel' },
        {
          text: `Acheter ${sheet.price.toFixed(2)}€`,
          onPress: () => processPurchase(sheet),
        },
        {
          text: '⭐ Devenir Premium',
          onPress: () => router.push('/premium'),
        },
      ]
    );
  };

  const processPurchase = async (sheet: ExerciseSheet) => {
    // Simulation de paiement (à remplacer par Stripe)
    Alert.alert(
      '💳 Paiement simulé',
      'Dans la version finale, le paiement sera traité par Stripe.\n\nPour cette démo, l\'achat est validé automatiquement.',
      [
        {
          text: 'OK',
          onPress: async () => {
            await savePurchase(sheet.id);
            Alert.alert(
              '✅ Achat réussi !',
              `Vous pouvez maintenant télécharger "${sheet.title}"`,
              [
                {
                  text: 'Télécharger',
                  onPress: () => handleDownload(sheet),
                },
                { text: 'Plus tard' },
              ]
            );
          },
        },
      ]
    );
  };

  const categories = [
    { id: 'tous', label: 'Tous', icon: 'apps-outline' },
    { id: 'vocabulaire', label: 'Vocabulaire', icon: 'book-outline' },
    { id: 'nombres', label: 'Nombres', icon: 'calculator-outline' },
    { id: 'animaux', label: 'Animaux', icon: 'paw-outline' },
  ];

  const filteredSheets = selectedCategory === 'tous'
    ? EXERCISE_SHEETS
    : EXERCISE_SHEETS.filter(sheet => sheet.category === selectedCategory);

  const canDownload = (sheetId: string) => {
    return user?.is_premium || purchasedSheets.includes(sheetId);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      <LinearGradient colors={['#4ECDC4', '#44A08D']} style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="white" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>🛒 Boutique</Text>
        <View style={styles.headerRight}>
          {user?.is_premium && (
            <View style={styles.premiumBadge}>
              <Ionicons name="star" size={16} color="#FFD700" />
              <Text style={styles.premiumText}>Premium</Text>
            </View>
          )}
        </View>
      </LinearGradient>

      {/* Catégories */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.categoriesContainer}
        contentContainerStyle={styles.categoriesContent}
      >
        {categories.map(cat => (
          <TouchableOpacity
            key={cat.id}
            style={[
              styles.categoryButton,
              selectedCategory === cat.id && styles.categoryButtonActive,
            ]}
            onPress={() => setSelectedCategory(cat.id)}
          >
            <Ionicons
              name={cat.icon as any}
              size={16}
              color={selectedCategory === cat.id ? 'white' : '#4ECDC4'}
            />
            <Text
              style={[
                styles.categoryText,
                selectedCategory === cat.id && styles.categoryTextActive,
              ]}
            >
              {cat.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Liste des fiches */}
      <ScrollView style={styles.sheetsList} contentContainerStyle={styles.sheetsContent}>
        {filteredSheets.map(sheet => {
          const downloadable = canDownload(sheet.id);
          const isPurchased = purchasedSheets.includes(sheet.id);

          return (
            <View key={sheet.id} style={styles.sheetCard}>
              <Image source={{ uri: sheet.imageUrl }} style={styles.sheetImage} />
              
              <View style={styles.sheetInfo}>
                <View style={styles.sheetHeader}>
                  <Text style={styles.sheetTitle}>{sheet.title}</Text>
                  {user?.is_premium && (
                    <View style={styles.freeBadge}>
                      <Text style={styles.freeBadgeText}>GRATUIT</Text>
                    </View>
                  )}
                  {!user?.is_premium && isPurchased && (
                    <View style={styles.purchasedBadge}>
                      <Ionicons name="checkmark-circle" size={16} color="#4CAF50" />
                    </View>
                  )}
                </View>

                <Text style={styles.sheetDescription}>{sheet.description}</Text>

                <View style={styles.sheetMeta}>
                  <View style={styles.metaItem}>
                    <Ionicons name="language-outline" size={16} color="#666" />
                    <Text style={styles.metaText}>{sheet.language}</Text>
                  </View>
                  <View style={styles.metaItem}>
                    <Ionicons name="people-outline" size={16} color="#666" />
                    <Text style={styles.metaText}>{sheet.ageRange}</Text>
                  </View>
                  <View style={styles.metaItem}>
                    <Ionicons
                      name={
                        sheet.difficulty === 'facile'
                          ? 'star'
                          : sheet.difficulty === 'moyen'
                          ? 'star-half'
                          : 'star-outline'
                      }
                      size={16}
                      color="#FFB700"
                    />
                    <Text style={styles.metaText}>{sheet.difficulty}</Text>
                  </View>
                </View>

                <View style={styles.sheetFooter}>
                  {!user?.is_premium && !isPurchased && (
                    <Text style={styles.price}>{sheet.price.toFixed(2)}€</Text>
                  )}
                  {downloadable && (
                    <Text style={styles.ownedText}>✓ Téléchargeable</Text>
                  )}
                  <TouchableOpacity
                    style={[
                      styles.downloadButton,
                      downloadable && styles.downloadButtonReady,
                    ]}
                    onPress={() => handleDownload(sheet)}
                  >
                    <Ionicons
                      name={downloadable ? 'download-outline' : 'cart-outline'}
                      size={20}
                      color="white"
                    />
                    <Text style={styles.downloadButtonText}>
                      {downloadable ? 'Télécharger' : 'Acheter'}
                    </Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>
          );
        })}
      </ScrollView>

      {/* Info Premium */}
      {!user?.is_premium && (
        <View style={styles.premiumBanner}>
          <LinearGradient
            colors={['#FFD700', '#FFA500']}
            style={styles.premiumGradient}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
          >
            <Ionicons name="star" size={24} color="white" />
            <View style={styles.premiumBannerText}>
              <Text style={styles.premiumBannerTitle}>Passez Premium !</Text>
              <Text style={styles.premiumBannerSubtitle}>
                Toutes les fiches gratuites
              </Text>
            </View>
            <TouchableOpacity
              style={styles.premiumButton}
              onPress={() => router.push('/premium')}
            >
              <Text style={styles.premiumButtonText}>2,90€/mois</Text>
            </TouchableOpacity>
          </LinearGradient>
        </View>
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    paddingTop: 20,
    paddingBottom: 16,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: 'white',
    flex: 1,
    textAlign: 'center',
  },
  headerRight: {
    width: 40,
  },
  premiumBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  premiumText: {
    color: 'white',
    fontSize: 10,
    fontWeight: '600',
    marginLeft: 4,
  },
  categoriesContainer: {
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#E9ECEF',
    maxHeight: 50,
  },
  categoriesContent: {
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  categoryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#F8F9FA',
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#E9ECEF',
  },
  categoryButtonActive: {
    backgroundColor: '#4ECDC4',
    borderColor: '#4ECDC4',
  },
  categoryText: {
    marginLeft: 4,
    fontSize: 12,
    fontWeight: '600',
    color: '#666',
  },
  categoryTextActive: {
    color: 'white',
  },
  sheetsList: {
    flex: 1,
  },
  sheetsContent: {
    padding: 16,
  },
  sheetCard: {
    backgroundColor: 'white',
    borderRadius: 16,
    marginBottom: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  sheetImage: {
    width: '100%',
    height: 250,
    resizeMode: 'contain',
    backgroundColor: '#F8F9FA',
  },
  sheetInfo: {
    padding: 16,
  },
  sheetHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  sheetTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#2C3E50',
    flex: 1,
  },
  freeBadge: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  freeBadgeText: {
    color: 'white',
    fontSize: 10,
    fontWeight: '700',
  },
  purchasedBadge: {
    marginLeft: 8,
  },
  sheetDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  sheetMeta: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
  },
  metaText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  sheetFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  price: {
    fontSize: 24,
    fontWeight: '700',
    color: '#4ECDC4',
  },
  ownedText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#4CAF50',
  },
  downloadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF6B6B',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 12,
  },
  downloadButtonReady: {
    backgroundColor: '#4ECDC4',
  },
  downloadButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 6,
  },
  premiumBanner: {
    margin: 16,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  premiumGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  premiumBannerText: {
    flex: 1,
    marginLeft: 12,
  },
  premiumBannerTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
  },
  premiumBannerSubtitle: {
    fontSize: 12,
    color: 'rgba(255, 255, 255, 0.9)',
  },
  premiumButton: {
    backgroundColor: 'white',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  premiumButtonText: {
    color: '#FFA500',
    fontSize: 14,
    fontWeight: '700',
  },
});

export default ShopScreen;
