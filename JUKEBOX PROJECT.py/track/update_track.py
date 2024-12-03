import tkinter as tk
from tkinter import messagebox

def update_track_gui(library):
    update_window = tk.Toplevel()
    update_window.title("Update Track")
    update_window.geometry("400x350")
    update_window.configure(bg="#1a1a1a")

    tk.Label(update_window, text="Track ID").grid(row=0, column=0)
    id_entry = tk.Entry(update_window)
    id_entry.grid(row=0, column=1)

    tk.Label(update_window, text="New Name").grid(row=1, column=0)
    name_entry = tk.Entry(update_window)
    name_entry.grid(row=1, column=1)

    tk.Label(update_window, text="New Artist").grid(row=2, column=0)
    artist_entry = tk.Entry(update_window)
    artist_entry.grid(row=2, column=1)

    tk.Label(update_window, text="New Genre").grid(row=3, column=0)
    genre_entry = tk.Entry(update_window)
    genre_entry.grid(row=3, column=1)

    tk.Label(update_window, text="New Rating").grid(row=4, column=0)
    rating_entry = tk.Entry(update_window)
    rating_entry.grid(row=4, column=1)

    tk.Label(update_window, text="New File Path / YouTube Link").grid(row=5, column=0)
    file_entry = tk.Entry(update_window)
    file_entry.grid(row=5, column=1)

    def update_track():
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
        if new_rating and not new_rating.isdigit():
            messagebox.showerror("Input Error", "Rating must be a valid integer")
            return

        track = library.find_track(IdTrack)
        if track:
            # Update track information
            if new_name:
                track["nameTrack"] = new_name
            if new_artist:
                track["artist"] = new_artist
            if new_genre:
                track["genre"] = new_genre
            if new_rating:
                track["rating"] = int(new_rating)  # Ensure rating is saved as an integer
            if new_file_path:
                track["file_path"] = new_file_path

            library.save_to_file()  # Save updated library to JSON
            messagebox.showinfo("Success", "Track updated successfully")
        else:
            messagebox.showerror("Error", "Track not found")
        update_window.destroy()

    tk.Button(update_window, text="Update", command=update_track).grid(row=6, column=0, columnspan=2)
