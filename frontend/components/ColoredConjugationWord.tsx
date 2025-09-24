import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { separatePrefixAndRoot, getTenseColor } from '../utils/conjugationColorSystem';

interface ColoredConjugationWordProps {
  word: string;
  language: 'shimaore' | 'kibouchi';
  onPress?: () => void;
  style?: any;
  textStyle?: any;
  showTenseIndicator?: boolean;
  disabled?: boolean;
}

/**
 * Composant qui affiche un mot avec coloration automatique des préfixes de conjugaison
 */
const ColoredConjugationWord: React.FC<ColoredConjugationWordProps> = ({
  word,
  language,
  onPress,
  style,
  textStyle,
  showTenseIndicator = true,
  disabled = false
}) => {
  const { prefix, root, tense } = separatePrefixAndRoot(word, language);
  const tenseColor = getTenseColor(tense);
  const hasPrefix = prefix.length > 0;

  // Noms des temps en français
  const tenseNames = {
    present: 'Présent',
    past: 'Passé',
    future: 'Futur',
    default: ''
  };

  const WordContent = () => (
    <View style={[styles.wordContainer, style]}>
      <View style={styles.textContainer}>
        {hasPrefix ? (
          <>
            {/* Préfixe coloré */}
            <Text style={[
              styles.prefixText,
              textStyle,
              { color: tenseColor, fontWeight: 'bold' }
            ]}>
              {prefix}
            </Text>
            {/* Racine normale */}
            <Text style={[styles.rootText, textStyle]}>
              {root}
            </Text>
          </>
        ) : (
          /* Mot complet sans préfixe */
          <Text style={[styles.fullWordText, textStyle]}>
            {word}
          </Text>
        )}
      </View>
      
      {/* Indicateur de temps (optionnel) */}
      {showTenseIndicator && hasPrefix && tense !== 'default' && (
        <View style={[styles.tenseIndicator, { backgroundColor: tenseColor }]}>
          <Text style={styles.tenseIndicatorText}>
            {tenseNames[tense as keyof typeof tenseNames]}
          </Text>
        </View>
      )}
    </View>
  );

  if (onPress && !disabled) {
    return (
      <TouchableOpacity onPress={onPress} disabled={disabled}>
        <WordContent />
      </TouchableOpacity>
    );
  }

  return <WordContent />;
};

const styles = StyleSheet.create({
  wordContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  textContainer: {
    flexDirection: 'row',
    alignItems: 'baseline',
    flexWrap: 'wrap',
  },
  prefixText: {
    fontSize: 16,
    fontWeight: 'bold',
    // La couleur est définie dynamiquement via les props
  },
  rootText: {
    fontSize: 16,
    color: '#495057',
    fontWeight: '600',
  },
  fullWordText: {
    fontSize: 16,
    color: '#495057',
    fontWeight: '600',
  },
  tenseIndicator: {
    marginTop: 4,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 12,
    minWidth: 60,
    alignItems: 'center',
  },
  tenseIndicatorText: {
    color: 'white',
    fontSize: 10,
    fontWeight: 'bold',
    textTransform: 'uppercase',
  },
});

export default ColoredConjugationWord;