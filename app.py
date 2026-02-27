import streamlit as st
import numpy as np
import pickle
import base64

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="Crop Yield Prediction", layout="wide")

# ------------------ Background Image ------------------ #
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
            background-size: cover;
            background-position: center;
            background-attachment: fixed
