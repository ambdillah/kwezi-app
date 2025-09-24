import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Modal } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { getTenseExplanations, TENSE_COLORS } from '../utils/conjugationColorSystem';

interface ConjugationColorLegendProps {
  language: 'shimaore' | 'kibouchi';
  compact?: boolean;
}

/**
 * Composant qui affiche la légende des couleurs de conjugaison avec exemples
 */
const ConjugationColorLegend: React.FC<ConjugationColorLegendProps> = ({
  language,
  compact = false
}) => {
  const [showFullLegend, setShowFullLegend] = useState(false);
  const explanations = getTenseExplanations();

  const ColorDot = ({ color, tense }: { color: string; tense: string }) => (
    <View style={styles.colorDotContainer}>
      <View style={[styles.colorDot, { backgroundColor: color }]} />
      <Text style={styles.colorLabel}>
        {explanations[tense as keyof typeof explanations]?.name || tense}
      </Text>
    </View>
  );

  // Version compacte pour affichage en jeu
  if (compact) {
    return (
      <View style={styles.compactContainer}>
        <TouchableOpacity 
          style={styles.compactButton}
          onPress={() => setShowFullLegend(true)}
        >
          <Text style={styles.compactButtonText}>🎨 Guide des couleurs</Text>
          <Ionicons name="help-circle-outline" size={16} color="#666" />
        </TouchableOpacity>

        {/* Modal avec légende complète */}
        <Modal
          visible={showFullLegend}
          animationType="slide"
          transparent={true}
          onRequestClose={() => setShowFullLegend(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              <View style={styles.modalHeader}>
                <Text style={styles.modalTitle}>
                  🎨 Guide des couleurs de conjugaison
                </Text>
                <TouchableOpacity
                  style={styles.closeButton}
                  onPress={() => setShowFullLegend(false)}
                >
                  <Ionicons name="close" size={24} color="#666" />
                </TouchableOpacity>
              </View>

              <Text style={styles.modalSubtitle}>
                Les préfixes des VERBES CONJUGUÉS sont colorés selon le temps :
              </Text>
              
              <View style={styles.pronounsNote}>
                <Text style={styles.pronounsNoteText}>
                  ℹ️ Les pronoms (wami, wassi, zahou, etc.) ne sont pas colorés car ils ne changent pas selon les temps.
                </Text>
              </View>

              {Object.entries(explanations).map(([tense, info]) => (
                <View key={tense} style={styles.tenseExplanation}>
                  <View style={styles.tenseHeader}>
                    <View style={[styles.colorDot, { backgroundColor: info.color }]} />
                    <Text style={styles.tenseName}>{info.name}</Text>
                  </View>
                  <Text style={styles.tenseDescription}>{info.description}</Text>
                  
                  <View style={styles.examplesContainer}>
                    <Text style={styles.examplesTitle}>Exemples en {language === 'shimaore' ? 'Shimaoré' : 'Kibouchi'} :</Text>
                    {info.examples[language].map((example, index) => (
                      <Text key={index} style={styles.exampleText}>
                        • {example}
                      </Text>
                    ))}
                  </View>
                </View>
              ))}
              
              <View style={styles.tipContainer}>
                <Text style={styles.tipText}>
                  💡 <Text style={styles.tipBold}>Astuce :</Text> Regardez la couleur du préfixe pour identifier rapidement le temps !
                </Text>
              </View>
            </View>
          </View>
        </Modal>
      </View>
    );
  }

  // Version complète pour affichage permanent
  return (
    <View style={styles.fullContainer}>
      <Text style={styles.fullTitle}>Couleurs des temps :</Text>
      <View style={styles.colorsRow}>
        <ColorDot color={TENSE_COLORS.present} tense="present" />
        <ColorDot color={TENSE_COLORS.past} tense="past" />
        <ColorDot color={TENSE_COLORS.future} tense="future" />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  // Styles pour version compacte
  compactContainer: {
    alignItems: 'center',
    marginBottom: 8,
  },
  compactButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
    borderWidth: 1,
    borderColor: '#E9ECEF',
    gap: 6,
  },
  compactButtonText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },

  // Styles pour modal
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 20,
    maxWidth: 400,
    width: '100%',
    maxHeight: '80%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    flex: 1,
  },
  closeButton: {
    padding: 4,
  },
  modalSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 16,
    textAlign: 'center',
  },
  
  // Style pour note sur les pronoms
  pronounsNote: {
    backgroundColor: '#E8F4FD',
    padding: 10,
    borderRadius: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#007BFF',
    marginBottom: 16,
  },
  pronounsNoteText: {
    fontSize: 12,
    color: '#0056B3',
    fontStyle: 'italic',
  },

  // Styles pour explications des temps
  tenseExplanation: {
    marginBottom: 16,
    padding: 12,
    backgroundColor: '#F8F9FA',
    borderRadius: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#4ECDC4',
  },
  tenseHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  tenseName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginLeft: 8,
  },
  tenseDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    fontStyle: 'italic',
  },
  examplesContainer: {
    marginTop: 8,
  },
  examplesTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 4,
    textTransform: 'uppercase',
  },
  exampleText: {
    fontSize: 13,
    color: '#495057',
    marginBottom: 2,
    paddingLeft: 8,
  },

  // Styles pour tip
  tipContainer: {
    backgroundColor: '#FFF3CD',
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#FFC107',
    marginTop: 8,
  },
  tipText: {
    fontSize: 13,
    color: '#856404',
    textAlign: 'center',
  },
  tipBold: {
    fontWeight: 'bold',
  },

  // Styles pour version complète
  fullContainer: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 10,
    padding: 12,
    marginBottom: 12,
    alignItems: 'center',
  },
  fullTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  colorsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },

  // Styles pour dots de couleur
  colorDotContainer: {
    alignItems: 'center',
    flex: 1,
  },
  colorDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginBottom: 4,
  },
  colorLabel: {
    fontSize: 10,
    color: '#666',
    fontWeight: '600',
    textAlign: 'center',
  },
});

export default ConjugationColorLegend;