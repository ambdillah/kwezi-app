# 📚 RÈGLES DE CONJUGAISON EN KIBOUCHI
## Résumé complet des règles implémentées dans l'application Kwezi

**Date:** 15 octobre 2025  
**Langue:** Kibouchi (langue de Mayotte)  
**Système:** 3 temps (Présent, Passé, Futur)

---

## 👥 PRONOMS PERSONNELS

| Français | Kibouchi |
|----------|----------|
| je | **zahou** |
| tu | **anaou** |
| il/elle | **izi** |
| nous | **zéhèyi** |
| vous | **anaréou** |
| ils/elles | **réou** |

---

## 🎯 RÈGLE GÉNÉRALE DE CONJUGAISON

Les verbes en kibouchi à l'infinitif commencent généralement par **"mi-"** ou **"m-"**.

### Exemple : **mihinagna** (manger)

---

## ⏰ CONJUGAISON PAR TEMPS

### 1️⃣ PRÉSENT : Garder le verbe à l'infinitif

**Règle :** Au présent, le verbe reste **à l'infinitif** (on garde le "m")

**Exemple avec "mihinagna" (manger) :**
- ✅ **mihinagna** (on garde tel quel)

**Conjugaison complète :**
```
zahou mihinagna       (je mange)
anaou mihinagna       (tu manges)
izi mihinagna         (il/elle mange)
zéhèyi mihinagna      (nous mangeons)
anaréou mihinagna     (vous mangez)
réou mihinagna        (ils/elles mangent)
```

**Autres exemples :**
- **misoma** (jouer) → **misoma** (reste identique)
- **milawa** (pêcher) → **milawa** (reste identique)
- **mihondragna** (voyager) → **mihondragna** (reste identique)

---

### 2️⃣ PASSÉ : Remplacer "m" par "n"

**Règle :** Remplacer le **"m"** du début par **"n"**

**Exemple avec "mihinagna" (manger) :**
- ❌ **m**ihinagna → ✅ **n**ihinagna

**Conjugaison complète :**
```
zahou nihinagna      (j'ai mangé)
anaou nihinagna      (tu as mangé)
izi nihinagna        (il/elle a mangé)
zéhèyi nihinagna     (nous avons mangé)
anaréou nihinagna    (vous avez mangé)
réou nihinagna       (ils/elles ont mangé)
```

**Autres exemples :**
- **misoma** → **nisoma** (j'ai joué)
- **milawa** → **nilawa** (j'ai pêché)
- **mihondragna** → **nihondragna** (j'ai voyagé)

**Variantes de préfixes du passé identifiées :**
- **ni-** (forme standard)
- **nan-** (variante pour certains verbes : "tu as...")
- **nam-** (variante pour certains verbes : "il/elle a...")

**Exemples avec variantes :**
```
zahou nihinagna      (j'ai mangé)
anaou nanhinagna     (tu as mangé) - variante
izi namhinagna       (il/elle a mangé) - variante
```

---

### 3️⃣ FUTUR : Remplacer "m" par "Mbou"

**Règle :** Remplacer le **"m"** du début par **"Mbou"**

**Exemple avec "mihinagna" (manger) :**
- ❌ **m**ihinagna → ✅ **Mbou**ihinagna

**Conjugaison complète :**
```
zahou Mbouihinagna     (je mangerai)
anaou Mbouihinagna     (tu mangeras)
izi Mbouihinagna       (il/elle mangera)
zéhèyi Mbouihinagna    (nous mangerons)
anaréou Mbouihinagna   (vous mangerez)
réou Mbouihinagna      (ils/elles mangeront)
```

**Autres exemples :**
- **misoma** → **Mbouisoma** (je jouerai)
- **milawa** → **Mbouilawa** (je pêcherai)
- **mihondragna** → **Mbouihondragna** (je voyagerai)

**Variantes de préfixes du futur :**
- **bou-** (forme abrégée, rarement utilisée)
- **Mbou-** (forme standard, capitalisée)
- **mbou-** (forme standard, minuscule)

---

## 🎨 PRÉFIXES IDENTIFIÉS DANS L'APPLICATION

### Préfixes PRÉSENT
```typescript
['za', 'ana', 'izi', 'zéheyi', 'anaréou', 'réou', 'zéhèyi', 'and', 'an', 'it', 'am', 'i']
```

**Explication des préfixes :**
- **za, ana, izi, zéhèyi, anaréou, réou** : Pronoms sujets (peuvent être confondus avec des préfixes)
- **and-, an-, it-, am-, i-** : Verbes conjugués au présent après suppression du "m"

### Préfixes PASSÉ
```typescript
['ni', 'nan', 'nam']
```

**Explication :**
- **ni-** : Forme standard (zahou **ni**hinagna)
- **nan-** : Variante "tu as..." (anaou **nan**hinagna)
- **nam-** : Variante "il/elle a..." (izi **nam**hinagna)

### Préfixes FUTUR
```typescript
['bou', 'mbou']
```

**Explication :**
- **mbou-** : Forme standard capitalisée (zahou **Mbou**ihinagna)
- **bou-** : Forme abrégée

---

## 📊 TABLEAU RÉCAPITULATIF

| Temps | Règle | Exemple (mihinagna) | Préfixes |
|-------|-------|---------------------|----------|
| **PRÉSENT** | Supprimer "m" | ihinagna | i-, and-, an-, it-, am- |
| **PASSÉ** | Remplacer "m" par "n" | nihinagna | ni-, nan-, nam- |
| **FUTUR** | Remplacer "m" par "Mbou" | Mbouihinagna | mbou-, bou- |

---

## 🎮 IMPLÉMENTATION DANS LE JEU

### Coloration automatique des préfixes

Dans le jeu "Construire des phrases", les préfixes de conjugaison sont colorés selon le temps :

- 🟢 **Vert** : Présent (action actuelle)
- 🟠 **Orange** : Passé (action passée)
- 🔵 **Bleu** : Futur (action future)

**Exemples visuels :**
```
zahou [i]hinagna         → [i] coloré en VERT (présent)
zahou [ni]hinagna        → [ni] coloré en ORANGE (passé)
zahou [Mbou]ihinagna     → [Mbou] coloré en BLEU (futur)
```

### Indicateur de temps

Un badge coloré s'affiche sous chaque verbe conjugué pour indiquer le temps :
- ✅ **PRÉSENT** (badge vert)
- ✅ **PASSÉ** (badge orange)
- ✅ **FUTUR** (badge bleu)

---

## 🔍 CAS PARTICULIERS

### Verbes sans "m" initial

Certains verbes kibouchi ne commencent pas par "m". Dans ce cas, les règles peuvent varier.

**Exemples identifiés dans la base de données :**
- **androubaka** (casser/abîmer) au présent
- **nandigni** (entrer) au passé
- **Mbouandeha** (aller) au futur

### Pronoms qui ressemblent à des préfixes

⚠️ **Attention** : Ne pas confondre les pronoms avec les préfixes de verbes !

**Pronoms seuls (NON colorés) :**
- **za** tout seul = "je" (pronom)
- **ana** tout seul = "tu" (pronom)

**Verbes conjugués (colorés) :**
- **za** + verbe = **za**mihinagna (incorrect - doit être **i**hinagna)
- **and**roubaka = verbe "casser" au présent (préfixe **and-** coloré)

---

## 📝 EXEMPLES COMPLETS DE CONJUGAISON

### Verbe : **mihinagna** (manger)

#### PRÉSENT
```
zahou ihinagna        (je mange)
anaou ihinagna        (tu manges)  
izi ihinagna          (il/elle mange)
zéhèyi ihinagna       (nous mangeons)
anaréou ihinagna      (vous mangez)
réou ihinagna         (ils/elles mangent)
```

#### PASSÉ
```
zahou nihinagna       (j'ai mangé)
anaou nanhinagna      (tu as mangé)
izi namhinagna        (il/elle a mangé)
zéhèyi nihinagna      (nous avons mangé)
anaréou nihinagna     (vous avez mangé)
réou nihinagna        (ils/elles ont mangé)
```

#### FUTUR
```
zahou Mbouihinagna    (je mangerai)
anaou Mbouihinagna    (tu mangeras)
izi Mbouihinagna      (il/elle mangera)
zéhèyi Mbouihinagna   (nous mangerons)
anaréou Mbouihinagna  (vous mangerez)
réou Mbouihinagna     (ils/elles mangeront)
```

---

## 📚 SOURCES

**Fichiers de référence dans l'application :**
1. `/app/frontend/components/ConjugationRules.tsx` - Affichage des règles
2. `/app/frontend/utils/conjugationColorSystem.ts` - Système de coloration
3. `/app/backend/conjugation_engine.py` - Moteur de conjugaison
4. `/app/REGLES_CONJUGAISON_JEU.md` - Documentation complète

**Base de données :**
- Collection `sentences` : 270 phrases conjuguées en shimaoré, kibouchi et français
- 90 phrases au présent + 90 au passé + 90 au futur

---

## ✅ RÉSUMÉ SIMPLE

**Pour conjuguer un verbe kibouchi, retiens ces 3 règles :**

1. **PRÉSENT** → Enlève le "m" : **m**ihinagna → **i**hinagna
2. **PASSÉ** → Change "m" en "n" : **m**ihinagna → **n**ihinagna  
3. **FUTUR** → Change "m" en "Mbou" : **m**ihinagna → **Mbou**ihinagna

**Et ajoute le pronom sujet devant !**

🎯 **Simple et efficace !**
