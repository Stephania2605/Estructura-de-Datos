

CIUDADES = ["Mérida", "Campeche", "Valladolid", "Cancún", "Chetumal",
            "Villahermosa", "Oaxaca", "Veracruz"]

ARISTAS = [
    (196, "Mérida",       "Campeche"),
    (160, "Mérida",       "Valladolid"),
    (320, "Mérida",       "Cancún"),
    (444, "Campeche",     "Villahermosa"),
    (520, "Campeche",     "Chetumal"),
    (370, "Cancún",       "Campeche"),
    (160, "Valladolid",   "Cancún"),
    (400, "Valladolid",   "Chetumal"),
    (380, "Cancún",       "Chetumal"),
    (600, "Chetumal",     "Villahermosa"),
    (340, "Veracruz",     "Oaxaca"),
    (520, "Chiapas" if False else "Oaxaca", "Chetumal"),   
    (360, "Veracruz",     "Villahermosa"),
    (480, "Oaxaca",       "Villahermosa"),
    (700, "Veracruz",     "Mérida"),
]

ARISTAS = [(c, u, v) for c, u, v in ARISTAS
           if u in CIUDADES and v in CIUDADES]

class UnionFind:
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}  
        self.rango  = {n: 0 for n in nodos}

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])  
        return self.padre[x]

    def unir(self, x, y):
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)
        if raiz_x == raiz_y:
            return False   
        if self.rango[raiz_x] < self.rango[raiz_y]:
            raiz_x, raiz_y = raiz_y, raiz_x
        self.padre[raiz_y] = raiz_x
        if self.rango[raiz_x] == self.rango[raiz_y]:
            self.rango[raiz_x] += 1
        return True


def kruskal(ciudades, aristas):
   
    aristas_ordenadas = sorted(aristas, key=lambda x: x[0])

    uf = UnionFind(ciudades)
    mst = []
    costo_total = 0

    print("  PROCESO — Evaluando aristas en orden de costo:\n")
    print(f"  {'Arista':<35} {'Costo':>6}  Decisión")
    print("  " + "-" * 58)

    for costo, u, v in aristas_ordenadas:
        if uf.unir(u, v):
            mst.append((costo, u, v))
            costo_total += costo
            decision = "ACEPTADA ✓ (añadida al MST)"
        else:
            decision = "RECHAZADA ✗ (formaría ciclo)"

        arista_str = f"{u} — {v}"
        print(f"  {arista_str:<35} {costo:>6}  {decision}")

        if len(mst) == len(ciudades) - 1:
            break

    return mst, costo_total

if __name__ == "__main__":
    print("=" * 65)
    print("  ALGORITMO DE KRUSKAL — Árbol de Expansión Mínima")
    print("=" * 65)
    print(f"\n  Nodos: {len(CIUDADES)} ciudades   Aristas disponibles: {len(ARISTAS)}\n")

    mst, costo_total = kruskal(CIUDADES, ARISTAS)

    print(f"\n  ÁRBOL DE EXPANSIÓN MÍNIMA (MST):\n")
    print(f"  {'Arista':<35} {'Costo':>6}")
    print("  " + "-" * 42)
    for costo, u, v in mst:
        print(f"  {u} — {v:<25} {costo:>6} km")
    print("  " + "-" * 42)
    print(f"  {'COSTO TOTAL':<35} {costo_total:>6} km")
    print(f"\n  Aristas en el MST: {len(mst)}  (debe ser {len(CIUDADES)-1} = nodos - 1)\n")
