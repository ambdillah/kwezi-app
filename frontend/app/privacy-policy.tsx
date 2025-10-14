import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

export default function PrivacyPolicyScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#4A90E2', '#357ABD']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
      >
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#FFF" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Politique de Confidentialité</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        <Text style={styles.lastUpdate}>Dernière mise à jour : 11 octobre 2024</Text>

        <Text style={styles.intro}>
          L'application Kwezi, éditée par Ambdillah BACAR, accorde une grande importance à la 
          protection de vos données personnelles. Cette politique de confidentialité vous informe 
          sur la manière dont nous collectons, utilisons et protégeons vos données.
        </Text>

        <Text style={styles.sectionTitle}>1. Responsable du traitement</Text>
        <Text style={styles.paragraph}>
          Le responsable du traitement des données personnelles est :{'\n\n'}
          <Text style={styles.bold}>Ambdillah BACAR</Text>{'\n'}
          SIRET : 88819641700016{'\n'}
          Email : ambdillah-bacar@hotmail.fr{'\n'}
          Téléphone : 06 13 65 30 76
        </Text>

        <Text style={styles.sectionTitle}>2. Données collectées</Text>
        <Text style={styles.paragraph}>
          Kwezi collecte uniquement les données strictement nécessaires au fonctionnement 
          de l'application :
        </Text>
        <Text style={styles.bulletPoint}>• Identifiant utilisateur unique (user_id) généré automatiquement</Text>
        <Text style={styles.bulletPoint}>• Adresse email (optionnelle, si vous la fournissez)</Text>
        <Text style={styles.bulletPoint}>• Progression d'apprentissage (mots appris, scores)</Text>
        <Text style={styles.bulletPoint}>• Statistiques d'utilisation (jours de connexion, exercices complétés)</Text>
        <Text style={styles.bulletPoint}>• Informations d'abonnement Premium (via Stripe)</Text>

        <Text style={styles.highlight}>
          ℹ️ Kwezi n'utilise pas de cookies et ne collecte aucune donnée de navigation web.
        </Text>

        <Text style={styles.sectionTitle}>3. Finalités du traitement</Text>
        <Text style={styles.paragraph}>Vos données sont utilisées exclusivement pour :</Text>
        <Text style={styles.bulletPoint}>• Personnaliser votre expérience d'apprentissage</Text>
        <Text style={styles.bulletPoint}>• Sauvegarder votre progression</Text>
        <Text style={styles.bulletPoint}>• Gérer votre abonnement Premium (paiement et facturation via Stripe)</Text>
        <Text style={styles.bulletPoint}>• Vous contacter en cas de besoin (support, mises à jour importantes)</Text>
        <Text style={styles.bulletPoint}>• Améliorer l'application (statistiques anonymisées)</Text>

        <Text style={styles.sectionTitle}>4. Base légale du traitement</Text>
        <Text style={styles.paragraph}>
          Le traitement de vos données repose sur :{'\n\n'}
          • <Text style={styles.bold}>Votre consentement</Text> : lors de l'utilisation de l'application{'\n'}
          • <Text style={styles.bold}>L'exécution du contrat</Text> : gestion de votre abonnement Premium{'\n'}
          • <Text style={styles.bold}>Notre intérêt légitime</Text> : amélioration du service
        </Text>

        <Text style={styles.sectionTitle}>5. Destinataires des données</Text>
        <Text style={styles.paragraph}>
          Vos données personnelles ne sont <Text style={styles.bold}>jamais vendues</Text> à des tiers.
        </Text>
        <Text style={styles.paragraph}>
          Seuls les prestataires suivants ont accès à vos données :{'\n\n'}
          • <Text style={styles.bold}>Stripe Inc.</Text> : traitement sécurisé des paiements 
          (conforme PCI DSS Level 1 et RGPD, serveurs en Union Européenne){'\n'}
          • <Text style={styles.bold}>Emergent.sh</Text> : hébergement de l'infrastructure 
          (serveurs en France)
        </Text>

        <Text style={styles.sectionTitle}>6. Durée de conservation</Text>
        <Text style={styles.paragraph}>
          Vos données sont conservées :{'\n\n'}
          • <Text style={styles.bold}>Tant que votre compte est actif</Text>{'\n'}
          • <Text style={styles.bold}>+ 1 an après suppression</Text> pour obligations légales 
          (facturation, contentieux éventuel){'\n'}
          • <Text style={styles.bold}>Données de paiement</Text> : conservées par Stripe selon 
          leurs conditions (jamais sur nos serveurs)
        </Text>

        <Text style={styles.sectionTitle}>7. Vos droits (RGPD)</Text>
        <Text style={styles.paragraph}>
          Conformément au Règlement Général sur la Protection des Données (RGPD), vous disposez des 
          droits suivants :
        </Text>

        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Droit d'accès</Text> : obtenir une copie de vos données</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Droit de rectification</Text> : corriger vos données inexactes</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Droit à l'effacement</Text> : supprimer votre compte et vos données</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Droit à la portabilité</Text> : récupérer vos données dans un format structuré</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Droit d'opposition</Text> : vous opposer au traitement de vos données</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Droit à la limitation</Text> : limiter le traitement de vos données</Text>

        <Text style={styles.paragraph}>
          Pour exercer ces droits, contactez-nous :{'\n\n'}
          📧 <Text style={styles.link}>ambdillah-bacar@hotmail.fr</Text>{'\n'}
          📞 06 13 65 30 76
        </Text>

        <Text style={styles.highlight}>
          ℹ️ Réponse sous 1 mois maximum. Une pièce d'identité pourra être demandée 
          pour vérifier votre identité.
        </Text>

        <Text style={styles.sectionTitle}>8. Sécurité des données</Text>
        <Text style={styles.paragraph}>
          Nous mettons en œuvre toutes les mesures techniques et organisationnelles appropriées 
          pour protéger vos données :
        </Text>
        <Text style={styles.bulletPoint}>• Chiffrement des communications (HTTPS/TLS)</Text>
        <Text style={styles.bulletPoint}>• Authentification sécurisée</Text>
        <Text style={styles.bulletPoint}>• Accès restreint aux données</Text>
        <Text style={styles.bulletPoint}>• Paiements sécurisés via Stripe (PCI DSS Level 1)</Text>
        <Text style={styles.bulletPoint}>• Serveurs hébergés en France</Text>
        <Text style={styles.bulletPoint}>• Sauvegardes régulières</Text>

        <Text style={styles.sectionTitle}>9. Transferts hors Union Européenne</Text>
        <Text style={styles.paragraph}>
          Vos données sont <Text style={styles.bold}>hébergées en France</Text> (Union Européenne).
        </Text>
        <Text style={styles.paragraph}>
          Stripe, notre prestataire de paiement, est basé aux États-Unis mais utilise des serveurs 
          en Union Européenne pour les clients européens et est conforme au RGPD.
        </Text>

        <Text style={styles.sectionTitle}>10. Mineurs</Text>
        <Text style={styles.paragraph}>
          Kwezi est accessible aux mineurs. Si vous avez moins de 15 ans, l'autorisation d'un 
          parent ou tuteur légal est requise pour utiliser l'application.
        </Text>

        <Text style={styles.sectionTitle}>11. Modifications de la politique</Text>
        <Text style={styles.paragraph}>
          Cette politique de confidentialité peut être mise à jour. Toute modification substantielle 
          vous sera notifiée via l'application ou par email.
        </Text>

        <Text style={styles.sectionTitle}>12. Réclamation (CNIL)</Text>
        <Text style={styles.paragraph}>
          Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une 
          réclamation auprès de la Commission Nationale de l'Informatique et des Libertés (CNIL) :
        </Text>
        <Text style={styles.paragraph}>
          CNIL{'\n'}
          3 Place de Fontenoy{'\n'}
          TSA 80715{'\n'}
          75334 Paris Cedex 07{'\n'}
          🌐 www.cnil.fr
        </Text>

        <Text style={styles.sectionTitle}>13. Contact</Text>
        <Text style={styles.paragraph}>
          Pour toute question concernant cette politique de confidentialité ou vos données 
          personnelles, contactez-nous :
        </Text>
        <Text style={styles.contactBox}>
          📧 ambdillah-bacar@hotmail.fr{'\n'}
          📞 06 13 65 30 76{'\n'}
          📝 SIRET : 88819641700016
        </Text>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            © 2024 Kwezi - Ambdillah BACAR{'\n'}
            Tous droits réservés
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  backButton: {
    padding: 8,
    marginRight: 12,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFF',
    flex: 1,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  lastUpdate: {
    fontSize: 12,
    color: '#7F8C8D',
    fontStyle: 'italic',
    marginBottom: 15,
  },
  intro: {
    fontSize: 15,
    color: '#2C3E50',
    lineHeight: 22,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginTop: 20,
    marginBottom: 12,
  },
  paragraph: {
    fontSize: 14,
    color: '#2C3E50',
    lineHeight: 21,
    marginBottom: 12,
  },
  bulletPoint: {
    fontSize: 14,
    color: '#2C3E50',
    lineHeight: 21,
    marginBottom: 8,
    paddingLeft: 10,
  },
  bold: {
    fontWeight: 'bold',
  },
  link: {
    color: '#4A90E2',
    textDecorationLine: 'underline',
  },
  highlight: {
    backgroundColor: '#E3F2FD',
    padding: 12,
    borderRadius: 8,
    fontSize: 13,
    color: '#1976D2',
    marginVertical: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#4A90E2',
  },
  contactBox: {
    backgroundColor: '#FFF',
    padding: 15,
    borderRadius: 10,
    fontSize: 14,
    color: '#2C3E50',
    lineHeight: 21,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  footer: {
    marginTop: 30,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#95A5A6',
    textAlign: 'center',
    lineHeight: 18,
  },
});
