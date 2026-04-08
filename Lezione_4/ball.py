import pygame

BALL_RADIUS  = 12
BALL_COLOR   = (220, 220,  80)
BALL_SPEED_X =  4
BALL_SPEED_Y = -5   # negativo: parte verso l'alto


class Ball:
    """
    Rappresenta la pallina: posizione, velocità e comportamento.
    """

    def __init__(self, x: int, y: int):
        self.x     = x
        self.y     = y
        self.vel_x = BALL_SPEED_X
        self.vel_y = BALL_SPEED_Y
        self.alive = True

    def update(self, screen_w: int, screen_h: int):
        """
        Aggiorna posizione e gestisce i rimbalzi sui bordi dello schermo.
        """
        # 1. Aggiornamento posizione
        self.x += self.vel_x
        self.y += self.vel_y

        # 2. Rimbalzo bordo sinistro
        if self.x - BALL_RADIUS <= 0:
            self.x = BALL_RADIUS
            self.vel_x = -self.vel_x

        # 3. Rimbalzo bordo destro
        if self.x + BALL_RADIUS >= screen_w:
            self.x = screen_w - BALL_RADIUS
            self.vel_x = -self.vel_x

        # 4. Rimbalzo bordo superiore
        if self.y - BALL_RADIUS <= 0:
            self.y = BALL_RADIUS
            self.vel_y = -self.vel_y

        # 5. Controllo bordo inferiore (caduta)
        if self.y - BALL_RADIUS >= screen_h:
            self.alive = False

    def bounce_off_paddle(self, paddle_rect: pygame.Rect):
        """
        Gestisce il rimbalzo dinamico sulla paddle.
        """
        # Crea il Rect della pallina per la collisione
        ball_rect = pygame.Rect(self.x - BALL_RADIUS, 
                                self.y - BALL_RADIUS, 
                                BALL_RADIUS * 2, 
                                BALL_RADIUS * 2)

        # Condizioni: la pallina cade (vel_y > 0) e tocca la paddle
        if self.vel_y > 0 and ball_rect.colliderect(paddle_rect):
            # Inverti direzione verticale
            self.vel_y = -self.vel_y
            
            # Correzione posizione per evitare che la pallina si "incastri" nella paddle
            self.y = paddle_rect.top - BALL_RADIUS
            
            # Effetto angolo basato sul punto di impatto
            offset = self.x - paddle_rect.centerx
            self.vel_x = offset // 10

    def draw(self, surface: pygame.Surface):
        """
        Disegna la pallina sulla superficie specificata.
        """
        pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)