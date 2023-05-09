import streamlit as st
from streamlitui.fr_ui import sidebar, parse_button, display_df
from streamlitui.utils import displaypdf, display_pdf_to_image

import os, sys
from io import StringIO
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "main_project"))
from main_project.main import recognize_this


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
            with tab1:
                with st.expander("See PDF"):
                    display_pdf_to_image(file=doc)

            # PARSING PROCESS
            if parseButton:
                with st.spinner("Parsing..."):
                    parseInfo = recognize_this(
                        doc_is_url=False, 
                        doc_path=doc.getvalue()
                    )
                        
                    with tab2:
                        try:
                            display_df(parseInfo[0])
                            display_df(parseInfo[1])
                        except:
                            st.error("No invoice information detected in your documents.")
                            st.warning("Your document might not an invoice document.")
                        
                st.success("Parsing complete. Click Data Parsed tab.")
    else:
        st.warning("No PDF uploaded.")

if __name__ == "__main__":
    main_streamlit()