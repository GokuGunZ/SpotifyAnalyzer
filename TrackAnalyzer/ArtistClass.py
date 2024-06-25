import collections

class ArtistClass():
    def __init__(self, jsonEntry):
        self.artistName = jsonEntry["master_metadata_album_artist_name"]
        self.trackDictionary = collections.defaultdict(int)
        self.trackDictionary[jsonEntry["master_metadata_track_name"]+"_"+jsonEntry["spotify_track_uri"].split(":")[2]] = 1
        self.albumDictionary = collections.defaultdict(int)
        self.albumDictionary[jsonEntry["master_metadata_album_album_name"]] = 1
        self.occurrencies = 1
        self.trackDoneCounter = 0
        self.msPlayedList = [jsonEntry["ms_played"]]
        if jsonEntry["reason_end"] == "trackdone" :
            self.trackDoneCounter = 1
        self.YearDictionary = collections.defaultdict(int)
        self.YearMonthDictionary = collections.defaultdict(int)
        self.YearDictionary[jsonEntry["ts"][:4]] = 1
        self.YearMonthDictionary[jsonEntry["ts"][:7]] = 1

    def update(self, jsonEntry):
        self.msPlayedList.append(jsonEntry["ms_played"])
        self.trackDictionary[jsonEntry["master_metadata_track_name"]+"_"+jsonEntry["spotify_track_uri"].split(":")[2]] += 1
        self.albumDictionary[jsonEntry["master_metadata_album_album_name"]] +=1
        self.occurrencies+=1
        if jsonEntry["reason_end"] == "trackdone" :
            self.trackDoneCounter+=1
        self.YearDictionary[jsonEntry["ts"][:4]] += 1
        self.YearMonthDictionary[jsonEntry["ts"][:7]] += 1

    def __repr__(self):
        return f"Artista: {self.artistName}, \n Albums: {self.albumDictionary.items()}, \n riprodotta {self.occurrencies} volte, \n ascoltata per {sum(self.msPlayedList)/1000} secondi. \n"
    
    def __str__(self):
        return f"Artista: {self.artistName}, \n Albums: {self.albumDictionary.items()}, \n riprodotta {self.occurrencies} volte, \n ascoltata per {sum(self.msPlayedList)/1000} secondi. \n"
    

    def printAlbum(self, albumDictionary):
        for album in self.albumDictionary.keys():
            print(albumDictionary[album])    
    
    def printAlbumExtended(self, albumDictionary, songDictionary):
        for album in self.albumDictionary.keys():
            for song in albumDictionary[album].trackDictionary.keys():
                print(songDictionary[song.split("_")[1]])

    def getMostFrequentSongPerArtistList(self, artistDictionary): #Redefine for class ArtistCollection
        artistList = []
        for artistName, artistObj in artistDictionary.items():
            artistList.append([artistName, artistObj.occurrencies])
        artistList.sort(key= lambda x: -x[1])
        return artistList
    
    def getMostTimeSongPerArtistList(self, artistDictionary): #Redefine for class ArtistCollection
        artistList = []
        for artistName, artistObj in artistDictionary.items():
            artistList.append([artistName, (sum(artistObj.msPlayedList)/60)/60])
        artistList.sort(key= lambda x: -x[1])
        return artistList
    
    def printSongs(self, artistName, artistDictionary, musicDictionary):
        for song in artistDictionary[artistName].trackDictionary.keys():
            print(musicDictionary[song.split("_")[1]])