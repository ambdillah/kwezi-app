# STRUCTURE DE LA BASE DE DONNÉES KWEZI

## Vue d'ensemble

La base de données utilise **MongoDB**, une base NoSQL qui stocke les données sous forme de documents JSON (pas de colonnes/lignes comme Excel).

## Structure actuelle d'un mot

Voici la structure complète d'un mot dans la base :

```json
{
  "french": "Ventiler",
  "shimaore": "oupépeya",
  "kibouchi": "micoupoucoupoukou",
  "category": "verbes",
  "emoji": "🌬️",
  "audio_filename_shimaore": "Oupépéya.m4a",
  "audio_filename_kibouchi": "Micoupoucoupoukou.m4a",
  "has_authentic_audio": true,
  "dual_audio_system": true
}
```

## Pourquoi c'était compliqué d'ajouter les verbes ?

### Problèmes rencontrés :

1. **Nommage des champs incohérent** :
   - Anciens mots : `audio_filename` (un seul fichier)
   - Nouveaux mots : `audio_filename_shimaore` + `audio_filename_kibouchi` (système dual)
   
2. **Flag système dual manquant** :
   - Le frontend cherchait un champ `dual_audio_system: true`
   - Les nouveaux verbes ne l'avaient pas → utilisation de synthèse vocale au lieu d'audio authentique

3. **Tri alphabétique absent** :
   - L'API backend ne triait pas les résultats
   - Les nouveaux verbes apparaissaient toujours à la fin

4. **Fichiers audio à copier manuellement** :
   - Les fichiers M4A devaient être extraits du ZIP
   - Copiés dans `/app/frontend/assets/audio/`
   - Liés manuellement dans la base de données

## Solutions appliquées

### 1. Tri alphabétique automatique ✅
L'API backend trie maintenant tous les mots par ordre alphabétique :
```python
cursor = words_collection.find(query).sort("french", 1)
```

### 2. Flag dual_audio_system ajouté ✅
Tous les verbes ont maintenant :
```python
{
  "dual_audio_system": True,
  "has_authentic_audio": True
}
```

### 3. Structure de données unifiée ✅
Tous les nouveaux mots suivent cette structure :
- `french`: Le mot en français
- `shimaore`: Traduction shimaoré
- `kibouchi`: Traduction kibouchi  
- `category`: Catégorie (verbes, animaux, etc.)
- `emoji`: Emoji représentatif
- `audio_filename_shimaore`: Nom du fichier audio shimaoré
- `audio_filename_kibouchi`: Nom du fichier audio kibouchi
- `dual_audio_system`: true
- `has_authentic_audio`: true

## Processus simplifié pour ajouter de nouveaux mots

### Étape 1 : Préparer les données
Créer un fichier CSV ou une image avec :
- Mot français | Shimaoré | Kibouchi

### Étape 2 : Préparer les audios
- Nommer les fichiers exactement comme les traductions
- Exemple : "oupépeya" → "Oupépéya.m4a"

### Étape 3 : Créer un script Python simple
```python
nouveaux_mots = [
    {
        "french": "Mot français",
        "shimaore": "traduction shimaoré",
        "kibouchi": "traduction kibouchi",
        "category": "verbes",
        "emoji": "🌬️",
        "audio_filename_shimaore": "Fichier.m4a",
        "audio_filename_kibouchi": "Fichier2.m4a",
        "has_authentic_audio": True,
        "dual_audio_system": True
    }
]

# Copier les fichiers audio
for audio in ["Fichier.m4a", "Fichier2.m4a"]:
    shutil.copy(f"/source/{audio}", f"/app/frontend/assets/audio/{audio}")

# Insérer dans MongoDB
for mot in nouveaux_mots:
    words_collection.insert_one(mot)
```

### Étape 4 : Vérification automatique
- L'API trie automatiquement par ordre alphabétique
- Le frontend détecte automatiquement les audios authentiques
- Pas besoin de redémarrage manuel

## Avantages de la nouvelle structure

✅ **Tri automatique** : Plus besoin de se soucier de l'ordre d'insertion
✅ **Détection audio automatique** : Le système sait quels mots ont des audios
✅ **Système dual** : Support complet de 2 audios par mot (shimaoré + kibouchi)
✅ **Extensible** : Facile d'ajouter de nouvelles catégories
✅ **Performance** : Index MongoDB pour recherches rapides

## État actuel

- **574 mots** au total
- **110 verbes** (100% avec audios authentiques)
- **16 catégories** différentes
- **Tri alphabétique** activé sur toutes les catégories
