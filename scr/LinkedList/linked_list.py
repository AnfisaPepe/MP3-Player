"""Двусвязный список"""
from scr.Linkedlistitem.linked_list_item import LinkedListItem


class LinkedList:
    """Двусвязный список"""
    def __init__(self):
        self.first_item = None
        self.last_item = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def append_left(self, item):
        new_item = LinkedListItem(item)
        if self.is_empty():
            new_item.next_item = new_item
            new_item.previous_item = new_item
            self.first_item = new_item
            self.last_item = new_item
        else:
            new_item.next_item = self.first_item
            new_item.previous_item = self.last_item
            self.first_item.previous_item = new_item
            self.last_item.next_item = new_item
            self.first_item = new_item
        self.size += 1

    def append_right(self, item):
        new_item = LinkedListItem(item)
        if self.is_empty():
            new_item.next_item = new_item
            new_item.previous_item = new_item
            self.first_item = new_item
            self.last_item = new_item
        else:
            new_item.previous_item = self.last_item
            new_item.next_item = self.first_item
            self.last_item.next_item = new_item
            self.first_item.previous_item = new_item
            self.last_item = new_item
        self.size += 1

    def _remove_node(self, item):
        if self.size == 0 or item is None:
            return
        if self.size == 1 and item is self.first_item:
            self.first_item = None
            self.last_item = None
            self.size = 0
            return
        prev_item = item.previous_item
        next_item = item.next_item
        prev_item.next_item = next_item
        next_item.previous_item = prev_item
        if item is self.first_item:
            self.first_item = next_item
        if item is self.last_item:
            self.last_item = prev_item
        self.size -= 1

    def remove(self, item):
        if isinstance(item, LinkedListItem):
            self._remove_node(item)
            return
        for node in self.iter_nodes():
            if (node.current_item == item
                    or getattr(node.current_item, "track_file_path", None) ==
                    getattr(item, "track_file_path", object())):
                self._remove_node(node)
                return
        raise ValueError(f"Трэк {item} не найден")

    def insert(self, previous_item, item):
        # Вставить новый элемент после предыдущего
        new_item = LinkedListItem(item)
        if self.is_empty() or previous_item is None:
            self.append_left(item)
            return
        node = previous_item
        next_node = node.next_item
        node.next_item = new_item
        new_item.previous_item = node
        new_item.next_item = next_node
        next_node.previous_item = new_item
        if node is self.last_item:
            self.last_item = new_item
        self.size += 1

    def iter_nodes(self):
        if self.is_empty():
            return
        yield self.first_item
        node = self.first_item.next_item
        while node is not self.first_item:
            yield node
            node = node.next_item

    def __iter__(self):
        if self.is_empty():
            return iter(())

        def generator():
            for node in self.iter_nodes():
                yield node.current_item
        return generator()

    def __len__(self):
        return self.size

    def append(self, item):
        """Алиас для append_right"""
        self.append_right(item)

    def last(self):
        """Последний элемент в списке"""
        if self.is_empty():
            return None
        return self.last_item.current_item

    def __getitem__(self, index):
        """Получить элемент по индексу"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0:
            index += self.size
        if index < 0 or index >= self.size:
            raise IndexError("Индекс не найден")

        current = self.first_item
        for _ in range(index):
            current = current.next_item
        return current.current_item

    def __reversed__(self):
        """Для reversed()"""
        if self.is_empty():
            return iter(())
        current = self.last_item
        yield current.current_item
        current = current.previous_item
        while current is not self.last_item:
            yield current.current_item
            current = current.previous_item

    def __contains__(self, item):
        if self.is_empty():
            return False
        for node in self.iter_nodes():
            if node.current_item == item:
                return True
        return False
