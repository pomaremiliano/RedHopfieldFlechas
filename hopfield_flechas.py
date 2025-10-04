# Red neuronal de hopfield que reconoce flechas 7x7

from random import randint

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


# Aqui ciclamos la matriz de pesos para entrenar la red
def entrenar_hopfield(patrones_vector):
    n = len(patrones_vector[0])
    W = [[0 for _ in range(n)] for _ in range(n)]
    for p in patrones_vector:
        for i in range(n):
            for j in range(n):
                if i != j:
                    W[i][j] += p[i] * p[j]
    W = [[w_ij / len(patrones_vector) for w_ij in w_i] for w_i in W]  # normalizamos
    return W


# Esta funcion sirve para actualizar cada numero de la red
def signo(x):
    return 1 if x >= 0 else -1


# Aqui la red recuerda el patron
def recordar_patron(w, estado_inicial, max_iter=100):
    s = estado_inicial[:]
    n = len(s)
    iteraciones = 0
    cambio = True
    while (
        cambio and iteraciones < max_iter
    ):  # mientras haya cambios y no se pase del maximo de iteraciones que es 100
        cambio = False
        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    suma += w[i][j] * s[j]
            nuevo = signo(suma)
            if nuevo != s[i]:
                s[i] = nuevo
                cambio = True
        iteraciones += 1
    return s, iteraciones  # regresa el estado final y el numero de iteraciones


# Esta funcion agrega el ruido a la matriz
def ruido(v):
    u = v[:]
    num_ruido = randint(1, 7)  # cantidad de elementos a modificar
    indices = set()
    while len(indices) < num_ruido:
        indices.add(randint(0, len(v) - 1))
    for idx in indices:
        u[idx] = -u[idx]
    return u


def main():
    archivos = [
        "flechas/flecha_abajo.txt",
        "flechas/flecha_arriba.txt",
        "flechas/flecha_derecha.txt",
        "flechas/flecha_izquierda.txt", # solo con 4 flechas funciona bien el reconocimiento
        #"flechas/flecha_esquina_abderecha.txt",
        #"flechas/flecha_esquina_abizquierda.txt",
        #"flechas/flecha_esquina_arderecha.txt",
        #"flechas/flecha_esquina_arizquierda.txt",

    ]

    patrones_vector = []
    patrones_binarios = []

    # Cargamos los patrones desde los archivos txt y los guardamos
    for archivo in archivos:
        v, m = cargar_patron_txt(archivo)
        patrones_vector.append(v)
        patrones_binarios.append(m)

    W = entrenar_hopfield(patrones_vector)

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

        v_ruido = ruido(patrones_vector[i])
        print("Ruido: ")
        dibuja_flecha(vector_grid(v_ruido))

        recordado, iters = recordar_patron(W, v_ruido)
        print(f"Patrón después de {iters} iteraciones: ")
        dibuja_flecha(vector_grid(recordado))


main()
