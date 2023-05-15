import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime

# Create a connection string
def conn_load_sql(updatedInfo):
    # SQL database details
    server = 'invoiceparser-sqlserver.database.windows.net'
    database = 'invoiceparser-sqldb'
    username = 'invoiceparser'
    password = "sU3g)2ZUG6FF,N',9u3r"
    conn_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    # Create a SQLAlchemy engine object
    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_string))
    # Connect to the database
    # conn = pyodbc.connect(conn_string)
    # ----------------------------------------------------------------------------------
    # Extracted data from docs
    # df = pd.DataFrame(updatedInfo)
    df = updatedInfo.copy()
    #print(f'dataframe 1: {df.head()}')
    df = df[["Attribute","Value"]]
    # df = df.loc[df["Attribute"].isin(["InvoiceId", "VendorName", "InvoiceDate", "InvoiceTotal"])].T
    df = df.set_index("Attribute").T
    #print(f'dataframe 2: {df.head()}')
    # df = df[df['Attribute'] != 'Conf']
    #print(f'dataframe 2: {df.head()}')
    df = df[["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal"]]
    current_time = datetime.datetime.now()
    #current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    df.loc["Value","DateCreated"] = current_time
    new_order = ["InvoiceId","VendorName", "InvoiceDate", "InvoiceTotal", 'DateCreated']
    # Reorder the columns using reindex()
    df = df.reindex(columns=new_order)
    #print(f'df.loc[0,"InvoiceDate"] = {df.loc[0,"InvoiceDate"]}')
    #if df.loc[0,"InvoiceDate"] == "":
    #    df.loc[0,"InvoiceDate"] = None
    # print(f'dataframe 3: {df.head()}')
    #print("----------------------------------------------------------------------------")
    #print(f'Datatype---> {type(df.loc[0,"InvoiceDate"])}')
    # ----------------------------------------------------------------------------------
    # Load the table into your Azure SQL database
    # Name of the existing table to append to
    existing_table = 'invoke_invoice_database'
    df.to_sql(existing_table, engine, index=False, if_exists='append')
    engine.dispose()
    return df
    # Append the pandas dataframe to the existing table in the Azure SQL database
    # df.to_sql(existing_table, conn, index=False, if_exists='append')

def parse_submitbutton():
    submitbutton = st.button(
        label="Publish Document",
        key="parse_submitbutton", 
        help="Click to publish the document"
        )
    return submitbutton


def view_df():
    import pyodbc
    # SQL database details
    server = 'invoiceparser-sqlserver.database.windows.net'
    database = 'invoiceparser-sqldb'
    username = 'invoiceparser'
    password = "sU3g)2ZUG6FF,N',9u3r"
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

    # Define the SQL query to retrieve the data from the table
    query = 'SELECT * FROM invoke_invoice_database'

    # Use pandas to read the data from the database into a DataFrame
    df_view = pd.read_sql(query, cnxn)

    return df_view