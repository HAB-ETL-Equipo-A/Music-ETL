from kaggle.api.kaggle_api_extended import KaggleApi
import os
import config

def download_datasets():
    
    api = KaggleApi()
    api.authenticate()
    
    folder_path = config.kaggle_datasets_path
    
    datasets = ["ludmin/billboard", "joebeachcapital/top-10000-spotify-songs-1960-now"]
    
    for d in datasets:
        api.dataset_download_files(d, path=folder_path, unzip=True)
    
    print(f"Dataset downloaded and extracted to {folder_path}")
    
    files_to_keep = {"hot100.csv", "top_10000_1960-now.csv"}
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path) and file_name not in files_to_keep:
            os.remove(file_path)
            print(f"Removed {file_path}")
        else:
            print(f"Kept {file_path}")

def main():
    download_datasets()

if __name__ == "__main__":
    main()