"""
TODO plus tard: différence entre 2 playlists
TODO ne faire la comparaison que si 1 mot en commun dans l'artiste
"""
from IPython import embed
from ytmusicapi import YTMusic

ytmusic = YTMusic()

playlist = ytmusic.get_playlist("PL_OJFY7MJas144Ov2y9HRqQh00p5rXWUs", limit=99999)

tracks = playlist["tracks"]
print("Music count " + str(len(tracks)))

t = tracks[0]


############ TEST######
from playlist import Playlist
from track import Track

Playlist.init_playlists()

for playlist in Playlist.playlists:
    n = len(playlist.tracks)
    for i in range(n):
        for j in range(i + 1, n):
            a = playlist.tracks[i]
            b = playlist.tracks[j]
            # track1 = Track(playlist["tracks"][0])
            # track2 = Track(playlist["tracks"][1])
            # Track.is_duplicate(track1, track2)


# track1 = Track(playlist["tracks"][0])
# track2 = Track(playlist["tracks"][1])
# Track.is_duplicate(track1, track2)
exit()


###############

titles = []
for track in playlist["tracks"]:
    title = track["title"]
    words = title.split(" ")

    words = [
        word for word in words 
        if "200" not in word
        and "aster" not in word
        and "riginal" not in word
        and "-" not in word
        and len(word) > 2
    ]
    
    
    for title_word in titles:
        found = 0
        for word in words:
            # 
            if word in title_word:
                found = found + 1

                if found == 3:
                    # print(f"{word} in {title_word} ?")
                    # print(">>>>>>>>Find a dupliate between " + title + " and " + " ".join(title_word))
                    print(">>>>>>>>Find a dupliate between " + title )
                    print(">>>>>>>>Find a dupliate between " + " ".join(title_word))
                    print("")
                    # embed()
                    # exit()

    titles.append(words)
