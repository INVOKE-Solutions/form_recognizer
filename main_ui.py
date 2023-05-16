import streamlit as st
from streamlitui.fr_ui import sidebar, parse_button, display_df
from streamlitui.utils import display_image_cached
import pyodbc
import pandas as pd
import re

import os, sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "main_project"))
from main_project.main import recognize_this
from main_project.sql_database import conn_load_sql, parse_submitbutton, view_df
from streamlit.components.v1 import html

from pdf2image import convert_from_path

def main_streamlit():
    # Force UI to use widemode
    st.set_page_config(layout="wide")
    st.title("INVOICE PARSER")

    # SETUP TAB & SIDEBAR
    uploaded_pdf = sidebar()
    st.header("Please review and update(if any) the extracted information before publish")
    status_message = st.empty()
    tab1, tab2 = st.tabs(["Input Data", "View Database"])

    with tab1:
        # SETUP COLUMNS & UPLOAD PART
        col1, col2 = st.columns(2)

        # UPLOAD PROCESS
        if uploaded_pdf:
            parseButton = parse_button()
            st.subheader("Invoice extracted details")
            for idx, doc in enumerate(uploaded_pdf):
                if len(doc.name) > 40:
                    truncated_name = doc.name[:37] + "..."
                else:
                    truncated_name = doc.name[:40]

                with col1:
                    with st.expander(f"See PDF: {truncated_name}"):
                        st.subheader("Invoice image")
                        images = display_image_cached(doc)
                        st.image(images, use_column_width=True)

                # PARSING PROCESS
                if parseButton:
                    with st.spinner("Parsing..."):
                        try:
                            parseInfo = recognize_this(
                                doc_is_url=False, 
                                doc_path=doc.getvalue()
                            )
                            st.session_state[f"parseInfo{idx}"] = parseInfo

                        except KeyError:
                            status_message.error("You are not authorized to perform this action")

                        except Exception as e:
                            status_message.error("No invoice information detected in your documents.")
                            status_message.warning("Your document might not an invoice document.")
                            raise e

                        status_message.success("Parsing complete. Click Data Parsed tab.")

                    with col2:
                        parsesubmitbutton = parse_submitbutton()
                        with st.expander(f"See Data: {truncated_name}"):
                            parseInfo = st.session_state.get(f"parseInfo{idx}", False)
                            if parseInfo:
                                print(parseInfo[0])
                                for ix, data in enumerate(parseInfo):
                                    df = display_df(data)
                                    data_table = st.experimental_data_editor(
                                        df,
                                        key=f"editable_df{ix}_{idx}",
                                        num_rows="dynamic",
                                        use_container_width=True
                                    )
                                    st.session_state[f'df{ix}+pdf{idx}'] = pd.DataFrame(data_table)
                                    break
                            else:
                                pass

                if st.session_state.get("parse_submitbutton", False):
                    updatedInfo = st.session_state.get(f"df{idx}+pdf0", False) # boolean

                    if updatedInfo is not False:
                        parsesubmitbutton = parse_submitbutton()

                        # SQL database details
                        try:
                            df = conn_load_sql(updatedInfo) 
                            st.write("Load data into database successful")
                            df_view = view_df()
                            st.subheader("Invoice database")
                            st.dataframe(df_view)
                        except Exception as e1:
                            st.error(f"E1: {e1}")
        else:
            st.warning("No PDF uploaded.")

if __name__ == "__main__":
    main_streamlit()