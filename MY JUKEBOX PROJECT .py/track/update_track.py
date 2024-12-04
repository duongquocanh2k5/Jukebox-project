import tkinter as tk
from tkinter import messagebox
import json

def update_track_gui(library):
    update_window = tk.Toplevel()
    update_window.title("Update Track")
    update_window.geometry("400x350")
    update_window.configure(bg="#1a1a1a")

    tk.Label(update_window, text="Track ID", bg="#1a1a1a", fg="white").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(update_window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(update_window, text="New Name", bg="#1a1a1a", fg="white").grid(row=1, column=0, padx=5, pady=5)
    name_entry = tk.Entry(update_window)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(update_window, text="New Artist", bg="#1a1a1a", fg="white").grid(row=2, column=0, padx=5, pady=5)
    artist_entry = tk.Entry(update_window)
    artist_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(update_window, text="New Genre", bg="#1a1a1a", fg="white").grid(row=3, column=0, padx=5, pady=5)
    genre_entry = tk.Entry(update_window)
    genre_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(update_window, text="New Rating", bg="#1a1a1a", fg="white").grid(row=4, column=0, padx=5, pady=5)
    rating_entry = tk.Entry(update_window)
    rating_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(update_window, text="New File Path / YouTube Link", bg="#1a1a1a", fg="white").grid(row=5, column=0, padx=5, pady=5)
    file_entry = tk.Entry(update_window)
    file_entry.grid(row=5, column=1, padx=5, pady=5)

    def update_track():
        try:
            IdTrack = id_entry.get().strip()
            new_name = name_entry.get().strip()
            new_artist = artist_entry.get().strip()
            new_genre = genre_entry.get().strip()
            new_rating = rating_entry.get().strip()
            new_file_path = file_entry.get().strip()

            # Validate input
            if not IdTrack:
                messagebox.showerror("Input Error", "Track ID is required")
                return
            
            if new_rating and not new_rating.replace('.', '').isdigit():
                messagebox.showerror("Input Error", "Rating must be a valid number")
                return

            # Read current JSON data
            try:
                with open('tracks.json', 'r', encoding='utf-8') as file:
                    tracks_data = json.load(file)
            except FileNotFoundError:
                messagebox.showerror("Error", "tracks.json file not found")
                return
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format in tracks.json")
                return

            # Find and update the track in JSON data
            track_found = False
            for track in tracks_data:
                if track["IdTrack"] == IdTrack:
                    track_found = True
                    if new_name:
                        track["nameTrack"] = new_name
                    if new_artist:
                        track["artist"] = new_artist
                    if new_genre:
                        track["genre"] = new_genre
                    if new_rating:
                        track["rating"] = float(new_rating)
                    if new_file_path:
                        track["file_path"] = new_file_path
                    break

            if not track_found:
                messagebox.showerror("Error", "Track ID not found")
                return

            # Save updated JSON data
            try:
                with open('tracks.json', 'w', encoding='utf-8') as file:
                    json.dump(tracks_data, file, indent=4, ensure_ascii=False)
                
                # Update the Track object in library
                track_obj = library.find_track(IdTrack)
                if track_obj:
                    if new_name:
                        track_obj.nameTrack = new_name
                    if new_artist:
                        track_obj.artist = new_artist
                    if new_genre:
                        track_obj.genre = new_genre
                    if new_rating:
                        track_obj.rating = float(new_rating)
                    if new_file_path:
                        track_obj.file_path = new_file_path

                messagebox.showinfo("Success", "Track updated successfully")
                update_window.destroy()
                
                # Reload the library from the updated JSON
                library.load_from_file()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save updates: {str(e)}")
                return

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    update_btn = tk.Button(update_window, text="Update", command=update_track, bg="#4a4a4a", fg="white")
    update_btn.grid(row=6, column=0, columnspan=2, pady=20)