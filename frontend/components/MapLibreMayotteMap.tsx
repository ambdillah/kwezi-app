import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  StyleSheet,
  Dimensions,
  Alert,
} from 'react-native';
import MapLibreGL from '@maplibre/maplibre-react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  interpolate,
  Easing,
} from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';
import {
  MAYOTTE_VILLAGES,
  MAYOTTE_COASTLINE,
  MAYOTTE_PATHS,
  MAYOTTE_CENTER,
  MAYOTTE_BOUNDS,
  VillageGeoData,
  GeoCoordinate,
  GeoPath
} from '../utils/mayotteGeoData';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// Configuration MapLibre
MapLibreGL.setAccessToken(null); // Pas besoin de token pour MapLibre

interface MapLibreMayotteMapProps {
  villages: VillageGeoData[];
  currentVillage: string;
  onVillagePress: (villageId: string) => void;
  makiPosition?: GeoCoordinate;
  isMoving?: boolean;
}

const MapLibreMayotteMap: React.FC<MapLibreMayotteMapProps> = ({
  villages,
  currentVillage,
  onVillagePress,
  makiPosition,
  isMoving = false,
}) => {
  const mapRef = useRef<MapLibreGL.MapView>(null);
  const cameraRef = useRef<MapLibreGL.Camera>(null);
  
  // Animation du maki
  const makiScale = useSharedValue(1);
  const makiRotation = useSharedValue(0);

  useEffect(() => {
    // Animation du maki quand il bouge
    if (isMoving) {
      makiScale.value = withTiming(1.2, { duration: 200 });
      makiRotation.value = withTiming(360, { 
        duration: 1000, 
        easing: Easing.linear 
      });
    } else {
      makiScale.value = withTiming(1, { duration: 200 });
      makiRotation.value = withTiming(0, { duration: 200 });
    }
  }, [isMoving]);

  // Style animé pour le maki
  const makiAnimatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        { scale: makiScale.value },
        { rotate: `${makiRotation.value}deg` }
      ],
    };
  });

  // Style de carte custom pour Mayotte
  const mapStyle = {
    version: 8,
    sources: {
      'osm-tiles': {
        type: 'raster',
        tiles: [
          'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
        ],
        tileSize: 256,
        attribution: '© OpenStreetMap contributors'
      },
      'mayotte-coastline': {
        type: 'geojson',
        data: MAYOTTE_COASTLINE
      }
    },
    layers: [
      {
        id: 'osm-tiles-layer',
        type: 'raster',
        source: 'osm-tiles',
        minzoom: 8,
        maxzoom: 18
      },
      {
        id: 'mayotte-fill',
        type: 'fill',
        source: 'mayotte-coastline',
        paint: {
          'fill-color': '#66BB6A',
          'fill-opacity': 0.8
        }
      },
      {
        id: 'mayotte-outline',
        type: 'line',
        source: 'mayotte-coastline',
        paint: {
          'line-color': '#2E7D32',
          'line-width': 2
        }
      },
      {
        id: 'water',
        type: 'background',
        paint: {
          'background-color': '#4FC3F7'
        }
      }
    ]
  };

  const handleVillagePress = (village: VillageGeoData) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    onVillagePress(village.id);
  };

  const centerOnVillage = (villageId: string) => {
    const village = villages.find(v => v.id === villageId);
    if (village && cameraRef.current) {
      cameraRef.current.setCamera({
        centerCoordinate: [village.coordinates.longitude, village.coordinates.latitude],
        zoomLevel: 12,
        animationDuration: 1000,
      });
    }
  };

  useEffect(() => {
    // Centrer sur le village actuel
    if (currentVillage) {
      centerOnVillage(currentVillage);
    }
  }, [currentVillage]);

  const renderVillageMarkers = () => {
    return villages.map((village) => {
      const isCurrentVillage = village.id === currentVillage;
      const isUnlocked = village.unlocked;

      return (
        <MapLibreGL.PointAnnotation
          key={village.id}
          id={village.id}
          coordinate={[village.coordinates.longitude, village.coordinates.latitude]}
          onSelected={() => handleVillagePress(village)}
        >
          <View style={[
            styles.villageMarker,
            {
              backgroundColor: isCurrentVillage 
                ? '#FF6B35' 
                : isUnlocked 
                  ? village.type === 'prefecture' 
                    ? '#4A90E2' 
                    : '#34C759'
                  : '#8E8E93',
              borderColor: isCurrentVillage ? '#FF3B00' : '#FFFFFF',
              transform: [{ scale: isCurrentVillage ? 1.2 : 1 }]
            }
          ]}>
            {village.type === 'prefecture' && (
              <View style={styles.prefectureIcon} />
            )}
            {!isUnlocked && (
              <View style={styles.lockedOverlay} />
            )}
          </View>

          <MapLibreGL.Callout title={village.name}>
            <View style={styles.callout}>
              <View style={styles.calloutHeader}>
                <View style={styles.calloutTitle}>
                  {village.name}
                </View>
                {village.type === 'prefecture' && (
                  <View style={styles.calloutBadge}>
                    Préfecture
                  </View>
                )}
              </View>
              <View style={styles.calloutContent}>
                🌟 {village.meta.specialite}
              </View>
              {village.meta.population && (
                <View style={styles.calloutPopulation}>
                  👥 {village.meta.population.toLocaleString()} habitants
                </View>
              )}
            </View>
          </MapLibreGL.Callout>
        </MapLibreGL.PointAnnotation>
      );
    });
  };

  const renderMaki = () => {
    if (!makiPosition) return null;

    return (
      <MapLibreGL.PointAnnotation
        id="maki-position"
        coordinate={[makiPosition.longitude, makiPosition.latitude]}
      >
        <Animated.View style={[styles.makiContainer, makiAnimatedStyle]}>
          <View style={styles.maki}>
            <View style={styles.makiBody} />
            <View style={styles.makiFace}>
              <View style={styles.makiEye} />
              <View style={styles.makiEye} />
            </View>
            <View style={styles.makiTail} />
          </View>
          <View style={styles.makiShadow} />
        </Animated.View>
      </MapLibreGL.PointAnnotation>
    );
  };

  const renderPaths = () => {
    return MAYOTTE_PATHS.map((path) => {
      const fromVillage = villages.find(v => v.id === path.from);
      const toVillage = villages.find(v => v.id === path.to);
      
      if (!fromVillage || !toVillage || !fromVillage.unlocked || !toVillage.unlocked) {
        return null;
      }

      const coordinates = path.coordinates.map(coord => [coord.longitude, coord.latitude]);

      return (
        <MapLibreGL.ShapeSource
          key={`path-${path.from}-${path.to}`}
          id={`path-${path.from}-${path.to}`}
          shape={{
            type: 'Feature',
            geometry: {
              type: 'LineString',
              coordinates: coordinates
            }
          }}
        >
          <MapLibreGL.LineLayer
            id={`path-line-${path.from}-${path.to}`}
            style={{
              lineColor: path.transport === 'barge' ? '#2196F3' : 
                         path.transport === 'sentier' ? '#8BC34A' : '#FFC107',
              lineWidth: 3,
              lineDasharray: path.transport === 'sentier' ? [2, 2] : undefined,
              lineOpacity: 0.8
            }}
          />
        </MapLibreGL.ShapeSource>
      );
    });
  };

  return (
    <View style={styles.container}>
      <MapLibreGL.MapView
        ref={mapRef}
        style={styles.map}
        styleJSON={JSON.stringify(mapStyle)}
        logoEnabled={false}
        attributionEnabled={true}
        pitchEnabled={false}
        rotateEnabled={false}
        scrollEnabled={true}
        zoomEnabled={true}
      >
        <MapLibreGL.Camera
          ref={cameraRef}
          centerCoordinate={[MAYOTTE_CENTER.longitude, MAYOTTE_CENTER.latitude]}
          zoomLevel={10}
          bounds={{
            sw: [MAYOTTE_BOUNDS.southwest.longitude, MAYOTTE_BOUNDS.southwest.latitude],
            ne: [MAYOTTE_BOUNDS.northeast.longitude, MAYOTTE_BOUNDS.northeast.latitude]
          }}
          padding={{
            paddingTop: 50,
            paddingBottom: 50,
            paddingLeft: 20,
            paddingRight: 20
          }}
        />

        {/* Chemins entre villages */}
        {renderPaths()}

        {/* Marqueurs des villages */}
        {renderVillageMarkers()}

        {/* Maki animé */}
        {renderMaki()}
      </MapLibreGL.MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  villageMarker: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5,
  },
  prefectureIcon: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#FFD700',
  },
  lockedOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0,0,0,0.5)',
    borderRadius: 10,
  },
  callout: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    padding: 12,
    minWidth: 200,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  calloutHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  calloutTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  calloutBadge: {
    backgroundColor: '#4A90E2',
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: 'bold',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  calloutContent: {
    fontSize: 14,
    color: '#FF6B35',
    fontWeight: '600',
    marginBottom: 4,
  },
  calloutPopulation: {
    fontSize: 12,
    color: '#666666',
  },
  makiContainer: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  maki: {
    width: 28,
    height: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
  makiBody: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#A1887F',
    borderWidth: 1,
    borderColor: '#5D4037',
    position: 'absolute',
  },
  makiFace: {
    width: 16,
    height: 12,
    backgroundColor: '#BCAAA4',
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    position: 'absolute',
    top: 2,
  },
  makiEye: {
    width: 2,
    height: 2,
    borderRadius: 1,
    backgroundColor: '#2E7D32',
  },
  makiTail: {
    width: 8,
    height: 3,
    backgroundColor: '#8D6E63',
    borderRadius: 2,
    position: 'absolute',
    right: -6,
    top: 8,
  },
  makiShadow: {
    width: 16,
    height: 4,
    backgroundColor: 'rgba(0,0,0,0.3)',
    borderRadius: 2,
    position: 'absolute',
    bottom: -2,
  },
});

export default MapLibreMayotteMap;