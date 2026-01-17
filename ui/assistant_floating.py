# ui/assistant_floating.py
from PySide6.QtWidgets import QToolButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon


class FloatingAssistantButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        size = 64  # diamètre (à ajuster)
        self.setFixedSize(size, size)

        # Pas de texte, uniquement l'icône
        self.setText("")
        self.setToolTip("Assistant")
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Charge ton image (chemin relatif au dossier d'exécution)
        pm = QPixmap("assets/logo_assistant.png")

        # Optionnel : si l'image n'est pas trouvée, tu le verras car pm sera null.
        # (Tu peux ajouter un fallback si tu veux.)
        self.setIcon(QIcon(pm))
        self.setIconSize(QSize(size - 12, size - 12))  # marge interne

        # Style rond + léger contour
        self.setStyleSheet(
            f"""
            QToolButton {{
                border: 3px solid #ff7a00;   /* orange */
                border-radius: {size // 2}px;
                background: rgba(255, 255, 255, 220);
                padding: 6px;
            }}
            QToolButton:hover {{
                background: rgba(245, 245, 245, 240);
                border: 3px solid #ff8c1a;   /* orange un peu plus clair */
            }}
            QToolButton:pressed {{
                background: rgba(230, 230, 230, 240);
                border: 3px solid #e66a00;   /* orange plus foncé */
            }}
        """
        )
