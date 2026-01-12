"""
Point d'entrée de l'application.

Responsabilité :
- créer l'objet QApplication (boucle d'événements Qt)
- afficher la fenêtre d'accueil
- démarrer la boucle principale Qt
"""

from PySide6.QtWidgets import QApplication
import sys

from ui.main_menu import MainMenuWindow


def main():
    # QApplication gère : boucle d'événements, gestion des fenêtres, signaux/slots, etc.
    app = QApplication(sys.argv)

    # On instancie la fenêtre d'accueil.
    w = MainMenuWindow()
    w.show()  # Affiche la fenêtre

    # Lance la boucle d'événements Qt (bloquante).
    # Quand l'app se ferme, exec() renvoie un code de sortie.
    # sys.exit(app.exec())
    app.exec()


if __name__ == "__main__":
    main()
