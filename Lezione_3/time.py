import pygame
import sys
import time

# ------------------------------------------------------------------ #
# COSTANTI                                                             #
# ------------------------------------------------------------------ #

SCREEN_W = 800
SCREEN_H = 600
FPS      = 60

BALL_RADIUS  = 30
BALL_COLOR   = ( 80, 180, 220)
BALL_EXPIRED = ( 80,  80,  80)   # colore quando il tempo è scaduto

COUNTDOWN    = 10                # durata del conto alla rovescia (secondi)

BG_COLOR     = ( 30,  30,  30)
TEXT_COLOR   = (200, 200, 200)
BAR_BG_COLOR = ( 80,  40,  40)
BAR_FG_COLOR = ( 80, 200,  80)

BAR_X = 50
BAR_Y = 20
BAR_W = SCREEN_W - 100
BAR_H = 24

# ------------------------------------------------------------------ #
# INIZIALIZZAZIONE                                                     #
# ------------------------------------------------------------------ #

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Il timer")
clock  = pygame.time.Clock()
font_large  = pygame.font.SysFont("Arial", 48, bold=True)
font_medium = pygame.font.SysFont("Arial", 28)
font_small  = pygame.font.SysFont("Arial", 20)

# ------------------------------------------------------------------ #
# STATO                                                                #
# ------------------------------------------------------------------ #

ball_x     = SCREEN_W // 2
ball_y     = SCREEN_H // 2

start_time = time.time()

# ------------------------------------------------------------------ #
# FUNZIONI — logica del timer                                          #
# ------------------------------------------------------------------ #

def time_elapsed(start: float) -> float:
    """Restituisce i secondi trascorsi da start fino ad ora."""
    return time.time() - start


def time_remaining(start: float, duration: int) -> float:
    """Restituisce i secondi rimanenti. Non scende sotto lo zero."""
    remaining = duration - time_elapsed(start)
    return max(0.0, remaining)


def is_expired(start: float, duration: int) -> bool:
    """Restituisce True se il tempo è scaduto."""
    return time_elapsed(start) >= duration


def bar_fill_width(remaining: float, duration: int, bar_width: int) -> int:
    """Restituisce la larghezza in pixel proporzionale al tempo rimanente."""
    ratio = remaining / duration
    # Limitiamo il ratio tra 0 e 1 per sicurezza
    ratio = max(0.0, min(1.0, ratio))
    return int(ratio * bar_width)

# ------------------------------------------------------------------ #
# FUNZIONI — disegno                                                   #
# ------------------------------------------------------------------ #

def draw_timer_bar(surface: pygame.Surface,
                   remaining: float, duration: int):
    """Disegna la barra di sfondo e quella di riempimento."""
    # 1. Sfondo della barra
    bg_rect = pygame.Rect(BAR_X, BAR_Y, BAR_W, BAR_H)
    pygame.draw.rect(surface, BAR_BG_COLOR, bg_rect, border_radius=6)
    
    # 2. Riempimento (proporzionale)
    fill_w = bar_fill_width(remaining, duration, BAR_W)
    if fill_w > 0:
        fill_rect = pygame.Rect(BAR_X, BAR_Y, fill_w, BAR_H)
        pygame.draw.rect(surface, BAR_FG_COLOR, fill_rect, border_radius=6)


def draw_timer_text(surface: pygame.Surface,
                    remaining: float, expired: bool):
    """Disegna il countdown o il messaggio di fine tempo."""
    if expired:
        msg = "Tempo scaduto!"
        text_surf = font_large.render(msg, True, (255, 100, 100))
    else:
        # Usiamo ceil per mostrare '1' fino all'ultimo istante
        import math
        msg = str(math.ceil(remaining))
        text_surf = font_medium.render(msg, True, TEXT_COLOR)
        
    text_rect = text_surf.get_rect(centerx=SCREEN_W // 2, top=BAR_Y + BAR_H + 10)
    surface.blit(text_surf, text_rect)


def draw_ball(surface: pygame.Surface,
              x: int, y: int, expired: bool):
    """Disegna la pallina cambiando colore se il tempo è scaduto."""
    color = BALL_EXPIRED if expired else BALL_COLOR
    pygame.draw.circle(surface, color, (x, y), BALL_RADIUS)

# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                      #
# ------------------------------------------------------------------ #

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- 2. AGGIORNA ---------------------------------------------- #
    remaining = time_remaining(start_time, COUNTDOWN)
    expired   = is_expired(start_time, COUNTDOWN)

    # ---- 3. DISEGNA ----------------------------------------------- #
    screen.fill(BG_COLOR)

    draw_timer_bar(screen, remaining, COUNTDOWN)
    draw_timer_text(screen, remaining, expired)
    draw_ball(screen, ball_x, ball_y, expired)

    hint_text = "Osserva la barra e il numero scendere..."
    hint = font_small.render(hint_text, True, TEXT_COLOR)
    screen.blit(hint, hint.get_rect(centerx=SCREEN_W // 2,
                                    bottom=SCREEN_H - 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()