import streamlit as st
import os

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")
st.markdown("---")

# Function to safely switch pages
def navigate_to(page_path):
    if os.path.exists(page_path):
        st.switch_page(page_path)
    else:
        st.error(f"📂 File Not Found: I looked for '{page_path}' but couldn't find it.")
        st.info("Check if your folder is named 'pages' and the filename is spelled correctly on GitHub.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔮 Prediction", use_container_width=True):
        navigate_to("pages/Predictive_
