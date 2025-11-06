import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useUser } from '../contexts/UserContext';

export default function PaymentSuccessScreen() {
  const router = useRouter();
  const { refreshUser } = useUser();
  const [isLoading, setIsLoading] = useState(true);
  const params = useLocalSearchParams();

  useEffect(() => {
    // Rafraîchir le statut utilisateur pour obtenir le premium
    const refreshStatus = async () => {
      try {
        await refreshUser();
        // Attendre 2 secondes pour laisser le temps au webhook de traiter
        setTimeout(() => {
          setIsLoading(false);
        }, 2000);
      } catch (error) {
        console.error('Erreur rafraîchissement:', error);
        setIsLoading(false);
      }
    };

    refreshStatus();
  }, []);

  if (isLoading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#27AE60" />
        <Text style={styles.loadingText}>Activation de votre abonnement Premium...</Text>
        <Text style={styles.subText}>Veuillez patienter quelques instants</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Icône de succès */}
      <View style={styles.iconContainer}>
        <Ionicons name="checkmark-circle" size={100} color="#27AE60" />
      </View>

      {/* Message de succès */}
      <Text style={styles.title}>Paiement Réussi ! 🎉</Text>
      <Text style={styles.message}>
        Votre abonnement Premium a été activé avec succès.
      </Text>

      {/* Bénéfices */}
      <View style={styles.benefitsContainer}>
        <View style={styles.benefitItem}>
          <Ionicons name="checkmark" size={24} color="#27AE60" />
          <Text style={styles.benefitText}>Accès à tous les 636 mots</Text>
        </View>
        <View style={styles.benefitItem}>
          <Ionicons name="checkmark" size={24} color="#27AE60" />
          <Text style={styles.benefitText}>Fiches d'exercices gratuites</Text>
        </View>
        <View style={styles.benefitItem}>
          <Ionicons name="checkmark" size={24} color="#27AE60" />
          <Text style={styles.benefitText}>Tous les jeux débloqués</Text>
        </View>
      </View>

      {/* Boutons d'action */}
      <TouchableOpacity
        style={styles.primaryButton}
        onPress={() => router.replace('/')}
      >
        <Text style={styles.primaryButtonText}>Commencer à apprendre</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.secondaryButton}
        onPress={() => router.push('/premium')}
      >
        <Text style={styles.secondaryButtonText}>Gérer mon abonnement</Text>
      </TouchableOpacity>

      {/* Informations */}
      <View style={styles.infoBox}>
        <Ionicons name="information-circle-outline" size={20} color="#4A90E2" />
        <Text style={styles.infoText}>
          Vous recevrez un email de confirmation de Stripe.
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2C3E50',
    marginTop: 20,
    textAlign: 'center',
  },
  subText: {
    fontSize: 14,
    color: '#7F8C8D',
    marginTop: 10,
    textAlign: 'center',
  },
  iconContainer: {
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#27AE60',
    marginBottom: 15,
    textAlign: 'center',
  },
  message: {
    fontSize: 16,
    color: '#2C3E50',
    textAlign: 'center',
    marginBottom: 30,
    lineHeight: 24,
  },
  benefitsContainer: {
    width: '100%',
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 20,
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  benefitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  benefitText: {
    fontSize: 15,
    color: '#2C3E50',
    marginLeft: 12,
    fontWeight: '500',
  },
  primaryButton: {
    width: '100%',
    backgroundColor: '#27AE60',
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#27AE60',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  primaryButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  secondaryButton: {
    width: '100%',
    backgroundColor: '#FFF',
    paddingVertical: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#4A90E2',
    marginBottom: 20,
  },
  secondaryButtonText: {
    color: '#4A90E2',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  infoBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E3F2FD',
    padding: 12,
    borderRadius: 8,
    width: '100%',
  },
  infoText: {
    fontSize: 13,
    color: '#1976D2',
    marginLeft: 8,
    flex: 1,
  },
});
