class Hole:
    """Rappresenta un singolo buco della griglia e il suo stato."""
    def __init__(self):
        #Inizialmente il buco non è attivo (grigio)
        self.is_active = False

    def toggle(self):
        """Inverte lo stato del buco."""
        self.is_active = not self.is_active


class GameModel:
    """Gestisce lo stato complessivo della griglia di gioco."""
    NUM_HOLES = 9

    def __init__(self):
        #Crea una lista lineare contenente 9 oggetti Hole
        self.holes = [Hole() for _ in range(self.NUM_HOLES)]

    def toggle_hole(self, index):
        """Inverte lo stato del buco all'indice specificato se valido."""
        if 0 <= index < len(self.holes):
            self.holes[index].toggle()