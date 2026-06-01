from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TableroLeido:
    s_Alto: int = 0
    s_Ancho: int = 0
    celdas: list[list[int]] = field(default_factory=list)


def lectura_tablero(name: str) -> TableroLeido:
    t = TableroLeido()
    try:
        with open(name, encoding="utf-8") as lect:
            primera = lect.readline().split()
            if len(primera) < 2:
                print("Lectura de archivo: Formato incorrecto en la primera linea")
                return t

            t.s_Alto = int(primera[0])
            t.s_Ancho = int(primera[1])
            t.celdas = [[0] * t.s_Ancho for _ in range(t.s_Alto)]

            for linea in lect:
                linea = linea.strip()
                if not linea:
                    continue

                partes = linea.split()
                if len(partes) < 2 or "," not in partes[1]:
                    print(
                        "Lectura de archivo: Formato incorrecto en una linea de coordenadas"
                    )
                    continue

                valor = int(partes[0])
                fila_str, col_str = partes[1].split(",", 1)
                fila = int(fila_str)
                col = int(col_str)

                if fila < 0 or fila >= t.s_Alto or col < 0 or col >= t.s_Ancho:
                    print(
                        "Lectura de archivo: Formato incorrecto en una linea de coordenadas"
                    )
                    continue

                t.celdas[fila][col] = valor

    except OSError:
        print("Lectura de archivo: Error al leer el tablero")
        return t

    return t


def vacio(t: TableroLeido) -> None:
    """Manejo de excepcion: el tablero esta vacio."""
    pass


def suma_num(t: TableroLeido) -> None:
    """Manejo de excepcion: los numeros suman mas que sus dimensiones."""
    pass
