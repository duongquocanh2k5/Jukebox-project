import tkinter as tk
from tkinter import ttk, messagebox
import json

def remove_track_gui(library):
    remove_window = tk.Toplevel()
    remove_window.title("Remove Track")
    remove_window.geometry("400x300")
    remove_window.configure(bg="#1a1a1a")
    
    # Create track selection frame
    track_frame = ttk.Frame(remove_window)
    track_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create track listbox with scrollbar
    track_listbox = tk.Listbox(track_frame, width=50, bg="#2a2a2a", fg="white")
    scrollbar = ttk.Scrollbar(track_frame, orient="vertical", command=track_listbox.yview)
    track_listbox.configure(yscrollcommand=scrollbar.set)
    
    # Pack widgets
    track_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Populate listbox with tracks
    for track in library.tracks:
        track_listbox.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
    
    def delete_track():
        selection = track_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a track to remove")
            return
            
        track_info = track_listbox.get(selection[0])
        track_id = track_info.split("-")[0].replace("ID:", "").strip()

        if messagebox.askyesno("Confirm", f"Are you sure you want to remove: {track_info}?"):
            try:
                # Read current JSON data
                with open('tracks.json', 'r', encoding='utf-8') as file:
                    tracks_data = json.load(file)
                
                # Remove track from JSON data
                tracks_data = [track for track in tracks_data if track["IdTrack"] != track_id]
                
                # Save updated JSON data
                with open('tracks.json', 'w', encoding='utf-8') as file:
                    json.dump(tracks_data, file, indent=4, ensure_ascii=False)
                
                # Remove from library
                library.remove_track(track_id)
                
                # Reload library from updated JSON
                library.load_from_file()
                
                messagebox.showinfo("Success", "Track removed successfully")
                remove_window.destroy()
                
            except FileNotFoundError:
                messagebox.showerror("Error", "tracks.json file not found")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format in tracks.json")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    delete_button = tk.Button(
        remove_window, 
        text="Delete Selected Track", 
        command=delete_track,
        bg="#4a4a4a",
        fg="white"
    )
    delete_button.pack(pady=10)