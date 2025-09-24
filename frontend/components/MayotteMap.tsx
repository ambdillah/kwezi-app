import React from 'react';
import { View } from 'react-native';
import Svg, { Path, Circle, Text as SvgText, G, Defs, LinearGradient, Stop } from 'react-native-svg';

interface MayotteMapProps {
  width: number;
  height: number;
  onCommunePress: (commune: CommuneData) => void;
  unlockedCommunes: string[];
  currentCommune?: string;
  makiPosition: { x: number; y: number };
}

export interface CommuneData {
  id: string;
  name: string;
  position: { x: number; y: number };
  isUnlocked: boolean;
  price?: number;
}

/**
 * Composant carte SVG de Mayotte avec communes et villages
 * Basé sur la géographie réelle de l'île
 */
const MayotteMap: React.FC<MayotteMapProps> = ({
  width,
  height,
  onCommunePress,
  unlockedCommunes,
  currentCommune,
  makiPosition
}) => {

  // Coordonnées des principales communes de Mayotte (adaptées au SVG)
  const communes: CommuneData[] = [
    { id: 'mamoudzou', name: 'Mamoudzou', position: { x: 200, y: 180 }, isUnlocked: true }, // Capitale - débloquée par défaut
    { id: 'dzaoudzi', name: 'Dzaoudzi', position: { x: 300, y: 220 }, isUnlocked: false },
    { id: 'sada', name: 'Sada', position: { x: 120, y: 160 }, isUnlocked: false },
    { id: 'chirongui', name: 'Chirongui', position: { x: 160, y: 240 }, isUnlocked: false },
    { id: 'tsingoni', name: 'Tsingoni', position: { x: 180, y: 140 }, isUnlocked: false },
    { id: 'koungou', name: 'Koungou', position: { x: 220, y: 120 }, isUnlocked: false },
    { id: 'dembeni', name: 'Dembéni', position: { x: 140, y: 200 }, isUnlocked: false },
    { id: 'bandrele', name: 'Bandrélé', position: { x: 180, y: 280 }, isUnlocked: false, price: 2.99 },
    { id: 'kani_keli', name: 'Kani-Kéli', position: { x: 150, y: 300 }, isUnlocked: false, price: 2.99 },
    { id: 'boueni', name: 'Bouéni', position: { x: 120, y: 240 }, isUnlocked: false, price: 4.99 },
  ];

  // Forme simplifiée de l'île de Mayotte (Grande-Terre)
  const mayotteIslandPath = `
    M 100 120
    Q 120 100 160 110
    L 240 100
    Q 280 110 310 140
    Q 330 160 340 200
    Q 345 240 330 280
    Q 310 320 280 340
    L 200 350
    Q 160 340 130 320
    Q 100 290 90 250
    Q 85 200 100 120
    Z
  `;

  // Petite-Terre (Dzaoudzi/Pamandzi)
  const petiteTerreSize = 25;

  const getCommuneStatus = (communeId: string) => {
    if (unlockedCommunes.includes(communeId) || communeId === 'mamoudzou') {
      return currentCommune === communeId ? 'current' : 'unlocked';
    }
    return 'locked';
  };

  const getCommuneColor = (status: string) => {
    switch (status) {
      case 'current': return '#FF6B35'; // Orange pour commune actuelle
      case 'unlocked': return '#28A745'; // Vert pour débloquée
      case 'locked': return '#6C757D'; // Gris pour verrouillée
      default: return '#6C757D';
    }
  };

  return (
    <View style={{ alignItems: 'center' }}>
      <Svg width={width} height={height} viewBox="0 0 400 400">
        <Defs>
          {/* Dégradé pour l'océan */}
          <LinearGradient id="oceanGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#4FC3F7" />
            <Stop offset="100%" stopColor="#29B6F6" />
          </LinearGradient>
          
          {/* Dégradé pour l'île */}
          <LinearGradient id="islandGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#A5D6A7" />
            <Stop offset="50%" stopColor="#81C784" />
            <Stop offset="100%" stopColor="#66BB6A" />
          </LinearGradient>
          
          {/* Ombre pour l'île */}
          <LinearGradient id="islandShadow" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#4CAF50" />
            <Stop offset="100%" stopColor="#388E3C" />
          </LinearGradient>
        </Defs>

        {/* Fond océan */}
        <Circle cx="200" cy="200" r="180" fill="url(#oceanGradient)" />
        
        {/* Île principale (Grande-Terre) avec ombre */}
        <Path 
          d={mayotteIslandPath} 
          fill="url(#islandShadow)"
          transform="translate(2, 2)"
          opacity="0.3"
        />
        <Path 
          d={mayotteIslandPath} 
          fill="url(#islandGradient)"
          stroke="#2E7D32"
          strokeWidth="2"
        />
        
        {/* Petite-Terre (Dzaoudzi) */}
        <Circle 
          cx={300} 
          cy={220} 
          r={petiteTerreSize} 
          fill="url(#islandGradient)"
          stroke="#2E7D32"
          strokeWidth="2"
        />

        {/* Communes avec cercles interactifs */}
        {communes.map(commune => {
          const status = getCommuneStatus(commune.id);
          const color = getCommuneColor(status);
          const isInteractive = status !== 'locked';
          
          return (
            <G key={commune.id}>
              {/* Point de la commune */}
              <Circle
                cx={commune.position.x}
                cy={commune.position.y}
                r={status === 'current' ? 12 : 8}
                fill={color}
                stroke="white"
                strokeWidth="2"
                opacity={status === 'locked' ? 0.6 : 1}
                onPress={() => isInteractive && onCommunePress(commune)}
              />
              
              {/* Icône de verrouillage pour communes payantes */}
              {status === 'locked' && commune.price && (
                <SvgText
                  x={commune.position.x}
                  y={commune.position.y + 2}
                  fontSize="8"
                  fill="white"
                  textAnchor="middle"
                  fontWeight="bold"
                >
                  🔒
                </SvgText>
              )}
              
              {/* Nom de la commune */}
              <SvgText
                x={commune.position.x}
                y={commune.position.y - 18}
                fontSize="10"
                fill="#2C3E50"
                textAnchor="middle"
                fontWeight="bold"
              >
                {commune.name}
              </SvgText>
              
              {/* Prix pour communes payantes */}
              {commune.price && status === 'locked' && (
                <SvgText
                  x={commune.position.x}
                  y={commune.position.y + 25}
                  fontSize="8"
                  fill="#E91E63"
                  textAnchor="middle"
                  fontWeight="bold"
                >
                  €{commune.price}
                </SvgText>
              )}
            </G>
          );
        })}

        {/* Maki animé */}
        <G>
          <Circle
            cx={makiPosition.x}
            cy={makiPosition.y}
            r="15"
            fill="#8D6E63"
            stroke="#5D4037"
            strokeWidth="2"
          />
          {/* Visage du maki */}
          <Circle cx={makiPosition.x - 4} cy={makiPosition.y - 3} r="2" fill="black" />
          <Circle cx={makiPosition.x + 4} cy={makiPosition.y - 3} r="2" fill="black" />
          <Circle cx={makiPosition.x} cy={makiPosition.y + 3} r="1" fill="black" />
          
          {/* Queue du maki */}
          <Path
            d={`M ${makiPosition.x + 12} ${makiPosition.y} Q ${makiPosition.x + 20} ${makiPosition.y - 8} ${makiPosition.x + 15} ${makiPosition.y + 5}`}
            stroke="#8D6E63"
            strokeWidth="4"
            fill="none"
            strokeLinecap="round"
          />
        </G>

        {/* Titre de la carte */}
        <SvgText
          x="200"
          y="30"
          fontSize="16"
          fill="#2C3E50"
          textAnchor="middle"
          fontWeight="bold"
        >
          🗺️ Découverte de Mayotte
        </SvgText>
        
        {/* Légende */}
        <G>
          <SvgText x="20" y="360" fontSize="8" fill="#666" fontWeight="bold">
            Légende:
          </SvgText>
          <Circle cx="30" cy="375" r="4" fill="#28A745" />
          <SvgText x="40" y="378" fontSize="8" fill="#666">Débloqué</SvgText>
          
          <Circle cx="100" cy="375" r="4" fill="#FF6B35" />
          <SvgText x="110" y="378" fontSize="8" fill="#666">Actuel</SvgText>
          
          <Circle cx="160" cy="375" r="4" fill="#6C757D" />
          <SvgText x="170" y="378" fontSize="8" fill="#666">Verrouillé</SvgText>
        </G>
      </Svg>
    </View>
  );
};

export default MayotteMap;