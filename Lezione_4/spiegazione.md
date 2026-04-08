# Breakout: don't drop the ball!

## Indice

- [Breakout: don't drop the ball!](#breakout-dont-drop-the-ball)
  - [Indice](#indice)
  - [Perché le classi?](#perché-le-classi)
  - [La struttura del progetto](#la-struttura-del-progetto)
  - [Anatomia di una classe Pygame](#anatomia-di-una-classe-pygame)
  - [Analisi del codice fornito](#analisi-del-codice-fornito)
    - [La classe Paddle](#la-classe-paddle)
    - [La classe Ball — scheletro](#la-classe-ball--scheletro)
    - [Il main e il loop](#il-main-e-il-loop)
  - [Cosa devi implementare](#cosa-devi-implementare)
  - [Il rimbalzo sulla paddle](#il-rimbalzo-sulla-paddle)
  - [Domande di comprensione](#domande-di-comprensione)
  - [Esperimenti guidati](#esperimenti-guidati)

---

## Perché le classi?

Nelle tappe precedenti la pallina era rappresentata da variabili separate: `ball_x`, `ball_y`, `vel_x`, `vel_y`. Funzionava, ma presentava un problema: quelle variabili non hanno nessun legame esplicito tra loro. Se volessimo aggiungere una seconda pallina dovremmo duplicare tutte le variabili — `ball2_x`, `ball2_y`, e così via.

Con una classe il problema scompare:

```python
ball1 = Ball(200, 300)
ball2 = Ball(400, 300)
```

Ogni istanza ha il suo stato incapsulato. Il loop principale non cambia:

```python
ball1.update(SCREEN_W, SCREEN_H)
ball2.update(SCREEN_W, SCREEN_H)
```

Questa è la motivazione pratica dell'OOP in questo contesto: non è una formalità, ma il modo più naturale di gestire oggetti multipli con stato e comportamento propri.

---

## La struttura del progetto

```
breakout/
├── main.py       ← loop principale, HUD, gestione stati
├── ball.py       ← classe Ball  (da implementare)
├── paddle.py     ← classe Paddle (già fornita)
└── assets/
    └── heart.png ← sprite cuore (da aggiungere tu)
```

Ogni classe sta in un file separato. `main.py` li importa:

```python
from ball   import Ball
from paddle import Paddle
```

Questo è un primo passo verso la separazione delle responsabilità che ritroverai nel pattern MVC.

---

## Anatomia di una classe Pygame

Il pattern che userai da qui in avanti per qualsiasi oggetto di gioco è sempre lo stesso:

```python
class NomeOggetto:

    def __init__(self, ...):
        # inizializza lo stato: posizione, velocità, colore...

    def update(self, ...):
        # aggiorna lo stato: sposta, controlla collisioni...

    def draw(self, surface):
        # disegna sull'oggetto Surface ricevuto come parametro
```

`update()` e `draw()` sono separati di proposito: `update()` cambia i dati, `draw()` li rappresenta visivamente. Non mescolare le due responsabilità — è la stessa logica del pattern MVC.

---

## Analisi del codice fornito

### La classe Paddle

`Paddle` è già completa. Leggila con attenzione prima di scrivere `Ball`: usa la stessa struttura che dovrai implementare.

```python
def __init__(self, screen_w, screen_h):
    x = screen_w // 2 - PADDLE_W // 2   # centrata orizzontalmente
    y = screen_h - PADDLE_Y_OFFSET       # vicina al bordo inferiore
    self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)
```

Notare che `Paddle` usa un `pygame.Rect` come attributo principale. `Rect` è comodo perché tiene insieme x, y, larghezza e altezza, e fornisce attributi calcolati come `rect.centerx`, `rect.top`, `rect.left`, `rect.right`.

```python
def update(self, keys):
    if keys[pygame.K_LEFT]:
        self.rect.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        self.rect.x += PADDLE_SPEED
    # blocca ai bordi con rect.left e rect.right
```

Il metodo riceve `keys` come parametro —non chiama `pygame.key.get_pressed()` al suo interno. Questo è il modo corretto: chi chiama `update()` decide quando e come leggere l'input, la classe non ha dipendenze nascoste.

---

### La classe Ball — scheletro

`Ball` ha tre metodi da implementare:

| Metodo | Responsabilità |
|--------|---------------|
| `update(screen_w, screen_h)` | sposta la pallina, rimbalza sui tre bordi, rileva la caduta |
| `bounce_off_paddle(paddle_rect)` | rileva e gestisce la collisione con la paddle |
| `draw(surface)` | disegna il cerchio |

L'attributo `alive` è il segnale che la pallina è caduta: quando diventa `False`, `main.py` sa che deve sottrarre una vita e ricreare la pallina.

---

### Il main e il loop

`main.py` coordina tutto. La struttura del loop che devi completare è:

```
EVENTI
  └── tasto R → reset_game()

AGGIORNA (solo se non game_over)
  ├── paddle.update(keys)
  ├── ball.update(SCREEN_W, SCREEN_H)
  ├── ball.bounce_off_paddle(paddle.rect)
  └── se ball.alive è False → gestisci perdita vita

DISEGNA
  ├── screen.fill(BG_COLOR)
  ├── draw_hud()
  ├── draw_timer_bar()
  ├── paddle.draw(screen)
  ├── ball.draw(screen)
  └── se game_over → draw_end_screen()
```

`reset_game()` è una funzione che crea da zero tutti gli oggetti di gioco e restituisce una tupla. Permette di riavviare la partita senza duplicare codice.

---

## Cosa devi implementare

**In `ball.py`:**

1. `update(screen_w, screen_h)` — sposta la pallina (`x += vel_x`, `y += vel_y`), rimbalza su sinistra, destra e alto, imposta `alive = False` se supera il bordo inferiore.

2. `bounce_off_paddle(paddle_rect)` — controlla se la pallina (in discesa) collide con la paddle e gestisce il rimbalzo con effetto angolo. Vedi la sezione dedicata qui sotto.

3. `draw(surface)` — disegna il cerchio con `pygame.draw.circle()`.

**In `main.py`:**

4. `draw_hud(surface, remaining, lives)` — testo del countdown centrato in alto, cuori allineati a destra.

5. `draw_timer_bar(surface, remaining, duration)` — barra sottile sotto il testo, stesso schema della tappa 3.

6. `reset_game()` — restituisce `(ball, paddle, start_time, lives)`.

7. **Loop** — tre blocchi di TODO nell'ordine eventi / aggiorna / disegna.

**Ordine consigliato:** inizia da `Ball.draw()` (una riga), poi `Ball.update()` (già visto nella tappa 1), poi `bounce_off_paddle()`, poi le funzioni di `main.py`.

---

## Il rimbalzo sulla paddle

Questa è la parte più nuova. La condizione di collisione usa `pygame.Rect.colliderect()`:

```python
ball_rect = pygame.Rect(self.x - BALL_RADIUS,
                        self.y - BALL_RADIUS,
                        BALL_RADIUS * 2,
                        BALL_RADIUS * 2)

if self.vel_y > 0 and ball_rect.colliderect(paddle_rect):
    # rimbalzo
```

Perché controllare anche `vel_y > 0`? Senza questa condizione la pallina potrebbe rimbalzare anche mentre sale, se le due hitbox si sovrappongono per un frame. Controllare che stia scendendo evita il problema.

**Effetto angolo:**

```python
offset = self.x - paddle_rect.centerx   # da -50 a +50 circa
self.vel_x = offset // 10               # da -5 a +5
```

Se la pallina colpisce il bordo sinistro della paddle, `offset` è negativo e `vel_x` diventa negativo (va a sinistra). Se colpisce il centro, `offset ≈ 0` e la pallina sale quasi verticalmente. Questo rende il gioco controllabile.

---

## Domande di comprensione

1. Cosa succederebbe se `Ball.update()` chiamasse internamente `pygame.key.get_pressed()` invece di ricevere i parametri dall'esterno?
2. Perché `alive` è un attributo di `Ball` e non una variabile in `main.py`?
3. `reset_game()` restituisce una tupla. Potresti usare un dizionario? Quali sarebbero i pro e i contro?
4. Perché controlliamo `vel_y > 0` prima di verificare la collisione con la paddle?
5. Cosa succede se rimuovi la correzione della posizione `self.y = paddle_rect.top - BALL_RADIUS` nel rimbalzo? Prova a immaginarlo prima di testarlo.
6. Il loop chiama `ball.update()` e poi `ball.bounce_off_paddle()`. Cosa succederebbe se li invertissimo?

---

## Esperimenti guidati

**Esperimento 1 — Accelerazione progressiva**
Ogni volta che la pallina rimbalza sulla paddle, aumenta leggermente la velocità:

```python
# in bounce_off_paddle(), dopo aver invertito vel_y:
self.vel_y = int(self.vel_y * 1.05)   # 5% più veloce ad ogni rimbalzo
```
Aggiungi un limite massimo per evitare che diventi ingestibile.

**Esperimento 2 — Paddle che si restringe**
Ogni volta che la pallina cade (perdita di vita), riduci la larghezza della paddle:

```python
paddle.rect.width = max(40, paddle.rect.width - 15)
```
Rende il gioco progressivamente più difficile.

**Esperimento 3 — Seconda pallina (per chi ha finito)**
Crea una seconda istanza di `Ball` e gestiscila nel loop esattamente come la prima. Osserva quanto poco codice aggiuntivo serve grazie all'OOP.