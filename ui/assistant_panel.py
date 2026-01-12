"""
Panneau latéral Assistant.

Responsabilité :
- afficher les catégories (Tour/Porte/Mur) et les suggestions
- (plus tard) gérer clic -> prévisualisation -> appliquer/ignorer
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AssistantPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Layout vertical pour empiler les composants
        layout = QVBoxLayout(self)

        # Placeholder
        layout.addWidget(QLabel("Suggestions IA (placeholder)"))
