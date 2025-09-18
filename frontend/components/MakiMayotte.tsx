/**
 * COMPOSANT MAKI DE MAYOTTE
 * =========================
 * Animal emblématique de Mayotte - Composant réutilisable
 */

import React from 'react';
import { Image, StyleSheet, ViewStyle, ImageStyle } from 'react-native';

interface MakiMayotteProps {
  size?: number;
  style?: ViewStyle | ImageStyle;
}

export const MakiMayotte: React.FC<MakiMayotteProps> = ({ 
  size = 40, 
  style 
}) => {
  return (
    <Image
      source={require('../assets/maki-mayotte.png')}
      style={[
        {
          width: size,
          height: size,
          resizeMode: 'contain'
        },
        style
      ]}
    />
  );
};

export const styles = StyleSheet.create({
  tiny: {
    width: 16,
    height: 16,
  },
  small: {
    width: 24,
    height: 24,
  },
  medium: {
    width: 40,
    height: 40,
  },
  large: {
    width: 60,
    height: 60,
  },
  xlarge: {
    width: 80,
    height: 80,
  },
  xxlarge: {
    width: 120,
    height: 120,
  }
});

export default MakiMayotte;