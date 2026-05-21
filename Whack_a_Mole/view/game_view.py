import pygame

#Dimensioni finestra
WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600

#Griglia (Variabili dinamiche per riga e colonna)
GRID_ROWS    = 3
GRID_COLS    = 3
HOLE_RADIUS  = 60
GRID_MARGIN  = 60

#Colori (RGB)
COLOR_BG       = (30, 30, 40)
COLOR_HOLE     = (90, 90, 100)
COLOR_HOLE_ON  = (230, 140, 40)


def hole_center(index):
    """Restituisce le coordinate (x, y) del centro del buco i-esimo."""
    #Calcola la riga e la colonna a partire dall'indice lineare
    row = index // GRID_COLS
    col = index % GRID_COLS
    
    #Calcola lo spazio utile per la griglia escludendo i margini esterni
    available_width = WINDOW_WIDTH - (2 * GRID_MARGIN)
    available_height = WINDOW_HEIGHT - (2 * GRID_MARGIN)
    
    #Calcola la dimensione di una singola cella della griglia
    cell_width = available_width / (GRID_COLS - 1) if GRID_COLS > 1 else available_width
    cell_height = available_height / (GRID_ROWS - 1) if GRID_ROWS > 1 else available_height
    
    #Calcola il centro esatto del cerchio posizionando i punti sulla griglia
    cx = GRID_MARGIN + (col * cell_width)
    cy = GRID_MARGIN + (row * cell_height)
    
    return int(cx), int(cy)


class GameView:
    def __init__(self, screen):
        #Memorizza la superficie dello schermo creata dal controller
        self.screen = screen

    def draw(self, model):
        """Disegna lo sfondo e tutti i buchi in base al loro stato attuale."""
        #Colore di sfondo della finestra
        self.screen.fill(COLOR_BG)
        
        #Itera su tutti i buchi presenti nel model
        for index, hole in enumerate(model.holes):
            #Seleziona il centro del cerchio tramite la funzione pura
            center = hole_center(index)
            
            #Sceglie il colore in base allo stato del buco
            color = COLOR_HOLE_ON if hole.is_active else COLOR_HOLE
            
            #Disegna il cerchio sulla superficie
            pygame.draw.circle(self.screen, color, center, HOLE_RADIUS)
            
        #Aggiorna il display per mostrare le modifiche
        pygame.display.flip()