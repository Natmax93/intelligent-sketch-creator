"""
Fenêtre principale d'édition.

Responsabilité :
- afficher la zone de dessin (QGraphicsView + QGraphicsScene)
- fournir une toolbar pour changer d'outil
- afficher un panneau assistant sous forme de DockWidget
"""

from PySide6.QtWidgets import QMainWindow, QToolBar, QGraphicsView, QDockWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt  # IMPORTANT : DockWidgetArea est ici

from drawing.scene import DrawingScene
from ui.assistant_panel import AssistantPanel
from drawing.tools import Tool


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur - Prototype HAII")

        # --- Scene/View ---
        # La scène contient les items (formes) ; la vue les affiche et gère le zoom/scroll si besoin
        self.scene = DrawingScene()
        self.view = QGraphicsView(self.scene)

        # Dans un QMainWindow, le widget central est la "zone principale"
        self.setCentralWidget(self.view)

        # --- Toolbar ---
        toolbar = QToolBar("Outils")
        self.addToolBar(toolbar)

        # Action : mode Sélection
        act_select = QAction("Sélection", self)
        act_select.triggered.connect(lambda: self.scene.set_tool(Tool.SELECT))
        toolbar.addAction(act_select)

        # Action : mode Stylo
        act_pen = QAction("Stylo", self)
        act_pen.triggered.connect(lambda: self.scene.set_tool(Tool.PEN))
        toolbar.addAction(act_pen)

        # --- Assistant dock ---
        dock = QDockWidget("Assistant", self)
        dock.setWidget(AssistantPanel())

        # Ajoute le dock à droite (ou gauche) de la fenêtre
        # Qt.RightDockWidgetArea / Qt.LeftDockWidgetArea sont des enums
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
