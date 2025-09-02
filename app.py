import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 Trending Product Analyzer")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Clean data: remove rows with missing product
    df_clean = df.dropna(subset=['flavour_or_product'])
    
    # Convert datetime
    df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
    
    # Show most frequent products
    st.subheader("🍦 Most Frequently Mentioned Products")
    freq_counts = df_clean['flavour_or_product'].value_counts().head(10)
    st.bar_chart(freq_counts)
    
    # Show trending products (weighted by recency)
    st.subheader("🔥 Trending Products (Recent Mentions Weighted More)")
    
    # Calculate weights
    latest_date = df_clean['datetime'].max()
    df_clean['days_ago'] = (latest_date - df_clean['datetime']).dt.days
    df_clean['weight'] = np.exp(-df_clean['days_ago'] / 30)  # decay factor 30 days
    
    trending = df_clean.groupby('flavour_or_product')['weight'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(trending)
    
    # Show raw data
    st.subheader("📋 Raw Data")
    st.dataframe(df_clean)