import tkinter as tk
from tkinter import messagebox, filedialog
from track_library import Track, TrackLibrary

# Function to create a GUI window for adding a new track
def add_track_gui(library):
    # Create a new top-level window for the "Add Track" feature
    add_window = tk.Toplevel()
    add_window.title("Add Track")
    add_window.geometry("400x350")

# Input field for Track ID
    tk.Label(add_window, text="ID").grid(row=0, column=0)
    id_entry = tk.Entry(add_window)
    id_entry.grid(row=0, column=1)

  # Input field for Track Name
    tk.Label(add_window, text="Name").grid(row=1, column=0)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=1, column=1)

    # Input field for Artist Name
    tk.Label(add_window, text="Artist").grid(row=2, column=0)
    artist_entry = tk.Entry(add_window)
    artist_entry.grid(row=2, column=1)

    # Input field for Genre
    tk.Label(add_window, text="Genre").grid(row=3, column=0)
    genre_entry = tk.Entry(add_window)
    genre_entry.grid(row=3, column=1)

  # Input field for Rating (1 to 5)
    tk.Label(add_window, text="Rating").grid(row=4, column=0)
    rating_entry = tk.Entry(add_window)
    rating_entry.grid(row=4, column=1)

 # Input field for File Path or YouTube Link
    tk.Label(add_window, text="File Path / YouTube Link").grid(row=5, column=0)
    file_entry = tk.Entry(add_window)
    file_entry.grid(row=5, column=1)
    
 # Function to allow the user to browse and select a file
    def browse_file():
        # Choose a file from the system
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path: # If a file is selected, update the file entry field
            file_entry.delete(0, tk.END) # Clear the current entry
            file_entry.insert(0, file_path)# Insert the selected file path

    # Button to browse files
    tk.Button(add_window, text="Browse", command=browse_file).grid(row=5, column=2)

 # Function to validate inputs and save the new track
    def save_track():
         # Get input values from all fields, stripping any leading/trailing whitespace
        IdTrack = id_entry.get().strip()
        nameTrack = name_entry.get().strip()
        artist = artist_entry.get().strip()
        genre = genre_entry.get().strip()
        rating = rating_entry.get().strip()
        file_path = file_entry.get().strip()

        # Input validation
        if not IdTrack or not nameTrack or not artist or not genre or not file_path:
            messagebox.showerror("Input Error", "Please fill all fields correctly")
            return
        
  # Validate the rating, if provide
        if rating:# Rating is optional
            if not rating.isdigit() or not (1 <= int(rating) <= 5):
                # Ensure rating is an integer between 1 and 5
                messagebox.showerror("Input Error", "Rating must be an integer between 1 and 5")
                return
            rating = int(rating)  # Convert rating to integer

        # Create a new track and save
        track = Track(IdTrack, nameTrack, artist, genre, file_path, rating)
        # Add the new track to the library and save the updated library to a file
        library.add_track(track)
        library.save_to_file()  # Save updated library to JSON
        messagebox.showinfo("Success", "Track added successfully") # Notify the user of success
        add_window.destroy() # Close the Add Track window
        
    # Button to save the track, connected to save_track function
    tk.Button(add_window, text="Save", command=save_track).grid(row=6, column=0, columnspan=2)
