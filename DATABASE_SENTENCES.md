# 📚 BASE DE DONNÉES - Collection "sentences"

## 📊 Vue d'ensemble

La collection `sentences` contient **270 phrases conjuguées** dans les 3 langues (Français, Shimaoré, Kibouchi) pour le jeu "Construire des phrases".

---

## 🗂️ Structure d'un document

```json
{
  "id": "9f9ee450-...",
  "type": "conjugated_corrected",
  "french": "j'abîme",
  "shimaore": "wami nismengna",
  "kibouchi": "zahou androubaka",
  "tense": "present",
  "subject": "je",
  "verb_infinitive_fr": "Abîmer",
  "difficulty": 1,
  "french_words": ["j'abîme"],
  "shimaore_words": ["wami", "nismengna"],
  "kibouchi_words": ["zahou", "androubaka"]
}
```

### Champs

- **id** : Identifiant unique (UUID)
- **type** : Type de phrase (`conjugated_corrected`)
- **french** : Phrase conjuguée en français
- **shimaore** : Traduction conjuguée en Shimaoré
- **kibouchi** : Traduction conjuguée en Kibouchi
- **tense** : Temps de conjugaison (`present`, `past`, `future`)
- **subject** : Pronom sujet (`je`, `tu`, `il`, `nous`, `vous`, `ils`)
- **verb_infinitive_fr** : Verbe à l'infinitif en français
- **difficulty** : Niveau de difficulté (1=présent, 2=passé, 3=futur)
- **french_words** : Phrase française découpée en mots (array)
- **shimaore_words** : Phrase Shimaoré découpée en mots (array)
- **kibouchi_words** : Phrase Kibouchi découpée en mots (array)

---

## 📈 Statistiques

### Total
- **270 phrases** au total

### Répartition par temps
- **Présent** : 90 phrases (difficulté 1)
- **Passé** : 90 phrases (difficulté 2)
- **Futur** : 90 phrases (difficulté 3)

### Répartition par pronom
- **je** : 45 phrases (15 par temps)
- **tu** : 45 phrases (15 par temps)
- **il** : 45 phrases (15 par temps)
- **nous** : 45 phrases (15 par temps)
- **vous** : 45 phrases (15 par temps)
- **ils** : 45 phrases (15 par temps)

### Verbes couverts
15 verbes conjugués dans tous les temps et pronoms :
- Abîmer, Acheter, Aider, Aller, Allumer
- Boire, Bouger, Changer, Combler, Commencer
- Comprendre, Connaître, Courir, Danser, Demander

---

## 🎯 Règles de conjugaison appliquées

### FRANÇAIS
- Conjugaisons complètes et correctes pour tous les temps
- Auxiliaires corrects (avoir/être) au passé composé
- Élision pour "je" avec voyelles ("j'abîme", "j'ai bu")

### SHIMAORÉ
**Règle générale** : Supprimer "ou" ou "w" de l'infinitif + ajouter préfixe

**Pronoms** : wami (je), wawé (tu), wayé (il/elle), wasi (nous), wagnou (vous), wawo (ils/elles)

**Préfixes par temps** :
- **Présent** : nis, ous, as, ris, mous, was
- **Passé** : naco, waco, aco, raco, moico, waco
- **Futur** : nitso, outso, atso, ritso, moutso, watso

**Exemple** : "ourenga" (parler)
- Présent : wami **nis**renga (je parle)
- Passé : wami **naco**renga (j'ai parlé)
- Futur : wami **nitso**renga (je parlerai)

### KIBOUCHI
**Règle générale** : Modifier le préfixe "m" selon le temps

**Pronoms** : zahou (je), anaou (tu), izi (il/elle), zéhèyi (nous), anaréou (vous), réou (ils/elles)

**Transformations** :
- **Présent** : Supprimer le "m"
- **Passé** : Remplacer "m" par "n"
- **Futur** : Remplacer "m" par "Mbou"

**Exemple** : "mihinagna" (manger)
- Présent : zahou **ihinagna** (je mange)
- Passé : zahou **nihinagna** (j'ai mangé)
- Futur : zahou **Mbouihinagna** (je mangerai)

---

## 🔧 API Endpoint

### GET /api/sentences

**Paramètres** :
- `difficulty` (optionnel) : Filtrer par difficulté (1, 2, ou 3)
- `tense` (optionnel) : Filtrer par temps (present, past, future)
- `limit` (optionnel, défaut=20) : Nombre de phrases à retourner

**Comportement par défaut** :
Si aucun paramètre n'est fourni, l'API retourne un **mélange équilibré** de tous les temps (présent, passé, futur).

**Exemples** :
```bash
# Mélange de tous les temps (recommandé)
GET /api/sentences?limit=10

# Uniquement le présent
GET /api/sentences?tense=present&limit=5

# Uniquement difficulté 2 (passé)
GET /api/sentences?difficulty=2&limit=10
```

---

## 🎮 Utilisation dans le jeu

Le jeu "Construire des phrases" :
1. Charge 10 phrases mélangées (tous temps confondus)
2. Affiche la phrase française
3. Demande au joueur de reconstituer la phrase en Shimaoré ou Kibouchi
4. Vérifie la réponse et prononce avec voix féminine
5. Passe à la phrase suivante

**Avantages** :
- ✅ Variété des temps pour apprentissage complet
- ✅ Mélange aléatoire pour éviter la monotonie
- ✅ Conjugaisons authentiques et correctes
- ✅ Couverture équilibrée de tous les pronoms

---

## 🔄 Mise à jour de la base

Pour régénérer toutes les phrases avec de nouvelles règles :

```bash
cd /app/backend
python3 regenerate_sentences_corrected.py
```

Ce script :
1. Supprime toutes les anciennes phrases
2. Génère 270 nouvelles phrases (15 verbes × 6 pronoms × 3 temps)
3. Applique les règles de conjugaison correctes
4. Insère dans la collection `sentences`
