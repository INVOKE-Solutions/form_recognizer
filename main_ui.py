import streamlit as st
from streamlitui.fr_ui import sidebar, parse_button, display_df
from streamlitui.utils import display_image_cached

import os, sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "main_project"))
from main_project.main import recognize_this

from pdf2image import convert_from_path

def main_streamlit():
    # SETUP SIDEBAR & UPLOAD PART
    uploaded_pdf = sidebar()

    # SETUP TAB
    col1, col2 = st.columns(2) #["PDF Uploaded", "Data Parsed"])
    # UPLOAD PROCESS
    if uploaded_pdf:
        parseButton = parse_button()
        for idx, doc in enumerate(uploaded_pdf):
            with col1:
                with st.expander(f"See PDF"):
                    images = display_image_cached(doc)
                    for page in images:
                        st.image(page, use_column_width=True)

            # PARSING PROCESS
            if parseButton:
                with st.spinner("Parsing..."):
                    try:
                        parseInfo = recognize_this(
                            doc_is_url=False, 
                            doc_path=doc.getvalue()
                        )
                        st.session_state[f"parseInfo{idx}"] = parseInfo
                    except:
                        st.error("No invoice information detected in your documents.")
                        st.warning("Your document might not an invoice document.")
                st.success("Parsing complete. Click Data Parsed tab.")

            with col2:
                with st.expander(f"See Data"):
                    parseInfo = st.session_state.get(f"parseInfo{idx}", False)
                    if parseInfo:
                        st.write(f"PDF {idx+1}")
                        for ix, df in enumerate(parseInfo):
                            st.experimental_data_editor(
                                display_df(df),
                                key=f"editable_df{ix}_{idx}",
                                use_container_width=True
                            )

    else:
        st.warning("No PDF uploaded.")

if __name__ == "__main__":
    main_streamlit()