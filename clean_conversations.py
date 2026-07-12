#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
import sqlite3
from datetime import datetime

# Dossiers d'Antigravity
BASE_DIR = os.path.expanduser("~/.gemini/antigravity-cli")
CONVS_DIR = os.path.join(BASE_DIR, "conversations")
BRAIN_DIR = os.path.join(BASE_DIR, "brain")

# UID de la conversation actuelle depuis l'environnement
ACTIVE_CONV_ID = os.environ.get("ANTIGRAVITY_CONVERSATION_ID")

def clean_description(content):
    if not content:
        return "<Sans contenu>"
    content = content.strip()
    # Supprimer les balises <USER_REQUEST> si présentes
    if content.startswith("<USER_REQUEST>"):
        content = content[len("<USER_REQUEST>"):].strip()
    if content.endswith("</USER_REQUEST>"):
        content = content[:-len("</USER_REQUEST>")].strip()
    # Remplacer les retours à la ligne par des espaces
    content = content.replace("\n", " ").replace("\r", " ")
    # Tronquer pour l'affichage
    if len(content) > 80:
        return content[:77] + "..."
    return content

def get_conversation_details(uuid):
    db_path = os.path.join(CONVS_DIR, f"{uuid}.db")
    mtime = os.path.getmtime(db_path)
    date_str = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M:%S")
    
    description = None
    # Tenter de lire le fichier de log de la conversation (transcript.jsonl)
    transcript_path = os.path.join(BRAIN_DIR, uuid, ".system_generated", "logs", "transcript.jsonl")
    if os.path.exists(transcript_path):
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get("type") == "USER_INPUT":
                            description = clean_description(data.get("content"))
                            break
                    except Exception:
                        continue
        except Exception:
            pass
            
    if not description:
        # Fallback sqlite
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT step_payload FROM steps WHERE step_type = 14 LIMIT 1")
            row = cursor.fetchone()
            if row:
                description = "<Conversation (protobuffer)>"
            else:
                description = "<Sans transcript / vide>"
            conn.close()
        except Exception:
            description = "<Détails indisponibles>"
            
    return {
        "uuid": uuid,
        "date": date_str,
        "description": description,
        "is_active": (uuid == ACTIVE_CONV_ID)
    }

def list_conversations():
    if not os.path.exists(CONVS_DIR):
        print(f"Le dossier {CONVS_DIR} n'existe pas.")
        return []
    
    uuids = []
    for f in os.listdir(CONVS_DIR):
        if f.endswith(".db"):
            uuids.append(f[:-3])
            
    conversations = []
    for uuid in uuids:
        try:
            conversations.append(get_conversation_details(uuid))
        except Exception:
            continue
            
    # Trier par date de modification (la plus récente en premier)
    conversations.sort(key=lambda x: x["date"], reverse=True)
    return conversations

def delete_conversation(uuid):
    # 1. Supprimer de la base summaries
    summaries_db = os.path.join(BASE_DIR, "conversation_summaries.db")
    if os.path.exists(summaries_db):
        try:
            conn = sqlite3.connect(summaries_db)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversation_summaries WHERE conversation_id = ?", (uuid,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Avertissement (summaries.db) : {e}")
            
    # 2. Mettre à jour last_conversations.json
    cache_path = os.path.join(BASE_DIR, "cache", "last_conversations.json")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            keys_to_remove = [k for k, v in data.items() if v == uuid]
            if keys_to_remove:
                for k in keys_to_remove:
                    del data[k]
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Avertissement (last_conversations.json) : {e}")

    # 3. Supprimer les fichiers de base de données sqlite
    for ext in [".db", ".db-shm", ".db-wal"]:
        path = os.path.join(CONVS_DIR, uuid + ext)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Erreur lors de la suppression de {path} : {e}")
                
    # 4. Supprimer le dossier brain
    brain_path = os.path.join(BRAIN_DIR, uuid)
    if os.path.exists(brain_path):
        try:
            shutil.rmtree(brain_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier {brain_path} : {e}")

def print_table(conversations):
    if not conversations:
        print("\nAucune conversation trouvée.")
        return
        
    print("\nConversations Antigravity :")
    print("-" * 125)
    print(f"{'N°':<4} | {'UID de la conversation':<38} | {'Dernière modification':<20} | {'Description (Premier message)'}")
    print("-" * 125)
    
    for i, c in enumerate(conversations, 1):
        status_tag = " (Session Active)" if c["is_active"] else ""
        uuid_display = c["uuid"] + status_tag
        print(f"{i:<4} | {uuid_display:<38} | {c['date']:<20} | {c['description']}")
    print("-" * 125)

def main():
    # Gestion des arguments de ligne de commande
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--list":
            convs = list_conversations()
            print_table(convs)
            sys.exit(0)
        elif arg == "--delete" and len(sys.argv) > 2:
            target_uuid = sys.argv[2]
            if target_uuid == ACTIVE_CONV_ID:
                print(f"Erreur : Impossible de supprimer la conversation en cours ({target_uuid}).")
                sys.exit(1)
            delete_conversation(target_uuid)
            print(f"Conversation {target_uuid} supprimée avec succès.")
            sys.exit(0)
        elif arg == "--delete-inactive":
            convs = list_conversations()
            inactive = [c for c in convs if not c["is_active"]]
            if not inactive:
                print("Aucune conversation inactive à supprimer.")
                sys.exit(0)
            confirm = input(f"Voulez-vous vraiment supprimer les {len(inactive)} conversations inactives ? (y/N) : ")
            if confirm.lower() in ['y', 'yes', 'o', 'oui']:
                for c in inactive:
                    delete_conversation(c["uuid"])
                print("Toutes les conversations inactives ont été supprimées.")
            else:
                print("Annulé.")
            sys.exit(0)
        else:
            print("Usage :")
            print("  python3 clean_conversations.py")
            print("  python3 clean_conversations.py --list")
            print("  python3 clean_conversations.py --delete <UUID>")
            print("  python3 clean_conversations.py --delete-inactive")
            sys.exit(1)

    # Mode interactif
    while True:
        convs = list_conversations()
        print_table(convs)
        
        print("\nOptions :")
        print("  [numéro]  Supprimer la conversation correspondante (ex: 1)")
        print("  [all]     Supprimer toutes les conversations inactives")
        print("  [q]       Quitter")
        
        try:
            choice = input("\nVotre choix : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAu revoir !")
            break
            
        if choice.lower() == 'q':
            print("Au revoir !")
            break
        elif choice.lower() == 'all':
            inactive = [c for c in convs if not c["is_active"]]
            if not inactive:
                print("\nAucune conversation inactive à supprimer.")
                continue
            confirm = input(f"\nVoulez-vous vraiment supprimer toutes les {len(inactive)} conversations inactives ? (y/N) : ").strip()
            if confirm.lower() in ['y', 'yes', 'o', 'oui']:
                for c in inactive:
                    delete_conversation(c["uuid"])
                print("\nConversations inactives supprimées.")
            else:
                print("\nAnnulé.")
        else:
            try:
                idx = int(choice)
                if idx < 1 or idx > len(convs):
                    print(f"\nNuméro invalide. Choisissez entre 1 et {len(convs)}.")
                    continue
                target = convs[idx-1]
                if target["is_active"]:
                    print("\nErreur : Impossible de supprimer la session active en cours.")
                    continue
                confirm = input(f"\nVoulez-vous vraiment supprimer la conversation {target['uuid']} ?\nDescription : {target['description']}\n(y/N) : ").strip()
                if confirm.lower() in ['y', 'yes', 'o', 'oui']:
                    delete_conversation(target["uuid"])
                    print(f"\nConversation {target['uuid']} supprimée.")
                else:
                    print("\nAnnulé.")
            except ValueError:
                print("\nChoix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
