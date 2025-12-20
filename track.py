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
        title = self.title

        # some exceptions
        EXCEPTIONS = [
            '(From "Saturday Night Fever" Soundtrack)'
            "Play & Win Radio Edit"
            "(Radio Edit)",
            "(feat. Snoop Dogg)",
            "(feat. Kardinal Offishall)",
        ]
        for exception in EXCEPTIONS:
            title = title.replace(exception, "")

        clean_words = []
        for word in title.split(" "):
            clean_word = word.lower()
            clean_word = clean_word.replace("(", "")
            clean_word = clean_word.replace(")", "")
            clean_words.append(clean_word)


        return clean_words

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

        WORDS_TO_IGNORE = [
            "remasterisé", "remastered", "à", "a", "en", "pt.", "ne", "toi", "et", "que", "les",
            "le", "la", "of", "the", "in", "de", "il", "elle", "mon", "vie", "je", "version", "tous",
            "feat.", "&", "all", "i", "remix", "remaster"
        ]
        YEARS = [str(year) for year in range(1940, 2031)]
        NUMBERS = [str(number) for number in range(1, 200)]
        WORDS_TO_IGNORE.extend(YEARS)
        WORDS_TO_IGNORE.extend(NUMBERS)
        
        count_match = 0
        for word1 in track1.title_as_word:
            for word2 in track2.title_as_word:

                # skip common words
                if word1 in WORDS_TO_IGNORE or word2 in WORDS_TO_IGNORE:
                    continue

                
                if word1 == word2:
                    count_match = count_match + 1

                if (
                    count_match == 2 # at least 2 words in common
                # or 1 for the small titles
                    or (count_match == 1 and ( len(track1.title_as_word) < 3 or len(track2.title_as_word) < 3))
                ):
                    print("")
                    print(f"matching word = {word1}")
                    print(">>>>>>>>Find a duplicate between " + track1.full_title)
                    print(">>>>>>>>Find a duplicate between " + track2.full_title)
                    # embed()

                    return True

        
        """ TODO LIST THE LEGITIMATE DUPLICATES
        >>>>>>>>Find a duplicate between RnB => The Way I Are (feat. Keri Hilson & D.O.E.) - timbaland
        >>>>>>>>Find a duplicate between RnB => The Way I Are (OneRepublic Remix Version) (feat. Keri Hilson & D.O.E.) - timbaland
        matching word = tourbillon
        >>>>>>>>Find a duplicate between Nostalgie => Le Tourbillon - vanessa paradis
        >>>>>>>>Find a duplicate between Nostalgie => Le tourbillon de la vie - vanessa paradis jeanne moreau
        """
