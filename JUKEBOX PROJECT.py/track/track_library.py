import json

class Track:
    def __init__(self, IdTrack, nameTrack, artist, genre, file_path=None, rating=0.0):
        self.IdTrack = IdTrack
        self.nameTrack = nameTrack
        self.artist = artist
        self.genre = genre
        self.file_path = file_path
        self.rating = rating

    def to_dict(self):
        return {
            "IdTrack": self.IdTrack,
            "nameTrack": self.nameTrack,
            "artist": self.artist,
            "genre": self.genre,
            "file_path": self.file_path,
            "rating": self.rating
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            IdTrack=data["IdTrack"],
            nameTrack=data["nameTrack"],
            artist=data["artist"],
            genre=data["genre"],
            rating=data.get("rating", 0.0),
            file_path=data.get("file_path")
        )


class TrackLibrary:
    def __init__(self, file_path="tracks.json"):
        self.file_path = file_path
        self.tracks = []

    def add_track(self, track):
        if not isinstance(track, Track):
            raise ValueError("The provided object is not an instance of Track.")
        self.tracks.append(track)

    def remove_track(self, IdTrack):
        self.tracks = [track for track in self.tracks if track.IdTrack != IdTrack]

    def find_track(self, track_id):
        for track in self.tracks:
            if track.IdTrack == int(track_id):
                return track
        return None

    def find_track_by_name(self, track_name):
        for track in self.tracks:
            if track_name.lower() in track.nameTrack.lower():
                return track
        return None

    def list_all_tracks(self):
        return [track.to_dict() for track in self.tracks]  # Return list of dictionaries

    def save_to_file(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([track.to_dict() for track in self.tracks], file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving tracks: {e}")

    def load_from_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tracks = [Track.from_dict(item) for item in data]  # Convert JSON objects to Track objects
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found. Starting with an empty library.")
            self.tracks = []
        except Exception as e:
            print(f"Error loading tracks: {e}")
