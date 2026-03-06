import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import google.generativeai as genai
import os

# --- STAGE 6: Streamlit Interface Setup ---
st.set_page_config(page_title="Pro Crypto Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- HIGH VISIBILITY GREEN GLASS CSS ---
st.markdown("""
<style>
    /* 1. Main Background: Soft, clean mint-to-white gradient */
    .stApp {
        background: linear-gradient(135deg, #d1fae5 0%, #f8fafc 100%);
    }
    
    /* 2. Sidebar: Clear Frosted Glass */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    /* 3. Global Text: FORCE HIGH-CONTRAST DARK GREEN */
    html, body, [class*="st-"], .stMarkdown p, .stMarkdown span, label {
        color: #064e3b !important; /* Deep Forest Green */
        font-weight: 500;
    }
    
    /* 4. Headers: Vibrant Emerald Green */
    h1, h2, h3, h4, h5, h6 {
        color: #047857 !important; 
        font-weight: 800 !important;
    }
    
    /* 5. Fix Input Boxes (Chat, Dropdowns, Sliders) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stChatInput textarea {
        background-color: #ffffff !important;
        color: #064e3b !important; /* Dark Green typing text */
        border: 2px solid #6ee7b7 !important; /* Light green border */
        border-radius: 8px !important;
        font-weight: bold;
    }
    
    /* 6. AI Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px;
        border: 1px solid #34d399;
        padding: 15px;
        color: #064e3b !important;
    }
    
    /* 7. Metric Values (The big numbers) */
    [data-testid="stMetricValue"] {
        color: #065f46 !important; 
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("💠 Pro Crypto Volatility Visualizer")
st.markdown("Analyze market swings with professional quantitative models and AI insights.")
st.markdown("---")

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

# !!! Replace "crypto_data.xlsx" with your exact Excel file name !!!
df = prepare_data("crypto_data.xlsx") 

# Retrieve initial dynamic base price if data exists, otherwise default to 50000
base_start_price = float(df['Price'].iloc[-1]) if df is not None else 50000.0

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Dashboard Controls")

# 1. Professional Math Simulation Controls
with st.sidebar.expander("🧮 Quant Math Simulation", expanded=False):
    st.markdown("Configure the **Stochastic Harmonic Model**")
    base_price = st.number_input("Base Starting Price ($)", value=base_start_price)
    drift = st.slider("Macro Trend (Drift)", -100.0, 100.0, 10.0, help="Long-term linear slope (Integral effect)")
    wave_amp = st.slider("Market Cycle Swing (Sine Amp)", 0.0, 5000.0, 1000.0, help="Wave-like macro swings")
    wave_freq = st.slider("Cycle Speed (Frequency)", 0.1, 5.0, 0.5)
    noise_vol = st.slider("Daily Volatility (Random Noise)", 0.0, 2000.0, 500.0, help="Sudden unpredictable jumps")

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
        paper_bgcolor='rgba(255,255,255,0.6)', 
        plot_bgcolor='rgba(255,255,255,0.8)',  
        font=dict(color='#064e3b'), # Dark Green text
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # --- STAGE 5: Professional Visualizations ---
    tab1, tab2, tab3 = st.tabs(["📊 Professional Charting", "🧮 Math Simulation", "🤖 AI Data Assistant"])

    with tab1:
        st.subheader("Bitcoin Candlestick Chart")
        if all(col in subset_df.columns for col in ['Open', 'High', 'Low', 'Price']):
            fig_candle = go.Figure(data=[go.Candlestick(x=subset_df['Timestamp'],
                            open=subset_df['Open'],
                            high=subset_df['High'],
                            low=subset_df['Low'],
                            close=subset_df['Price'],
                            increasing_line_color='#059669', # Solid Green
                            decreasing_line_color='#ef4444')]) # Red for contrast
            
            fig_candle.update_layout(**glass_chart_layout, title='Price Action', yaxis_title='Price (USD)', xaxis_title='Date')
            st.plotly_chart(fig_candle, use_container_width=True)
        else:
            st.warning("Need Open, High, Low, and Close/Price columns for Candlestick chart.")

        st.subheader("Trading Volume Analysis")
        vol_col = 'Volume' if 'Volume' in subset_df.columns else 'Volume_(BTC)' if 'Volume_(BTC)' in subset_df.columns else None
        if vol_col:
            fig_vol = px.bar(subset_df, x='Timestamp', y=vol_col)
            fig_vol.update_traces(marker_color='#10b981') # Bright Green
            fig_vol.update_layout(**glass_chart_layout)
            st.plotly_chart(fig_vol, use_container_width=True)

    with tab2:
        st.subheader("Stochastic Harmonic Market Model")
        st.markdown(r"**Mathematical Formula:** $Price(t) = P_0 + (\mu \cdot t) + (A \cdot \sin(\omega t)) + (\sigma \cdot Z_t)$")
        st.markdown("This professional quantitative model combines long-term drift, macro market wave cycles (Sine), and unpredictable daily market volatility (Random Noise).")
        
        # Professional Math implementation integrating Sine, Drift, and Noise
        t_sim = np.linspace(0, 100, 200) # Time vector
        trend_component = drift * t_sim
        wave_component = wave_amp * np.sin(wave_freq * t_sim)
        noise_component = noise_vol * np.random.randn(200)
        
        # Combine all mathematical elements
        simulated_prices = base_price + trend_component + wave_component + noise_component
        
        # Plotting the professional simulation
        fig_sim = go.Figure()
        
        # The volatile raw price
        fig_sim.add_trace(go.Scatter(x=t_sim, y=simulated_prices, mode='lines', 
                                     name='Simulated Raw Price', line=dict(color='#34d399', width=1.5)))
        
        # The underlying mathematical "True" trend (without noise)
        true_trend = base_price + trend_component + wave_component
        fig_sim.add_trace(go.Scatter(x=t_sim, y=true_trend, mode='lines', 
                                     name='Underlying Macro Wave', line=dict(color='#047857', width=3, dash='dash')))

        fig_sim.update_layout(**glass_chart_layout, title='Monte Carlo Harmonic Simulation', 
                              xaxis_title='Days (t)', yaxis_title='Simulated Price ($)')
        st.plotly_chart(fig_sim, use_container_width=True)

    # --- AI DATA ASSISTANT ---
    with tab3:
        st.subheader("🤖 Ask Gemini About Your Data")
        
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            data_context = f"""
            You are a professional crypto data analyst assistant. Here is the data summary:
            - Current Price: ${current_price:.2f}
            - Highest Price: ${max_price:.2f}
            - Lowest Price: ${min_price:.2f}
            - Volatility (Max - Min): ${volatility:.2f}
            Use this to answer the user accurately. Keep your tone highly professional.
            """

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("E.g., Based on the volatility, what is the current market risk?"):
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
