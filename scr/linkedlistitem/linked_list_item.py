"""Элементы двусвязного списка"""
from scr.Composition.composition import Composition


class LinkedListItem:
    """Элементы двусвязного списка"""
    def __init__(self, track):
        # Если трек уже Composition
        if isinstance(track, Composition):
            self.current_item = track
        else:
            # Создание класса Composition
            self.current_item = Composition(track)
        self._next_item = None
        self._previous_item = None

    @property
    def next_item(self) -> Composition:
        """Getter"""
        return self._next_item

    @next_item.setter
    def next_item(self, item):
        self._next_item = item

    @property
    def previous_item(self) -> Composition:
        """Getter"""
        return self._previous_item

    @previous_item.setter
    def previous_item(self, item):
        self._previous_item = item
