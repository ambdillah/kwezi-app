import React from 'react';
import { View } from 'react-native';
import Svg, { Path, Circle, Text as SvgText, G, Defs, LinearGradient, Stop, RadialGradient, Polygon, Ellipse } from 'react-native-svg';

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
 * Composant carte SVG détaillée et réaliste de Mayotte
 * Basée sur la véritable géographie de l'île en forme d'hippocampe
 */
const MayotteMap: React.FC<MayotteMapProps> = ({
  width,
  height,
  onCommunePress,
  unlockedCommunes,
  currentCommune,
  makiPosition
}) => {

  // Coordonnées réelles des communes de Mayotte (positionnement géographique authentique)
  const communes: CommuneData[] = [
    // Grande-Terre (île principale)
    { id: 'mamoudzou', name: 'Mamoudzou', position: { x: 285, y: 220 }, isUnlocked: true }, // Centre-est, capitale
    { id: 'koungou', name: 'Koungou', position: { x: 300, y: 180 }, isUnlocked: false }, // Nord-est
    { id: 'dembeni', name: 'Dembéni', position: { x: 240, y: 200 }, isUnlocked: false }, // Centre
    { id: 'tsoundzou', name: 'Tsoundzou', position: { x: 220, y: 180 }, isUnlocked: false }, // Centre-nord
    { id: 'tsingoni', name: 'Tsingoni', position: { x: 200, y: 190 }, isUnlocked: false }, // Centre-ouest
    { id: 'sada', name: 'Sada', position: { x: 160, y: 210 }, isUnlocked: false, price: 1.99 }, // Ouest
    { id: 'ouangani', name: 'Ouangani', position: { x: 180, y: 240 }, isUnlocked: false }, // Sud-ouest
    { id: 'chirongui', name: 'Chirongui', position: { x: 210, y: 280 }, isUnlocked: false }, // Sud
    { id: 'kani_keli', name: 'Kani-Kéli', position: { x: 190, y: 300 }, isUnlocked: false, price: 2.99 }, // Pointe sud
    { id: 'bandrele', name: 'Bandrélé', position: { x: 240, y: 290 }, isUnlocked: false, price: 2.99 }, // Sud-est
    { id: 'boueni', name: 'Bouéni', position: { x: 170, y: 260 }, isUnlocked: false, price: 4.99 }, // Sud-ouest
    { id: 'acoua', name: 'Acoua', position: { x: 220, y: 140 }, isUnlocked: false, price: 3.99 }, // Nord
    { id: 'mtsamboro', name: 'Mtsamboro', position: { x: 180, y: 150 }, isUnlocked: false, price: 3.99 }, // Nord-ouest
    
    // Petite-Terre
    { id: 'dzaoudzi', name: 'Dzaoudzi', position: { x: 350, y: 280 }, isUnlocked: false, price: 4.99 }, // Petite-Terre
    { id: 'pamandzi', name: 'Pamandzi', position: { x: 360, y: 290 }, isUnlocked: false, price: 4.99 }, // Aéroport
    
    // Communes rurales
    { id: 'bandraboua', name: 'Bandraboua', position: { x: 200, y: 160 }, isUnlocked: false, price: 2.99 }, // Nord-centre
    { id: 'mtsangamouji', name: 'Mtsangamouji', position: { x: 260, y: 160 }, isUnlocked: false, price: 2.99 }, // Nord-est
  ];

  // Forme détaillée et réaliste de Grande-Terre (ressemble à un hippocampe)
  const grandeTerreDetaillee = `
    M 180 140
    C 190 135 210 138 230 145
    L 250 150
    C 270 155 290 165 305 180
    C 315 190 320 205 318 220
    C 316 235 310 245 300 250
    L 285 255
    C 275 260 265 270 260 285
    C 255 295 250 300 240 305
    L 220 310
    C 200 315 185 312 175 305
    C 165 295 160 280 162 265
    C 164 250 170 240 175 225
    C 180 210 175 195 170 185
    C 165 170 168 155 175 150
    Z
  `;

  // Forme de Petite-Terre (Dzaoudzi-Pamandzi) - plus réaliste
  const petiteTerre = `
    M 345 275
    C 355 270 370 275 375 285
    C 378 295 375 300 365 305
    C 355 308 345 305 340 295
    C 338 285 342 280 345 275
    Z
  `;

  // Montagnes et reliefs de Mayotte (Mount Benara, Mount Choungui, etc.)
  const montagnes = [
    { x: 220, y: 200, name: 'Mt Benara', height: 660 }, // Point culminant
    { x: 200, y: 280, name: 'Mt Choungui', height: 594 },
    { x: 240, y: 180, name: 'Mt Combani', height: 477 },
    { x: 180, y: 180, name: 'Mt Mtsapéré', height: 572 },
  ];

  // Baies et caps caractéristiques
  const baies = [
    { path: 'M 160 200 Q 150 210 160 220 Q 170 215 160 200', name: 'Baie de Bouéni' }, // Ouest
    { path: 'M 280 210 Q 290 200 300 210 Q 295 220 280 210', name: 'Baie de Mamoudzou' }, // Est
    { path: 'M 200 290 Q 190 300 200 310 Q 210 305 200 290', name: 'Baie de Chirongui' }, // Sud
  ];

  // Récif corallien et lagon (caractéristique de Mayotte)
  const recifCorallien = `
    M 120 120
    Q 140 100 180 110
    L 260 105
    Q 300 110 330 130
    Q 360 150 380 190
    Q 390 230 385 270
    Q 380 310 360 340
    Q 330 365 290 375
    L 220 380
    Q 180 375 150 360
    Q 120 340 110 310
    Q 105 270 110 230
    Q 115 190 130 160
    Q 140 130 120 120
    Z
  `;

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
      case 'locked': return '#95A5A6'; // Gris pour verrouillée
      default: return '#95A5A6';
    }
  };

  return (
    <View style={{ alignItems: 'center' }}>
      <Svg width={width} height={height} viewBox="0 0 450 420">
        <Defs>
          {/* Dégradé pour l'océan Indien */}
          <RadialGradient id="oceanGradient" cx="50%" cy="50%" r="80%">
            <Stop offset="0%" stopColor="#1E88E5" />
            <Stop offset="40%" stopColor="#2196F3" />
            <Stop offset="80%" stopColor="#42A5F5" />
            <Stop offset="100%" stopColor="#64B5F6" />
          </RadialGradient>
          
          {/* Dégradé pour le lagon (eau turquoise) */}
          <RadialGradient id="lagonGradient" cx="50%" cy="50%" r="60%">
            <Stop offset="0%" stopColor="#4DD0E1" />
            <Stop offset="50%" stopColor="#26C6DA" />
            <Stop offset="100%" stopColor="#00BCD4" />
          </RadialGradient>
          
          {/* Dégradé pour Grande-Terre (végétation tropicale) */}
          <LinearGradient id="grandeTerreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#C8E6C9" />
            <Stop offset="30%" stopColor="#A5D6A7" />
            <Stop offset="60%" stopColor="#81C784" />
            <Stop offset="100%" stopColor="#66BB6A" />
          </LinearGradient>
          
          {/* Ombre pour les reliefs */}
          <LinearGradient id="reliefShadow" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#4CAF50" />
            <Stop offset="50%" stopColor="#388E3C" />
            <Stop offset="100%" stopColor="#2E7D32" />
          </LinearGradient>
          
          {/* Dégradé pour Petite-Terre */}
          <LinearGradient id="petiteTerreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#DCEDC8" />
            <Stop offset="50%" stopColor="#C5E1A5" />
            <Stop offset="100%" stopColor="#AED581" />
          </LinearGradient>

          {/* Dégradé pour récif corallien */}
          <LinearGradient id="recifGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor="#E0F2F1" />
            <Stop offset="50%" stopColor="#B2DFDB" />
            <Stop offset="100%" stopColor="#80CBC4" />
          </LinearGradient>
        </Defs>

        {/* Fond océan Indien */}
        <Circle cx="225" cy="210" r="200" fill="url(#oceanGradient)" />
        
        {/* Récif corallien et lagon */}
        <Path 
          d={recifCorallien}
          fill="url(#lagonGradient)"
          stroke="url(#recifGradient)"
          strokeWidth="3"
          opacity="0.8"
        />

        {/* Récif de corail (détails) */}
        <Path 
          d={recifCorallien}
          fill="none"
          stroke="#00ACC1"
          strokeWidth="1"
          strokeDasharray="3,2"
          opacity="0.6"
        />

        {/* Baies caractéristiques */}
        {baies.map((baie, index) => (
          <Path
            key={index}
            d={baie.path}
            fill="#1976D2"
            opacity="0.4"
          />
        ))}

        {/* Grande-Terre avec ombre réaliste */}
        <Path 
          d={grandeTerreDetaillee} 
          fill="url(#reliefShadow)"
          transform="translate(3, 3)"
          opacity="0.3"
        />
        <Path 
          d={grandeTerreDetaillee} 
          fill="url(#grandeTerreGradient)"
          stroke="#2E7D32"
          strokeWidth="2"
        />

        {/* Détails topographiques - montagnes */}
        {montagnes.map((montagne, index) => (
          <G key={index}>
            {/* Ombre de la montagne */}
            <Ellipse
              cx={montagne.x + 2}
              cy={montagne.y + 2}
              rx="8"
              ry="6"
              fill="#1B5E20"
              opacity="0.3"
            />
            {/* Montagne */}
            <Polygon
              points={`${montagne.x},${montagne.y - 8} ${montagne.x - 6},${montagne.y + 4} ${montagne.x + 6},${montagne.y + 4}`}
              fill="#388E3C"
              stroke="#2E7D32"
              strokeWidth="1"
            />
            {/* Sommet enneigé/nuageux */}
            <Polygon
              points={`${montagne.x},${montagne.y - 8} ${montagne.x - 3},${montagne.y - 2} ${montagne.x + 3},${montagne.y - 2}`}
              fill="#E8F5E8"
              opacity="0.8"
            />
          </G>
        ))}

        {/* Forêts et végétation dense */}
        <Circle cx="220" cy="200" r="15" fill="#2E7D32" opacity="0.6" />
        <Circle cx="240" cy="180" r="12" fill="#388E3C" opacity="0.5" />
        <Circle cx="200" cy="220" r="10" fill="#43A047" opacity="0.4" />
        <Circle cx="180" cy="180" r="8" fill="#4CAF50" opacity="0.5" />

        {/* Petite-Terre (Dzaoudzi-Pamandzi) avec ombre */}
        <Path 
          d={petiteTerre}
          fill="url(#reliefShadow)"
          transform="translate(2, 2)"
          opacity="0.3"
        />
        <Path 
          d={petiteTerre}
          fill="url(#petiteTerreGradient)"
          stroke="#689F38"
          strokeWidth="2"
        />

        {/* Aéroport sur Petite-Terre */}
        <G>
          <Ellipse cx="360" cy="290" rx="8" ry="4" fill="#78909C" stroke="#546E7A" strokeWidth="1" />
          <SvgText x="360" y="293" fontSize="6" fill="white" textAnchor="middle" fontWeight="bold">✈️</SvgText>
        </G>

        {/* Îlots et rochers autour de Mayotte */}
        <Circle cx="140" cy="160" r="3" fill="#A5D6A7" stroke="#4CAF50" strokeWidth="1" />
        <Circle cx="320" cy="140" r="2" fill="#C8E6C9" stroke="#66BB6A" strokeWidth="1" />
        <Circle cx="380" cy="320" r="2.5" fill="#DCEDC8" stroke="#8BC34A" strokeWidth="1" />
        <Circle cx="130" cy="280" r="2" fill="#E8F5E8" stroke="#9CCC65" strokeWidth="1" />

        {/* Routes principales (simplified) */}
        <Path 
          d="M 280 220 Q 250 200 220 190 Q 200 185 180 200" 
          stroke="#8D6E63" 
          strokeWidth="2" 
          fill="none"
          opacity="0.6"
        />
        <Path 
          d="M 280 220 Q 260 240 240 260 Q 220 280 200 290" 
          stroke="#8D6E63" 
          strokeWidth="2" 
          fill="none"
          opacity="0.6"
        />

        {/* Communes avec cercles interactifs et design amélioré */}
        {communes.map(commune => {
          const status = getCommuneStatus(commune.id);
          const color = getCommuneColor(status);
          const isInteractive = status !== 'locked';
          
          return (
            <G key={commune.id}>
              {/* Halo lumineux pour commune active */}
              {status === 'current' && (
                <Circle
                  cx={commune.position.x}
                  cy={commune.position.y}
                  r="20"
                  fill={color}
                  opacity="0.2"
                />
              )}
              
              {/* Ombre du point de commune */}
              <Circle
                cx={commune.position.x + 1}
                cy={commune.position.y + 1}
                r={status === 'current' ? 12 : 8}
                fill="#000000"
                opacity="0.3"
              />
              
              {/* Point principal de la commune */}
              <Circle
                cx={commune.position.x}
                cy={commune.position.y}
                r={status === 'current' ? 12 : 8}
                fill={color}
                stroke="white"
                strokeWidth="2"
                opacity={status === 'locked' ? 0.7 : 1}
                onPress={() => isInteractive && onCommunePress(commune)}
              />
              
              {/* Anneau décoratif pour commune débloquée */}
              {status === 'unlocked' && (
                <Circle
                  cx={commune.position.x}
                  cy={commune.position.y}
                  r="12"
                  fill="none"
                  stroke={color}
                  strokeWidth="1"
                  opacity="0.5"
                />
              )}
              
              {/* Icône de verrouillage pour communes payantes */}
              {status === 'locked' && commune.price && (
                <SvgText
                  x={commune.position.x}
                  y={commune.position.y + 3}
                  fontSize="8"
                  fill="white"
                  textAnchor="middle"
                  fontWeight="bold"
                >
                  🔒
                </SvgText>
              )}
              
              {/* Nom de la commune avec fond semi-transparent */}
              <G>
                <SvgText
                  x={commune.position.x}
                  y={commune.position.y - 20}
                  fontSize="9"
                  fill="white"
                  textAnchor="middle"
                  fontWeight="bold"
                  stroke="#2C3E50"
                  strokeWidth="0.5"
                >
                  {commune.name}
                </SvgText>
              </G>
              
              {/* Prix pour communes payantes */}
              {commune.price && status === 'locked' && (
                <G>
                  <SvgText
                    x={commune.position.x}
                    y={commune.position.y + 25}
                    fontSize="8"
                    fill="#E91E63"
                    textAnchor="middle"
                    fontWeight="bold"
                    stroke="white"
                    strokeWidth="0.3"
                  >
                    €{commune.price}
                  </SvgText>
                </G>
              )}
            </G>
          );
        })}

        {/* Maki aventurier avec design amélioré */}
        <G>
          {/* Ombre du maki */}
          <Ellipse
            cx={makiPosition.x + 2}
            cy={makiPosition.y + 18}
            rx="12"
            ry="4"
            fill="#000000"
            opacity="0.3"
          />
          
          {/* Corps du maki */}
          <Ellipse
            cx={makiPosition.x}
            cy={makiPosition.y + 5}
            rx="12"
            ry="16"
            fill="#8D6E63"
            stroke="#5D4037"
            strokeWidth="1"
          />
          
          {/* Tête du maki */}
          <Circle
            cx={makiPosition.x}
            cy={makiPosition.y - 5}
            r="10"
            fill="#A1887F"
            stroke="#6D4C41"
            strokeWidth="1"
          />
          
          {/* Oreilles */}
          <Circle cx={makiPosition.x - 7} cy={makiPosition.y - 10} r="4" fill="#8D6E63" />
          <Circle cx={makiPosition.x + 7} cy={makiPosition.y - 10} r="4" fill="#8D6E63" />
          
          {/* Yeux */}
          <Circle cx={makiPosition.x - 3} cy={makiPosition.y - 7} r="2" fill="white" />
          <Circle cx={makiPosition.x + 3} cy={makiPosition.y - 7} r="2" fill="white" />
          <Circle cx={makiPosition.x - 3} cy={makiPosition.y - 7} r="1" fill="black" />
          <Circle cx={makiPosition.x + 3} cy={makiPosition.y - 7} r="1" fill="black" />
          
          {/* Museau */}
          <Ellipse cx={makiPosition.x} cy={makiPosition.y - 2} rx="3" ry="2" fill="#BCAAA4" />
          <Circle cx={makiPosition.x} cy={makiPosition.y - 1} r="0.5" fill="black" />
          
          {/* Bras */}
          <Circle cx={makiPosition.x - 8} cy={makiPosition.y + 2} r="3" fill="#8D6E63" />
          <Circle cx={makiPosition.x + 8} cy={makiPosition.y + 2} r="3" fill="#8D6E63" />
          
          {/* Queue caractéristique */}
          <Path
            d={`M ${makiPosition.x + 10} ${makiPosition.y + 8} 
                Q ${makiPosition.x + 18} ${makiPosition.y - 2} 
                  ${makiPosition.x + 15} ${makiPosition.y + 12}
                Q ${makiPosition.x + 12} ${makiPosition.y + 15}
                  ${makiPosition.x + 8} ${makiPosition.y + 10}`}
            stroke="#8D6E63"
            strokeWidth="4"
            fill="none"
            strokeLinecap="round"
          />
          
          {/* Chapeau d'explorateur */}
          <Ellipse
            cx={makiPosition.x}
            cy={makiPosition.y - 12}
            rx="8"
            ry="3"
            fill="#D84315"
            stroke="#BF360C"
            strokeWidth="1"
          />
        </G>

        {/* Titre avec style amélioré */}
        <G>
          <SvgText
            x="225"
            y="35"
            fontSize="16"
            fill="white"
            textAnchor="middle"
            fontWeight="bold"
            stroke="#1565C0"
            strokeWidth="0.5"
          >
            🏝️ Mayotte - L'île aux parfums
          </SvgText>
        </G>
        
        {/* Boussole décorative */}
        <G>
          <Circle cx="50" cy="60" r="20" fill="#E3F2FD" stroke="#1565C0" strokeWidth="2" opacity="0.8" />
          <Path d="M 50 45 L 55 60 L 50 75 L 45 60 Z" fill="#F44336" />
          <Path d="M 35 60 L 50 55 L 65 60 L 50 65 Z" fill="#2196F3" />
          <SvgText x="50" y="90" fontSize="8" fill="#1565C0" textAnchor="middle" fontWeight="bold">N</SvgText>
        </G>
        
        {/* Légende améliorée */}
        <G>
          <SvgText x="20" y="380" fontSize="10" fill="#2C3E50" fontWeight="bold">
            Légende:
          </SvgText>
          <Circle cx="30" cy="395" r="4" fill="#28A745" />
          <SvgText x="40" y="398" fontSize="8" fill="#2C3E50">Débloqué</SvgText>
          
          <Circle cx="100" cy="395" r="4" fill="#FF6B35" />
          <SvgText x="110" y="398" fontSize="8" fill="#2C3E50">Actuel</SvgText>
          
          <Circle cx="160" cy="395" r="4" fill="#95A5A6" />
          <SvgText x="170" y="398" fontSize="8" fill="#2C3E50">Verrouillé</SvgText>
          
          <SvgText x="250" y="395" fontSize="8" fill="#00BCD4" fontWeight="bold">~ Lagon ~</SvgText>
          <SvgText x="320" y="395" fontSize="8" fill="#2E7D32" fontWeight="bold">⛰️ Reliefs</SvgText>
        </G>
      </Svg>
    </View>
  );
};

export default MayotteMap;