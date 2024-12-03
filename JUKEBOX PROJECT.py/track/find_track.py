import tkinter as tk
from tkinter import ttk, messagebox

def find_track_gui(library):
    find_window = tk.Toplevel()
    find_window.title("Find Track")
    find_window.geometry("400x300")
    
    # Create search frame
    search_frame = ttk.Frame(find_window)
    search_frame.pack(fill="x", padx=10, pady=5)
    
    # Create search options
    search_by = ttk.Combobox(search_frame, values=["ID", "Name", "Artist", "Genre"])
    search_by.set("Name")
    search_by.pack(side="left", padx=5)
    
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    # Results listbox
    results_frame = ttk.Frame(find_window)
    results_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    results_list = tk.Listbox(results_frame, width=50)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_list.yview)
    results_list.configure(yscrollcommand=scrollbar.set)
    
    results_list.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def search_tracks():
        results_list.delete(0, tk.END)
        search_text = search_entry.get().lower()
        search_type = search_by.get()
        
        for track in library.tracks:
            if search_type == "ID" and search_text in track.IdTrack.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
            elif search_type == "Name" and search_text in track.nameTrack.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
            elif search_type == "Artist" and search_text in track.artist.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
            elif search_type == "Genre" and search_text in track.genre.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
    
    ttk.Button(find_window, text="Search", command=search_tracks).pack(pady=5)

    def show_details():
        selection = results_list.curselection()
        if selection:
            track_info = results_list.get(selection[0])
            track_id = track_info.split("-")[0].replace("ID:", "").strip()
            track = library.find_track(track_id)
            if track:
                info = f"ID: {track.IdTrack}\nName: {track.nameTrack}\nArtist: {track.artist}\nGenre: {track.genre}"
                messagebox.showinfo("Track Details", info)
    
    ttk.Button(find_window, text="Show Details", command=show_details).pack(pady=5)