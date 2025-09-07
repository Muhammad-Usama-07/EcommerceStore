# # import streamlit as st
# # import pandas as pd
# # import numpy as np

# # st.title("📈 Trending Product Analyzer")

# # uploaded_file = st.file_uploader("Upload CSV", type="csv")

# # if uploaded_file:
# #     df = pd.read_csv(uploaded_file)
    
# #     # Clean data: remove rows with missing product
# #     df_clean = df.dropna(subset=['flavour_or_product'])
    
# #     # Convert datetime
# #     df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
    
# #     # Show most frequent products
# #     st.subheader("🍦 Most Frequently Mentioned Products")
# #     freq_counts = df_clean['flavour_or_product'].value_counts().head(10)
# #     st.bar_chart(freq_counts)
    
# #     # Show trending products (weighted by recency)
# #     st.subheader("🔥 Trending Products (Recent Mentions Weighted More)")
    
# #     # Calculate weights
# #     latest_date = df_clean['datetime'].max()
# #     df_clean['days_ago'] = (latest_date - df_clean['datetime']).dt.days
# #     df_clean['weight'] = np.exp(-df_clean['days_ago'] / 30)  # decay factor 30 days
    
# #     trending = df_clean.groupby('flavour_or_product')['weight'].sum().sort_values(ascending=False).head(10)
# #     st.bar_chart(trending)
    
# #     # Show raw data
# #     st.subheader("📋 Raw Data")
# #     st.dataframe(df_clean)
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# st.title("📈 Trending Product Analyzer with Platform Insights")

# uploaded_file = st.file_uploader("Upload CSV", type="csv")

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
    
#     # Clean data: remove rows with missing product
#     df_clean = df.dropna(subset=['flavour_or_product'])
    
#     # Convert datetime
#     df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
    
#     # Sidebar filters
#     st.sidebar.header("🔍 Filters")
    
#     # Niche filter
#     niches = ['All'] + sorted(df_clean['niche'].dropna().unique().tolist())
#     selected_niche = st.sidebar.selectbox("Select Niche", niches)
    
#     # Platform filter
#     platforms = ['All'] + sorted(df_clean['social_platform'].dropna().unique().tolist())
#     selected_platform = st.sidebar.selectbox("Select Social Platform", platforms)
    
#     # Apply filters
#     if selected_niche != 'All':
#         df_clean = df_clean[df_clean['niche'] == selected_niche]
#     if selected_platform != 'All':
#         df_clean = df_clean[df_clean['social_platform'] == selected_platform]
    
#     if len(df_clean) == 0:
#         st.warning("No data available with selected filters!")
#     else:
#         # Show most frequent products
#         st.subheader("🍦 Most Frequently Mentioned Products")
#         freq_counts = df_clean['flavour_or_product'].value_counts().head(10)
#         st.bar_chart(freq_counts)
        
#         # Show trending products (weighted by recency)
#         st.subheader("🔥 Trending Products (Recent Mentions Weighted More)")
        
#         # Calculate weights
#         latest_date = df_clean['datetime'].max()
#         df_clean['days_ago'] = (latest_date - df_clean['datetime']).dt.days
#         df_clean['weight'] = np.exp(-df_clean['days_ago'] / 30)  # decay factor 30 days
        
#         trending = df_clean.groupby('flavour_or_product')['weight'].sum().sort_values(ascending=False).head(10)
#         st.bar_chart(trending)
        
#         # Platform-specific analysis
#         st.subheader("📱 Product Trends by Social Platform")
        
#         # Group by product and platform
#         platform_trends = df_clean.groupby(['flavour_or_product', 'social_platform']).agg({
#             'weight': 'sum',
#             'datetime': 'count'
#         }).reset_index()
#         platform_trends.columns = ['product', 'platform', 'trend_score', 'mention_count']
        
#         # Show top products per platform
#         st.write("**Top Products by Platform (Trend Score)**")
        
#         # Create a pivot table for better visualization
#         pivot_df = platform_trends.pivot_table(
#             index='product', 
#             columns='platform', 
#             values='trend_score', 
#             aggfunc='sum',
#             fill_value=0
#         )
        
#         # Display heatmap-style table
#         st.dataframe(pivot_df.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
        
#         # Bar chart for each platform
#         st.write("**Trending Products per Platform**")
        
#         platforms_list = platform_trends['platform'].unique()
#         for platform in platforms_list:
#             platform_data = platform_trends[platform_trends['platform'] == platform]
#             top_products = platform_data.nlargest(5, 'trend_score')
            
#             if len(top_products) > 0:
#                 st.write(f"**{platform}**")
#                 fig, ax = plt.subplots(figsize=(10, 4))
#                 ax.barh(top_products['product'], top_products['trend_score'], color='skyblue')
#                 ax.set_xlabel('Trend Score')
#                 ax.set_title(f'Top Trending Products on {platform}')
#                 plt.gca().invert_yaxis()
#                 st.pyplot(fig)
        
#         # Raw data with platform information
#         st.subheader("📋 Detailed Data with Platform Info")
#         st.dataframe(df_clean[['datetime', 'niche', 'flavour_or_product', 'social_platform', 'country']])
        
#         # Download option
#         csv = df_clean.to_csv(index=False)
#         st.download_button(
#             label="Download Filtered Data as CSV",
#             data=csv,
#             file_name="filtered_trending_products.csv",
#             mime="text/csv"
#         )

# else:
#     st.info("Please upload a CSV file to get started.")
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

st.title("📈 Trending Product Analyzer - Time Duration Filters")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Clean data
    df_clean = df.dropna(subset=['flavour_or_product'])
    df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
    latest_date = df_clean['datetime'].max()
    df_clean['days_ago'] = (latest_date - df_clean['datetime']).dt.days
    
    # Sidebar filters
    st.sidebar.header("⏰ Time Duration Filters")
    
    # Time period selection
    time_period = st.sidebar.selectbox(
        "Select Time Period:",
        ["All Time", "Last 7 Days (1 Week)", "Last 14 Days (2 Weeks)", 
         "Last 21 Days (3 Weeks)", "Last 30 Days (1 Month)"]
    )
    
    # Analysis method selection
    analysis_method = st.sidebar.radio(
        "Select Analysis Method:",
        ["Trend Score (Weighted by Recency)", "Raw Mention Count"]
    )
    
    # Niche filter
    niches = ['All'] + sorted(df_clean['niche'].dropna().unique().tolist())
    selected_niche = st.sidebar.selectbox("Select Niche", niches)
    
    # Platform filter
    platforms = ['All'] + sorted(df_clean['social_platform'].dropna().unique().tolist())
    selected_platform = st.sidebar.selectbox("Select Social Platform", platforms)
    
    # Apply time filter
    if time_period == "Last 7 Days (1 Week)":
        filtered_data = df_clean[df_clean['days_ago'] <= 7]
        period_days = 7
    elif time_period == "Last 14 Days (2 Weeks)":
        filtered_data = df_clean[df_clean['days_ago'] <= 14]
        period_days = 14
    elif time_period == "Last 21 Days (3 Weeks)":
        filtered_data = df_clean[df_clean['days_ago'] <= 21]
        period_days = 21
    elif time_period == "Last 30 Days (1 Month)":
        filtered_data = df_clean[df_clean['days_ago'] <= 30]
        period_days = 30
    else:
        filtered_data = df_clean
        period_days = "all"
    
    # Apply niche and platform filters
    if selected_niche != 'All':
        filtered_data = filtered_data[filtered_data['niche'] == selected_niche]
    if selected_platform != 'All':
        filtered_data = filtered_data[filtered_data['social_platform'] == selected_platform]
    
    # Display filter info
    st.sidebar.info(f"📊 Showing data for: {time_period}")
    if period_days != "all":
        st.sidebar.write(f"📅 Period: Last {period_days} days")
    st.sidebar.write(f"📦 Niche: {selected_niche}")
    st.sidebar.write(f"📱 Platform: {selected_platform}")
    st.sidebar.write(f"🔢 Total mentions: {len(filtered_data)}")
    
    if len(filtered_data) == 0:
        st.warning("No data available with selected filters!")
    else:
        # Show timeframe summary
        st.subheader(f"⏰ Analysis Period: {time_period}")
        
        if analysis_method == "Raw Mention Count":
            # Raw count method
            st.subheader("🔢 Raw Mention Count")
            raw_counts = filtered_data['flavour_or_product'].value_counts().head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(raw_counts.index, raw_counts.values, color='lightblue')
            ax.set_xlabel('Number of Mentions')
            ax.set_title(f'Top Products by Mention Count ({time_period})')
            plt.gca().invert_yaxis()
            st.pyplot(fig)
            
            # Platform analysis
            platform_counts = filtered_data.groupby(['flavour_or_product', 'social_platform']).size().reset_index(name='count')
            st.subheader("📱 Platform Distribution")
            
            if len(platform_counts) > 0:
                pivot_df = platform_counts.pivot_table(
                    index='flavour_or_product', 
                    columns='social_platform', 
                    values='count', 
                    aggfunc='sum',
                    fill_value=0
                )
                st.dataframe(pivot_df.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
            
        else:
            # Trend score method
            st.subheader("🔥 Trend Score (Weighted by Recency)")
            
            # Calculate weights with exponential decay based on selected period
            if period_days == "all":
                half_life = 30  # Default for all time
            else:
                half_life = period_days / 4  # Adaptive half-life based on period
            
            filtered_data['weight'] = np.exp(-filtered_data['days_ago'] / half_life)
            
            # Overall trending products
            trending = filtered_data.groupby('flavour_or_product')['weight'].sum().sort_values(ascending=False).head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(trending.index, trending.values, color='lightcoral')
            ax.set_xlabel('Trend Score')
            ax.set_title(f'Top Products by Trend Score ({time_period})')
            plt.gca().invert_yaxis()
            st.pyplot(fig)
            
            # Platform-specific analysis
            platform_trends = filtered_data.groupby(['flavour_or_product', 'social_platform']).agg({
                'weight': 'sum',
                'datetime': 'count'
            }).reset_index()
            platform_trends.columns = ['product', 'platform', 'trend_score', 'total_mentions']
            
            st.subheader("📱 Platform Trends (Weighted Score)")
            if len(platform_trends) > 0:
                pivot_df = platform_trends.pivot_table(
                    index='product', 
                    columns='platform', 
                    values='trend_score', 
                    aggfunc='sum',
                    fill_value=0
                )
                st.dataframe(pivot_df.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
        
        # Time series analysis
        st.subheader("📅 Mentions Over Time")
        
        # Create daily counts
        daily_counts = filtered_data.copy()
        daily_counts['date'] = daily_counts['datetime'].dt.date
        time_series = daily_counts.groupby(['date', 'flavour_or_product']).size().reset_index(name='count')
        
        # Show top 5 products over time
        top_products = filtered_data['flavour_or_product'].value_counts().head(5).index.tolist()
        top_products_data = time_series[time_series['flavour_or_product'].isin(top_products)]
        
        if len(top_products_data) > 0:
            pivot_time = top_products_data.pivot_table(
                index='date', 
                columns='flavour_or_product', 
                values='count', 
                aggfunc='sum',
                fill_value=0
            )
            
            fig, ax = plt.subplots(figsize=(12, 6))
            for product in pivot_time.columns:
                ax.plot(pivot_time.index, pivot_time[product], marker='o', label=product, linewidth=2)
            
            ax.set_xlabel('Date')
            ax.set_ylabel('Daily Mentions')
            ax.set_title('Daily Mentions of Top Products')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Raw data preview
        with st.expander("📋 View Filtered Data"):
            st.dataframe(filtered_data[['datetime', 'niche', 'flavour_or_product', 'social_platform', 'country', 'days_ago']])
        
        # Download option
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"trending_products_{time_period.replace(' ', '_').lower()}.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload a CSV file to get started.")