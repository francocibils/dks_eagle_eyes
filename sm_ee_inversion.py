import streamlit as st
import pandas as pd
from io import BytesIO

from helper_functions import *


st.title('DKS - Eagle Eyes')
st.header('File upload')
st.markdown('Upload file to obtain Spend for Inbound TV - Eagle Eyes.')

raw_file = st.file_uploader('Upload DKS - Eagle Eyes file', type = ['xlsx', 'xls', 'csv'])

if raw_file is not None:
    file_type = get_file_type(raw_file)
    
    if file_type == 'csv':
        df = pd.read_csv(raw_file, encoding = 'latin-1')
    elif file_type == 'xlsx' or file_type == 'xls':
        df = pd.read_excel(raw_file)
    
    st.success('DKS - Eagle Eyes file uploaded successfully.')

if st.button('Process file'):

    df_processed = process_ee_investment(df)

    st.header('Processed data')
    st.success('DKS files have been processed successfully.')
    
    # Convert the DataFrame to an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine = 'xlsxwriter') as writer:
        df_processed.to_excel(writer, index = False, sheet_name = 'Supermetrics table')
        writer.close()

    # Rewind the buffer
    output.seek(0)

    # Create a download button
    st.download_button(
        label = "Download Excel file",
        data = output,
        file_name = "DKS.xlsx",
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )