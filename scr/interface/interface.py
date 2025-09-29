"""Интерфейс"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pygame
from scr.Playlist.play_list import PlayList
from scr.Composition.composition import Composition


class Interface:
    """Интерфейс"""
    def __init__(self, root):
        self.current_track_var = None
        self.playlist_combo = None
        self.playlist_var = None
        self.track_listbox = None
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("800x600")

        # Инициализация mixer
        pygame.mixer.init()

        # Текущий плейлист
        self.current_playlist = None
        self.playlists = {}

        self.setup_ui()

    def setup_ui(self):
        """Установка окна"""
        # Основное окно
        main_frame = ttk.Frame(
            self.root,
            padding="10"
        )
        main_frame.grid(
            row=0,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S)
        )

        playlist_frame = ttk.LabelFrame(
            main_frame,
            text="Управление плейлистами",
            padding="5"
        )
        playlist_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 10)
        )

        # Список функций плейлиста
        (ttk.Button(playlist_frame,
                    text="Новый плейлист",
                    command=self.create_playlist
                    )
        .grid(row=0, column=0, padx=(0, 5)))

        (ttk.Button(playlist_frame,
                    text="Удалить плейлист",
                    command=self.delete_playlist
                    )
        .grid(row=0, column=1, padx=5))

        (ttk.Button(playlist_frame,
                    text="Добавить трек",
                    command=self.add_track
                    )
        .grid(row=0, column=2, padx=5))

        (ttk.Button(playlist_frame,
                    text="Удалить трек",
                    command=self.remove_track
                    )
        .grid(row=0, column=3, padx=5))

        # Выбор плейлистов
        ttk.Label(
            playlist_frame,
            text="Выбрать плейлист:"
        ).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))

        self.playlist_var = tk.StringVar()
        self.playlist_combo = ttk.Combobox(
            playlist_frame,
            textvariable=self.playlist_var,
            state="readonly"
        )
        self.playlist_combo.grid(
            row=1,
            column=1,
            sticky=(tk.W, tk.E),
            padx=(5, 0),
            pady=(10, 0)
        )
        self.playlist_combo.bind('<<ComboboxSelected>>', self.on_playlist_selected)

        # Окно для списка треков
        tracks_frame = ttk.LabelFrame(main_frame, text="Треки", padding="5")
        tracks_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            pady=(0, 10)
        )

        # Список треков с контролбаром
        listbox_frame = ttk.Frame(tracks_frame)
        listbox_frame.grid(
            row=0,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S)
        )

        self.track_listbox = tk.Listbox(
            listbox_frame,
            height=10
        )
        scrollbar = ttk.Scrollbar(
            listbox_frame,
            orient=tk.VERTICAL,
            command=self.track_listbox.yview
        )
        self.track_listbox.configure(
            yscrollcommand=scrollbar.set
        )

        self.track_listbox.grid(
            row=0,
            column=0,
            sticky=(tk.W, tk.E, tk.N, tk.S)
        )
        scrollbar.grid(
            row=0,
            column=1,
            sticky=(tk.N, tk.S)
        )

        # Кнопки вверх-вниз
        move_frame = ttk.Frame(tracks_frame)
        move_frame.grid(row=1, column=0, pady=(5, 0))

        (ttk.Button(move_frame,
                    text="Вверх",
                    command=self.move_track_up
                    )
         .grid(row=0, column=0, padx=(0, 5)))

        (ttk.Button(
            move_frame,
            text="Вниз",
            command=self.move_track_down)
         .grid(row=0, column=1, padx=5))

        # Управление плеером
        player_frame = ttk.LabelFrame(
            main_frame,
            text="Управление плеером",
            padding="5"
        )

        player_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 10)
        )

        # Кнопки упраления плеером
        control_frame = ttk.Frame(player_frame)
        control_frame.grid(
            row=0,
            column=0,
            sticky=(tk.W, tk.E)
        )

        ttk.Button(
            control_frame,
            text="Воспроизвести",
            command=self.play
        ).grid(row=0, column=0, padx=(0, 5))

        ttk.Button(
            control_frame,
            text="Пауза",
            command=self.pause
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            control_frame,
            text="Продолжить",
            command=self.unpause
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            control_frame,
            text="Стоп",
            command=self.stop
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            control_frame,
            text="Предыдущий",
            command=self.previous_track
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            control_frame,
            text="Следующий",
            command=self.next_track
        ).grid(row=0, column=5, padx=5)

        # Текущий трек
        self.current_track_var = tk.StringVar(value="Трек не выбран")

        ttk.Label(
            player_frame,
            text="Текущий трек:"
        ).grid(row=1, column=0, sticky=tk.W, pady=(10, 0))

        ttk.Label(
            player_frame,
            textvariable=self.current_track_var
        ).grid(row=1, column=1, sticky=tk.W, pady=(10, 0))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        tracks_frame.columnconfigure(0, weight=1)
        tracks_frame.rowconfigure(0, weight=1)
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)

    def create_playlist(self):
        """Создать новый плейлист"""
        playlist_name = tk.simpledialog.askstring(
            "Новый плейлист",
            "Введите название плейлиста:"
        )
        if playlist_name and playlist_name not in self.playlists:
            self.playlists[playlist_name] = PlayList()
            self.update_playlist_combo()
            self.playlist_var.set(playlist_name)
            self.on_playlist_selected()
            messagebox.showinfo(
                "Успех",
                f"Плейлист '{playlist_name}' создан!"
            )
        elif playlist_name in self.playlists:
            messagebox.showerror(
                "Ошибка",
                "Плейлист с таким именем уже существует!"
            )

    def delete_playlist(self):
        """Удалить плейлист"""
        playlist_name = self.playlist_var.get()
        if playlist_name and playlist_name in self.playlists:
            if messagebox.askyesno(
                    "Подтверждение",
                    f"Удалить плейлист '{playlist_name}'?"
            ):
                del self.playlists[playlist_name]
                self.update_playlist_combo()
                self.current_playlist = None
                self.track_listbox.delete(0, tk.END)
                self.current_track_var.set("Трек не выбран")
        else:
            messagebox.showwarning(
                "Предупреждение",
                "Плейлист не выбран!"
            )

    def add_track(self):
        """Добавить трек в плейлист"""
        if self.current_playlist is None:
            messagebox.showwarning(
                "Предупреждение",
                "Плейлист не выбран!"
            )
            return

        file_paths = filedialog.askopenfilenames(
            title="Выберите MP3 файлы",
            filetypes=[("MP3 файлы", "*.mp3"), ("Все файлы", "*.*")]
        )

        if not file_paths:
            return

        added_count = 0
        for file_path in file_paths:
            try:
                composition = Composition(file_path)
                self.current_playlist.append_right(composition)
                added_count += 1
            except Exception as exception:
                messagebox.showerror(
                    "Ошибка",
                    f"Не удалось добавить трек: {exception}"
                )

        if added_count > 0:
            self.update_track_list()
            messagebox.showinfo(
                "Успех",
                f"Добавлено {added_count} трек(ов)"
            )
        else:
            messagebox.showwarning(
                "Предупреждение",
                "Треки не были добавлены"
            )

    def remove_track(self):
        """Удалить трек из плейлиста"""
        if self.current_playlist is None:
            messagebox.showwarning(
                "Предупреждение",
                "Плейлист не выбран!"
            )
            return

        selection = self.track_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Предупреждение",
                "Трек не выбран!"
            )
            return

        index = selection[0]
        track = self.current_playlist[index]
        self.current_playlist.remove(track)
        self.update_track_list()

    def move_track_up(self):
        """Переместить трек выше"""
        self.move_track(-1)

    def move_track_down(self):
        """Переместить трек ниже"""
        self.move_track(1)

    def move_track(self, direction):
        """Переместить трек"""
        if self.current_playlist is None:
            return

        selection = self.track_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        new_index = index + direction

        if 0 <= new_index < len(self.current_playlist):
            # Воспроизвести трек
            track = self.current_playlist[index]
            other_track = self.current_playlist[new_index]

            # Удалить оба трека
            self.current_playlist.remove(track)
            self.current_playlist.remove(other_track)

            # Переместить на новую позицию
            if direction == -1:  # Вверх
                self.insert_at(new_index, track)
                self.insert_at(index, other_track)
            else:  # Вниз
                self.insert_at(index, other_track)
                self.insert_at(new_index, track)

            self.update_track_list()
            self.track_listbox.selection_set(new_index)

    def insert_at(self, index, item):
        """Для метода insert"""
        if index == 0:
            self.current_playlist.append_left(item)
        else:
            prev_node = self.current_playlist.first_item
            for _ in range(index - 1):
                prev_node = prev_node.next_item
            self.current_playlist.insert(prev_node, item)

    def play(self):
        """Воспроизведение текущего трека"""
        if self.current_playlist is None or self.current_playlist.is_empty():
            messagebox.showwarning(
                "Предупреждение",
                "В плейлисте нет треков!"
            )
            return

        selection = self.track_listbox.curselection()
        if selection:
            track = self.current_playlist[selection[0]]
            self.current_playlist.play_all(track)
        else:
            self.current_playlist.play_all()

        self.update_current_track_display()
        self.play_track()

    def pause(self):
        """Пауза"""
        pygame.mixer.music.pause()
        if self.current_playlist:
            self.current_playlist.stop()

    @staticmethod
    def unpause():
        """"Продолжить"""
        pygame.mixer.music.unpause()

    def stop(self):
        """Стоп"""
        pygame.mixer.music.stop()
        if self.current_playlist:
            self.current_playlist.stop()
        self.current_track_var.set("Трек не выбран")

    def next_track(self):
        """Следующий"""
        if self.current_playlist is None:
            return

        track = self.current_playlist.next_track()
        if track:
            self.update_current_track_display()
            self.play_track()

    def previous_track(self):
        """Предыдущий"""
        if self.current_playlist is None:
            return

        track = self.current_playlist.previous_track()
        if track:
            self.update_current_track_display()
            self.play_track()

    def play_track(self):
        """Текущий"""
        if not self.current_playlist or not self.current_playlist.current:
            return

        track = self.current_playlist.current
        try:
            pygame.mixer.music.load(track.track_file_path)
            pygame.mixer.music.play()

            # Подготовка следующего трека
            self.root.after(1000, self.check_track_finished)
        except pygame.error as exception:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось воспроизвести трек: {exception}"
            )

    def check_track_finished(self):
        """Проверка, закончилась ли песня"""
        if pygame.mixer.music.get_busy():
            # Если трек еще играет
            self.root.after(1000, self.check_track_finished)
        else:
            # Если трек закончился
            if self.current_playlist and self.current_playlist.is_playing:
                self.next_track()

    def update_playlist_combo(self):
        """Обновление списка"""
        playlists = list(self.playlists.keys())
        self.playlist_combo['values'] = playlists

    def on_playlist_selected(self, event=None):
        """Список плейлистов"""
        playlist_name = self.playlist_var.get()
        if playlist_name in self.playlists:
            self.current_playlist = self.playlists[playlist_name]
            self.update_track_list()
        else:
            self.current_playlist = None
            self.track_listbox.delete(0, tk.END)

    def update_track_list(self):
        """Обновление списка треков"""
        self.track_listbox.delete(0, tk.END)
        if self.current_playlist is not None:
            for track in self.current_playlist:
                self.track_listbox.insert(tk.END, str(track))

    def update_current_track_display(self):
        """Обновление отображения дисплея"""
        if self.current_playlist and self.current_playlist.current:
            self.current_track_var.set(str(self.current_playlist.current))
        else:
            self.current_track_var.set("Трек не выбран")
