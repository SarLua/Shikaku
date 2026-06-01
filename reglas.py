from __future__ import annotations


def letra_por_indice(n: int) -> str:
    if n < 26:
        return chr(ord("A") + n)
    letra = chr(ord("A") + (n - 26) % 26)
    repeticiones = 2 + (n - 26) // 26
    return letra * repeticiones


def normalizar_esquinas(fila_i, col_i, fila_f, col_f):
    return (
        min(fila_i, fila_f),
        min(col_i, col_f),
        max(fila_i, fila_f),
        max(col_i, col_f),
    )


def calcular_area(r0: int, c0: int, r1: int, c1: int) -> int:
    return (r1 - r0 + 1) * (c1 - c0 + 1)


def celdas_de(f0: int, c0: int, f1: int, c1: int) -> list[tuple[int, int]]:
    return [(f, c) for f in range(f0, f1 + 1) for c in range(c0, c1 + 1)]


def pistas_en_rectangulo(
    celdas: list[list[int]], r0: int, c0: int, r1: int, c1: int
) -> list[int]:
    pistas = []
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if celdas[r][c] > 0:
                pistas.append(celdas[r][c])
    return pistas


def pista_dentro(fila: int, col: int, r0: int, c0: int, r1: int, c1: int) -> bool:
    return r0 <= fila <= r1 and c0 <= col <= c1


def dentro_limites(
    r0: int, c0: int, r1: int, c1: int, alto: int, ancho: int
) -> bool:
    return r0 >= 0 and c0 >= 0 and r1 < alto and c1 < ancho


def validar_area_rectangulo(
    celdas: list[list[int]], r0: int, c0: int, r1: int, c1: int
):
    area = calcular_area(r0, c0, r1, c1)
    pistas = pistas_en_rectangulo(celdas, r0, c0, r1, c1)

    if len(pistas) == 0:
        return False, {"codigo": "sin_pista"}
    if len(pistas) > 1:
        return False, {"codigo": "multiples_pistas"}
    if pistas[0] != area:
        return False, {
            "codigo": "area_incorrecta",
            "area": area,
            "pista": pistas[0],
        }

    return True, pistas[0]


def validar_candidato_rectangulo(
    celdas: list[list[int]],
    fila_pista: int,
    col_pista: int,
    r0: int,
    c0: int,
    r1: int,
    c1: int,
) -> bool:
    if not pista_dentro(fila_pista, col_pista, r0, c0, r1, c1):
        return False
    ok, _ = validar_area_rectangulo(celdas, r0, c0, r1, c1)
    return ok


def suma_pistas(celdas: list[list[int]], filas: int, cols: int) -> int:
    total = 0
    for f in range(filas):
        for c in range(cols):
            if celdas[f][c] > 0:
                total += celdas[f][c]
    return total


def tablero_tiene_pistas(celdas: list[list[int]], filas: int, cols: int) -> bool:
    for f in range(filas):
        for c in range(cols):
            if celdas[f][c] > 0:
                return True
    return False


def suma_coherente(celdas: list[list[int]], filas: int, cols: int) -> bool:
    return suma_pistas(celdas, filas, cols) == filas * cols
