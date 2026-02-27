import streamlit as st
import os

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Crop Yield Analytics Platform")
st.markdown("---")

# Navigation Columns
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔮 Prediction", use_container_width=True):
        # We try both common paths to be safe
        if os.path.exists("pages/Predictive_page.py"):
            st.switch_page("pages/Predictive_page.py")
        else:
            st.switch_page("Predictive_page.py")

with col2:
    if st.button("📊 Dashboard Overview", use_container_width=True):
        if os.path.exists("pages/Dashboard_Overview.py"):
            st.switch_page("pages/Dashboard_Overview.py")
        else:
            st.switch_page("Dashboard_Overview.py")

with col3:
    if st.button("🌦 Climate Impact", use_container_width=True):
        if os.path.exists("pages/Climate_Impact.py"):
            st.switch_page("pages/Climate_Impact.py")
        else:
            st.switch_page("Climate_Impact.py")

# DEBUG SECTION (Only shows if something is wrong)
with st.expander("🛠 Debug: Check File Structure"):
    st.write("Current Files in Root:")
    st.write(os.listdir("."))
    if os.path.exists("pages"):
        st.write("Files in 'pages' folder:")
        st.write(os.listdir("pages"))
