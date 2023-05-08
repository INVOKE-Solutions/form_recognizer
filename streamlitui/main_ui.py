import streamlit as st
from fr_ui import sidebar, parse_button
from utils import displaypdf, display_pdf_to_image
from main_project.main import main

def main_streamlit():
    uploaded_pdf = sidebar()
    if uploaded_pdf:
        for idx, doc in enumerate(uploaded_pdf):
            # displaypdf(file=doc)
            st.write(f"PDF name: {doc.name}")
            with st.expander("See PDF"):
                display_pdf_to_image(file=doc)

        parseButton = parse_button()
        if parseButton:
            with st.spinner("Parsing..."):
                main()


if __name__ == "__main__":
    main_streamlit()