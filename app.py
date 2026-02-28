import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Crop Intelligence Dashboard", layout="wide")

# --- CUSTOM CSS FOR DARK THEME & CARDS ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 25px; color: #f2a900; }
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #f2a900;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA & MODELS ---
@st.cache_data
def load_data():
    df = pd.read_csv("yield_data.csv") # Ensure this matches your filename exactly
    return df

@st.cache_resource
def load_models():
    model = pickle.load(open("Rs.pkl", "rb"))
    prep = pickle.load(open("preprocessor.pkl", "rb"))
    return model, prep

df = load_data()
model, preprocessor = load_models()

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🔮 Predictor", "🌍 Global Performance", "🌡️ Climate Impact"])

# ---------------- TAB 1: PREDICTOR ----------------
with tab1:
    st.header("Crop Yield Prediction")
    c1, c2 = st.columns(2)
    with c1:
        Area_in = st.selectbox("Select Area", df['Area'].unique())
        Item_in = st.selectbox("Select Crop", df['Item'].unique())
        Year_in = st.number_input("Year", 2024)
    with c2:
        Rain_in = st.number_input("Rainfall (mm)", 1000.0)
        Temp_in = st.number_input("Temp (°C)", 20.0)
        Pest_in = st.number_input("Pesticide (tonnes)", 100.0)
    
    if st.button("Predict"):
        features = np.array([[Area_in, Item_in, Year_in, Rain_in, Temp_in, Pest_in]], dtype=object)
        transformed = preprocessor.transform(features)
        pred = model.predict(transformed)
        st.success(f"Predicted Yield: {pred[0]:.2f} hg/ha")

# ---------------- TAB 2: GLOBAL PERFORMANCE ----------------
with tab2:
    # Sidebar-style metrics on the left
    m1, m2 = st.columns([1, 4])
    
    with m1:
        st.metric("Total Production", "2bn") # You can calculate these from df
        st.metric("Avg Production", f"{df['hg/ha_yield'].mean()/1000:.2f}K")
        st.metric("Total Countries", df['Area'].nunique())
        st.metric("Total Crops", df['Item'].nunique())
        
    with m2:
        st.subheader("Crop-wise Yield vs Pesticide Usage")
        # Dual Bar Chart
        fig_crop = px.bar(df.groupby('Item').agg({'hg/ha_yield':'mean', 'pesticides_tonnes':'mean'}).reset_index(), 
                          x='Item', y=['hg/ha_yield', 'pesticides_tonnes'], barmode='group',
                          color_discrete_sequence=['#1f77b4', '#f2a900'])
        st.plotly_chart(fig_crop, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Yield Distribution by Country")
        fig_map = px.choropleth(df, locations="Area", locationmode='country names', color="hg/ha_yield", hover_name="Area")
        st.plotly_chart(fig_map, use_container_width=True)
    with c2:
        st.subheader("Yield Per Year")
        fig_line = px.line(df.groupby('Year')['hg/ha_yield'].mean().reset_index(), x='Year', y='hg/ha_yield')
        st.plotly_chart(fig_line, use_container_width=True)

# ---------------- TAB 3: CLIMATE IMPACT ----------------
with tab3:
    st.header("Climate Impact Dashboard")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        # Dual axis trend for Rainfall
        st.subheader("Yield vs Average Rainfall Trend")
        fig_rain = px.area(df.groupby('Year').mean().reset_index(), x='Year', y='hg/ha_yield')
        st.plotly_chart(fig_rain, use_container_width=True)
        
        st.subheader("Yield vs Average Temperature Trend")
        fig_temp = px.line(df.groupby('Year').mean().reset_index(), x='Year', y='avg_temp', color_discrete_sequence=['red'])
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_b:
        st.subheader("Impact of Rainfall on Yield")
        fig_scat1 = px.scatter(df, x="average_rain_fall_mm_per_year", y="hg/ha_yield", color="Item", opacity=0.5)
        st.plotly_chart(fig_scat1, use_container_width=True)
        
        st.subheader("Impact of Temperature on Yield")
        fig_scat2 = px.scatter(df, x="avg_temp", y="hg/ha_yield", color="Item", opacity=0.5)
        st.plotly_chart(fig_scat2, use_container_width=True)
