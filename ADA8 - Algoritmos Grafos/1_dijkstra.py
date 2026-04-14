
import heapq

grafo = {
    "Mérida":       {"Campeche": 196, "Valladolid": 160, "Cancún": 320},
    "Campeche":     {"Mérida": 196, "Villahermosa": 444, "Chetumal": 520},
    "Valladolid":   {"Mérida": 160, "Cancún": 160, "Chetumal": 400},
    "Cancún":       {"Valladolid": 160, "Campeche": 370, "Chetumal": 380},
    "Chetumal":     {"Campeche": 520, "Valladolid": 400, "Cancún": 380, "Villahermosa": 600},
    "Villahermosa": {"Campeche": 444, "Chetumal": 600},
}

def dijkstra(grafo, inicio):
    distancias = {nodo: float("inf") for nodo in grafo}
    distancias[inicio] = 0
    previo = {nodo: None for nodo in grafo}

    heap = [(0, inicio)]

    while heap:
        dist_actual, nodo_actual = heapq.heappop(heap)

        if dist_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual].items():
            nueva_dist = dist_actual + peso

            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                previo[vecino] = nodo_actual
                heapq.heappush(heap, (nueva_dist, vecino))

    return distancias, previo
def reconstruir_camino(previo, inicio, destino):
    """Reconstruye el camino desde inicio hasta destino usando el dict previo."""
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = previo[actual]
    camino.reverse()
    if camino[0] != inicio:
        return []   
    return camino
if __name__ == "__main__":
    INICIO = "Mérida"
    print("=" * 60)
    print("  ALGORITMO DE DIJKSTRA")
    print(f"  Nodo origen: {INICIO}")
    print("=" * 60)
    distancias, previo = dijkstra(grafo, INICIO)
    print(f"\n  {'Destino':<15} {'Distancia':>10}  Camino")
    print("  " + "-" * 55)
    for nodo, dist in distancias.items():
        if nodo == INICIO:
            continue
        camino = reconstruir_camino(previo, INICIO, nodo)
        camino_str = " → ".join(camino)
        print(f"  {nodo:<15} {dist:>8} km  {camino_str}")

    print()
