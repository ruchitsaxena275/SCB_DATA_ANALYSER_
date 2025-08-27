import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("SCB Data Analyzer")

# Function to process file
def process_file(df):
    # Example: calculate mean current per string
    string_cols = df.columns[1:19]  # B to S (18 strings)
    df["Expected_Current"] = df[string_cols].mean(axis=1)
    comparison = df[string_cols].div(df["Expected_Current"], axis=0)
    return comparison

# Function to plot heatmap
def plot_heatmap(result):
    plt.figure(figsize=(12, 6))
    sns.heatmap(result, cmap="coolwarm", cbar=True)
    st.pyplot(plt)

# File uploader
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    file_name = uploaded_file.name

    # Read file
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        if "Timestamp" in df.columns:  # if a timestamp column exists
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
            df = df.set_index("Timestamp")
        else:
            st.error("No Timestamp column found. Please include one in your data.")
            st.stop()

    # Date filter
    start_date = st.date_input("Start Date", value=df.index.min().date())
    end_date = st.date_input("End Date", value=df.index.max().date())
    df = df.loc[str(start_date):str(end_date)]

    # Fixed time filter (07:00–19:00)
    df = df.between_time("07:00", "19:00")

    # Processing
    result = process_file(df)

    # Plot heatmap
    st.subheader("Heatmap of String Current Comparison")
    plot_heatmap(result)

    # Preview processed data
    st.subheader("Preview of Processed Data")
    st.dataframe(result.head())
