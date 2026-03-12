# 1. Primero definimos la clase para que Python la conozca
class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre

    def esta_vacia(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None

    def __str__(self):
        # Mostramos la pila de forma que la base esté a la izquierda
        return f"{self.nombre}: {self.items}"

# 2. Definimos la función lógica del juego
def hanoi(n, origen, destino, auxiliar):
    if n > 0:
        hanoi(n - 1, origen, auxiliar, destino)
        
        disco = origen.pop()
        destino.push(disco)
        print(f"Moviendo disco {disco} de {origen.nombre} a {destino.nombre}")
        print(f"  Estado: {torre_A} | {torre_B} | {torre_C}\n")
        
        hanoi(n - 1, auxiliar, destino, origen)

# 3. Bloque principal de ejecución
if __name__ == "__main__":
    torre_A = Pila("Torre A")
    torre_B = Pila("Torre B")
    torre_C = Pila("Torre C")

    # Inicializamos con 3 discos
    for disco in [3, 2, 1]:
        torre_A.push(disco)

    print("Estado Inicial:")
    print(f"{torre_A} | {torre_B} | {torre_C}\n")
    
    hanoi(3, torre_A, torre_C, torre_B)
    
    print("¡Juego completado!")