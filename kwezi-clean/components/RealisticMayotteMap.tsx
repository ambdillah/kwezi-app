import React, { useState, useRef } from 'react';
import {
  View,
  StyleSheet,
  Dimensions,
  PanResponder,
  Animated,
} from 'react-native';
import Svg, {
  Path,
  Circle,
  Text as SvgText,
  G,
  Defs,
  LinearGradient,
  Stop,
  ClipPath,
  Rect,
} from 'react-native-svg';
import { Ionicons } from '@expo/vector-icons';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

interface Village {
  id: string;
  name: string;
  pos: { x: number; y: number };
  type: string;
  unlocked: boolean;
  meta: {
    specialite: string;
    description: string;
  };
}

interface RealisticMayotteMapProps {
  villages: Village[];
  currentVillage: string;
  onVillagePress: (villageId: string) => void;
  scale?: number;
}

const RealisticMayotteMap: React.FC<RealisticMayotteMapProps> = ({
  villages,
  currentVillage,
  onVillagePress,
  scale = 1,
}) => {
  // Coordonnées réalistes basées sur la vraie géographie de Mayotte
  const mayotteMainIslandPath = `
    M 200,150 
    C 180,120 160,140 140,180
    C 120,220 110,280 120,320
    C 130,360 150,400 180,440
    C 220,480 260,500 300,520
    C 340,540 380,560 420,580
    C 460,600 500,620 540,640
    C 580,650 620,640 650,620
    C 680,600 700,570 720,540
    C 740,510 760,480 780,440
    C 800,400 820,360 840,320
    C 860,280 870,240 860,200
    C 850,160 830,120 800,100
    C 770,80 730,70 690,80
    C 650,90 610,110 570,140
    C 530,170 490,200 450,220
    C 410,240 370,250 330,240
    C 290,230 250,210 220,180
    C 200,165 200,150 200,150 Z
  `;

  // Petite Terre (Dzaoudzi/Labattoir)
  const mayottePetiteTerrePath = `
    M 850,320
    C 860,310 880,315 890,325
    C 900,335 895,345 885,350
    C 875,355 865,350 860,340
    C 855,330 850,320 850,320 Z
  `;

  // Zones de récifs coralliens
  const coralReefPath = `
    M 100,100
    C 120,80 900,50 950,100
    C 980,150 950,700 900,720
    C 850,740 150,750 100,700
    C 80,650 70,500 80,350
    C 90,200 100,100 100,100 Z
  `;

  const [zoomLevel, setZoomLevel] = useState(1);
  const [panOffset, setPanOffset] = useState({ x: 0, y: 0 });
  const pan = useRef(new Animated.ValueXY({ x: 0, y: 0 })).current;
  const zoom = useRef(new Animated.Value(1)).current;

  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: () => true,
      onPanResponderGrant: () => {
        pan.setOffset({
          x: pan.x._value,
          y: pan.y._value,
        });
      },
      onPanResponderMove: Animated.event([null, { dx: pan.x, dy: pan.y }], {
        useNativeDriver: false,
      }),
      onPanResponderRelease: () => {
        pan.flattenOffset();
      },
    })
  ).current;

  const zoomIn = () => {
    const newZoom = Math.min(zoomLevel * 1.5, 3);
    setZoomLevel(newZoom);
    Animated.spring(zoom, {
      toValue: newZoom,
      useNativeDriver: false,
    }).start();
  };

  const zoomOut = () => {
    const newZoom = Math.max(zoomLevel / 1.5, 0.5);
    setZoomLevel(newZoom);
    Animated.spring(zoom, {
      toValue: newZoom,
      useNativeDriver: false,
    }).start();
  };

  const resetView = () => {
    setZoomLevel(1);
    setPanOffset({ x: 0, y: 0 });
    Animated.parallel([
      Animated.spring(zoom, { toValue: 1, useNativeDriver: false }),
      Animated.spring(pan, { toValue: { x: 0, y: 0 }, useNativeDriver: false }),
    ]).start();
  };

  const renderVillage = (village: Village) => {
    const isCurrentVillage = village.id === currentVillage;
    const isUnlocked = village.unlocked;
    
    return (
      <G key={village.id}>
        {/* Cercle du village */}
        <Circle
          cx={village.pos.x}
          cy={village.pos.y}
          r={isCurrentVillage ? 8 : 6}
          fill={
            isCurrentVillage 
              ? '#FF6B35' 
              : isUnlocked 
                ? village.type === 'prefecture' 
                  ? '#4A90E2' 
                  : '#34C759'
                : '#8E8E93'
          }
          stroke={isCurrentVillage ? '#FF3B00' : '#FFFFFF'}
          strokeWidth={2}
          onPress={() => isUnlocked && onVillagePress(village.id)}
        />
        
        {/* Nom du village */}
        <SvgText
          x={village.pos.x}
          y={village.pos.y - 12}
          fontSize="12"
          fill={isUnlocked ? '#2C3E50' : '#8E8E93'}
          textAnchor="middle"
          fontWeight={isCurrentVillage ? 'bold' : 'normal'}
        >
          {village.name}
        </SvgText>
        
        {/* Icône spéciale pour préfecture */}
        {village.type === 'prefecture' && (
          <Circle
            cx={village.pos.x + 10}
            cy={village.pos.y - 10}
            r={4}
            fill="#FFD700"
            stroke="#FFA500"
            strokeWidth={1}
          />
        )}
        
        {/* Icône de verrouillage si non débloqué */}
        {!isUnlocked && (
          <Circle
            cx={village.pos.x}
            cy={village.pos.y}
            r={10}
            fill="rgba(0,0,0,0.3)"
          />
        )}
      </G>
    );
  };

  return (
    <View style={styles.container}>
      {/* Contrôles de zoom */}
      <View style={styles.zoomControls}>
        <View style={styles.zoomButton} onTouchEnd={zoomIn}>
          <Ionicons name="add" size={20} color="#FFFFFF" />
        </View>
        <View style={styles.zoomButton} onTouchEnd={zoomOut}>
          <Ionicons name="remove" size={20} color="#FFFFFF" />
        </View>
        <View style={styles.zoomButton} onTouchEnd={resetView}>
          <Ionicons name="refresh" size={20} color="#FFFFFF" />
        </View>
      </View>

      {/* Carte interactive */}
      <Animated.View
        style={[
          styles.mapContainer,
          {
            transform: [
              { translateX: pan.x },
              { translateY: pan.y },
              { scale: zoom },
            ],
          },
        ]}
        {...panResponder.panHandlers}
      >
        <Svg width={1000} height={800} viewBox="0 0 1000 800">
          <Defs>
            {/* Dégradé pour l'océan */}
            <LinearGradient id="oceanGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <Stop offset="0%" stopColor="#4FC3F7" />
              <Stop offset="50%" stopColor="#29B6F6" />
              <Stop offset="100%" stopColor="#0288D1" />
            </LinearGradient>
            
            {/* Dégradé pour l'île principale */}
            <LinearGradient id="landGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <Stop offset="0%" stopColor="#66BB6A" />
              <Stop offset="30%" stopColor="#4CAF50" />
              <Stop offset="70%" stopColor="#388E3C" />
              <Stop offset="100%" stopColor="#2E7D32" />
            </LinearGradient>
            
            {/* Dégradé pour les récifs */}
            <LinearGradient id="reefGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <Stop offset="0%" stopColor="#80DEEA" />
              <Stop offset="100%" stopColor="#4DD0E1" />
            </LinearGradient>

            {/* Zone de clipping pour les effets */}
            <ClipPath id="islandClip">
              <Path d={mayotteMainIslandPath} />
            </ClipPath>
          </Defs>

          {/* Fond océan */}
          <Rect width="100%" height="100%" fill="url(#oceanGradient)" />
          
          {/* Récifs coralliens */}
          <Path
            d={coralReefPath}
            fill="url(#reefGradient)"
            opacity={0.3}
            stroke="#00BCD4"
            strokeWidth={1}
            strokeDasharray="5,5"
          />
          
          {/* Île principale (Grande Terre) */}
          <Path
            d={mayotteMainIslandPath}
            fill="url(#landGradient)"
            stroke="#2E7D32"
            strokeWidth={2}
          />
          
          {/* Petite Terre */}
          <Path
            d={mayottePetiteTerrePath}
            fill="url(#landGradient)"
            stroke="#2E7D32"
            strokeWidth={2}
          />

          {/* Villages */}
          {villages.map(renderVillage)}
          
          {/* Légende */}
          <G transform="translate(50, 650)">
            <Rect width="200" height="120" fill="rgba(255,255,255,0.9)" rx="8" />
            
            <SvgText x="10" y="20" fontSize="14" fill="#2C3E50" fontWeight="bold">
              Légende
            </SvgText>
            
            <Circle cx="20" cy="40" r="5" fill="#4A90E2" />
            <SvgText x="35" y="45" fontSize="12" fill="#2C3E50">Préfecture</SvgText>
            
            <Circle cx="20" cy="60" r="5" fill="#34C759" />
            <SvgText x="35" y="65" fontSize="12" fill="#2C3E50">Commune</SvgText>
            
            <Circle cx="20" cy="80" r="5" fill="#FF6B35" />
            <SvgText x="35" y="85" fontSize="12" fill="#2C3E50">Position actuelle</SvgText>
            
            <Circle cx="20" cy="100" r="5" fill="#8E8E93" />
            <SvgText x="35" y="105" fontSize="12" fill="#2C3E50">Non débloqué</SvgText>
          </G>
        </Svg>
      </Animated.View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E3F2FD',
  },
  mapContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  zoomControls: {
    position: 'absolute',
    top: 50,
    right: 20,
    zIndex: 10,
    gap: 8,
  },
  zoomButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
});

export default RealisticMayotteMap;