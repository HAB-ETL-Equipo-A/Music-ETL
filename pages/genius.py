import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import pandas as pd
import sys
import asyncio
import json
import secrets
import os
import time
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('..')
from genius_api import GeniusAPI
from classifier import Classifier
import threading

st.set_page_config(layout="wide")
cookies = EncryptedCookieManager(prefix="ktosiek/streamlit-cookies-manager/", password=os.environ.get("COOKIES_PASSWORD", ""))
if not cookies.ready():
    st.stop()

query_params = st.query_params
access_token = cookies.get("genius_access_token")
api = GeniusAPI(access_token, redirect_url='http://localhost:8501/genius')

@st.cache_resource
def init_model():
    return Classifier('zero-shot-classification', 'roberta-large-mnli')

cls = init_model()

with open('datasets/topic_labels.json', 'r') as file:
    labels_json = json.load(file)
label_pairs = labels_json['labels']

def auth_details():
    with open('secrets.json') as f:
        _secrets = json.load(f)
    client_id = _secrets['GENIUS_CLIENT_ID']
    client_secret = _secrets['GENIUS_CLIENT_SECRET']
    return client_id, client_secret

# API Callback Function
def callback(code):
    st.write(f"Authorization code received: {code}")

    client_id, client_secret = auth_details()
    access_token = asyncio.run(api.authenticate(code, client_id, client_secret))
    
    if access_token:
        cookies["genius_access_token"] = access_token
        cookies.save()
        st.success("Access token received!")
        main()
    else:
        st.error("Failed to exchange code for access token.")

async def fetch_lyrics(song, artist):
    result = await api.get_songs_data([song], [artist], retries=2, delay=3)
    if result:
        lyrics_link = result[0]['result']['url']
        lyrics = api.get_lyrics(lyrics_link)  # Assume this is another function to fetch lyrics from the URL
        st.session_state.lyrics = lyrics
        st.session_state.song = song
        st.session_state.artist = artist
    else:
        st.session_state.lyrics = None
        st.write("No results found.")
        
def show_form():
    with st.form(key='song_form'):
        song = st.text_input("Song Name")
        artist = st.text_input("Artist Name")
        submit_button = st.form_submit_button("Search Lyrics")
        
        if submit_button:
            if song or artist:
                st.spinner('Fetching lyrics...')
                asyncio.run(fetch_lyrics(song, artist))
            else:
                st.error("Please enter a song or artist names.")
                
def create_plot(data):
    values = []
    labels = []
    for pair in label_pairs:
        values.append([data[pair[0]], data[pair[1]]])
        labels.append(f'{pair[0]} vs {pair[1]}')
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    y_pos = np.arange(len(label_pairs))
    ax.barh(y_pos, [v[0] for v in values], align='center', color='skyblue', label='First value')
    ax.barh(y_pos, [v[1] for v in values], align='center', left=[v[0] for v in values], color='salmon', label='Second value')
    
    # Add labels and title
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Value')
    ax.set_title('Stacked Pairs of Data')
    ax.legend()
    
    plt.tight_layout()
    return fig

def show_classify():
    
    lyrics = st.session_state.lyrics
    classify_button = st.button('Classify')
    
    if classify_button:
        with st.spinner('Classifying...'):
            results = cls.classify([lyrics], label_pairs)
        
        st.success("Done!")
        
        df = pd.DataFrame(results)
        st.table(df)
        
        fig = create_plot(results[0])
        st.pyplot(fig)
        
def init():
    
    if 'code' in query_params:
        code = query_params["code"]
        callback(code)
    
    authenticated = asyncio.run(api.authenticated())

    if not authenticated:    
        state = secrets.token_urlsafe(16)
        client_id, _ = auth_details()
        
        auth_url = api.get_auth_url(state, client_id)
        st.markdown(f"Click below to authorize the Genius API:")
        
        st.link_button('Authenticate', auth_url)
        
    else:
        st.write("You're authenticated, proceed with using the Genius API!")
        main()

def main():
    show_form()
    
    if 'lyrics' in st.session_state and st.session_state.lyrics:
        st.write(f"**Song**: {st.session_state.song}")
        st.write(f"**Artist**: {st.session_state.artist}")
        st.write(f"**Lyrics**: {st.session_state.lyrics}")

        clear_button = st.button('Clear')
        if clear_button:
            st.session_state.lyrics = None
            st.session_state.song = None
            st.session_state.artist = None
            st.rerun()

        show_classify()
        
    elif 'lyrics' in st.session_state and st.session_state.lyrics is None:
        st.write("No lyrics available.")

init()
