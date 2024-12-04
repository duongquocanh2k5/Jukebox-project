import json
# Class to represent an individual track with its details
class Track:
    def __init__(self, IdTrack, nameTrack, artist, genre, file_path=None, rating=0.0):  # Initialize track attributes
        self.IdTrack = IdTrack # Unique identifier for the track
        self.nameTrack = nameTrack  #Name of the track
        self.artist = artist    # Artist of the track
        self.genre = genre     # Genre of the track
        self.file_path = file_path    # File path or URL 
        self.rating = rating     # Rating of the track 

 # Convert the track object to a dictionary
    def to_dict(self):
        return {
            "IdTrack": self.IdTrack,
            "nameTrack": self.nameTrack,
            "artist": self.artist,
            "genre": self.genre,
            "file_path": self.file_path,
            "rating": self.rating
        }
 # Create a Track object
    @classmethod
    def from_dict(cls, data):
        # Use dictionary keys to initialize the track
        return cls(
            IdTrack=data["IdTrack"],
            nameTrack=data["nameTrack"],
            artist=data["artist"],
            genre=data["genre"],
            rating=data.get("rating", 0.0),  # Default to 0.0 if "rating" key is missing
            file_path=data.get("file_path")   # Default to None if "file_path" key is missing
        )

# Class to manage a collection of tracks and perform operations on them
class TrackLibrary: 
    def __init__(self, file_path="tracks.json"):
        # Initialize the library with a file path and an empty track list
        self.file_path = file_path  # Path to the JSON file for saving/loading tracks
        self.tracks = []  # List to store Track objects

# Add a new track
    def add_track(self, track):
        if not isinstance(track, Track):
            raise ValueError("The provided object is not an instance of Track.")
        self.tracks.append(track)

# Remove a track
    def remove_track(self, IdTrack):
        self.tracks = [track for track in self.tracks if track.IdTrack != IdTrack]
# Fine a track 
    def find_track(self, track_id):
        for track in self.tracks:
            if track.IdTrack == int(track_id):
                return track
        return None
# Find a track in the library by its name
    def find_track_by_name(self, track_name):
        for track in self.tracks:
            if track_name.lower() in track.nameTrack.lower():
                return track
        return None
 # List all tracks  
    def list_all_tracks(self):
        return [track.to_dict() for track in self.tracks]  # Return list of dictionaries
# Save all tracks
    def save_to_file(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([track.to_dict() for track in self.tracks], file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving tracks: {e}")
# Load tracks from a JSON file
    def load_from_file(self):
        try: # Open the file in read mode and load JSON data
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tracks = [Track.from_dict(item) for item in data]  # Convert JSON objects to Track objects
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found. Starting with an empty library.")
            self.tracks = [] # Initialize an empty track list
        except Exception as e: # Catch and print any other errors
            print(f"Error loading tracks: {e}")
