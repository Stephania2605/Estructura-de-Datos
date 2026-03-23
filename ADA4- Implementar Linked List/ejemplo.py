from MyLinkedList import MyLinkedList

lista = MyLinkedList()

lista.append(10)
lista.append(20)
lista.append(30)
lista.prepend(5)
lista.insert_at(2, 15)

print("Lista:", lista)
print("Tamaño:", lista.length())
print("Elemento en índice 2:", lista.get(2))
print("Índice de 20:", lista.search(20))
print("¿Contiene 99?:", lista.contains(99))

lista.remove(15)
print("Después de eliminar 15:", lista)

lista.remove_at(0)
print("Después de eliminar índice 0:", lista)

print("¿Está vacía?:", lista.is_empty())
lista.clear()
print("Después de clear:", lista)
print("¿Está vacía?:", lista.is_empty())
