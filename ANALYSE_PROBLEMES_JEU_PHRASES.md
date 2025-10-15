# 🔍 Analyse des problèmes du jeu "Construire des phrases"

**Date:** 15 octobre 2025  
**Problèmes identifiés:** 2

---

## 🎨 PROBLÈME 1 : Coloration incomplète des préfixes de verbes

### Problème identifié
La règle de coloration des préfixes selon les temps n'est pas toujours appliquée sur tous les verbes.

### Cause racine
Les listes de préfixes dans `/app/frontend/utils/conjugationColorSystem.ts` sont **incomplètes**.

#### Préfixes actuellement reconnus (Shimaoré):
```typescript
SHIMAORE_PREFIXES = {
  present: ['nis', 'ous', 'as', 'ris', 'mous', 'was'],
  past: ['naco', 'waco', 'aco', 'raco', 'mwaco'],
  future: ['nitso', 'outso', 'atso', 'ritso', 'moutso', 'watso']
}
```

#### Préfixes actuellement reconnus (Kibouchi):
```typescript
KIBOUCHI_PREFIXES = {
  present: ['za', 'ana', 'izi', 'zéheyi', 'anaréou', 'réou'],
  past: ['ni'],
  future: ['bou']
}
```

### Préfixes manquants détectés
D'après l'analyse de la base de données, plusieurs préfixes utilisés dans les phrases ne sont pas reconnus :

**Shimaoré :**
- Présent : `wawé`, `wayé` (variantes de `wa-`)
- Passé : `moicomengna` (peut-être `moi-`)

**À noter :** Les verbes avec ces préfixes non reconnus ne seront pas colorés et l'indicateur de temps ne s'affichera pas.

### Solution recommandée
1. Analyser toutes les 270 phrases de la base de données
2. Extraire tous les préfixes uniques utilisés
3. Mettre à jour les listes `SHIMAORE_PREFIXES` et `KIBOUCHI_PREFIXES`
4. Tenir compte des variations phonétiques (ex: `wa-`, `wawé`, `wayé`)

---

## 🔄 PROBLÈME 2 : Pas de proposition automatique de nouvelle session

### Problème identifié
Lorsque la session se termine (toutes les phrases complétées), une alerte s'affiche mais :
- Elle propose "Recommencer" OU "Retour"
- L'utilisateur doit manuellement choisir
- Pas de démarrage automatique d'une nouvelle session

### Code actuel (ligne 1062-1066 de games.tsx)
```typescript
} else {
  Alert.alert('Félicitations! 🎊', `Jeu terminé! Score final: ${sentenceScore + 10}`, [
    { text: 'Recommencer', onPress: () => startGame('build-sentence') },
    { text: 'Retour', onPress: () => { setGameStarted(false); setCurrentGame(null); } }
  ]);
}
```

### Solution recommandée
Ajouter un démarrage automatique après quelques secondes + possibilité d'annuler :

```typescript
} else {
  // Fin de session
  setSentenceScore(sentenceScore + 10);
  const finalScore = sentenceScore + 10;
  
  Alert.alert(
    'Félicitations! 🎊', 
    `Session terminée! Score final: ${finalScore}\n\nUne nouvelle session va démarrer dans 3 secondes...`,
    [
      { 
        text: 'Retour au menu', 
        onPress: () => { 
          setGameStarted(false); 
          setCurrentGame(null); 
        },
        style: 'cancel'
      },
      { 
        text: 'Nouvelle session maintenant', 
        onPress: () => startGame('build-sentence')
      }
    ]
  );
  
  // Démarrage automatique après 3 secondes
  const autoRestartTimeout = setTimeout(() => {
    startGame('build-sentence');
  }, 3000);
  
  // Possibilité d'annuler le démarrage automatique si l'utilisateur choisit "Retour"
  // Note: Il faudrait stocker ce timeout dans un état pour pouvoir le clear
}
```

---

## 📋 PLAN DE CORRECTION

### Étape 1 : Analyse complète des préfixes
1. ✅ Script Python pour analyser toutes les phrases
2. ⏳ Extraire tous les préfixes uniques
3. ⏳ Classifier par temps (présent, passé, futur)
4. ⏳ Mettre à jour `conjugationColorSystem.ts`

### Étape 2 : Amélioration de la fin de session
1. ⏳ Modifier la fonction `nextSentence()` dans `games.tsx`
2. ⏳ Ajouter un état pour le timeout de redémarrage automatique
3. ⏳ Implémenter le démarrage automatique avec compte à rebours
4. ⏳ Tester le flux complet

### Étape 3 : Tests
1. ⏳ Tester la coloration sur toutes les phrases
2. ⏳ Vérifier que tous les verbes sont correctement colorés
3. ⏳ Tester le redémarrage automatique de session
4. ⏳ Vérifier la possibilité d'annuler

---

## 🎯 IMPACT ATTENDU

### Problème 1 - Coloration complète
- ✅ Tous les verbes auront leurs préfixes colorés
- ✅ L'indicateur de temps s'affichera pour tous les verbes
- ✅ Meilleure expérience pédagogique

### Problème 2 - Redémarrage automatique
- ✅ L'utilisateur peut enchaîner les sessions sans interruption
- ✅ Possibilité de quitter si souhaité
- ✅ Meilleure rétention et engagement

---

**Prochaine étape:** Implémenter les corrections
