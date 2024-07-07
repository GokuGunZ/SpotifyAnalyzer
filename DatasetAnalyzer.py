import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os
import apiCall
import json


def main():
    global user
    user = "Pit"

    df = loadData(user)
    apiCall.setup_connection(user)

    # Canzoni
    songs = df[['spotify_track_uri', 'master_metadata_track_name','master_metadata_album_album_name', 'master_metadata_album_artist_name']].drop_duplicates().reset_index(drop=True)

    # Artisti
    artists = df[['master_metadata_album_artist_name']].drop_duplicates().reset_index(drop=True)

    # Album
    albums = df[['master_metadata_album_album_name', 'master_metadata_album_artist_name']].drop_duplicates().reset_index(drop=True)

    # Aggiungi chiavi per artisti e album nel DataFrame principale
    df = df.merge(songs, on=['spotify_track_uri', 'master_metadata_track_name', 'master_metadata_album_album_name', 'master_metadata_album_artist_name'], how='left')
    df = df.merge(artists, on='master_metadata_album_artist_name', how='left')
    df = df.merge(albums, on=['master_metadata_album_album_name', 'master_metadata_album_artist_name'], how='left')
    
    # Estrai mese e anno dai timestamp
    df['month'] = df['ts'].dt.month
    df['year'] = df['ts'].dt.year

    df['year_month'] = df['ts'].dt.to_period('M')

    songUris = songs["spotify_track_uri"].apply(lambda x: str(x).split(":")[-1])
    #apiCall.getTracksInfos(list(songUris))

def createMonthlyPlaylists(df):
    
    # Canzoni
    songs = df[['spotify_track_uri', 'master_metadata_track_name','master_metadata_album_album_name', 'master_metadata_album_artist_name']].drop_duplicates().reset_index(drop=True)

    # Artisti
    artists = df[['master_metadata_album_artist_name']].drop_duplicates().reset_index(drop=True)

    # Album
    albums = df[['master_metadata_album_album_name', 'master_metadata_album_artist_name']].drop_duplicates().reset_index(drop=True)

    # Aggiungi chiavi per artisti e album nel DataFrame principale
    df = df.merge(songs, on=['spotify_track_uri', 'master_metadata_track_name', 'master_metadata_album_album_name', 'master_metadata_album_artist_name'], how='left')
    df = df.merge(artists, on='master_metadata_album_artist_name', how='left')
    df = df.merge(albums, on=['master_metadata_album_album_name', 'master_metadata_album_artist_name'], how='left')
    
    # Estrai mese e anno dai timestamp
    df['month'] = df['ts'].dt.month
    df['year'] = df['ts'].dt.year

    df['year_month'] = df['ts'].dt.to_period('M')

    monthlyPlayedSongs = df.groupby(['year_month', 'spotify_track_uri'])['ms_played'].agg(['sum','count']).reset_index()
    monthlyPlayedSongs.columns = ['year_month', 'spotify_track_uri', 'total_mins_played', 'played_count']
    monthlyPlayedSongs['total_mins_played'] = monthlyPlayedSongs['total_mins_played']/60000
    monthlyPlayedSongs = monthlyPlayedSongs.sort_values(by=['year_month', 'total_mins_played'], ascending=[True, False])

    apiCall.setup_connection(user)

    infos = []
    lens = []
    for period in monthlyPlayedSongs['year_month'].unique():
        period_df = monthlyPlayedSongs[monthlyPlayedSongs['year_month'] == period]
        period_df.columns = ['year_month', 'spotify_track_uri', 'total_mins_played', 'played_count']
        period_df = period_df[period_df['played_count'] >= 3]
        #period_df = period_df[period_df['total_mins_played'] > 10] 
        threshold = period_df['total_mins_played'].quantile(60/100.00)
        period_df = period_df[period_df['total_mins_played'] >= threshold]
        period_df = period_df.merge(songs, on="spotify_track_uri", how="left")
        if len(period_df) > 100:
            period_df = period_df[:100]
        uris = []
        description = []
        for index, row in period_df.iterrows():
            uris.append(row['spotify_track_uri'])
            description.append(row['master_metadata_track_name']+f" - {row['master_metadata_album_artist_name']} -- mins: {round(row['total_mins_played'],0)}")
        description = "----".join(description)
        playlist_id = apiCall.createPlaylist(period.strftime('%m-%Y'), description[:500])
        apiCall.add_items_to_playlist(playlist_id, uris)

def getListeningSession(df):
    df = df.sort_values(by='ts')
    df['prev_ts'] = df['ts'].shift(1)
    df['time_diff'] = (df['ts'] - df['prev_ts']).dt.total_seconds() / 60
    df['new_session'] = df['time_diff'] > 30

    # Assegnare un ID di sessione incrementale
    df['session_id'] = df['new_session'].cumsum()

    # Analisi delle sessioni
    session_stats = df.groupby('session_id').agg({
        'ts': ['min', 'max'],
        'ms_played': 'sum',
        'master_metadata_track_name': 'count'
    }).reset_index()

    # Rinomina le colonne
    session_stats.columns = ['session_id', 'start_time', 'end_time', 'total_ms_played', 'tracks_played']
    session_stats['total_min_played'] = session_stats['total_ms_played']/60000
    session_stats = session_stats.sort_values(by='total_ms_played', ascending=False)

    print(session_stats.head())
    return session_stats

def loadData(userFolderName):
    # Carica il file JSON
    all_data = []
    directory_Path = "./TrackAnalyzer/Dataset/" + userFolderName
    for jsonPath in os.listdir(directory_Path):
        if jsonPath.endswith(".json"): 
            if "Audio" in jsonPath.split("_"):
                with open(directory_Path+"/"+jsonPath, encoding="utf-8") as file:
                    data = json.load(file)
                    all_data.extend(data) 
                    

    # Crea il DataFrame
    df = pd.DataFrame(all_data)

    df['ts'] = pd.to_datetime(df['ts'])
    df['ms_played'] = df['ms_played'].astype(int)
    df['shuffle'] = df['shuffle'].astype(bool)
    df['offline'] = df['offline'].astype(bool)
    df['incognito_mode'] = df['incognito_mode'].astype(bool)

    ## Filter None values
    df = df[df['spotify_track_uri'] != None]
    ## Filtering short listens
    df = df[df['ms_played'] > 30000]
    return df

def printMonthlyAcrossYears(df):
    # Query di base: Numero di canzoni ascoltate per mese e anno
    monthly_listens = df.groupby(['year', 'month']).size().reset_index(name='count')

    # Creare il plot
    plt.figure(figsize=(12, 6))
    palette = sns.color_palette("husl", monthly_listens['year'].nunique())  # Colori distinti per ogni anno

    # Sovrapporre i dati di anni diversi
    for i, year in enumerate(monthly_listens['year'].unique()):
        yearly_data = monthly_listens[monthly_listens['year'] == year]
        plt.bar(yearly_data['month'] + i*0.1, yearly_data['count'], width=0.1, label=year, color=palette[i], alpha=0.6)

    plt.xlabel('Month')
    plt.ylabel('Number of Songs')
    plt.title('Number of Songs Listened Per Month Across Different Years')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Year')
    plt.show()

def printDurationDistribution(df):    
    plt.figure(figsize=(12, 6))
    plt.hist(df['ms_played'] / 1000, bins=500, color='blue', alpha=0.7)
    plt.xlabel('Seconds Played')
    plt.ylabel('Frequency')
    plt.title('Distribution of Listening Duration')
    plt.show()

def plotMonthlyGridHistogram(df):
    
    df['year_month'] = df['ts'].dt.to_period('M')

    monthlyPlayedSongs = df.groupby(['year_month', 'spotify_track_uri'])['ms_played'].agg(['sum','count']).reset_index()
    monthlyPlayedSongs.columns = ['year_month', 'spotify_track_uri', 'total_mins_played', 'played_count']
    monthlyPlayedSongs['total_mins_played'] = monthlyPlayedSongs['total_mins_played']/60000
    monthlyPlayedSongs = monthlyPlayedSongs.sort_values(by=['year_month', 'total_mins_played'], ascending=[True, False])

    monthlyPlayedSongs['year'] = monthlyPlayedSongs['year_month'].dt.year
    
    years = monthlyPlayedSongs['year'].unique()

    for year in years:
        yearData = monthlyPlayedSongs[monthlyPlayedSongs['year'] == year]
        fig, axs = plt.subplots(4, 3, figsize=(20,15))
        fig.suptitle(f'Distributions for Year {year}', fontsize=20)

        
        months = yearData['year_month'].unique()
        for i, month in enumerate(months):
            # Seleziona i dati per il mese corrente
            month_data = yearData[yearData['year_month'] == month]
            
            # Determina la posizione del subplot
            row = i // 3
            col = i % 3
            
            # Istogramma
            axs[row, col].hist(month_data['total_mins_played'], bins=300, alpha=0.7)
            axs[row, col].set_title(f'Histogram for {month}')
            axs[row, col].set_xlabel('Total Minutes Played', fontsize=8)
            axs[row, col].set_ylabel('Frequency')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()


if __name__ == "__main__":
    main()