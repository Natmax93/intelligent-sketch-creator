import csv
import os
from datetime import datetime
import uuid


class EventLogger:
    def __init__(self, path="events.csv"):
        self.path = path

        # Identifiant de session (déjà présent)
        self.session_id = str(uuid.uuid4())

        # --- Contexte expérimental (Solution A) ---
        # Remplis par l'app (une fois pour condition, à chaque essai pour task/trial)
        self.condition = ""  # ex: "H_ONLY" ou "H_PLUS_IA"
        self.task_id = ""  # ex: "cat", "castle", "car"
        self.trial_index = ""  # "1", "2", "3"

        self.fieldnames = [
            "timestamp",
            "session_id",
            "condition",
            "task_id",
            "trial_index",
            "event_type",
            "tool",
            "item_type",
            "n_points",
            "notes",
        ]

        self._ensure_header()

    def set_context(self, *, condition=None, task_id=None, trial_index=None):
        """Met à jour le contexte utilisé automatiquement sur les prochains logs."""
        if condition is not None:
            self.condition = condition
        if task_id is not None:
            self.task_id = task_id
        if trial_index is not None:
            self.trial_index = str(trial_index)

    def _ensure_header(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            with open(self.path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def log(self, event_type: str, **fields):
        row = {k: "" for k in self.fieldnames}

        # Champs obligatoires
        row["timestamp"] = datetime.now().isoformat()
        row["session_id"] = self.session_id
        row["condition"] = self.condition
        row["task_id"] = self.task_id
        row["trial_index"] = self.trial_index
        row["event_type"] = event_type

        # Champs optionnels
        for key, value in fields.items():
            if key in row:
                row[key] = value

        with open(self.path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)
