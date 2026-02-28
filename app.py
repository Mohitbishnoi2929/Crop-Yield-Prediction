import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Crop Intelligence Hub", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CUSTOM STYLING (Dark Theme & Metrics) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #f2a900 !important; }
    .result-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #f2a900;
        text-align: center;
        font-size: 24px;
        color: #f2a900;
    }
    h1, h2, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & MODEL LOADING ---
@st.cache_data
def load_data():
    # Looking for your specific file yield_df.csv
    file_path = "yield_df.csv"
    if not os.path.exists(file_path):
        st.error(f"Error: '{file_path}' not found in the root directory.")
        st.info(f"Files found in GitHub: {os.listdir('.')}")
        st.stop()
    return pd.read_csv(file_path)

@st.cache_resource
def load_models():
    # Loading models from root directory based on your folder structure
    with open("Rs.pkl", "rb") as f:
        model = pickle.load(f)
    with open("preprocessor.pkl", "rb") as f:
        prep = pickle.load(f)
    return model, prep

df = load_data()
model, preprocessor = load_models()

# --- 4. TABS NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🔮 Yield Predictor", "🌍 Global Performance", "🌡️ Climate Impact"])

# ---------------- TAB 1: PREDICTOR ----------------
with tab1:
    st.title("Crop Yield Prediction")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            Area = st.selectbox("Select Country/Area", sorted(df['Area'].unique()))
            Item = st.selectbox("Select Crop Type", sorted(df['Item'].unique()))
            Year = st.number_input("Year", min_value=1990, max_value=2030, value=2024)
        with col2:
            Rainfall = st.number_input("Average Rainfall (mm/year)", value=1100.0)
            Temp = st.number_input("Average Temperature (°C)", value=20.0)
            Pesticide = st.number_input("Pesticide Used (tonnes)", value=100.0)

    if st.button("Predict Yield", use_container_width=True):
        try:
            # Preparing features for preprocessor
            features = np.array([[Area, Item, Year, Rainfall, Temp, Pesticide]], dtype=object)
            transformed = preprocessor.transform(features)
            prediction = model.predict(transformed)
            
            st.markdown(f"""<div class='result-box'>
                🌾 Predicted Crop Yield: {round(float(prediction[0]), 2)} hg/ha
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction Error: {e}")

# ---------------- TAB 2: GLOBAL PERFORMANCE ----------------
with tab2:
    st.title("Global Crop Performance")
    
    # KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Countries", df['Area'].nunique())
    m2.metric("Total Crops", df['Item'].nunique())
    m3.metric("Avg Yield", f"{round(df['hg/ha_yield'].mean(), 2)} hg/ha")
    m4.metric("Max Yield Record", f"{df['hg/ha_yield'].max()} hg/ha")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Crop-wise Yield vs Pesticide Usage")
        # Aggregating data for the bar chart
        crop_stats = df.groupby('Item').agg({'hg/ha_yield':'mean', 'pesticides_tonnes':'mean'}).reset_index()
        fig1 = px.bar(crop_stats, x='Item', y=['hg/ha_yield', 'pesticides_tonnes'], 
                      barmode='group', color_discrete_sequence=['#1f77b4', '#f2a900'], template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Top 10 Producing Countries")
        top_countries = df.groupby('Area')['hg/ha_yield'].mean().sort_values(ascending=False).head(10).reset_index()
        fig2 = px.bar(top_countries, x='hg/ha_yield', y='Area', orientation='h', color_discrete_sequence=['#f2a900'], template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Yield Distribution Map")
    fig_map = px.choropleth(df, locations="Area", locationmode='country names', color="hg/ha_yield", 
                            hover_name="Area", color_continuous_scale="Viridis", template="plotly_dark")
    st.plotly_chart(fig_map, use_container_width=True)

# ---------------- TAB 3: CLIMATE IMPACT ----------------
with tab3:
    st.title("Climate Impact Dashboard")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Yield vs Average Rainfall Trend")
        yearly_rain = df.groupby('Year').agg({'hg/ha_yield':'mean', 'average_rain_fall_mm_per_year':'mean'}).reset_index()
        fig3 = px.area(yearly_rain, x='Year', y='hg/ha_yield', color_discrete_sequence=['#00CC96'], template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Impact of Rainfall on Yield")
        fig4 = px.scatter(df, x="average_rain_fall_mm_per_year", y="hg/ha_yield", color="Item", opacity=0.4, template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)

    with c2:
        st.subheader("Yield vs Average Temperature Trend")
        yearly_temp = df.groupby('Year').agg({'hg/ha_yield':'mean', 'avg_temp':'mean'}).reset_index()
        fig5 = px.line(yearly_temp, x='Year', y='avg_temp', color_discrete_sequence=['#EF553B'], template="plotly_dark")
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("Impact of Temperature on Yield")
        fig6 = px.scatter(df, x="avg_temp", y="hg/ha_yield", color="Item", opacity=0.4, template="plotly_dark")
        st.plotly_chart(fig6, use_container_width=True)
