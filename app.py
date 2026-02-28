import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Crop Intelligence Hub", layout="wide")

# --- 2. CLEANER BACKGROUND & TEXT STYLING ---
st.markdown("""
    <style>
    .stApp {
        /* High-visibility green field background */
        background-image: url("https://images.unsplash.com/photo-1530507629858-e4977d30e9e0?q=80&w=2000");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Frosted Glass with high opacity for black text contrast */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.90); 
        border-radius: 15px;
        padding: 40px;
        margin-top: 25px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }
    /* Bold Black for all UI elements and labels */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], 
    h1, h2, h3, p, label, .stSelectbox label, .stNumberInput label { 
        color: #000000 !important; 
        font-weight: 800 !important; 
    }
    .result-box {
        background-color: rgba(0, 0, 0, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 3px solid #000000;
        text-align: center;
        font-size: 26px;
        color: #000000;
        font-weight: 900;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER: STRONG BLACK AXIS STYLING ---
def style_chrome_final(fig):
    fig.update_layout(
        font=dict(color="black", size=13, family="Arial Black"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0.05)',
        margin=dict(l=60, r=60, t=50, b=50),
        legend=dict(font=dict(color="black"))
    )
    # Applying thick black lines to axes for visibility
    fig.update_xaxes(showline=True, linewidth=3, linecolor='black', tickfont=dict(color='black', size=11, family="Arial Black"), gridcolor='rgba(0,0,0,0.1)', title_font=dict(color='black'))
    fig.update_yaxes(showline=True, linewidth=3, linecolor='black', tickfont=dict(color='black', size=11, family="Arial Black"), gridcolor='rgba(0,0,0,0.1)', title_font=dict(color='black'))
    return fig

# --- 4. DATA & MODELS ---
@st.cache_data
def load_data():
    if not os.path.exists("yield_df.csv"):
        st.error("File 'yield_df.csv' not found in root directory!")
        st.stop()
    return pd.read_csv("yield_df.csv")

@st.cache_resource
def load_models():
    with open("Rs.pkl", "rb") as f: model = pickle.load(f)
    with open("preprocessor.pkl", "rb") as f: prep = pickle.load(f)
    return model, prep

df = load_data()
model, preprocessor = load_models()

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["🔮 Yield Predictor", "🌍 Global Performance", "🌡️ Climate Impact"])

# ---------------- TAB 1: PREDICTOR ----------------
with tab1:
    st.title("🌾 Crop Yield Prediction")
    c1, c2 = st.columns(2)
    with c1:
        Area_in = st.selectbox("Select Country", sorted(df['Area'].unique()))
        Item_in = st.selectbox("Select Crop", sorted(df['Item'].unique()))
        Year_in = st.number_input("Year", 1990, 2030, 2024)
    with c2:
        Rain_in = st.number_input("Avg Rainfall (mm/year)", value=1100.0)
        Temp_in = st.number_input("Avg Temp (°C)", value=20.0)
        Pest_in = st.number_input("Pesticide (tonnes)", value=100.0)

    if st.button("Predict Yield Now", use_container_width=True):
        feats = np.array([[Area_in, Item_in, Year_in, Rain_in, Temp_in, Pest_in]], dtype=object)
        pred = model.predict(preprocessor.transform(feats))
        st.markdown(f"<div class='result-box'>🌾 Predicted Yield: {round(float(pred[0]), 2)} hg/ha</div>", unsafe_allow_html=True)

# ---------------- TAB 2: GLOBAL PERFORMANCE ----------------
with tab2:
    st.title("🌍 Global Crop Performance")
    
    kcols = st.columns(6)
    kcols[0].metric("Total Prod.", f"{df['hg/ha_yield'].sum()/1e9:.1f}B")
    kcols[1].metric("Avg Yield", f"{int(df['hg/ha_yield'].mean())}")
    kcols[2].metric("Countries", df['Area'].nunique())
    kcols[3].metric("Crops", df['Item'].nunique())
    kcols[4].metric("Pest. Eff.", "2.08") 
    kcols[5].metric("Total Pest.", f"{df['pesticides_tonnes'].sum()/1e6:.1f}M")

    l, r = st.columns([3, 2])
    with l:
        st.subheader("Crop-wise Yield vs Pesticide Usage")
        crop_agg = df.groupby('Item').mean(numeric_only=True).reset_index()
        f1 = px.bar(crop_agg, x='Item', y=['hg/ha_yield', 'pesticides_tonnes'], barmode='group', text_auto='.2s')
        st.plotly_chart(style_chrome_final(f1), use_container_width=True)
    with r:
        rank_type = st.radio("Rank Countries:", ["Top 10", "Bottom 10"], horizontal=True)
        cy = df.groupby('Area')['hg/ha_yield'].mean().sort_values(ascending=(rank_type=="Bottom 10")).head(10).reset_index()
        f2 = px.bar(cy, x='hg/ha_yield', y='Area', orientation='h', text=(cy['hg/ha_yield']/cy['hg/ha_yield'].sum()*100).round(1).astype(str)+'%')
        st.plotly_chart(style_chrome_final(f2), use_container_width=True)

    st.subheader("Global Yield Distribution Map")
    f_map = px.choropleth(df, locations="Area", locationmode='country names', color="hg/ha_yield", color_continuous_scale="YlGnBu")
    f_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black", family="Arial Black"))
    st.plotly_chart(f_map, use_container_width=True)

# ---------------- TAB 3: CLIMATE IMPACT ----------------
with tab3:
    st.title("🌡️ Climate Impact Analysis")
    
    ck = st.columns(4)
    ck[0].metric("Avg Rain", f"{int(df['average_rain_fall_mm_per_year'].mean())} mm")
    ck[1].metric("Avg Temp", f"{round(df['avg_temp'].mean(), 2)} °C")
    ck[2].metric("Efficiency", "67.06%")
    ck[3].metric("Max Prod", f"{int(df['hg/ha_yield'].max()/1000)}K")

    st.subheader("Yield vs Average Temperature Trend")
    t_trend = df.groupby('Year').mean(numeric_only=True).reset_index()
    f_temp = go.Figure()
    f_temp.add_trace(go.Scatter(x=t_trend['Year'], y=t_trend['hg/ha_yield'], name="Yield (hg/ha)", line=dict(color='black', width=4)))
    f_temp.add_trace(go.Scatter(x=t_trend['Year'], y=t_trend['avg_temp'], name="Temp (°C)", yaxis="y2", line=dict(color='red', width=4)))
    
    f_temp.update_layout(
        yaxis=dict(title="Yield (hg/ha)", titlefont=dict(color="black"), tickfont=dict(color="black")),
        yaxis2=dict(title="Temp (°C)", titlefont=dict(color="red"), tickfont=dict(color="red"), overlaying='y', side='right', showline=True, linewidth=3, linecolor='red')
    )
    st.plotly_chart(style_chrome_final(f_temp), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Impact of Temperature on Yield")
        f_scat = px.scatter(df, x="avg_temp", y="hg/ha_yield", color="Item", hover_data=['Area'])
        st.plotly_chart(style_chrome_final(f_scat), use_container_width=True)
    with c2:
        st.subheader("Annual Yield Growth %")
        y_trend = df.groupby('Year')['hg/ha_yield'].mean().reset_index()
        y_trend['Growth'] = (y_trend['hg/ha_yield'].pct_change() * 100).round(1)
        f_growth = px.line(y_trend.dropna(), x='Year', y='Growth', markers=True, text=y_trend['Growth'].dropna().apply(lambda x: f'{x}%'))
        st.plotly_chart(style_chrome_final(f_growth), use_container_width=True)
