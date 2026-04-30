

def shell_sort(arr):
    n = len(arr)
    gap = n // 2                        # Brecha inicial
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Desplaza elementos mayores que temp hacia la derecha
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2                       # Reduce la brecha a la mitad
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]        # Pivote = elemento del medio
    menores  = [x for x in arr if x <  pivote]
    iguales  = [x for x in arr if x == pivote]
    mayores  = [x for x in arr if x >  pivote]
    return quick_sort(menores) + iguales + quick_sort(mayores)

def heapify(arr, n, i):
    """Mantiene la propiedad de heap máximo en el subárbol con raíz i."""
    mayor = i
    izq   = 2 * i + 1
    der   = 2 * i + 2
    if izq < n and arr[izq] > arr[mayor]:
        mayor = izq
    if der < n and arr[der] > arr[mayor]:
        mayor = der
    if mayor != i:
        arr[i], arr[mayor] = arr[mayor], arr[i]
        heapify(arr, n, mayor)

def heap_sort(arr):
    n = len(arr)
    # Construir heap máximo
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    # Extraer elementos del heap uno a uno
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]   # Mover raíz al final
        heapify(arr, i, 0)
    return arr


def counting_sort_por_digito(arr, exp):
    """Counting Sort estable por dígito en posición 'exp'."""
    n = len(arr)
    salida  = [0] * n
    conteo  = [0] * 10

    for num in arr:
        indice = (num // exp) % 10
        conteo[indice] += 1

    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    for i in range(n - 1, -1, -1):
        indice = (arr[i] // exp) % 10
        salida[conteo[indice] - 1] = arr[i]
        conteo[indice] -= 1

    for i in range(n):
        arr[i] = salida[i]

def radix_sort(arr):
    if not arr:
        return arr
    maximo = max(arr)
    exp = 1
    while maximo // exp > 0:
        counting_sort_por_digito(arr, exp)
        exp *= 10
    return arr


def pedir_numeros():
    """Solicita al usuario la cantidad de números y los números."""
    while True:
        try:
            cantidad = int(input("\n¿Cuántos números deseas ordenar? "))
            if cantidad <= 0:
                print("  ✖ Ingresa un número mayor a 0.")
                continue
            break
        except ValueError:
            print("  ✖ Entrada inválida. Escribe un número entero.")

    numeros = []
    print(f"Ingresa {cantidad} número(s) entero(s):")
    for i in range(cantidad):
        while True:
            try:
                n = int(input(f"  Número {i + 1}: "))
                numeros.append(n)
                break
            except ValueError:
                print("  ✖ Entrada inválida. Escribe un número entero.")
    return numeros


def mostrar_resultado(original, ordenado, metodo):
    print(f"\n{'─'*45}")
    print(f"  Método : {metodo}")
    print(f"  Antes  : {original}")
    print(f"  Después: {ordenado}")
    print(f"{'─'*45}")




def menu():
    print("\n" + "═"*45)
    print("   ADA2 - Métodos de Ordenamiento")
    print("═"*45)
    print("  1. Shell Sort")
    print("  2. Quick Sort")
    print("  3. Heap Sort")
    print("  4. Radix Sort")
    print("  5. Salir")
    print("═"*45)

def main():
    while True:
        menu()
        opcion = input("  Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            nums = pedir_numeros()
            original = nums.copy()
            resultado = shell_sort(nums)
            mostrar_resultado(original, resultado, "Shell Sort")

        elif opcion == "2":
            nums = pedir_numeros()
            original = nums.copy()
            resultado = quick_sort(nums)
            mostrar_resultado(original, resultado, "Quick Sort")

        elif opcion == "3":
            nums = pedir_numeros()
            original = nums.copy()
            resultado = heap_sort(nums)
            mostrar_resultado(original, resultado, "Heap Sort")

        elif opcion == "4":
            nums = pedir_numeros()
            # Radix Sort estándar solo trabaja con enteros no negativos
            if any(n < 0 for n in nums):
                print("\n  ✖ Radix Sort solo admite números enteros no negativos.")
                print("    Usa otro método para listas con negativos.")
            else:
                original = nums.copy()
                resultado = radix_sort(nums)
                mostrar_resultado(original, resultado, "Radix Sort")

        elif opcion == "5":
            print("\n  ✔ ¡Hasta luego!\n")
            break

        else:
            print("\n  ✖ Opción inválida. Elige entre 1 y 5.")

        input("\n  Presiona Enter para continuar...")


CONCLUSIONES = """

"""

if __name__ == "__main__":
    print(CONCLUSIONES)
    main()
