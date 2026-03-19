"""
SISTEMA DE POSTRES
Estructura: Arreglo ordenado alfabéticamente de postres,
donde cada postre apunta a una lista enlazada de ingredientes.
"""


class Nodo:
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente
        self.siguiente = None



class ListaIngredientes:
    def __init__(self):
        self.cabeza = None  

    
    def imprimir(self):
        if self.cabeza is None:
            print("  (lista vacía)")
            return
        actual = self.cabeza
        while actual:
            print(f"  - {actual.ingrediente}")
            actual = actual.siguiente

   
    def insertar(self, ingrediente):
        actual = self.cabeza
        while actual:
            if actual.ingrediente.lower() == ingrediente.lower():
                print(f"  '{ingrediente}' ya existe en la lista.")
                return
            actual = actual.siguiente

        nuevo = Nodo(ingrediente)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        print(f"  Ingrediente '{ingrediente}' insertado.")

    def eliminar(self, ingrediente):
        if self.cabeza is None:
            print("  La lista está vacía, no hay nada que eliminar.")
            return

        if self.cabeza.ingrediente.lower() == ingrediente.lower():
            self.cabeza = self.cabeza.siguiente
            print(f"  Ingrediente '{ingrediente}' eliminado.")
            return

        anterior = self.cabeza
        actual = self.cabeza.siguiente
        while actual:
            if actual.ingrediente.lower() == ingrediente.lower():
                anterior.siguiente = actual.siguiente
                print(f"  Ingrediente '{ingrediente}' eliminado.")
                return
            anterior = actual
            actual = actual.siguiente

        print(f"  Ingrediente '{ingrediente}' no encontrado.")


class SistemaPostres:
    def __init__(self):
        self.postres = []

    def _buscar(self, nombre):
        izq, der = 0, len(self.postres) - 1
        nombre_lower = nombre.lower()
        while izq <= der:
            mid = (izq + der) // 2
            actual = self.postres[mid][0].lower()
            if actual == nombre_lower:
                return mid
            elif nombre_lower < actual:
                der = mid - 1
            else:
                izq = mid + 1
        return -1

    def _posicion_insercion(self, nombre):
        nombre_lower = nombre.lower()
        for i, (n, _) in enumerate(self.postres):
            if nombre_lower < n.lower():
                return i
        return len(self.postres)

    def imprimir_ingredientes(self, nombre):
        idx = self._buscar(nombre)
        if idx == -1:
            print(f"Postre '{nombre}' no encontrado.")
            return
        print(f"Ingredientes de '{self.postres[idx][0]}':")
        self.postres[idx][1].imprimir()

    def insertar_ingrediente(self, nombre_postre, ingrediente):
        idx = self._buscar(nombre_postre)
        if idx == -1:
            print(f"Postre '{nombre_postre}' no encontrado.")
            return
        self.postres[idx][1].insertar(ingrediente)

    def eliminar_ingrediente(self, nombre_postre, ingrediente):
        idx = self._buscar(nombre_postre)
        if idx == -1:
            print(f"Postre '{nombre_postre}' no encontrado.")
            return
        self.postres[idx][1].eliminar(ingrediente)

    def alta_postre(self, nombre, ingredientes):
        if self._buscar(nombre) != -1:
            print(f"El postre '{nombre}' ya existe.")
            return
        lista = ListaIngredientes()
        for ing in ingredientes:
            lista.insertar(ing)
        pos = self._posicion_insercion(nombre)
        self.postres.insert(pos, (nombre, lista))
        print(f"Postre '{nombre}' dado de alta correctamente.")

    def baja_postre(self, nombre):
        idx = self._buscar(nombre)
        if idx == -1:
            print(f"Postre '{nombre}' no encontrado.")
            return
        self.postres.pop(idx)
        print(f"Postre '{nombre}' eliminado del sistema.")

    def listar_postres(self):
        if not self.postres:
            print("No hay postres registrados.")
            return
        print("Postres registrados (orden alfabético):")
        for nombre, _ in self.postres:
            print(f"  * {nombre}")


def menu():
    sistema = SistemaPostres()

    sistema.alta_postre("Cheesecake", ["Queso crema", "Galletas", "Mantequilla", "Azúcar"])
    sistema.alta_postre("Flan", ["Huevos", "Leche", "Azúcar", "Vainilla"])
    sistema.alta_postre("Brownie", ["Chocolate", "Harina", "Mantequilla", "Huevos"])

    while True:
        print("\n===== SISTEMA DE POSTRES =====")
        print("1. Ver ingredientes de un postre")
        print("2. Insertar ingrediente a un postre")
        print("3. Eliminar ingrediente de un postre")
        print("4. Dar de alta un postre")
        print("5. Dar de baja un postre")
        print("6. Listar todos los postres")
        print("0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del postre: ").strip()
            sistema.imprimir_ingredientes(nombre)

        elif opcion == "2":
            nombre = input("Nombre del postre: ").strip()
            ing = input("Ingrediente a insertar: ").strip()
            sistema.insertar_ingrediente(nombre, ing)

        elif opcion == "3":
            nombre = input("Nombre del postre: ").strip()
            ing = input("Ingrediente a eliminar: ").strip()
            sistema.eliminar_ingrediente(nombre, ing)

        elif opcion == "4":
            nombre = input("Nombre del nuevo postre: ").strip()
            ings = input("Ingredientes (separados por coma): ").strip()
            lista = [i.strip() for i in ings.split(",") if i.strip()]
            sistema.alta_postre(nombre, lista)

        elif opcion == "5":
            nombre = input("Nombre del postre a eliminar: ").strip()
            sistema.baja_postre(nombre)

        elif opcion == "6":
            sistema.listar_postres()

        elif opcion == "0":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
