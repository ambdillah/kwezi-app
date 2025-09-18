/**
 * COMPOSANT FLEUR D'YLANG-YLANG
 * =============================
 * Fleur emblématique de Mayotte - Composant réutilisable
 */

import React from 'react';
import { Image, StyleSheet, ViewStyle, ImageStyle } from 'react-native';

interface YlangYlangFlowerProps {
  size?: number;
  style?: ViewStyle | ImageStyle;
}

export const YlangYlangFlower: React.FC<YlangYlangFlowerProps> = ({ 
  size = 40, 
  style 
}) => {
  return (
    <Image
      source={require('../assets/ylang-ylang.png')}
      resizeMode="contain"
      style={[
        {
          width: size,
          height: size,
        },
        style
      ]}
    />
  );
};

export const styles = StyleSheet.create({
  small: {
    width: 20,
    height: 20,
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

export default YlangYlangFlower;