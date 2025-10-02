# 📚 Règles de Conjugaison - Jeu "Construire des Phrases"

## 🎯 Vue d'ensemble

Le jeu "Construire des phrases" utilise des phrases générées automatiquement avec un moteur de conjugaison pour **3 langues** : Français, Shimaoré et Kibouchi.

Les phrases sont stockées dans la base de données MongoDB (collection `sentences`).

---

## 🔧 Moteur de Conjugaison - 3 Langues

### Temps Implémentés

Le moteur de conjugaison supporte **3 temps** :

1. **Présent** (present)
2. **Passé** (past)
3. **Futur** (future)

---

## 📋 Règles de Conjugaison - PRÉSENT

### Pronoms Personnels Supportés
- je
- tu
- il/elle
- nous
- vous
- ils/elles

### Verbes Conjugués au Présent

**Verbes du 1er groupe (-er) :**
- parler : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent
- manger : je mange, tu manges, il mange, nous mangeons, vous mangez, ils mangent
- jouer : je joue, tu joues, il joue, nous jouons, vous jouez, ils jouent
- marcher : je marche, tu marches, il marche, nous marchons, vous marchez, ils marchent
- donner : je donne, tu donnes, il donne, nous donnons, vous donnez, ils donnent
- regarder : je regarde, tu regardes, il regarde, nous regardons, vous regardez, ils regardent
- écouter : j'écoute, tu écoutes, il écoute, nous écoutons, vous écoutez, ils écoutent
- chanter : je chante, tu chantes, il chante, nous chantons, vous chantez, ils chantent
- danser : je danse, tu danses, il danse, nous dansons, vous dansez, ils dansent
- travailler : je travaille, tu travailles, il travaille, nous travaillons, vous travaillez, ils travaillent
- aimer : j'aime, tu aimes, il aime, nous aimons, vous aimez, ils aiment
- détester : je déteste, tu détestes, il déteste, nous détestons, vous détestez, ils détestent
- acheter : j'achète, tu achètes, il achète, nous achetons, vous achetez, ils achètent
- fermer : je ferme, tu fermes, il ferme, nous fermons, vous fermez, ils ferment
- commencer : je commence, tu commences, il commence, nous commençons, vous commencez, ils commencent

**Verbes du 2ème groupe (-ir) :**
- dormir : je dors, tu dors, il dort, nous dormons, vous dormez, ils dorment
- courir : je cours, tu cours, il court, nous courons, vous courez, ils courent
- ouvrir : j'ouvre, tu ouvres, il ouvre, nous ouvrons, vous ouvrez, ils ouvrent

**Verbes du 3ème groupe (irréguliers) :**
- boire : je bois, tu bois, il boit, nous buvons, vous buvez, ils boivent
- voir : je vois, tu vois, il voit, nous voyons, vous voyez, ils voient
- lire : je lis, tu lis, il lit, nous lisons, vous lisez, ils lisent
- écrire : j'écris, tu écris, il écrit, nous écrivons, vous écrivez, ils écrivent
- vendre : je vends, tu vends, il vend, nous vendons, vous vendez, ils vendent
- prendre : je prends, tu prends, il prend, nous prenons, vous prenez, ils prennent

**Auxiliaires et verbes très irréguliers :**
- avoir : j'ai, tu as, il a, nous avons, vous avez, ils ont
- être : je suis, tu es, il est, nous sommes, vous êtes, ils sont
- faire : je fais, tu fais, il fait, nous faisons, vous faites, ils font
- aller : je vais, tu vas, il va, nous allons, vous allez, ils vont
- venir : je viens, tu viens, il vient, nous venons, vous venez, ils viennent

---

## 📋 Règles de Conjugaison - PASSÉ COMPOSÉ

### Structure
**Auxiliaire (avoir/être) au présent + Participe passé**

### Verbes avec AVOIR

**Verbes du 1er groupe (-er) → Participe passé en -é :**
- parler → j'ai parlé, tu as parlé, il a parlé, nous avons parlé, vous avez parlé, ils ont parlé
- manger → j'ai mangé, tu as mangé, il a mangé, nous avons mangé, vous avez mangé, ils ont mangé
- jouer → j'ai joué
- regarder → j'ai regardé
- écouter → j'ai écouté
- chanter → j'ai chanté
- danser → j'ai dansé
- travailler → j'ai travaillé
- aimer → j'ai aimé
- acheter → j'ai acheté
- fermer → j'ai fermé

**Verbes du 2ème et 3ème groupe :**
- dormir → j'ai dormi, tu as dormi, il a dormi
- courir → j'ai couru
- boire → j'ai bu
- voir → j'ai vu
- lire → j'ai lu
- écrire → j'ai écrit
- prendre → j'ai pris
- faire → j'ai fait
- avoir → j'ai eu

### Verbes avec ÊTRE

**14 verbes de mouvement (+ verbes pronominaux) :**
- aller → je suis allé(e), tu es allé(e), il/elle est allé(e), nous sommes allé(e)s, vous êtes allé(e)(s), ils/elles sont allé(e)s
- venir → je suis venu(e), tu es venu(e), il/elle est venu(e)
- arriver → je suis arrivé(e)
- partir → je suis parti(e)
- entrer → je suis entré(e)
- sortir → je suis sorti(e)
- monter → je suis monté(e)
- descendre → je suis descendu(e)
- rester → je suis resté(e)
- tomber → je suis tombé(e)
- naître → je suis né(e)
- mourir → il/elle est mort(e)
- devenir → je suis devenu(e)
- retourner → je suis retourné(e)

**Note importante :** Accord du participe passé avec le sujet pour les verbes avec ÊTRE

---

## ⚠️ Particularités Orthographiques

### Élision
- je + voyelle → j' (j'ai, j'aime, j'achète, j'écoute, j'écris, j'ouvre)

### Changement de radical
- acheter : j'achète, tu achètes, il achète (mais nous achetons, vous achetez)
- manger : nous mangeons (ajout du 'e' devant 'o')
- commencer : nous commençons (cédille devant 'o')

### Participes passés irréguliers
- avoir → eu
- être → été
- faire → fait
- voir → vu
- boire → bu
- lire → lu
- écrire → écrit
- prendre → pris
- venir → venu
- aller → allé

---

## 🎮 Implémentation dans le Jeu

### Structure d'une Phrase en Base de Données

```json
{
  "french": "Je mange une pomme",
  "shimaore": "Nissi chaoula toufa",
  "kibouchi": "Zahou ihinagna hatrouka",
  "french_words": ["Je", "mange", "une", "pomme"],
  "shimaore_words": ["Nissi", "chaoula", "toufa"],
  "kibouchi_words": ["Zahou", "ihinagna", "hatrouka"],
  "difficulty": 1,
  "tense": "present",
  "subject": "je"
}
```

### Difficulté des Phrases

**Niveau 1 (Facile) :**
- Présent simple
- Pronoms : je, tu, il
- Verbes courants (manger, parler, jouer)
- 3-4 mots

**Niveau 2 (Moyen) :**
- Présent + Passé composé
- Pronoms : je, tu, il, nous, vous
- Verbes plus variés
- 4-5 mots

**Niveau 3 (Difficile) :**
- Présent + Passé composé
- Tous les pronoms
- Verbes irréguliers
- 5-6 mots

---

## 🔍 Vérification de l'Erreur

**Pour identifier l'erreur que vous avez constatée, j'ai besoin de :**

1. **La phrase française affichée** (exactement comme elle apparaît)
2. **La traduction Shimaoré ou Kibouchi** proposée
3. **Le temps de la phrase** (présent ou passé composé)
4. **Le pronom utilisé** (je, tu, il, nous, vous, ils)
5. **Le verbe concerné**

**Exemples d'erreurs possibles :**
- ❌ "Je parle" conjugué comme "Je parlé"
- ❌ "Nous mangeons" conjugué comme "Nous mangons" (sans 'e')
- ❌ "Il a mangé" sans auxiliaire "avoir"
- ❌ Mauvais accord du participe passé avec ÊTRE

---

## 📝 Note Importante

Les règles de conjugaison sont implémentées dans :
- **Backend :** `/app/backend/conjugation_engine.py`
- **Base de données :** Collection `sentences` dans MongoDB
- **Script de génération :** `/app/backend/fix_french_conjugation_complete.py`

Si vous constatez une erreur, dites-moi précisément quelle phrase est incorrecte et je pourrai la corriger ! 🔧
