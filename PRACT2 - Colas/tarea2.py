import tkinter as tk
from tkinter import messagebox, ttk

class Order:
    def __init__(self, qtty: int, customer: str):
        self.customer = customer
        self.qtty = qtty

class Node:
    def __init__(self, info):
        self.info = info
        self.next = None

class Queue:
    def __init__(self, capacity: int):
        self.front_node = None
        self.rear_node = None
        self._size = 0
        self.capacity = capacity

    def is_full(self):
        return self._size >= self.capacity

    def is_empty(self):
        return self.front_node is None

    def enqueue(self, info):
        if self.is_full():
            return False
        new_node = Node(info)
        if self.is_empty():
            self.front_node = self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        self._size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        info_extraida = self.front_node.info
        self.front_node = self.front_node.next
        if self.front_node is None:
            self.rear_node = None
        self._size -= 1
        return info_extraida

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Pedidos Pro")
        self.root.geometry("500x550")
        self.root.configure(padx=20, pady=20)
        
        # Estado inicial
        self.cola = None

        # --- SECCIÓN CONFIGURACIÓN ---
        self.frame_config = ttk.LabelFrame(root, text=" Configuración inicial ", padding=10)
        self.frame_config.pack(fill="x", pady=5)
        
        ttk.Label(self.frame_config, text="Límite de la cola:").grid(row=0, column=0)
        self.entry_limite = ttk.Entry(self.frame_config, width=10)
        self.entry_limite.grid(row=0, column=1, padx=5)
        self.btn_set_limite = ttk.Button(self.frame_config, text="Establecer", command=self.set_limit)
        self.btn_set_limite.grid(row=0, column=2)

        # --- SECCIÓN ENTRADA ---
        self.frame_inputs = ttk.LabelFrame(root, text=" Nuevo Pedido ", padding=10)
        self.frame_inputs.pack(fill="x", pady=10)

        ttk.Label(self.frame_inputs, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.entry_cliente = ttk.Entry(self.frame_inputs)
        self.entry_cliente.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.frame_inputs, text="Cantidad:").grid(row=1, column=0, sticky="w")
        self.entry_qtty = ttk.Entry(self.frame_inputs)
        self.entry_qtty.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.btn_add = ttk.Button(self.frame_inputs, text="Agregar a la Cola (Enqueue)", command=self.add_order, state="disabled")
        self.btn_add.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # --- SECCIÓN VISTA Y ACCIONES ---
        self.lbl_status = ttk.Label(root, text="Estado: Configura el límite para empezar", font=("Arial", 10, "bold"))
        self.lbl_status.pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("Cliente", "Cantidad"), show="headings", height=8)
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(fill="both", expand=True)

        self.btn_remove = ttk.Button(root, text="Atender / Eliminar pedido (Dequeue)", command=self.remove_order, state="disabled")
        self.btn_remove.pack(fill="x", pady=10)

    def set_limit(self):
        try:
            limite = int(self.entry_limite.get())
            if limite <= 0: raise ValueError
            self.cola = Queue(limite)
            self.lbl_status.config(text=f"Cola lista: 0/{limite} pedidos")
            self.btn_add.config(state="normal")
            self.btn_remove.config(state="normal")
            self.btn_set_limite.config(state="disabled")
            self.entry_limite.config(state="disabled")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido mayor a 0")

    def add_order(self):
        cliente = self.entry_cliente.get()
        cantidad = self.entry_qtty.get()

        if not cliente or not cantidad:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios")
            return

        try:
            cantidad = int(cantidad)
            pedido = Order(cantidad, cliente)
            if self.cola.enqueue(pedido):
                self.update_view()
                self.entry_cliente.delete(0, tk.END)
                self.entry_qtty.delete(0, tk.END)
            else:
                messagebox.showwarning("Lleno", "La cola ha alcanzado su límite máximo")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número")

    def remove_order(self):
        pedido = self.cola.dequeue()
        if pedido:
            messagebox.showinfo("Atendido", f"Atendiendo pedido de: {pedido.customer}")
            self.update_view()
        else:
            messagebox.showwarning("Vacío", "No hay pedidos pendientes")

    def update_view(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Rellenar tabla
        current = self.cola.front_node
        while current:
            self.tree.insert("", "end", values=(current.info.customer, current.info.qtty))
            current = current.next
        
        # Actualizar estado
        self.lbl_status.config(text=f"Estado: {self.cola.size()}/{self.cola.capacity} pedidos")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()