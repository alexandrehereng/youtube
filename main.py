from playlist import Playlist
from track import Track

Playlist.init_playlists()

for playlist in Playlist.playlists:
    n = len(playlist.tracks)
    for i in range(n):
        for j in range(i + 1, n):
            track1 = playlist.tracks[i]
            track2 = playlist.tracks[j]

            Track.is_duplicate(track1, track2)
