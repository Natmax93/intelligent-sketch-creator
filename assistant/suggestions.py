"""
Catalogue de suggestions (templates).

Responsabilité :
- décrire les suggestions disponibles
- fournir une méthode qui créera des QGraphicsItem
  (pour l'instant : placeholder)
"""


class Suggestion:
    def __init__(self, label: str):
        # Nom affiché dans l'UI
        self.label = label

    def create_items(self):
        """
        Retournera plus tard une liste de QGraphicsItem.
        Exemple futur :
            return [QGraphicsRectItem(...), QGraphicsEllipseItem(...)]
        """
        return []


def list_suggestions(category: str):
    """
    Retourne la liste de Suggestion d'une catégorie.
    category pourrait être : "Tour", "Porte", "Mur"
    """
    return []
