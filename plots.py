import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

def features_histogram():

    features_df = pd.read_csv('datasets/rank_1/features_scaled.csv')
    
    float_cols = features_df.select_dtypes(include='float64').columns
    fig, ax = plt.subplots(figsize=(12, 6))
    
    features_df[float_cols].hist(ax=ax, bins=40, layout=(3, 5))
    
    plt.rcParams.update({'font.size': 10})
    plt.tight_layout()
    
    return fig

def features_changes_over_time():

    features_df = pd.read_csv('datasets/rank_1/features_scaled.csv')
    charts_df = pd.read_csv('datasets/rank_1/charts.csv')

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