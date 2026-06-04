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


==================================================
SEPARACIÓN: HEURÍSTICA vs ALGORITMO EXACTO
==================================================


--------------------------------------------------
HEURÍSTICA: ORDENAMIENTO MRV
--------------------------------------------------

La heurística MRV (Minimum Remaining Values) ordena los números
antes del backtracking para acelerar la búsqueda.

    /**
     * @function aplicarHeuristicaMRV
     * 
     * Ordena la lista de números por cantidad de rectángulos posibles
     * (de menor a mayor) para aplicar la heurística MRV.
     * 
     * @param numeros
     *        Lista de objetos Numero con sus respectivos
     *        listaRectangulosPosibles ya calculados.
     *        Cada Numero contiene:
     *          - fila: posición en filas del número
     *          - columna: posición en columnas del número
     *          - valor: área que debe cubrir el rectángulo
     *          - listaRectangulosPosibles: candidatos geométricos válidos
     * 
     * @return numeros (reordenado)
     *         La misma lista, pero ordenada de menor a mayor
     *         por tamaño de listaRectangulosPosibles.
     *         Números con pocas opciones van primero.
     * 
     * @complexity O(n log n) donde n = cantidad de números
     * 
     * @note Modifica la lista in-place. La ordenación es estable.
     */
    FUNCIÓN aplicarHeuristicaMRV(numeros)

        ordenar numeros por:
            tamaño(listaRectangulosPosibles)
            de menor a mayor

        RETORNAR numeros

    FIN FUNCIÓN

VENTAJA:
    - Resuelve primero números "restrictivos" (pocas opciones)
    - Detecta conflictos temprano
    - Reduce el espacio de búsqueda exponencialmente

TIPO: Heurística de poda inteligente (no es aproximación)
      Garantiza encontrar la solución si existe.


--------------------------------------------------
ALGORITMO EXACTO: BACKTRACKING CON MRV
--------------------------------------------------

El algoritmo exacto combina:
  1. Generación exhaustiva de candidatos (Pasos 1-2)
  2. Poda inteligente con MRV (Paso 3)
  3. Búsqueda exhaustiva con backtracking (Paso 5)

GARANTÍA: Encuentra la solución óptima (o determina que no existe)


    /**
     * @function resolverShikakuExacto
     * 
     * Resuelve un puzzle Shikaku de forma exhaustiva usando backtracking
     * combinado con la heurística MRV para acelerar la búsqueda.
     * 
     * El algoritmo:
     *   1. Extrae todos los números del tablero
     *   2. Genera rectángulos candidatos para cada número
     *   3. Ordena números por cantidad de opciones (MRV)
     *   4. Ejecuta backtracking exhaustivo para encontrar asignación válida
     * 
     * @param tablero
     *        Matriz 2D de tamaño filas × columnas donde:
     *          - tablero[r][c] > 0: contiene un número (pista)
     *          - tablero[r][c] = 0: celda vacía
     *        El valor del número indica el área del rectángulo que lo contiene.
     * 
     * @return boolean
     *         - true: existe solución y se encontró
     *         - false: no existe solución válida para este tablero
     * 
     * @note Usa matrices auxiliares:
     *       - ocupado[][]  : controla qué celdas están asignadas
     *       - dueno[][]    : registra cuál número posee cada celda
     *       - solucion[]   : almacena el rectángulo elegido por cada número
     * 
     * @complexity Peor caso: O(∏ |candidatos_i|) exponencial
     *            Caso promedio: O(n × m) donde n×m = tablero size
     *            MRV reduce dramáticamente la constante exponencial
     */
    FUNCIÓN resolverShikakuExacto(tablero)

        // PASO 1: Extraer números
        numeros <- extraerNumeros(tablero)

        // PASO 2: Generar candidatos
        PARA cada numero EN numeros HACER
            numero.listaRectangulosPosibles <- generarCandidatos(numero)
        FIN PARA

        // Validación temprana
        SI algún número tiene 0 candidatos ENTONCES
            RETORNAR false
        FIN SI

        // PASO 3: Aplicar heurística MRV
        numeros <- aplicarHeuristicaMRV(numeros)

        // PASO 4: Inicializar matrices
        ocupado[][] <- falso
        dueno[][]   <- 0
        solucion[]  <- []

        // PASO 5: Búsqueda exhaustiva con backtracking
        RETORNAR resolverRecursivo(0, numeros, ocupado, dueno, solucion)

    FIN FUNCIÓN


    /**
     * @function resolverRecursivo
     * 
     * Función recursiva que implementa backtracking exhaustivo.
     * Intenta asignar un rectángulo válido a cada número en orden,
     * retrocediendo (backtrack) si alguna rama no conduce a solución.
     * 
     * @param indice
     *        Índice del número actual a resolver (0 <= indice < cantidad(numeros))
     *        Sirve como profundidad en el árbol de recursión.
     * 
     * @param numeros[]
     *        Lista de números ya ordenados por MRV.
     *        El número en numeros[indice] es el que se intenta resolver.
     * 
     * @param ocupado[][]
     *        Matriz booleana que marca qué celdas ya tienen asignación.
     *        - ocupado[r][c] = true: celda (r,c) ya está cubierta
     *        - ocupado[r][c] = false: celda (r,c) está disponible
     *        Se modifica durante la ejecución (marca/desmarcar).
     * 
     * @param dueno[][]
     *        Matriz entera que registra qué número posee cada celda.
     *        - dueno[r][c] = 0: sin asignar
     *        - dueno[r][c] = id: la celda pertenece al número con id
     *        Se modifica durante la ejecución (marca/desmarcar).
     * 
     * @param solucion[]
     *        Vector que almacena el rectángulo elegido para cada número.
     *        - solucion[indice] = Rectangulo asignado a numeros[indice]
     *        Se rellena conforme la recursión avanza.
     * 
     * @return boolean
     *         - true: se encontró una asignación válida desde este punto
     *         - false: no existe asignación válida (requiere backtrack)
     * 
     * @note Esta función implementa:
     *       1. Caso base: cuando indice == cantidad(numeros), retorna true
     *       2. Prueba exhaustiva: for-loop sobre listaRectangulosPosibles
     *       3. Poda: continúa solo si noColisiona()
     *       4. Backtrack: desmarcar y probar siguiente candidato si recursión falla
     * 
     * @complexity O(∏ |candidatos_i| × area_media)
     *            El factor área_media viene de marcar/desmarcar celdas
     */
    FUNCIÓN resolverRecursivo(indice, numeros, ocupado, dueno, solucion)

        // Caso base: todos los números asignados correctamente
        SI indice == cantidad(numeros) ENTONCES
            RETORNAR true (solución encontrada)
        FIN SI

        numeroActual <- numeros[indice]
        idRect <- indice + 1

        // Probar cada candidato para este número
        PARA cada rectangulo EN numeroActual.listaRectangulosPosibles HACER

            // Verificar viabilidad: ¿no colisiona con asignaciones previas?
            SI noColisiona(rectangulo, ocupado) ENTONCES

                // Marcar: reservar estas celdas para este número
                marcar(rectangulo, ocupado, dueno, idRect)
                solucion[indice] <- rectangulo

                // Continuar: intentar resolver el siguiente número
                SI resolverRecursivo(indice + 1, numeros, ocupado, dueno, solucion) ENTONCES
                    RETORNAR true (éxito en rama recursiva)
                FIN SI

                // Backtrack: esta rama no funcionó, deshacer cambios
                desmarcar(rectangulo, ocupado, dueno)

            FIN SI

        FIN PARA

        // Sin opción válida: todos los candidatos fueron rechazados
        RETORNAR false

    FIN FUNCIÓN


COMPLEJIDAD:
    - Peor caso: O(∏ |candidatos_i|) — exponencial puro
    - Caso promedio: MRV reduce dramáticamente el árbol de búsqueda
    - Espacio: O(filas × columnas) para matrices de ocupación


CARACTERÍSTICAS DEL ALGORITMO EXACTO:
    ✓ Completo: encuentra solución si existe
    ✓ Óptimo: la solución encontrada es válida
    ✓ Con poda: MRV acelera la búsqueda
    ✓ Determinista: mismo tablero = mismo resultado