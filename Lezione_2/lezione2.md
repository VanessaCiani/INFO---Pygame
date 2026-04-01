# Pallina interattiva — eventi del mouse e della tastiera

## Indice

- [Pallina interattiva — eventi del mouse e della tastiera](#pallina-interattiva--eventi-del-mouse-e-della-tastiera)
  - [Indice](#indice)
  - [Due modi di leggere l'input](#due-modi-di-leggere-linput)
    - [`pygame.event.get()` — eventi discreti](#pygameeventget--eventi-discreti)
    - [`pygame.key.get_pressed()` — stato continuo](#pygamekeyget_pressed--stato-continuo)
  - [Eventi: il sistema a coda](#eventi-il-sistema-a-coda)
  - [Lo stato istantaneo della tastiera](#lo-stato-istantaneo-della-tastiera)
  - [Analisi del codice](#analisi-del-codice)
    - [La funzione clamp](#la-funzione-clamp)
    - [Rilevare il clic sulla pallina](#rilevare-il-clic-sulla-pallina)
    - [Movimento con la tastiera e clamp](#movimento-con-la-tastiera-e-clamp)
    - [Cambio colore circolare](#cambio-colore-circolare)
  - [Cosa devi implementare](#cosa-devi-implementare)
  - [Domande di comprensione](#domande-di-comprensione)
  - [Esperimenti guidati](#esperimenti-guidati)

---

## Due modi di leggere l'input

Pygame offre due meccanismi distinti per gestire l'input dell'utente, e scegliere quello sbagliato produce comportamenti inattesi.

### `pygame.event.get()` — eventi discreti

Restituisce la lista degli eventi avvenuti dall'ultima chiamata. Ogni evento appare **una volta sola**, nel frame in cui si verifica. È il meccanismo giusto per azioni puntuali: un clic del mouse, la pressione di un tasto per sparare, la chiusura della finestra.

```python
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        # eseguito una volta sola al momento del clic
```

### `pygame.key.get_pressed()` — stato continuo

Restituisce un'istantanea dello stato di tutti i tasti **in questo momento**. È il meccanismo giusto per azioni continue: tenere premuto il tasto freccia per muoversi.

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    ball_x -= BALL_SPEED   # eseguito ogni frame finché il tasto è premuto
```

**Regola pratica:** se l'azione risponde a «premi una volta», usa gli eventi. Se risponde a «tieni premuto», usa `get_pressed()`.

Cosa succederebbe se usassi gli eventi per il movimento? La pallina si sposterebbe di un solo pixel per pressione, con un ritardo percettibile —esattamente il comportamento del cursore di testo quando tieni premuto un tasto.

---

## Eventi: il sistema a coda

Pygame raccoglie gli eventi in una **coda FIFO** (First In, First Out). Ad ogni frame, `pygame.event.get()` svuota la coda e restituisce tutti gli eventi accumulati.

```
  [ QUIT ][ MOUSEBUTTONDOWN ][ KEYDOWN ] ...
       ↑                                 ↑
    più vecchio                       più recente

  pygame.event.get() li restituisce tutti nell'ordine
  in cui sono arrivati, poi svuota la coda.
```

Gli eventi del mouse più usati:

| Tipo | Quando |
|------|--------|
| `pygame.MOUSEBUTTONDOWN` | pulsante premuto |
| `pygame.MOUSEBUTTONUP`   | pulsante rilasciato |
| `pygame.MOUSEMOTION`     | mouse spostato |

Ogni evento `MOUSEBUTTONDOWN` ha due attributi utili:
- `event.pos` — tupla `(x, y)` con le coordinate del clic
- `event.button` — numero del pulsante: `1` = sinistro, `2` = centrale, `3` = destro

---

## Lo stato istantaneo della tastiera

`pygame.key.get_pressed()` restituisce una sequenza indicizzata dai **codici dei tasti** (`pygame.K_*`). I codici più usati:

| Costante | Tasto |
|----------|-------|
| `pygame.K_LEFT`  | freccia sinistra |
| `pygame.K_RIGHT` | freccia destra |
| `pygame.K_UP`    | freccia su |
| `pygame.K_DOWN`  | freccia giù |
| `pygame.K_a` … `pygame.K_z` | lettere |
| `pygame.K_SPACE` | barra spaziatrice |
| `pygame.K_ESCAPE`| Esc |

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    ball_x -= BALL_SPEED
```

È possibile controllare più tasti nello stesso frame: se l'utente tiene premuto ↑ e → contemporaneamente, la pallina si muove in diagonale.

---

## Analisi del codice

### La funzione clamp

```python
def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))
```

`clamp` costringe un valore a restare dentro un intervallo. È un pattern talmente comune in grafica e giochi da meritare un nome proprio.

Come funziona con due valori annidati:

```
clamp(150, 0, 100)
  → min(150, 100) = 100
  → max(0, 100)   = 100   ✓ bloccato al massimo

clamp(-5, 0, 100)
  → min(-5, 100)  = -5
  → max(0, -5)    = 0     ✓ bloccato al minimo

clamp(42, 0, 100)
  → min(42, 100)  = 42
  → max(0, 42)    = 42    ✓ invariato
```

Per fermare la pallina ai bordi considerando il raggio:

```python
ball_x = clamp(ball_x, BALL_RADIUS, SCREEN_W - BALL_RADIUS)
ball_y = clamp(ball_y, BALL_RADIUS, SCREEN_H - BALL_RADIUS)
```

Perché `BALL_RADIUS` come minimo e `SCREEN_W - BALL_RADIUS` come massimo? Perché `ball_x` è il **centro**: il bordo sinistro della pallina è a `ball_x - BALL_RADIUS`, il bordo destro è a `ball_x + BALL_RADIUS`.

---

### Rilevare il clic sulla pallina

Per sapere se un clic ha colpito la pallina, dobbiamo verificare se il punto cliccato si trova dentro il cerchio. La condizione è:

```
distanza(punto, centro) ≤ raggio
```

La distanza tra due punti si calcola con Pitagora:

```
d = √((px - cx)² + (py - cy)²)
```

In pratica si evita la radice quadrata confrontando i quadrati:

```python
dx = px - cx
dy = py - cy
return dx * dx + dy * dy <= radius * radius
```

È matematicamente equivalente ma più veloce (la radice quadrata è costosa computazionalmente).

---

### Movimento con la tastiera e clamp

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    ball_x -= BALL_SPEED
if keys[pygame.K_RIGHT]:
    ball_x += BALL_SPEED
# ... e così via per gli altri assi

ball_x = clamp(ball_x, BALL_RADIUS, SCREEN_W - BALL_RADIUS)
ball_y = clamp(ball_y, BALL_RADIUS, SCREEN_H - BALL_RADIUS)
```

Notare che il `clamp` viene applicato **dopo** tutti gli aggiornamenti, non dentro ogni `if`. È più leggibile e funziona correttamente anche quando più tasti sono premuti contemporaneamente.

---

### Cambio colore circolare

La lista `COLORS` contiene cinque colori. Ad ogni clic valido vogliamo passare al colore successivo, tornando al primo dopo l'ultimo. L'operatore modulo `%` è perfetto per questo:

```python
new_index = (current_index + 1) % len(COLORS)
```

Esempi con `len(COLORS) = 5`:

| `current_index` | `+ 1` | `% 5` |
|----------------|-------|-------|
| 0 | 1 | 1 |
| 3 | 4 | 4 |
| 4 | 5 | **0** ← riparte |

---

## Cosa devi implementare

Il file `eventi.py` contiene quattro punti con il commento `TODO`. Nell'ordine suggerito:

**1. `point_in_circle()`** — la funzione è già dichiarata con il suo docstring. Implementa il corpo usando il teorema di Pitagora (senza radice quadrata).

**2. `next_color()`** — restituisce una tupla `(nuovo_indice, nuovo_colore)`. Usa l'operatore `%` per il comportamento circolare.

**3. Gestione del clic** — nel blocco eventi, intercetta `pygame.MOUSEBUTTONDOWN`, verifica il tasto sinistro, chiama `point_in_circle()` e se il clic è dentro la pallina chiama `next_color()` aggiornando `color_index` e `ball_color`.

**4. Movimento e disegno** — leggi `keys` con `pygame.key.get_pressed()`, aggiorna `ball_x` e `ball_y` in base ai tasti freccia (o WASD), applica `clamp()`, poi disegna la pallina con `pygame.draw.circle()`.

---

## Domande di comprensione

1. Perché per il movimento usi `get_pressed()` e non gli eventi? Cosa succederebbe al contrario?
2. Cosa restituisce `pygame.key.get_pressed()` — una lista, un dizionario, o qualcos'altro?
3. Se l'utente clicca fuori dalla pallina, `point_in_circle()` restituisce `False`. Cosa fa il programma in quel caso?
4. Con `len(COLORS) = 5`, qual è il risultato di `(4 + 1) % 5`? E di `(3 + 1) % 5`?
5. Perché `clamp` viene applicato dopo tutti gli aggiornamenti della posizione e non dentro ogni `if`?
6. È possibile muovere la pallina in diagonale? Come?

---

## Esperimenti guidati

**Esperimento 1 — Velocità variabile**
Aggiungi `pygame.K_LSHIFT` come modificatore: quando Shift è tenuto premuto, la velocità raddoppia.

```python
speed = BALL_SPEED * 2 if keys[pygame.K_LSHIFT] else BALL_SPEED
```

**Esperimento 2 — Clic destro**
Fai sì che il clic destro (`event.button == 3`) riporti la pallina al centro dello schermo.

**Esperimento 3 — Trascina**
Gestisci `pygame.MOUSEMOTION`: se il pulsante sinistro è tenuto premuto (`event.buttons[0] == 1`) e il mouse è sopra la pallina, aggiorna `ball_x` e `ball_y` con `event.pos`.

**Esperimento 4 — Rimbalzo misto (per chi ha finito)**
Reintegra la velocità automatica della tappa 1: la pallina rimbalza da sola, ma la tastiera aggiunge velocità nella direzione premuta anziché impostare una posizione fissa.