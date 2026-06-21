import PySimpleGUI as sg
import os
from pathlib import Path

# Set PySimpleGUI theme
sg.theme('DarkBlue3')


class MusicPlayer:
    def __init__(self):
        self.current_playlist = []
        self.current_index = 0
        self.is_playing = False
        self.music_folder = str(Path.home() / "Music")  # Default to user's Music folder

    def get_music_files(self, folder):
        """Get all music files from a folder"""
        supported_formats = ('.mp3', '.wav', '.flac', '.ogg', '.m4a')
        music_files = []

        try:
            for file in os.listdir(folder):
                if file.lower().endswith(supported_formats):
                    music_files.append(file)
            return sorted(music_files)
        except:
            return []

    def get_all_folders(self, start_path):
        """Get folder structure for Browse tab"""
        folders = []
        try:
            for item in os.listdir(start_path):
                path = os.path.join(start_path, item)
                if os.path.isdir(path):
                    folders.append(item)
        except:
            pass
        return sorted(folders)


def create_window():
    """Create the main window with three tabs"""
    player = MusicPlayer()

    # ==================== BROWSE TAB ====================
    browse_layout = [
        [sg.Text("📁 Browse Music Library", font=("Arial", 12, "bold"))],
        [sg.Text("Current Folder:"), sg.Text(player.music_folder, key="-CURRENT-FOLDER-", size=(40, 1))],
        [sg.Button("📂 Change Folder", key="-BROWSE-FOLDER-"),
         sg.Button("🔄 Refresh", key="-REFRESH-BROWSE-")],
        [sg.Multiline(size=(70, 20), key="-BROWSE-LIST-", disabled=True,
                      font=("Courier", 10))],
        [sg.Button("▶ Play Selected", key="-PLAY-FROM-BROWSE-"),
         sg.Button("➕ Add to Playlist", key="-ADD-TO-PLAYLIST-")]
    ]

    # ==================== SEARCH TAB ====================
    search_layout = [
        [sg.Text("🔍 Search Songs", font=("Arial", 12, "bold"))],
        [sg.Text("Search Query:"), sg.InputText(key="-SEARCH-INPUT-", size=(40, 1))],
        [sg.Button("🔎 Search", key="-SEARCH-BTN-"),
         sg.Button("Clear", key="-SEARCH-CLEAR-")],
        [sg.Multiline(size=(70, 15), key="-SEARCH-RESULTS-", disabled=True,
                      font=("Courier", 10))],
        [sg.Text(f"Found: 0 results", key="-SEARCH-COUNT-", text_color="yellow")],
        [sg.Button("▶ Play Selected", key="-PLAY-FROM-SEARCH-"),
         sg.Button("➕ Add to Playlist", key="-ADD-SEARCH-TO-PLAYLIST-")]
    ]

    # ==================== PLAYER TAB ====================
    player_layout = [
        [sg.Text("🎵 Now Playing", font=("Arial", 12, "bold"))],

        # Now Playing Info
        [sg.Text("Song:"), sg.Text("No song selected", key="-NOW-PLAYING-SONG-",
                                   size=(55, 1), text_color="yellow")],
        [sg.Text("Artist:"), sg.Text("Unknown", key="-NOW-PLAYING-ARTIST-", size=(55, 1))],

        # Progress Bar
        [sg.Text("Progress:"),
         sg.ProgressBar(100, orientation='h', size=(50, 20), key="-PROGRESS-BAR-"),
         sg.Text("0:00 / 3:00", key="-TIME-DISPLAY-")],

        # Control Buttons
        [sg.Button("⏮ Previous", key="-PREV-"),
         sg.Button("⏯ Play/Pause", key="-PLAY-PAUSE-", size=(12, 1)),
         sg.Button("⏭ Next", key="-NEXT-"),
         sg.Button("⏹ Stop", key="-STOP-"),
         sg.Button("🔁 Repeat", key="-REPEAT-")],

        # Volume Control
        [sg.Text("Volume:"),
         sg.Slider(range=(0, 100), default_value=70, orientation='h', size=(40, 15),
                   key="-VOLUME-SLIDER-"),
         sg.Text("70%", key="-VOLUME-DISPLAY-", size=(5, 1))],

        # Playlist
        [sg.Text("📋 Current Playlist", font=("Arial", 12, "bold"))],
        [sg.Multiline(size=(70, 10), key="-PLAYLIST-", disabled=True,
                      font=("Courier", 9))],
        [sg.Button("🗑 Clear Playlist", key="-CLEAR-PLAYLIST-"),
         sg.Button("💾 Save Playlist", key="-SAVE-PLAYLIST-"),
         sg.Button("📂 Load Playlist", key="-LOAD-PLAYLIST-")]
    ]

    # ==================== CREATE TABBED LAYOUT ====================
    layout = [
        [sg.Text("🎶 Music Player", font=("Arial", 16, "bold"))],
        [sg.TabGroup([
            [sg.Tab('Browse', browse_layout)],
            [sg.Tab('Search', search_layout)],
            [sg.Tab('Player', player_layout)]
        ], key="-TAB-GROUP-")],

        # Status Bar at bottom
        [sg.Text("Status: Ready", key="-STATUS-", text_color="lime"),
         sg.Text("", key="-STATUS-TIME-")]
    ]

    window = sg.Window('Music Player', layout, size=(800, 700), finalize=True)
    return window, player


def update_browse_list(window, player, folder):
    """Update the browse list with music files"""
    files = player.get_music_files(folder)
    content = "\n".join(files) if files else "No music files found in this folder"
    window["-BROWSE-LIST-"].update(content)
    window["-CURRENT-FOLDER-"].update(folder)


def search_songs(search_query, player):
    """Search for songs in the current folder"""
    files = player.get_music_files(player.music_folder)
    query_lower = search_query.lower()
    results = [f for f in files if query_lower in f.lower()]
    return results


def main():
    window, player = create_window()

    # Initialize browse tab with default music folder
    update_browse_list(window, player, player.music_folder)

    # Sample playlist for demo
    playlist = ["Song 1.mp3", "Song 2.mp3", "Song 3.mp3"]

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        # ==================== BROWSE TAB EVENTS ====================
        elif event == "-REFRESH-BROWSE-":
            update_browse_list(window, player, player.music_folder)
            window["-STATUS-"].update("Status: Folder refreshed")

        elif event == "-BROWSE-FOLDER-":
            folder = sg.popup_get_folder("Select Music Folder",
                                         default_path=player.music_folder)
            if folder:
                player.music_folder = folder
                update_browse_list(window, player, folder)
                window["-STATUS-"].update(f"Status: Folder changed to {folder}")

        elif event == "-PLAY-FROM-BROWSE-":
            selected = values["-BROWSE-LIST-"].strip()
            if selected:
                window["-NOW-PLAYING-SONG-"].update(selected)
                window["-PLAYLIST-"].update("\n".join(playlist))
                window["-STATUS-"].update(f"Status: Now playing {selected}")

        elif event == "-ADD-TO-PLAYLIST-":
            window["-STATUS-"].update("Status: Song added to playlist")

        # ==================== SEARCH TAB EVENTS ====================
        elif event == "-SEARCH-BTN-":
            search_query = values["-SEARCH-INPUT-"]
            if search_query:
                results = search_songs(search_query, player)
                search_text = "\n".join(results) if results else "No results found"
                window["-SEARCH-RESULTS-"].update(search_text)
                window["-SEARCH-COUNT-"].update(f"Found: {len(results)} results")
                window["-STATUS-"].update(f"Status: Found {len(results)} songs")
            else:
                window["-STATUS-"].update("Status: Enter a search query")

        elif event == "-SEARCH-CLEAR-":
            window["-SEARCH-INPUT-"].update("")
            window["-SEARCH-RESULTS-"].update("")
            window["-SEARCH-COUNT-"].update("Found: 0 results")
            window["-STATUS-"].update("Status: Search cleared")

        elif event == "-PLAY-FROM-SEARCH-":
            results = values["-SEARCH-RESULTS-"].strip()
            if results:
                song = results.split('\n')[0]
                window["-NOW-PLAYING-SONG-"].update(song)
                window["-STATUS-"].update(f"Status: Now playing {song}")

        # ==================== PLAYER TAB EVENTS ====================
        elif event == "-PLAY-PAUSE-":
            status = "Playing" if not player.is_playing else "Paused"
            player.is_playing = not player.is_playing
            window["-STATUS-"].update(f"Status: {status}")

        elif event == "-STOP-":
            player.is_playing = False
            window["-NOW-PLAYING-SONG-"].update("No song selected")
            window["-PROGRESS-BAR-"].update(0)
            window["-STATUS-"].update("Status: Stopped")

        elif event == "-PREV-":
            if player.current_index > 0:
                player.current_index -= 1
                window["-STATUS-"].update("Status: Previous song")

        elif event == "-NEXT-":
            if player.current_index < len(playlist) - 1:
                player.current_index += 1
                window["-STATUS-"].update("Status: Next song")

        elif event == "-REPEAT-":
            window["-STATUS-"].update("Status: Repeat enabled")

        elif event == "-VOLUME-SLIDER-":
            volume = int(values["-VOLUME-SLIDER-"])
            window["-VOLUME-DISPLAY-"].update(f"{volume}%")
            window["-STATUS-"].update(f"Status: Volume {volume}%")

        elif event == "-CLEAR-PLAYLIST-":
            playlist.clear()
            window["-PLAYLIST-"].update("")
            window["-STATUS-"].update("Status: Playlist cleared")

        elif event == "-SAVE-PLAYLIST-":
            window["-STATUS-"].update("Status: Playlist saved")

        elif event == "-LOAD-PLAYLIST-":
            window["-STATUS-"].update("Status: Playlist loaded")

    window.close()


if __name__ == "__main__":
    main()