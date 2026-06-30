import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from library import get_all_songs

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BoombaFM(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title = "Bomba FM 🎶🎙️"
        self.geometry("950x650")

        self.songs = get_all_songs()
        self.current_song = None
        self.is_playing = False

        self.build_header()
        self.build_tabs()

    def build_header(self):
        header = ctk.CTkFrame(self, height=60, fg_color="#1a1a2e")
        header.pack(fill="x", side="top")

        ctk.CTkLabel(
            header,
            text="Bomba FM 🎶🎙️",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00ff88",
        ).pack(side="left", padx=20, pady=10,)
        ctk.CTkLabel(
            header,
            text="Your Personal Music Streaming App.🎵",
            font=ctk.CTkFont(size=24),
            text_color="#888888",
        ).pack(side="left", padx=5, pady=10,)
    def build_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        self.tabview.add("🎵All Songs🎵")
        self.tabview.add("🔍Search🔎")
        self.tabview.add("🎼Browse🎼")
        self.build_all_songs_tab()
        self.build_search_tab()
        self.build_browse_tab()
        self.build_player_bar()

    def build_all_songs_tab(self):
        tab = self.tabview.tab("🎵All Songs🎵")
        ctk.CTkLabel(
            tab,
            text="All Songs Library",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=10)
        self.all_songs_listbox= tk.Listbox(
            tab, bg="#2a2a2a",fg="white",
            font=("Arial", 11), height=15,
            selectbackground="#00ff88",
            selectforeground="black",
        )
        self.all_songs_listbox.pack(fill="both", expand=True, padx=20, pady=5,)
        self.all_songs_listbox.bind("<Double-Button-1>", self.play_from_all_songs)
        for songs in self.songs:
            self.all_songs_listbox.insert(
                tk.END,
                f"{songs.title} - {songs.artist} [{songs.genre}] ({songs.year})"
            )
        ctk.CTkLabel(
            tab,
            text="Double-click a song to play it",
            font=ctk.CTkFont(size=14),
            text_color="#888888",
        ).pack (pady=10)
    def build_search_tab(self):
        tab = self.tabview.tab("🔍Search🔎")
        ctk.CTkLabel(
            tab,
            text="Search Songs",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)
        search_frame= ctk.CTkFrame(tab, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search Songs By Artist, Genre, Title",
            width=400, height=40,
            font=ctk.CTkFont(size=13),
        )
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=100, height=40,
            fg_color="#00ff88",
            text_color="black",
            font=ctk.CTkFont(weight="bold"),
            command=self.perform_search
        ).pack(side="left", padx=5)

        self.search_count_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=12),
            text_color="#00ff88",
        )
        self.search_count_label.pack(pady=2)

        self.search_listbox = tk.Listbox(
            tab, bg="#2a2a2a", fg="White",
            font=("Arial", 11), height=13,
            selectbackground="#00ff88",
            selectforeground="black",
        )
        self.search_listbox.pack(fill="both", expand=True, padx=20, pady=5,)
        self.search_listbox.bind("<Double-Button-1>", self.play_from_search)

        self.search_results_data = []

    def perform_search(self):
        query=self.search_entry.get().lower().strip()
        if not query:
            messagebox.showwarning("Empty", "Please enter a search term!")
            return
        self.search_results_data = [
            song for song in self.songs
            if query in song.title.lower()
            or query in song.artist.lower()
            or query in song.genre.lower()
        ]

        self.search_listbox.delete(0, tk.END)

        if self.search_results_data:
            for song in self.search_results_data:
                self.search_listbox.insert(
                    tk.END,
                    f" {song.title} - {song.artist} [{song.genre}]"
                )
                self.search_count_label.configure(
                    text=f"Found {len(self.search_results_data)} result(s)"
                )
        else:
            self.search_listbox.insert(tk.END, "No results found!")
            self.search_count_label.configure(text="No results found!")

    def play_from_search(self, event):
        try:
            idx = self.search_listbox.curselection()[0]
            self.play_song(self.search_results_data[idx])
        except IndexError:
            pass
    def build_browse_tab(self):
        tab = self.tabview.tab("🎼Browse🎼")

        ctk.CTkLabel(
            tab,
            text="Browse Songs By Artist or Genre",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=10)

        filter_frame= ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(filter_frame, text="Genre:").pack(side="left", padx=5)
        unique_genres = ["All"] + sorted(set(s.genre for s in self.songs))
        self.genre_var = ctk.StringVar(value="All")
        self.genre_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=unique_genres,
            variable=self.genre_var,
            command=self.filter_songs,
            width=150,
        )
        self.genre_menu.pack(side="left", padx=5)

        ctk.CTkLabel(filter_frame, text="Artist:").pack(side="left", padx=15)
        unique_artist = ["All"] + sorted(set(s.artist for s in self.songs))
        self.artist_var = ctk.StringVar(value="All")
        self.artist_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=unique_artist,
            variable=self.artist_var,
            command=self.filter_songs,
            width=200,
        )
        self.artist_menu.pack(side="left", padx=15)

        ctk.CTkButton(
            filter_frame,
            text="Show All",
            width=90,
            fg_color="#444444",
            command=self.reset_browse
        ).pack(side="left", padx=10)

        self.browse_count_label = ctk.CTkLabel(
            tab,
            text=f"Showing all {len(self.songs)} songs",
            font=ctk.CTkFont(size=12),
            text_color="#00ff88",
        )
        self.browse_count_label.pack(pady=2)

        self.browse_listbox = tk.Listbox(
            tab, bg="#2a2a2a", fg="White",
            font=("Arial", 11), height=13,
            selectbackground="#00ff88",
            selectforeground="black",
        )
        self.browse_listbox.pack(fill="both", expand=True, padx=20, pady=5)
        self.browse_listbox.bind("<Double-Button-1>", self.play_from_browse)

        self.browse_results_data = list(self.songs)
        self.refresh_browse_list(self.songs)

    def refresh_browse_list(self, song_list):
        self.browse_listbox.delete(0, tk.END)
        for s in song_list:
            self.browse_listbox.insert(
                tk.END,
                f" {s.title} - {s.artist} [{s.genre}]"
            )
            self.browse_count_label.configure(
                text=f"Showing {len(song_list)} songs"
            )
    def reset_browse(self):
        self.genre_var.set("All")
        self.artist_var.set("All")
        self.search_browse_data = list(self.songs)
        self.refresh_browse_list(self.songs)

    def filter_songs(self, _=None):
        genre = self.genre_var.get()
        artist = self.artist_var.get()
        filtered = self.songs
        if genre != "All":
            filtered = [s for s in filtered if s.genre == genre]
        if artist != "All":
            filtered = [s for s in filtered if s.artist == artist]
        self.browse_results_data = filtered
        self.refresh_browse_list(filtered)
        
    def play_from_browse(self, event):
        try:
            idx = self.browse_listbox.curselection()[0]
            self.play_song(self.browse_results_data[idx])
        except IndexError:
                pass

    def build_player_bar(self):
                player_bar = ctk.CTkFrame(self, height=100, fg_color="#1a1a2e")
                player_bar.pack(fill="x", side="bottom")

                info_frame = ctk.CTkFrame(player_bar, fg_color="transparent")
                info_frame.pack(side="left", padx=20, pady=10)

                ctk.CTkLabel(
                    info_frame,
                    text="NOW PLAYING",
                    font=ctk.CTkFont(size=10),
                    text_color="#888888"
                ).pack(anchor="w")

                self.now_playing_label = ctk.CTkLabel(
                info_frame,
                text="No song selected",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#00ff88"
                )
                self.now_playing_label.pack(anchor="w")

                self.now_playing_artist = ctk.CTkLabel(
                info_frame, text="",
                font=ctk.CTkFont(size=11),
                text_color="#888888"
                )
                self.now_playing_artist.pack(anchor="w")

                controls_frame = ctk.CTkFrame(player_bar, fg_color="transparent")
                controls_frame.pack(side="left", expand=True, pady=10)

                ctk.CTkButton(
                controls_frame, text="⏮", width=45,
                fg_color="#333333",
                command=self.play_previous
                ).pack(side="left", padx=5)

                self.play_pause_btn = ctk.CTkButton(
                controls_frame, text="▶ Play", width=90,
                fg_color="#00ff88", text_color="black",
                font=ctk.CTkFont(weight="bold"),
                command=self.toggle_play_pause
                )
                self.play_pause_btn.pack(side="left", padx=5)

                ctk.CTkButton(
                controls_frame, text="⏹ Stop", width=80,
                fg_color="#333333",
                command=self.stop_song
                ).pack(side="left", padx=5)

                ctk.CTkButton(
                controls_frame, text="⏭", width=45,
                fg_color="#333333",
                command=self.play_next
                ).pack(side="left", padx=5)

                volume_frame = ctk.CTkFrame(player_bar, fg_color="transparent")
                volume_frame.pack(side="right", padx=20, pady=10)

                ctk.CTkLabel(
                volume_frame,
                text="🔊 Volume",
                font=ctk.CTkFont(size=11)
                ).pack()

                self.volume_slider = ctk.CTkSlider(
                volume_frame, from_=0, to=1,
                width=120, command=self.set_volume
                )
                self.volume_slider.set(0.7)
                self.volume_slider.pack()

    def play_song(self, song):
        self.current_song = song
        self.now_playing_label.configure(text=song.title)
        self.now_playing_artist.configure(text=song.artist)
        self.play_pause_btn.configure(text="⏸ Pause")
        self.is_playing = True
        if PYGAME_AVAILABLE and song.file_path:
            try:
                pygame.mixer.music.load(song.file_path)
                pygame.mixer.music.play()
            except Exception:
                pass

    def toggle_play_pause(self):
        if not self.current_song:
            messagebox.showinfo("No Song", "Please select a song first!")
            return
        if self.is_playing:
            if PYGAME_AVAILABLE:
                pygame.mixer.music.pause()
            self.is_playing = False
            self.play_pause_btn.configure(text="▶ Play")
        else:
            if PYGAME_AVAILABLE:
                pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_pause_btn.configure(text="⏸ Pause")

    def stop_song(self):
        if PYGAME_AVAILABLE:
            pygame.mixer.music.stop()
        self.is_playing = False
        self.play_pause_btn.configure(text="▶ Play")
        self.now_playing_label.configure(text="No song selected")
        self.now_playing_artist.configure(text="")
        self.current_song = None

    def play_next(self):
        if not self.current_song:
            return
        idx = next((i for i, s in enumerate(self.songs)
                    if s.id == self.current_song.id), None)
        if idx is not None and idx + 1 < len(self.songs):
            self.play_song(self.songs[idx + 1])

    def play_previous(self):
        if not self.current_song:
            return
        idx = next((i for i, s in enumerate(self.songs)
                    if s.id == self.current_song.id), None)
        if idx is not None and idx - 1 >= 0:
            self.play_song(self.songs[idx - 1])

    def set_volume(self, value):
        if PYGAME_AVAILABLE:
            pygame.mixer.music.set_volume(float(value))

    def play_from_all_songs(self, event):
        try:
            idx = self.all_songs_listbox.curselection()[0]
            self.play_song(self.songs[idx])
        except IndexError:
            pass

if __name__ == "__main__":
    app = BoombaFM()
    app.mainloop()