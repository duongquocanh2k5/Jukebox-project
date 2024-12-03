import tkinter as tk
from tkinter import ttk, messagebox

def remove_track_gui(library):
    remove_window = tk.Toplevel()
    remove_window.title("Remove Track")
    remove_window.geometry("400x300")
    
    # Create track selection frame
    track_frame = ttk.Frame(remove_window)
    track_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create track listbox with scrollbar
    track_listbox = tk.Listbox(track_frame, width=50)
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
            library.remove_track(track_id)
            messagebox.showinfo("Success", "Track removed successfully")
            remove_window.destroy()

    ttk.Button(remove_window, text="Delete Selected Track", command=delete_track).pack(pady=10)