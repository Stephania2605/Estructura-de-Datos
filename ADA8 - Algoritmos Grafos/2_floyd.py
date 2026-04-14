

INF = float("inf")

CIUDADES = ["Mérida", "Campeche", "Valladolid", "Cancún", "Chetumal", "Villahermosa"]
IDX = {ciudad: i for i, ciudad in enumerate(CIUDADES)}
N = len(CIUDADES)

ARISTAS = [
    ("Mérida",       "Campeche",      196),
    ("Mérida",       "Valladolid",    160),
    ("Mérida",       "Cancún",        320),
    ("Campeche",     "Villahermosa",  444),
    ("Campeche",     "Chetumal",      520),
    ("Valladolid",   "Cancún",        160),
    ("Valladolid",   "Chetumal",      400),
    ("Cancún",       "Chetumal",      380),
    ("Cancún",       "Campeche",      370),
    ("Chetumal",     "Villahermosa",  600),
]


def construir_matriz(n, aristas, idx):
    """Construye la matriz de distancias inicial."""
    dist = [[INF] * n for _ in range(n)]
    siguiente = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in aristas:
        i, j = idx[u], idx[v]
        dist[i][j] = w
        dist[j][i] = w
        siguiente[i][j] = j
        siguiente[j][i] = i

    return dist, siguiente


def floyd_warshall(dist, siguiente):
   
    n = len(dist)
    for k in range(n):           
        for i in range(n):       
            for j in range(n):   
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    siguiente[i][j] = siguiente[i][k]
    return dist, siguiente


def reconstruir_camino(siguiente, i, j):
    if siguiente[i][j] is None:
        return []
    camino = [i]
    while i != j:
        i = siguiente[i][j]
        camino.append(i)
    return camino

if __name__ == "__main__":
    print("=" * 70)
    print("  ALGORITMO DE FLOYD-WARSHALL")
    print("=" * 70)

    dist, siguiente = construir_matriz(N, ARISTAS, IDX)
    floyd_warshall(dist, siguiente)

    print("\n  MATRIZ DE DISTANCIAS MÍNIMAS (km):\n")
    ancho = 14
    print(" " * 15 + "".join(f"{c[:12]:>{ancho}}" for c in CIUDADES))
    print(" " * 15 + "-" * (ancho * N))
    for i, origen in enumerate(CIUDADES):
        fila = f"  {origen:<13}"
        for j in range(N):
            val = dist[i][j]
            fila += f"{'INF':>{ancho}}" if val == INF else f"{val:>{ancho}}"
        print(fila)

    print("\n  CAMINOS MÁS CORTOS ENTRE PARES:\n")
    print(f"  {'Origen':<15} {'Destino':<15} {'km':>6}  Ruta")
    print("  " + "-" * 65)
    for i, origen in enumerate(CIUDADES):
        for j, destino in enumerate(CIUDADES):
            if i >= j:
                continue
            if dist[i][j] == INF:
                print(f"  {origen:<15} {destino:<15}   Sin ruta")
                continue
            camino_idx = reconstruir_camino(siguiente, i, j)
            camino_str = " → ".join(CIUDADES[k] for k in camino_idx)
            print(f"  {origen:<15} {destino:<15} {dist[i][j]:>5}  {camino_str}")

    print()
