"""Двусвязный список"""

__version__ = "1.0.0"

from .Linkedlistitem import linked_list_item
from .LinkedList import linked_list
from .Interface import interface
from .Playlist import play_list
from .Composition import composition


__all__ = [
    "linked_list",
    "linked_list_item",
    "interface",
    "play_list",
    "composition"
]