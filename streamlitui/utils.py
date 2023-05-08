import streamlit as st
import base64

def displaypdf(file: st.runtime.uploaded_file_manager.UploadedFile):
    bytes_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{bytes_pdf}" width="600" height="400" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)