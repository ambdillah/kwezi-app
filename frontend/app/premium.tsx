import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  Linking,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { useUser } from '../contexts/UserContext';
import Constants from 'expo-constants';

export default function PremiumScreen() {
  const router = useRouter();
  const { user, isPremium, refreshUser } = useUser();
  const [isLoading, setIsLoading] = useState(false);

  const backendUrl = Constants.expoConfig?.extra?.backendUrl || process.env.EXPO_PUBLIC_BACKEND_URL || 'http://localhost:8001';

  const handleSubscribe = async () => {
    if (!user) {
      Alert.alert('Erreur', 'Utilisateur non identifié. Veuillez redémarrer l\'application.');
      return;
    }

    setIsLoading(true);

    try {
      // Créer une session de paiement Stripe
      const response = await fetch(`${backendUrl}/api/stripe/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.user_id,
          success_url: `${backendUrl}/api/payment/success?user_id=${user.user_id}`,
          cancel_url: `${backendUrl}/api/payment/cancel`,
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la création de la session de paiement');
      }

      const data = await response.json();

      // Ouvrir la page de paiement Stripe dans le navigateur
      const supported = await Linking.canOpenURL(data.url);

      if (supported) {
        await Linking.openURL(data.url);
        
        // Afficher un message pour guider l'utilisateur
        Alert.alert(
          'Paiement en cours',
          'Vous allez être redirigé vers la page de paiement sécurisée Stripe. Une fois le paiement effectué, revenez à l\'application et vos avantages Premium seront activés automatiquement.',
          [
            {
              text: 'J\'ai terminé le paiement',
              onPress: async () => {
                // Rafraîchir les données utilisateur
                await refreshUser();
                router.back();
              },
            },
            {
              text: 'Annuler',
              style: 'cancel',
            },
          ]
        );
      } else {
        Alert.alert('Erreur', 'Impossible d\'ouvrir le lien de paiement');
      }
    } catch (error) {
      console.error('Erreur souscription:', error);
      Alert.alert(
        'Erreur',
        'Une erreur est survenue lors de la création de la session de paiement. Veuillez réessayer.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleManageSubscription = async () => {
    if (!user) {
      Alert.alert('Erreur', 'Utilisateur non identifié');
      return;
    }

    setIsLoading(true);

    try {
      // Appeler l'API pour créer une session du portail client Stripe
      const response = await fetch(`${backendUrl}/api/stripe/create-portal-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          customer_id: user.stripe_customer_id, // Le customer_id Stripe de l'utilisateur
          return_url: `${backendUrl}/app`, // URL de retour après gestion
        }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la création de la session du portail client');
      }

      const data = await response.json();

      // Ouvrir le portail client Stripe dans le navigateur
      const supported = await Linking.canOpenURL(data.url);

      if (supported) {
        await Linking.openURL(data.url);
        
        Alert.alert(
          'Portail Client Stripe',
          'Vous allez être redirigé vers le portail de gestion de votre abonnement. Vous pourrez y annuler votre abonnement, mettre à jour votre carte ou voir votre historique de facturation.',
          [
            {
              text: 'OK',
              onPress: async () => {
                // Rafraîchir les données utilisateur au retour
                await refreshUser();
              },
            },
          ]
        );
      } else {
        Alert.alert('Erreur', 'Impossible d\'ouvrir le portail de gestion');
      }
    } catch (error) {
      console.error('Erreur gestion abonnement:', error);
      Alert.alert(
        'Erreur',
        'Une erreur est survenue. Si vous souhaitez annuler votre abonnement, contactez-nous à support@kwezi.com'
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Si l'utilisateur est déjà Premium
  if (isPremium) {
    return (
      <View style={styles.container}>
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {/* Header */}
          <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={24} color="#2C3E50" />
          </TouchableOpacity>

          {/* Badge Premium */}
          <LinearGradient
            colors={['#FFD700', '#FFA500']}
            style={styles.premiumBadge}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
          >
            <Ionicons name="star" size={60} color="#FFF" />
            <Text style={styles.premiumBadgeTitle}>Vous êtes Premium !</Text>
            <Text style={styles.premiumBadgeSubtitle}>
              Merci de votre soutien 🙏
            </Text>
          </LinearGradient>

          {/* Avantages actifs */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>✨ Vos avantages Premium actifs</Text>
            
            <View style={styles.benefitCard}>
              <Ionicons name="book" size={30} color="#4A90E2" />
              <View style={styles.benefitText}>
                <Text style={styles.benefitTitle}>Accès illimité</Text>
                <Text style={styles.benefitDescription}>
                  626 mots en Shimaoré et Kibouchi
                </Text>
              </View>
            </View>

            <View style={styles.benefitCard}>
              <Ionicons name="document-text" size={30} color="#4A90E2" />
              <View style={styles.benefitText}>
                <Text style={styles.benefitTitle}>Fiches d'exercices gratuites</Text>
                <Text style={styles.benefitDescription}>
                  Toutes les fiches PDF disponibles
                </Text>
              </View>
            </View>

            <View style={styles.benefitCard}>
              <Ionicons name="download" size={30} color="#4A90E2" />
              <View style={styles.benefitText}>
                <Text style={styles.benefitTitle}>Contenu hors ligne</Text>
                <Text style={styles.benefitDescription}>
                  Apprenez partout, même sans connexion
                </Text>
              </View>
            </View>

            <View style={styles.benefitCard}>
              <Ionicons name="flash" size={30} color="#4A90E2" />
              <View style={styles.benefitText}>
                <Text style={styles.benefitTitle}>Mises à jour prioritaires</Text>
                <Text style={styles.benefitDescription}>
                  Nouveau contenu en avant-première
                </Text>
              </View>
            </View>
          </View>

          {/* Bouton gérer l'abonnement */}
          <TouchableOpacity
            style={styles.manageButton}
            onPress={handleManageSubscription}
          >
            <Ionicons name="settings" size={20} color="#FFF" />
            <Text style={styles.manageButtonText}>Gérer mon abonnement</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>
    );
  }

  // Si l'utilisateur n'est PAS Premium
  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#2C3E50" />
        </TouchableOpacity>

        {/* Hero Section */}
        <LinearGradient
          colors={['#4A90E2', '#357ABD']}
          style={styles.heroSection}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <Ionicons name="star" size={60} color="#FFD700" />
          <Text style={styles.heroTitle}>Passez Premium</Text>
          <Text style={styles.heroSubtitle}>
            Débloquez tout le contenu et soutenez l'éducation en Shimaoré et Kibouchi
          </Text>
        </LinearGradient>

        {/* Prix */}
        <View style={styles.priceSection}>
          <Text style={styles.priceAmount}>2,90€</Text>
          <Text style={styles.pricePeriod}>/ mois</Text>
        </View>
        <Text style={styles.priceNote}>Résiliable à tout moment</Text>

        {/* Avantages */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>✨ Ce que vous obtenez</Text>
          
          <View style={styles.benefitCard}>
            <Ionicons name="lock-open" size={30} color="#4A90E2" />
            <View style={styles.benefitText}>
              <Text style={styles.benefitTitle}>Accès illimité</Text>
              <Text style={styles.benefitDescription}>
                Débloquez les 626 mots (vs 250 en version gratuite)
              </Text>
            </View>
            <Ionicons name="checkmark-circle" size={24} color="#27AE60" />
          </View>

          <View style={styles.benefitCard}>
            <Ionicons name="document-text" size={30} color="#4A90E2" />
            <View style={styles.benefitText}>
              <Text style={styles.benefitTitle}>Fiches d'exercices gratuites</Text>
              <Text style={styles.benefitDescription}>
                Toutes les fiches PDF sans frais supplémentaires
              </Text>
            </View>
            <Ionicons name="checkmark-circle" size={24} color="#27AE60" />
          </View>

          <View style={styles.benefitCard}>
            <Ionicons name="download" size={30} color="#4A90E2" />
            <View style={styles.benefitText}>
              <Text style={styles.benefitTitle}>Contenu hors ligne</Text>
              <Text style={styles.benefitDescription}>
                Téléchargez et apprenez sans connexion internet
              </Text>
            </View>
            <Ionicons name="checkmark-circle" size={24} color="#27AE60" />
          </View>

          <View style={styles.benefitCard}>
            <Ionicons name="flash" size={30} color="#4A90E2" />
            <View style={styles.benefitText}>
              <Text style={styles.benefitTitle}>Nouveau contenu en priorité</Text>
              <Text style={styles.benefitDescription}>
                Accédez aux nouvelles leçons en avant-première
              </Text>
            </View>
            <Ionicons name="checkmark-circle" size={24} color="#27AE60" />
          </View>

          <View style={styles.benefitCard}>
            <Ionicons name="heart" size={30} color="#E74C3C" />
            <View style={styles.benefitText}>
              <Text style={styles.benefitTitle}>Soutenez notre mission</Text>
              <Text style={styles.benefitDescription}>
                Aidez à préserver les langues de Mayotte
              </Text>
            </View>
            <Ionicons name="checkmark-circle" size={24} color="#27AE60" />
          </View>
        </View>

        {/* CTA Button */}
        <TouchableOpacity
          style={[styles.subscribeButton, isLoading && styles.subscribeButtonDisabled]}
          onPress={handleSubscribe}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator size="small" color="#FFF" />
          ) : (
            <>
              <Ionicons name="star" size={20} color="#FFF" />
              <Text style={styles.subscribeButtonText}>
                Devenir Premium - 2,90€/mois
              </Text>
            </>
          )}
        </TouchableOpacity>

        {/* Footer */}
        <Text style={styles.footerText}>
          Paiement sécurisé par Stripe 🔒{'\n'}
          Résiliez à tout moment depuis votre compte
        </Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  scrollContent: {
    padding: 20,
    paddingTop: 60,
  },
  backButton: {
    position: 'absolute',
    top: 20,
    left: 20,
    zIndex: 10,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#FFF',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  heroSection: {
    borderRadius: 20,
    padding: 40,
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFF',
    marginTop: 15,
    marginBottom: 10,
  },
  heroSubtitle: {
    fontSize: 16,
    color: '#FFF',
    textAlign: 'center',
    opacity: 0.95,
  },
  priceSection: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'baseline',
    marginBottom: 5,
  },
  priceAmount: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  pricePeriod: {
    fontSize: 20,
    color: '#7F8C8D',
    marginLeft: 5,
  },
  priceNote: {
    textAlign: 'center',
    color: '#7F8C8D',
    fontSize: 14,
    marginBottom: 30,
  },
  section: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 15,
  },
  benefitCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF',
    padding: 15,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  benefitText: {
    flex: 1,
    marginLeft: 15,
  },
  benefitTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2C3E50',
    marginBottom: 4,
  },
  benefitDescription: {
    fontSize: 14,
    color: '#7F8C8D',
  },
  subscribeButton: {
    backgroundColor: '#FFD700',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#FFD700',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  subscribeButtonDisabled: {
    opacity: 0.6,
  },
  subscribeButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginLeft: 10,
  },
  footerText: {
    textAlign: 'center',
    fontSize: 13,
    color: '#95A5A6',
    lineHeight: 20,
    marginBottom: 30,
  },
  premiumBadge: {
    borderRadius: 20,
    padding: 40,
    alignItems: 'center',
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  premiumBadgeTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFF',
    marginTop: 15,
  },
  premiumBadgeSubtitle: {
    fontSize: 16,
    color: '#FFF',
    marginTop: 5,
    opacity: 0.95,
  },
  manageButton: {
    backgroundColor: '#4A90E2',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    borderRadius: 12,
    marginTop: 10,
  },
  manageButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFF',
    marginLeft: 10,
  },
});
