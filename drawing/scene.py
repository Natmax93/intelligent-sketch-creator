"""
QGraphicsScene spécialisée pour notre éditeur.

Responsabilité :
- stocker l'outil courant
- (plus tard) gérer les événements souris selon l'outil
- (plus tard) créer/ajouter des QGraphicsItem dans la scène
"""

from PySide6.QtWidgets import QGraphicsScene
from drawing.tools import Tool


class DrawingScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        # Outil actif (par défaut : sélection)
        self._tool = Tool.SELECT

    def set_tool(self, tool: Tool):
        """
        Change l'outil courant.
        Typiquement appelé par la toolbar.
        """
        self._tool = tool

    def tool(self) -> Tool:
        """
        Retourne l'outil courant.
        Utile dans mousePressEvent/mouseMoveEvent/mouseReleaseEvent.
        """
        return self._tool
