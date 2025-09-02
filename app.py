import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title
st.title("📊 CSV File Analyzer")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display success message
    st.success("File uploaded successfully!")
    
    # Show basic info
    st.subheader("🔍 Data Overview")
    st.write(f"**Number of Rows:** {df.shape[0]}")
    st.write(f"**Number of Columns:** {df.shape[1]}")
    
    # Show the dataframe
    st.subheader("📄 Data Preview")
    st.dataframe(df)
    
    # Show statistics for numeric columns
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())
    
    # Optional: Plot a histogram for a numeric column
    st.subheader("📊 Plot a Histogram")
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_columns:
        selected_column = st.selectbox("Select a numeric column to plot", numeric_columns)
        if selected_column:
            fig, ax = plt.subplots()
            ax.hist(df[selected_column].dropna(), bins=20, edgecolor="black")
            ax.set_xlabel(selected_column)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
    else:
        st.warning("No numeric columns found for plotting.")
else:
    st.info("Please upload a CSV file to get started.")