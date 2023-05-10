import pyodbc
import pandas as pd


# SQL database details
server = 'invoiceparser-sqlserver.database.windows.net'
database = 'invoiceparser-sqldb'
username = 'invoiceparser'
password = "sU3g)2ZUG6FF,N',9u3r"
# Create a connection string
def conn_load_sql():
    conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    # Connect to the database
    conn = pyodbc.connect(conn_string)
    # ----------------------------------------------------------------------------------
    # Extracted data from docs
    df = pd.DataFrame(basic_information)
    df = df["InvoiceId", "VendorName", "InvoiceDate", "InvoiceTotal"]
    # ----------------------------------------------------------------------------------
    # Load the table into your Azure SQL database
    # Name of the existing table to append to
    existing_table = 'invoke_invoice_database'

    # Append the pandas dataframe to the existing table in the Azure SQL database
    df.to_sql(existing_table, conn, index=False, if_exists='append')

