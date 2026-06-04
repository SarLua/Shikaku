ALGORITMO ResolverShikaku(tablero)

ENTRADA:
    tablero[][]

SALIDA:
    true si tiene solución
    false si no tiene solución


--------------------------------------------------
ESTRUCTURAS
--------------------------------------------------

Numero:
    fila
    columna
    valor
    listaRectangulosPosibles

Rectangulo:
    filaInicio
    columnaInicio
    alto
    ancho


--------------------------------------------------
PASO 1: OBTENER TODOS LOS NÚMEROS
--------------------------------------------------

numeros <- extraerNumeros(tablero)


--------------------------------------------------
PASO 2: GENERAR RECTÁNGULOS POSIBLES
--------------------------------------------------

PARA cada numero EN numeros HACER

    numero.listaRectangulosPosibles <- []

    factores <- obtenerFactorizaciones(numero.valor)

    PARA cada (alto, ancho) EN factores HACER

        PARA cada posición posible del rectángulo
            que incluya al número HACER

            SI el rectángulo:
                - está dentro del tablero
                - contiene el número
            ENTONCES

                agregar rectángulo a:
                numero.listaRectangulosPosibles

            FIN SI

        FIN PARA

    FIN PARA

FIN PARA


--------------------------------------------------
PASO 3: ORDENAR POR MENOS OPCIONES
--------------------------------------------------

ordenar numeros por:
    tamaño(listaRectangulosPosibles)
    de menor a mayor


--------------------------------------------------
PASO 4: CREAR MATRIZ DE OCUPACIÓN
--------------------------------------------------

ocupado[][] <- falso


--------------------------------------------------
PASO 5: BACKTRACKING
--------------------------------------------------

RETORNAR resolverRecursivo(0)


==================================================
FUNCIÓN RECURSIVA
==================================================

FUNCIÓN resolverRecursivo(indice)

    SI indice == cantidad(numeros)
        RETORNAR true
    FIN SI


    numeroActual <- numeros[indice]


    PARA cada rectangulo EN
        numeroActual.listaRectangulosPosibles HACER

        --------------------------------------------------
        VERIFICAR SI SE PUEDE COLOCAR
        --------------------------------------------------

        SI noColisiona(rectangulo, ocupado)
           Y noGeneraInconsistencias(rectangulo)
        ENTONCES

            --------------------------------------------------
            MARCAR
            --------------------------------------------------

            marcar(rectangulo, ocupado)

            --------------------------------------------------
            CONTINUAR
            --------------------------------------------------

            SI resolverRecursivo(indice + 1)
                RETORNAR true
            FIN SI

            --------------------------------------------------
            BACKTRACK
            --------------------------------------------------

            desmarcar(rectangulo, ocupado)

        FIN SI

    FIN PARA


    --------------------------------------------------
    SI NINGUNA OPCIÓN FUNCIONA
    --------------------------------------------------

    RETORNAR false

FIN FUNCIÓN


==================================================
FUNCIÓN noColisiona
==================================================

FUNCIÓN noColisiona(rectangulo, ocupado)

    PARA cada celda del rectángulo HACER

        SI ocupado[fila][columna] == true
            RETORNAR false
        FIN SI

    FIN PARA

    RETORNAR true

FIN FUNCIÓN


==================================================
FUNCIÓN marcar
==================================================

FUNCIÓN marcar(rectangulo, ocupado)

    PARA cada celda del rectángulo HACER
        ocupado[fila][columna] <- true
    FIN PARA

FIN FUNCIÓN


==================================================
FUNCIÓN desmarcar
==================================================

FUNCIÓN desmarcar(rectangulo, ocupado)

    PARA cada celda del rectángulo HACER
        ocupado[fila][columna] <- false
    FIN PARA

FIN FUNCIÓN