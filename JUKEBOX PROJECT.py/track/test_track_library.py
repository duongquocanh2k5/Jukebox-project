import pytest
from track_library import Track, TrackLibrary
import json
import os

# Test cases for Track class
class TestTrack:
    def test_track_initialization(self):
        track = Track(1, "Test Song", "Test Artist", "Rock", "path/to/file", 4.5)
        assert track.IdTrack == 1
        assert track.nameTrack == "Test Song"
        assert track.artist == "Test Artist"
        assert track.genre == "Rock"
        assert track.file_path == "path/to/file"
        assert track.rating == 4.5

    def test_track_to_dict(self):
        track = Track(1, "Test Song", "Test Artist", "Rock", "path/to/file", 4.5)
        track_dict = track.to_dict()
        assert track_dict == {
            "IdTrack": 1,
            "nameTrack": "Test Song",
            "artist": "Test Artist",
            "genre": "Rock",
            "file_path": "path/to/file",
            "rating": 4.5
        }

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
        assert track.IdTrack == 1
        assert track.nameTrack == "Test Song"
        assert track.rating == 4.5

    def test_track_from_dict_without_optional_fields(self):
        data = {
            "IdTrack": 1,
            "nameTrack": "Test Song",
            "artist": "Test Artist",
            "genre": "Rock"
        }
        track = Track.from_dict(data)
        assert track.rating == 0.0
        assert track.file_path is None

# Test cases for TrackLibrary class
class TestTrackLibrary:
    @pytest.fixture
    def track_library(self):
        return TrackLibrary("test_tracks.json")

    @pytest.fixture
    def sample_track(self):
        return Track(1, "Test Song", "Test Artist", "Rock")

    def test_add_track(self, track_library, sample_track):
        track_library.add_track(sample_track)
        assert len(track_library.tracks) == 1
        assert track_library.tracks[0].IdTrack == 1

    def test_add_invalid_track(self, track_library):
        with pytest.raises(ValueError):
            track_library.add_track("Not a track object")

    def test_remove_track(self, track_library, sample_track):
        track_library.add_track(sample_track)
        track_library.remove_track(1)
        assert len(track_library.tracks) == 0

    def test_find_track(self, track_library, sample_track):
        track_library.add_track(sample_track)
        found_track = track_library.find_track(1)
        assert found_track.nameTrack == "Test Song"
        
        not_found_track = track_library.find_track(999)
        assert not_found_track is None

    def test_find_track_by_name(self, track_library, sample_track):
        track_library.add_track(sample_track)
        found_track = track_library.find_track_by_name("Test")
        assert found_track.IdTrack == 1
        
        not_found_track = track_library.find_track_by_name("Nonexistent")
        assert not_found_track is None

    def test_list_all_tracks(self, track_library, sample_track):
        track_library.add_track(sample_track)
        tracks_list = track_library.list_all_tracks()
        assert len(tracks_list) == 1
        assert tracks_list[0]["IdTrack"] == 1

    def test_save_and_load_from_file(self, track_library, sample_track):
        # Test saving
        track_library.add_track(sample_track)
        track_library.save_to_file()
        assert os.path.exists("test_tracks.json")

        # Test loading
        new_library = TrackLibrary("test_tracks.json")
        new_library.load_from_file()
        assert len(new_library.tracks) == 1
        assert new_library.tracks[0].nameTrack == "Test Song"

        # Cleanup
        os.remove("test_tracks.json")

    def test_load_nonexistent_file(self, track_library):
        track_library.file_path = "nonexistent.json"
        track_library.load_from_file()
        assert len(track_library.tracks) == 0

    def test_save_with_invalid_path(self, track_library, sample_track):
        track_library.file_path = "/invalid/path/tracks.json"
        track_library.add_track(sample_track)
        # Should handle the error gracefully
        track_library.save_to_file()