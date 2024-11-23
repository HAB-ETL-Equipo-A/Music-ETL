import streamlit as st
import matplotlib.pyplot as plt

st.title('Graphs')

features_df = pd.read_csv('datasets/rank_1/features_scaled.csv')

float_cols = features_df.select_dtypes(include='float64').columns
features_df[float_cols].hist(figsize=(12, 6), bins=40, layout=(3, 5))
plt.rcParams.update({'font.size': 10})
plt.tight_layout() 
plt.show()