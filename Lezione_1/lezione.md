# Pallina che rimbalza — spiegazione completa

## Indice

- [Pallina che rimbalza — spiegazione completa](#pallina-che-rimbalza--spiegazione-completa)
  - [Indice](#indice)
  - [Cos'è Pygame?](#cosè-pygame)
  - [Il loop di gioco](#il-loop-di-gioco)
  - [Il concetto di fotogramma (frame)](#il-concetto-di-fotogramma-frame)
  - [Analisi del codice riga per riga](#analisi-del-codice-riga-per-riga)
    - [Costanti e inizializzazione](#costanti-e-inizializzazione)
    - [Lo stato della pallina](#lo-stato-della-pallina)
    - [Gestione degli eventi](#gestione-degli-eventi)
    - [Aggiornamento della posizione](#aggiornamento-della-posizione)
    - [Rilevamento dei bordi e rimbalzo](#rilevamento-dei-bordi-e-rimbalzo)
    - [Disegno e flip](#disegno-e-flip)
    - [Il clock e i FPS](#il-clock-e-i-fps)
  - [Il sistema di coordinate](#il-sistema-di-coordinate)
  - [Domande di comprensione](#domande-di-comprensione)
  - [Esperimenti guidati](#esperimenti-guidati)

---

## Cos'è Pygame?

Pygame è una libreria Python che fornisce gli strumenti per creare applicazioni grafiche interattive: gestisce la finestra, il disegno di forme e immagini, gli eventi di tastiera e mouse, l'audio. Non è un motore di gioco completo, ma un livello di astrazione sopra SDL (Simple DirectMedia Layer), una libreria scritta in C.

Per installarla:

```bash
pip install pygame
```

---

## Il loop di gioco

La struttura fondamentale di qualsiasi programma interattivo in tempo reale è il **loop di gioco** (*game loop*). È un ciclo `while` che non termina mai finché l'utente non chiude l'applicazione, e che ad ogni iterazione esegue sempre le stesse tre operazioni nell'ordine:

```
┌─────────────────────────────────────┐
│                                     │
│   ┌──────────┐                      │
│   │  EVENTI  │  cosa ha fatto       │
│   │          │  l'utente?           │
│   └────┬─────┘                      │
│        │                            │
│   ┌────▼─────┐                      │
│   │ AGGIORNA │  sposta oggetti,     │
│   │          │  controlla collisioni│
│   └────┬─────┘                      │
│        │                            │
│   ┌────▼─────┐                      │
│   │ DISEGNA  │  ridisegna tutto     │
│   │          │  da zero             │
│   └────┬─────┘                      │
│        │                            │
│        └──────── ripeti ────────────┤
│                                     │
└─────────────────────────────────────┘
```

Questo schema si chiama anche **EVA** (Events – Update – Draw) o **UDR** (Update – Draw – Repeat). Qualunque sia il nome, il principio è identico: ogni fotogramma è una fotografia immobile; l'illusione del movimento nasce dalla successione rapida di fotografie leggermente diverse.

---

## Il concetto di fotogramma (frame)

Un **fotogramma** (*frame*) è una singola iterazione del loop. Se il loop gira 60 volte al secondo, il programma mostra 60 fotogrammi al secondo (**60 FPS**).

Questo ha una conseguenza importante: la velocità di un oggetto si misura in **pixel per frame**, non in pixel al secondo. Se la pallina si sposta di 5 pixel ad ogni frame e il programma gira a 60 FPS, la pallina percorre 300 pixel al secondo. Se il loop rallenta (perché la CPU è occupata), la pallina rallenta.

Per questo usiamo `clock.tick(FPS)`: impone un limite superiore al numero di iterazioni al secondo, rendendo la velocità prevedibile.

---

## Analisi del codice riga per riga

### Costanti e inizializzazione

```python
SCREEN_W  = 800
SCREEN_H  = 600
FPS       = 60
```

Le costanti sono scritte in maiuscolo per convenzione (PEP 8). Raccoglierle in cima al file ha un vantaggio pratico: per cambiare la dimensione della finestra o la velocità della pallina basta modificare un solo punto.

```python
pygame.init()
```

`pygame.init()` inizializza tutti i sottosistemi di Pygame (grafica, audio, eventi). Va chiamata una sola volta all'inizio, prima di qualsiasi altra funzione Pygame.

```python
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
```

Crea la finestra e restituisce la **surface** principale. Una `Surface` è un rettangolo di pixel in memoria su cui si può disegnare. Tutta la grafica passa per questo oggetto.

```python
clock = pygame.time.Clock()
```

Oggetto che gestisce il tempo. Il suo metodo `tick(fps)` mette il programma in pausa per il tempo necessario affinché il loop non superi il limite di FPS indicato.

---

### Lo stato della pallina

```python
ball_x = SCREEN_W // 2
ball_y = SCREEN_H // 2
vel_x  = BALL_SPEED_X
vel_y  = BALL_SPEED_Y
```

Lo **stato** del programma è l'insieme delle variabili che possono cambiare durante l'esecuzione. Qui lo stato è minimo: posizione e velocità della pallina.

`ball_x` e `ball_y` indicano il **centro** della pallina. È una scelta convenzionale in Pygame: `pygame.draw.circle` accetta il centro, non il bordo superiore sinistro.

`vel_x` e `vel_y` sono le **componenti del vettore velocità**. Ad ogni frame si sommano alla posizione. Se `vel_x = 5`, la pallina si sposta di 5 pixel verso destra ad ogni fotogramma.

---

### Gestione degli eventi

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
```

`pygame.event.get()` svuota la coda degli eventi accumulati dall'ultima iterazione e li restituisce come lista. Se non chiamassimo questa funzione ogni frame, la coda si riempirebbe e il programma sembrerebbe bloccato.

`pygame.QUIT` è l'evento generato quando l'utente clicca la X della finestra. Impostare `running = False` fa uscire dal loop al prossimo controllo della condizione `while running`.

---

### Aggiornamento della posizione

```python
ball_x += vel_x
ball_y += vel_y
```

Aggiornamento banale ma fondamentale: ad ogni frame la posizione aumenta della velocità. È il modello più semplice di moto uniforme discreto.

---

### Rilevamento dei bordi e rimbalzo

```python
if ball_x + BALL_RADIUS >= SCREEN_W:
    ball_x = SCREEN_W - BALL_RADIUS
    vel_x  = -vel_x
```

Il controllo del bordo destro ha **due** istruzioni, non una sola:

1. **Correzione della posizione** (`ball_x = SCREEN_W - BALL_RADIUS`): se non correggessimo, la pallina potrebbe essere già uscita parzialmente dallo schermo nel fotogramma precedente. La correzione la riporta esattamente sul bordo.

2. **Inversione della velocità** (`vel_x = -vel_x`): moltiplicare per −1 inverte la direzione. Se stava andando a destra (+5), ora va a sinistra (−5).

Perché `ball_x + BALL_RADIUS` e non solo `ball_x`? Perché `ball_x` è il **centro**: il bordo destro della pallina si trova a `ball_x + BALL_RADIUS`. Se controllassimo solo il centro, la pallina uscirebbe di metà prima di rimbalzare.

```
         ball_x
           │
     ◄─────┼─────►  BALL_RADIUS
           │
     ┌─────●─────┐
     │           │   ← la pallina occupa spazio
     └───────────┘
                 │
           bordo = ball_x + BALL_RADIUS
```

---

### Disegno e flip

```python
screen.fill(BG_COLOR)
pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)
pygame.display.flip()
```

**Perché `screen.fill()` prima di tutto?**

Pygame non «cancella» automaticamente il fotogramma precedente. Se non riempiamo lo sfondo, ogni nuovo cerchio si sovrappone ai precedenti e vediamo una scia. Riempire lo sfondo ad ogni frame è il modo corretto per ottenere l'illusione del movimento.

**`pygame.draw.circle`** accetta:
- la surface su cui disegnare
- il colore (tupla RGB)
- il centro (tupla di interi)
- il raggio

Con `width=0` (default) disegna un cerchio pieno. Con `width > 0` disegna solo il contorno.

**`pygame.display.flip()`** completa il fotogramma. Pygame usa il **double buffering**: si disegna su un buffer nascosto, e `flip()` lo scambia con quello visibile. Senza questa chiamata, lo schermo non si aggiorna mai.

---

### Il clock e i FPS

```python
clock.tick(FPS)
```

Va chiamato **alla fine** di ogni iterazione. Misura quanto tempo è trascorso dall'ultima chiamata e, se il frame è stato più veloce di `1/FPS` secondi, mette il programma in pausa per il tempo rimanente.

Effetto: il loop non gira mai più veloce di `FPS` iterazioni al secondo. Può girare più lento se il calcolo richiede troppo tempo, ma nel nostro caso è impossibile.

---

## Il sistema di coordinate

In Pygame (e nella grafica 2D in generale) il sistema di coordinate è diverso da quello cartesiano:

```
(0,0) ──────────────────────► X
  │
  │
  │
  │
  ▼
  Y
```

- L'origine `(0, 0)` è nell'angolo **superiore sinistro**.
- X cresce verso destra.
- Y cresce verso il **basso** (non verso l'alto come in matematica).

Questo significa che `vel_y = +4` sposta la pallina **verso il basso**, e `vel_y = -4` la sposta verso l'alto.

---

## Domande di comprensione

1. Cosa succede se rimuovi `screen.fill(BG_COLOR)`? Perché?
2. Cosa succede se rimuovi `pygame.display.flip()`?
3. Se `BALL_RADIUS = 30` e `SCREEN_W = 800`, qual è il valore massimo che `ball_x` può raggiungere prima del rimbalzo?
4. La pallina si muove di 5 pixel per frame a 60 FPS. Quanti pixel percorre in un secondo? E in 10 secondi?
5. Cosa succede se imposti `vel_x = 0`? E se imposti `vel_x = vel_y = 0`?
6. Perché correggiamo la posizione (`ball_x = SCREEN_W - BALL_RADIUS`) oltre a invertire la velocità? Cosa succederebbe senza la correzione?

---

## Esperimenti guidati

Prova a modificare il codice per ottenere i seguenti risultati. Non è necessario capire tutto subito: l'obiettivo è osservare cosa cambia.

**Esperimento 1 — Velocità**
Cambia `BALL_SPEED_X` e `BALL_SPEED_Y`. Cosa succede se sono uguali? Cosa succede se uno è molto più grande dell'altro?

**Esperimento 2 — Dimensione**
Cambia `BALL_RADIUS`. Cosa devi cambiare per far sì che la pallina non esca mai dallo schermo con qualsiasi raggio?

**Esperimento 3 — Colore dinamico**
Fai cambiare il colore della pallina ad ogni rimbalzo. Suggerimento: usa `random.randint(0, 255)` per generare i tre canali RGB.

```python
import random
# all'interno del blocco del rimbalzo:
BALL_COLOR = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
```

**Esperimento 4 — Gravità (per i più curiosi)**
Aggiungi una costante `GRAVITY = 0.3` e ad ogni frame scrivi:

```python
vel_y += GRAVITY
```

Osserva il comportamento. Perché la pallina non rimbalza alla stessa altezza di partenza?