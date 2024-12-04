import tkinter as tk
from tkinter import ttk, messagebox

# Function to create a GUI for finding tracks in the library
def find_track_gui(library):
    # Create a new top-level window for the "Find Track" functionality
    find_window = tk.Toplevel()
    find_window.title("Find Track")# Set the window title
    find_window.geometry("400x300")# Set the window size
    
    # Create search frame
    search_frame = ttk.Frame(find_window)
    search_frame.pack(fill="x", padx=10, pady=5)# Add padding for aesthetics
    
    # Create search options
    search_by = ttk.Combobox(search_frame, values=["ID", "Name", "Artist", "Genre"])
    search_by.set("Name")# Default search criterion is "Name"
    search_by.pack(side="left", padx=5)# Align to the left with some padding

     # Input field for entering the search query
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)# Expand to fill available space
    
    # Results listbox
    results_frame = ttk.Frame(find_window)
    results_frame.pack(fill="both", expand=True, padx=10, pady=5)
       # Listbox to display search results
    results_list = tk.Listbox(results_frame, width=50)
    # Scrollbar to handle long lists
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_list.yview)
    results_list.configure(yscrollcommand=scrollbar.set)# Connect scrollbar to listbox
    
    # Pack the listbox and scrollbar in the results frame
    results_list.pack(side="left", fill="both", expand=True)# Expand listbox to fit frame
    scrollbar.pack(side="right", fill="y") # Scrollbar aligned to the right, filling vertically

    # Function to handle track searchin
    def search_tracks(): 
        results_list.delete(0, tk.END)  # Clear the current results from the listbox
        search_text = search_entry.get().lower()# Get the search text and convert to lowercase for case-insensitive matching
        search_type = search_by.get()  # Get the selected search criterion (ID, Name, Artist, or Genre)
        
        for track in library.tracks:  # Iterate through the library's tracks and search based on the selected criterion
              # Check if the search query matches the track's attributes
            if search_type == "ID" and search_text in track.IdTrack.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
            elif search_type == "Name" and search_text in track.nameTrack.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
            elif search_type == "Artist" and search_text in track.artist.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
            elif search_type == "Genre" and search_text in track.genre.lower():
                results_list.insert(tk.END, f"ID: {track.IdTrack} - {track.nameTrack} by {track.artist}")
    
    # Button to trigger the search_tracks function
    ttk.Button(find_window, text="Search", command=search_tracks).pack(pady=5)
# Function to display details of a selected track
    def show_details():
        selection = results_list.curselection()  # Get the currently selected item from the listbox
        if selection: # Ensure an item is selected
            track_info = results_list.get(selection[0]) # Get the selected track information
            track_id = track_info.split("-")[0].replace("ID:", "").strip() # Extract the track ID
            track = library.find_track(track_id) # Find the track in the library using the extracted ID
            if track:  # Show a message box with detailed track information
                info = f"ID: {track.IdTrack}\nName: {track.nameTrack}\nArtist: {track.artist}\nGenre: {track.genre}"
                messagebox.showinfo("Track Details", info)
     # Button to trigger the show_details function
    ttk.Button(find_window, text="Show Details", command=show_details).pack(pady=5)