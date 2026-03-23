class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class MyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, index, data):
        if index < 0 or index > self.size:
            raise IndexError("Índice fuera de rango")
        if index == 0:
            self.prepend(data)
            return
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def remove(self, data):
        if self.head is None:
            raise ValueError("La lista está vacía")
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return
            current = current.next
        raise ValueError(f"Elemento '{data}' no encontrado")

    def remove_at(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        if index == 0:
            self.head = self.head.next
            self.size -= 1
            return
        current = self.head
        for _ in range(index - 1):
            current = current.next
        current.next = current.next.next
        self.size -= 1

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def search(self, data):
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def contains(self, data):
        return self.search(data) != -1

    def is_empty(self):
        return self.size == 0

    def length(self):
        return self.size

    def clear(self):
        self.head = None
        self.size = 0

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __str__(self):
        nodes = self.to_list()
        return " -> ".join(str(n) for n in nodes) + " -> None"

    def __len__(self):
        return self.size
