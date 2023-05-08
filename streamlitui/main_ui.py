import streamlit as st
from fr_ui import sidebar, parse_button, display_df
from utils import displaypdf, display_pdf_to_image
from form_recognizer.main_project.main import main

def main_streamlit():
    # SETUP SIDEBAR & UPLOAD PART
    uploaded_pdf = sidebar()

    # SETUP TAB
    tab1, tab2 = st.tabs(["PDF Uploaded", "Data Parsed"])
    # UPLOAD PROCESS
    if uploaded_pdf:
        parseButton = parse_button()
        for idx, doc in enumerate(uploaded_pdf):
            # displaypdf(file=doc)
            st.write(f"PDF name: {doc.name}")
            with tab1:
                with st.expander("See PDF"):
                    display_pdf_to_image(file=doc)

        # PARSING PROCESS
        if parseButton:
            with st.spinner("Parsing..."):
                parseInfo = main()
                
            with tab2:
                display_df(parseInfo[0])
                display_df(parseInfo[1])
    else:
        st.warning("No PDF uploaded.")

if __name__ == "__main__":
    main_streamlit()