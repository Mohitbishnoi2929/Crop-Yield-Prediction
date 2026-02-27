import streamlit as st
import numpy as np
import pickle

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="Crop Yield Prediction", layout="wide")

# ------------------ Background Styling ------------------ #
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.main-card {
    background: rgba(0, 0, 0, 0.65);
    padding: 40px;
    border-radius: 15px;
    color: white;
}

h1, h2, h3, label, p {
    color: white !important;
}

.stButton > button {
    background-color: #4CAF50;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

.stButton
