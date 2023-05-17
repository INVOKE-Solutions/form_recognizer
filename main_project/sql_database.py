import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime
import re

# Create a connection string
def conn_load_sql(df_cleaned):
    # SQL database details
    server = st.secrets["SQL_SERVER"]
    database = st.secrets["SQL_DATABASE"]
    username = st.secrets["SQL_USERNAME"]
    password = st.secrets["SQL_PASSWORD"]
    conn_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Create a SQLAlchemy engine object
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_string))
    df = dataframeSetup(df_cleaned)
    # Name of the existing table to append to
    existing_table = 'invoke_invoice_database'
    df.to_sql(existing_table, engine, index=False, if_exists='append')
    engine.dispose()
    return df

def dataframeSetup(updatedInfo):
    df = updatedInfo.copy()
    df = df[["Attribute","Value"]]
    df = df.set_index("Attribute").T
    df = df[["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal", "Currency"]]
    current_time = datetime.datetime.now()
    df.loc["Value","DateCreated"] = current_time
    df["VendorName"] = df['VendorName'].str.upper()
    new_order = ["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal", "Currency", 'DateCreated']

    # Check datatype of date
    try:
        date = re.split("[^0-9]+", df.at["Value", "InvoiceDate"])
        date = [num for num in date if num != ""]
        date = "-".join(date[:3])
        date = pd.to_datetime(date, dayfirst=True)
        df.loc[:, "InvoiceDate"] = date

    except pd._libs.tslibs.parsing.DateParseError:
        raise ValueError("Enter a valid date into the InvoiceDate column")

    except ValueError:
        raise ValueError("Enter a valid date into the InvoiceDate column")

    # Reorder the columns using reindex()
    df_cleaned = df.reindex(columns=new_order)
    return df_cleaned

def parse_submitbutton():
    submitbutton = st.button(
        label="Save Document",
        key="parse_submitbutton", 
        help="Click to publish the document"
        )
    return submitbutton

def view_df():
    import pyodbc
    # SQL database details
    server = st.secrets["SQL_SERVER"]
    database = st.secrets["SQL_DATABASE"]
    username = st.secrets["SQL_USERNAME"]
    password = st.secrets["SQL_PASSWORD"]
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    # Define the SQL query to retrieve the data from the table
    query = 'SELECT * FROM invoke_invoice_database'
    # Use pandas to read the data from the database into a DataFrame
    df_view = pd.read_sql(query, cnxn)
    return df_view