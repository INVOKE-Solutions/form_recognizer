from fr_ui import sidebar, parse_button

from utils import displaypdf
import streamlit as st
def main():
    uploaded_pdf = sidebar()
    if uploaded_pdf:
        for idx, doc in enumerate(uploaded_pdf):
            displaypdf(file=doc)
        # parse_button()


if __name__ == "__main__":
    main()