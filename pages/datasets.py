import streamlit as st
import glob
import os
import pandas as pd

st.set_page_config(layout="wide")

st.title('Datasets')

csv_files = glob.glob(os.path.join('datasets/rank_1', '*.csv'))

for file in csv_files:
    df = pd.read_csv(file)
    
    with st.expander(f"Click to expand: {os.path.basename(file)}"):
        st.dataframe(df, use_container_width=True)
