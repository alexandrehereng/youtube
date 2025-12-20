from IPython import embed
from dataclasses import dataclass, field
from typing import List, Dict

# TODO hérite de playlist pour avoi la class mère
@dataclass
class Track:
    title: str
    artists: List[str]  # list of artist names already in lowercase
    playlist_title: str = field(init=False) 

    @property
    def title_as_word(self) -> List[str]:
        """Renvoie la liste des mots du titre à la volée"""
        return self.title.split(" ")

    @property
    def full_title(self) -> str:
        return f"{self.playlist_title} => {self.title} - " + " ".join(self.artists)

    @classmethod
    def from_dict(cls, track: Dict):
        """Constructeur alternatif depuis un dictionnaire"""
        title = track["title"]
        artists = [artist["name"].lower() for artist in track["artists"]]
        return cls(title=title, artists=artists)

    def is_duplicate(track1, track2):

        artist_match = False
        # TODO compare artist word by word
        # return false if no match in artist
        for artist1 in track1.artists:
            for artist2 in track2.artists:
                if artist1 == artist2:
                    artist_match = True
                    break

            if artist_match:
                break
        
        if not artist_match:
            return False

        # then compare words in song

        for word1 in track1.title_as_word:
            for word2 in track2.title_as_word:
                if word1 == word2:
                    print("")
                    print(">>>>>>>>Find a duplicate between " + track1.full_title)
                    print(">>>>>>>>Find a duplicate between " + track2.full_title)
                    embed()
                    return True
