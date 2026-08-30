---
name: Dungeon World Localités Assistant
description: Skill pour aider le MENEUR DE JEU (MJ) à créer, détailler et faire évoluer des localités (villages, bourgs, forteresses, villes) dans Dungeon World avec gestion des marqueurs et génération d'une liste de lieux d'intérêt.
---

# 📖 Présentation

Ce skill accompagne la création et la gestion des **Localités** (villages, bourgs, forteresses et villes) en suivant les règles officielles de **Dungeon World** (voir https://pbta.fr/wiki/dungeonworld:monde#creation_du_monde).

Il permet de générer des communautés vivantes grâce au système de **marqueurs** (prospérité, population, défenses, caractéristiques) et d'établir une **liste complète de lieux d'intérêt et de quartiers** adaptés aux besoins des Joueurs (PJ).

---

# 📚 Fiches de référence

Pour un guide détaillé sur les marqueurs, la création pas-à-pas, la génération de lieux et les mécaniques d'évolution entre les sessions, consultez les fiches ci-dessous :

- [🏷️ 1. Guide des marqueurs de localité](file:///home/fallen/agy/.agents/skills/dungeon_world_localites/references/01_marqueurs.md)
- [🏙️ 2. Création pas-à-pas par type (Village, Bourg, Forteresse, Ville)](file:///home/fallen/agy/.agents/skills/dungeon_world_localites/references/02_creation_par_type.md)
- [🏰 3. Guide de génération des lieux d'intérêt et quartiers](file:///home/fallen/agy/.agents/skills/dungeon_world_localites/references/03_lieux_et_quartiers.md)
- [🔄 4. Évolution des localités & Mécaniques de carte](file:///home/fallen/agy/.agents/skills/dungeon_world_localites/references/04_evolution_et_mecaniques.md)

---

## 🛠️ Workflow de création d'une localité

1. **Choisir le type de localité** :
   - *Village* (petite communauté rurale ou isolée)
   - *Bourg* (centre d'échange autour d'un point de passage ou moulin)
   - *Forteresse* (bastion militaire défendant une zone stratégique)
   - *Ville* (métropole commerciale et multiculturelle)

2. **Établir les marqueurs de base** (selon le type choisi).
3. **Sélectionner une Origine / Caractéristique** (ajuste les marqueurs `+` / `-`).
4. **Sélectionner un Problème local** (ajuste les marqueurs `+` / `-`).
5. **Finaliser le profil de marqueurs** :
   - *Prospérité* : Crasseuse, Pauvre, Moyenne, Aisée, Riche.
   - *Population* : Exode, En déclin, Stable, Croissante, En plein essor.
   - *Défenses* : Aucune, Milice, Guet, Garde, Garnison, Bataillon, Légion.
   - *Marqueurs secondaires* : Magie, Religion, Crime, Artisanat, Ressource, Besoin, Serment, Commerce, Inimitié, etc.

6. **Générer la liste des Lieux d'Intérêt & Quartiers** :
   - Associer chaque marqueur majeur à au moins un lieu (ex: *Magie* ➔ tour d'arcaniste ; *Religion* ➔ grand temple ; *Crime* ➔ tripot clandestin ; *Marché* ➔ grande halle).
   - Inclure des tavernes, forges, comptoirs, marchés, lieux de culte, garnisons et zones criminelles ou mystérieuses.

7. **Créer 2 à 4 PNJ clés** (définis par leur *But* et leur *Moyen*).

8. **Rédiger les accroches & liens avec les Fronts** (rumeurs, menaces et opportunités pour les PJ).

---

## 📋 Modèle de Fiche de Localité (à remplir)

```markdown
# 🏘️ Localité : <Nom de la localité>

- **Type** : <Village | Bourg | Forteresse | Ville>
- **Localisation** : <Emplacement sur la carte de campagne>
- **Description globale** : <2-3 phrases décrivant le paysage, le style architectural et le ressenti général>

---

## 🏷️ Marqueurs

- **Prospérité** : <Crasseuse | Pauvre | Moyenne | Aisée | Riche>
- **Population** : <Exode | En déclin | Stable | Croissante | En plein essor>
- **Défenses** : <Aucune | Milice | Guet | Garde | Garnison | Bataillon | Légion>
- **Marqueurs secondaires** : <ex: Ressource (Fer), Besoin (Nourriture), Serment (Fort-Espoir), Crime, Magie...>

---

## 🏛️ Lieux d'Intérêt & Quartiers

### 1. 🍷 <Nom du lieu / Taverne> (Taverne & Auberge)
- **Quartier / Zone** : <Nom du quartier ou emplacement>
- **Description & Ambiance** : <Visuel, odeurs, ambiance sonore>
- **PNJ remarquable** : <Nom du PNJ> (But : <Désir>, Moyen : <Méthode>)
- **Services & Opportunités** : <Ce qu'on y trouve, rumeurs ou affaires à conclure>

### 2. ⚒️ <Nom du lieu / Forge / Échoppe> (Commerce & Artisanat)
- **Quartier / Zone** : <Nom du quartier>
- **Description & Ambiance** : <Description>
- **PNJ remarquable** : <Nom du PNJ> (But : <Désir>, Moyen : <Méthode>)
- **Services & Opportunités** : <Biens vendus, équipements spécialisés>

### 3. 🛡️ <Nom du lieu / Bastion> (Autorité & Défense)
- **Quartier / Zone** : <Nom du quartier>
- **Description & Ambiance** : <Description>
- **PNJ remarquable** : <Nom du PNJ> (But : <Désir>, Moyen : <Méthode>)
- **Services & Opportunités** : <Primes, recrutement, justice>

### 4. 🔮 / ⛩️ <Nom du lieu / Temple / Tour> (Magie / Religion)
- **Quartier / Zone** : <Nom du quartier>
- **Description & Ambiance** : <Description>
- **PNJ remarquable** : <Nom du PNJ> (But : <Désir>, Moyen : <Méthode>)
- **Services & Opportunités** : <Soins, identificateurs d'objets magiques, quêtes pures>

### 5. 🗡️ <Nom du lieu / Bas-fonds> (Crime / Clandestin)
- **Quartier / Zone** : <Les Bas-fonds / Les Quais>
- **Description & Ambiance** : <Description>
- **PNJ remarquable** : <Nom du PNJ> (But : <Désir>, Moyen : <Méthode>)
- **Services & Opportunités** : <Marché noir, receleur, informations secrètes>

---

## 👥 Personnages Remarquables (PNJ Clés)

1. **<Nom du PNJ 1>** - <Rôle / Titre>
   - **But** : <Son objectif principal dans la localité>
   - **Moyen** : <Ses moyens d'action ou ressources>
2. **<Nom du PNJ 2>** - <Rôle / Titre>
   - **But** : <Son objectif principal>
   - **Moyen** : <Ses moyens d'action>

---

## 📜 Rumeurs & Accroches d'Aventure

- **Rumeur 1** : <Élément en lien avec les marqueurs ou un Front proche>
- **Rumeur 2** : <Problème local nécessitant l'aide d'aventuriers>
```

---

## 🤖 Prompts d'exemple pour l'IA Antigravity

- "Crée un **Village** côtier qui possède la ressource *Poisson*, avec un marqueur *Culte* et le problème *Monstres menaçants*. Génère 4 lieux d'intérêt dont un sanctuaire sous-marin."
- "Donne-moi le profil de marqueurs et la liste des quartiers/lieux pour une **Ville** de montagne dirigée par une guilde de nains forgerons."
- "Génère 5 lieux d'intérêt vivants pour un **Bourg** ayant les marqueurs *Aisée*, *Magie* et *Crime*."
- "Met à jour la carte de campagne : la localité de Fort-Gris subit un siège et manque de nourriture, quels marqueurs évoluent ?"

---
*Ce skill est entièrement rédigé en français et s'appuie rigoureusement sur les règles officielles de Dungeon World.*
