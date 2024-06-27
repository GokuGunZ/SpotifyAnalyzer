import webbrowser
import requests
import json
from urllib.parse import urlencode, urlparse, parse_qs

def main():
    pass

def setup_connection():
    global urlBase
    urlBase = "https://api.spotify.com/v1/"
    global username
    global headers
    


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
    headers = {"Content-Type": "application/json", 'Authorization': 'Bearer '+token_info['access_token']}
    username = getUsername()
    
    return

def getUsername():
    url = urlBase+"me"
    response = requests.get(url, headers=headers)
    return response.json()['id']

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
  
