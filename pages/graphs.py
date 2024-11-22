import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('..')
import plots

st.title('Graphs')

st.subheader('Hot 100 Rank 1 Features Distribution')

fig = plots.features_histogram()
st.pyplot(fig)

st.subheader('Change in Features Over Time')

fig = plots.features_changes_over_time()
st.pyplot(fig)