import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('..')
from etl_plots import ETLPlots

st.set_page_config(layout="centered")

st.title('Plots')

plotter = ETLPlots('datasets')
plots = plotter.all_plots()

for fig in plots:
    st.pyplot(fig)
