"""
scene.py

QGraphicsScene spécialisée pour un éditeur de dessin.

Responsabilités :
- gérer l'outil courant (stylo, sélection, etc.)
- intercepter les événements souris (press / move / release)
- créer et manipuler des QGraphicsItem
- notifier le logger des actions utilisateur

La scène ne s'occupe PAS :
- de l'UI (toolbar, boutons)
- de la logique de l'assistant IA
"""

from PySide6.QtWidgets import QGraphicsScene, QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPen
from PySide6.QtCore import QRectF

from drawing.tools import Tool


class DrawingScene(QGraphicsScene):
    def __init__(self, logger=None):
        """
        Parameters
        ----------
        logger : EventLogger | None
            Logger utilisé pour enregistrer les interactions utilisateur.
        """
        super().__init__()

        # Dimensions fixes de la zone de dessin (ex : A4 en pixels logiques)
        width = 1280
        height = 720

        self.setSceneRect(QRectF(0, 0, width, height))

        # Outil actif (par défaut : sélection)
        self._tool = Tool.SELECT

        # Logger HAII (peut être None si désactivé)
        self.logger = logger

        # ---- État interne pour Tool.PEN ----

        # Path en cours de construction (QPainterPath)
        self._current_path = None

        # Item graphique correspondant au path
        self._current_item = None

        # Nombre de points ajoutés au path (utile pour les logs)
        self._points_count = 0

        # ---- État interne pour Tool.SELECT ----

        # Item cliqué au moment du mousePress
        self._press_item = None

        # Position de la souris au mousePress
        self._press_pos = None

    # ------------------------------------------------------------------
    # Gestion de l'outil courant
    # ------------------------------------------------------------------

    def set_tool(self, tool: Tool):
        """
        Change l'outil actif.

        Appelée depuis la toolbar (EditorWindow).
        """
        self._tool = tool

        if self.logger:
            self.logger.log(event_type="tool_change", tool=tool.name)

    def tool(self) -> Tool:
        """Retourne l'outil courant."""
        return self._tool

    # ------------------------------------------------------------------
    # Événements souris
    # ------------------------------------------------------------------

    def mousePressEvent(self, event):
        """
        Appelé quand l'utilisateur appuie sur un bouton de la souris.
        """

        # ---------------- Tool.PEN ----------------
        if self._tool == Tool.PEN and event.button():
            # Position de départ du trait
            p = event.scenePos()

            # Création du path
            self._current_path = QPainterPath(p)
            self._points_count = 1

            # Création de l'item graphique associé
            self._current_item = QGraphicsPathItem(self._current_path)

            # Style minimal du stylo
            pen = QPen()
            pen.setWidth(2)
            self._current_item.setPen(pen)

            # IMPORTANT :
            # rendre l'item sélectionnable et déplaçable pour Tool.SELECT
            self._current_item.setFlag(
                self._current_item.GraphicsItemFlag.ItemIsSelectable, True
            )
            self._current_item.setFlag(
                self._current_item.GraphicsItemFlag.ItemIsMovable, True
            )

            # Ajout immédiat à la scène (dessin en temps réel)
            self.addItem(self._current_item)

            if self.logger:
                self.logger.log(event_type="pen_start", tool="PEN")

            event.accept()
            return

        # ---------------- Tool.SELECT ----------------
        if self._tool == Tool.SELECT:
            # Détection de l'item sous la souris (peut être None)
            if self.views():
                view = self.views()[0]
                self._press_item = self.itemAt(event.scenePos(), view.transform())
            else:
                self._press_item = None

            self._press_pos = event.scenePos()

            if self.logger:
                self.logger.log(
                    event_type="select_press",
                    tool="SELECT",
                    item_type=(
                        type(self._press_item).__name__ if self._press_item else "None"
                    ),
                )

        # Laisser Qt gérer le comportement standard (sélection, propagation)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Appelé quand la souris se déplace avec un bouton appuyé.
        """

        # ---------------- Tool.PEN ----------------
        if self._tool == Tool.PEN and self._current_path is not None:
            p = event.scenePos()

            # Ajoute un segment au path
            self._current_path.lineTo(p)
            self._points_count += 1

            # Met à jour l'item graphique
            self._current_item.setPath(self._current_path)

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Appelé quand l'utilisateur relâche un bouton de la souris.
        """

        # ---------------- Tool.PEN ----------------
        if self._tool == Tool.PEN and self._current_path is not None:
            if self.logger:
                self.logger.log(
                    event_type="pen_end",
                    tool="PEN",
                    item_type="QGraphicsPathItem",
                    n_points=str(self._points_count),
                )

            # Réinitialisation de l'état interne
            self._current_path = None
            self._current_item = None
            self._points_count = 0

            event.accept()
            return

        # ---------------- Tool.SELECT ----------------
        if self._tool == Tool.SELECT and self._press_pos is not None:
            # Détecte un déplacement significatif (drag)
            delta = event.scenePos() - self._press_pos
            moved = abs(delta.x()) + abs(delta.y()) > 2.0

            if moved and self.logger:
                self.logger.log(event_type="item_moved", tool="SELECT")

            self._press_item = None
            self._press_pos = None

        super().mouseReleaseEvent(event)
