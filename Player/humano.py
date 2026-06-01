class Player:

    MENSAJES = {
        "formato_invalido": "Formato invalido. Use: 0,0 2,1",
        "coordenadas_invalidas": "Coordenadas invalidas. Use fila,col (ej: 0,1)",
        "fuera_limites": "El rectangulo esta fuera de los limites del tablero",
        "sin_pista": "El rectangulo no contiene ninguna pista",
        "multiples_pistas": "Hay mas de un numero en el rectangulo",
    }

    def __init__(self):
        pass

    def init(self, tablero):
        self.m_Tablero = tablero

    def play(self):
        return input("Digite la jugada (fila_ini,col_ini fila_fin,col_fin): ")

    def _mensaje_error(self, info):
        codigo = info.get("codigo")
        if codigo == "celda_ocupada":
            return (
                f"Celda ({info['fila']},{info['col']}) ya ocupada "
                f"por la region '{info['region']}'"
            )
        if codigo == "area_incorrecta":
            return f"Area={info['area']}, pista={info['pista']}"
        return self.MENSAJES.get(codigo, "Jugada invalida")

    def report(self, r):
        ok, info = r
        if ok:
            letra = info["letra"]
            area = info["area"]
            pista = info["pista"]
            print(f"Rectangulo {letra}: area={area}, pista={pista}")
        else:
            print(self._mensaje_error(info))
