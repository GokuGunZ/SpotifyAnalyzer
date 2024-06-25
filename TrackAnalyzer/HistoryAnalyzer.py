import json
import collections
import os
from MusicClass import MusicClass
from ArtistClass import ArtistClass
from AlbumClass import AlbumClass

jsonPath = "Streaming_History_Audio_2019-2020_0.json"
jsonData = json.loads(open(jsonPath, encoding="utf-8").read())

myMusic = collections.defaultdict(object)
myArtist = collections.defaultdict(object)
myAlbum = collections.defaultdict(object)
dailyTime = collections.defaultdict(int)

def initializeAllFile(myMusic, myArtist, myAlbum, dailyTime):
    for jsonPath in os.listdir("."):
        if jsonPath.endswith(".json"):          
            jsonData = json.loads(open(jsonPath, encoding="utf-8").read())      
            for jsonEntry in jsonData:
                if jsonEntry["spotify_track_uri"] == None: continue
                if jsonEntry["ms_played"] < 15000: continue

                dailyTime[jsonEntry["ts"][:10]] += jsonEntry["ms_played"]

                if jsonEntry["spotify_track_uri"].split(":")[2] not in myMusic:
                    myMusic[jsonEntry["spotify_track_uri"].split(":")[2]] = MusicClass(jsonEntry)
                else:
                    myMusic[jsonEntry["spotify_track_uri"].split(":")[2]].update(jsonEntry)

                if jsonEntry["master_metadata_album_artist_name"] not in myArtist:
                    myArtist[jsonEntry["master_metadata_album_artist_name"]] = ArtistClass(jsonEntry)
                else:
                    myArtist[jsonEntry["master_metadata_album_artist_name"]].update(jsonEntry)

                if jsonEntry["master_metadata_album_album_name"] not in myAlbum:
                    myAlbum[jsonEntry["master_metadata_album_album_name"]] = AlbumClass(jsonEntry)
                else:
                    myAlbum[jsonEntry["master_metadata_album_album_name"]].update(jsonEntry)
    

initializeAllFile(myMusic, myArtist, myAlbum, dailyTime)

artistList = ArtistClass.getMostTimeSongPerArtistList(ArtistClass, myArtist)
for artist in artistList[:20]:
    print(artist)
    
"""
myArtist["Dani Faiv"].printAlbum(myAlbum)
myArtist["Dani Faiv"].printAlbumExtended(myAlbum, myMusic)
myAlbum["The Waiter"].printSong(myMusic)

artistList = ArtistClass.getSortedArtistList(myArtist)
"""