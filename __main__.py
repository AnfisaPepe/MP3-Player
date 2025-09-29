"""
MP3 Player - Приложения для проигрывания mp3 файлов
"""

import tkinter as tk
from scr.Interface.interface import MP3PlayerInterface


def main():
    root = tk.Tk()
    MP3PlayerInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
