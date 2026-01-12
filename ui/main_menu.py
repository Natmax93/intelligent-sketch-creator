"""
Fenêtre d'accueil.

Responsabilité :
- proposer à l'utilisateur de créer un nouveau projet (et plus tard : ouvrir un projet existant)
- ouvrir la fenêtre d'éditeur quand on clique sur "Nouveau dessin"
"""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from ui.editor import EditorWindow


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu - Prototype HAII")

        # Widget racine (conteneur principal)
        root = QWidget()

        # Layout vertical : empile les widgets de haut en bas
        layout = QVBoxLayout(root)

        # Bouton "Nouveau dessin"
        btn_new = QPushButton("Nouveau dessin")
        btn_new.clicked.connect(self.open_editor)  # signal -> slot
        layout.addWidget(btn_new)

        # Place le widget racine au centre du QMainWindow
        self.setCentralWidget(root)

        # Référence conservée pour éviter que Python détruisse l'éditeur (GC)
        self._editor = None

    def open_editor(self):
        """
        Ouvre l'éditeur puis ferme le menu.
        """
        self._editor = EditorWindow()
        self._editor.show()
        self.close()
