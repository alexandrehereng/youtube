from IPython import embed
from dataclasses import dataclass, field
from typing import List, Dict
import csv
import os


@dataclass
class Track:
    title: str
    artists: List[str]  # liste des noms d'artistes déjà en minuscules
    video_id: str = ""
    playlist_title: str = field(init=False) 

    @property
    def title_as_word(self) -> List[str]:
        """Renvoie la liste des mots du titre à la volée"""
        title = self.title

        # quelques exceptions
        EXCEPTIONS = [
            '(From "Saturday Night Fever" Soundtrack)',
            "Play & Win Radio Edit",
            "(Play & Win Radio Version)",
            "[Play & Win Radio Edit]",
            "(Radio Edit)",
            "(feat. Snoop Dogg)",
            "(feat. Kardinal Offishall)",
            "(feat. Daft Punk)",
            "(feat. DJ Oriska)",
            "(Video Edit)",
            "(feat. Eden Martin)",
            "(feat. Mod Martin)",
            "Theme - Ancient (Civilization 6 OST)",
            "(feat. Pharrell Williams)",
            "(feat. Norma Jean Martine)",
        ]
        for exception in EXCEPTIONS:
            title = title.replace(exception, "")

        clean_words = []
        for word in title.split(" "):
            if word: # supprime les espaces
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
        csv_path = os.path.join(os.path.dirname(__file__), "legitimate_duplicates.csv")
        
        legitimate_pairs = []
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        legitimate_pairs.append((row[0].lower(), row[1].lower()))
        
        t1 = track1.title.lower()
        t2 = track2.title.lower()

        # Vérifie si les titres correspondent aux paires d'exceptions
        for p1, p2 in legitimate_pairs:
            if (p1 in t1 and p2 in t2) or (p2 in t1 and p1 in t2):
                return True
                
        return False
        
    @staticmethod
    def is_duplicate(track1, track2):
        IGNORED_ARTISTS = ["sachafcb"]
        
        for artist in track1.artists + track2.artists:
            for ignored in IGNORED_ARTISTS:
                if ignored in artist:
                    return False

        # Ignore les paires légitimes enregistrées
        if Track._is_legitimate_duplicate(track1, track2):
            return False

        artist_match = False
        # vérifie d'abord s'il y a une correspondance dans les artistes
        for artist1 in track1.artists:
            for artist2 in track2.artists:
                if artist1 == artist2:
                    artist_match = True
                    break

            if artist_match:
                break
        
        if not artist_match:
            return False

        # puis compare les mots dans le morceau
        WORDS_TO_IGNORE = [
            "remasterisé", "remastered", "à", "a", "en", "pt.", "ne", "toi", "et", "que", "les",
            "le", "la", "of", "the", "in", "de", "il", "elle", "mon", "vie", "je", "version", "tous",
            "feat.", "&", "all", "i", "remix", "remaster", "-", "tu", "you", "are", "love", "radio", "mix"
        ]
        YEARS = [str(year) for year in range(1940, 2031)]
        NUMBERS = [str(number) for number in range(1, 200)]
        WORDS_TO_IGNORE.extend(YEARS)
        WORDS_TO_IGNORE.extend(NUMBERS)
        
        count_match = 0
        for word1 in track1.title_as_word:
            for word2 in track2.title_as_word:

                # ignore les mots courants
                if word1 in WORDS_TO_IGNORE or word2 in WORDS_TO_IGNORE:
                    continue
                
                if word1 == word2:
                    count_match = count_match + 1

                if (
                    count_match == 2 # au moins 2 mots en commun
                    # ou 1 pour les petits titres
                    or (count_match == 1 and ( len(track1.title_as_word) < 3 or len(track2.title_as_word) < 3))
                ):
                    print("")
                    print(f"matching word = {word1}")
                    print(f">>>>>>>>Find a duplicate between {track1.full_title}")
                    print(f"        🔗 https://www.youtube.com/watch?v={track1.video_id}")
                    print(f">>>>>>>>Find a duplicate between {track2.full_title}")
                    print(f"        🔗 https://www.youtube.com/watch?v={track2.video_id}")
                    # embed()

                    csv_path = os.path.join(os.path.dirname(__file__), "legitimate_duplicates.csv")
                    choice = ""
                    while choice not in ['Y', 'N']:
                        choice = input("Doublon légitime ? (Y pour enregistrer dans le CSV, N pour ignorer) : ").strip().upper()
                        
                    if choice == 'Y':
                        with open(csv_path, "a", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow([track1.title, track2.title])
                        # On retourne False car ce n'est plus un vrai doublon (assumé légitime)
                        return False

                    return True
