import streamlit as st
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
    
    return uploaded_pdf
    
def parse_button():
    parse_button = st.button(
        label="Parse Document",
        key="parse_button", 
        help="Click to parse the document"
        )
    return parse_button



