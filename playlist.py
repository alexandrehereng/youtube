
from dataclasses import dataclass, field
from typing import List
from ytmusicapi import YTMusic
from IPython import embed
from track import Track

ytmusic = YTMusic()

# @alexandre.hereng I found this ID in yt playlist object.
CHANNEL_ID = "UCDBKxTSxmFK_JzRY7_y3E1Q" 

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
            self.tracks.append(track)

    @classmethod
    def init_playlists(cls):    
        yt_user = ytmusic.get_user(CHANNEL_ID)
        yt_playlists = ytmusic.get_user_playlists(CHANNEL_ID, yt_user["playlists"]["params"])

        yt_playlists = [yt_playlists[1]]
        for yt_playlist in yt_playlists:

            new_playlist = cls(
                title=yt_playlist["title"],
                id=yt_playlist["playlistId"]
            )
            cls.playlists.append(new_playlist)

if __name__ == "__main__":
    Playlist.init_playlists()
    print(Playlist.playlists)
    