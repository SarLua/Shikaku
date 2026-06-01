import Ejemplos.Lectura_Archivos as lect
import reglas


class Tablero:

    s_Tablero = None
    s_Alto = None
    s_Ancho = None
    celdas = None
    s_Completo = None
    s_RegionIndex = None

    def __init__(self, name_tablero):
        tablero = lect.lectura_tablero(name_tablero)
        self.s_Alto = tablero.s_Alto
        self.s_Ancho = tablero.s_Ancho
        self.celdas = tablero.celdas
        self.s_Completo = False
        self.s_RegionIndex = 0
        self.s_Tablero = [("", False)] * (self.s_Alto * self.s_Ancho)

    def finished(self):
        return self.s_Completo

    def _idx(self, fila, col):
        return fila * self.s_Ancho + col

    def _siguiente_letra(self):
        letra = reglas.letra_por_indice(self.s_RegionIndex)
        self.s_RegionIndex += 1
        return letra

    def _normalizar(self, fila_i, col_i, fila_f, col_f):
        return reglas.normalizar_esquinas(fila_i, col_i, fila_f, col_f)

    def rectangulo_valido(self, fila_i, col_i, fila_f, col_f):
        r0, c0, r1, c1 = self._normalizar(fila_i, col_i, fila_f, col_f)

        if not reglas.dentro_limites(r0, c0, r1, c1, self.s_Alto, self.s_Ancho):
            return False, {"codigo": "fuera_limites"}

        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                valor, ocupada = self.s_Tablero[self._idx(r, c)]
                if ocupada:
                    return False, {
                        "codigo": "celda_ocupada",
                        "fila": r,
                        "col": c,
                        "region": valor,
                    }

        return True, (r0, c0, r1, c1)

    def area_rectangulo(self, r0, c0, r1, c1):
        return reglas.validar_area_rectangulo(self.celdas, r0, c0, r1, c1)

    def _colocar(self, letra, r0, c0, r1, c1):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                self.s_Tablero[self._idx(r, c)] = (letra, True)
        self.s_Completo = all(ocupada for _, ocupada in self.s_Tablero)

    def _parsear_jugada(self, jugada):
        """
        Formato esperado: 0,0 2,1
        - fila,col esquina inicial (base 0)
        - fila,col esquina final   (base 0, inclusiva)
        """
        partes = jugada.strip().split()
        if len(partes) != 2:
            return None, {"codigo": "formato_invalido"}

        try:
            fi, ci = map(int, partes[0].split(","))
            ff, cf = map(int, partes[1].split(","))
        except ValueError:
            return None, {"codigo": "coordenadas_invalidas"}

        return (fi, ci, ff, cf), None

    def click(self, jugada):
        """
        Procesa una jugada del jugador.
        Exito:  (True,  {"letra": str, "area": int, "pista": int})
        Error:  (False, {"codigo": str, ...})
        """
        parsed, err = self._parsear_jugada(jugada)
        if err:
            return False, err

        fi, ci, ff, cf = parsed

        ok, res = self.rectangulo_valido(fi, ci, ff, cf)
        if not ok:
            return False, res

        r0, c0, r1, c1 = res
        ok, res = self.area_rectangulo(r0, c0, r1, c1)
        if not ok:
            return False, res

        pista = res
        area = reglas.calcular_area(r0, c0, r1, c1)
        letra = self._siguiente_letra()
        self._colocar(letra, r0, c0, r1, c1)
        return True, {"letra": letra, "area": area, "pista": pista}

    def _valor_celda(self, fila, col):
        letra, ocupada = self.s_Tablero[self._idx(fila, col)]
        if ocupada:
            return letra
        pista = self.celdas[fila][col]
        return str(pista) if pista > 0 else " "

    def __str__(self):
        h = "     " + "".join("+---" for _ in range(self.s_Ancho)) + "+"
        s = "     " + "".join("  c " for _ in range(self.s_Ancho)) + "\n"
        s += "     "
        s += "".join("  " + str(v) + " " for v in range(self.s_Ancho))
        s += "\n     " + "".join("  | " for _ in range(self.s_Ancho))
        s += "\n     " + "".join("  V " for _ in range(self.s_Ancho))
        s += "\n" + h + "\nr0-> | "

        for r in range(self.s_Alto):
            s += " ".join(
                self._valor_celda(r, c) + " |"
                for c in range(self.s_Ancho)
            )
            s += "\n" + h
            if r < self.s_Alto - 1:
                s += "\nr" + str(r + 1) + "-> | "
        return s
