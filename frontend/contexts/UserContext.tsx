import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

interface User {
  id: string;
  user_id: string;
  email?: string;
  is_premium: boolean;
  premium_expires_at?: string;
  subscription_type?: string;
  stripe_customer_id?: string;      // ID client Stripe
  stripe_subscription_id?: string;  // ID abonnement Stripe
  words_learned: number;
  total_score: number;
  streak_days: number;
  created_at: string;
  last_login?: string;
}

interface UserContextType {
  user: User | null;
  isLoading: boolean;
  isPremium: boolean;
  initializeUser: () => Promise<void>;
  upgradeToPremium: (subscriptionType: string) => Promise<boolean>;
  updateUserActivity: (wordsLearned: number, score: number) => Promise<void>;
  refreshUser: () => Promise<void>;
  logout: () => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

 const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL || 'https://kwezi-backend.onrender.com';

  // Générer un ID utilisateur unique
  const generateUserId = () => {
    return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  // Initialiser l'utilisateur au démarrage
  const initializeUser = async () => {
    try {
      setIsLoading(true);
      
      // Vérifier si un user_id existe dans AsyncStorage
      let userId = await AsyncStorage.getItem('user_id');
      
      if (!userId) {
        // Créer un nouvel utilisateur
        userId = generateUserId();
        await AsyncStorage.setItem('user_id', userId);
        
        // Enregistrer l'utilisateur sur le backend
        const response = await fetch(`${backendUrl}/api/users/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId }),
        });
        
        if (response.ok) {
          const data = await response.json();
          setUser(data.user);
        }
      } else {
        // Récupérer les infos utilisateur existant
        const response = await fetch(`${backendUrl}/api/users/${userId}`);
        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        }
      }
    } catch (error) {
      console.error('Erreur initialisation utilisateur:', error);
      // Créer un utilisateur local en cas d'erreur
      const localUserId = generateUserId();
      await AsyncStorage.setItem('user_id', localUserId);
      setUser({
        id: localUserId,
        user_id: localUserId,
        is_premium: false,
        words_learned: 0,
        total_score: 0,
        streak_days: 0,
        created_at: new Date().toISOString(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Rafraîchir les données utilisateur
  const refreshUser = async () => {
    try {
      const userId = await AsyncStorage.getItem('user_id');
      if (!userId) return;

      const response = await fetch(`${backendUrl}/api/users/${userId}`);
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (error) {
      console.error('Erreur refresh utilisateur:', error);
    }
  };

  // Passer à Premium
  const upgradeToPremium = async (subscriptionType: string = 'monthly'): Promise<boolean> => {
    try {
      const userId = await AsyncStorage.getItem('user_id');
      if (!userId) return false;

      const response = await fetch(`${backendUrl}/api/users/${userId}/upgrade`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, subscription_type: subscriptionType }),
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Erreur upgrade premium:', error);
      return false;
    }
  };

  // Mettre à jour l'activité utilisateur
  const updateUserActivity = async (wordsLearned: number, score: number) => {
    try {
      const userId = await AsyncStorage.getItem('user_id');
      if (!userId) return;

      const response = await fetch(`${backendUrl}/api/users/${userId}/activity`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ words_learned: wordsLearned, score }),
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (error) {
      console.error('Erreur mise à jour activité:', error);
    }
  };

  // Déconnexion (pour debug/test)
  const logout = async () => {
    try {
      await AsyncStorage.removeItem('user_id');
      setUser(null);
      await initializeUser();
    } catch (error) {
      console.error('Erreur logout:', error);
    }
  };

  // Initialiser au montage du composant
  useEffect(() => {
    initializeUser();
  }, []);

  const value: UserContextType = {
    user,
    isLoading,
    isPremium: user?.is_premium || false,
    initializeUser,
    upgradeToPremium,
    updateUserActivity,
    refreshUser,
    logout,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

// Hook personnalisé pour utiliser le contexte
export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser doit être utilisé dans un UserProvider');
  }
  return context;
};
