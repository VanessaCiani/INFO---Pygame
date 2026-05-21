import math
import pygame
import sys
from model.game_model import GameModel
from view.game_view import GameView, hole_center, HOLE_RADIUS, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_ROWS, GRID_COLS


class GameController:
    def __init__(self):
        #Inizializza i moduli di Pygame
        pygame.init()
        
        #Configura la finestra e il clock di sistema
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Whack-a-Mole — Step 1")
        self.clock = pygame.time.Clock()
        
        #Inizializza Model e View aggiornando dinamicamente il numero di buchi totali
        self.model = GameModel()
        self.model.NUM_HOLES = GRID_ROWS * GRID_COLS
        self.model.holes = [self.model.holes[0].__class__() for _ in range(self.model.NUM_HOLES)]
        
        self.view = GameView(self.screen)
        self.running = True

    def run(self):
        """Loop principale del gioco."""
        while self.running:
            #Gestione degli Eventi (Input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Cattura la posizione (x, y) del clic del mouse
                    self._handle_click(event.pos)
            
            #Aggiornamento Grafico (Output)
            self.view.draw(self.model)
            
            #Controlla il framerate (fissato a 60 FPS)
            self.clock.tick(60)
            
        #Chiusura pulita dell'applicazione
        pygame.quit()
        sys.exit()

    def _handle_click(self, pos):
        """Trova se un buco è stato cliccato e notifica il model."""
        hole_index = self._hole_at(pos)
        if hole_index is not None:
            self.model.toggle_hole(hole_index)

    def _hole_at(self, pos):
        """Verifica se la posizione del clic è all'interno di un cerchio."""
        for index in range(len(self.model.holes)):
            cx, cy = hole_center(index)
            #Calcola la distanza euclidea tra il mouse (pos) e il centro del cerchio (cx, cy)
            distance = math.hypot(pos[0] - cx, pos[1] - cy)
            
            #Se la distanza è minore del raggio, il punto è dentro il cerchio
            if distance <= HOLE_RADIUS:
                return index
        return None