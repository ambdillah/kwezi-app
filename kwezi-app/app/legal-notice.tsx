import React from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  Linking,
} from 'react-native';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

export default function LegalNoticeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#E67E22', '#D35400']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
      >
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#FFF" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Mentions Légales</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        <Text style={styles.lastUpdate}>Dernière mise à jour : 11 octobre 2024</Text>

        <Text style={styles.intro}>
          Conformément aux dispositions de la loi n° 2004-575 du 21 juin 2004 pour la confiance 
          dans l'économie numérique, il est précisé aux utilisateurs de l'application Kwezi 
          l'identité des différents intervenants dans le cadre de sa réalisation et de son suivi.
        </Text>

        <Text style={styles.sectionTitle}>1. Éditeur de l'Application</Text>
        <Text style={styles.editorBox}>
          <Text style={styles.bold}>Ambdillah BACAR</Text>{'\n'}
          Entrepreneur individuel{'\n\n'}
          SIRET : 88819641700016{'\n\n'}
          📧 Email : ambdillah-bacar@hotmail.fr{'\n'}
          📞 Téléphone : 06 13 65 30 76
        </Text>

        <Text style={styles.sectionTitle}>2. Directeur de la Publication</Text>
        <Text style={styles.paragraph}>
          Le directeur de la publication de l'application Kwezi est :
        </Text>
        <Text style={styles.highlight}>
          <Text style={styles.bold}>Ambdillah BACAR</Text>
        </Text>

        <Text style={styles.sectionTitle}>3. Hébergement</Text>
        <Text style={styles.paragraph}>
          L'application Kwezi est développée avec les technologies suivantes :
        </Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Frontend :</Text> React Native / Expo</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Backend :</Text> FastAPI (Python)</Text>
        <Text style={styles.bulletPoint}>• <Text style={styles.bold}>Base de données :</Text> MongoDB</Text>

        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Infrastructure d'hébergement :</Text>
        </Text>
        <Text style={styles.hostingBox}>
          <Text style={styles.bold}>Emergent.sh</Text>{'\n\n'}
          Plateforme de développement et d'hébergement{'\n'}
          Serveurs localisés en France{'\n'}
          Conformité RGPD et hébergement sécurisé
        </Text>

        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Traitement des paiements :</Text>
        </Text>
        <Text style={styles.hostingBox}>
          <Text style={styles.bold}>Stripe Inc.</Text>{'\n'}
          510 Townsend Street{'\n'}
          San Francisco, CA 94103{'\n'}
          États-Unis{'\n\n'}
          🔒 Certifié PCI DSS Level 1{'\n'}
          🇪🇺 Serveurs Union Européenne pour clients EU{'\n'}
          ✅ Conforme RGPD
        </Text>

        <Text style={styles.sectionTitle}>4. Propriété Intellectuelle</Text>
        <Text style={styles.paragraph}>
          L'ensemble des contenus de l'application Kwezi (structure, textes, audios, images, 
          vidéos, bases de données, logiciels, marques, logos, etc.) est la propriété exclusive 
          d'Ambdillah BACAR, sauf mention contraire.
        </Text>
        <Text style={styles.paragraph}>
          Toute reproduction, représentation, modification, publication, transmission, dénaturation, 
          totale ou partielle de l'application ou de son contenu, par quelque procédé que ce soit 
          et sur quelque support que ce soit, est interdite, sauf autorisation écrite préalable.
        </Text>
        <Text style={styles.paragraph}>
          Seul l'usage à des fins exclusivement privées dans un cercle de famille est autorisé, 
          conformément aux dispositions du Code de la propriété intellectuelle.
        </Text>

        <Text style={styles.sectionTitle}>5. Responsabilité</Text>
        <Text style={styles.paragraph}>
          L'éditeur s'efforce d'assurer l'exactitude et la mise à jour des informations diffusées 
          sur l'application, dont il se réserve le droit de corriger le contenu à tout moment et 
          sans préavis.
        </Text>
        <Text style={styles.paragraph}>
          Toutefois, l'éditeur ne peut garantir l'exhaustivité ni l'absence d'évolution de ces 
          informations. Les informations fournies le sont à titre indicatif et ne sauraient 
          dispenser l'utilisateur d'une analyse complémentaire et personnalisée.
        </Text>
        <Text style={styles.paragraph}>
          L'éditeur ne pourra être tenu responsable des dommages directs et indirects causés au 
          matériel de l'utilisateur lors de l'accès à l'application Kwezi, et résultant soit de 
          l'utilisation d'un matériel ne répondant pas aux spécifications indiquées, soit de 
          l'apparition d'un bug ou d'une incompatibilité.
        </Text>

        <Text style={styles.sectionTitle}>6. Données Personnelles</Text>
        <Text style={styles.paragraph}>
          Le traitement des données personnelles des utilisateurs est régi par notre Politique 
          de Confidentialité, accessible dans l'application.
        </Text>
        <Text style={styles.paragraph}>
          Conformément au Règlement Général sur la Protection des Données (RGPD) et à la loi 
          Informatique et Libertés, les utilisateurs disposent d'un droit d'accès, de rectification, 
          d'effacement, de limitation, de portabilité et d'opposition sur leurs données personnelles.
        </Text>
        <TouchableOpacity onPress={() => router.push('/privacy-policy')}>
          <Text style={styles.link}>
            → Consulter la Politique de Confidentialité
          </Text>
        </TouchableOpacity>

        <Text style={styles.sectionTitle}>7. Cookies</Text>
        <Text style={styles.cookieBox}>
          ✅ <Text style={styles.bold}>Kwezi n'utilise PAS de cookies</Text>{'\n\n'}
          L'application ne collecte aucune donnée de navigation via cookies ou technologies 
          similaires. Seules les données strictement nécessaires au fonctionnement de l'application 
          sont stockées localement sur votre appareil.
        </Text>

        <Text style={styles.sectionTitle}>8. Liens Hypertextes</Text>
        <Text style={styles.paragraph}>
          L'application Kwezi peut contenir des liens hypertextes vers d'autres sites internet. 
          L'éditeur n'exerce aucun contrôle sur ces sites et décline toute responsabilité quant 
          à leur contenu.
        </Text>
        <Text style={styles.paragraph}>
          La présence de liens vers d'autres sites n'implique pas nécessairement une relation 
          entre l'éditeur et les propriétaires de ces sites, ni une validation du contenu de 
          ces sites.
        </Text>

        <Text style={styles.sectionTitle}>9. Droit Applicable</Text>
        <Text style={styles.paragraph}>
          Les présentes mentions légales sont régies par le droit français.
        </Text>
        <Text style={styles.paragraph}>
          En cas de litige, et à défaut d'accord amiable, les tribunaux français seront seuls 
          compétents.
        </Text>

        <Text style={styles.sectionTitle}>10. Modification des Mentions Légales</Text>
        <Text style={styles.paragraph}>
          L'éditeur se réserve le droit de modifier les présentes mentions légales à tout moment. 
          Les utilisateurs sont invités à les consulter régulièrement.
        </Text>

        <Text style={styles.sectionTitle}>11. Contact</Text>
        <Text style={styles.paragraph}>
          Pour toute question ou demande d'information concernant l'application, vous pouvez 
          nous contacter :
        </Text>
        <Text style={styles.contactBox}>
          <Text style={styles.bold}>Ambdillah BACAR</Text>{'\n\n'}
          📧 ambdillah-bacar@hotmail.fr{'\n'}
          📞 06 13 65 30 76{'\n\n'}
          SIRET : 88819641700016
        </Text>

        <Text style={styles.sectionTitle}>12. Crédits</Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Conception et développement :</Text> Ambdillah BACAR{'\n'}
          <Text style={styles.bold}>Contenu pédagogique :</Text> Équipe Kwezi{'\n'}
          <Text style={styles.bold}>Audios authentiques :</Text> Locuteurs natifs Shimaoré et Kibouchi{'\n'}
          <Text style={styles.bold}>Technologies :</Text> React Native, Expo, FastAPI, MongoDB, Stripe
        </Text>

        <View style={styles.footer}>
          <Text style={styles.footerTitle}>📱 Kwezi</Text>
          <Text style={styles.footerText}>
            Application d'apprentissage des langues{'\n'}
            Shimaoré et Kibouchi de Mayotte
          </Text>
          <View style={styles.footerLinks}>
            <TouchableOpacity onPress={() => router.push('/privacy-policy')}>
              <Text style={styles.footerLink}>Confidentialité</Text>
            </TouchableOpacity>
            <Text style={styles.footerSeparator}> • </Text>
            <TouchableOpacity onPress={() => router.push('/terms-of-sale')}>
              <Text style={styles.footerLink}>CGV</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.footerCopyright}>
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
    fontSize: 14,
    color: '#4A90E2',
    textDecorationLine: 'underline',
    marginVertical: 10,
  },
  editorBox: {
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
  hostingBox: {
    backgroundColor: '#F5F5F5',
    padding: 15,
    borderRadius: 10,
    fontSize: 13,
    color: '#2C3E50',
    lineHeight: 20,
    marginVertical: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#E67E22',
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
  cookieBox: {
    backgroundColor: '#D4EDDA',
    padding: 15,
    borderRadius: 10,
    fontSize: 13,
    color: '#155724',
    marginVertical: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#28A745',
    lineHeight: 20,
  },
  highlight: {
    backgroundColor: '#FFE5B4',
    padding: 12,
    borderRadius: 8,
    fontSize: 14,
    color: '#856404',
    marginVertical: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#E67E22',
    fontWeight: 'bold',
  },
  footer: {
    marginTop: 30,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
    alignItems: 'center',
  },
  footerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 5,
  },
  footerText: {
    fontSize: 13,
    color: '#7F8C8D',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 15,
  },
  footerLinks: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  footerLink: {
    fontSize: 13,
    color: '#4A90E2',
    textDecorationLine: 'underline',
  },
  footerSeparator: {
    fontSize: 13,
    color: '#95A5A6',
  },
  footerCopyright: {
    fontSize: 11,
    color: '#95A5A6',
    textAlign: 'center',
    lineHeight: 16,
  },
});
