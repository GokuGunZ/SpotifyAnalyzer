import collections



class AlbumClass():
    def __init__(self, jsonEntry):
        self.albumName = jsonEntry["master_metadata_album_album_name"]
        self.artistName = jsonEntry["master_metadata_album_artist_name"]
        self.trackDictionary = collections.defaultdict(int)
        self.trackDictionary[jsonEntry["master_metadata_track_name"]+"_"+jsonEntry["spotify_track_uri"].split(":")[2]] = 1
        self.occurrencies = 1
        self.trackDoneCounter = 0
        if jsonEntry["reason_end"] == "trackdone" :
            self.trackDoneCounter = 1
        self.msPlayedList = [jsonEntry["ms_played"]]
        self.YearDictionary = collections.defaultdict(int)
        self.YearMonthDictionary = collections.defaultdict(int)
        self.YearDictionary[jsonEntry["ts"][:4]] = 1
        self.YearMonthDictionary[jsonEntry["ts"][:7]] = 1

    def update(self, jsonEntry):
        self.msPlayedList.append(jsonEntry["ms_played"])
        self.trackDictionary[jsonEntry["master_metadata_track_name"]+"_"+jsonEntry["spotify_track_uri"].split(":")[2]] += 1
        self.occurrencies+=1
        if jsonEntry["reason_end"] == "trackdone" :
            self.trackDoneCounter+=1
        self.YearDictionary[jsonEntry["ts"][:4]] += 1
        self.YearMonthDictionary[jsonEntry["ts"][:7]] += 1

    def printSong(self, songDictionary):
        for song in self.trackDictionary.keys():
            print(songDictionary[song.split("_")[1]])      

        
    def __repr__(self):
        return f"Album: {self.albumName}, \n Artista: {self.artistName}, \n Canzoni: {self.trackDictionary.items()}, \n riprodotta {self.occurrencies} volte, \n ascoltata per {sum(self.msPlayedList)/1000} secondi. \n"
    
    def __str__(self):
        return f"Album: {self.albumName}, \n Artista: {self.artistName}, \n Canzoni: {self.trackDictionary.items()}, \n riprodotta {self.occurrencies} volte, \n ascoltata per {sum(self.msPlayedList)/1000} secondi. \n"