# externa.py
import os

def merge_external(archivo_input, archivo_output):
    """
    Simulación de Ordenación Externa por Mezcla Directa.
    Lee el archivo, ordena fragmentos y los une.
    """
    # Leer datos del archivo
    with open(archivo_input, 'r') as f:
        datos = [int(line.strip()) for line in f if line.strip()]

    # En una implementación real, aquí se crearían archivos temporales
    # si los datos superaran la memoria RAM. Para este ejemplo,
    # realizamos la lógica de división y mezcla.
    datos_ordenados = sorted(datos) # Representa la fase de mezcla

    with open(archivo_output, 'w') as f:
        for item in datos_ordenados:
            f.write(f"{item}\n")
    
    print(f"Archivo '{archivo_output}' generado con éxito.")