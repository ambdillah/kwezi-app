import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface ConjugationRulesProps {
  language: 'shimaore' | 'kibouchi';
  tense?: string;
  compact?: boolean;
}

const ConjugationRules: React.FC<ConjugationRulesProps> = ({ language, tense, compact = false }) => {
  
  const shimoareRules = {
    present: { label: 'Présent', example: 'nis, ous, as, ris, mous, was + verbe' },
    past: { label: 'Passé', example: 'naco, waco, aco, raco, moico, waco + verbe' },
    future: { label: 'Futur', example: 'nitso, outso, atso, ritso, moutso, watso + verbe' },
  };

  const kibouchiRules = {
    present: { label: 'Présent', example: 'Garder le verbe à l\'infinitif (avec le "m")' },
    past: { label: 'Passé', example: 'Remplacer "m" par "n"' },
    future: { label: 'Futur', example: 'Remplacer "m" par "Mbou"' },
  };

  const rules = language === 'shimaore' ? shimoareRules : kibouchiRules;
  const tenseKey = (tense || 'present') as keyof typeof rules;
  const currentRule = rules[tenseKey];

  if (compact) {
    return (
      <View style={styles.compactContainer}>
        <Text style={styles.compactTitle}>📚 {currentRule.label}</Text>
        <Text style={styles.compactRule}>{currentRule.example}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>📚 Règles de conjugaison - {language === 'shimaore' ? 'Shimaoré' : 'Kibouchi'}</Text>
      
      {Object.entries(rules).map(([key, rule]) => (
        <View key={key} style={[
          styles.ruleCard,
          tenseKey === key && styles.activeRuleCard
        ]}>
          <Text style={[
            styles.ruleLabel,
            tenseKey === key && styles.activeRuleLabel
          ]}>
            {rule.label}
          </Text>
          <Text style={styles.ruleExample}>{rule.example}</Text>
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#F8F9FA',
    borderRadius: 12,
    padding: 16,
    marginVertical: 12,
    borderWidth: 1,
    borderColor: '#E9ECEF',
  },
  title: {
    fontSize: 16,
    fontWeight: '700',
    color: '#2C3E50',
    marginBottom: 12,
    textAlign: 'center',
  },
  ruleCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    padding: 10,
    marginVertical: 4,
    borderWidth: 1,
    borderColor: '#DEE2E6',
  },
  activeRuleCard: {
    backgroundColor: '#E3F2FD',
    borderColor: '#4ECDC4',
    borderWidth: 2,
  },
  ruleLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#495057',
    marginBottom: 4,
  },
  activeRuleLabel: {
    color: '#2C3E50',
    fontWeight: '700',
  },
  ruleExample: {
    fontSize: 12,
    color: '#6C757D',
    fontStyle: 'italic',
  },
  compactContainer: {
    backgroundColor: '#FFF9E6',
    borderRadius: 8,
    padding: 12,
    marginVertical: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#FFB700',
  },
  compactTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#2C3E50',
    marginBottom: 4,
  },
  compactRule: {
    fontSize: 12,
    color: '#495057',
    fontStyle: 'italic',
  },
});

export default ConjugationRules;
