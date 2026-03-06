import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import google.generativeai as genai
import os

# --- STAGE 6: Streamlit Interface Setup ---
st.set_page_config(page_title="Pro Crypto Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- THE GLASS OS CSS FIX ---
st.markdown("""
<style>
    /* 1. Main Background: Soft, clean light blue-to-white gradient */
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    
    /* 2. Sidebar: Clear Frosted Glass */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.6);
    }
    
    /* 3. Global Text Override: Force ALL text to be dark slate so it never vanishes */
    html, body, [class*="st-"], .stMarkdown p, .stMarkdown span, label {
        color: #1e293b !important;
    }
    
    /* 4. Headers: Deep Professional Blue */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important; 
        font-weight: 700 !important;
    }
    
    /* 5. Fix Input Boxes (Chat, Dropdowns, Sliders) so you can see what you type */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stChatInput textarea {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 8px !important;
    }
    
    /* 6. AI Chat Message Bubbles: Glass effect */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 15px;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("💠 Pro Crypto Volatility Visualizer")
st.markdown("Analyze market swings with professional tools and AI insights.")
st.markdown("---")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Dashboard Controls")

# 1. Math Simulation Controls
with st.sidebar.expander("1. Math Simulation Controls", expanded=False):
    pattern = st.selectbox("Choose Pattern", ["Sine Wave (Stable)", "Random Noise (Volatile)"])
    amplitude = st.slider("Amplitude (Swing Size)", 1.0, 50.0, 10.0)
    frequency = st.slider("Frequency (Swing Speed)", 0.1, 5.0, 1.0)
    drift = st.slider("Drift (Long-term slope)", -2.0, 2.0, 0.0)

# --- STAGE 4: Data Preparation ---
@st.cache_data
def prepare_data(filepath):
    try:
        df = pd.read_excel(filepath) 
    except Exception as e:
        return None
    
    if 'Close' in df.columns:
        df.rename(columns={'Close': 'Price'}, inplace=True)
        
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='ignore') 
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.rename(columns={'Date': 'Timestamp'}, inplace=True)
        
    df = df.dropna().sort_values(by='Timestamp')
    return df

df = prepare_data("crypto_data.xlsx.xlsx") 

if df is not None:
    st.sidebar.markdown("---")
    st.sidebar.header("📅 Real Data Timeline")
    days_to_show = st.sidebar.slider("Data points to analyze", 10, len(df), min(500, len(df)))
    subset_df = df.tail(days_to_show)

    # Key Metrics Row 
    col1, col2, col3, col4 = st.columns(4)
    current_price = subset_df['Price'].iloc[-1]
    max_price = subset_df['High'].max()
    min_price = subset_df['Low'].min()
    volatility = max_price - min_price
    
    col1.metric("Current Price", f"${current_price:,.2f}", delta=f"{(current_price - subset_df['Price'].iloc[-2]):.2f}")
    col2.metric("Period High", f"${max_price:,.2f}", delta="Peak", delta_color="normal")
    col3.metric("Period Low", f"${min_price:,.2f}", delta="Bottom", delta_color="inverse")
    col4.metric("Volatility Swing", f"${volatility:,.2f}", delta="Risk Level", delta_color="off")

    st.markdown("---")

    # Define a Glass layout template for Plotly Charts
    glass_chart_layout = dict(
        paper_bgcolor='rgba(255,255,255,0.4)', # Glassy background
        plot_bgcolor='rgba(255,255,255,0.7)',  # Slightly more solid plot area
        font=dict(color='#1e293b'),            # Dark slate text
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # --- STAGE 5: Professional Visualizations ---
    tab1, tab2, tab3 = st.tabs(["📊 Professional Charting", "🧮 Math Simulation", "🤖 AI Data Assistant"])

    with tab1:
        st.subheader("Bitcoin Candlestick Chart (Professional)")
        if all(col in subset_df.columns for col in ['Open', 'High', 'Low', 'Price']):
            fig_candle = go.Figure(data=[go.Candlestick(x=subset_df['Timestamp'],
                            open=subset_df['Open'],
                            high=subset_df['High'],
                            low=subset_df['Low'],
                            close=subset_df['Price'],
                            increasing_line_color='#10b981', # GREEN for up
                            decreasing_line_color='#ef4444')]) # RED for down
            
            fig_candle.update_layout(**glass_chart_layout, title='Price Action', yaxis_title='Price (USD)', xaxis_title='Date')
            st.plotly_chart(fig_candle, use_container_width=True)
        else:
            st.warning("Need Open, High, Low, and Close/Price columns for Candlestick chart.")

        st.subheader("Trading Volume Analysis")
        vol_col = 'Volume' if 'Volume' in subset_df.columns else 'Volume_(BTC)' if 'Volume_(BTC)' in subset_df.columns else None
        if vol_col:
            fig_vol = px.bar(subset_df, x='Timestamp', y=vol_col)
            fig_vol.update_traces(marker_color='#3b82f6') # BLUE for volume
            fig_vol.update_layout(**glass_chart_layout)
            st.plotly_chart(fig_vol, use_container_width=True)

    with tab2:
        st.subheader("Mathematical Simulation of Market Swings")
        x_sim = np.linspace(0, 10, 100)
        if pattern == "Sine Wave (Stable)":
            y_sim = amplitude * np.sin(frequency * x_sim) + (drift * x_sim)
            color = '#10b981' # GREEN for stable
        else:
            y_sim = amplitude * np.random.randn(100) * frequency + (drift * x_sim)
            color = '#ef4444' # RED for volatile

        sim_fig = px.line(x=x_sim, y=y_sim, title=f"Simulated {pattern}")
        sim_fig.update_traces(line_color=color)
        sim_fig.update_layout(**glass_chart_layout)
        st.plotly_chart(sim_fig, use_container_width=True)

    # --- AI DATA ASSISTANT ---
    with tab3:
        st.subheader("🤖 Ask Gemini About Your Data")
        st.markdown("Ask anything about the trends, volatility, or current stats of the chart.")
        
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            data_context = f"""
            You are a crypto data analyst assistant. Here is the data summary for the currently selected timeframe:
            - Current Price: ${current_price:.2f}
            - Highest Price: ${max_price:.2f}
            - Lowest Price: ${min_price:.2f}
            - Volatility (Max - Min): ${volatility:.2f}
            - Data points analyzed: {days_to_show}
            Use this data to answer the user's questions accurately.
            """

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("E.g., What is the price volatility?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    try:
                        full_prompt = f"{data_context}\n\nUser Question: {prompt}"
                        response = model.generate_content(full_prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Error communicating with AI: {e}")
        else:
            st.info("⚠️ Please add your GEMINI_API_KEY to your Streamlit secrets (.streamlit/secrets.toml) to enable the chatbot.")

else:
    st.error("⚠️ Please check the file name in the code. Ensure your Excel file is in the same folder as this app.")
