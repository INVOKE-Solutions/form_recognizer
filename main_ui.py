import streamlit as st
from streamlitui.fr_ui import sidebar, parse_button, display_df
from streamlitui.utils import display_image_cached
import pyodbc
import pandas as pd
import pytz
import datetime
import os, sys
from hmac import compare_digest
from hashlib import sha512
from time import sleep

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), "main_project"))
from main_project.main import recognize_this
from main_project.sql_database import conn_load_sql, parse_submitbutton, view_df, dataframeSetup
import numpy as np

def main_streamlit():
    # Force UI to use widemode
    st.title("INVOICE PARSER")

    # SETUP TAB & SIDEBAR
    uploaded_pdf = sidebar()
    st.header("Please review and update(if any) the extracted information before publish")
    status_message = st.empty()
    tab1, tab2 = st.tabs(["Input Data", "View Database"])

    with tab1:
        # Setup columns within the Input Data tab
        col1, col2 = st.columns(2)
        data_container = st.container()
        data_elements = []

        # Uploading files to webapp
        st.session_state["truncated_names"] = []
        if uploaded_pdf:
            for idx, doc in enumerate(uploaded_pdf):
                filename = doc.name
                if len(filename) > 40:
                    filename = filename[:37]+"..."
                st.session_state.get("truncated_names", None).append(filename)
        else:
            status_message.warning("No PDF Uploaded")

        # Generating visual elements for data
        truncated_names = st.session_state.get("truncated_names", False)
        if truncated_names:
            with data_container:
                for idx in range(len(uploaded_pdf)):
                    expander = st.expander(f"See PDF: {truncated_names[idx]}")
                    with expander:
                        data_col1, data_col2 = st.columns(2)
                    data_elements.append((expander, data_col1, data_col2))

        # Displaying parser button and images
        with col1:
            parseButton = parse_button()
            truncated_names = st.session_state.get("truncated_names", False)

            for idx, doc in enumerate(uploaded_pdf):
                with data_elements[idx][0]:
                    with data_elements[idx][1]:
                        st.subheader("Invoice image")
                        images = display_image_cached(doc)
                        st.image(images, use_column_width=True)

        # Parsing uploaded files
        if st.session_state.get("parse_button", False):
            with st.spinner("Parsing..."):
                try:
                    st.session_state["parseInfo"] = []
                    for idx, doc in enumerate(uploaded_pdf):
                        parseInfo = recognize_this(
                            doc_is_url=False, 
                            doc_path=doc.getvalue()
                        )
                        st.session_state["parseInfo"].append(parseInfo)
                    status_message.success("Parsing complete. Click Save Document to save to database.")

                except KeyError:
                    status_message.error("You are not authorized to perform this action")

                except Exception as e:
                    status_message.error("No invoice information detected in your documents.")
                    status_message.warning("Your document might not an invoice document.")
                    raise e

        # Displaying parsed results
        parseInfo = st.session_state.get("parseInfo", False)
        truncated_names = st.session_state.get("truncated_names", False)
        if parseInfo and truncated_names:
            with col2:
                parsesubmitbutton = parse_submitbutton()

            for idx, data in enumerate(parseInfo):
                with data_elements[idx][0]:
                    with data_elements[idx][2]:
                        st.subheader("Invoice extracted details")
                        data_table = st.experimental_data_editor(
                            display_df(parseInfo[idx][0]),
                            key=f"editable_df{idx}",
                            num_rows="dynamic",
                            use_container_width=True
                        )
                        pdf = pd.DataFrame(data_table)
                        pdf = pdf.replace(["None", "none", "", "False"], np.NAN)
                        st.session_state[f"pdf{idx}"] = pdf


        # Saving extracted document data to database
        if st.session_state.get("parse_submitbutton", False):
            for idx in range(len(uploaded_pdf)):
                updatedInfo = st.session_state.get(f"pdf{idx}", False) # boolean
                if updatedInfo is not False:
                    # SQL database details
                    try:
                        df = conn_load_sql(updatedInfo)
                        status_message.success("Load data into database successful. Go to View Database tab to see the database.")
                    except Exception as e: 
                        sqlstate = e.args[0]
                        if '42000' in str(sqlstate):
                            # Handling code for the specific error
                            st.error("DataTypeError: Please make sure InvoiceTotal in number format.")
                        elif '23000' in str(sqlstate):
                            st.error("Invoice number has been used in the database.")
                        elif '22007' in str(sqlstate):
                            st.error("DataTypeError: Please make sure invoiceDate in date format.")
                        else:
                            st.error(f"Other error: {e}")
                        
            with tab2:
                try:
                    df_view = view_df()
                    st.subheader("Invoice database")
                    st.dataframe(df_view)

                    timezone = pytz.timezone('Asia/Kuala_Lumpur')
                    current_time = datetime.datetime.now(timezone)
                    time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    st.download_button(label="Download as CSV", data=df_view.to_csv().encode('utf-8'), 
                                    file_name=f"invoice_database_{time_string}.csv", 
                                    mime='text/csv')
                except Exception as viewdfError:
                    st.error(f"ViewDfError: {viewdfError}")

def main_login():
    if st.session_state.get("login", False):
        return True
    _, col, _ = st.columns([4, 3, 4])
    with col:
        placeholder = st.empty()
        with placeholder.form("login"):
            st.markdown("#### Login")
            password = st.text_input("Password", placeholder="Password", type="password")
            login_button = st.form_submit_button("Login")

            st.session_state["password"] = sha512(bytes(password, "UTF-8")).hexdigest()
            del password

            if login_button:
                if not (compare_digest(bytes(st.session_state.get("password", ""), "UTF-8"),
                                       bytes(st.secrets["LOGIN_KEY"], "UTF-8"))):
                    st.error("Password is incorrect.")
                    return False
                else:
                    placeholder.empty()
                    return True



if __name__ == "__main__":
    st.set_page_config(layout="wide")
    login = main_login()
    if login:
        main_streamlit()