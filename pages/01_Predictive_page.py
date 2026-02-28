import streamlit as st
import pickle
import os

# 1. FIND THE PATHS
current_script_path = os.path.abspath(__file__)
pages_folder = os.path.dirname(current_script_path)
root_folder = os.path.dirname(pages_folder)

# 2. SHOW DEBUG INFO ON SCREEN
st.title("🛠 Debugging File Paths")
st.write(f"**Current Script:** `{current_script_path}`")
st.write(f"**Looking in Root Folder:** `{root_folder}`")

# List all files in the root folder so we can see them
files_in_root = os.listdir(root_folder)
st.write("**Files actually found in Root:**", files_in_root)

# 3. ATTEMPT TO LOAD
model_path = os.path.join(root_folder, "Rs.pkl")
prep_path = os.path.join(root_folder, "preprocessor.pkl")

if os.path.exists(model_path) and os.path.exists(prep_path):
    st.success("✅ SUCCESS: Files found!")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(prep_path, "rb") as f:
        preprocessor = pickle.load(f)
else:
    st.error("❌ ERROR: Files NOT found in the root folder.")
    if "Rs.pkl" in [f.lower() for f in files_in_root]:
        st.warning("Hint: I found a file with a similar name, check your Capitalization (Rs.pkl vs rs.pkl)!")
