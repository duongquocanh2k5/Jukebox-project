import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import time
import threading
import pygame
import webbrowser

from create_track_list import add_track_gui
from remove_track import remove_track_gui
from find_track import find_track_gui
from update_track import update_track_gui
from track_library import TrackLibrary

pygame.mixer.init()

class ModernJukeBox:
    def __init__(self):
        self.library = TrackLibrary()
        try:
            self.library.load_from_file()
        except Exception as e:
            print(f"Error loading library: {e}")
            self.library.tracks = []

        self.root = tk.Tk()
        self.root.title("Modern Music Player")
        self.root.geometry("750x400")
        self.root.configure(bg="#1E1E1E")  # Dark theme background

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.setup_styles()
        self.create_header()
        self.create_main_layout()
        self.create_player_controls()
        self.start_time_thread()

    def setup_styles(self):
        self.style = ttk.Style()
        
        # Modern dark theme colors
        self.primary_color = "#9750ab"     # Dark background
        self.secondary_color = "#252525"    # Slightly lighter dark
        self.accent_color = "#0078D4"      # Blue accent
        self.text_color = "#4302ab"        #  text color 
        self.subtle_text = "#ab83eb"       #  text color

        self.style.configure("Header.TFrame", background=self.primary_color)
        self.style.configure("Main.TFrame", background=self.secondary_color)
        self.style.configure("Controls.TFrame", background=self.primary_color)
        
        # Modern button style
        self.style.configure(
            "Modern.TButton",
            background=self.accent_color,
            foreground=self.text_color,
            padding=8,
            font=("Segoe UI", 10)
        )

    def create_header(self):
        header = ttk.Frame(self.root, style="Header.TFrame", height=60)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # Modern app title
        title = ttk.Label(
            header,
            text=" MUSIC BOX",
            font=("Segoe UI", 18, "bold"),
            foreground=self.accent_color,
            background=self.primary_color
        )
        title.pack(side="left", padx=20)

        # Search bar
        search_frame = ttk.Frame(header, style="Header.TFrame")
        search_frame.pack(side="right", padx=20)
        
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)

        self.time_label = ttk.Label(
            search_frame,
            font=("Segoe UI", 10),
            foreground=self.text_color,
            background=self.primary_color
        )
        self.time_label.pack(side="right", padx=20)

    def create_main_layout(self):
        # Navigation sidebar
        sidebar = ttk.Frame(self.root, style="Main.TFrame", width=200)
        sidebar.grid(row=1, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        nav_items = [
            ("Library", lambda: self.show_frame("library")),
            ("Add Music", lambda: add_track_gui(self.library)),
            ("Find Track", lambda: find_track_gui(self.library)),
            ("Remove Track", lambda: remove_track_gui(self.library)),
            ("Update Track", lambda: update_track_gui(self.library))
        ]

        for text, command in nav_items:
            btn = ttk.Button(
                sidebar,
                text=text,
                style="Modern.TButton",
                command=command
            )
            btn.pack(fill="x", padx=10, pady=5)

        # Main content area
        self.main_content = ttk.Frame(self.root, style="Main.TFrame")
        self.main_content.grid(row=1, column=1, sticky="nsew")

        self.frames = {}
        for page in ["library", "search", "playlists"]:
            frame = ttk.Frame(self.main_content, style="Main.TFrame")
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            if page == "library":
                self.create_library_view(frame)
            elif page == "search":
                self.create_search_view(frame)
            elif page == "playlists":
                self.create_playlists_view(frame)

        self.show_frame("library")

    def create_player_controls(self):
        controls = ttk.Frame(self.root, style="Controls.TFrame", height=100)
        controls.grid(row=2, column=0, columnspan=2, sticky="ew")
        controls.grid_propagate(False)

        # Track info
        info_frame = ttk.Frame(controls, style="Controls.TFrame")
        info_frame.pack(side="left", padx=20)

        self.track_name_label = ttk.Label(
            info_frame,
            text="No Track Playing",
            font=("Segoe UI", 12),
            foreground=self.text_color,
            background=self.primary_color
        )
        self.track_name_label.pack(anchor="w")

        # Playback controls
        control_frame = ttk.Frame(controls, style="Controls.TFrame")
        control_frame.pack(side="left", expand=True)

        self.is_playing = False
        self.current_time = 0
        self.current_track = None

        self.time_label_playbar = ttk.Label(
            control_frame,
            text="0:00",
            foreground=self.text_color,
            background=self.primary_color
        )
        self.time_label_playbar.pack(side="left", padx=5)

        self.play_pause_button = ttk.Button(
            control_frame,
            text="▶",
            style="Modern.TButton",
            command=self.play_pause_track
        )
        self.play_pause_button.pack(side="left", padx=10)

    def create_library_view(self, parent):
        tracks_frame = ttk.Frame(parent, style="Main.TFrame")
        tracks_frame.pack(fill="both", expand=True, padx=20, pady=20)

        headers = ["Title", "Artist", "Genre", "Rating"]
        for i, header in enumerate(headers):
            ttk.Label(
                tracks_frame,
                text=header,
                font=("Segoe UI", 12, "bold"),
                foreground=self.text_color,
                background=self.secondary_color
            ).grid(row=0, column=i, padx=10, pady=5, sticky="w")

        if self.library.tracks:
            for i, track in enumerate(self.library.tracks, 1):
                track_label = ttk.Label(
                    tracks_frame,
                    text=track.nameTrack,
                    foreground=self.text_color,
                    background=self.secondary_color
                )
                track_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                track_label.bind("<Button-1>", lambda event, t=track: self.play_track_from_library(t))

                ttk.Label(
                    tracks_frame,
                    text=track.artist,
                    foreground=self.text_color,
                    background=self.secondary_color
                ).grid(row=i, column=1, padx=10, pady=5, sticky="w")

                ttk.Label(
                    tracks_frame,
                    text=track.genre,
                    foreground=self.text_color,
                    background=self.secondary_color
                ).grid(row=i, column=2, padx=10, pady=5, sticky="w")

                ttk.Label(
                    tracks_frame,
                    text=str(track.rating),
                    foreground=self.text_color,
                    background=self.secondary_color
                ).grid(row=i, column=3, padx=10, pady=5, sticky="w")

    def create_search_view(self, parent):
        ttk.Label(
            parent,
            text="Search Music",
            font=("Segoe UI", 24, "bold"),
            foreground=self.text_color,
            background=self.secondary_color
        ).pack(pady=50)

    def create_playlists_view(self, parent):
        ttk.Label(
            parent,
            text="Playlists",
            font=("Segoe UI", 24, "bold"),
            foreground=self.text_color,
            background=self.secondary_color
        ).pack(pady=50)

    # The remaining methods (show_frame, play_pause_track, start_playback, etc.) 
    # remain exactly the same as they handle core functionality

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

    def play_pause_track(self):
        if self.current_track:
            if not self.is_playing:
                self.start_playback()
            else:
                self.pause_playback()
        else:
            messagebox.showwarning("Warning", "Please select a track first")

    def start_playback(self):
        if self.current_track and self.current_track.file_path and self.current_track.file_path.startswith("http"):
            webbrowser.open(self.current_track.file_path)
            self.play_pause_button.configure(text="⏹")
            return

        try:
            pygame.mixer.music.play()
            self.is_playing = True
            self.update_time_playbar()
            self.play_pause_button.configure(text="⏸")
            self.track_name_label.config(text=f"{self.current_track.nameTrack} - {self.current_track.artist}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not play the track: {e}")

    def pause_playback(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.play_pause_button.configure(text="▶")

    def stop_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_time = 0
        self.time_label_playbar.configure(text="0:00")
        self.play_pause_button.configure(text="▶")
        self.current_track = None
        self.track_name_label.config(text="No Track Playing")

    def update_time_playbar(self):
        if self.is_playing:
            try:
                self.current_time = pygame.mixer.music.get_pos() // 1000
                minutes, seconds = divmod(self.current_time, 60)
                time_string = f"{minutes:02d}:{seconds:02d}"
                self.time_label_playbar.configure(text=time_string)
                self.root.after(1000, self.update_time_playbar)
            except pygame.error:
                self.stop_track()

    def play_track_from_library(self, track):
        if not track:
            return

        self.current_track = track

        if track.file_path and track.file_path.startswith("http"):
            webbrowser.open(track.file_path)
            messagebox.showinfo("Now Playing", f"Playing {track.nameTrack} on YouTube")
            self.play_pause_button.configure(text="▶")
            return

        try:
            pygame.mixer.music.load(track.file_path)
            self.start_playback()
        except Exception as e:
            messagebox.showerror("Error", f"Could not play track: {e}")

    def update_time(self):
        while True:
            current_time = time.strftime("%I:%M %p")
            self.time_label.configure(text=current_time)
            time.sleep(1)

    def start_time_thread(self):
        time_thread = threading.Thread(target=self.update_time, daemon=True)
        time_thread.start()

    def run(self):
        self.root.mainloop()

def main_gui():
    app = ModernJukeBox()
    app.run()

if __name__ == "__main__":
    main_gui()