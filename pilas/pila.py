import tkinter as tk
from tkinter import ttk, messagebox

# --- Colores y Estilos ---
COLOR_FONDO = "#F5F5F7"
COLOR_LIENZO = "#FFFFFF"
COLOR_BLOQUE = "#4285F4"
COLOR_BORDE = "#1A73E8"
COLOR_TEXTO_BLOQUE = "#FFFFFF"
COLOR_PUSH = "#34A853"
COLOR_POP = "#EA4335"
COLOR_CLEAR = "#FB8C00" # Naranja para la nueva función de vaciar

FUENTE_TITULO = ("Helvetica Neue", 16, "bold")
FUENTE_TEXTO = ("Helvetica Neue", 10, "bold")
FUENTE_DATOS = ("Consolas", 12, "bold")

class PilaLinda:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Visual de Pila")
        self.root.geometry("380x620") 
        self.root.configure(bg=COLOR_FONDO)
        
        self.pila = []
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')

        # --- Interfaz ---
        tk.Label(root, text="Estructura de Datos: PILA", font=FUENTE_TITULO, bg=COLOR_FONDO, fg="#333333").pack(pady=(15, 5))
        tk.Label(root, text="(LIFO - Last In, First Out)", font=("Helvetica", 9, "italic"), bg=COLOR_FONDO, fg="#666666").pack()

        # Lienzo
        self.canvas_frame = tk.Frame(root, bg=COLOR_BORDE, bd=1)
        self.canvas_frame.pack(pady=10)
        self.canvas = tk.Canvas(self.canvas_frame, width=300, height=350, bg=COLOR_LIENZO, highlightthickness=0)
        self.canvas.pack(padx=2, pady=2)
        
        # Área de Control
        control_frame = tk.Frame(root, bg=COLOR_FONDO)
        control_frame.pack(pady=10, fill=tk.X, padx=40)
        
        self.entry = tk.Entry(control_frame, font=FUENTE_DATOS, justify="center", bd=1, relief="solid")
        self.entry.pack(fill=tk.X, pady=(0, 10), ipady=5)
        self.entry.insert(0, "A")
        
        # --- Botones ---
        self.setup_styles()
        
        # Fila 1 de botones (Push y Pop)
        btn_row1 = tk.Frame(control_frame, bg=COLOR_FONDO)
        btn_row1.pack(fill=tk.X)
        ttk.Button(btn_row1, text="↑ Push", command=self.push, style="Push.TButton").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        ttk.Button(btn_row1, text="↓ Pop", command=self.pop, style="Pop.TButton").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        # Fila 2 de botones (Vaciar)
        btn_row2 = tk.Frame(control_frame, bg=COLOR_FONDO)
        btn_row2.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btn_row2, text="⚠ Vaciar Pila (Clear)", command=self.clear_all, style="Clear.TButton").pack(fill=tk.X)

        self.actualizar_vista()

    def setup_styles(self):
        # Push
        self.estilo.configure("Push.TButton", background=COLOR_PUSH, foreground="white", font=FUENTE_TEXTO)
        self.estilo.map("Push.TButton", background=[('active', '#2D9249')])
        # Pop
        self.estilo.configure("Pop.TButton", background=COLOR_POP, foreground="white", font=FUENTE_TEXTO)
        self.estilo.map("Pop.TButton", background=[('active', '#D33A2C')])
        # Clear (Nuevo)
        self.estilo.configure("Clear.TButton", background=COLOR_CLEAR, foreground="white", font=FUENTE_TEXTO)
        self.estilo.map("Clear.TButton", background=[('active', '#E67E00')])

    def dibujar_bloque(self, x, y, ancho, alto, texto, es_cima=False):
        # Sombra
        self.canvas.create_rectangle(x+3, y+3, x+ancho+3, y+alto+3, fill="#E0E0E0", outline="")
        # Bloque
        color_borde = "#FFD600" if es_cima else COLOR_BORDE
        ancho_borde = 3 if es_cima else 1
        self.canvas.create_rectangle(x, y, x+ancho, y+alto, fill=COLOR_BLOQUE, outline=color_borde, width=ancho_borde)
        # Texto
        self.canvas.create_text(x+ancho/2, y+alto/2, text=texto, fill="white", font=FUENTE_DATOS)
        if es_cima:
            self.canvas.create_text(x-35, y+alto/2, text="TOP", fill=COLOR_POP, font=("Arial", 8, "bold"))

    def actualizar_vista(self):
        self.canvas.delete("all")
        ancho_b, alto_b = 200, 32
        x_start = 50
        y_base = 330
        
        # Suelo de la pila
        self.canvas.create_line(x_start-20, y_base, x_start+ancho_b+20, y_base, fill="#9E9E9E", width=3)

        for i, elemento in enumerate(self.pila):
            y_bloque = y_base - ((i+1) * (alto_b + 4))
            self.dibujar_bloque(x_start, y_bloque, ancho_b, alto_b, elemento, es_cima=(i == len(self.pila)-1))

    def push(self):
        val = self.entry.get().strip()
        if val:
            if len(self.pila) < 8:
                self.pila.append(val)
                self.actualizar_vista()
                self.entry.delete(0, tk.END)
                if val.isalpha() and len(val) == 1:
                    self.entry.insert(0, chr(ord(val)+1) if val < 'Z' else 'A')
            else: messagebox.showwarning("Tope", "¡Pila llena!")
        else: messagebox.showwarning("Error", "Escribe algo.")

    def pop(self):
        if self.pila:
            self.pila.pop()
            self.actualizar_vista()
        else: messagebox.showwarning("Vacía", "No hay nada que sacar.")

    def clear_all(self):
        if not self.pila:
            messagebox.showinfo("Info", "La pila ya está vacía.")
            return
            
        # Preguntar antes de borrar todo
        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres vaciar TODA la pila?")
        if confirmar:
            self.pila = [] # Limpiar la lista
            self.actualizar_vista()
            messagebox.showinfo("Listo", "La pila ha sido vaciada por completo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaLinda(root)
    root.mainloop()