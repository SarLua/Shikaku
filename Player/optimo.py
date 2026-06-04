"""
Módulo: Solver Óptimo para Shikaku con Backtracking y Heurística MRV

Implementa la solución exacta del puzzle Shikaku combinando:
  - Generación exhaustiva de candidatos geométricos
  - Heurística MRV (Minimum Remaining Values) para poda inteligente
  - Backtracking exhaustivo para búsqueda de solución

Este módulo es la versión Python del algoritmo descrito en pseudocodeShikakuOptimo.md
"""

from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class Rectangulo:
    """
    Representa un rectángulo en el tablero Shikaku.

    Attributes:
        fila_inicio (int): Fila superior del rectángulo (0-indexado).
        columna_inicio (int): Columna izquierda del rectángulo (0-indexado).
        alto (int): Altura del rectángulo en celdas.
        ancho (int): Ancho del rectángulo en celdas.

    @note Un rectángulo cubre desde (fila_inicio, columna_inicio)
          hasta (fila_inicio + alto - 1, columna_inicio + ancho - 1) inclusive.
    """
    fila_inicio: int = 0
    columna_inicio: int = 0
    alto: int = 0
    ancho: int = 0


@dataclass
class Numero:
    """
    Representa un número (pista) del puzzle Shikaku.

    Attributes:
        fila (int): Fila donde está ubicado el número.
        columna (int): Columna donde está ubicado el número.
        valor (int): Área que debe cubrir el rectángulo asociado.
        lista_rectangulos_posibles (list[Rectangulo]): Candidatos geométricos válidos
                                                       que satisfacen:
                                                       - Contienen la celda (fila, columna)
                                                       - Su área es igual a 'valor'
                                                       - No incluyen otros números

    @note Inicialmente vacío; se rellena en PASO 2 del algoritmo.
    """
    fila: int = 0
    columna: int = 0
    valor: int = 0
    lista_rectangulos_posibles: list[Rectangulo] = field(default_factory=list)



def _extraer_numeros(celdas: list[list[int]], filas: int, cols: int) -> list[Numero]:
    """
    PASO 1: Extrae todos los números (pistas) del tablero.

    Recorre la matriz completa y crea un objeto Numero por cada
    celda que contiene un valor positivo.

    @param celdas
           Matriz 2D de tamaño filas × cols donde:
             - celdas[r][c] > 0: contiene la pista (valor del área)
             - celdas[r][c] = 0: celda vacía
           Se espera que celdas esté completamente inicializada.

    @param filas
           Número de filas del tablero.

    @param cols
           Número de columnas del tablero.

    @return list[Numero]
            Lista de objetos Numero extraídos en orden de aparición
            (iterando filas de arriba a abajo, columnas de izquierda a derecha).
            Cada Numero contiene fila, columna, valor, pero
            lista_rectangulos_posibles aún está vacía (se rellena en PASO 2).

    @complexity O(filas × cols) — itera cada celda una vez.
    """
    numeros: list[Numero] = []
    for r in range(filas):
        for c in range(cols):
            if celdas[r][c] > 0:
                numeros.append(Numero(fila=r, columna=c, valor=celdas[r][c]))
    return numeros



def _obtener_factorizaciones(area: int) -> list[tuple[int, int]]:
    """
    PASO 2 (Auxiliar): Obtiene todas las factorizaciones de un área.

    Encuentra todos los pares (alto, ancho) tales que alto × ancho == area.
    Incluye ambas orientaciones: (h, w) y (w, h) si h ≠ w.

    @param area
           Número positivo (área = valor del número en Shikaku).

    @return list[tuple[int, int]]
            Lista de pares (alto, ancho) donde alto × ancho == area.
            Los pares están en orden: primero h desde 1 hasta sqrt(area),
            luego sus complementos.
            Ejemplo: area=6 → [(1,6), (6,1), (2,3), (3,2)]

    @complexity O(√area) — el loop corre desde 1 hasta √area.

    @note No hay garantía de orden específico más allá de que
          los factores ≤ √area aparecen primero.
    """
    pares: list[tuple[int, int]] = []
    a = 1
    while a * a <= area:
        if area % a == 0:
            b = area // a
            pares.append((a, b))
            if a != b:
                pares.append((b, a))
        a += 1
    return pares


def _rectangulo_contiene_solo_su_numero(
    rc: Rectangulo,
    celdas: list[list[int]],
    numero_actual: Numero,
) -> bool:
    """
    PASO 2 (Auxiliar): Valida la regla Shikaku: un rectángulo contiene exactamente un número.

    Verifica que dentro de los límites del rectángulo no exista ningún número
    distinto al número actual. Este es un chequeo crucial para mantener
    la validez del puzzle.

    @param rc
           Rectangulo candidato a validar.
           Se inspecciona desde (fila_inicio, columna_inicio)
           hasta (fila_inicio+alto-1, columna_inicio+ancho-1).

    @param celdas
           Matriz original del tablero con los números (pistas).
           Se usa solo para lectura.

    @param numero_actual
           El número propietario del rectángulo (la pista dentro de él).
           Se usa para identificar cuál es el número "correcto".

    @return bool
            - true: el rectángulo contiene solo el número 'numero_actual' (válido)
            - false: el rectángulo contiene otro número además del actual (inválido)

    @complexity O(alto × ancho) — itera cada celda del rectángulo.

    @note Esta validación ocurre durante PASO 2 (generación de candidatos)
          para evitar agregar candidatos inválidos desde el inicio.
    """
    for r in range(rc.fila_inicio, rc.fila_inicio + rc.alto):
        for c in range(rc.columna_inicio, rc.columna_inicio + rc.ancho):
            if celdas[r][c] > 0:
                if not (r == numero_actual.fila and c == numero_actual.columna):
                    return False
    return True


def _generar_rectangulos_posibles(
    numero: Numero,
    celdas: list[list[int]],
    filas: int,
    cols: int,
) -> None:
    """
    PASO 2: Genera todos los rectángulos candidatos válidos para un número.

    Para un número dado:
      1. Obtiene todas las factorizaciones de su valor (área)
      2. Para cada factorización (alto, ancho), prueba todas las posiciones
         que incluyen la celda del número
      3. Descarta rectángulos que salen del tablero
      4. Descarta rectángulos que contienen otros números (regla Shikaku)
      5. Agrega los candidatos válidos a numero.lista_rectangulos_posibles

    @param numero
           Objeto Numero a procesar.
           Se modifica in-place: se llena numero.lista_rectangulos_posibles.
           Contiene: fila, columna, valor, lista_rectangulos_posibles (vacía al entrada).

    @param celdas
           Matriz original del tablero para verificar la regla Shikaku.
           Se usa solo para lectura.

    @param filas
           Altura del tablero (límite superior para validación).

    @param cols
           Ancho del tablero (límite derecho para validación).

    @return None (modificación in-place de numero.lista_rectangulos_posibles)

    @complexity O(√area × area) donde area = numero.valor
               - √area factorizaciones
               - area posiciones posibles por cada factorización
               - O(alto × ancho) para validar cada candidato
               En la práctica: O(area^1.5) o mejor debido a la poda geométrica.

    @note Modifica numero.lista_rectangulos_posibles directamente.
          Primero la vacía, luego la llena con candidatos válidos.
    """
    numero.lista_rectangulos_posibles = []

    for alto, ancho in _obtener_factorizaciones(numero.valor):
        for fila_inicio in range(numero.fila - (alto - 1), numero.fila + 1):
            for col_inicio in range(numero.columna - (ancho - 1), numero.columna + 1):
                if fila_inicio < 0 or col_inicio < 0:
                    continue
                if fila_inicio + alto > filas or col_inicio + ancho > cols:
                    continue

                rc = Rectangulo(
                    fila_inicio=fila_inicio,
                    columna_inicio=col_inicio,
                    alto=alto,
                    ancho=ancho,
                )

                if _rectangulo_contiene_solo_su_numero(rc, celdas, numero):
                    numero.lista_rectangulos_posibles.append(rc)




def _no_colisiona(rc: Rectangulo, ocupado: list[list[bool]]) -> bool:
    """
    PASO 5 (Auxiliar): Verifica si un rectángulo no colisiona con asignaciones previas.

    Comprueba que todas las celdas del rectángulo estén marcadas como
    "no ocupadas" en la matriz de ocupación. Esta es la validación
    central durante el backtracking.

    @param rc
           Rectangulo a verificar.
           Se inspeccionan celdas desde (fila_inicio, columna_inicio)
           hasta (fila_inicio+alto-1, columna_inicio+ancho-1).

    @param ocupado
           Matriz booleana que registra celdas ocupadas.
           - ocupado[r][c] = true: ya tiene asignación (colisión)
           - ocupado[r][c] = false: disponible (sin colisión)
           Se usa solo para lectura.

    @return bool
            - true: todas las celdas del rectángulo están libres (válido)
            - false: al menos una celda está ocupada (inválido)

    @complexity O(alto × ancho) — itera cada celda del rectángulo.

    @note Esta función es crítica para la eficiencia del backtracking.
          Se ejecuta miles de veces durante la búsqueda.
    """
    for r in range(rc.fila_inicio, rc.fila_inicio + rc.alto):
        for c in range(rc.columna_inicio, rc.columna_inicio + rc.ancho):
            if ocupado[r][c]:
                return False
    return True


def _marcar(
    rc: Rectangulo,
    ocupado: list[list[bool]],
    dueno: list[list[int]],
    id_numero: int,
) -> None:
    """
    PASO 5 (Auxiliar): Marca un rectángulo como asignado.

    Actualiza dos matrices para registrar que el rectángulo
    pertenece a un número específico:
      1. ocupado: marca las celdas como "en uso"
      2. dueno: registra cuál número posee cada celda

    Esta operación es reversible mediante _desmarcar().

    @param rc
           Rectangulo a marcar.
           Todas las celdas desde (fila_inicio, columna_inicio)
           hasta (fila_inicio+alto-1, columna_inicio+ancho-1) se marcan.

    @param ocupado
           Matriz booleana de ocupación.
           Se modifica: ocupado[r][c] = true para cada celda del rectángulo.

    @param dueno
           Matriz entera que registra propietarios.
           Se modifica: dueno[r][c] = id_numero para cada celda del rectángulo.

    @param id_numero
           ID del número propietario (típicamente indice + 1 en el backtracking).
           Debe ser > 0 para distinguir de "no asignado" (que es 0).

    @return None (modificación in-place de ocupado y dueno)

    @complexity O(alto × ancho) — itera cada celda del rectángulo una vez.

    @note Esta operación es parte de la fase "MARCAR" del backtracking.
          Debe ser seguida eventualmente por _desmarcar() para deshacer cambios.
    """
    for r in range(rc.fila_inicio, rc.fila_inicio + rc.alto):
        for c in range(rc.columna_inicio, rc.columna_inicio + rc.ancho):
            ocupado[r][c] = True
            dueno[r][c] = id_numero


def _desmarcar(
    rc: Rectangulo,
    ocupado: list[list[bool]],
    dueno: list[list[int]],
) -> None:
    """
    PASO 5 (Auxiliar): Desmarca un rectángulo (deshacer asignación).

    Revierte los cambios realizados por _marcar(). Se utiliza durante
    el backtracking cuando una rama de búsqueda no conduce a solución.

    @param rc
           Rectangulo a desmarcar.
           Todas las celdas se vuelven a marcar como "no ocupadas" y "sin dueño".

    @param ocupado
           Matriz booleana de ocupación.
           Se modifica: ocupado[r][c] = false para cada celda del rectángulo.

    @param dueno
           Matriz entera de propietarios.
           Se modifica: dueno[r][c] = 0 (sin asignación) para cada celda.

    @return None (modificación in-place de ocupado y dueno)

    @complexity O(alto × ancho) — itera cada celda del rectángulo una vez.

    @note Operación inversa de _marcar().
          Se ejecuta en la fase "BACKTRACK" del backtracking cuando
          la recursión de un hijo falla.
    """
    for r in range(rc.fila_inicio, rc.fila_inicio + rc.alto):
        for c in range(rc.columna_inicio, rc.columna_inicio + rc.ancho):
            ocupado[r][c] = False
            dueno[r][c] = 0


def _resolver_recursivo(
    indice: int,
    numeros: list[Numero],
    ocupado: list[list[bool]],
    dueno: list[list[int]],
    solucion: list[Rectangulo],
) -> bool:
    """
    PASO 5: Función recursiva de backtracking exhaustivo.

    Implementa la búsqueda exhaustiva con poda temprana. Intenta asignar
    un rectángulo válido a cada número en orden (ordenado por MRV en el Paso 3).
    Si una rama falla, retrocede (backtrack) y prueba el siguiente candidato.

    Estructura:
      1. CASO BASE: si indice == len(numeros), todos están asignados → true
      2. PRUEBA: for-loop sobre cada rectangulo candidato
      3. PODA: verifica noColisiona() antes de explorar
      4. MARCAR: reserva celdas para este número
      5. RECURSAR: intenta resolver el siguiente número
      6. BACKTRACK: desmarca y prueba siguiente candidato si falla

    @param indice
           Índice del número a resolver (0 <= indice < len(numeros)).
           Representa la profundidad actual en el árbol de búsqueda.
           numeros[indice] es el número que se intenta asignar.

    @param numeros
           Lista completa de números, YA ORDENADA por MRV (Paso 3).
           Números con pocas opciones están primero.

    @param ocupado
           Matriz booleana de celdas ocupadas.
           Se modifica durante ejecución: se marca/desmarcar según backtracking.
           Al retornar, debe estar exactamente como entró.

    @param dueno
           Matriz de dueños (cuál número posee cada celda).
           Se modifica durante ejecución: marca/desmarcar según backtracking.
           Al retornar, debe estar exactamente como entró.

    @param solucion
           Vector que acumula la solución.
           solucion[indice] = Rectangulo asignado a numeros[indice].
           Debe tener tamaño len(numeros) inicialmente.

    @return bool
            - true: se encontró una asignación válida desde este punto
                   (y solucion queda con los rectángulos parciales/completos)
            - false: no existe asignación válida desde este punto
                    (ocupado y dueno vuelven a su estado de entrada)

    @complexity O(∏ |candidatos_i| × area_media)
               Peor caso: exponencial en cantidad de números
               El factor area_media viene de marcar/desmarcar
               MRV reduce dramáticamente la constante exponencial

    @note Implementa el pseudocódigo de resolverRecursivo (L94-L145).
          Las matrices ocupado y dueno se preservan (se revierten en backtrack).
          Esta es una búsqueda DFS (depth-first search) pura.
    """

    if indice == len(numeros):
        return True

    numero_actual = numeros[indice]
    id_rect = indice + 1

    for rc in numero_actual.lista_rectangulos_posibles:

        if not _no_colisiona(rc, ocupado):
            continue

        _marcar(rc, ocupado, dueno, id_rect)
        solucion[indice] = rc

        if _resolver_recursivo(indice + 1, numeros, ocupado, dueno, solucion):
            return True

        _desmarcar(rc, ocupado, dueno)

    return False





def resolver_shikaku(
    celdas: list[list[int]], filas: int, cols: int
) -> list[Rectangulo] | None:
    """
    ALGORITMO PRINCIPAL: Resuelve un puzzle Shikaku de forma exhaustiva.

    Ejecuta los 5 pasos del algoritmo:
      1. Extrae números del tablero
      2. Genera rectángulos candidatos para cada número
      3. Ordena números por heurística MRV (Minimum Remaining Values)
      4. Inicializa matrices de ocupación
      5. Ejecuta backtracking exhaustivo

    @param celdas
           Matriz 2D de tamaño filas × cols donde:
             - celdas[r][c] > 0: número (pista) con ese valor de área
             - celdas[r][c] = 0: celda vacía
           La matriz debe estar completamente inicializada.

    @param filas
           Número de filas del tablero.

    @param cols
           Número de columnas del tablero.

    @return list[Rectangulo] | None
            - Si existe solución: lista de len(numeros) Rectangulos
              donde solucion[i] es el rectángulo asignado a numeros[i]
              (tras el ordenamiento MRV del Paso 3).
            - Si no existe solución: None

    @complexity Peor caso: O(∏ |candidatos_i|) — exponencial
               Caso promedio: O(n × m × f) donde:
                 - n×m = tamaño del tablero
                 - f = número de factorizaciones (típicamente pequeño)
               MRV reduce dramáticamente la constante exponencial.

    @note Validación temprana: si algún número tiene 0 candidatos,
          retorna None inmediatamente (sin solución).

    @example
            celdas = [
              [4, 0, 0, 4],
              [0, 0, 0, 0],
              [4, 0, 0, 4],
              [0, 0, 0, 0],
            ]
            sol = resolver_shikaku(celdas, 4, 4)
            # sol es una lista de 4 Rectangulos (uno para cada número)
    """

    numeros = _extraer_numeros(celdas, filas, cols)

    for n in numeros:
        _generar_rectangulos_posibles(n, celdas, filas, cols)

    if any(len(n.lista_rectangulos_posibles) == 0 for n in numeros):
        return None

    numeros.sort(key=lambda n: len(n.lista_rectangulos_posibles))

    ocupado: list[list[bool]] = [[False] * cols for _ in range(filas)]
    dueno: list[list[int]] = [[0] * cols for _ in range(filas)]
    solucion: list[Rectangulo] = [Rectangulo() for _ in numeros]

    if not _resolver_recursivo(0, numeros, ocupado, dueno, solucion):
        return None

    return solucion




def _rect_a_jugada(rc: Rectangulo) -> str:
    """
    Convierte un Rectangulo a formato de jugada del proyecto.

    Traduce un Rectangulo interno a la representación de jugada
    que espera Tablero.click(): "f0,c0 f1,c1" donde:
      - (f0, c0) es la esquina superior-izquierda
      - (f1, c1) es la esquina inferior-derecha
      - Ambas coordenadas son 0-indexadas
      - El rango es inclusivo en ambos lados

    @param rc
           Rectangulo a convertir.
           Contiene: fila_inicio, columna_inicio, alto, ancho.

    @return str
            Formato "f0,c0 f1,c1" donde:
              f0 = rc.fila_inicio
              c0 = rc.columna_inicio
              f1 = rc.fila_inicio + rc.alto - 1
              c1 = rc.columna_inicio + rc.ancho - 1

    @example
            rc = Rectangulo(fila_inicio=0, columna_inicio=1,
                           alto=2, ancho=2)
            jugada = _rect_a_jugada(rc)
            # resultado: "0,1 1,2"

    @note Esta conversión es necesaria porque el Rectangulo usa
          (alto, ancho) pero Tablero.click() espera (f0,c0, f1,c1).
    """
    f0 = rc.fila_inicio
    c0 = rc.columna_inicio
    f1 = rc.fila_inicio + rc.alto - 1
    c1 = rc.columna_inicio + rc.ancho - 1
    return f"{f0},{c0} {f1},{c1}"





class Player:
    """
    Interfaz del jugador automático óptimo para el juego Shikaku.

    Implementa la interfaz estándar de Player del proyecto:
      - __init__(): inicializa el jugador
      - init(tablero): calcula la solución al tablero
      - play(): devuelve la siguiente jugada
      - report(response): recibe feedback de la jugada anterior

    Attributes:
        m_jugadas (list[str]): cola de jugadas a ejecutar
        m_sin_solucion (bool): flag si el tablero no tiene solución
    """

    def __init__(self):
        """
        Inicializa el Player óptimo.

        Prepara estructuras internas vacías. El cálculo real ocurre
        cuando init(tablero) es llamado por el Juego.

        @note No requiere parámetros.
        """
        self.m_jugadas: list[str] = []
        self.m_sin_solucion: bool = False

    def init(self, tablero) -> None:
        """
        Calcula la solución del tablero.

        Llamado por Juego.__init__() al inicio. Ejecuta el algoritmo
        completo resolver_shikaku() y almacena las jugadas en orden.

        @param tablero
               Objeto Tablero con atributos:
                 - s_Alto: número de filas
                 - s_Ancho: número de columnas
                 - celdas: matriz 2D con los números

        @return None (modifica self.m_jugadas y self.m_sin_solucion)

        @note Si no existe solución, print() notifica al usuario
              y deja m_jugadas vacío.

        @side-effect Llama a resolver_shikaku(), que puede ser
                     costosa computacionalmente para tableros grandes.
        """
        filas = tablero.s_Alto
        cols = tablero.s_Ancho
        solucion = resolver_shikaku(tablero.celdas, filas, cols)

        if solucion is None:
            self.m_sin_solucion = True
            self.m_jugadas = []
            print("Optimo: SIN SOLUCION para este tablero.")
            return

        self.m_sin_solucion = False
        self.m_jugadas = [_rect_a_jugada(rc) for rc in solucion]

    def play(self) -> str:
        """
        Devuelve la siguiente jugada.

        Llamado por Juego.solve() antes de cada click al tablero.
        Extrae y retorna la jugada en formato "f0,c0 f1,c1".

        @return str
                La siguiente jugada en formato "f0,c0 f1,c1".
                Las coordenadas son 0-indexadas e inclusivas.

        @raise RuntimeError
               Si no hay solución o se agotaron las jugadas.

        @note Modifica m_jugadas (pop()).
        """
        if self.m_sin_solucion or not self.m_jugadas:
            raise RuntimeError("Optimo: no hay jugadas disponibles.")
        return self.m_jugadas.pop(0)

    def report(self, response) -> None:
        """
        Recibe feedback de la jugada ejecutada.

        Llamado por Juego.solve() después de cada click para
        reportar éxito o error. En este jugador óptimo, simplemente
        imprime el resultado (no adapta estrategia, pues ya calculó todo).

        @param response
               Tupla (ok, info) donde:
                 - ok: bool indicando si la jugada fue válida
                 - info: dict con detalles de éxito o error

        @return None (solo imprime)

        @note Este jugador es determinista y no aprende durante la ejecución.
              El report es informativo solamente.
        """
        ok, info = response
        if ok:
            print(
                f"[OPT] Region {info['letra']}: area={info['area']}, pista={info['pista']}"
            )
        else:
            print(f"[OPT] Error inesperado: {info}")