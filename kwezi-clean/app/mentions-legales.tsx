import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function MentionsLegales() {
  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#2563EB" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Mentions Légales</Text>
      </View>

      <ScrollView style={styles.scrollView} contentContainerStyle={styles.content}>
        <Text style={styles.lastUpdated}>Dernière mise à jour : 14 octobre 2025</Text>

        {/* Éditeur du site */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>1. Éditeur du Site</Text>
          <Text style={styles.text}>
            Le site et l'application mobile Kwezi sont édités par :
          </Text>
          <Text style={styles.text}>
            <Text style={styles.bold}>Raison sociale :</Text> Entreprise individuelle{'\n'}
            <Text style={styles.bold}>Nom commercial :</Text> Kwezi{'\n'}
            <Text style={styles.bold}>Directeur de la publication :</Text> Propriétaire de l'application{'\n'}
            <Text style={styles.bold}>Adresse :</Text> Mayotte, France{'\n'}
            <Text style={styles.bold}>Email :</Text> contact@kwezi-app.com{'\n'}
            <Text style={styles.bold}>SIRET :</Text> [À compléter si applicable]
          </Text>
        </View>

        {/* Hébergeur */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>2. Hébergement</Text>
          <Text style={styles.text}>
            L'application et ses services sont hébergés par :
          </Text>
          <Text style={styles.text}>
            <Text style={styles.bold}>Hébergeur :</Text> Services cloud professionnels{'\n'}
            <Text style={styles.bold}>Infrastructure :</Text> Serveurs sécurisés conformes aux normes européennes{'\n'}
            <Text style={styles.bold}>Localisation des données :</Text> Union Européenne
          </Text>
        </View>

        {/* Propriété intellectuelle */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>3. Propriété Intellectuelle</Text>
          <Text style={styles.text}>
            L'ensemble du contenu de l'application Kwezi (textes, images, logos, fichiers audio, 
            vidéos, bases de données) est la propriété exclusive de l'éditeur, sauf mention contraire.
          </Text>
          <Text style={styles.text}>
            Toute reproduction, distribution, modification, adaptation, retransmission ou publication 
            de ces différents éléments est strictement interdite sans l'accord exprès par écrit de l'éditeur.
          </Text>
          <Text style={styles.text}>
            Les enregistrements audio en langues shimaoré et kibouchi sont des créations originales 
            protégées par le droit d'auteur.
          </Text>
        </View>

        {/* Données personnelles */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>4. Données Personnelles</Text>
          <Text style={styles.text}>
            Le traitement de vos données personnelles est régi par notre Politique de Confidentialité, 
            conforme au Règlement Général sur la Protection des Données (RGPD).
          </Text>
          <Text style={styles.text}>
            <Text style={styles.bold}>Responsable du traitement :</Text> Kwezi{'\n'}
            <Text style={styles.bold}>Délégué à la protection des données :</Text> contact@kwezi-app.com
          </Text>
          <Text style={styles.text}>
            Vous disposez d'un droit d'accès, de rectification, de suppression et de portabilité 
            de vos données. Pour exercer ces droits, contactez-nous à : contact@kwezi-app.com
          </Text>
        </View>

        {/* Cookies */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>5. Cookies et Technologies de Suivi</Text>
          <Text style={styles.text}>
            L'application utilise des technologies de stockage local pour :
          </Text>
          <Text style={styles.bulletPoint}>• Sauvegarder votre progression d'apprentissage</Text>
          <Text style={styles.bulletPoint}>• Mémoriser vos préférences linguistiques</Text>
          <Text style={styles.bulletPoint}>• Améliorer votre expérience utilisateur</Text>
          <Text style={styles.text}>
            Ces données sont stockées localement sur votre appareil et ne sont pas transmises 
            à des tiers sans votre consentement.
          </Text>
        </View>

        {/* Limitation de responsabilité */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>6. Limitation de Responsabilité</Text>
          <Text style={styles.text}>
            L'éditeur s'efforce d'assurer l'exactitude et la mise à jour des informations diffusées 
            sur l'application. Toutefois, il ne peut garantir l'exactitude, la précision ou 
            l'exhaustivité des informations mises à disposition.
          </Text>
          <Text style={styles.text}>
            L'éditeur ne pourra être tenu responsable des dommages directs ou indirects résultant 
            de l'utilisation de l'application, notamment en cas d'interruption de service, de perte 
            de données ou de dysfonctionnement.
          </Text>
        </View>

        {/* Loi applicable */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>7. Loi Applicable et Juridiction</Text>
          <Text style={styles.text}>
            Les présentes mentions légales sont régies par le droit français.
          </Text>
          <Text style={styles.text}>
            En cas de litige, et à défaut d'accord amiable, le tribunal compétent sera celui 
            du ressort du siège social de l'éditeur ou du domicile du défendeur.
          </Text>
        </View>

        {/* Médiation */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>8. Médiation de la Consommation</Text>
          <Text style={styles.text}>
            Conformément à l'article L.612-1 du Code de la consommation, nous proposons un 
            dispositif de médiation de la consommation.
          </Text>
          <Text style={styles.text}>
            En cas de litige, vous pouvez déposer votre réclamation sur la plateforme de 
            Règlement en Ligne des Litiges (RLL) de la Commission Européenne : 
            https://ec.europa.eu/consumers/odr/
          </Text>
        </View>

        {/* Paiements et transactions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>9. Paiements et Transactions</Text>
          <Text style={styles.text}>
            Les paiements sont traités de manière sécurisée par Stripe, Inc., conforme aux 
            normes PCI-DSS et à la directive européenne sur les services de paiement (DSP2).
          </Text>
          <Text style={styles.text}>
            L'éditeur ne stocke aucune information de carte bancaire. Toutes les transactions 
            sont chiffrées et sécurisées.
          </Text>
        </View>

        {/* Crédits */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>10. Crédits</Text>
          <Text style={styles.text}>
            <Text style={styles.bold}>Conception et développement :</Text> Kwezi Team{'\n'}
            <Text style={styles.bold}>Enregistrements audio :</Text> Locuteurs natifs de Mayotte{'\n'}
            <Text style={styles.bold}>Contenu pédagogique :</Text> Experts en langues shimaoré et kibouchi{'\n'}
            <Text style={styles.bold}>Design graphique :</Text> Équipe interne
          </Text>
        </View>

        {/* Contact */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>11. Nous Contacter</Text>
          <Text style={styles.text}>
            Pour toute question concernant ces mentions légales, vous pouvez nous contacter :
          </Text>
          <Text style={styles.text}>
            <Text style={styles.bold}>Email :</Text> contact@kwezi-app.com{'\n'}
            <Text style={styles.bold}>Adresse :</Text> Mayotte, France
          </Text>
        </View>

        {/* Modifications */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>12. Modifications</Text>
          <Text style={styles.text}>
            L'éditeur se réserve le droit de modifier les présentes mentions légales à tout moment. 
            Les utilisateurs seront informés de toute modification significative.
          </Text>
          <Text style={styles.text}>
            La version en vigueur est celle accessible sur l'application à la date de votre utilisation.
          </Text>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            © 2025 Kwezi - Tous droits réservés
          </Text>
          <Text style={styles.footerText}>
            Application d'apprentissage des langues de Mayotte
          </Text>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
    paddingTop: 50,
  },
  backButton: {
    marginRight: 12,
    padding: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#111827',
  },
  scrollView: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  lastUpdated: {
    fontSize: 14,
    color: '#6B7280',
    fontStyle: 'italic',
    marginBottom: 24,
  },
  section: {
    marginBottom: 28,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1F2937',
    marginBottom: 12,
  },
  text: {
    fontSize: 15,
    lineHeight: 24,
    color: '#374151',
    marginBottom: 12,
  },
  bold: {
    fontWeight: '600',
    color: '#1F2937',
  },
  bulletPoint: {
    fontSize: 15,
    lineHeight: 24,
    color: '#374151',
    marginBottom: 8,
    paddingLeft: 8,
  },
  footer: {
    marginTop: 32,
    paddingTop: 24,
    borderTopWidth: 1,
    borderTopColor: '#E5E7EB',
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 4,
  },
});
