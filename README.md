# Shikaku

Proyecto final del curso **Análisis de Algoritmos**.

Implementación del puzzle [Shikaku](https://en.wikipedia.org/wiki/Shikaku): dividir un tablero en rectángulos no solapados de modo que cada rectángulo contenga exactamente una pista numérica y su área coincida con ese número.

---

## Estructura del proyecto

```
Shikaku/
├── Interfaz.py              # Punto de entrada: saludo, argumentos y arranque del juego
├── Juego.py                 # Bucle principal del juego
├── Tablero.py               # Tablero, validación de jugadas y reglas de Shikaku
├── Player/
│   ├── humano.py            # Jugador humano por consola
│   ├── fuerza_bruta.py      # Jugador automático (fuerza bruta)
│   └── optimo.py            # Jugador automático (aproximación/óptimo)
├── Ejemplos/
│   ├── Lectura_Archivos.py  # Lectura de tableros desde archivo de texto
│   ├── 1tab_5x5.txt         # Tablero de ejemplo 5×5
│   └── 2tab_5x5.txt         # Tablero de ejemplo 5×5
└── README.md
```

---

## Ejecución

```bash
python3 Interfaz.py <tablero> <jugador> <prueba>
```

| Argumento | Descripción |
|---|---|
| `tablero` | Ruta al archivo de tablero (ej. `Ejemplos/1tab_5x5.txt`) |
| `jugador` | Ruta al módulo del jugador (ej. `Player/humano.py`) |
| `prueba` | `true` o `false` — indica si es modo prueba |

Ejemplo con jugador humano:

```bash
python3 Interfaz.py Ejemplos/1tab_5x5.txt Player/humano.py false
```

---

## Formato del archivo de tablero

La **primera línea** define las dimensiones:

```
alto ancho
```

Cada **línea siguiente** define una pista: el número y su posición `fila,col`:

```
5 5
2 0,1
2 0,2
1 0,3
5 0,4
```

- Las coordenadas usan **base 0** (la primera fila y columna son `0`).
- Una celda sin pista se representa con `0` internamente (no aparece en el archivo).

---

## Formato de jugada

El jugador humano introduce jugadas **sin** la palabra `COLOCAR`:

```
A 0,1 1,2
│  │   └── esquina final   → fila 1, columna 2 (inclusiva)
│  └────── esquina inicial → fila 0, columna 1
└───────── letra que identifica la región
```

### Convención de coordenadas

| Concepto | Detalle |
|---|---|
| Base | **0** (primera fila/columna = 0) |
| Rango | **Inclusivo** en ambas esquinas |
| Rectángulo | Todas las celdas del bounding box entre las dos esquinas |

Ejemplo: `B 0,0 0,1` selecciona las celdas `(0,0)` y `(0,1)` → rectángulo de 1×2 = área 2.

Las esquinas pueden escribirse en cualquier orden; el sistema las normaliza automáticamente (`2,3 0,1` ≡ `0,1 2,3`).

---

## Reglas de Shikaku implementadas

### 1. Validación geométrica — `rectangulo_valido`

Comprueba que la región propuesta sea legal antes de colocarla:

1. **Normalización de esquinas**: se calcula `min`/`max` de filas y columnas para obtener un rectángulo axis-aligned.
2. **Dentro del tablero**: ninguna coordenada puede quedar fuera de `[0, alto-1]` × `[0, ancho-1]`.
3. **Forma rectangular**: al usar el bounding box completo entre dos esquinas opuestas, la región siempre es un rectángulo alineado a filas/columnas (no se admiten formas en L ni selecciones diagonales sueltas).
4. **Sin solapamiento**: ninguna celda del rectángulo puede estar ocupada por otra letra distinta. Se permite re-colocar la misma letra sobre sus propias celdas.

### 2. Validación de pista — `area_rectangulo`

Comprueba las reglas del puzzle sobre el rectángulo normalizado:

1. **Área**: `(fila_fin - fila_ini + 1) × (col_fin - col_ini + 1)`.
2. **Exactamente una pista**: debe haber un solo número en `celdas` dentro del rectángulo.
3. **Área = pista**: el valor de esa pista debe coincidir con el área calculada.

| Error | Mensaje |
|---|---|
| Sin pista en la región | `El rectangulo no contiene ninguna pista` |
| Más de una pista | `Hay mas de un numero en el rectangulo` |
| Área incorrecta | `Area=4, pista=2` |
| Fuera de límites | `El rectangulo esta fuera de los limites del tablero` |
| Solapamiento | `Celda (r,c) ya ocupada por la region 'X'` |
| Formato inválido | `Formato invalido. Use: A 0,0 2,1` |

---

## Flujo de una jugada — `click(jugada)`

```
"A 0,1 1,2"
     │
     ▼
_parsear_jugada()       → extrae letra y coordenadas
     │
     ▼
rectangulo_valido()     → límites + sin solapamiento
     │
     ▼
area_rectangulo()       → pista única + área correcta
     │
     ▼
_colocar()              → marca celdas con la letra
     │
     ▼
(True, "Rectangulo A: area=4, pista=4")
```

**Retorno de `click`:**

- `(True, mensaje)` — jugada válida, región colocada.
- `(False, mensaje)` — jugada rechazada, el tablero no cambia.

---

## Modelo de datos interno

La clase `Tablero` mantiene **dos matrices** separadas:

| Atributo | Tipo | Rol |
|---|---|---|
| `celdas` | `list[list[int]]` | Pistas originales del archivo (`0` = celda vacía). Solo lectura durante el juego. |
| `s_Tablero` | `list[(letra, ocupada)]` | Estado del juego. Lista plana de tamaño `alto × ancho`. |
| `s_Alto`, `s_Ancho` | `int` | Dimensiones del tablero. |
| `s_Completo` | `bool` | `True` cuando todas las celdas están ocupadas. |

Índice plano de una celda: `fila * s_Ancho + columna`.

### Visualización

Al imprimir el tablero (`print(tablero)`):

- Celda **ocupada** → muestra la letra de la región (`A`, `B`, …).
- Celda **libre con pista** → muestra el número.
- Celda **libre sin pista** → espacio en blanco.

Las etiquetas de fila y columna usan base 0, coherente con las coordenadas de jugada.

---

## Bucle del juego — `Juego.solve()`

1. Muestra el tablero actual.
2. Pide una jugada al jugador (`Player.play()`).
3. Procesa la jugada con `Tablero.click()`.
4. Informa el resultado al jugador (`Player.report()`).
5. Repite hasta que `Tablero.finished()` sea `True` (todas las celdas ocupadas).

---

## Interfaz de un jugador (`Player`)

Todo módulo en `Player/` debe exponer una clase `Player` con:

| Método | Descripción |
|---|---|
| `__init__()` | Constructor. |
| `init(tablero)` | Recibe referencia al tablero al iniciar la partida. |
| `play()` | Devuelve un `str` con la jugada (ej. `"A 0,1 1,2"`). |
| `report(r)` | Recibe el resultado de `click()` — tupla `(bool, mensaje)`. |

---

## Ejemplos de jugadas válidas e inválidas

Tablero `Ejemplos/1tab_5x5.txt`:

| Jugada | Resultado | Motivo |
|---|---|---|
| `A 0,3 0,3` | ✓ | 1×1, pista 1, área 1 |
| `B 0,0 0,1` | ✓ | 1×2, una pista 2, área 2 |
| `B 0,1 1,2` | ✗ | Dos pistas dentro del rectángulo |
| `C 0,1 0,2` | ✗ | Dos pistas en la misma fila (ambas valen 2) |
| `D 0,0 5,5` | ✗ | Coordenadas fuera del tablero 5×5 |

---

## Lectura de tableros desde Python

```python
from Ejemplos.Lectura_Archivos import lectura_tablero

datos = lectura_tablero("Ejemplos/1tab_5x5.txt")
print(datos.s_Alto, datos.s_Ancho, datos.celdas)
```

`lectura_tablero` devuelve un `TableroLeido` con `s_Alto`, `s_Ancho` y `celdas`.

---

## Uso programático del tablero

```python
from Tablero import Tablero

t = Tablero("Ejemplos/1tab_5x5.txt")
print(t)

ok, msg = t.click("A 0,3 0,3")
print(ok, msg)          # True Rectangulo A: area=1, pista=1

ok, msg = t.click("B 0,0 0,1")
print(ok, msg)          # True Rectangulo B: area=2, pista=2

print(t.finished())     # False — aún quedan celdas libres
```

---

## Notas

- El comando `VERIFICAR` (comprobar solución completa sin colocar) **no está implementado**.
- La condición de victoria actual es que **todas las celdas estén ocupadas**; no se valida en ese momento que cada región cumpla individualmente las reglas (eso ocurre en cada `click`).
- Los módulos `Player/fuerza_bruta.py` y `Player/optimo.py` están preparados como jugadores automáticos; su lógica de resolución puede implementarse sobre la misma interfaz `play()` / `report()`.
