import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function PaymentCancelScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      {/* Icône */}
      <View style={styles.iconContainer}>
        <Ionicons name="close-circle-outline" size={100} color="#E74C3C" />
      </View>

      {/* Message */}
      <Text style={styles.title}>Paiement Annulé</Text>
      <Text style={styles.message}>
        Votre paiement a été annulé. Aucun montant n'a été débité.
      </Text>

      {/* Informations */}
      <View style={styles.infoBox}>
        <Ionicons name="information-circle-outline" size={20} color="#4A90E2" />
        <Text style={styles.infoText}>
          Vous pouvez continuer à utiliser l'application avec l'accès gratuit (250 mots).
        </Text>
      </View>

      {/* Boutons */}
      <TouchableOpacity
        style={styles.primaryButton}
        onPress={() => router.push('/premium')}
      >
        <Text style={styles.primaryButtonText}>Réessayer</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.secondaryButton}
        onPress={() => router.replace('/')}
      >
        <Text style={styles.secondaryButtonText}>Retour à l'accueil</Text>
      </TouchableOpacity>
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
  iconContainer: {
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#E74C3C',
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
  infoBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E3F2FD',
    padding: 15,
    borderRadius: 12,
    width: '100%',
    marginBottom: 30,
  },
  infoText: {
    fontSize: 14,
    color: '#1976D2',
    marginLeft: 10,
    flex: 1,
    lineHeight: 20,
  },
  primaryButton: {
    width: '100%',
    backgroundColor: '#4A90E2',
    paddingVertical: 16,
    borderRadius: 12,
    marginBottom: 12,
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
    borderColor: '#7F8C8D',
  },
  secondaryButtonText: {
    color: '#7F8C8D',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
});
