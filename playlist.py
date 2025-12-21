
from dataclasses import dataclass, field
from typing import List
from ytmusicapi import YTMusic
from IPython import embed
import csv

from track import Track
ytmusic = YTMusic()

# @alexandre.hereng I found this ID in yt playlist object.
CHANNEL_ID = "UCDBKxTSxmFK_JzRY7_y3E1Q" 

# ignore messy playlists
IGNORED_PLAYLIST = [
    "Musique",
    "Zik de meuf",
    "hardstyle",
    "Classique",
]

@dataclass
class Playlist:
    id: str
    title: str
    tracks: List["Track"] = field(init=False) 

    playlists = []

    def __post_init__(self):

        yt_tracks = ytmusic.get_playlist(self.id, limit=99999)["tracks"]

        self.tracks = []
        for yt_track in yt_tracks:
            track = Track.from_dict(yt_track)
            track.playlist_title = self.title   
            self.tracks.append(track)

    @classmethod
    def init_playlists(cls):    
        yt_user = ytmusic.get_user(CHANNEL_ID)
        yt_playlists = ytmusic.get_user_playlists(CHANNEL_ID, yt_user["playlists"]["params"])

        for yt_playlist in yt_playlists:
            
            if yt_playlist["title"] not in IGNORED_PLAYLIST:
                new_playlist = cls(
                    title=yt_playlist["title"],
                    id=yt_playlist["playlistId"]
                )
                cls.playlists.append(new_playlist)

    @classmethod
    def export_as_csv(cls):
        with open("playlists.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["playlist", "title", "artists"])  # header

            for playlist in cls.playlists:
                for track in playlist.tracks:
                    writer.writerow([
                        playlist.title,
                        track.title,
                        ", ".join(track.artists)
                    ])

if __name__ == "__main__":
    Playlist.init_playlists()
    Playlist.export_as_csv()
    print(Playlist.playlists)
    