import webbrowser
import requests
import json
import os
from urllib.parse import urlencode, urlparse, parse_qs
from datetime import datetime, timedelta

def main():
    pass

def setup_connection(user):
    folderPath = "./TrackAnalyzer/Dataset/"+user+"/tmp/"
    global urlBase
    urlBase = "https://api.spotify.com/v1/"
    global username
    username = None
    global headers
    token_info = {"user":user}

    if not os.path.exists(folderPath+"credentials.json"):
        with open(folderPath+"credentials.json", "w") as file:
            json.dump(token_info, file)
    
    with open(folderPath+"credentials.json", "r") as file:
        token_info = json.load(file)
    expiration_time = datetime.strptime(token_info.get('expires_at'), '%Y-%m-%d %H:%M:%S.%f') if 'expires_at' in token_info else datetime.now()
    if "username" in token_info:
        username = token_info["username"]
    if datetime.now() < expiration_time:
        headers = {"Content-Type": "application/json", 'Authorization': 'Bearer '+token_info['access_token']}
        return
    else:
        client_id = "7aa97f34d8594ce0bd8ffb7ae4e1bfd1"
        scope = "playlist-modify-public user-read-private user-read-email"
        redirect_uri = "https://localhost"
        client_secret = "b5740aa828b8416d9ce0108951ed3246"

        auth_url = 'https://accounts.spotify.com/authorize'
        params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': scope
        }
        auth_url_with_params = f"{auth_url}?{urlencode(params)}"

        # Apri il browser per l'autenticazione
        webbrowser.open(auth_url_with_params)

        # Qui il codice si ferma e aspetta che tu inserisca manualmente il 'code' ottenuto
        # dopo l'autenticazione e la redirezione all'URL specificato.

        # Una volta ottenuto il 'code', puoi usarlo per richiedere l'access token
        authorization_code = input("Inserisci il codice di autorizzazione: ")
        parsed_url = urlparse(authorization_code)
        query_params = parse_qs(parsed_url.query)

        # Estrai il codice di autorizzazione
        authorization_code = query_params.get('code', [None])[0]

        # Parametri per la richiesta del token
        token_url = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        # Fai la richiesta POST per ottenere l'access token
        response = requests.post(token_url, data=payload)
        token_info = response.json()
        expires_at = datetime.now() + timedelta(seconds=token_info['expires_in'])
        token_info['expires_at'] = expires_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        headers = {"Content-Type": "application/json", 'Authorization': 'Bearer '+token_info['access_token']}
        if username is None:
            username = getUsername()
            token_info['username'] = username
        with open(folderPath+"credentials.json", "w") as file:
            json.dump(token_info, file)
        print(token_info)
        return

def getUsername():
    url = urlBase+"me"
    response = requests.get(url, headers=headers)
    return response.json()['id']

def getTracksInfos(tracksId):
    if len(tracksId) > 100:
        for x in range(0, len(tracksId), 100):
            idList = ",".join(tracksId[x:x+100])
            url = urlBase+"audio-features?ids="+idList
            response = requests.get(url, headers=headers)
    

def createPlaylist(name, description):
    url = urlBase+"users/"+username+"/playlists"
    body = {'name': name, 'description': description, 'public': 'false'}
    response = requests.post(url, json=body, headers=headers)
    print(response.json())
    return response.json()['id']

def add_items_to_playlist(playlist_id, tracks):
    url = urlBase+"playlists/"+playlist_id+"/tracks"
    body = {'uris': tracks}
    response = requests.post(url, json=body, headers=headers)
    print(response.json())
    return response.text
  

if __name__=="__main__":
    main()
  
