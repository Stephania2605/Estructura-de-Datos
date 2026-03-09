import tkinter as tk
from tkinter import ttk, messagebox

# --- Configuración Visual ---
COLOR_FONDO = "#F5F5F7"
COLOR_DATO = "#4285F4"      # Azul (Datos)
COLOR_VAR = "#FB8C00"       # Naranja (Variables)
COLOR_POSTE = "#555555"

class PilaHanoiPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Hanoi: Control Total y Automático")
        self.root.geometry("850x750")
        self.root.configure(bg=COLOR_FONDO)
        
        self.pila_a = []  # Principal
        self.pila_b = []  # Auxiliar
        self.bloqueado = False
        
        # --- Interfaz ---
        tk.Label(root, text="SISTEMA HANOI: PUSH / POP / AUTO", 
                 font=("Helvetica", 16, "bold"), bg=COLOR_FONDO).pack(pady=15)
        
        self.canvas = tk.Canvas(root, width=800, height=400, bg="white", highlightthickness=1)
        self.canvas.pack(pady=10)

        # --- Controles Manuales ---
        ctrl_frame = tk.Frame(root, bg=COLOR_FONDO)
        ctrl_frame.pack(pady=10)

        tk.Label(ctrl_frame, text="Bloque:", bg=COLOR_FONDO).grid(row=0, column=0)
        self.ent_letra = tk.Entry(ctrl_frame, font=("Consolas", 12), width=5)
        self.ent_letra.grid(row=0, column=1, padx=5)
        self.ent_letra.insert(0, "X")

        ttk.Button(ctrl_frame, text="↑ Push", command=self.push_manual).grid(row=0, column=2, padx=5)
        
        tk.Label(ctrl_frame, text="Eliminar ID:", bg=COLOR_FONDO).grid(row=0, column=3, padx=10)
        self.ent_eli = tk.Entry(ctrl_frame, font=("Consolas", 12), width=5)
        self.ent_eli.grid(row=0, column=4, padx=5)
        
        ttk.Button(ctrl_frame, text="↓ Buscar y Eliminar", command=self.pop_inteligente).grid(row=0, column=5, padx=5)

        # --- Controles de Tarea ---
        tarea_frame = tk.Frame(root, bg=COLOR_FONDO)
        tarea_frame.pack(pady=10)
        
        ttk.Button(tarea_frame, text="▶ Ejecutar Tarea Automática", command=self.secuencia_tarea).pack(side=tk.LEFT, padx=10)
        ttk.Button(tarea_frame, text="↺ Reiniciar", command=self.reset).pack(side=tk.LEFT, padx=10)

        self.msg_label = tk.Label(root, text="Listo", font=("Arial", 11, "bold"), bg=COLOR_FONDO, fg="#1A73E8")
        self.msg_label.pack(pady=10)

        self.actualizar_vista()

    def actualizar_vista(self):
        self.canvas.delete("all")
        y_base = 350
        
        # Postes
        self.canvas.create_rectangle(195, 100, 205, y_base, fill=COLOR_POSTE) 
        self.canvas.create_rectangle(595, 100, 605, y_base, fill=COLOR_POSTE) 
        self.canvas.create_text(200, y_base+20, text="POSTE A (PILA)", font=("Arial", 9, "bold"))
        self.canvas.create_text(600, y_base+20, text="POSTE B (AUX)", font=("Arial", 9, "bold"))

        for i, (n, c) in enumerate(self.pila_a):
            self.dibujar_bloque(200, y_base - ((i+1) * 35), n, c)

        for i, (n, c) in enumerate(self.pila_b):
            self.dibujar_bloque(600, y_base - ((i+1) * 35), n, c)

    def dibujar_bloque(self, x, y, texto, color):
        ancho = 120
        self.canvas.create_rectangle(x-ancho/2, y, x+ancho/2, y+30, fill=color, outline="white", width=2)
        self.canvas.create_text(x, y+15, text=texto, fill="white", font=("Consolas", 12, "bold"))

    def set_msg(self, txt):
        self.msg_label.config(text=txt)
        self.root.update()

    def push_manual(self):
        if self.bloqueado: return
        letra = self.ent_letra.get().upper().strip()
        if letra:
            color = COLOR_VAR if letra in ["Z", "T", "U", "P"] else COLOR_DATO
            self.pila_a.append((letra, color))
            self.actualizar_vista()
            if len(letra) == 1:
                self.ent_letra.delete(0, tk.END)
                self.ent_letra.insert(0, chr(ord(letra)+1))
        else: messagebox.showwarning("Error", "Escribe una letra")

    def pop_inteligente(self, callback=None):
        objetivo = self.ent_eli.get().upper().strip()
        if self.bloqueado or not objetivo: return
        
        indices = [i for i, x in enumerate(self.pila_a) if x[0] == objetivo]
        if not indices:
            messagebox.showerror("Error", f"No se encontró el bloque {objetivo}")
            return

        self.bloqueado = True
        idx_obj = indices[-1]

        def reacomodo():
            if len(self.pila_a) - 1 > idx_obj:
                item = self.pila_a.pop()
                self.pila_b.append(item)
                self.set_msg(f"Moviendo {item[0]} al Poste B...")
                self.actualizar_vista()
                self.root.after(600, reacomodo)
            else:
                eliminado = self.pila_a.pop()
                self.set_msg(f"ELIMINADO: {eliminado[0]}")
                self.actualizar_vista()
                self.root.after(1000, restaurar)

        def restaurar():
            if self.pila_b:
                item = self.pila_b.pop()
                self.pila_a.append(item)
                self.set_msg(f"Restaurando {item[0]}...")
                self.actualizar_vista()
                self.root.after(600, restaurar)
            else:
                self.bloqueado = False
                self.set_msg("Listo")
                if callback: callback()

        reacomodo()

    def secuencia_tarea(self):
        self.reset()
        pasos = [
            ("a", "push", "X"), ("b", "push", "Y"),
            ("c", "push", "Z"), ("c_e", "pop", "Z"),
            ("d", "push", "T"), ("d_e", "pop", "T"),
            ("e", "push", "U"), ("e_e", "pop", "U"),
            ("f", "push", "V"), ("g", "push", "W"),
            ("h", "push", "P"), ("h_e", "pop", "P"),
            ("i", "push", "R")
        ]
        self.ejecutar_paso_auto(pasos, 0)

    def ejecutar_paso_auto(self, lista, i):
        if i >= len(lista):
            self.set_msg("TAREA COMPLETADA")
            return
        
        p, acc, letra = lista[i]
        if acc == "push":
            color = COLOR_VAR if letra in ["Z", "T", "U", "P"] else COLOR_DATO
            self.pila_a.append((letra, color))
            self.set_msg(f"Paso {p}: Push {letra}")
            self.actualizar_vista()
            self.root.after(1000, lambda: self.ejecutar_paso_auto(lista, i+1))
        else:
            self.ent_eli.delete(0, tk.END)
            self.ent_eli.insert(0, letra)
            self.set_msg(f"Paso {p}: Pop {letra}")
            self.pop_inteligente(callback=lambda: self.ejecutar_paso_auto(lista, i+1))

    def reset(self):
        self.pila_a, self.pila_b, self.bloqueado = [], [], False
        self.actualizar_vista()
        self.set_msg("Reinicio")

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaHanoiPro(root)
    root.mainloop()