import streamlit as st
import glob
import os
import pandas as pd

csv_files = glob.glob(os.path.join('datasets', '*.csv'))

for file in csv_files:
    df = pd.read_csv(file)
    
    with st.expander(f"Click to expand: {os.path.basename(file)}"):
        st.write(df)