---
name: Dungeon World Fronts Assistant
description: Skill to help Game Masters design Fronts for Dungeon World, with dedicated reference sheets for every danger type.
---

# 📖 Présentation
Ce skill accompagne la création de **Fronts** – collections de dangers interconnectés – en suivant les règles officielles de **Dungeon World** (voir https://pbta.fr/wiki/dungeonworld:fronts).

## 📚 Principaux composants d’un Front (selon les règles)
1. **Front** – Le groupe global (campagne ou aventure). 
2. **Dangers** – Entités majeures (organisations, forces planaires, ennemis occultes, hordes, lieux maudits). Chaque danger possède :
   - *Nom* et *Description* courte.
   - *But* (motivation essentielle).
   - *Acteurs* (personnages, créatures, sites liés).
   - *Actions sur‑mesure* (MJ‑only actions).
3. **Catastrophe imminente** – Un événement catastrophique qui se déclenche si le danger n’est pas maîtrisé. Choisissez parmi ces 6 types officiels :
   - *Tyrannie* (du fort sur le faible)
   - *Pestilence* (propagation de maladie, fin du bien-être)
   - *Destruction* (apocalypse, ruine et malheur)
   - *Usurpation* (la chaîne de commandement se disloque)
   - *Malheur* (esclavage, renoncement à la bonté)
   - *Chaos rampant* (les lois de la réalité ou de la société disparaissent)
4. **Sinistres présages** – Étapes (1‑3 pour une aventure, 3‑5 pour une campagne) qui marquent la progression du danger.
5. **Enjeux** – Ce qui est en jeu pour les PJ.
6. **Acteurs généraux** – Liste des personnages et groupes impliqués dans le front.

---

# 📄 Fiches de référence des dangers
Pour un guide complet sur chaque type de danger, avec leurs buts typiques, exemples, acteurs, actions de MJ et conseils, référez-vous aux fichiers ci-dessous :

- [1️⃣ Organisations ambitieuses](file:///home/fallen/agy/.agents/skills/dungeon_world_fronts/references/01_organisations_ambitieuses.md)
- [2️⃣ Forces planaires](file:///home/fallen/agy/.agents/skills/dungeon_world_fronts/references/02_forces_planaires.md)
- [3️⃣ Ennemis occultes](file:///home/fallen/agy/.agents/skills/dungeon_world_fronts/references/03_ennemis_occultes.md)
- [4️⃣ Hordes](file:///home/fallen/agy/.agents/skills/dungeon_world_fronts/references/04_hordes.md)
- [5️⃣ Lieux maudits](file:///home/fallen/agy/.agents/skills/dungeon_world_fronts/references/05_lieux_maudits.md)

---

## 🛠️ Workflow de création
1. **Choisir le type de front** – Campagne ou aventure.
2. **Créer 2‑3 dangers** : pour chaque danger choisir le type, remplir les champs *Nom*, *But*, *Description*, *Acteurs*, *Catastrophe imminente* et *Actions sur‑mesure*.
3. **Définir les sinistres présages** : 1‑3 (aventure) ou 3‑5 (campagne).
4. **Formuler 1‑3 questions sur les enjeux**.
5. **Lister les acteurs généraux du front**.
6. **Rédiger la conclusion** – Succès / Échec / Compromis.

---

## 📋 Modèle de Front (à remplir)
```
# Front : <Nom du Front> (Campagne/Adventure)

## Dangers
### 1. <Nom du danger>
- **Type**: <Organisation ambitieuse | Force planaire | Ennemis occultes | Horde | Lieu maudit>
- **But**: <Motivation essentielle>
- **Description**: <Phrase courte>
- **Acteurs**: <Nom 1>, <Nom 2>, …
- **Catastrophe imminente**: <Événement si danger non maîtrisé>
- **Actions sur‑mesure**:
  - <Action MJ 1>
  - <Action MJ 2>

### 2. <Nom du danger>
… (répétez)

## Sinistres présages
1. <Présage 1>
2. <Présage 2>
3. <Présage 3>
… (ajoutez jusqu’à 5)

## Enjeux (questions)
- <Question 1>
- <Question 2>
- <Question 3>

## Acteurs généraux du front
- <Acteur 1>
- <Acteur 2>
…

## Conclusion du front
- **Succès**: <Ce qui arrive si les PJ résolvent le front>
- **Échec**: <Conséquences si la catastrophe s’accomplit>
- **Compromis** (optionnel): <Résultat intermédiaire>
```

---

## 🤖 Prompts d’exemple pour l’IA Antigravity
- "Donne‑moi 3 types de dangers pour un front de campagne."
- "Propose une catastrophe imminente pour le danger Cabale lié à un culte secret."
- "Liste 2 actions sur‑mesure pour une Horde de barbares."
- "Écris 4 sinistres présages pour un front d’aventure impliquant une porte des glaces."

### 🎲 Prompts avancés pour la session de jeu
- "À partir du premier sinistre présage du Front L’ouverture de la Porte des Glaces, génère‑moi une scène d'introduction détaillée."
- "Propose‑moi 3 idées de rencontres (combat, social, mystère) qui utilisent le deuxième danger du même Front."
- "Crée un PNJ secondaire qui aide les PJ à résoudre le troisième sinistre présage, avec 2 traits de personnalité et un secret."
- "Donne‑moi 2 variantes de la catastrophe imminente si les PJ échouent à temps, en incluant un rebondissement dramatique."

---
*Ce skill est entièrement en français et respecte les règles officielles de Dungeon World.*
