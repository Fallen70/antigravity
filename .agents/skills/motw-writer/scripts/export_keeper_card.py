#!/usr/bin/env python3
"""
Script d'exportation pour Monster of the Week (motw-writer).
Architecture orientée objet : une classe par entité du jeu
(Monstre, Phénomène, Sbire, Lieu, Figurant) avec polymorphisme
et Factory Pattern pour la menace principale.

Usage:
    python3 export_keeper_card.py mystery_data.json [output_path.md]
    cat mystery_data.json | python3 export_keeper_card.py - [output_path.md]
"""

from abc import ABC, abstractmethod
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List


# ==========================================
# 1. Classe abstraite commune (Renderable)
# ==========================================

class Renderable(ABC):
    """Interface commune pour tous les objets pouvant générer du Markdown."""

    @abstractmethod
    def render_markdown(self) -> List[str]:
        """Génère les lignes Markdown représentant cet objet."""
        pass


# ==========================================
# 2. Menace Principale (Monstre / Phénomène)
# ==========================================

class BaseThreat(Renderable):
    """Classe abstraite représentant la menace principale d'un Mystère."""

    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name", "Menace Inconnue")
        self.category = data.get("category", "Inconnue")
        self.type = data.get("type", "N/A")
        self.motivation = data.get("motivation", "")
        self.moves = data.get("moves", [])


class MonsterThreat(BaseThreat):
    """Représente un Monstre (avec PV, Armure, Faiblesse et Attaques)."""

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.hp = data.get("hp", "N/A")
        self.armor = data.get("armor", 0)
        self.weakness = data.get("weakness", "Non identifiée")
        self.attacks = data.get("attacks", [])

    def render_markdown(self) -> List[str]:
        lines = [
            f"## 👹 Menace Principale : Monstre ({self.name})",
            f"- **Type & Motivation** : `{self.type}` — *{self.motivation}*",
            f"- **Points de Vie (PV)** : {self.hp} | **Armure** : {self.armor}",
            f"- **⚡ FAIBLESSE** : **{self.weakness}**",
        ]
        if self.attacks:
            lines.append("- **Attaques** :")
            for atk in self.attacks:
                lines.append(f"  - {atk}")
        if self.moves:
            lines.append("- **Manœuvres de Monstre** :")
            for mv in self.moves:
                lines.append(f"  - {mv}")
        return lines


class PhenomenonThreat(BaseThreat):
    """Représente un Phénomène (avec Altération de la réalité et Confinement/Résolution)."""

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.alteration = data.get("alteration", "")
        self.containment = data.get("containment", data.get("weakness", "Non identifié"))
        self.effects = data.get("effects", data.get("attacks", []))

    def render_markdown(self) -> List[str]:
        lines = [
            f"## 🌀 Menace Principale : Phénomène ({self.name})",
            f"- **Type & Motivation** : `{self.type}` — *{self.motivation}*",
        ]
        if self.alteration:
            lines.append(f"- **Altération de la réalité** : {self.alteration}")
        if self.containment:
            lines.append(f"- **🛡️ CONDITION DE CONFINEMENT / RÉSOLUTION** : **{self.containment}**")
        if self.effects:
            lines.append("- **Effets & Manifestations** :")
            for eff in self.effects:
                lines.append(f"  - {eff}")
        if self.moves:
            lines.append("- **Manœuvres de Phénomène** :")
            for mv in self.moves:
                lines.append(f"  - {mv}")
        return lines


# ==========================================
# 3. Sbires (Minions)
# ==========================================

class Minion(Renderable):
    """Représente un Sbire au service de la menace principale."""

    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name", "Sbire Inconnu")
        self.type = data.get("type", "N/A")
        self.motivation = data.get("motivation", "")
        self.master = data.get("master", "")
        self.description = data.get("description", "")
        self.behavior = data.get("behavior", "")
        self.hp = data.get("hp", "N/A")
        self.armor = data.get("armor", 0)
        self.weaknesses = data.get("weaknesses", "")
        self.attacks = data.get("attacks", [])
        self.moves = data.get("moves", [])

    def render_markdown(self) -> List[str]:
        lines = [
            f"### ⚔️ {self.name}",
            f"- **Type & Motivation** : `{self.type}` — *{self.motivation}*",
        ]
        if self.master:
            lines.append(f"- **Maître** : {self.master}")
        if self.description:
            lines.append(f"- **Description** : {self.description}")
        if self.behavior:
            lines.append(f"- **Comportement** : {self.behavior}")
        lines.append(f"- **PV** : {self.hp} | **Armure** : {self.armor}")
        if self.weaknesses:
            lines.append(f"- **Vulnérabilités** : {self.weaknesses}")
        if self.attacks:
            lines.append("- **Attaques** :")
            for atk in self.attacks:
                lines.append(f"  - {atk}")
        if self.moves:
            lines.append("- **Manœuvres de Sbire** :")
            for mv in self.moves:
                lines.append(f"  - {mv}")
        return lines


# ==========================================
# 4. Lieux (Locations)
# ==========================================

class Location(Renderable):
    """Représente un Lieu clé du Mystère."""

    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name", "Lieu Inconnu")
        self.type = data.get("type", "N/A")
        self.motivation = data.get("motivation", "")
        self.description = data.get("description", "")
        self.moves = data.get("moves", [])

    def render_markdown(self) -> List[str]:
        lines = [
            f"### • {self.name} (`{self.type}`)",
        ]
        if self.motivation:
            lines.append(f"  *Motivation* : {self.motivation}")
        if self.description:
            lines.append(f"  {self.description}")
        if self.moves:
            lines.append("  *Manœuvres de Lieu* :")
            for mv in self.moves:
                lines.append(f"    - {mv}")
        return lines


# ==========================================
# 5. Figurants (Bystanders)
# ==========================================

class Bystander(Renderable):
    """Représente un Figurant (PNJ) gravitant autour du Mystère."""

    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name", "Figurant Inconnu")
        self.role = data.get("role", "Figurant")
        self.type = data.get("type", "N/A")
        self.motivation = data.get("motivation", "")
        self.description = data.get("description", "")
        self.clue = data.get("clue", "")
        self.reveal_condition = data.get("reveal_condition", "")

    def render_markdown(self) -> List[str]:
        lines = [
            f"### 🧑 {self.name} — {self.role}",
            f"- **Type & Motivation** : `{self.type}` — *{self.motivation}*",
        ]
        if self.description:
            lines.append(f"- **Description** : {self.description}")
        if self.clue:
            lines.append(f"- 💡 **Indice détenu** : {self.clue}")
        if self.reveal_condition:
            lines.append(f"- 🔑 **Condition de révélation** : {self.reveal_condition}")
        return lines


# ==========================================
# 6. Threat Factory (Factory Pattern)
# ==========================================

class ThreatFactory:
    """Factory instanciant la sous-classe de menace appropriée selon la catégorie."""

    @staticmethod
    def create(data: Dict[str, Any]) -> BaseThreat:
        cat = str(data.get("category", "monstre")).lower()
        if "phénomène" in cat or "phenomenon" in cat or "phenomene" in cat:
            return PhenomenonThreat(data)
        return MonsterThreat(data)


# ==========================================
# 7. Reader & Writer (IO Handlers)
# ==========================================

class JSONReader:
    """Charge et valide le JSON (minifié ou standard) depuis un fichier ou stdin."""

    @staticmethod
    def load(source: str) -> Dict[str, Any]:
        if source == "-":
            raw = sys.stdin.read()
        else:
            with open(source, "r", encoding="utf-8") as f:
                raw = f.read()
        return json.loads(raw.strip())


class KeeperCardWriter:
    """Compile et écrit la fiche Gardien Markdown."""

    @staticmethod
    def build_markdown(data: Dict[str, Any]) -> str:
        title = data.get("title", "Mystère Sans Titre")
        concept = data.get("concept", "Non spécifié")
        hook = data.get("hook", "Aucune accroche définie.")

        md = [
            f"# 📜 FICHE GARDIEN : {title.upper()}",
            f"**Concept** : {concept}\n",
            "---",
            "## 🎣 Accroche Initiale (Hook)",
            f"> {hook}\n",
            "---",
        ]

        # --- Menace Principale (via ThreatFactory) ---
        threat_data = data.get("threat", {})
        if threat_data:
            threat = ThreatFactory.create(threat_data)
            md.extend(threat.render_markdown())
            md.append("\n---")

        # --- Compte à Rebours ---
        countdown = data.get("countdown", {})
        md.append("## ⏳ Compte à Rebours (Countdown)")
        phases = [
            ("Jour (Day)", countdown.get("day", "-")),
            ("Ombres (Shadows)", countdown.get("shadows", "-")),
            ("Coucher du soleil (Sunset)", countdown.get("sunset", "-")),
            ("Crépuscule (Dusk)", countdown.get("dusk", "-")),
            ("Nuit (Night)", countdown.get("night", "-")),
            ("Minuit (Midnight)", countdown.get("midnight", "-")),
        ]
        for label, text in phases:
            md.append(f"- **{label}** : {text}")
        md.append("\n---")

        # --- Sbires (classe Minion) ---
        minions_data = data.get("minions", [])
        if minions_data:
            md.append("## ⚔️ Sbires")
            for m_data in minions_data:
                minion = Minion(m_data)
                md.extend(minion.render_markdown())
            md.append("\n---")

        # --- Lieux Clés (classe Location) ---
        locations_data = data.get("locations", [])
        if locations_data:
            md.append("## 📍 Lieux Clés")
            for l_data in locations_data:
                location = Location(l_data)
                md.extend(location.render_markdown())
            md.append("\n---")

        # --- Figurants (classe Bystander) ---
        bystanders_data = data.get("bystanders", [])
        if bystanders_data:
            md.append("## 👥 Figurants (PNJ)")
            for b_data in bystanders_data:
                bystander = Bystander(b_data)
                md.extend(bystander.render_markdown())

        return "\n".join(md)

    @staticmethod
    def write(output_path: str, content: str) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Exportateur MotW — classes dédiées par entité.")
    parser.add_argument("input", help="Fichier JSON d'entrée ou '-' pour stdin")
    parser.add_argument("output", nargs="?", default="keeper_card.md", help="Fichier Markdown de sortie")
    args = parser.parse_args()

    try:
        # 1. Lecture via JSONReader
        data = JSONReader.load(args.input)

        # 2. Construction du Markdown via KeeperCardWriter
        md_content = KeeperCardWriter.build_markdown(data)

        # 3. Écriture du fichier
        KeeperCardWriter.write(args.output, md_content)
        print(f"✅ Fiche Gardien générée avec succès : {Path(args.output).absolute()}")
    except Exception as e:
        print(f"❌ Erreur lors du traitement : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
