def setup_browse_tab(self):
    # Create genre dropdown
    genre_label = tk.Label(self.browse_tab, text="Choose a Genre", fg="yellow", bg="black")
    genre_label.grid(row=0, column=0, padx=5, pady=5)

    unique_genres = sorted({s["genre"] for s in songs})
    self.genre_choice = tk.StringVar()
    genre_menu = ttk.Combobox(self.browse_tab, textvariable=self.genre_choice, values=unique_genres)
    genre_menu.grid(row=0, column=1, padx=5, pady=5)
    genre_menu.bind("<<ComboboxSelected>>", self.update_song_list)

    # Song listbox
    self.song_display = tk.Listbox(self.browse_tab, width=50, height=12, bg="gray20", fg="white")
    self.song_display.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Show all songs initially
    self.show_songs(songs)

def show_songs(self, song_data):
    self.song_display.delete(0, tk.END)
    for s in song_data:
        entry = f"{s['artist']} - {s['title']} [{s['genre']}]"
        self.song_display.insert(tk.END, entry)
    self.song_display.bind("<Double-Button-1>", self.play_selected_song)

def update_song_list(self, event):
    chosen = self.genre_choice.get()
    filtered = [s for s in songs if s["genre"] == chosen]
    self.show_songs(filtered)
