# Consegna Esercizio: ball.py
## Risposte alle domande di comprensione

**1. Cosa succede se rimuovi screen.fill(BG_COLOR)? Perché?**
Se tolgo il comando fill, la pallina lascia una scia colorata che riempie lo schermo man mano che si muove. 

**2. Cosa succede se rimuovi pygame.display.flip()?**
Lo schermo rimane bloccato o nero. E non ci viene mostrato più nessun disegno.

**3. Se BALL_RADIUS = 30 e SCREEN_W = 800, qual è il valore massimo che ball_x può raggiungere prima del rimbalzo?**
Il valore massimo è 770. Dobbiamo semplicemente andare a togliere il raggio (30) dalla larghezza totale (800) per capire quando il bordo tocca il muro.

**4. La pallina si muove di 5 pixel per frame a 60 FPS. Quanti pixel percorre in un secondo? E in 10 secondi?**
In un secondo fa 300 pixel (5 pixel * 60 frame). In 10 secondi invece ne percorre 3000.

**5. Cosa succede se imposti vel_x = 0? E se imposti vel_x = vel_y = 0?**
Se metto vel_x a 0, la pallina si muove solo in verticale. Se le azzero entrambe, la pallina sta ferma al centro e non succede nulla.

**6. Perché correggiamo la posizione (ball_x = SCREEN_W - BALL_RADIUS) oltre a invertire la velocità? Cosa succederebbe senza la correzione?**
Serve a "staccare" la pallina dal muro. Senza questa riga, la pallina potrebbe compenetrarsi col bordo e il codice continuerebbe a invertire la velocità ogni millisecondo, facendola vibrare sul posto invece di farla rimbalzare via.

---

## Resoconto Esperimenti
**Esperimento 1 — Velocità**
Ho provato a cambiare i valori: se le velocità X e Y sono uguali, la traiettoria è una diagonale perfetta a 45 gradi. Se una è molto più alta dell'altra, la pallina si muove in modo "schiacciato" (tipo un sasso che rimbalza sull'acqua).

**Esperimento 2 — Dimensione**
Cambiando il raggio, i rimbalzi si adattano da soli perché usiamo la variabile BALL_RADIUS nei calcoli. Se però metto un raggio troppo grande, la pallina fa fatica a muoversi perché tocca i bordi quasi subito.

**Esperimento 3 — Colore dinamico**
Ho aggiunto il modulo random e messo il cambio colore dentro gli "if" del rimbalzo. Adesso la pallina cambia colore ogni volta che urta una parete. Esteticamente è molto meglio e si capisce subito quando avviene il contatto.

**Esperimento 4 — Gravità**
Aggiungendo la gravità alla velocità Y, il movimento diventa curvo (una parabola). La pallina cade verso il basso e accelera, proprio come farebbe una palla vera se la lanciassi in una stanza.