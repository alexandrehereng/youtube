from playlist import Playlist
from track import Track


Playlist.init_playlists()

all_tracks = []
for playlist in Playlist.playlists:
    all_tracks.extend(playlist.tracks)

# compare every tracks
n = len(all_tracks)
for i in range(n):
    for j in range(i + 1, n):
        track1 = all_tracks[i]
        track2 = all_tracks[j]

        Track.is_duplicate(track1, track2)

