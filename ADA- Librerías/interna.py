# interna.py

def quick_sort(arr):
    """Algoritmo QuickSort: Divide y vencerás."""
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izq = [x for x in arr if x < pivote]
    centro = [x for x in arr if x == pivote]
    der = [x for x in arr if x > pivote]
    return quick_sort(izq) + centro + quick_sort(der)

def shell_sort(arr):
    """Algoritmo ShellSort: Mejora de la inserción por brechas."""
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr