import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import os
import sys
sys.path.append('..')
from spotify_api import SpotifyAPI

st.set_page_config(layout="wide")
cookies = EncryptedCookieManager(prefix="ktosiek/streamlit-cookies-manager/", password=os.environ.get("COOKIES_PASSWORD", ""))
if not cookies.ready():
    st.stop()

query_params = st.query_params
access_token = cookies.get("spotify_access_token")
token_expires = cookies.get("spotify_token_expires")

