import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

class ETLPlots:

    def __init__(self, datasets_path):
        self._features_df_path = f'{datasets_path}/rank_1/features_scaled.csv'
        self._charts_df_path = f'{datasets_path}/rank_1/charts.csv'
        self._sentiment_df_path = f'{datasets_path}/rank_1/lyric_sentiment_scaled.csv'
        self._info_df_path = f'{datasets_path}/rank_1/track_info.csv'

    def all_plots(self):
        return [
            self.features_histogram(),
            self.features_changes_over_time(),
            self.sentiment_distribution_per_track(),
            self.sentiment_distribution_over_time()
        ]

    def features_histogram(self):
    
        features_df = pd.read_csv(self._features_df_path)
        
        float_cols = features_df.select_dtypes(include='float64').columns
        fig, ax = plt.subplots(figsize=(12, 6))
        
        features_df[float_cols].hist(ax=ax, bins=40, layout=(3, 5))
        
        plt.title('Features Distribution')
        plt.rcParams.update({'font.size': 10})
        plt.tight_layout()
        
        return fig
    
    def features_changes_over_time(self):
    
        features_df = pd.read_csv(self._features_df_path)
        charts_df = pd.read_csv(self._charts_df_path)
    
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
        
        sentiment_df = pd.read_csv(self._sentiment_df_path)
        info_df = pd.read_csv(self._info_df_path)
    
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
        sentiment_df = pd.read_csv(self._sentiment_df_path)
        charts_df = pd.read_csv(self._charts_df_path)
        
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
        
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
    
        ax.legend(title='Sentiments', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
    
        return fig
