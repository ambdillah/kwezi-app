import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface MapZoomControlsProps {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetView: () => void;
  currentZoom: number;
  minZoom?: number;
  maxZoom?: number;
}

/**
 * Contrôles de zoom pour la carte de Mayotte
 */
const MapZoomControls: React.FC<MapZoomControlsProps> = ({
  onZoomIn,
  onZoomOut,
  onResetView,
  currentZoom,
  minZoom = 0.5,
  maxZoom = 3.0
}) => {
  const canZoomIn = currentZoom < maxZoom;
  const canZoomOut = currentZoom > minZoom;

  return (
    <View style={styles.container}>
      {/* Bouton Zoom In */}
      <TouchableOpacity
        style={[styles.zoomButton, !canZoomIn && styles.disabledButton]}
        onPress={onZoomIn}
        disabled={!canZoomIn}
      >
        <Ionicons name="add" size={20} color={canZoomIn ? "white" : "#AAA"} />
      </TouchableOpacity>

      {/* Indicateur de zoom */}
      <View style={styles.zoomIndicator}>
        <Text style={styles.zoomText}>
          {(currentZoom * 100).toFixed(0)}%
        </Text>
      </View>

      {/* Bouton Zoom Out */}
      <TouchableOpacity
        style={[styles.zoomButton, !canZoomOut && styles.disabledButton]}
        onPress={onZoomOut}
        disabled={!canZoomOut}
      >
        <Ionicons name="remove" size={20} color={canZoomOut ? "white" : "#AAA"} />
      </TouchableOpacity>

      {/* Bouton Reset vue */}
      <TouchableOpacity
        style={styles.resetButton}
        onPress={onResetView}
      >
        <Ionicons name="refresh" size={16} color="#666" />
        <Text style={styles.resetText}>Reset</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    right: 15,
    top: 60,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 25,
    paddingVertical: 8,
    paddingHorizontal: 6,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    alignItems: 'center',
  },
  zoomButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#4ECDC4',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 4,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3,
  },
  disabledButton: {
    backgroundColor: '#E0E0E0',
  },
  zoomIndicator: {
    paddingHorizontal: 8,
    paddingVertical: 6,
    marginVertical: 6,
    backgroundColor: '#F5F5F5',
    borderRadius: 12,
    minWidth: 45,
    alignItems: 'center',
  },
  zoomText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: '#333',
  },
  resetButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 6,
    marginTop: 8,
    backgroundColor: '#F8F9FA',
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#E9ECEF',
  },
  resetText: {
    fontSize: 9,
    color: '#666',
    marginLeft: 4,
    fontWeight: '600',
  },
});

export default MapZoomControls;