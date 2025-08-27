import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("SCB Data Analyzer")

# Function to process file
def process_file(df):
    # Example: calculate mean current per string
    string_cols = df.columns[1:19]  # B to S (18 strings)
    df["Expected_Current"] = df[string_cols].mean(axis=1)
    comparison = df[string_cols].div(df["Expected_Current"], axis=0)
    return comparison

# Function to plot heatmap with matplotlib
def plot_heatmap(result):
    fig, ax = plt.subplots(figsize=(12, 6))
    cax = ax.matshow(result.T, cmap="coolwarm", aspect="auto")
    fig.colorbar(cax)

    ax.set_xticks(range(len(result.index)))
    ax.set_xticklabels(result.index.strftime("%H:%M"), rotation=90, fontsize=8)
    ax.set_yticks(range(len(result.columns)))
    ax.set_yticklabels(result.columns, fontsize=8)

    st.pyplot(fig)

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
    start_date = st.date_input("Start Date", value=df.inde
