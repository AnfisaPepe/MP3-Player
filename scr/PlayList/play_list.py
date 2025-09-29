"""Плейлист"""
from typing import Union

from scr.LinkedList.linked_list import LinkedList
from scr.Composition.composition import Composition


class PlayList(LinkedList):
    """Плейлист"""
    def __init__(self) -> None:
        super().__init__()
        self.current_node = None
        self.is_playing = False

    def play_all(self, item=None) -> None:
        """Проигрывание всех песен, начиная с выбранного"""
        if self.is_empty():
            return

        if item is None:
            self.current_node = self.first_item
        else:
            # Нахождение узла с треком
            for node in self.iter_nodes():
                if node.current_item == item:
                    self.current_node = node
                    break
            else:
                self.current_node = self.first_item

        self.is_playing = True

    def next_track(self) -> Union[Composition, None]:
        """Переместить трек ниже"""
        if self.is_empty() or self.current_node is None:
            return None

        self.current_node = self.current_node.next_item
        return self.current_node.current_item

    def previous_track(self) -> Union[Composition, None]:
        """Переместить трек выше"""
        if self.is_empty() or self.current_node is None:
            return None

        self.current_node = self.current_node.previous_item
        return self.current_node.current_item

    @property
    def current(self) -> Union[Composition, None]:
        """Текущий трек"""
        if self.current_node is None:
            return None
        return self.current_node.current_item

    def stop(self) -> None:
        """Остановить трек"""
        self.is_playing = False
        self.current_node = None
