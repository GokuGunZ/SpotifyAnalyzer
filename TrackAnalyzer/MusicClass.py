import collections

class MusicClass():
    def __init__(self, jsonEntry):
        self.trackUri = jsonEntry["spotify_track_uri"].split(":")[2]
        self.trackName = jsonEntry["master_metadata_track_name"]
        self.artistName = jsonEntry["master_metadata_album_artist_name"]
        self.albumName = jsonEntry["master_metadata_album_album_name"]
        self.msPlayedList = [jsonEntry["ms_played"]]
        self.timestampList = [jsonEntry["ts"]]
        self.occurrencies = 1
        self.trackDoneCounter = 0
        if jsonEntry["reason_end"] == "trackdone" :
            self.trackDoneCounter = 1
        self.YearDictionary = collections.defaultdict(int)
        self.YearMonthDictionary = collections.defaultdict(int)
        self.YearDictionary[jsonEntry["ts"][:4]] = 1
        self.YearMonthDictionary[jsonEntry["ts"][:7]] = 1

    def update(self, jsonEntry):
        self.msPlayedList.append(jsonEntry["ms_played"])
        self.timestampList.append(jsonEntry["ts"])
        self.occurrencies+=1
        if jsonEntry["reason_end"] == "trackdone" :
            self.trackDoneCounter+=1
        self.YearDictionary[jsonEntry["ts"][:4]] += 1
        self.YearMonthDictionary[jsonEntry["ts"][:7]] += 1


    def __repr__(self) -> str:
        return f"Canzone: {self.trackName}, \n Artista: {self.artistName}, \n Album: {self.albumName}, \n riprodotta {self.occurrencies} volte, \n ascoltata per {sum(self.msPlayedList)/1000} secondi. \n"
    
    def __str__(self):
        return f"Canzone: {self.trackName}, \n Artista: {self.artistName}, \n Album: {self.albumName}, \n riprodotta {self.occurrencies} volte, \n ascoltata per {sum(self.msPlayedList)/1000} secondi. \n"