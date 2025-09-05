# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title("📈 Trending Product Analyzer")

# uploaded_file = st.file_uploader("Upload CSV", type="csv")

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
    
#     # Clean data: remove rows with missing product
#     df_clean = df.dropna(subset=['flavour_or_product'])
    
#     # Convert datetime
#     df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
    
#     # Show most frequent products
#     st.subheader("🍦 Most Frequently Mentioned Products")
#     freq_counts = df_clean['flavour_or_product'].value_counts().head(10)
#     st.bar_chart(freq_counts)
    
#     # Show trending products (weighted by recency)
#     st.subheader("🔥 Trending Products (Recent Mentions Weighted More)")
    
#     # Calculate weights
#     latest_date = df_clean['datetime'].max()
#     df_clean['days_ago'] = (latest_date - df_clean['datetime']).dt.days
#     df_clean['weight'] = np.exp(-df_clean['days_ago'] / 30)  # decay factor 30 days
    
#     trending = df_clean.groupby('flavour_or_product')['weight'].sum().sort_values(ascending=False).head(10)
#     st.bar_chart(trending)
    
#     # Show raw data
#     st.subheader("📋 Raw Data")
#     st.dataframe(df_clean)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Trending Product Analyzer with Platform Insights")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Clean data: remove rows with missing product
    df_clean = df.dropna(subset=['flavour_or_product'])
    
    # Convert datetime
    df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Niche filter
    niches = ['All'] + sorted(df_clean['niche'].dropna().unique().tolist())
    selected_niche = st.sidebar.selectbox("Select Niche", niches)
    
    # Platform filter
    platforms = ['All'] + sorted(df_clean['social_platform'].dropna().unique().tolist())
    selected_platform = st.sidebar.selectbox("Select Social Platform", platforms)
    
    # Apply filters
    if selected_niche != 'All':
        df_clean = df_clean[df_clean['niche'] == selected_niche]
    if selected_platform != 'All':
        df_clean = df_clean[df_clean['social_platform'] == selected_platform]
    
    if len(df_clean) == 0:
        st.warning("No data available with selected filters!")
    else:
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
        
        # Platform-specific analysis
        st.subheader("📱 Product Trends by Social Platform")
        
        # Group by product and platform
        platform_trends = df_clean.groupby(['flavour_or_product', 'social_platform']).agg({
            'weight': 'sum',
            'datetime': 'count'
        }).reset_index()
        platform_trends.columns = ['product', 'platform', 'trend_score', 'mention_count']
        
        # Show top products per platform
        st.write("**Top Products by Platform (Trend Score)**")
        
        # Create a pivot table for better visualization
        pivot_df = platform_trends.pivot_table(
            index='product', 
            columns='platform', 
            values='trend_score', 
            aggfunc='sum',
            fill_value=0
        )
        
        # Display heatmap-style table
        st.dataframe(pivot_df.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
        
        # Bar chart for each platform
        st.write("**Trending Products per Platform**")
        
        platforms_list = platform_trends['platform'].unique()
        for platform in platforms_list:
            platform_data = platform_trends[platform_trends['platform'] == platform]
            top_products = platform_data.nlargest(5, 'trend_score')
            
            if len(top_products) > 0:
                st.write(f"**{platform}**")
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.barh(top_products['product'], top_products['trend_score'], color='skyblue')
                ax.set_xlabel('Trend Score')
                ax.set_title(f'Top Trending Products on {platform}')
                plt.gca().invert_yaxis()
                st.pyplot(fig)
        
        # Raw data with platform information
        st.subheader("📋 Detailed Data with Platform Info")
        st.dataframe(df_clean[['datetime', 'niche', 'flavour_or_product', 'social_platform', 'country']])
        
        # Download option
        csv = df_clean.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_trending_products.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload a CSV file to get started.")