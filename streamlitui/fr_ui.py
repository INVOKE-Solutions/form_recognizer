import streamlit as st
import time


# SIDEBAR

def sidebar():
    sidebar = st.sidebar
    sidebar.write("Invoice Parser")
    uploaded_pdf = sidebar.file_uploader(
        label="Upload your PDF here", 
        type="pdf", 
        accept_multiple_files=True, 
        key="pdf_upload"
    )
    if uploaded_pdf:
        progress_bar = sidebar.progress(len(uploaded_pdf) + (100-len(uploaded_pdf)))
        sidebar.success("File successfully uploaded.")



if __name__ == "__main__":
    sidebar()

