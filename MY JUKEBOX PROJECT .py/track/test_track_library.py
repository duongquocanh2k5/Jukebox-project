import pytest
from track_library import Track, TrackLibrary
import json
import os

# Test cases for Track class
class TestTrack:
    def test_track_initialization(self):
        track = Track(1, "Test Song", "Test Artist", "Rock", "path/to/file", 4.5)
        # Verify that all fields are correctly assigned
        assert track.IdTrack == 1
        assert track.nameTrack == "Test Song"
        assert track.artist == "Test Artist"
        assert track.genre == "Rock"
        assert track.file_path == "path/to/file"
        assert track.rating == 4.5

    def test_track_to_dict(self): # Test conversion of a Track object to a dictionary
        track = Track(1, "Test Song", "Test Artist", "Rock", "path/to/file", 4.5)
        track_dict = track.to_dict()
        assert track_dict == {  #Verify that the dictionary representation matches expected values
            "IdTrack": 1,
            "nameTrack": "Test Song",
            "artist": "Test Artist",
            "genre": "Rock",
            "file_path": "path/to/file",
            "rating": 4.5
        }
 # Test creation of a Track object from a dictionary
    def test_track_from_dict(self):
        data = {
            "IdTrack": 1,
            "nameTrack": "Test Song",
            "artist": "Test Artist",
            "genre": "Rock",
            "file_path": "path/to/file",
            "rating": 4.5
        }
        track = Track.from_dict(data)
         # Verify that the Track object fields are correctly assigned
        assert track.IdTrack == 1
        assert track.nameTrack == "Test Song"
        assert track.rating == 4.5

 # Test creation of a Track object from a dictionary with missing optional fields
    def test_track_from_dict_without_optional_fields(self):
        data = {
            "IdTrack": 1,
            "nameTrack": "Test Song",
            "artist": "Test Artist",
            "genre": "Rock"
        }
        track = Track.from_dict(data) # Verify that missing fields are assigned default values
        assert track.rating == 0.0
        assert track.file_path is None

# Test cases for TrackLibrary class
class TestTrackLibrary: # Fixture to initialize a TrackLibrary instance for testing
    @pytest.fixture
    def track_library(self):
        return TrackLibrary("test_tracks.json")

    @pytest.fixture
    def sample_track(self): # Fixture to provide a sample Track object for tests
        return Track(1, "Test Song", "Test Artist", "Rock")

    def test_add_track(self, track_library, sample_track): # Test adding a track to the library
        track_library.add_track(sample_track)
        assert len(track_library.tracks) == 1
        assert track_library.tracks[0].IdTrack == 1

    def test_add_invalid_track(self, track_library):  # Test adding an invalid track (not a Track object)
        with pytest.raises(ValueError):
            track_library.add_track("Not a track object")

    def test_remove_track(self, track_library, sample_track): # Test removing a track from the library
        track_library.add_track(sample_track)
        track_library.remove_track(1)
        assert len(track_library.tracks) == 0

    def test_find_track(self, track_library, sample_track): # Test finding a track by ID in the library
        track_library.add_track(sample_track)
        found_track = track_library.find_track(1)
        assert found_track.nameTrack == "Test Song" # Verify that the correct track is found
        
        not_found_track = track_library.find_track(999)  # Verify that searching for a nonexistent track returns None
        assert not_found_track is None

    def test_find_track_by_name(self, track_library, sample_track):    # Test finding a track by name
        track_library.add_track(sample_track)
        found_track = track_library.find_track_by_name("Test") # Verify that the correct track is found
        assert found_track.IdTrack == 1
        
        not_found_track = track_library.find_track_by_name("Nonexistent")  #  Verify that searching for a nonexistent name returns None
        assert not_found_track is None

    def test_list_all_tracks(self, track_library, sample_track): # Test listing all tracks in the library
        track_library.add_track(sample_track)
        tracks_list = track_library.list_all_tracks()
        assert len(tracks_list) == 1
        assert tracks_list[0]["IdTrack"] == 1

    def test_save_and_load_from_file(self, track_library, sample_track):  # Test saving the library to a file and loading it back
        # Test saving
        track_library.add_track(sample_track) 
        track_library.save_to_file()
        assert os.path.exists("test_tracks.json") # Verify that the file exists

        # Test loading
        new_library = TrackLibrary("test_tracks.json")
        new_library.load_from_file()
        assert len(new_library.tracks) == 1 # Verify that the loaded library contains the correct track
        assert new_library.tracks[0].nameTrack == "Test Song"

        # Cleanup
        os.remove("test_tracks.json") #Remove the test file

# Test loading
    def test_load_nonexistent_file(self, track_library):
        track_library.file_path = "nonexistent.json"
        track_library.load_from_file()
        assert len(track_library.tracks) == 0 # Verify that the library remains empty

 # Test saving the library to an invalid file path
    def test_save_with_invalid_path(self, track_library, sample_track):
        track_library.file_path = "/invalid/path/tracks.json" # Invalid file path
        track_library.add_track(sample_track)
        # Should handle the error gracefully
        track_library.save_to_file()