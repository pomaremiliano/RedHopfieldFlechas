# Red neuronal de hopfield que reconoce flechas 7x7
# Usa 8 patrones de flechas pero solo reconoce bien 4 a la vez
# Usa ruido en cruz central o diagonal


# Cargamos los archivos txt y los guardamos en vector
def cargar_patron_txt(ruta):
    matriz = []
    with open(ruta, "r") as file:
        for linea in file:
            fila = [int(x) for x in linea.strip().split()]
            matriz.append(fila)
    v = []
    for fila in matriz:
        for x in fila:
            v.append(1 if x == 1 else -1)  # aqui cambiamos los 1 y 0 por 1 y -1
    return v, matriz


# Despues pasamos el vector a una matriz 7x7
def vector_grid(v, m=7, n=7):
    grid = []
    k = 0
    for _ in range(m):
        fila = []
        for _ in range(n):
            fila.append(v[k])
            k += 1
        grid.append(fila)
    return grid


# Despues dibujamos las flechas con X
def dibuja_flecha(grid):
    for fila in grid:
        linea = "".join("X" if x == 1 else "·" for x in fila)
        print(linea)
    print()


# Aqui ciclamos la matriz de pesos para entrenar la red y ponemos la diagonal T en 0
def entrenar_hopfield(patrones_vector):
    n = len(patrones_vector[0])
    T = [[0 for _ in range(n)] for _ in range(n)]
    for p in patrones_vector:
        for i in range(n):
            for j in range(n):
                T[i][j] += p[i] * p[j]
    # Poner la diagonal en cero
    for i in range(n):
        T[i][i] = 0
    return T


# Esta funcion sirve para actualizar cada numero de la red
def signo(x):
    return 1 if x >= 0 else -1


# Aqui la red recuerda el patron
def recordar_patron(T, estado_inicial, max_iter=100):
    s = estado_inicial[:]
    n = len(s)
    iteraciones = 0
    cambio = True
    while cambio and iteraciones < max_iter:
        # mientras haya cambios y no se pase del maximo de iteraciones que es 100
        cambio = False
        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    suma += T[i][j] * s[j]
            nuevo = signo(suma)
            if nuevo != s[i]:
                s[i] = nuevo
                cambio = True
        iteraciones += 1
    return s, iteraciones  # regresa el estado final y el numero de iteraciones


# Para agregar ruido, primero clasificamos por cercania
def cercania(a, b):
    d = 0
    for x, y in zip(a, b):
        if x != y:
            d += 1
    return d


def clasificar_por_cercania(v, patrones_vec, etiquetas):
    mejor_label = None
    mejor_dist = None
    for label in etiquetas:
        for p in patrones_vec:
            d = cercania(v, p)
            if mejor_dist is None or d < mejor_dist:
                mejor_dist = d
                mejor_label = label
    return mejor_label, mejor_dist


# Despues hacemos 2 tipos de ruido para cubrir la matriz
# cruz central y diagonal
def cruz_central():
    M = 7
    N = 7
    r = [[0 for _ in range(N)] for _ in range(M)]
    mid = 3
    for j in range(N):
        r[mid][j] = 1
    for i in range(M):
        r[i][mid] = 1
    return r


def diagonal():
    M = 7
    N = 7
    r = [[0 for _ in range(N)] for _ in range(M)]
    for i in range(M):
        r[i][i] = 1
    return r


def ruido(v, matriz_ruido):
    # convertimos la matriz de ruido a vector
    vector_ruido = []
    for fila in matriz_ruido:
        for x in fila:
            vector_ruido.append(x)
    v_ruido = v[:]
    for i in range(len(v_ruido)):  # voltear signo si es 1
        if vector_ruido[i] == 1:
            v_ruido[i] = -v_ruido[i]
    return v_ruido


def main():
    archivos = [
        "flechas/flecha_abajo.txt",
        "flechas/flecha_arriba.txt",
        "flechas/flecha_derecha.txt",
        "flechas/flecha_izquierda.txt",  # solo con 4 flechas a la vez funciona bien el reconocimiento
        # "flechas/flecha_esquina_abderecha.txt",
        # "flechas/flecha_esquina_abizquierda.txt",
        # "flechas/flecha_esquina_arderecha.txt",
        # "flechas/flecha_esquina_arizquierda.txt",
    ]

    patrones_vector = []
    patrones_binarios = []

    # Cargamos los patrones desde los archivos txt y los guardamos
    for archivo in archivos:
        v, m = cargar_patron_txt(archivo)
        patrones_vector.append(v)
        patrones_binarios.append(m)

    T = entrenar_hopfield(patrones_vector)

    flechas = [
        "abajo",
        "arriba",
        "derecha",
        "izquierda",
        "esquina abajo derecha",
        "esquina abajo izquierda",
        "esquina arriba derecha",
        "esquina arriba izquierda",
    ]  # estas flechas son para identificar cada patron en la salida
    for i in range(len(patrones_vector)):
        print(f"Objetivo: {flechas[i]}")
        print("Patrón del archivo: ")
        dibuja_flecha(patrones_binarios[i])

        # Puedes elegir el tipo de ruido
        matriz_ruido = diagonal()
        # matriz_ruido = cruz_central()
        v_ruido = ruido(patrones_vector[i], matriz_ruido)
        print("Ruido: ")
        dibuja_flecha(vector_grid(v_ruido))

        recordado, iters = recordar_patron(T, v_ruido)
        print(f"Patrón después de {iters} iteraciones: ")
        dibuja_flecha(vector_grid(recordado))

        if (recordado not in patrones_vector):  # si no encuentra el patron, lo clasifica por cercania
            etiqueta = clasificar_por_cercania(recordado, patrones_vector, flechas)
            print(f"Clasificado como: {etiqueta}")


main()
