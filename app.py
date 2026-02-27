import streamlit as st
import os

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")
st.markdown("---")

col1, col2, col3 = st.columns(3)

# Define the filenames
p1 = "Predictive_page.py"
p2 = "Dashboard_Overview.py"
p3 = "Climate_Impact.py"

with col1:
    if st.button("🔮 Prediction", use_container_width=True):
        if os.path.exists(f"pages/{p1}"):
            st.switch_page(f"pages/{p1}")
        else:
            st.switch_page(p1)

with col2:
    if st.button("📊 Dashboard Overview", use_container_width=True):
        if os.path.exists(f"pages/{p2}"):
            st.switch_page(f"pages/{p2}")
        else:
            st.switch_page(p2)

with col3:
    if st.button("🌦 Climate Impact", use_container_width=True):
        if os.path.exists(f"pages/{p3}"):
            st.switch_page(f"pages/{p3}")
        else:
            st.switch_page(p3)
