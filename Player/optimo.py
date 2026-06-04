from __future__ import annotations

from dataclasses import dataclass, field


# ------------------------------------------------------------
# ESTRUCTURAS  (pseudocódigo L11-L26)
# ------------------------------------------------------------

@dataclass
class Rectangulo:
    fila_inicio: int = 0
    columna_inicio: int = 0
    alto: int = 0
    ancho: int = 0


@dataclass
class Numero:
    fila: int = 0
    columna: int = 0
    valor: int = 0
    lista_rectangulos_posibles: list[Rectangulo] = field(default_factory=list)


# ------------------------------------------------------------
# PASO 1: OBTENER TODOS LOS NÚMEROS  (pseudocódigo L28-L33)
# ------------------------------------------------------------

def _extraer_numeros(celdas: list[list[int]], filas: int, cols: int) -> list[Numero]:
    numeros: list[Numero] = []
    for r in range(filas):
        for c in range(cols):
            if celdas[r][c] > 0:
                numeros.append(Numero(fila=r, columna=c, valor=celdas[r][c]))
    return numeros


# ------------------------------------------------------------
# PASO 2: GENERAR RECTÁNGULOS POSIBLES  (pseudocódigo L35-L64)
# ------------------------------------------------------------

def _obtener_factorizaciones(area: int) -> list[tuple[int, int]]:
    """Devuelve todos los pares (alto, ancho) con alto*ancho == area."""
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
    """Verifica que el rectángulo no incluya ningún número distinto al propio."""
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
    """Rellena numero.lista_rectangulos_posibles con todos los rectángulos válidos."""
    numero.lista_rectangulos_posibles = []

    # (pseudocódigo L43-L45) Para cada factorización (alto, ancho)
    for alto, ancho in _obtener_factorizaciones(numero.valor):
        # (pseudocódigo L47-L60) Todas las posiciones que incluyen la celda del número
        for fila_inicio in range(numero.fila - (alto - 1), numero.fila + 1):
            for col_inicio in range(numero.columna - (ancho - 1), numero.columna + 1):
                # Verificar que esté dentro del tablero
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

                # Regla Shikaku: no puede incluir otros números
                if _rectangulo_contiene_solo_su_numero(rc, celdas, numero):
                    numero.lista_rectangulos_posibles.append(rc)


# ------------------------------------------------------------
# PASO 5: BACKTRACKING + funciones auxiliares (pseudocódigo L90-L191)
# ------------------------------------------------------------

def _no_colisiona(rc: Rectangulo, ocupado: list[list[bool]]) -> bool:
    """(pseudocódigo L153-L165)"""
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
    """(pseudocódigo L172-L178)"""
    for r in range(rc.fila_inicio, rc.fila_inicio + rc.alto):
        for c in range(rc.columna_inicio, rc.columna_inicio + rc.ancho):
            ocupado[r][c] = True
            dueno[r][c] = id_numero


def _desmarcar(
    rc: Rectangulo,
    ocupado: list[list[bool]],
    dueno: list[list[int]],
) -> None:
    """(pseudocódigo L185-L191)"""
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
    """(pseudocódigo L94-L145)"""

    # (pseudocódigo L96-L98) Caso base: todos los números asignados
    if indice == len(numeros):
        return True

    # (pseudocódigo L101)
    numero_actual = numeros[indice]
    id_rect = indice + 1

    # (pseudocódigo L104-L137) Probar cada rectángulo candidato
    for rc in numero_actual.lista_rectangulos_posibles:

        # (pseudocódigo L107-L113) Verificar si se puede colocar
        if not _no_colisiona(rc, ocupado):
            continue

        # (pseudocódigo L115-L120) Marcar
        _marcar(rc, ocupado, dueno, id_rect)
        solucion[indice] = rc

        # (pseudocódigo L125-L127) Continuar recursión
        if _resolver_recursivo(indice + 1, numeros, ocupado, dueno, solucion):
            return True

        # (pseudocódigo L129-L134) Backtrack
        _desmarcar(rc, ocupado, dueno)

    # (pseudocódigo L140-L145) Sin opción válida
    return False


# ------------------------------------------------------------
# ALGORITMO ResolverShikaku  (pseudocódigo L1-L88)
# ------------------------------------------------------------

def resolver_shikaku(
    celdas: list[list[int]], filas: int, cols: int
) -> list[Rectangulo] | None:
    """
    Devuelve la lista de rectángulos solución (uno por número) o None si no hay solución.
    El índice i de la lista corresponde al número numeros[i] después del ordenamiento MRV.
    """

    # PASO 1 (pseudocódigo L28-L33)
    numeros = _extraer_numeros(celdas, filas, cols)

    # PASO 2 (pseudocódigo L35-L64)
    for n in numeros:
        _generar_rectangulos_posibles(n, celdas, filas, cols)

    # Comprobación temprana: si algún número no tiene candidatos, no hay solución
    if any(len(n.lista_rectangulos_posibles) == 0 for n in numeros):
        return None

    # PASO 3 (pseudocódigo L67-L74): ordenar por menor cantidad de opciones (MRV)
    numeros.sort(key=lambda n: len(n.lista_rectangulos_posibles))

    # PASO 4 (pseudocódigo L76-L81): matrices de ocupación
    ocupado: list[list[bool]] = [[False] * cols for _ in range(filas)]
    dueno: list[list[int]] = [[0] * cols for _ in range(filas)]
    solucion: list[Rectangulo] = [Rectangulo() for _ in numeros]

    # PASO 5 (pseudocódigo L83-L88): backtracking
    if not _resolver_recursivo(0, numeros, ocupado, dueno, solucion):
        return None

    return solucion


# ------------------------------------------------------------
# Conversión a formato de jugada del proyecto ("f0,c0 f1,c1")
# ------------------------------------------------------------

def _rect_a_jugada(rc: Rectangulo) -> str:
    f0 = rc.fila_inicio
    c0 = rc.columna_inicio
    f1 = rc.fila_inicio + rc.alto - 1
    c1 = rc.columna_inicio + rc.ancho - 1
    return f"{f0},{c0} {f1},{c1}"


# ------------------------------------------------------------
# Player
# ------------------------------------------------------------

class Player:

    def __init__(self):
        self.m_jugadas: list[str] = []
        self.m_sin_solucion: bool = False

    def init(self, tablero) -> None:
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
        if self.m_sin_solucion or not self.m_jugadas:
            raise RuntimeError("Optimo: no hay jugadas disponibles.")
        return self.m_jugadas.pop(0)

    def report(self, response) -> None:
        ok, info = response
        if ok:
            print(
                f"[OPT] Region {info['letra']}: area={info['area']}, pista={info['pista']}"
            )
        else:
            print(f"[OPT] Error inesperado: {info}")