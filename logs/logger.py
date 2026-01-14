"""
logger.py

Journalisation minimale des interactions utilisateur au format CSV.

Objectifs :
- produire un fichier events.csv exploitable pour l'analyse HAII
- associer tous les événements d'une même session à un identifiant unique
- rester simple, extensible et conforme RGPD (pas de données personnelles)

Ce logger est volontairement :
- synchrone (simple à comprendre)
- orienté événements (event_type + champs contextuels)
"""

import csv
import os
from datetime import datetime
import uuid


class EventLogger:
    def __init__(self, path="events.csv"):
        """
        Initialise le logger.

        Parameters
        ----------
        path : str
            Chemin vers le fichier CSV de sortie.
        """
        self.path = path

        # Identifiant unique de session (UUID v4)
        # - généré aléatoirement
        # - anonyme
        # - constant pendant toute la durée de l'application
        self.session_id = str(uuid.uuid4())

        # Liste des colonnes du CSV.
        # IMPORTANT :
        # - toutes les lignes auront exactement ces colonnes
        # - les champs non renseignés seront laissés vides
        self.fieldnames = [
            "timestamp",  # date ISO 8601
            "session_id",  # identifiant de session
            "event_type",  # type d'événement (pen_start, pen_end, select_press, etc.)
            "tool",  # outil actif (PEN, SELECT, ...)
            "item_type",  # type d'objet graphique concerné
            "n_points",  # nombre de points (pour le stylo)
            "notes",  # champ libre (debug / contexte)
        ]

        # Crée le fichier + en-tête si nécessaire
        self._ensure_header()

    def _ensure_header(self):
        """
        Crée le fichier CSV et écrit la ligne d'en-tête
        uniquement si le fichier n'existe pas encore.
        """
        if os.path.exists(self.path):
            return

        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def log(self, event_type: str, **fields):
        """
        Ajoute une ligne d'événement au CSV.

        Parameters
        ----------
        event_type : str
            Nom de l'événement (ex: "pen_start", "item_moved", "tool_change").

        **fields :
            Champs optionnels (tool, item_type, n_points, notes, etc.).
            Les champs inconnus sont ignorés silencieusement.
        """

        # On initialise une ligne avec toutes les colonnes vides
        row = {k: "" for k in self.fieldnames}

        # Champs obligatoires remplis automatiquement
        row["timestamp"] = (
            datetime.now().isoformat()
        )  # TODO Changé car utcnow() est obsolète
        row["session_id"] = self.session_id
        row["event_type"] = event_type

        # On copie uniquement les champs autorisés
        # (évite les fautes de frappe et garde un CSV propre)
        for key, value in fields.items():
            if key in row:
                row[key] = value

        # Écriture effective dans le fichier CSV
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)
