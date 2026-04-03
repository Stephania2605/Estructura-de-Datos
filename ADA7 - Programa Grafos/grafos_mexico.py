
import heapq
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx


ESTADOS = [
    "Yucatán",
    "Campeche",
    "Quintana Roo",
    "Tabasco",
    "Chiapas",
    "Veracruz",
    "Oaxaca",
]

CONEXIONES = [
    ("Yucatán",     "Campeche",      196),
    ("Yucatán",     "Quintana Roo",  320),
    ("Campeche",    "Quintana Roo",  370),
    ("Campeche",    "Tabasco",       444),
    ("Campeche",    "Chiapas",       530),
    ("Quintana Roo","Chiapas",       690),
    ("Tabasco",     "Chiapas",       290),
    ("Tabasco",     "Veracruz",      360),
    ("Chiapas",     "Oaxaca",        520),
    ("Veracruz",    "Oaxaca",        340),
    ("Veracruz",    "Yucatán",       900),   
]

def construir_grafo(conexiones):
    grafo = {estado: {} for estado in ESTADOS}
    for u, v, costo in conexiones:
        grafo[u][v] = costo
        grafo[v][u] = costo
    return grafo

grafo = construir_grafo(CONEXIONES)


def mostrar_relaciones(grafo):
    print("=" * 60)
    print("  INCISO E) ESTADOS Y SUS RELACIONES")
    print("=" * 60)
    for estado, vecinos in grafo.items():
        print(f"\n  {estado}:")
        for vecino, costo in vecinos.items():
            print(f"      → {vecino:15s}  costo: {costo} km")
    print()


def camino_hamiltoniano(grafo, inicio="Yucatán"):
    """
    Encuentra el camino Hamiltoniano de menor costo desde 'inicio'
    visitando todos los estados exactamente una vez.
    Usa backtracking (fuerza bruta sobre permutaciones de los demás nodos).
    """
    otros = [e for e in ESTADOS if e != inicio]
    mejor_costo = float("inf")
    mejor_ruta = None

    for perm in itertools.permutations(otros):
        ruta = [inicio] + list(perm)
        costo = 0
        valido = True
        for i in range(len(ruta) - 1):
            u, v = ruta[i], ruta[i + 1]
            if v in grafo[u]:
                costo += grafo[u][v]
            else:
                valido = False
                break
        if valido and costo < mejor_costo:
            mejor_costo = costo
            mejor_ruta = ruta

    return mejor_ruta, mejor_costo


def recorrido_con_repeticion(grafo, inicio="Yucatán"):
    """
    Encuentra el recorrido más corto que visita todos los estados
    REPITIENDO AL MENOS UNO de ellos obligatoriamente.
    Estrategia: toma el camino hamiltoniano óptimo e inserta
    una visita extra al nodo de menor costo de reinsertar (ida y vuelta
    desde algún punto de la ruta), garantizando así la repetición.
    """
    ruta_base, _ = camino_hamiltoniano(grafo, inicio)

    mejor_extra = float("inf")
    mejor_insercion = None  
    for i, estado in enumerate(ruta_base):
        for vecino, costo_ida in grafo[estado].items():
            if vecino in ruta_base:  
                costo_vuelta = grafo[vecino].get(estado, float("inf"))
                extra = costo_ida + costo_vuelta
                if extra < mejor_extra:
                    mejor_extra = extra
                    mejor_insercion = (i + 1, vecino)

    pos, repetido = mejor_insercion
    ruta_con_rep = ruta_base[:pos] + [repetido] + ruta_base[pos:]

    costo_total = 0
    for i in range(len(ruta_con_rep) - 1):
        u, v = ruta_con_rep[i], ruta_con_rep[i + 1]
        costo_total += grafo[u][v]

    return ruta_con_rep, costo_total


def dibujar_grafo(grafo, ruta_sin_rep=None, ruta_con_rep=None):
    """Dibuja el grafo con NetworkX y Matplotlib."""
    G = nx.Graph()
    for u, vecinos in grafo.items():
        for v, w in vecinos.items():
            G.add_edge(u, v, weight=w)

    pos = {
        "Yucatán":      (2.0,  2.0),
        "Campeche":     (1.0,  1.2),
        "Quintana Roo": (2.8,  1.0),
        "Tabasco":      (0.2,  0.5),
        "Chiapas":      (1.2, -0.5),
        "Veracruz":     (-0.8, 0.8),
        "Oaxaca":       (0.0, -0.8),
    }

    fig, axes = plt.subplots(1, 3, figsize=(22, 8))
    fig.patch.set_facecolor("#0d1117")

    titulos = [
        "Grafo Completo\n(todos los estados y conexiones)",
        "Inciso A) Sin repetir\n(Camino Hamiltoniano)",
        "Inciso B) Con repetición\n(al menos un estado repetido)",
    ]
    rutas = [None, ruta_sin_rep, ruta_con_rep]

    edge_labels = nx.get_edge_attributes(G, "weight")

    for ax, titulo, ruta in zip(axes, titulos, rutas):
        ax.set_facecolor("#0d1117")
        ax.set_title(titulo, color="white", fontsize=11, pad=12,
                     fontfamily="monospace")

        nx.draw_networkx_edges(G, pos, ax=ax,
                               edge_color="#334155", width=1.5,
                               alpha=0.6)

        if ruta:
            edges_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
            edge_colors_ruta = []
            for e in edges_ruta:
                u, v = e
                if G.has_edge(u, v):
                    edge_colors_ruta.append("#f59e0b")
                else:
                    edge_colors_ruta.append("#ef4444")
            nx.draw_networkx_edges(G, pos, edgelist=edges_ruta,
                                   ax=ax, edge_color="#f59e0b",
                                   width=3.5, arrows=False)

        nx.draw_networkx_nodes(G, pos, ax=ax,
                               node_color="#1e40af",
                               node_size=800,
                               edgecolors="#60a5fa", linewidths=2)

        nx.draw_networkx_labels(G, pos, ax=ax,
                                font_color="white",
                                font_size=7.5,
                                font_weight="bold")

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     ax=ax,
                                     font_color="#94a3b8",
                                     font_size=6.5,
                                     bbox=dict(boxstyle="round,pad=0.2",
                                               fc="#0d1117", ec="none",
                                               alpha=0.7))
        ax.axis("off")

    plt.suptitle("Grafos — 7 Estados de la República Mexicana",
                 color="white", fontsize=15, fontweight="bold",
                 fontfamily="monospace", y=1.01)
    plt.tight_layout()
    import os
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafo_mexico.png")
    plt.savefig(ruta, dpi=150, bbox_inches="tight", facecolor="#0d1117")
    print(f"  [OK] Imagen guardada en: {ruta}")
    plt.show()


def main():
    print("\n" + "=" * 60)
    print("   GRAFOS — 7 ESTADOS DE LA REPÚBLICA MEXICANA")
    print("=" * 60)

    mostrar_relaciones(grafo)

    print("=" * 60)
    print("  INCISO A) RECORRIDO SIN REPETIR ESTADOS")
    print("  (Camino Hamiltoniano de menor costo)")
    print("=" * 60)
    ruta_a, costo_a = camino_hamiltoniano(grafo, inicio="Yucatán")
    if ruta_a:
        print("\n  Ruta encontrada:")
        for i, estado in enumerate(ruta_a):
            if i < len(ruta_a) - 1:
                sig = ruta_a[i + 1]
                print(f"    {estado:15s} ──({grafo[estado][sig]} km)──► {sig}")
            else:
                print(f"    {estado:15s} [DESTINO FINAL]")
        print(f"\n   Costo total (inciso a): {costo_a} km\n")
    else:
        print("   No existe un camino hamiltoniano directo.")

    print("=" * 60)
    print("  INCISO B) RECORRIDO REPITIENDO AL MENOS UN ESTADO")
    print("=" * 60)
    ruta_b, costo_b = recorrido_con_repeticion(grafo, inicio="Yucatán")
    print("\n  Ruta encontrada:")
    for i, estado in enumerate(ruta_b):
        if i < len(ruta_b) - 1:
            sig = ruta_b[i + 1]
            costo_seg = grafo.get(estado, {}).get(sig, "—")
            print(f"    {estado:15s} ──({costo_seg} km)──► {sig}")
        else:
            print(f"    {estado:15s} [DESTINO FINAL]")

    repetidos = [e for e in ESTADOS if ruta_b.count(e) > 1]
    print(f"\n  Estados repetidos: {repetidos if repetidos else 'ninguno'}")
    print(f"\n  Costo total (inciso b): {costo_b} km\n")

    print("=" * 60)
    print("  INCISO C) RESUMEN DE COSTOS")
    print("=" * 60)
    print(f"\n  Inciso a) Sin repetir   → {costo_a} km")
    print(f"  Inciso b) Con repetición → {costo_b} km")
    diferencia = abs(costo_b - costo_a)
    print(f"  Diferencia              → {diferencia} km\n")

    print("=" * 60)
    print("  INCISO D) DIBUJANDO EL GRAFO...")
    print("=" * 60)
    dibujar_grafo(grafo, ruta_sin_rep=ruta_a, ruta_con_rep=ruta_b)

if __name__ == "__main__":
    main()
