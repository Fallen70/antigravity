# Récapitulatif d'Analyse : Optimisation des Skills & Refactorisation de `motw-writer`

**Date** : 28 juillet 2026  
**Workspace** : `/home/fallen/agy`  
**Cible** : Architecture des Skills & Skill `motw-writer`

---

## 1. Principes Généraux d'Optimisation des Tokens pour les Skills

L'objectif de l'optimisation d'une skill est de limiter le nombre de tokens injectés dans le prompt système et la fenêtre de contexte de l'agent AI, tout en maintenant un haut niveau de performance.

### A. La Divulgation Progressive (*Progressive Disclosure*)
- **Principe** : Ne pas charger toute la documentation au démarrage.
- **Fichier `SKILL.md` principal** : Doit être léger et se limiter au rôle général, aux principes clés et à l'aiguillage.
- **Sous-fichiers (`references/`, `templates/`)** : Hébergent la documentation détaillée et les modèles. L'agent les consulte via `view_file` **uniquement à l'étape où ils sont nécessaires**.

### B. Optimisation du Frontmatter YAML
- Le champ `description` dans le YAML au sommet de `SKILL.md` est le seul élément constamment chargé en mémoire pour la détection d'activation.
- **Règle** : Garder la `description` courte, orientée vers les déclencheurs (*triggers* / mots-clés d'activation), sans y inclure de documentation ou de code.

### C. Automatisation via des Scripts Exécutables (`scripts/`)
- Déporter le traitement lourd de texte ou la validation de schémas dans des scripts autonomes (Python, Bash, Node) logés dans un dossier `scripts/`.
- L'agent exécute le script via la ligne de commande (`run_command`), ce qui n'injecte dans le contexte que le résultat final au lieu de centaines de lignes de consignes.

### D. Rédaction Sobres et Directe
- Préférer les listes à puces, tableaux et consignes impératives ("FAIRE", "NE PAS FAIRE").
- Supprimer les bavardages narratives et les exemples redondants.

---

## 2. Analyse de la Skill `motw-writer`

La skill **`motw-writer`** (`.agents/skills/motw-writer/`) est un assistant d'écriture pour le jeu de rôle *Monster of the Week* (PbtA).

### Structure Initiale
- **Fichiers** : `SKILL.md`
- **Dossiers** : `references/` (5 fichiers), `templates/` (4 fichiers)
- **Point Fort Initial** : La skill possédait déjà une découpe en fichiers de référence et de modèles.

### Dysfonctionnements & Goulots d'Étranglement Identifiés
1. **Consommation excessive de tokens** : L'ancien `SKILL.md` référençait tous les templates simultanément sans consigne de lecture différée. L'agent risquait de lire les 9 fichiers de référence dès le 1er tour.
2. **Workflow trop abrupt** : La procédure demandait de tout remplir d'un coup, sans offrir un échange pas-à-pas interactif avec le Gardien (MJ).
3. **Manques sur les règles MotW** : Absence de références explicites pour les Témoins/Innocents (*Bystanders*) et pour les Manœuvres sur mesure (*Custom Moves*).

---

## 3. Modifications Appliquées dans `SKILL.md`

Le fichier [SKILL.md](file:///home/fallen/agy/.agents/skills/motw-writer/SKILL.md) a été refactorisé avec les améliorations suivantes :

### A. Consignes d'Optimisation Strictes
```markdown
> [!IMPORTANT]
> **Consignes d'optimisation de tokens & interaction pas-à-pas** :
> 1. **Lecture à la demande** : Ne lisez PAS tous les fichiers de référence/template au début. Consultez un fichier via `view_file` uniquement à l'étape où il est nécessaire.
> 2. **Progression séquentielle** : Avancez une étape à la fois. Posez 1 à 2 questions ciblées au Gardien et attendez sa réponse avant de passer à l'étape suivante.
```

### B. Découpage en Procédure Interactives en 5 Étapes
1. **Étape 1 : Concept & Type de Scénario** (Monstre vs Phénomène) -> consulte `references/scenario_types.md`.
2. **Étape 2 : La Menace Principale** (Caractéristiques, PV, Faiblesse) -> consulte `templates/monster_template.md` ou `references/phenomena.md`.
3. **Étape 3 : L'Accroche & Le Compte à rebours** (Progression 6 phases) -> consulte `references/countdown_guide.md`.
4. **Étape 4 : Lieux & Menaces Secondaires** (Sbires, PNJ, Lieux) -> consulte `references/threat_types.md`, `templates/location_template.md` et `references/location_moves.md`.
5. **Étape 5 : Synthèse & Fiche Finale** -> consulte `templates/mystery_template.md` pour la compilation finale.

---

## 4. Feuille de Route / Recommandations Futures

| Axe | Action à réaliser | Emplacement suggéré |
| :--- | :--- | :--- |
| **Règles PbtA** | Ajouter la référence des types/motivations des Témoins (*Bystanders*) | `references/bystanders.md` |
| **Game Design** | Ajouter un guide de création de manœuvres personnalisées (*Custom Moves*) | `references/custom_moves.md` |
| **Outillage** | Script Python d'exportation de fiche synthétique 1-page pour l'impression/jeu direct | `scripts/export_keeper_card.py` |
| **Inspiration** | Table de tirage d'idées/amorces de mystères (légendes urbaines, tropes) | `references/hooks_generator.md` |
