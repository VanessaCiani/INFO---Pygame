#!/usr/bin/env python3

import pygame
import sys

# ------------------------------------------------------------------ #
# COSTANTI                                                             #
# Definite in cima al file per trovarle e modificarle facilmente.     #
# ------------------------------------------------------------------ #

SCREEN_W  = 800   # larghezza finestra in pixel
SCREEN_H  = 600   # altezza finestra in pixel
FPS       = 60    # fotogrammi al secondo

BALL_RADIUS  = 30
BALL_COLOR   = (220,  80,  80)   # rosso
BALL_SPEED_X =  5   # pixel per frame sull'asse orizzontale
BALL_SPEED_Y =  4   # pixel per frame sull'asse verticale

BG_COLOR   = ( 30,  30,  30)   # grigio scuro
TEXT_COLOR = (200, 200, 200)


# ------------------------------------------------------------------ #
# INIZIALIZZAZIONE                                                     #
# ------------------------------------------------------------------ #

pygame.init()

# Creiamo la finestra: display.set_mode restituisce la "surface"
# principale, cioè la tela su cui disegniamo tutto.
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Pallina che rimbalza")

# Clock: ci serve per limitare il loop a FPS fotogrammi al secondo.
# Senza di esso il programma girerebbe il più veloce possibile,
# consumando CPU inutilmente e rendendo la velocità dipendente
# dall'hardware.
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)


# ------------------------------------------------------------------ #
# STATO INIZIALE DELLA PALLINA                                       #
# Lo stato è tutto ciò che può cambiare durante il gioco.            #
# Per ora usiamo semplici variabili; più avanti useremo una classe.  #
# ------------------------------------------------------------------ #

ball_x = SCREEN_W // 2   # posizione centrale orizzontale
ball_y = SCREEN_H // 2   # posizione centrale verticale
vel_x  = BALL_SPEED_X    # velocità orizzontale (pixel/frame)
vel_y  = BALL_SPEED_Y    # velocità verticale   (pixel/frame)

frame_count = 0   # contiamo i fotogrammi per mostrarlo a schermo


# ------------------------------------------------------------------ #
# LOOP PRINCIPALE                                                    #
#                                                                    #
# Struttura di ogni iterazione (fotogramma):                         #
#   1. EVENTI   — cosa ha fatto l'utente?                            #
#   2. AGGIORNA — sposta la pallina, controlla i bordi               #
#   3. DISEGNA  — ridisegna tutto da zero                            #
#   4. FLIP     — mostra il fotogramma completato                    #
# ------------------------------------------------------------------ #

running = True

while running:
    
    # ---- 1. EVENTI ------------------------------------------------ #
    # pygame.event.get() restituisce tutti gli eventi avvenuti
    # dall'ultima iterazione (tasti, clic, chiusura finestra...).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # L'utente ha cliccato la X della finestra
            running = False
            
    # ---- 2. AGGIORNA ---------------------------------------------- #
            
    # Sposta la pallina aggiungendo la velocità alla posizione
    ball_x += vel_x
    ball_y += vel_y
    
    # Rimbalzo sul bordo destro e sinistro
    # Usiamo BALL_RADIUS perché la posizione (ball_x, ball_y)
    # indica il CENTRO della pallina, non il bordo.
    if ball_x + BALL_RADIUS >= SCREEN_W:
        ball_x = SCREEN_W - BALL_RADIUS   # correzione: rimetti dentro
        vel_x  = -vel_x                    # inverti la direzione
    if ball_x - BALL_RADIUS <= 0:
        ball_x = BALL_RADIUS
        vel_x  = -vel_x
        
    # Rimbalzo sul bordo inferiore e superiore
    if ball_y + BALL_RADIUS >= SCREEN_H:
        ball_y = SCREEN_H - BALL_RADIUS
        vel_y  = -vel_y
    if ball_y - BALL_RADIUS <= 0:
        ball_y = BALL_RADIUS
        vel_y  = -vel_y
        
    frame_count += 1
    
    # ---- 3. DISEGNA ----------------------------------------------- #
    
    # IMPORTANTE: riempire lo sfondo PRIMA di disegnare tutto il resto.
    # Se non lo facciamo, ogni fotogramma si sovrappone al precedente
    # e vediamo una scia invece di una pallina in movimento.
    screen.fill(BG_COLOR)
    
    # Disegna la pallina: cerchio pieno (width=0 significa pieno)
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)
    
    # HUD: informazioni utili durante lo sviluppo
    info = font.render(
        f"pos: ({ball_x}, {ball_y})   vel: ({vel_x}, {vel_y})   frame: {frame_count}",
        True,
        TEXT_COLOR
    )
    screen.blit(info, (10, 10))
    
    # ---- 4. FLIP -------------------------------------------------- #
    # display.flip() scambia il buffer nascosto con quello visibile.
    # Senza questo niente appare sullo schermo.
    pygame.display.flip()
    
    # Aspetta il tempo necessario per restare a FPS fotogrammi/secondo
    clock.tick(FPS)
    
    
# ------------------------------------------------------------------ #
# USCITA PULITA                                                        #
# ------------------------------------------------------------------ #
    
pygame.quit()
sys.exit()
