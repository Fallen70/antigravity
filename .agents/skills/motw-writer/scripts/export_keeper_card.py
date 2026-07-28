#!/usr/bin/env python3
"""
Script d'exportation pour Monster of the Week (motw-writer).
Utilise un design pattern Factory et le Polymorphisme pour gérer
les différents types de menaces (Monstres vs Phénomènes) et générer
la Fiche Gardien (Keeper Card) au format Markdown.

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
# 1. Hiérarchie des Menaces (Polymorphisme)
# ==========================================

class BaseThreat(ABC):
    """Classe abstraite représentant une menace dans Monster of the Week."""
    
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name", "Menace Inconnue")
        self.category = data.get("category", "Inconnue")
        self.type = data.get("type", "N/A")
        self.motivation = data.get("motivation", "")

    @abstractmethod
    def render_markdown(self) -> List[str]:
        """Génère la section Markdown spécifique au type de menace."""
        pass


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
            lines.append("- **Attaques / Pouvoirs** :")
            for atk in self.attacks:
                lines.append(f"  - {atk}")
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
        return lines


# ==========================================
# 2. Threat Factory (Factory Pattern)
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
# 3. Reader & Writer (IO Factory / Handlers)
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
    """Compiles et écrit la fiche Gardien Markdown."""
    
    @staticmethod
    def build_markdown(data: Dict[str, Any]) -> str:
        title = data.get("title", "Mystère Sans Titre")
        concept = data.get("concept", "Non spécifié")
        hook = data.get("hook", "Aucune accroche définie.")

        md = [
            f"# 📜 FICHE GARDIEN : {title.upper()}",
            f"**Concept** : {concept}\n",
            "---",
            "## 🎣 Accroche Initial (Hook)",
            f"> {hook}\n",
            "---",
        ]

        # Instanciation dynamique via la ThreatFactory
        threat_data = data.get("threat", {})
        if threat_data:
            threat = ThreatFactory.create(threat_data)
            md.extend(threat.render_markdown())
            md.append("\n---")

        # Compte à Rebours
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

        # Lieux Clés
        locations = data.get("locations", [])
        if locations:
            md.append("## 📍 Lieux Clés")
            for loc in locations:
                md.append(f"### • {loc.get('name')} (`{loc.get('type')}`)")
                if "motivation" in loc:
                    md.append(f"  *Motivation* : {loc.get('motivation')}")
                if "description" in loc:
                    md.append(f"  {loc.get('description')}")
                moves = loc.get("moves", [])
                if moves:
                    md.append("  *Manœuvres* : " + ", ".join(f"`{m}`" for m in moves))
            md.append("\n---")

        # Figurants
        bystanders = data.get("bystanders", [])
        if bystanders:
            md.append("## 👥 Figurants & Sbires")
            for b in bystanders:
                role = b.get("role", "Figurant")
                md.append(f"- **{b.get('name')}** ({role}) — `{b.get('type')}` : *{b.get('motivation')}*")
                if "clue" in b:
                    md.append(f"  - 💡 *Indice détenu* : {b.get('clue')}")

        return "\n".join(md)

    @staticmethod
    def write(output_path: str, content: str) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Exportateur MotW (Threat Factory & Polymorphisme).")
    parser.add_argument("input", help="Fichier JSON d'entrée ou '-' pour stdin")
    parser.add_argument("output", nargs="?", default="keeper_card.md", help="Fichier Markdown de sortie")
    args = parser.parse_args()

    try:
        # 1. Lecture via JSONReader
        data = JSONReader.load(args.input)
        
        # 2. Construction du Markdown via KeeperCardWriter (et ThreatFactory)
        md_content = KeeperCardWriter.build_markdown(data)
        
        # 3. Écriture du fichier
        KeeperCardWriter.write(args.output, md_content)
        print(f"✅ Fiche Gardien générée avec succès : {Path(args.output).absolute()}")
    except Exception as e:
        print(f"❌ Erreur lors du traitement : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
