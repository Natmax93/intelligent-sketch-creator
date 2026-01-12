"""
Journalisation minimale au format CSV.

Objectif :
- produire un fichier events.csv compatible avec l'approche HAII
- stocker un session_id stable pendant toute la session
- faciliter l'ajout de nouveaux champs plus tard

Ce logger est volontairement simple.
"""

import csv
import os
from datetime import datetime
import uuid


class EventLogger:
    def __init__(self, path="events.csv"):
        # Chemin de sortie du fichier
        self.path = path

        # Identifiant unique de session (anonyme)
        self.session_id = str(uuid.uuid4())

        # Si le fichier n'existe pas, on crée l'en-tête
        self._ensure_header()

        # Liste des colonnes présentes dans notre CSV (cohérence DictWriter)
        self.fieldnames = ["timestamp", "session_id", "event_type", "notes"]

    def _ensure_header(self):
        """
        Crée le fichier CSV et écrit la ligne d'en-tête si le fichier n'existe pas.
        """
        if os.path.exists(self.path):
            return

        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["timestamp", "session_id", "event_type", "notes"]
            )
            writer.writeheader()

    def log(self, event_type: str, notes: str = ""):
        """
        Ajoute une ligne de log au CSV.

        event_type : type d'événement ("invoke_help", "user_action", "show_hint", ...)
        notes : champ libre (optionnel)
        """
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": self.session_id,
                    "event_type": event_type,
                    "notes": notes,
                }
            )
