"""Инфа о композиции"""
import os


class Composition:
    """Инфа о композиции"""
    def __init__(self, track_file_path, duration=None):
        self.track_file_path = track_file_path
        self.duration = duration if duration is not None else 0

    def __str__(self):
        return os.path.basename(self.track_file_path)
    
    def __eq__(self, other):
        if isinstance(other, Composition):
            return self.track_file_path == other.track_file_path
        return False
    
    def __repr__(self):
        return f"Трек('{self.track_file_path}')"