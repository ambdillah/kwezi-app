import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSequence,
  withRepeat,
  interpolate,
  Easing,
} from 'react-native-reanimated';
import Svg, { Path, Circle, Ellipse, G } from 'react-native-svg';

interface AnimatedMakiProps {
  position: { x: number; y: number };
  isMoving: boolean;
  direction?: 'left' | 'right' | 'up' | 'down';
  size?: number;
}

const AnimatedMaki: React.FC<AnimatedMakiProps> = ({
  position,
  isMoving,
  direction = 'right',
  size = 40,
}) => {
  // Valeurs animées
  const walkCycle = useSharedValue(0);
  const bobOffset = useSharedValue(0);
  const eyeBlink = useSharedValue(0);
  const tailWag = useSharedValue(0);

  useEffect(() => {
    if (isMoving) {
      // Animation de marche
      walkCycle.value = withRepeat(
        withTiming(1, { duration: 600, easing: Easing.linear }),
        -1,
        false
      );
      
      // Animation de balancement
      bobOffset.value = withRepeat(
        withSequence(
          withTiming(-2, { duration: 300 }),
          withTiming(2, { duration: 300 })
        ),
        -1,
        true
      );
      
      // Mouvement de la queue
      tailWag.value = withRepeat(
        withSequence(
          withTiming(20, { duration: 400 }),
          withTiming(-20, { duration: 400 })
        ),
        -1,
        true
      );
    } else {
      // Arrêter les animations de mouvement
      walkCycle.value = withTiming(0, { duration: 200 });
      bobOffset.value = withTiming(0, { duration: 300 });
      
      // Animation de queue au repos
      tailWag.value = withRepeat(
        withSequence(
          withTiming(10, { duration: 800 }),
          withTiming(-5, { duration: 800 })
        ),
        -1,
        true
      );
    }

    // Animation de clignement des yeux (indépendante)
    const blinkAnimation = () => {
      eyeBlink.value = withSequence(
        withTiming(1, { duration: 100 }),
        withTiming(0, { duration: 100 })
      );
    };

    const blinkInterval = setInterval(blinkAnimation, 3000 + Math.random() * 2000);
    
    return () => clearInterval(blinkInterval);
  }, [isMoving]);

  // Style animé pour la position
  const makiStyle = useAnimatedStyle(() => {
    return {
      transform: [
        { translateX: position.x - size / 2 },
        { translateY: position.y - size / 2 + bobOffset.value },
        { scaleX: direction === 'left' ? -1 : 1 },
      ],
    };
  });

  // Style animé pour les pattes
  const frontPawStyle = useAnimatedStyle(() => {
    const rotation = interpolate(walkCycle.value, [0, 0.5, 1], [0, 20, 0]);
    return {
      transform: [{ rotate: `${rotation}deg` }],
    };
  });

  const backPawStyle = useAnimatedStyle(() => {
    const rotation = interpolate(walkCycle.value, [0, 0.5, 1], [0, -20, 0]);
    return {
      transform: [{ rotate: `${rotation}deg` }],
    };
  });

  // Style animé pour la queue
  const tailStyle = useAnimatedStyle(() => {
    return {
      transform: [{ rotate: `${tailWag.value}deg` }],
    };
  });

  // Style animé pour les yeux
  const eyeStyle = useAnimatedStyle(() => {
    const scaleY = interpolate(eyeBlink.value, [0, 1], [1, 0.1]);
    return {
      transform: [{ scaleY }],
    };
  });

  return (
    <Animated.View style={[styles.makiContainer, makiStyle]}>
      <Svg width={size} height={size} viewBox="0 0 100 100">
        {/* Ombre */}
        <Ellipse
          cx="50"
          cy="95"
          rx="20"
          ry="5"
          fill="rgba(0,0,0,0.2)"
        />
        
        {/* Queue (derrière) */}
        <G transform="translate(15, 40)">
          <Animated.View style={tailStyle}>
            <Path
              d="M 0,0 Q -15,-10 -25,-5 Q -30,0 -25,10 Q -15,15 -5,10"
              fill="#8D6E63"
              stroke="#5D4037"
              strokeWidth="1"
            />
          </Animated.View>
        </G>

        {/* Corps principal */}
        <Ellipse
          cx="50"
          cy="60"
          rx="18"
          ry="25"
          fill="#A1887F"
          stroke="#5D4037"
          strokeWidth="1"
        />

        {/* Tête */}
        <Circle
          cx="50"
          cy="35"
          r="20"
          fill="#BCAAA4"
          stroke="#5D4037"
          strokeWidth="1"
        />

        {/* Oreilles */}
        <Ellipse cx="38" cy="22" rx="6" ry="10" fill="#8D6E63" />
        <Ellipse cx="62" cy="22" rx="6" ry="10" fill="#8D6E63" />
        
        {/* Intérieur des oreilles */}
        <Ellipse cx="38" cy="22" rx="3" ry="6" fill="#D7CCC8" />
        <Ellipse cx="62" cy="22" rx="3" ry="6" fill="#D7CCC8" />

        {/* Yeux */}
        <Animated.View style={eyeStyle}>
          <Circle cx="43" cy="32" r="4" fill="#2E7D32" />
          <Circle cx="57" cy="32" r="4" fill="#2E7D32" />
          
          {/* Reflets des yeux */}
          <Circle cx="44" cy="31" r="1.5" fill="#FFFFFF" />
          <Circle cx="58" cy="31" r="1.5" fill="#FFFFFF" />
        </Animated.View>

        {/* Museau */}
        <Ellipse
          cx="50"
          cy="42"
          rx="8"
          ry="6"
          fill="#D7CCC8"
          stroke="#5D4037"
          strokeWidth="0.5"
        />

        {/* Nez */}
        <Ellipse cx="50" cy="39" rx="2" ry="1.5" fill="#5D4037" />

        {/* Bouche */}
        <Path
          d="M 50,41 Q 48,43 46,42 M 50,41 Q 52,43 54,42"
          stroke="#5D4037"
          strokeWidth="1"
          fill="none"
        />

        {/* Pattes avant */}
        <G transform="translate(35, 75)">
          <Animated.View style={frontPawStyle}>
            <Ellipse rx="4" ry="12" fill="#8D6E63" stroke="#5D4037" strokeWidth="0.5" />
          </Animated.View>
        </G>
        <G transform="translate(50, 75)">
          <Animated.View style={frontPawStyle}>
            <Ellipse rx="4" ry="12" fill="#8D6E63" stroke="#5D4037" strokeWidth="0.5" />
          </Animated.View>
        </G>

        {/* Pattes arrière */}
        <G transform="translate(40, 80)">
          <Animated.View style={backPawStyle}>
            <Ellipse rx="4" ry="10" fill="#8D6E63" stroke="#5D4037" strokeWidth="0.5" />
          </Animated.View>
        </G>
        <G transform="translate(55, 80)">
          <Animated.View style={backPawStyle}>
            <Ellipse rx="4" ry="10" fill="#8D6E63" stroke="#5D4037" strokeWidth="0.5" />
          </Animated.View>
        </G>

        {/* Ventre */}
        <Ellipse
          cx="50"
          cy="65"
          rx="12"
          ry="18"
          fill="#EFEBE9"
        />

        {/* Expression de contentement si pas en mouvement */}
        {!isMoving && (
          <G>
            {/* Joues roses */}
            <Circle cx="35" cy="38" r="3" fill="#FFCDD2" opacity="0.6" />
            <Circle cx="65" cy="38" r="3" fill="#FFCDD2" opacity="0.6" />
          </G>
        )}
      </Svg>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  makiContainer: {
    position: 'absolute',
    zIndex: 10,
  },
});

export default AnimatedMaki;