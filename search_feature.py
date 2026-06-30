import tkinter as tk
from tkinter import messagebox
from library import get_all_songs


def create_search_tab(self):
    self.current_search_results = []

    tk.Label(self.search_tab, text="Search Artist or Genre:", fg="white", bg="#1a1a1a",
             font=("Arial", 12, "bold")).pack(pady=10)

    self.search_entry = tk.Entry(self.search_tab, width=40, font=("Arial", 11))
    self.search_entry.pack(pady=5)

    search_btn = tk.Button(self.search_tab, text="Search", bg="#00ff88", fg="black", font=("Arial", 10, "bold"),
                           width=15, command=self.perform_search)
    search_btn.pack(pady=5)

    self.search_results = tk.Listbox(self.search_tab, height=15, bg="#2a2a2a", fg="white", font=("Arial", 10))
    self.search_results.pack(fill="both", expand=True, padx=20, pady=10)
    self.search_results.bind("<Double-Button-1>", self.play_selected_song)


def perform_search(self):
    query = self.search_entry.get().lower().strip()

    if not query:
        messagebox.showwarning("Empty", "Please enter a search term")
        return

    songs = get_all_songs()

    self.current_search_results = [
        song for song in songs if
        query in song.artist.lower() or
        query in song.genre.lower() or
        query in song.title.lower()
    ]

    self.search_results.delete(0, tk.END)

    if self.current_search_results:
        for song in self.current_search_results:
            self.search_results.insert(tk.END, f"{song.title} - {song.artist}")
    else:
        self.search_results.insert(tk.END, "No results found")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Boomba FM - Search Testing")
    window.geometry("400x500")
    window.configure(bg="#1a1a1a")


    class BlankApp:
        def __init__(self, root_window):
            self.search_tab = root_window
            create_search_tab(self)

        def perform_search(self):
            perform_search(self)

        def play_selected_song(self, event):
            try:
                selected_idx = self.search_results.curselection()[0]
                clicked_song = self.current_search_results[selected_idx]
                messagebox.showinfo("Playback Trigger",
                                    f"Double-clicked!\nSong: {clicked_song.title}\nArtist: {clicked_song.artist}")
            except IndexError:
                pass


    app = BlankApp(window)
    window.mainloop()
