from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

import reglas


SIN_SOLUCION = None


@dataclass
class Numero:
    fila: int
    col: int
    valor: int
    etiqueta: str


@dataclass
class Rectangulo:
    etiqueta: str
    f0: int
    c0: int
    f1: int
    c1: int
    celdas: list[tuple[int, int]] = field(default_factory=list)


def extraer_numeros(celdas: list[list[int]], filas: int, cols: int) -> list[Numero]:
    numeros = []
    indice = 0
    for f in range(filas):
        for c in range(cols):
            if celdas[f][c] > 0:
                numeros.append(
                    Numero(
                        fila=f,
                        col=c,
                        valor=celdas[f][c],
                        etiqueta=reglas.letra_por_indice(indice),
                    )
                )
                indice += 1
    return numeros


def generar_rectangulos_para_numero(
    celdas: list[list[int]], n: Numero, filas: int, cols: int
) -> list[Rectangulo]:
    rectangulos = []
    area = n.valor

    for h in range(1, area + 1):
        if area % h != 0:
            continue

        w = area // h

        for f0 in range(filas - h + 1):
            for c0 in range(cols - w + 1):
                f1 = f0 + h - 1
                c1 = c0 + w - 1

                if reglas.validar_candidato_rectangulo(
                    celdas, n.fila, n.col, f0, c0, f1, c1
                ):
                    rectangulos.append(
                        Rectangulo(
                            etiqueta=n.etiqueta,
                            f0=f0,
                            c0=c0,
                            f1=f1,
                            c1=c1,
                            celdas=reglas.celdas_de(f0, c0, f1, c1),
                        )
                    )

    return rectangulos


def generar_candidatos(
    celdas: list[list[int]], numeros: list[Numero], filas: int, cols: int
):
    candidatos = []

    for n in numeros:
        lista = generar_rectangulos_para_numero(celdas, n, filas, cols)
        if not lista:
            return SIN_SOLUCION
        candidatos.append(lista)

    return candidatos


def producto_cartesiano(candidatos: list[list[Rectangulo]]) -> list[list[Rectangulo]]:
    if not candidatos:
        return [[]]
    return [list(comb) for comb in product(*candidatos)]


def es_solucion_valida(combinacion: list[Rectangulo], filas: int, cols: int) -> bool:
    ocupadas: set[tuple[int, int]] = set()

    for rect in combinacion:
        for celda in rect.celdas:
            if celda in ocupadas:
                return False
            ocupadas.add(celda)

    return len(ocupadas) == filas * cols


def tablero_celda_unica(n: Numero, filas: int, cols: int) -> list[Rectangulo]:
    return [
        Rectangulo(
            etiqueta=n.etiqueta,
            f0=0,
            c0=0,
            f1=filas - 1,
            c1=cols - 1,
            celdas=reglas.celdas_de(0, 0, filas - 1, cols - 1),
        )
    ]


def resolver_shikaku(
    celdas: list[list[int]], filas: int, cols: int
) -> list[Rectangulo] | None:
    if not reglas.tablero_tiene_pistas(celdas, filas, cols):
        return SIN_SOLUCION

    if not reglas.suma_coherente(celdas, filas, cols):
        return SIN_SOLUCION

    numeros = extraer_numeros(celdas, filas, cols)

    if len(numeros) == 1 and numeros[0].valor == filas * cols:
        return tablero_celda_unica(numeros[0], filas, cols)

    candidatos = generar_candidatos(celdas, numeros, filas, cols)
    if candidatos is SIN_SOLUCION:
        return SIN_SOLUCION

    for combinacion in producto_cartesiano(candidatos):
        if es_solucion_valida(combinacion, filas, cols):
            return combinacion

    return SIN_SOLUCION


def _rect_a_jugada(rect: Rectangulo) -> str:
    return f"{rect.f0},{rect.c0} {rect.f1},{rect.c1}"


class Player:

    def __init__(self):
        self.m_Jugadas: list[str] = []
        self.m_SinSolucion = False

    def init(self, tablero):
        filas = tablero.s_Alto
        cols = tablero.s_Ancho
        solucion = resolver_shikaku(tablero.celdas, filas, cols)

        if solucion is SIN_SOLUCION:
            self.m_SinSolucion = True
            self.m_Jugadas = []
            print("Fuerza bruta: SIN SOLUCION para este tablero.")
            return

        self.m_SinSolucion = False
        self.m_Jugadas = [_rect_a_jugada(rect) for rect in solucion]

    def play(self):
        if self.m_SinSolucion or not self.m_Jugadas:
            raise RuntimeError("Fuerza bruta: no hay jugadas disponibles.")
        return self.m_Jugadas.pop(0)

    def report(self, response):
        ok, info = response
        if ok:
            print(
                f"[FB] Region {info['letra']}: area={info['area']}, pista={info['pista']}"
            )
        else:
            print(f"[FB] Error inesperado: {info}")
