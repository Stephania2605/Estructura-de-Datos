import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os
import time

# --- LÓGICA DE PROCESAMIENTO ---

def extraer_numeros(texto):
    """Extractor universal de números."""
    encontrados = re.findall(r'-?\d+\.?\d*', texto)
    return [float(n) if '.' in n else int(n) for n in encontrados if n != '.']

def quick_sort(arr):
    """Algoritmo QuickSort para la memoria RAM."""
    if len(arr) <= 1: return arr
    pivote = arr[len(arr) // 2]
    izq = [x for x in arr if x < pivote]
    centro = [x for x in arr if x == pivote]
    der = [x for x in arr if x > pivote]
    return quick_sort(izq) + centro + quick_sort(der)

# --- INTERFAZ GRÁFICA FORMAL ---

class AppIngenieriaFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA DE GESTIÓN DE ORDENAMIENTO V3.0")
        self.root.geometry("700x800")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook.Tab", padding=[20, 5], font=("Segoe UI", 10))
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- PESTAÑA 1: ORDENACIÓN INTERNA ---
        self.tab_interna = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_interna, text=" 💻 Ordenación Interna ")
        self.setup_interna()

        # --- PESTAÑA 2: ORDENACIÓN EXTERNA ---
        self.tab_externa = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_externa, text=" 🗄️ Ordenación Externa ")
        self.setup_externa()

        self.setup_bitacora()

        # Variables para externa
        self.datos_acumulados_externa = []
        self.nombres_archivos_externa = []

    def setup_interna(self):
        ttk.Label(self.tab_interna, text="Procesamiento en RAM (Resultados visibles en la caja):", font=("Segoe UI", 9, "italic")).pack(anchor="w")
        
        btn_frame = ttk.Frame(self.tab_interna)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="📂 Importar Archivo a RAM", command=self.importar_a_ram).pack(side="left", padx=5)
        
        # Caja de entrada donde se verán los números ordenados
        self.entrada_manual = ttk.Entry(self.tab_interna, font=("Consolas", 10))
        self.entrada_manual.pack(fill="x", pady=5)
        self.entrada_manual.insert(0, "Escriba números aquí...")

        ttk.Button(self.tab_interna, text="EJECUTAR Y ACTUALIZAR CAJA", style="Action.TButton", command=self.ejecutar_interna).pack(pady=10)

    def setup_externa(self):
        ttk.Label(self.tab_externa, text="Mezcla secuencial (Resultados en archivo .txt):", font=("Segoe UI", 9, "italic")).pack(anchor="w")
        ttk.Button(self.tab_externa, text="➕ Añadir Archivo", command=self.agregar_archivo_externo).pack(pady=10)
        self.listbox_externa = tk.Listbox(self.tab_externa, height=6, font=("Segoe UI", 10), bd=1, relief="solid")
        self.listbox_externa.pack(fill="both", expand=True, pady=5)
        ctrl_frame = ttk.Frame(self.tab_externa)
        ctrl_frame.pack(fill="x", pady=10)
        ttk.Button(ctrl_frame, text="🗑️ Limpiar", command=self.limpiar_externa).pack(side="left", padx=5)
        self.btn_procesar_ext = ttk.Button(ctrl_frame, text="COMPARAR Y MEZCLAR", state="disabled", style="Action.TButton", command=self.procesar_externa)
        self.btn_procesar_ext.pack(side="right", padx=5)

    def setup_bitacora(self):
        frame_log = ttk.LabelFrame(self.root, text=" Bitácora de Eventos ", padding=10)
        frame_log.pack(fill="both", expand=False, padx=20, pady=15)
        self.txt_log = tk.Text(frame_log, height=10, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 9), borderwidth=0)
        self.txt_log.pack(fill="both", expand=True)

    def log(self, msg):
        t = time.strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{t}] {msg}\n")
        self.txt_log.see(tk.END)

    # --- LÓGICA INTERNA (CORREGIDA) ---
    def ejecutar_interna(self):
        # 1. Obtener texto de la caja
        texto_original = self.entrada_manual.get()
        nums = extraer_numeros(texto_original)
        
        if nums:
            # 2. Ordenar
            start = time.perf_counter()
            ordenados = quick_sort(nums)
            end = time.perf_counter()
            
            # 3. ACTUALIZAR LA CAJA VISUALMENTE
            self.entrada_manual.delete(0, tk.END) # Borra lo desordenado
            # Convierte la lista ordenada a texto separado por espacios
            resultado_texto = " ".join(map(str, ordenados))
            self.entrada_manual.insert(0, resultado_texto) # Pone lo ordenado
            
            self.log(f"Interna: {len(ordenados)} números ordenados visualmente en {(end-start)*1000:.2f} ms.")
        else:
            messagebox.showwarning("Aviso", "No se detectaron números para ordenar.")

    def importar_a_ram(self):
        f = filedialog.askopenfilename()
        if f:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                nums = extraer_numeros(file.read())
            self.entrada_manual.delete(0, tk.END)
            self.entrada_manual.insert(0, " ".join(map(str, nums)))
            self.log(f"Interna: Cargados {len(nums)} números desde archivo.")

    # --- LÓGICA EXTERNA ---
    def agregar_archivo_externo(self):
        f = filedialog.askopenfilename()
        if f:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                nuevos_datos = extraer_numeros(file.read())
            if nuevos_datos:
                self.datos_acumulados_externa.extend(nuevos_datos)
                self.listbox_externa.insert(tk.END, f"  📄 {os.path.basename(f)} ({len(nuevos_datos)} datos)")
                self.btn_procesar_ext.config(state="normal")
                self.log(f"Externa: Archivo '{os.path.basename(f)}' en cola.")

    def limpiar_externa(self):
        self.datos_acumulados_externa = []
        self.listbox_externa.delete(0, tk.END)
        self.btn_procesar_ext.config(state="disabled")

    def procesar_externa(self):
        resultado = sorted(self.datos_acumulados_externa)
        archivo_salida = "RESULTADO_MEZCLA.txt"
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for n in resultado: f.write(f"{n}\n")
            f.flush()
            os.fsync(f.fileno())
        self.log(f"Externa: Mezcla lista en {archivo_salida}")
        messagebox.showinfo("Éxito", f"Archivo generado: {archivo_salida}")
        self.limpiar_externa()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppIngenieriaFinal(root)
    root.mainloop()