import React, { useState } from 'react';
import { View, PanResponder, Dimensions } from 'react-native';
import Svg, { Path, Circle, Text as SvgText, G, Defs, LinearGradient, Stop, RadialGradient, Polygon, Ellipse } from 'react-native-svg';
import Animated, { useSharedValue, useAnimatedStyle, useAnimatedGestureHandler, runOnJS } from 'react-native-reanimated';
import { PinchGestureHandler, PanGestureHandler, State } from 'react-native-gesture-handler';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

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
 * Composant carte SVG détaillée et réaliste de Mayotte avec zoom/pan
 * Basée sur la vraie forme géographique de l'île en hippocampe
 */
const MayotteMap: React.FC<MayotteMapProps> = ({
  width,
  height,
  onCommunePress,
  unlockedCommunes,
  currentCommune,
  makiPosition
}) => {
  // États pour le zoom et le pan
  const scale = useSharedValue(1);
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  const [lastScale, setLastScale] = useState(1);
  const [lastTranslateX, setLastTranslateX] = useState(0);
  const [lastTranslateY, setLastTranslateY] = useState(0);

  // Coordonnées précises des communes selon la vraie géographie
  const communes: CommuneData[] = [
    // Grande-Terre - Nord
    { id: 'mtsamboro', name: 'Mtsamboro', position: { x: 180, y: 120 }, isUnlocked: false, price: 3.99 },
    { id: 'acoua', name: 'Acoua', position: { x: 220, y: 110 }, isUnlocked: false, price: 3.99 },
    { id: 'mtsangamouji', name: 'Mtsangamouji', position: { x: 280, y: 130 }, isUnlocked: false, price: 2.99 },
    { id: 'koungou', name: 'Koungou', position: { x: 320, y: 150 }, isUnlocked: false },
    
    // Grande-Terre - Centre
    { id: 'bandraboua', name: 'Bandraboua', position: { x: 200, y: 160 }, isUnlocked: false, price: 2.99 },
    { id: 'dembeni', name: 'Dembéni', position: { x: 240, y: 180 }, isUnlocked: false },
    { id: 'tsoundzou', name: 'Tsoundzou', position: { x: 220, y: 200 }, isUnlocked: false },
    { id: 'tsingoni', name: 'Tsingoni', position: { x: 190, y: 210 }, isUnlocked: false, price: 2.99 },
    { id: 'mamoudzou', name: 'Mamoudzou', position: { x: 300, y: 210 }, isUnlocked: true }, // Capitale
    
    // Grande-Terre - Ouest 
    { id: 'sada', name: 'Sada', position: { x: 150, y: 240 }, isUnlocked: false, price: 1.99 },
    { id: 'ouangani', name: 'Ouangani', position: { x: 180, y: 280 }, isUnlocked: false },
    { id: 'chiconi', name: 'Chiconi', position: { x: 160, y: 320 }, isUnlocked: false, price: 2.99 },
    { id: 'boueni', name: 'Bouéni', position: { x: 140, y: 360 }, isUnlocked: false, price: 4.99 },
    
    // Grande-Terre - Sud
    { id: 'kani_keli', name: 'Kani-Kéli', position: { x: 190, y: 400 }, isUnlocked: false, price: 2.99 },
    { id: 'chirongui', name: 'Chirongui', position: { x: 230, y: 380 }, isUnlocked: false },
    { id: 'bandrele', name: 'Bandrélé', position: { x: 280, y: 350 }, isUnlocked: false, price: 2.99 },
    
    // Petite-Terre
    { id: 'dzaoudzi', name: 'Dzaoudzi', position: { x: 380, y: 320 }, isUnlocked: false, price: 4.99 },
    { id: 'pamandzi', name: 'Pamandzi', position: { x: 395, y: 335 }, isUnlocked: false, price: 4.99 },
  ];

  // Forme authentique de Mayotte basée sur la vraie géographie (hippocampe)
  const mayotteRealShape = `
    M 180 100
    C 190 95 210 90 240 95
    L 280 100
    C 310 105 330 115 340 130
    C 350 145 355 160 360 180
    L 365 200
    C 370 220 375 240 370 260
    C 365 280 355 295 340 305
    L 320 315
    C 300 325 285 335 280 350
    C 275 370 270 390 260 405
    C 250 420 235 425 220 420
    C 205 415 195 405 190 390
    C 185 375 180 360 175 345
    C 170 330 165 315 160 300
    C 155 280 150 260 155 240
    C 160 220 165 200 170 180
    C 175 160 180 140 185 120
    C 187 110 185 105 180 100
    Z
  `;

  // Forme de Petite-Terre (plus précise)
  const petiteTerreShape = `
    M 375 310
    C 385 305 400 308 410 315
    C 420 322 425 330 422 340
    C 419 350 410 355 395 352
    C 380 349 375 340 372 330
    C 370 320 372 315 375 310
    Z
  `;

  // Montagnes avec positions réelles
  const realMountains = [
    { x: 240, y: 180, name: 'Mt Benara', height: 660 }, // Point culminant - centre
    { x: 210, y: 350, name: 'Mt Choungui', height: 594 }, // Sud-ouest  
    { x: 280, y: 160, name: 'Mt Combani', height: 477 }, // Nord-est
    { x: 200, y: 200, name: 'Mt Mtsapéré', height: 572 }, // Centre-ouest
    { x: 190, y: 280, name: 'Pic Tricorne', height: 320 }, // Ouest
  ];

  // Baies caractéristiques avec formes réelles
  const realBays = [
    { path: 'M 130 230 Q 120 245 135 260 Q 150 250 130 230', name: 'Baie de Bouéni' },
    { path: 'M 290 200 Q 305 190 320 205 Q 310 220 290 200', name: 'Baie de Mamoudzou' },
    { path: 'M 220 370 Q 210 385 225 395 Q 240 385 220 370', name: 'Baie de Chirongui' },
    { path: 'M 350 140 Q 365 130 375 145 Q 365 160 350 140', name: 'Baie de Koungou' },
  ];

  // Gestionnaire de pincement pour le zoom
  const pinchGestureHandler = useAnimatedGestureHandler({
    onStart: (_, context: any) => {
      context.startScale = scale.value;
    },
    onActive: (event, context) => {
      const newScale = Math.min(Math.max(context.startScale * event.scale, 0.5), 4);
      scale.value = newScale;
    },
    onEnd: () => {
      runOnJS(setLastScale)(scale.value);
    },
  });

  // Gestionnaire de panoramique
  const panGestureHandler = useAnimatedGestureHandler({
    onStart: (_, context: any) => {
      context.startX = translateX.value;
      context.startY = translateY.value;
    },
    onActive: (event, context) => {
      const maxTranslate = 200 * scale.value;
      translateX.value = Math.min(Math.max(context.startX + event.translationX, -maxTranslate), maxTranslate);
      translateY.value = Math.min(Math.max(context.startY + event.translationY, -maxTranslate), maxTranslate);
    },
    onEnd: () => {
      runOnJS(setLastTranslateX)(translateX.value);
      runOnJS(setLastTranslateY)(translateY.value);
    },
  });

  // Style animé pour la transformation
  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [
        { translateX: translateX.value },
        { translateY: translateY.value },
        { scale: scale.value },
      ],
    };
  });

  const getCommuneStatus = (communeId: string) => {
    if (unlockedCommunes.includes(communeId) || communeId === 'mamoudzou') {
      return currentCommune === communeId ? 'current' : 'unlocked';
    }
    return 'locked';
  };

  const getCommuneColor = (status: string) => {
    switch (status) {
      case 'current': return '#FF6B35';
      case 'unlocked': return '#28A745';
      case 'locked': return '#95A5A6';
      default: return '#95A5A6';
    }
  };

  return (
    <View style={{ alignItems: 'center', backgroundColor: '#E3F2FD' }}>
      <PinchGestureHandler onGestureEvent={pinchGestureHandler}>
        <Animated.View>
          <PanGestureHandler onGestureEvent={panGestureHandler}>
            <Animated.View style={animatedStyle}>
              <Svg width={width} height={height} viewBox="0 0 500 480">
                <Defs>
                  {/* Dégradé océanique réaliste */}
                  <RadialGradient id="oceanGradient" cx="50%" cy="50%" r="85%">
                    <Stop offset="0%" stopColor="#1565C0" />
                    <Stop offset="30%" stopColor="#1976D2" />
                    <Stop offset="60%" stopColor="#1E88E5" />
                    <Stop offset="100%" stopColor="#42A5F5" />
                  </RadialGradient>
                  
                  {/* Dégradé lagon turquoise */}
                  <RadialGradient id="lagonGradient" cx="50%" cy="50%" r="70%">
                    <Stop offset="0%" stopColor="#4DD0E1" />
                    <Stop offset="40%" stopColor="#26C6DA" />
                    <Stop offset="80%" stopColor="#00BCD4" />
                    <Stop offset="100%" stopColor="#0097A7" />
                  </RadialGradient>
                  
                  {/* Dégradé Grande-Terre (végétation luxuriante) */}
                  <LinearGradient id="grandeTerreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <Stop offset="0%" stopColor="#C8E6C9" />
                    <Stop offset="25%" stopColor="#A5D6A7" />
                    <Stop offset="50%" stopColor="#81C784" />
                    <Stop offset="75%" stopColor="#66BB6A" />
                    <Stop offset="100%" stopColor="#4CAF50" />
                  </LinearGradient>
                  
                  {/* Ombres pour reliefs */}
                  <LinearGradient id="reliefShadow" x1="20%" y1="20%" x2="80%" y2="80%">
                    <Stop offset="0%" stopColor="#388E3C" />
                    <Stop offset="50%" stopColor="#2E7D32" />
                    <Stop offset="100%" stopColor="#1B5E20" />
                  </LinearGradient>
                  
                  {/* Dégradé Petite-Terre */}
                  <LinearGradient id="petiteTerreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <Stop offset="0%" stopColor="#DCEDC8" />
                    <Stop offset="50%" stopColor="#C5E1A5" />
                    <Stop offset="100%" stopColor="#AED581" />
                  </LinearGradient>
                </Defs>

                {/* Fond océan Indien */}
                <Circle cx="250" cy="240" r="230" fill="url(#oceanGradient)" />
                
                {/* Lagon protégé par le récif */}
                <Circle cx="250" cy="240" r="180" fill="url(#lagonGradient)" opacity="0.8" />

                {/* Baies caractéristiques */}
                {realBays.map((baie, index) => (
                  <Path
                    key={index}
                    d={baie.path}
                    fill="#1976D2"
                    opacity="0.6"
                  />
                ))}

                {/* Grande-Terre avec ombre réaliste */}
                <Path 
                  d={mayotteRealShape} 
                  fill="url(#reliefShadow)"
                  transform="translate(4, 4)"
                  opacity="0.4"
                />
                <Path 
                  d={mayotteRealShape} 
                  fill="url(#grandeTerreGradient)"
                  stroke="#2E7D32"
                  strokeWidth="2"
                />

                {/* Reliefs montagneux détaillés */}
                {realMountains.map((montagne, index) => (
                  <G key={index}>
                    {/* Ombre montagne */}
                    <Ellipse
                      cx={montagne.x + 3}
                      cy={montagne.y + 3}
                      rx="12"
                      ry="8"
                      fill="#1B5E20"
                      opacity="0.4"
                    />
                    {/* Montagne principale */}
                    <Polygon
                      points={`${montagne.x},${montagne.y - 15} ${montagne.x - 10},${montagne.y + 6} ${montagne.x + 10},${montagne.y + 6}`}
                      fill="#388E3C"
                      stroke="#2E7D32"
                      strokeWidth="1.5"
                    />
                    {/* Sommet */}
                    <Polygon
                      points={`${montagne.x},${montagne.y - 15} ${montagne.x - 5},${montagne.y - 5} ${montagne.x + 5},${montagne.y - 5}`}
                      fill="#E8F5E8"
                      opacity="0.9"
                    />
                    {/* Altitude */}
                    <SvgText
                      x={montagne.x}
                      y={montagne.y + 20}
                      fontSize="7"
                      fill="#2E7D32"
                      textAnchor="middle"
                      fontWeight="bold"
                    >
                      {montagne.height}m
                    </SvgText>
                  </G>
                ))}

                {/* Forêts denses et végétation */}
                <Circle cx="240" cy="180" r="18" fill="#2E7D32" opacity="0.7" />
                <Circle cx="200" cy="200" r="15" fill="#388E3C" opacity="0.6" />
                <Circle cx="280" cy="160" r="12" fill="#43A047" opacity="0.5" />
                <Circle cx="190" cy="280" r="10" fill="#4CAF50" opacity="0.6" />
                <Circle cx="220" cy="350" r="8" fill="#66BB6A" opacity="0.5" />

                {/* Petite-Terre avec ombre */}
                <Path 
                  d={petiteTerreShape}
                  fill="url(#reliefShadow)"
                  transform="translate(2, 2)"
                  opacity="0.3"
                />
                <Path 
                  d={petiteTerreShape}
                  fill="url(#petiteTerreGradient)"
                  stroke="#689F38"
                  strokeWidth="2"
                />

                {/* Aéroport Dzaoudzi-Pamandzi */}
                <G>
                  <Ellipse cx="390" cy="330" rx="12" ry="6" fill="#78909C" stroke="#546E7A" strokeWidth="1" />
                  <Path d="M 384 330 L 396 330 M 390 325 L 390 335" stroke="white" strokeWidth="1" />
                  <SvgText x="390" y="345" fontSize="6" fill="#37474F" textAnchor="middle" fontWeight="bold">✈️ Aéroport</SvgText>
                </G>

                {/* Routes principales */}
                <Path d="M 300 210 Q 260 190 220 200 Q 190 210 170 240" stroke="#8D6E63" strokeWidth="3" fill="none" opacity="0.7" />
                <Path d="M 300 210 Q 280 280 250 350 Q 230 380 200 400" stroke="#8D6E63" strokeWidth="3" fill="none" opacity="0.7" />
                <Path d="M 300 210 Q 330 180 360 160 Q 380 150 400 170" stroke="#8D6E63" strokeWidth="3" fill="none" opacity="0.7" />

                {/* Communes avec design amélioré */}
                {communes.map(commune => {
                  const status = getCommuneStatus(commune.id);
                  const color = getCommuneColor(status);
                  const isInteractive = status !== 'locked';
                  
                  return (
                    <G key={commune.id}>
                      {/* Halo pour commune active */}
                      {status === 'current' && (
                        <Circle
                          cx={commune.position.x}
                          cy={commune.position.y}
                          r="25"
                          fill={color}
                          opacity="0.15"
                        />
                      )}
                      
                      {/* Ombre du point */}
                      <Circle
                        cx={commune.position.x + 1}
                        cy={commune.position.y + 1}
                        r={status === 'current' ? 10 : 7}
                        fill="#000000"
                        opacity="0.3"
                      />
                      
                      {/* Point principal */}
                      <Circle
                        cx={commune.position.x}
                        cy={commune.position.y}
                        r={status === 'current' ? 10 : 7}
                        fill={color}
                        stroke="white"
                        strokeWidth="2"
                        opacity={status === 'locked' ? 0.8 : 1}
                        onPress={() => isInteractive && onCommunePress(commune)}
                      />
                      
                      {/* Icône verrouillage */}
                      {status === 'locked' && commune.price && (
                        <SvgText
                          x={commune.position.x}
                          y={commune.position.y + 2}
                          fontSize="6"
                          fill="white"
                          textAnchor="middle"
                          fontWeight="bold"
                        >
                          🔒
                        </SvgText>
                      )}
                      
                      {/* Nom commune avec meilleure lisibilité */}
                      <SvgText
                        x={commune.position.x}
                        y={commune.position.y - 15}
                        fontSize="8"
                        fill="white"
                        textAnchor="middle"
                        fontWeight="bold"
                        stroke="#2C3E50"
                        strokeWidth="0.3"
                      >
                        {commune.name}
                      </SvgText>
                      
                      {/* Prix */}
                      {commune.price && status === 'locked' && (
                        <SvgText
                          x={commune.position.x}
                          y={commune.position.y + 20}
                          fontSize="6"
                          fill="#E91E63"
                          textAnchor="middle"
                          fontWeight="bold"
                          stroke="white"
                          strokeWidth="0.2"
                        >
                          €{commune.price}
                        </SvgText>
                      )}
                    </G>
                  );
                })}

                {/* Maki aventurier amélioré */}
                <G>
                  <Ellipse
                    cx={makiPosition.x + 2}
                    cy={makiPosition.y + 20}
                    rx="15"
                    ry="5"
                    fill="#000000"
                    opacity="0.3"
                  />
                  
                  <Ellipse cx={makiPosition.x} cy={makiPosition.y + 8} rx="10" ry="14" fill="#8D6E63" stroke="#5D4037" strokeWidth="1" />
                  <Circle cx={makiPosition.x} cy={makiPosition.y - 3} r="8" fill="#A1887F" stroke="#6D4C41" strokeWidth="1" />
                  
                  <Circle cx={makiPosition.x - 6} cy={makiPosition.y - 8} r="3" fill="#8D6E63" />
                  <Circle cx={makiPosition.x + 6} cy={makiPosition.y - 8} r="3" fill="#8D6E63" />
                  
                  <Circle cx={makiPosition.x - 2} cy={makiPosition.y - 5} r="1.5" fill="white" />
                  <Circle cx={makiPosition.x + 2} cy={makiPosition.y - 5} r="1.5" fill="white" />
                  <Circle cx={makiPosition.x - 2} cy={makiPosition.y - 5} r="0.8" fill="black" />
                  <Circle cx={makiPosition.x + 2} cy={makiPosition.y - 5} r="0.8" fill="black" />
                  
                  <Ellipse cx={makiPosition.x} cy={makiPosition.y - 1} rx="2" ry="1.5" fill="#BCAAA4" />
                  <Circle cx={makiPosition.x} cy={makiPosition.y} r="0.3" fill="black" />
                  
                  <Circle cx={makiPosition.x - 7} cy={makiPosition.y + 3} r="2.5" fill="#8D6E63" />
                  <Circle cx={makiPosition.x + 7} cy={makiPosition.y + 3} r="2.5" fill="#8D6E63" />
                  
                  <Path
                    d={`M ${makiPosition.x + 8} ${makiPosition.y + 10} 
                        Q ${makiPosition.x + 16} ${makiPosition.y + 2} 
                          ${makiPosition.x + 13} ${makiPosition.y + 15}
                        Q ${makiPosition.x + 10} ${makiPosition.y + 18}
                          ${makiPosition.x + 6} ${makiPosition.y + 12}`}
                    stroke="#8D6E63"
                    strokeWidth="3"
                    fill="none"
                    strokeLinecap="round"
                  />
                  
                  <Ellipse cx={makiPosition.x} cy={makiPosition.y - 10} rx="6" ry="2.5" fill="#D84315" stroke="#BF360C" strokeWidth="1" />
                </G>

                {/* Titre */}
                <SvgText x="250" y="30" fontSize="14" fill="white" textAnchor="middle" fontWeight="bold" stroke="#1565C0" strokeWidth="0.4">
                  🏝️ Mayotte - L'île aux parfums
                </SvgText>

                {/* Instructions zoom */}
                <SvgText x="250" y="460" fontSize="9" fill="#37474F" textAnchor="middle" fontWeight="bold">
                  📱 Pincez pour zoomer • Glissez pour explorer
                </SvgText>

                {/* Légende compacte */}
                <G>
                  <Circle cx="40" cy="440" r="4" fill="#28A745" />
                  <SvgText x="50" y="443" fontSize="7" fill="#2C3E50">Libre</SvgText>
                  
                  <Circle cx="100" cy="440" r="4" fill="#FF6B35" />
                  <SvgText x="110" y="443" fontSize="7" fill="#2C3E50">Actuel</SvgText>
                  
                  <Circle cx="160" cy="440" r="4" fill="#95A5A6" />
                  <SvgText x="170" y="443" fontSize="7" fill="#2C3E50">🔒 Premium</SvgText>
                </G>
              </Svg>
            </Animated.View>
          </PanGestureHandler>
        </Animated.View>
      </PinchGestureHandler>
    </View>
  );
};

export default MayotteMap;