import streamlit as st
import numpy as np
import pickle

# ---------------- Page Config ---------------- #
st.set_page_config(page_title="Crop Yield Prediction", layout="wide")

# ---------------- Background CSS (Safe Version) ---------------- #
st.markdown(
    "<style>"
    ".stApp {"
    "background-image: url('https://images.unsplash.com/photo-1500382017468-9049fed747ef');"
    "background-size: cover;"
    "background-position: center;"
    "background-attachment: fixed;"
    "}"
    ".main-card {"
