"""
MP3 Player - Приложения для проигрывания mp3 файлов
"""

import tkinter as tk
from scr.Interface.interface import Interface


def main():
    """Запуск приложения"""
    root = tk.Tk()
    Interface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
