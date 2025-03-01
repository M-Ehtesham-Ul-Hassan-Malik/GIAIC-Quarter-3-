import pandas as pd
import streamlit as st
from io import BytesIO
import os

# Ensure 'st.title' is not reassigned anywhere above

# Setting up the app
st.set_page_config(page_title='Data Sweeper', layout='wide') 

st.title("Data Sweeper")
st.write("Transform your CSV and Excel files with built-in data cleaning and visualization")

# Load CSV file

files = st.file_uploader('upload your files here: ', type=['csv', 'xlsx'], accept_multiple_files=True)

if files:
    for file in files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.write(f"Error: {file.name} is not a valid CSV or Excel file.")
            continue

# Display info about the files
st.write(f'File names: {file.name}')
st.write(f'File size: {file.size}')

# Display the first 5 rows of the dataframe
st.write("Head of the Dataframe")
st.dataframe(df.head())

# Options for the data cleaning

st.subheader('Data Cleaning Options')
if st.checkbox(f'Clean Data for {file.name}'):
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f'Remove duplicates for {file.name}'):
            df.drop_duplicates(inplace=True)
            st.write(f'Duplicates removed for {file.name}')
        # if st.button(f'Handle missing values for {file.name}'):
        #     df.fillna(df.mean(), inplace=True)
        #     st.write(f'Missing values handled for {file.name}')
        # if st.button(f'Convert data types for {file.name}'):
        #     df = df.apply(lambda x: x.astype('category'))
        #     st.write(f'Data types converted for {file.name}')
        # if st.button(f'Outlier detection for {file.name}'):
        #     import scipy.stats as stats
        #     df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
        #     st.write(f'Outliers removed for {file.name}')
        # if st.button(f'Save cleaned data for {file.name}'):
        #     buffer = BytesIO()
        #     df.to_csv(buffer, index=False)
        #     buffer.seek(0)
        #     st.download_button(label=f'Download Cleaned Data for {file.name}', data=buffer, file_name=f'cleaned_{file.name}')
        #     st.success(f'Cleaned data saved for {file.name}')
        

    with col2:
        if st.button(f'Handle missing values for {file.name}'):
            num_col = df.select_dtypes(include=['number']).columns
            df[num_col] = df[num_col].fillna(df[num_col].mean())
            st.write(f'Missing values handled for {file.name}')


# Choose specific columns to keep or convert
st.subheader('Select columns to Convert')
columns = st.multiselect(f'Chose columns for {file.name}', df.columns, default=df.columns)
df = df[columns]

# Create some visualizations
st.subheader('Data Visuals')
if st.checkbox(f'Show visualization for {file.name}'):
    st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])




# convertion options
st.subheader('Conversion Options')
convertion_type = st.radio(f'Convert {file.name} to :'['CSV', 'Excel'], key=file.name)
if st.button(f'Convert "{file.name}'):
    buffer = BytesIO()
    if convertion_type == 'CSV':
        df.to_csv(buffer, index=False)
        file_name = file.name.replace(file_ext, '.csv')
        mime_type = 'text/csv'

    elif convertion_type == 'Excel':
        df.to_excel(buffer, index=False)
        file_name = file.name.replace(file_ext, '.xlsx')
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    buffer.seek(0)

# Download Button
    st.download_button(
        label=f'Download {file_name} as {convertion_type}',
        data=buffer, 
        file_name=file_name,
        mimetype=mime_type
        )
    st.success('All files processed successfully!') 

# clean_options = {
#     'Remove duplicates': df.drop_duplicates(),
#     'Handle missing values': df.dropna(),
#     'Fill missing values': df.fillna(df.mean()),
#     'Convert data types': df.apply(lambda x: x.astype('category')),
#     'Outlier detection': df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
# }