from IPython import embed
from dataclasses import dataclass, field
from typing import List, Dict

# TODO hérite de playlist pour avoi la class mère
@dataclass
class Track:
    title: str
    artists: List[str]  # list of artist names already in lowercase
    video_id: str = ""
    playlist_title: str = field(init=False) 

    @property
    def title_as_word(self) -> List[str]:
        """Renvoie la liste des mots du titre à la volée"""
        title = self.title

        # some exceptions
        EXCEPTIONS = [
            '(From "Saturday Night Fever" Soundtrack)',
            "Play & Win Radio Edit",
            "(Play & Win Radio Version)",
            "[Play & Win Radio Edit]",
            "(Radio Edit)",
            "(feat. Snoop Dogg)",
            "(feat. Kardinal Offishall)",
            "(feat. Daft Punk)",
            "| Sachafcb",
            "(feat. DJ Oriska)",
            "(Video Edit)",
            "(feat. Eden Martin)",
            "(feat. Mod Martin) ",
            "Theme - Ancient (Civilization 6 OST)",
        ]
        for exception in EXCEPTIONS:
            title = title.replace(exception, "")

        clean_words = []
        for word in title.split(" "):
            if word: # remove spaces
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
        video_id = track.get("videoId", "")
        return cls(title=title, artists=artists, video_id=video_id)

    @staticmethod
    def _is_legitimate_duplicate(track1, track2):
        # Known pairs that are false positives
        LEGITIMATE_PAIRS = [
            ("wati by night", "wati house"),
            ("pour que tu m'aimes encore", "destin"),
            ("bye bye (refugee camp band remix)", "bye bye (feat. imane d.)"),
            ("slipping away", "crier la vie"),
            ("le tourbillon", "tourbillon de la vie"),
            ("the way i are", "onerepublic remix"),
            ("Day 'N' Nite (Crookers Remix)", "Day 'N' Nite (Mobin Master Remix)"),
            ("Ça m'énerve 2020", "Ça m'énerve (Radio Edit)"),
            ("xxxx", "xxxxxxx"),
            ("xxxx", "xxxxxxx"),
            ("xxxx", "xxxxxxx"),
            ("xxxx", "xxxxxxx"),

        ]
        LEGITIMATE_PAIRS = [(p1.lower(), p2.lower()) for p1, p2 in LEGITIMATE_PAIRS]
        
        t1 = track1.title.lower()
        t2 = track2.title.lower()

        # Check if titles match exception pairs
        for p1, p2 in LEGITIMATE_PAIRS:
            if (p1 in t1 and p2 in t2) or (p2 in t1 and p1 in t2):
                return True
                
        return False
        
    @staticmethod
    def is_duplicate(track1, track2):
        # Ignore hardcoded legitimate pairs
        if Track._is_legitimate_duplicate(track1, track2):
            return False

        artist_match = False
        # first check if there is a match in artists
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
            "feat.", "&", "all", "i", "remix", "remaster", "-", "tu", "you", "are", "love"
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
                    print(f">>>>>>>>Find a duplicate between {track1.full_title}")
                    print(f"        🔗 https://www.youtube.com/watch?v={track1.video_id}")
                    print(f">>>>>>>>Find a duplicate between {track2.full_title}")
                    print(f"        🔗 https://www.youtube.com/watch?v={track2.video_id}")
                    # embed()

                    return True

        
        """ TODO LIST THE LEGITIMATE DUPLICATES
        >>>>>>>>Find a duplicate between RnB => The Way I Are (feat. Keri Hilson & D.O.E.) - timbaland
        >>>>>>>>Find a duplicate between RnB => The Way I Are (OneRepublic Remix Version) (feat. Keri Hilson & D.O.E.) - timbaland
        matching word = tourbillon
        >>>>>>>>Find a duplicate between Nostalgie => Le Tourbillon - vanessa paradis
        >>>>>>>>Find a duplicate between Nostalgie => Le tourbillon de la vie - vanessa paradis jeanne moreau

        >>>>>>>>Find a duplicate between Divers 2025 => Slipping Away - moby
>>>>>>>>Find a duplicate between Divers 2025 => Slipping Away (Crier la Vie) (feat. Mylène Farmer) - moby


>>>>>>>>Find a duplicate between RFM => Bye Bye (Refugee Camp Band Remix) - ménélik
>>>>>>>>Find a duplicate between RFM => Bye Bye (feat. Imane D.) - ménélik
=> Pour que tu m'aimes encore (Live à Paris 1995) - céline dion
        🔗 https://www.youtube.com/watch?v=npcjJqJDMVw
>>>>>>>>Find a duplicate between Live => Destin (Live à Paris 1995) - céline dion
        🔗 https://www.youtube.com/watch?v=5kiQFjL2Ckw

matching word = wati
>>>>>>>>Find a duplicate between RAP FR => Wati by Night - sexion d'assaut
        🔗 https://www.youtube.com/watch?v=JVh7ISjF70M
>>>>>>>>Find a duplicate between RAP FR => Wati House - sexion d'assaut
        """
