import streamlit as st
import os

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")

# --- DEBUGGING UTILITY ---
# This helper finds the file regardless of where it is hidden
def try_switch(page_name):
    # Potential paths to check
    paths_to_try = [
        page_name, 
        os.path.join("pages", page_name),
        page_name.lower(),
        os.path.join("pages", page_name.lower())
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            st.switch_page(path)
            return
            
    st.error(f"❌ Cannot find '{page_name}'. Checked: {paths_to_try}")
    st.info("💡 Tip: Check if you spelled the filename correctly on GitHub (including .py)")

# --- UI LAYOUT ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔮 Prediction", use_container_width=True):
        try_switch("Predictive_page.py")

with col2:
    if st.button("📊 Dashboard Overview", use_container_width=True):
        try_switch("Dashboard_Overview.py")

with col3:
    if st.button("🌦 Climate Impact", use_container_width=True):
        try_switch("Climate_Impact.py")

# --- FILE LISTER (Check this if it fails) ---
with st.expander("🔍 Click here to see what files are actually on the server"):
    st.write("Files in main folder:", os.listdir("."))
    if os.path.exists("pages"):
        st.write("Files in 'pages' folder:", os.listdir("pages"))
