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
    if file_name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file,
