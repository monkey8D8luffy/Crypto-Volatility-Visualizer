import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- STAGE 6: Streamlit Interface Setup ---
st.set_page_config(page_title="Crypto Volatility Visualizer", layout="wide")
st.title("Crypto Volatility Visualizer 📈")
st.markdown("Welcome to the FinTechLab Pvt. Ltd. Dashboard for analyzing market swings.")

# --- STAGE 4: Data Preparation & Exploration ---
@st.cache_data
def load_and_clean_data(filepath):
    # Loading the dataset
    df = pd.read_csv(filepath)
    
    # Check and clean column names (Rename columns into simpler names if needed)
    df.columns = df.columns.str.strip().str.capitalize()
    
    # Convert Timestamp to a proper date-time format
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    elif 'Date' in df.columns: # Fallback just in case your CSV uses 'Date'
        df['Date'] = pd.to_datetime(df['Date'])
        df.rename(columns={'Date': 'Timestamp'}, inplace=True)
        
    # Handle missing data by dropping rows with blank values
    df = df.dropna()
    
    # Sort by date
    df = df.sort_values(by='Timestamp')
    
    return df

# Please ensure your CSV file is in the same folder and named correctly.
# Replace 'crypto_data.csv' with the actual name of your Excel/CSV file.
try:
    data = load_and_clean_data('crypto_data.csv')
    
    # --- Sidebar Filters (Subset for simplicity) ---
    st.sidebar.header("Dashboard Controls")
    st.sidebar.write("Adjust the controls to explore the data.")
    
    # Date range selector to take a smaller part of the dataset
    min_date = data['Timestamp'].min()
    max_date = data['Timestamp'].max()
    
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data based on sidebar selection
    mask = (data['Timestamp'] >= pd.to_datetime(start_date)) & (data['Timestamp'] <= pd.to_datetime(end_date))
    filtered_data = data.loc[mask]

    # --- STAGE 5: Build Visualizations ---
    st.subheader("Market Swings Analysis")
    
        
    # 1. Line Graph of Price Over Time (Close Price)
    st.markdown("### Bitcoin Price Over Time")
    fig_close = px.line(filtered_data, x='Timestamp', y='Close', 
                        title="Close Price Movements (Volatility over time)",
                        labels={'Timestamp': 'Date', 'Close': 'Close Price'})
    st.plotly_chart(fig_close, use_container_width=True)

    # 2. High vs Low Comparison
    st.markdown("### High vs Low Price Comparison")
    fig_hl = go.Figure()
    fig_hl.add_trace(go.Scatter(x=filtered_data['Timestamp'], y=filtered_data['High'], mode='lines', name='High Price', line=dict(color='green')))
    fig_hl.add_trace(go.Scatter(x=filtered_data['Timestamp'], y=filtered_data['Low'], mode='lines', name='Low Price', line=dict(color='red')))
    fig_hl.update_layout(title="Daily Volatility: Highs and Lows", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig_hl, use_container_width=True)

    # 3. Volume Analysis (Bar Chart)
    st.markdown("### Trading Volume Analysis")
    fig_vol = px.bar(filtered_data, x='Timestamp', y='Volume', 
                     title="Volume Traded Over Time",
                     labels={'Timestamp': 'Date', 'Volume': 'Volume Traded'})
    st.plotly_chart(fig_vol, use_container_width=True)
    
    # 4. Key Metrics Display
    st.sidebar.markdown("---")
    st.sidebar.subheader("Key Metrics")
    avg_close = filtered_data['Close'].mean()
    price_swing = filtered_data['High'].max() - filtered_data['Low'].min()
    
    st.sidebar.metric(label="Average Close Price", value=f"{avg_close:.2f}")
    st.sidebar.metric(label="Max Price Swing (Volatility)", value=f"{price_swing:.2f}")

except FileNotFoundError:
    st.error("Dataset not found. Please make sure your CSV file is named 'crypto_data.csv' and is in the same folder as app.py.")
