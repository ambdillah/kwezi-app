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

export default function TermsOfSaleScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#27AE60', '#229954']}
        style={styles.header}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
      >
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <Ionicons name="arrow-back" size={24} color="#FFF" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Conditions Générales de Vente</Text>
      </LinearGradient>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        <Text style={styles.lastUpdate}>Dernière mise à jour : 11 octobre 2024</Text>

        <Text style={styles.intro}>
          Les présentes Conditions Générales de Vente (CGV) régissent la vente de l'abonnement 
          Premium à l'application Kwezi, édité par Ambdillah BACAR, entrepreneur individuel.
        </Text>

        <Text style={styles.sectionTitle}>Article 1 - Objet</Text>
        <Text style={styles.paragraph}>
          Les présentes CGV ont pour objet de définir les droits et obligations des parties dans 
          le cadre de la souscription à l'abonnement Premium de l'application Kwezi, disponible 
          sur iOS et Android.
        </Text>

        <Text style={styles.sectionTitle}>Article 2 - Éditeur et Contact</Text>
        <Text style={styles.contactBox}>
          <Text style={styles.bold}>Ambdillah BACAR</Text>{'\n'}
          Entrepreneur individuel{'\n'}
          SIRET : 88819641700016{'\n\n'}
          📧 ambdillah-bacar@hotmail.fr{'\n'}
          📞 06 13 65 30 76
        </Text>

        <Text style={styles.sectionTitle}>Article 3 - Service Proposé</Text>
        <Text style={styles.paragraph}>
          L'abonnement <Text style={styles.bold}>Kwezi Premium</Text> donne accès aux avantages suivants :
        </Text>
        <Text style={styles.bulletPoint}>• Accès illimité aux 626 mots en Shimaoré et Kibouchi (vs 250 en version gratuite)</Text>
        <Text style={styles.bulletPoint}>• Accès gratuit à toutes les fiches d'exercices PDF</Text>
        <Text style={styles.bulletPoint}>• Téléchargement de contenu pour utilisation hors ligne</Text>
        <Text style={styles.bulletPoint}>• Accès prioritaire aux nouvelles fonctionnalités et contenus</Text>
        <Text style={styles.bulletPoint}>• Soutien à la préservation et l'enseignement des langues de Mayotte</Text>

        <Text style={styles.sectionTitle}>Article 4 - Prix</Text>
        <Text style={styles.priceBox}>
          <Text style={styles.priceAmount}>2,90 € TTC par mois</Text>{'\n\n'}
          Prix incluant la TVA française au taux en vigueur (20%)
        </Text>
        <Text style={styles.paragraph}>
          Le prix est celui en vigueur au moment de la commande. Il est exprimé en euros, 
          toutes taxes comprises (TTC).
        </Text>
        <Text style={styles.paragraph}>
          L'éditeur se réserve le droit de modifier les prix à tout moment. Les modifications 
          ne s'appliquent pas aux abonnements déjà souscrits, qui conservent leur tarif initial 
          jusqu'à leur résiliation.
        </Text>

        <Text style={styles.sectionTitle}>Article 5 - Modalités de Paiement</Text>
        <Text style={styles.paragraph}>
          Le paiement s'effectue exclusivement en ligne par l'intermédiaire de la plateforme 
          sécurisée <Text style={styles.bold}>Stripe</Text>.
        </Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Moyens de paiement acceptés :</Text>{'\n'}
          • Carte bancaire (Visa, Mastercard, American Express){'\n'}
          • PayPal
        </Text>
        <Text style={styles.paragraph}>
          Le paiement est <Text style={styles.bold}>prélevé automatiquement chaque mois</Text> à 
          la date anniversaire de votre souscription.
        </Text>
        <Text style={styles.highlight}>
          🔒 Paiement 100% sécurisé{'\n'}
          Stripe est certifié PCI DSS Level 1 (le plus haut niveau de sécurité).{'\n'}
          Kwezi ne stocke jamais vos données bancaires.
        </Text>

        <Text style={styles.sectionTitle}>Article 6 - Durée et Résiliation</Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Durée :</Text> L'abonnement Premium est souscrit pour une 
          durée d'<Text style={styles.bold}>un mois</Text>, renouvelable automatiquement par 
          tacite reconduction.
        </Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Résiliation :</Text> Vous pouvez résilier votre abonnement 
          à tout moment, sans frais et sans justification, via le bouton "Gérer mon abonnement" 
          dans l'application.
        </Text>
        <Text style={styles.paragraph}>
          La résiliation prend effet <Text style={styles.bold}>immédiatement</Text> mais vous 
          conservez l'accès Premium jusqu'à la <Text style={styles.bold}>fin de la période déjà 
          payée</Text>.
        </Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Exemple :</Text> Si vous souscrivez le 1er janvier et 
          résiliez le 15 janvier, vous gardez l'accès Premium jusqu'au 31 janvier inclus.
        </Text>

        <Text style={styles.sectionTitle}>Article 7 - Droit de Rétractation</Text>
        <Text style={styles.paragraph}>
          Conformément à l'article L221-18 du Code de la consommation, vous disposez d'un délai 
          de <Text style={styles.bold}>14 jours</Text> pour exercer votre droit de rétractation 
          à compter de la souscription de l'abonnement.
        </Text>
        
        <Text style={styles.warningBox}>
          ⚠️ IMPORTANT - Modalités de rétractation{'\n\n'}
          En cas d'exercice du droit de rétractation dans les 14 jours :{'\n\n'}
          • <Text style={styles.bold}>Aucun remboursement</Text> des sommes déjà payées ne sera effectué{'\n'}
          • <Text style={styles.bold}>Arrêt immédiat</Text> des prélèvements futurs{'\n'}
          • <Text style={styles.bold}>Conservation de l'accès</Text> jusqu'à la fin de la période payée
        </Text>

        <Text style={styles.paragraph}>
          Pour exercer ce droit, contactez-nous :{'\n\n'}
          📧 ambdillah-bacar@hotmail.fr{'\n'}
          📞 06 13 65 30 76{'\n\n'}
          Ou résiliez directement via le bouton "Gérer mon abonnement" dans l'application.
        </Text>

        <Text style={styles.sectionTitle}>Article 8 - Disponibilité du Service</Text>
        <Text style={styles.paragraph}>
          L'éditeur s'engage à fournir le service avec diligence et selon les règles de l'art. 
          Le service est accessible 24h/24 et 7j/7, sauf en cas de :
        </Text>
        <Text style={styles.bulletPoint}>• Maintenance programmée (notification préalable)</Text>
        <Text style={styles.bulletPoint}>• Force majeure ou cas fortuit</Text>
        <Text style={styles.bulletPoint}>• Défaillance des réseaux de télécommunication</Text>

        <Text style={styles.paragraph}>
          L'éditeur ne saurait être tenu responsable des interruptions et des conséquences qui 
          peuvent en découler pour l'utilisateur ou tout tiers.
        </Text>

        <Text style={styles.sectionTitle}>Article 9 - Responsabilité</Text>
        <Text style={styles.paragraph}>
          L'éditeur ne peut être tenu responsable :
        </Text>
        <Text style={styles.bulletPoint}>• Des dommages indirects (perte de données, manque à gagner, etc.)</Text>
        <Text style={styles.bulletPoint}>• De l'impossibilité temporaire d'accès au service</Text>
        <Text style={styles.bulletPoint}>• De l'usage frauduleux des moyens de paiement par un tiers</Text>
        <Text style={styles.bulletPoint}>• Du non-respect des présentes CGV par l'utilisateur</Text>

        <Text style={styles.paragraph}>
          En tout état de cause, la responsabilité de l'éditeur est limitée au montant de 
          l'abonnement payé par l'utilisateur au cours des 12 derniers mois.
        </Text>

        <Text style={styles.sectionTitle}>Article 10 - Utilisation par les Enfants et Responsabilité Parentale</Text>
        <Text style={styles.warningBox}>
          ⚠️ AVERTISSEMENT IMPORTANT
        </Text>
        <Text style={styles.paragraph}>
          L'application Kwezi est un <Text style={styles.bold}>outil éducatif mis à disposition du public</Text>. 
          L'éditeur ne peut être tenu responsable des conséquences liées à l'utilisation de cet outil 
          par le public, notamment les enfants.
        </Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Âge recommandé :</Text> Cette application est recommandée pour les 
          enfants ayant l'âge de lire et de s'éduquer (généralement à partir de 6 ans), sous la 
          supervision d'un adulte.
        </Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Responsabilité parentale :</Text> Il appartient aux parents ou 
          responsables légaux de :
        </Text>
        <Text style={styles.bulletPoint}>• Superviser l'utilisation de l'application par les enfants</Text>
        <Text style={styles.bulletPoint}>• S'assurer que le contenu est adapté à l'âge et au niveau de l'enfant</Text>
        <Text style={styles.bulletPoint}>• Contrôler le temps d'écran et l'utilisation du service</Text>
        <Text style={styles.bulletPoint}>• Gérer les achats et abonnements effectués depuis l'appareil</Text>
        <Text style={styles.paragraph}>
          L'éditeur décline toute responsabilité en cas d'utilisation inappropriée ou non supervisée 
          de l'application par des mineurs. Les parents sont seuls responsables de l'encadrement de 
          leurs enfants dans l'utilisation de cette application éducative.
        </Text>

        <Text style={styles.sectionTitle}>Article 11 - Propriété Intellectuelle</Text>
        <Text style={styles.paragraph}>
          Tous les contenus présents dans l'application Kwezi (textes, images, audios, 
          vidéos, marques, logos, etc.) sont la propriété exclusive d'Ambdillah BACAR ou 
          de ses partenaires.
        </Text>
        <Text style={styles.paragraph}>
          Toute reproduction, représentation, modification, publication ou adaptation, totale 
          ou partielle, est strictement interdite sans autorisation écrite préalable, sauf pour 
          usage personnel et privé.
        </Text>

        <Text style={styles.sectionTitle}>Article 11 - Données Personnelles</Text>
        <Text style={styles.paragraph}>
          Le traitement de vos données personnelles est régi par notre Politique de Confidentialité, 
          accessible dans l'application.
        </Text>
        <Text style={styles.paragraph}>
          Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement, 
          de portabilité et d'opposition sur vos données personnelles.
        </Text>

        <Text style={styles.sectionTitle}>Article 12 - Modification des CGV</Text>
        <Text style={styles.paragraph}>
          L'éditeur se réserve le droit de modifier les présentes CGV à tout moment. Les 
          modifications entrent en vigueur dès leur publication dans l'application.
        </Text>
        <Text style={styles.paragraph}>
          Les utilisateurs seront informés des modifications substantielles par notification 
          dans l'application ou par email.
        </Text>

        <Text style={styles.sectionTitle}>Article 13 - Droit Applicable et Juridiction</Text>
        <Text style={styles.paragraph}>
          Les présentes CGV sont régies par le <Text style={styles.bold}>droit français</Text>.
        </Text>
        <Text style={styles.paragraph}>
          En cas de litige, une solution amiable sera recherchée avant toute action judiciaire.
        </Text>
        <Text style={styles.paragraph}>
          À défaut d'accord amiable, tout litige relatif à l'interprétation ou à l'exécution 
          des présentes CGV sera de la compétence exclusive des tribunaux français.
        </Text>
        <Text style={styles.paragraph}>
          Conformément à l'article L612-1 du Code de la consommation, vous pouvez également 
          recourir gratuitement à un médiateur de la consommation en cas de litige :
        </Text>
        <Text style={styles.paragraph}>
          <Text style={styles.bold}>Médiateur de la consommation :</Text>{'\n'}
          Centre de médiation et règlement amiable des huissiers de justice (CNMH){'\n'}
          🌐 www.cnmh-conso.fr
        </Text>

        <Text style={styles.sectionTitle}>Article 14 - Réclamation</Text>
        <Text style={styles.paragraph}>
          Pour toute réclamation, contactez le service client :
        </Text>
        <Text style={styles.contactBox}>
          📧 ambdillah-bacar@hotmail.fr{'\n'}
          📞 06 13 65 30 76{'\n\n'}
          Réponse sous 48 heures ouvrées
        </Text>

        <Text style={styles.sectionTitle}>Article 15 - Acceptation des CGV</Text>
        <Text style={styles.paragraph}>
          La souscription à l'abonnement Premium implique l'acceptation pleine et entière des 
          présentes Conditions Générales de Vente, que l'utilisateur reconnaît avoir lues et comprises.
        </Text>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            © 2024 Kwezi - Ambdillah BACAR{'\n'}
            SIRET : 88819641700016{'\n'}
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
    fontSize: 18,
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
  priceBox: {
    backgroundColor: '#E8F5E9',
    padding: 15,
    borderRadius: 10,
    fontSize: 14,
    color: '#2C3E50',
    lineHeight: 21,
    marginVertical: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#27AE60',
  },
  priceAmount: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#27AE60',
  },
  warningBox: {
    backgroundColor: '#FFF3CD',
    padding: 15,
    borderRadius: 10,
    fontSize: 13,
    color: '#856404',
    marginVertical: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#FFC107',
    lineHeight: 20,
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
    lineHeight: 20,
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
