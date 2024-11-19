from kaggle.api.kaggle_api_extended import KaggleApi
import os
import pandas as pd
import streamlit as st

def download_datasets(kaggle_datasets_path):
    
    api = KaggleApi()
    api.authenticate()
    
    datasets = ["ludmin/billboard", "joebeachcapital/top-10000-spotify-songs-1960-now"]
    
    for d in datasets:
        api.dataset_download_files(d, path=kaggle_datasets_path, unzip=True)
    
    print(f"Dataset downloaded and extracted to {kaggle_datasets_path}")
    
    files_to_keep = {"hot100.csv", "top_10000_1960-now.csv"}
    
    for file_name in os.listdir(kaggle_datasets_path):
        file_path = os.path.join(kaggle_datasets_path, file_name)
        
        if os.path.isfile(file_path) and file_name not in files_to_keep:
            os.remove(file_path)
            print(f"Removed {file_path}")
        else:
            print(f"Kept {file_path}")

def merge_datasets(kaggle_datasets_path):
    
    hot_100_df = pd.read_csv(f'{kaggle_datasets_path}/hot100.csv')
    spotify_df = pd.read_csv(f'{kaggle_datasets_path}/top_10000_1960-now.csv')
    
    hot_100_rank_1 = hot_100_df[hot_100_df['Rank'] == 1]
    spotify_df.rename(columns={'Track Name': 'Song', 'Artist Name(s)': 'Artist'}, inplace=True)
    
    merged_df = hot_100_rank_1.merge(spotify_df, on=['Song', 'Artist'], how='inner')

    merged_df_path = 'datasets/hot_100_spotify_rank1.csv'
    merged_df.to_csv(merged_df_path, index=False)

    print(f"Saved dataset to {merged_df_path}")

def main():
    
    kaggle_datasets_path = 'datasets/kaggle'
    
    download_datasets(kaggle_datasets_path)
    merge_datasets(kaggle_datasets_path)

if __name__ == "__main__":
    main()