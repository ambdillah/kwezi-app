import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Dimensions } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import * as Speech from '../utils/safeSpeech';
import { speakEducationalContent } from '../utils/feminineSpeechUtils';
import YlangYlangFlower from '../components/YlangYlangFlower';
import MakiMayotte from '../components/MakiMayotte';

const { width, height } = Dimensions.get('window');

export default function WelcomeScreen() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simuler un chargement initial
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const playWelcomeSound = () => {
    // Utiliser la voix féminine pour le message de bienvenue
    speakEducationalContent("Kwezi! Bienvenue dans votre application pour apprendre le Shimaoré et le Kibouchi!", 'fr');
  };

  if (isLoading) {
    return (
      <LinearGradient
        colors={['#FFD700', '#FFA500', '#000000']}
        style={styles.container}
      >
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.loadingContainer}>
            <Text style={styles.loadingText}>Kwezi... 🌺</Text>
            <Text style={styles.subtitleText}>Chargement de votre app Mayotte</Text>
          </View>
        </SafeAreaView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient
      colors={['#FFD700', '#FFA500', '#000000']}
      style={styles.container}
    >
      <StatusBar barStyle="dark-content" />
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.content}>
          {/* Header avec motif ylang-ylang stylisé */}
          <View style={styles.header}>
            <Text style={styles.welcomeText}>Kwezi! 🌺</Text>
            <Text style={styles.appTitle}>Apprendre le Shimaoré & Kibouchi</Text>
            <TouchableOpacity onPress={playWelcomeSound} style={styles.soundButton}>
              <Ionicons name="volume-high" size={24} color="#000" />
            </TouchableOpacity>
          </View>

          {/* Section makis stylisés */}
          <View style={styles.makiSection}>
            <MakiMayotte size={60} />
            <Text style={styles.makiText}>Avec les makis de Mayotte</Text>
          </View>

          {/* Boutons principaux */}
          <View style={styles.buttonContainer}>
            <TouchableOpacity style={styles.mainButton} onPress={() => router.push('/learn')}>
              <LinearGradient
                colors={['#FFD700', '#FFA500']}
                style={styles.buttonGradient}
              >
                <Ionicons name="school" size={24} color="#000" />
                <Text style={styles.buttonText}>Commencer à apprendre</Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity style={styles.mainButton} onPress={() => router.push('/games')}>
              <LinearGradient
                colors={['#32CD32', '#228B22']}
                style={styles.buttonGradient}
              >
                <Ionicons name="game-controller" size={24} color="#fff" />
                <Text style={[styles.buttonText, styles.whiteText]}>Jouer et s'amuser</Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity style={styles.mainButton} onPress={() => router.push('/progress')}>
              <LinearGradient
                colors={['#FF6B6B', '#FF4757']}
                style={styles.buttonGradient}
              >
                <Ionicons name="bar-chart" size={24} color="#fff" />
                <Text style={[styles.buttonText, styles.whiteText]}>Mes progrès</Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity style={styles.mainButton} onPress={() => router.push('/badges')}>
              <LinearGradient
                colors={['#9B59B6', '#8E44AD']}
                style={styles.buttonGradient}
              >
                <Ionicons name="trophy" size={24} color="#fff" />
                <Text style={[styles.buttonText, styles.whiteText]}>Mes badges</Text>
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity style={styles.mainButton} onPress={() => router.push('/shop')}>
              <LinearGradient
                colors={['#4ECDC4', '#44A08D']}
                style={styles.buttonGradient}
              >
                <Ionicons name="cart" size={24} color="#fff" />
                <Text style={[styles.buttonText, styles.whiteText]}>Boutique</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>

          {/* Footer avec éléments culturels */}
          <View style={styles.footer}>
            <View style={styles.cultureRow}>
              <YlangYlangFlower size={24} />
              <Text style={styles.cultureText}> Ylang-ylang • </Text>
              <MakiMayotte size={24} />
              <Text style={styles.cultureText}> Maki • 🏝️ Mayotte</Text>
            </View>
            <Text style={styles.languageText}>Français • Shimaoré • Kibouchi</Text>
          </View>
        </View>
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
  loadingContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitleText: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  header: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 15,
  },
  welcomeText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 8,
  },
  appTitle: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
    marginBottom: 10,
    fontWeight: '600',
  },
  soundButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 20,
    padding: 8,
    marginTop: 5,
  },
  makiSection: {
    alignItems: 'center',
    marginBottom: 20,
  },
  makiEmoji: {
    fontSize: 64,
    marginBottom: 10,
  },
  makiText: {
    fontSize: 14,
    color: '#333',
    fontStyle: 'italic',
  },
  buttonContainer: {
    gap: 12,
  },
  mainButton: {
    height: 60,
    borderRadius: 15,
    overflow: 'hidden',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.2,
    shadowRadius: 2.5,
  },
  buttonGradient: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 16,
    gap: 12,
  },
  buttonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#000',
  },
  whiteText: {
    color: '#fff',
  },
  footer: {
    alignItems: 'center',
    marginTop: 30,
    paddingBottom: 20,
  },
  cultureRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  cultureText: {
    fontSize: 16,
    color: '#333',
    textAlign: 'center',
  },
  languageText: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
    textAlign: 'center',
  },
});