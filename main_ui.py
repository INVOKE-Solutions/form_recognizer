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

from pdf2image import convert_from_path

def main_streamlit():
    # Force UI to use widemode
    st.set_page_config(layout="wide")

    st.title("INVOICE PARSER")
    # SETUP SIDEBAR & UPLOAD PART
    uploaded_pdf = sidebar()
    st.header("Please review and update(if any) the extracted information before publish")
    parseButton = parse_button()
    # SETUP TAB
    col1, col2 = st.columns(2) #["PDF Uploaded", "Data Parsed"])
    # UPLOAD PROCESS
    if uploaded_pdf:
        status_message = st.empty()
        #parseButton = parse_button()
        for idx, doc in enumerate(uploaded_pdf):
            with col1:
                #with st.expander(f"See PDF: {doc.name[:35]}"):
                st.subheader("Invoice image")
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

                    except KeyError:
                        st.error("You are not authorized to perform this action")

                    except Exception as e:
                        st.error("No invoice information detected in your documents.")
                        st.warning("Your document might not an invoice document.")
                        raise e

                status_message.success("Parsing complete. Click Data Parsed tab.")

            with col2:
                #with st.expander(f"See Data: {doc.name[:35]}"):
                st.subheader("Invoice extracted details")
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
            parsesubmitbutton = parse_submitbutton()
            if parsesubmitbutton:
                updatedInfo = st.session_state.get(f"df{idx}+pdf0", False) # boolean
                #st.write(f"DEBUG {df}")
                #st.dataframe(updatedInfo.set_index("Attribute").T[["InvoiceId", "VendorName", "InvoiceDate", "InvoiceTotal"]])

                if updatedInfo is not False:
                    # SQL database details
                    try:
                        df = conn_load_sql(updatedInfo) 
                        st.write("Load data into database successful")
                        df_view = view_df()
                        st.subheader("Invoice database")
                        st.dataframe(df_view)
                        # st.dataframe(df)
                    except Exception as e1:
                        st.error(f"E1: {e1}")
                    #try:
                        # existing_table = 'invoke_invoice_database'
                        # df.to_sql(existing_table, conn, index=False, if_exists='append')
                        # Close the SQLAlchemy engine object
                        # engine.dispose()
                        # st.write("Load data into database successful")
                        # st.dataframe(df)
                    #except Exception as e2:
                    #    st.error(f"E2: {e2}")
                    # except:
                    #     st.error("Unable to connect to SQL Database.")
                    #     st.warning("Load data into database failed")
    else:
        st.warning("No PDF uploaded.")

if __name__ == "__main__":
    main_streamlit()