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
  Polygon,
} from 'react-native-svg';
import { Ionicons } from '@expo/vector-icons';
import { VillageGeoData, GeoCoordinate } from '../utils/mayotteGeoData';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

interface HybridRealisticMayotteMapProps {
  villages: VillageGeoData[];
  currentVillage: string;
  onVillagePress: (villageId: string) => void;
  makiPosition?: GeoCoordinate;
  isMoving?: boolean;
}

const HybridRealisticMayotteMap: React.FC<HybridRealisticMayotteMapProps> = ({
  villages,
  currentVillage,
  onVillagePress,
  makiPosition,
  isMoving = false,
}) => {
  // Coordonnées réelles converties en coordonnées SVG (avec bounding box de Mayotte)
  const MAYOTTE_BOUNDS = {
    minLat: -13.0000,
    maxLat: -12.6500,
    minLon: 45.0500,
    maxLon: 45.3000
  };

  const MAP_WIDTH = 1000;
  const MAP_HEIGHT = 800;

  // Convertir coordonnées GPS en coordonnées SVG
  const gpsToSvg = (gpsCoord: GeoCoordinate) => {
    const x = ((gpsCoord.longitude - MAYOTTE_BOUNDS.minLon) / (MAYOTTE_BOUNDS.maxLon - MAYOTTE_BOUNDS.minLon)) * MAP_WIDTH;
    const y = MAP_HEIGHT - ((gpsCoord.latitude - MAYOTTE_BOUNDS.minLat) / (MAYOTTE_BOUNDS.maxLat - MAYOTTE_BOUNDS.minLat)) * MAP_HEIGHT;
    return { x, y };
  };

  // Forme réaliste de Mayotte basée sur les vraies coordonnées
  const createMayotteShape = () => {
    // Points de contour de Grande-Terre (simplifiés mais basés sur OSM)
    const grandeTerreBounds = [
      { lat: -12.6717, lon: 45.1025 }, // Mtsamboro (Nord-Ouest)
      { lat: -12.6800, lon: 45.1300 }, // Nord
      { lat: -12.6900, lon: 45.1600 }, // Nord-Est
      { lat: -12.7200, lon: 45.2000 }, // Est
      { lat: -12.7336, lon: 45.2036 }, // Koungou
      { lat: -12.7500, lon: 45.2200 }, // Centre-Est
      { lat: -12.7822, lon: 45.2281 }, // Mamoudzou
      { lat: -12.8200, lon: 45.2200 }, // Sud-Est
      { lat: -12.8600, lon: 45.2100 }, // Sud-Est côte
      { lat: -12.9089, lon: 45.1958 }, // Bandrélé
      { lat: -12.9400, lon: 45.1900 }, // Sud
      { lat: -12.9683, lon: 45.1919 }, // Kani-Kéli (point Sud)
      { lat: -12.9400, lon: 45.1700 }, // Sud-Ouest
      { lat: -12.9075, lon: 45.1456 }, // Bouéni
      { lat: -12.8700, lon: 45.1300 }, // Ouest
      { lat: -12.8347, lon: 45.1300 }, // Sada
      { lat: -12.8000, lon: 45.1200 }, // Ouest
      { lat: -12.7847, lon: 45.1119 }, // Tsingoni
      { lat: -12.8267, lon: 45.1681 }, // Dembéni
      { lat: -12.8000, lon: 45.1400 }, // Centre-Ouest
      { lat: -12.7500, lon: 45.1200 }, // Nord-Ouest
      { lat: -12.7000, lon: 45.1100 }, // Nord-Ouest
    ];

    return grandeTerreBounds.map(coord => {
      const svgCoord = gpsToSvg(coord);
      return `${svgCoord.x},${svgCoord.y}`;
    }).join(' ');
  };

  // Petite-Terre (Dzaoudzi)
  const createPetiteTerrShape = () => {
    const petiteTerreBounds = [
      { lat: -12.7850, lon: 45.2550 }, // Nord-Ouest
      { lat: -12.7850, lon: 45.2700 }, // Nord-Est  
      { lat: -12.7950, lon: 45.2750 }, // Sud-Est
      { lat: -12.8000, lon: 45.2650 }, // Sud-Ouest
      { lat: -12.7950, lon: 45.2550 }, // Ouest
    ];

    return petiteTerreBounds.map(coord => {
      const svgCoord = gpsToSvg(coord);
      return `${svgCoord.x},${svgCoord.y}`;
    }).join(' ');
  };

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

  const renderVillage = (village: VillageGeoData) => {
    const svgPos = gpsToSvg(village.coordinates);
    const isCurrentVillage = village.id === currentVillage;
    const isUnlocked = village.unlocked;
    
    return (
      <G key={village.id}>
        {/* Cercle du village */}
        <Circle
          cx={svgPos.x}
          cy={svgPos.y}
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
          x={svgPos.x}
          y={svgPos.y - 12}
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
            cx={svgPos.x + 10}
            cy={svgPos.y - 10}
            r={4}
            fill="#FFD700"
            stroke="#FFA500"
            strokeWidth={1}
          />
        )}
        
        {/* Icône de verrouillage si non débloqué */}
        {!isUnlocked && (
          <Circle
            cx={svgPos.x}
            cy={svgPos.y}
            r={10}
            fill="rgba(0,0,0,0.3)"
          />
        )}
      </G>
    );
  };

  const renderMaki = () => {
    if (!makiPosition) return null;
    
    const svgPos = gpsToSvg(makiPosition);
    
    return (
      <G key="maki" transform={`translate(${svgPos.x - 16}, ${svgPos.y - 16})`}>
        {/* Ombre */}
        <Circle
          cx="16"
          cy="30"
          r="10"
          fill="rgba(0,0,0,0.2)"
        />
        
        {/* Corps du maki */}
        <Circle
          cx="16"
          cy="20"
          r="12"
          fill="#A1887F"
          stroke="#5D4037"
          strokeWidth="1"
        />
        
        {/* Tête */}
        <Circle
          cx="16"
          cy="12"
          r="10"
          fill="#BCAAA4"
          stroke="#5D4037"
          strokeWidth="1"
        />
        
        {/* Oreilles */}
        <Circle cx="10" cy="8" r="4" fill="#8D6E63" />
        <Circle cx="22" cy="8" r="4" fill="#8D6E63" />
        
        {/* Yeux */}
        <Circle cx="13" cy="11" r="2" fill="#2E7D32" />
        <Circle cx="19" cy="11" r="2" fill="#2E7D32" />
        
        {/* Reflets des yeux */}
        <Circle cx="13.5" cy="10.5" r="0.8" fill="#FFFFFF" />
        <Circle cx="19.5" cy="10.5" r="0.8" fill="#FFFFFF" />
        
        {/* Nez */}
        <Circle cx="16" cy="13" r="1" fill="#5D4037" />
        
        {/* Queue */}
        <Circle
          cx="5"
          cy="18"
          r="6"
          fill="#8D6E63"
          stroke="#5D4037"
          strokeWidth="0.5"
        />
        
        {/* Animation si en mouvement */}
        {isMoving && (
          <G>
            <Circle
              cx="16"
              cy="12"
              r="15"
              fill="none"
              stroke="#FF6B35"
              strokeWidth="2"
              strokeDasharray="5,5"
              opacity="0.6"
            />
          </G>
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
        <Svg width={MAP_WIDTH} height={MAP_HEIGHT} viewBox={`0 0 ${MAP_WIDTH} ${MAP_HEIGHT}`}>
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
          </Defs>

          {/* Fond océan */}
          <Rect width="100%" height="100%" fill="url(#oceanGradient)" />
          
          {/* Récifs coralliens (zone élargie autour de Mayotte) */}
          <Polygon
            points={`50,50 950,80 970,750 80,720`}
            fill="url(#reefGradient)"
            opacity={0.3}
            stroke="#00BCD4"
            strokeWidth={1}
            strokeDasharray="5,5"
          />
          
          {/* Grande-Terre (forme réaliste basée sur GPS) */}
          <Polygon
            points={createMayotteShape()}
            fill="url(#landGradient)"
            stroke="#2E7D32"
            strokeWidth={2}
          />
          
          {/* Petite-Terre (Dzaoudzi) */}
          <Polygon
            points={createPetiteTerrShape()}
            fill="url(#landGradient)"
            stroke="#2E7D32"
            strokeWidth={2}
          />

          {/* Villages avec vraies positions GPS */}
          {villages.map(renderVillage)}
          
          {/* Maki animé */}
          {renderMaki()}
          
          {/* Légende améliorée */}
          <G transform="translate(50, 650)">
            <Rect width="220" height="130" fill="rgba(255,255,255,0.95)" rx="8" stroke="#2E7D32" strokeWidth="1" />
            
            <SvgText x="10" y="20" fontSize="14" fill="#2E7D32" fontWeight="bold">
              Découverte de Mayotte
            </SvgText>
            
            <Circle cx="20" cy="40" r="5" fill="#4A90E2" />
            <SvgText x="35" y="45" fontSize="11" fill="#2C3E50">Préfecture</SvgText>
            
            <Circle cx="20" cy="60" r="5" fill="#34C759" />
            <SvgText x="35" y="65" fontSize="11" fill="#2C3E50">Commune</SvgText>
            
            <Circle cx="20" cy="80" r="5" fill="#FF6B35" />
            <SvgText x="35" y="85" fontSize="11" fill="#2C3E50">Position actuelle</SvgText>
            
            <Circle cx="20" cy="100" r="5" fill="#8E8E93" />
            <SvgText x="35" y="105" fontSize="11" fill="#2C3E50">Non débloqué</SvgText>
            
            <SvgText x="10" y="125" fontSize="10" fill="#666" fontStyle="italic">
              Coordonnées GPS réelles
            </SvgText>
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

export default HybridRealisticMayotteMap;