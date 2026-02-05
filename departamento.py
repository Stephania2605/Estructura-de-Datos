meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

departamentos = ["Ropa", "Deportes", "Juguetería"]

ventas = [
    [12000, 8500, 4300],
    [15000, 9200, 5000],
    [18000, 11000, 6200],
    [17000, 10500, 6000],
    [20000, 13000, 7500],
    [22000, 14000, 8000],
    [21000, 13500, 7800],
    [23000, 15000, 8500],
    [19000, 12000, 7000],
    [25000, 16000, 9000],
    [27000, 17000, 9500],
    [30000, 20000, 12000]
]

def linea():
    print("+------------+------------+------------+------------+")

def mostrar_tabla():
    print("\nTABLA DE VENTAS\n")
    linea()
    print(f"| {'Mes':<10} | {'Ropa':<10} | {'Deportes':<10} | {'Juguetería':<10} |")
    linea()

    for i in range(12):
        print(f"| {meses[i]:<10} | {ventas[i][0]:<10} | {ventas[i][1]:<10} | {ventas[i][2]:<10} |")
        linea()

def modificar_venta():
    mes = int(input("Mes (1-12): "))
    depto = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): "))
    monto = float(input("Nuevo monto: "))

    f = mes - 1
    c = depto - 1

    if 0 <= f < 12 and 0 <= c < 3:
        ventas[f][c] = monto
        print("✔ Venta modificada")

def buscar_venta():
    mes = int(input("Mes (1-12): "))
    depto = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): "))

    f = mes - 1
    c = depto - 1

    if 0 <= f < 12 and 0 <= c < 3:
        print("🔍 Venta encontrada:", ventas[f][c])

def eliminar_venta():
    mes = int(input("Mes (1-12): "))
    depto = int(input("Departamento (1=Ropa, 2=Deportes, 3=Juguetería): "))

    f = mes - 1
    c = depto - 1

    if 0 <= f < 12 and 0 <= c < 3:
        ventas[f][c] = 0
        print("🗑 Venta eliminada")

# -------- MENÚ --------

while True:
    mostrar_tabla()

    print("\n1. Modificar venta")
    print("2. Buscar venta")
    print("3. Eliminar venta")
    print("4. Salir")

    op = int(input("Elige opción: "))

    if op == 1:
        modificar_venta()
    elif op == 2:
        buscar_venta()
    elif op == 3:
        eliminar_venta()
    elif op == 4:
        print("Programa terminado")
        break
    else:
        print("Opción inválida")
