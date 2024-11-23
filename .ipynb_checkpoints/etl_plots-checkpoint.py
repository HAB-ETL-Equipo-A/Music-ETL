import matplotlib.pyplot as plt

def features_histogram(features_df):

    features_df = pd.read_csv('datasets/rank_1/features_scaled.csv')
    
    float_cols = features_df.select_dtypes(include='float64').columns
    fig, ax = plt.subplots(figsize=(12, 6))
    
    features_df[float_cols].hist(ax=ax, bins=40, layout=(3, 5))
    
    plt.rcParams.update({'font.size': 10})
    plt.tight_layout()
    
    return fig