"""RISPOSTE ALLE DOMANDE CONCETTUALI

1. Perché conviene usare una lista lineare di 9 elementi invece di una matrice 3x3?
   -> Uso una lista da 0 a 8 perché è molto più semplice da gestire nel codice. 
      Posso fare i cicli con un solo 'for' invece di due, e in futuro sarà facilissimo 
      scegliere un buco a caso per far comparire la talpa usando un semplice numero. 
      Se mi servono la riga e la colonna, posso calcolarle al volo con le formule 
      matematiche (divisione intera // e resto %).

2. Se cambio WINDOW_WIDTH a 800, cosa succede ai buchi? Devo modificare hole_center()?
   -> Se allargo la finestra a 800 pixel, i buchi si allontaneranno automaticamente 
      tra di loro in orizzontale, sfruttando il nuovo spazio. Non devo toccare la 
      funzione hole_center() perché calcola già le posizioni in base alla larghezza 
      e all'altezza della finestra. Il layout si adatta da solo.

3. Perché controlliamo MOUSEBUTTONDOWN invece di usare pygame.mouse.get_pressed()?
   -> Uso MOUSEBUTTONDOWN perché questo evento scatta una sola volta quando premo il 
      click (è un singolo impulso). Se usassi get_pressed(), il programma vedrebbe 
      il tasto premuto per tutta la durata del click (che dura diversi frame). 
      Questo farebbe impazzire il cerchio, che continuerebbe a cambiare colore 
      decine di volte al secondo a ogni minimo tocco."""

from controller.game_controller import GameController

if __name__ == "__main__":
    #Avvia l'applicazione inizializzando il Controller
    game = GameController()
    game.run()