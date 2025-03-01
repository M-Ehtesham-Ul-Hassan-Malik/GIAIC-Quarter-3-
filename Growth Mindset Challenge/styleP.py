import pandas as pd
import numpy as np
import scipy.stats as stats
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import os

# Set up Streamlit app
st.set_page_config(page_title='Data Sweeper', layout='wide')

# Hero Section with Styling
st.markdown(
    """
    <div style="text-align: center; padding: 30px; background-color: #0e76a8; color: white; border-radius: 10px;">
        <h1 style="margin-bottom: 5px;">The Data Doctor</h1>
        <h3>Your Data Physician – No More Messy Spreadsheets!</h3>
        <p>Transform your CSV and Excel files with built-in data cleaning and visualization.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for DataFrames and raw file data
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}
if 'raw_files' not in st.session_state:
    st.session_state.raw_files = {}

# Upload multiple files
uploaded_files = st.file_uploader('Upload your files here:', type=['csv', 'xlsx'], accept_multiple_files=True)

# Process new files and store raw bytes
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.raw_files:
            st.session_state.raw_files[file.name] = file.getvalue()
            
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(BytesIO(file.getvalue()))
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(BytesIO(file.getvalue()))
                else:
                    continue
                st.session_state.dataframes[file.name] = df
            except Exception as e:
                st.error(f"Error reading {file.name}: {str(e)}")

# Process each file's data
for file_name, df in st.session_state.dataframes.items():
    st.subheader(f'🛠 Data Cleaning for {file_name}')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f'Remove Duplicates - {file_name}'):
            df = df.drop_duplicates()
            st.session_state.dataframes[file_name] = df
            st.success(f"Removed duplicates from {file_name}")
    
    with col2:
        if st.button(f'Handle Missing Values - {file_name}'):
            df.fillna(df.select_dtypes(include='number').mean(), inplace=True)
            st.session_state.dataframes[file_name] = df
            st.success("Filled missing values with column means")
    
    with col3:
        if st.button(f'Detect and Remove Outliers - {file_name}'):
            numeric_cols = df.select_dtypes(include='number').columns
            if not numeric_cols.empty:
                z_scores = np.abs(stats.zscore(df[numeric_cols]))
                df = df[(z_scores < 3).all(axis=1)]
                st.session_state.dataframes[file_name] = df
                st.success(f"Outliers removed for {file_name}")
            else:
                st.warning("No numeric columns found for outlier detection")

    st.subheader(f'📌 Select Columns for {file_name}')
    selected_columns = st.multiselect("Choose columns to keep:", options=df.columns.tolist(), default=df.columns.tolist(), key=f"cols_{file_name}")
    if selected_columns:
        df = df[selected_columns]
        st.session_state.dataframes[file_name] = df

    st.subheader(f'Cleaned Data Preview: {file_name}')
    st.dataframe(df.head())

    # --- Visualization Section ---
    st.subheader(f'Data Visuals for {file_name}')
    if st.checkbox(f'Show visualizations for {file_name}', key=f"viz_{file_name}"):
        numeric_data = df.select_dtypes(include='number')
        if not numeric_data.empty:
            columns_to_plot = st.multiselect("Select columns to visualize:", options=numeric_data.columns.tolist(), default=numeric_data.columns.tolist()[:2], key=f"viz_cols_{file_name}")
            if columns_to_plot:
                st.write("### Bar Chart")
                st.bar_chart(numeric_data[columns_to_plot])
                
                st.write("### Line Chart")
                st.line_chart(numeric_data[columns_to_plot])
                
                st.write("### Histogram")
                for col in columns_to_plot:
                    st.write(f"**{col}**")
                    st.bar_chart(numeric_data[col].value_counts())
                
                if len(columns_to_plot) >= 2:
                    st.write("### Scatter Plot")
                    fig, ax = plt.subplots()
                    colors = sns.color_palette("husl", len(columns_to_plot))
                    for i, col in enumerate(columns_to_plot[1:]):
                        ax.scatter(numeric_data[columns_to_plot[0]], numeric_data[col], label=col, color=colors[i])
                    ax.set_xlabel(columns_to_plot[0])
                    ax.set_ylabel("Values")
                    ax.legend()
                    st.pyplot(fig)
                
                st.write("### Box Plot (Outlier Detection)")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(data=numeric_data[columns_to_plot], ax=ax, palette="coolwarm")
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                st.pyplot(fig)
            else:
                st.warning("Select at least one column for visualization.")
        else:
            st.warning("No numeric columns available for visualization.")
    
    st.subheader(f'🔄 Download Processed {file_name}')
    export_format = st.radio("Choose export format:", ["CSV", "Excel"], key=f"format_{file_name}")
    if st.button(f"Export {file_name}"):
        buffer = BytesIO()
        base_name = os.path.splitext(file_name)[0]
        if export_format == "CSV":
            df.to_csv(buffer, index=False)
            mime = "text/csv"
            ext = ".csv"
        else:
            df.to_excel(buffer, index=False)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ext = ".xlsx"
        buffer.seek(0)
        st.download_button(label=f"Download {export_format}", data=buffer, file_name=f"cleaned_{base_name}{ext}", mime=mime)
