"""
Définition des outils disponibles dans l'éditeur.

Pourquoi un Enum ?
- évite les chaînes de caractères ("pen", "select"...)
- plus sûr, autocomplétion, moins d'erreurs
"""

from enum import Enum, auto


class Tool(Enum):
    SELECT = auto()  # Outil de sélection / déplacement
    PEN = auto()  # Dessin libre
    RECT = auto()  # Rectangle
    ELLIPSE = auto()  # Ellipse
    LINE = auto()  # Ligne
