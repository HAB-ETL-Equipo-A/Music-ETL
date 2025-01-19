import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import seaborn as sns
import os
import json
from airtable_api import AirtableAPI

class ETLPlots:

    def __init__(self):
        
        class_dir = os.path.dirname(os.path.abspath(__file__))
        secrets_file_path = os.path.join(class_dir, 'secrets.json')
        
        with open(secrets_file_path, 'r') as f:
            secrets = json.load(f)
            access_token = secrets['AIRTABLE_ACCESS_TOKEN']
            app_id = secrets['AIRTABLE_APP_ID']

        self.api = AirtableAPI(app_id, access_token)

        self.features_scaled_json = self.api.get_table_data('features_scaled')
        self.charts_json = self.api.get_table_data('charts')
        self.lyric_sentiment_json = self.api.get_table_data('lyric_sentiment_scaled')
        self.track_info_json = self.api.get_table_data('track_info')
        self.binary_classification_json = self.api.get_table_data('binary_classifications')

    def all_plots(self):
        return [
            self.features_histogram(),
            self.features_changes_over_time(),
            self.sentiment_distribution_per_track(),
            self.sentiment_distribution_over_time(),
            self.binary_classification(),
            self.key_classification(),
            self.mode_classification()
        ]

    def features_histogram(self):
        
        features_df = pd.DataFrame(self.features_scaled_json)
        
        float_cols = features_df.select_dtypes(include='float64').columns
        fig, ax = plt.subplots(figsize=(12, 6))
        
        features_df[float_cols].hist(ax=ax, bins=40, layout=(3, 5))
        
        plt.title('Features Distribution')
        plt.rcParams.update({'font.size': 10})
        plt.tight_layout()
        
        return fig
    
    def features_changes_over_time(self):
    
        features_df = pd.DataFrame(self.features_scaled_json)
        charts_df = pd.DataFrame(self.charts_json)
    
        charts_df_first = charts_df.drop_duplicates(subset='Track ID', keep='first')
        merged_df = pd.merge(charts_df_first, features_df, left_on='Track ID', right_on='track_id')
        
        merged_df['Date'] = pd.to_datetime(merged_df['Date'], errors='coerce')
        
        merged_df.set_index('Date', inplace=True)
        
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab20.colors)
        
        features_to_plot = [
            'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence', 'tempo', 'tempo_confidence', 
            'time_signature_confidence', 'key_confidence', 'mode_confidence'
        ]
        
        fig = plt.figure(figsize=(12, 8))
        
        for feature in features_to_plot:
            x = (merged_df.index - merged_df.index[0]).days
            y = merged_df[feature]
            
            p = np.poly1d(np.polyfit(x, y, 3))
            plt.plot(merged_df.index, p(x), label=feature, linewidth=2)
        
        plt.title('Features Trendlines Over Time')
        plt.xlabel('Date')
        plt.ylabel('Feature Value')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
        
        plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
    
        return fig

    def sentiment_distribution_per_track(self):
        
        sentiment_df = pd.DataFrame(self.lyric_sentiment_json)
        info_df = pd.DataFrame(self.track_info_json)
    
        song_names = info_df.set_index('track_id').loc[sentiment_df['track_id'], 'track_name'].tolist()
    
        df = sentiment_df.copy()
        df = df.drop(columns=['track_id'])
    
        fig, ax = plt.subplots(figsize=(8, 6))
        
        df.plot(kind='bar', stacked=True, ax=ax)
    
        ax.set_title('Sentiment Distribution per Track')
        ax.set_xlabel('Tracks')
        ax.set_ylabel('Sentiment Levels')
        ax.set_xticks(range(len(song_names)))
        ax.set_xticklabels(song_names, rotation=90, ha='right')
        ax.legend(title='Sentiments', bbox_to_anchor=(1.05, 1), loc='upper left')
    
        plt.tight_layout()
        
        return fig

    def sentiment_distribution_over_time(self):
        
        sentiment_df = pd.DataFrame(self.lyric_sentiment_json)
        charts_df = pd.DataFrame(self.charts_json)
        
        charts_df.rename(columns={'Track ID': 'track_id'}, inplace=True)
        merged_df = pd.merge(sentiment_df, charts_df, on='track_id')
        
        merged_df['date'] = pd.to_datetime(merged_df['Date'])
        merged_df['month_year'] = merged_df['date'].dt.strftime('%m-%Y')
        merged_df = merged_df.sort_values(by='date')
        merged_df.set_index('month_year', inplace=True)
        
        merged_df.drop(columns=['track_id', 'date'], inplace=True)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        merged_df.plot(kind='bar', stacked=True, ax=ax)
    
        ax.set_title('Sentiment Distribution Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sentiment Levels')
        labels = ax.get_xticklabels()

        tick_positions = ax.get_xticks()
        
        ax.set_xticks(tick_positions[::2])
        ax.set_xticklabels(labels[::2], rotation=90, ha='right')
    
        ax.legend(title='Sentiments', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
    
        return fig

    def binary_classification(self):
        
        plot_df = pd.DataFrame(self.binary_classification_json)

        plot_df['Date'] = pd.to_datetime(plot_df['Date'])
        
        fig = plt.figure(figsize=(14, 3))
        labels = plot_df.columns[1:].tolist()
        
        explicit_occurrences = plot_df[plot_df['Explicit'] == 1]
        plt.scatter(explicit_occurrences['Date'], [0.8] * len(explicit_occurrences), label=labels[0], color='red')
        
        minor_occurrences = plot_df[plot_df['Minor Key'] == 1]
        plt.scatter(minor_occurrences['Date'], [1.0] * len(minor_occurrences), label=labels[1], color='blue')
        
        _34_occurrences = plot_df[plot_df['3/4 Time Signature'] == 1]
        plt.scatter(_34_occurrences['Date'], [1.2] * len(_34_occurrences), label=labels[2], color='green')
        
        plt.title('Occurences Over Time')
        
        plt.xticks(rotation=0)
        plt.yticks([0.8, 1, 1.2], labels)
        plt.ylim(0.5, 1.5)

        plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
        
        plt.tight_layout()
        
        return fig

    def key_classification(self):
        
        songs_data = pd.DataFrame(self.track_info_json)

        sns.set(style="whitegrid")
        
        fig = plt.figure(figsize=(10, 6))
        sns.kdeplot(data=songs_data, x="key", fill=True, color="red", alpha=0.5)
        
        plt.title("Distribución de las tonalidades (key) de canciones Top 1", fontsize=16)
        plt.xlabel("Tonalidad (key)", fontsize=12)
        plt.ylabel("Densidad", fontsize=12)
        plt.xticks(range(12), ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
        
        return fig

    def mode_classification(self):
        songs_data = pd.DataFrame(self.track_info_json)
        songs_data['mode'] = songs_data['mode'].apply(lambda x: 0 if x == 'Minor' else 1)
        
        fig = plt.figure(figsize=(10, 6))
        sns.kdeplot(data=songs_data, x="mode", fill=True, color="salmon", alpha=0.5)
        plt.title("Distribución de modos (Mayor/menor) en canciones Top 1", fontsize=16)
        plt.xlabel("Modo (0 = Menor, 1 = Mayor)", fontsize=12)
        plt.ylabel("Densidad", fontsize=12)
        plt.xticks([0, 1], ["Menor", "Mayor"])
        return fig
