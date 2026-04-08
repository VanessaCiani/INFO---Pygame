import pygame


PADDLE_W      = 100
PADDLE_H      =  14
PADDLE_COLOR  = ( 80, 180, 220)
PADDLE_SPEED  =   6
PADDLE_Y_OFFSET = 60   # distanza dal bordo inferiore dello schermo


class Paddle:
    """
    Rappresenta la barra controllata dal giocatore.
    Questa classe è già completa: non devi modificarla.

    Attributi:
        rect  -- pygame.Rect che definisce posizione e dimensione
    """

    def __init__(self, screen_w: int, screen_h: int):
        x = screen_w // 2 - PADDLE_W // 2
        y = screen_h - PADDLE_Y_OFFSET
        self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)
        self._screen_w = screen_w

    def update(self, keys: pygame.key.ScancodeWrapper):
        """
        Sposta la paddle in base ai tasti freccia sinistra/destra.
        Si ferma ai bordi dello schermo.
        """
        if keys[pygame.K_LEFT]:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PADDLE_SPEED

        # Blocca ai bordi
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self._screen_w:
            self.rect.right = self._screen_w

    def draw(self, surface: pygame.Surface):
        """Disegna la paddle con angoli arrotondati."""
        
        pygame.draw.rect(surface, PADDLE_COLOR, self.rect, border_radius=6)