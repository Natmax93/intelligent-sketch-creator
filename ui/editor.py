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
from logs.logger import EventLogger


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur - Prototype HAII")

        # --- Logger ---
        self.logger = EventLogger("logs/events.csv")

        # --- Scene/View ---
        # La scène contient les items (formes) ; la vue les affiche et gère le zoom/scroll si besoin
        self.scene = DrawingScene(logger=self.logger)
        self.view = QGraphicsView(self.scene)

        # Permet de sélectionner un item par clic (comportement standard)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)

        # Dans un QMainWindow, le widget central est la "zone principale"
        self.setCentralWidget(self.view)

        # --- Toolbar ---
        toolbar = QToolBar("Outils")
        self.addToolBar(toolbar)

        # Action : mode Sélection
        act_select = QAction("Sélection", self)
        act_select.triggered.connect(
            lambda: (
                self.scene.set_tool(Tool.SELECT),
                self.view.setDragMode(QGraphicsView.RubberBandDrag),
            )
        )
        toolbar.addAction(act_select)

        # Action : mode Stylo
        act_pen = QAction("Stylo", self)
        act_pen.triggered.connect(lambda: self.scene.set_tool(Tool.PEN))
        toolbar.addAction(act_pen)

        # Action : mode Gomme
        act_eraser = QAction("Gomme", self)
        act_eraser.triggered.connect(
            lambda: (
                self.scene.set_tool(Tool.ERASER),
                self.view.setDragMode(QGraphicsView.NoDrag),
            )
        )
        toolbar.addAction(act_eraser)

        # Action : mode Trait
        act_line = QAction("Trait", self)
        act_line.triggered.connect(
            lambda: (
                self.scene.set_tool(Tool.LINE),
                self.view.setDragMode(QGraphicsView.NoDrag),
            )
        )
        toolbar.addAction(act_line)

        # Action : mode Rectangle
        act_rect = QAction("Rectangle", self)
        act_rect.triggered.connect(
            lambda: (
                self.scene.set_tool(Tool.RECT),
                self.view.setDragMode(QGraphicsView.NoDrag),
            )
        )
        toolbar.addAction(act_rect)

        # Action : mode Ellipse
        act_ellipse = QAction("Ellipse", self)
        act_ellipse.triggered.connect(
            lambda: (
                self.scene.set_tool(Tool.ELLIPSE),
                self.view.setDragMode(QGraphicsView.NoDrag),
            )
        )
        toolbar.addAction(act_ellipse)

        # TODO ce code ne sert à rien : à effacer...

        # act_select.triggered.connect(
        #     lambda: (
        #         self.scene.set_tool(Tool.SELECT),
        #         self.view.setDragMode(QGraphicsView.RubberBandDrag),
        #     )
        # )

        # act_pen.triggered.connect(
        #     lambda: (
        #         self.scene.set_tool(Tool.PEN),
        #         self.view.setDragMode(QGraphicsView.NoDrag),
        #     )
        # )

        # --- Assistant dock ---
        dock = QDockWidget("Assistant", self)
        dock.setWidget(AssistantPanel())

        # Ajoute le dock à droite (ou gauche) de la fenêtre
        # Qt.RightDockWidgetArea / Qt.LeftDockWidgetArea sont des enums
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
