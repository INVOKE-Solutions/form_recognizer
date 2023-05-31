import streamlit as st
import pandas as pd
from typing import Dict
# SIDEBAR
def sidebar():
    sidebar = st.sidebar
    sidebar.write("Invoice Parser")
    uploaded_pdf = sidebar.file_uploader(
        label="Upload your PDF here (size < 4 MB)", 
        type="pdf", 
        accept_multiple_files=True, 
        key="pdf_upload"
    )
    if uploaded_pdf:
        progress_bar = sidebar.progress(len(uploaded_pdf) + (100-len(uploaded_pdf)))
        sidebar.success("File successfully uploaded.")
    
    return uploaded_pdf
    
def parse_button():
    parse_button = st.button(
        label="Parse Document",
        key="parse_button", 
        help="Click to parse the document"
        )
    return parse_button

def display_df(data:Dict):
    df = pd.DataFrame(data)
    df = df[df['Attribute'].isin(["InvoiceId", "VendorName", "InvoiceDate", "InvoiceTotal", "Currency"])]
    attribute = df["Attribute"].to_list()
    col = ["InvoiceId", "VendorName", "InvoiceDate", "InvoiceTotal", "Currency", "InvoiceCategory"]
    for i in col:
        if i in attribute:
            pass
        else:
            new_row = {'Attribute': i, 'Value': None, 'Conf': 0}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    #df = df.loc[df["Conf"].notna()]
    df = df.reset_index(drop=True)
    return df