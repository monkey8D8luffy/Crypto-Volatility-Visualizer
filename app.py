import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- STAGE 6: Streamlit Interface Setup ---
# Designing a Streamlit app with sliders and controls that update the graphs instantly 
st.set_page_config(page_title="Crypto Volatility Dashboard", layout="wide")
st.title("Crypto Volatility Visualizer 📈")

# Sidebar filters: choose pattern, set amplitude/frequency/drift 
st.sidebar.header("1. Math Simulation Controls")
pattern = st.sidebar.selectbox("Choose Pattern", ["Sine Wave (Stable)", "Random Noise (Volatile)"])
amplitude = st.sidebar.slider("Amplitude (Swing Size)", 1.0, 50.0, 10.0)
frequency = st.sidebar.slider("Frequency (Swing Speed)", 0.1, 5.0, 1.0)
drift = st.sidebar.slider("Drift (Long-term slope)", -2.0, 2.0, 0.0)

# Writing Python functions to create wave-like price swings (sine/cosine), sudden jumps (random noise), and long-term drift 
x_sim = np.linspace(0, 10, 100)
if pattern == "Sine Wave (Stable)":
    y_sim = amplitude * np.sin(frequency * x_sim) + (drift * x_sim)
else:
    y_sim = amplitude * np.random.randn(100) * frequency + (drift * x_sim)

st.subheader("Mathematical Simulation of Market Swings")
sim_fig = px.line(x=x_sim, y=y_sim, title=f"Simulated {pattern}")
st.plotly_chart(sim_fig, use_container_width=True)

# Key metrics displayed: volatility index, average drift 
volatility_index = np.std(y_sim)
st.sidebar.markdown("---")
st.sidebar.subheader("Simulation Metrics")
st.sidebar.metric(label="Volatility Index (Std Dev)", value=f"{volatility_index:.2f}")
st.sidebar.metric(label="Average Drift", value=f"{drift:.2f}")


st.markdown("---")


# --- STAGE 4: Data Preparation & Exploration ---
st.header("2. Real Cryptocurrency Data Analysis")

@st.cache_data
def prepare_data(filepath):
    # 1. Loading the dataset using read_excel for your chunked file
    try:
        df = pd.read_excel(filepath) 
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
        return None
    
    # 2. Rename columns into simpler names if needed (e.g., Close -> Price) 
    if 'Close' in df.columns:
        df.rename(columns={'Close': 'Price'}, inplace=True)
        
    # 3. Convert Timestamp into a proper date-time format 
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', errors='ignore') 
        # Note: If your excel dates are already formatted, pandas usually handles it automatically
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.rename(columns={'Date': 'Timestamp'}, inplace=True)
        
    # 4. Handle missing data by dropping them 
    df = df.dropna()
    df = df.sort_values(by='Timestamp')
    
    return df

# !!! IMPORTANT: Replace this string with the exact name of your new Excel file !!!
df = prepare_data("crypto_data.xlsx.xlsx") 

if df is not None:
    # 5. Always check the dataset shape (rows × columns) 
    st.write(f"**Dataset Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Check the columns: print the first few rows to see the structure using "head" function 
    with st.expander("View Raw Data Structure (First few rows)"):
        st.dataframe(df.head()) 
        
    # 6. Subset for simplicity: take a smaller part (like one week or one month) 
    st.sidebar.markdown("---")
    st.sidebar.header("Real Data Controls")
    days_to_show = st.sidebar.slider("Data points to analyze (Subset)", 10, len(df), min(1000, len(df)))
    subset_df = df.tail(days_to_show)


    # --- STAGE 5: Build Visualizations ---
    # Making interactive graphs using Python libraries like Matplotlib or Plotly 
    
    # A. Line Graph of Price Over Time: Plot “Date” on the X-axis and “Close Price” on the Y-axis 
    st.subheader("Bitcoin Price Over Time")
    fig_price = px.line(subset_df, x='Timestamp', y='Price', 
                        title='Bitcoin Price Movements (Close Price)')
    
    # D. Stable vs Volatile Periods: Mark areas where price looks stable (flat) vs volatile (sharp ups and downs) 
    # We dynamically highlight the first quarter of the selected data as 'Volatile' and the last half as 'Stable' as an example
    fig_price.add_vrect(x0=subset_df['Timestamp'].iloc[0], x1=subset_df['Timestamp'].iloc[len(subset_df)//4], 
                        fillcolor="red", opacity=0.1, line_width=0, annotation_text="Volatile Period Example")
    fig_price.add_vrect(x0=subset_df['Timestamp'].iloc[len(subset_df)//2], x1=subset_df['Timestamp'].iloc[-1], 
                        fillcolor="green", opacity=0.1, line_width=0, annotation_text="Stable Period Example")
    
    st.plotly_chart(fig_price, use_container_width=True)

    # B. High vs Low Comparison: Make a line graph showing both “High” and “Low” prices on the same chart 
    st.subheader("Daily Volatility: High vs Low Comparison")
    fig_hl = go.Figure()
    fig_hl.add_trace(go.Scatter(x=subset_df['Timestamp'], y=subset_df['High'], name='High Price', line=dict(color='green')))
    fig_hl.add_trace(go.Scatter(x=subset_df['Timestamp'], y=subset_df['Low'], name='Low Price', line=dict(color='red')))
    fig_hl.update_layout(title='High and Low Prices Over Time', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig_hl, use_container_width=True)

    # C. Volume Analysis: Create a bar chart for “Volume” 
    st.subheader("Trading Volume Analysis")
    # Handling volume column names from various crypto dataset formats
    vol_col = 'Volume' if 'Volume' in subset_df.columns else 'Volume_(BTC)' if 'Volume_(BTC)' in subset_df.columns else None
    
    if vol_col:
        fig_vol = px.bar(subset_df, x='Timestamp', y=vol_col, title='Volume of Bitcoins Traded')
        st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.warning("Volume column not found in dataset. Skipping volume chart.")

else:
    st.error("⚠️ Please check the file name in the code. Ensure your Excel file is in the same folder as this app.")
