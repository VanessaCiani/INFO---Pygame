# Il timer — misurare e visualizzare il tempo

## Indice

1. [Il tempo in un programma interattivo](#il-tempo-in-un-programma-interattivo)
2. [time.time() e i timestamp](#timetime-e-i-timestamp)
3. [Tempo trascorso e tempo rimanente](#tempo-trascorso-e-tempo-rimanente)
4. [Perché non usare il contatore di frame](#perché-non-usare-il-contatore-di-frame)
5. [Analisi del codice](#analisi-del-codice)
   - [Le funzioni del timer](#le-funzioni-del-timer)
   - [La barra del timer](#la-barra-del-timer)
   - [Il testo e la pallina](#il-testo-e-la-pallina)
6. [Cosa devi implementare](#cosa-devi-implementare)
7. [Domande di comprensione](#domande-di-comprensione)
8. [Esperimenti guidati](#esperimenti-guidati)

---

## Il tempo in un programma interattivo

Nelle tappe precedenti il programma non aveva memoria del tempo: ogni frame era identico al precedente dal punto di vista della logica. Aggiungere un timer significa introdurre un concetto nuovo — lo **stato che cambia in funzione del tempo reale**, non solo degli input dell'utente.

Questo è il meccanismo alla base di quasi ogni gioco: round a tempo, power-up che scadono, animazioni con durata fissa, ritardi tra un'azione e l'altra.

---

## time.time() e i timestamp

Il modulo `time` della libreria standard Python fornisce la funzione `time.time()`, che restituisce i secondi trascorsi dall'**epoca Unix** (1 gennaio 1970, mezzanotte UTC) come numero in virgola mobile.

```python
import time

t = time.time()
print(t)   # qualcosa come 1718023456.342
```

Il valore assoluto non ci interessa. Quello che ci interessa è la **differenza** tra due chiamate:

```python
inizio = time.time()
# ... dopo un po' ...
trascorso = time.time() - inizio   # secondi trascorsi, es. 3.7
```

Questa differenza è indipendente dalla velocità del computer e dal numero di frame: misura il tempo reale dell'orologio da parete.

---

## Tempo trascorso e tempo rimanente

Date queste due grandezze, tutto il resto si ricava:

```
trascorso  = time.time() - start_time
rimanente  = max(0.0, duration - trascorso)
scaduto    = trascorso >= duration
```

`max(0.0, ...)` impedisce che il rimanente diventi negativo quando il tempo è già esaurito —senza questo controllo la barra potrebbe avere larghezza negativa, con risultati imprevedibili.

---

## Perché non usare il contatore di frame

Un approccio alternativo sarebbe contare i frame e dividere per i FPS:

```python
frame_count += 1
trascorso = frame_count / FPS   # SBAGLIATO in generale
```

Questo funziona solo se il loop gira esattamente a `FPS` frame al secondo, il che non è garantito. Se il computer è lento, il loop rallenta, i frame si accumulano più lentamente e il timer risulta **più lento dell'orologio reale**.

`time.time()` è sempre sincronizzato con l'orologio di sistema, indipendentemente dalla velocità del loop. È la scelta corretta per qualsiasi misurazione temporale.

---

## Analisi del codice

### Le funzioni del timer

Il timer è suddiviso in quattro funzioni con responsabilità ben separate:

```
time_elapsed()     →  quanto tempo è passato?
time_remaining()   →  quanto tempo manca?
is_expired()       →  il tempo è scaduto?
bar_fill_width()   →  quanti pixel deve avere la barra?
```

Questa separazione ha un vantaggio pratico: ogni funzione è piccola, testabile e riutilizzabile. `bar_fill_width()` in particolare non sa niente di Pygame —riceve numeri, restituisce un numero.

**Calcolo della larghezza della barra:**

```python
ratio    = remaining / duration     # valore tra 0.0 e 1.0
fill_w   = int(ratio * bar_width)   # pixel proporzionali
```

Con `remaining=7`, `duration=10`, `bar_width=700`:

```
ratio  = 7 / 10 = 0.7
fill_w = int(0.7 * 700) = 490 pixel
```

---

### La barra del timer

La barra è composta da **due rettangoli sovrapposti**: prima si disegna lo sfondo (sempre pieno), poi sopra il riempimento (proporzionale al tempo). L'ordine è importante: chi viene disegnato dopo copre chi è stato disegnato prima.

```
┌─────────────────────────────────────────┐  ← sfondo (BAR_BG_COLOR)
├─────────────────────┐                   │
│  riempimento        │                   │  ← fill (BAR_FG_COLOR)
└─────────────────────┴───────────────────┘
         ↑                      ↑
    fill_width             parte vuota
```

```python
# sfondo
pygame.draw.rect(surface, BAR_BG_COLOR,
                 pygame.Rect(BAR_X, BAR_Y, BAR_W, BAR_H),
                 border_radius=6)

# riempimento
fill_w = bar_fill_width(remaining, duration, BAR_W)
if fill_w > 0:
    pygame.draw.rect(surface, BAR_FG_COLOR,
                     pygame.Rect(BAR_X, BAR_Y, fill_w, BAR_H),
                     border_radius=6)
```

Notare il controllo `if fill_w > 0`: `pygame.draw.rect` con larghezza zero non causa errori, ma disegnare un rettangolo vuoto è inutile.

---

### Il testo e la pallina

**Centrare il testo orizzontalmente:**

```python
surf = font.render(testo, True, colore)
rect = surf.get_rect(centerx=SCREEN_W // 2, top=y)
surface.blit(surf, rect)
```

`get_rect()` accetta argomenti opzionali che posizionano il rettangolo: `centerx` imposta il centro orizzontale, `top` imposta il bordo superiore. È più comodo che calcolare manualmente `x = SCREEN_W // 2 - surf.get_width() // 2`.

**Stato della pallina:**

La pallina ha due possibili stati: attiva (colore normale) e scaduta (colore grigio). La funzione `draw_ball()` riceve il flag `expired` e sceglie il colore di conseguenza. È un pattern che ritroverai spesso: separare la logica di stato (`is_expired`) dal rendering (`draw_ball`).

---

## Cosa devi implementare

**Funzioni logiche** (niente Pygame, solo aritmetica):

1. `time_elapsed(start)` — differenza tra `time.time()` e `start`.
2. `time_remaining(start, duration)` — usa `time_elapsed()` e impedisci valori negativi con `max()`.
3. `is_expired(start, duration)` — una riga: confronta `time_elapsed()` con `duration`.
4. `bar_fill_width(remaining, duration, bar_width)` — calcola il rapporto e moltiplica per `bar_width`. Usa `int()` per convertire e `max(0, min(...))` per i limiti.

**Funzioni di disegno** (Pygame):

5. `draw_timer_bar(surface, remaining, duration)` — due rettangoli sovrapposti. Usa `bar_fill_width()` per la larghezza del riempimento.
6. `draw_timer_text(surface, remaining, expired)` — se `expired` è `False` mostra il numero (con `font_medium`), altrimenti mostra «Tempo scaduto!» (con `font_large`). Centra orizzontalmente con `get_rect(centerx=...)`.
7. `draw_ball(surface, x, y, expired)` — sceglie il colore in base a `expired` e disegna il cerchio.

**Ordine consigliato:** implementa prima le quattro funzioni logiche (sono testabili aggiungendo dei `print`), poi le tre funzioni di disegno.

---

## Domande di comprensione

1. Cosa restituisce `time.time()`? Il valore è utile da solo oppure solo in differenza?
2. Perché usiamo `max(0, ...)` nel calcolo del tempo rimanente?
3. Se il loop gira a 30 FPS invece di 60, il timer cambia comportamento? Perché?
4. Cosa succede a `bar_fill_width()` se `remaining` è già 0? E se fosse negativo senza il `max()`?
5. In `draw_timer_bar()`, perché si disegna prima lo sfondo e poi il riempimento e non viceversa?
6. Quale sarebbe il problema di usare `frame_count / FPS` come misura del tempo?

---

## Esperimenti guidati

**Esperimento 1 — Colore della barra dinamico**
Fai cambiare il colore del riempimento in base al tempo rimanente: verde quando è abbondante, giallo a metà, rosso quasi a zero.

```python
if remaining > duration * 0.6:
    colore = (80, 200, 80)    # verde
elif remaining > duration * 0.3:
    colore = (220, 200, 80)   # giallo
else:
    colore = (220, 80, 80)    # rosso
```

**Esperimento 2 — Riavvio**
Aggiungi la gestione del tasto `R`: quando viene premuto, reimposta `start_time = time.time()` per riavviare il conto alla rovescia.

**Esperimento 3 — Durata configurabile**
Prima che il timer parta, premi ↑ per aumentare la durata di 5 secondi e ↓ per diminuirla (minimo 5 secondi). Mostra la durata scelta a schermo. Il timer parte quando premi Spazio.

**Esperimento 4 — Timer che conta in avanti (stopwatch)**
Invece di un conto alla rovescia, mostra il tempo trascorso che cresce. Premi `Spazio` per fermarlo e riprenderlo (pausa).

---