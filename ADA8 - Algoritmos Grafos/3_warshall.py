

NODOS = ["Login", "BD", "Cache", "API", "Reportes", "Email"]
IDX   = {n: i for i, n in enumerate(NODOS)}
N     = len(NODOS)

ARISTAS_DIRIGIDAS = [
    ("Login",    "BD"),
    ("Login",    "Cache"),
    ("API",      "Login"),
    ("API",      "BD"),
    ("API",      "Cache"),
    ("Reportes", "BD"),
    ("Reportes", "Email"),
    ("Email",    "BD"),
]


def construir_matriz_alcance(n, aristas, idx):
    """Matriz booleana de adyacencia directa."""
    R = [[False] * n for _ in range(n)]
    for i in range(n):
        R[i][i] = True          
    for u, v in aristas:
        R[idx[u]][idx[v]] = True
    return R


def warshall(R):
    n = len(R)
    for k in range(n):        
        for i in range(n):   
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    return R


def imprimir_matriz(R, nodos, titulo=""):
    print(f"\n  {titulo}")
    ancho = 10
    print(" " * 12 + "".join(f"{n[:8]:>{ancho}}" for n in nodos))
    print(" " * 12 + "-" * (ancho * len(nodos)))
    for i, origen in enumerate(nodos):
        fila = f"  {origen:<10}"
        for j in range(len(nodos)):
            simbolo = " SI" if R[i][j] else " NO"
            fila += f"{simbolo:>{ancho}}"
        print(fila)


if __name__ == "__main__":
    print("=" * 65)
    print("  ALGORITMO DE WARSHALL — Cierre Transitivo")
    print("=" * 65)

    print("\n  Grafo dirigido (A → B = A puede alcanzar directamente a B):")
    for u, v in ARISTAS_DIRIGIDAS:
        print(f"    {u} → {v}")

    R_inicial = construir_matriz_alcance(N, ARISTAS_DIRIGIDAS, IDX)
    imprimir_matriz(R_inicial, NODOS, "MATRIZ DE ADYACENCIA INICIAL (conexiones directas):")

    R_cierre = [fila[:] for fila in R_inicial]   
    warshall(R_cierre)
    imprimir_matriz(R_cierre, NODOS, "CIERRE TRANSITIVO (conexiones directas e INDIRECTAS):")

    print("\n  ANÁLISIS DE ALCANZABILIDAD:")
    print(f"  {'Origen':<12} {'Destino':<12}  Alcanzable?  Nota")
    print("  " + "-" * 55)
    consultas = [
        ("API",      "Email",    "API → Login → ... → Email?"),
        ("Login",    "Email",    "Login no tiene ruta a Email"),
        ("Reportes", "Cache",    "Reportes → BD → Cache?"),
        ("Email",    "Login",    "Email no apunta hacia Login"),
        ("Cache",    "BD",       "Cache no tiene salidas"),
    ]
    for origen, destino, nota in consultas:
        i, j = IDX[origen], IDX[destino]
        res = "SI" if R_cierre[i][j] else "NO"
        print(f"  {origen:<12} {destino:<12}  {res:<11}  {nota}")

    print()
