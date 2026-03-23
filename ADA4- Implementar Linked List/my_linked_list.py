from typing import Any, Optional, Iterator


class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[Node] = None


class MyLinkedList:
    def __init__(self):
        self._head: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def append(self, data: Any):
        node = Node(data)
        if not self._head:
            self._head = node
        else:
            cur = self._head
            while cur.next:
                cur = cur.next
            cur.next = node
        self._size += 1

    def prepend(self, data: Any):
        node = Node(data)
        node.next = self._head
        self._head = node
        self._size += 1

    def insert(self, index: int, data: Any):
        if index <= 0:
            self.prepend(data)
        elif index >= self._size:
            self.append(data)
        else:
            node = Node(data)
            cur = self._head
            for _ in range(index - 1):
                cur = cur.next
            node.next = cur.next
            cur.next = node
            self._size += 1

    def delete(self, data: Any) -> bool:
        if not self._head:
            return False
        if self._head.data == data:
            self._head = self._head.next
            self._size -= 1
            return True
        cur = self._head
        while cur.next:
            if cur.next.data == data:
                cur.next = cur.next.next
                self._size -= 1
                return True
            cur = cur.next
        return False

    def delete_at(self, index: int) -> Any:
        if index < 0:
            index = self._size + index
        if not (0 <= index < self._size):
            raise IndexError(f"Índice {index} fuera de rango.")
        if index == 0:
            val = self._head.data
            self._head = self._head.next
            self._size -= 1
            return val
        cur = self._head
        for _ in range(index - 1):
            cur = cur.next
        val = cur.next.data
        cur.next = cur.next.next
        self._size -= 1
        return val

    def search(self, data: Any) -> int:
        cur, i = self._head, 0
        while cur:
            if cur.data == data:
                return i
            cur, i = cur.next, i + 1
        return -1

    def get(self, index: int) -> Any:
        if index < 0:
            index = self._size + index
        if not (0 <= index < self._size):
            raise IndexError(f"Índice {index} fuera de rango.")
        cur = self._head
        for _ in range(index):
            cur = cur.next
        return cur.data

    def reverse(self):
        prev, cur = None, self._head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        self._head = prev

    def to_list(self) -> list:
        return list(self)

    @classmethod
    def from_list(cls, items: list) -> "MyLinkedList":
        ll = cls()
        for item in items:
            ll.append(item)
        return ll

    def clear(self):
        self._head = None
        self._size = 0

    def __len__(self):          return self._size
    def __contains__(self, d):  return self.search(d) != -1
    def __getitem__(self, i):   return self.get(i)

    def __iter__(self) -> Iterator:
        cur = self._head
        while cur:
            yield cur.data
            cur = cur.next

    def __str__(self):
        return " -> ".join(str(v) for v in self) + " -> None"

    def __repr__(self):
        return f"MyLinkedList({self.to_list()})"
