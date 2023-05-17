from dotenv import load_dotenv
import pandas as pd
import numpy as np

def enforce_date_format(df:pd.DataFrame, mode:str):
    # Check datatype of date
    try:
        date = re.split("[^0-9]+", df.at["Value", "InvoiceDate"])
        date = [num for num in date if num != ""]
        date = "-".join(date[:3])
        date = pd.to_datetime(date, dayfirst=True)
        df.loc[:, "InvoiceDate"] = date

    except (pd._libs.tslibs.parsing.DateParseError, ValueError):
        match mode
            case "raise":
                raise ValueError("Enter a valid date into the InvoiceDate column")
            case "warn":
                print("Enter a valid date into the InvoiceDate column.")
                return
            case "default":
                df.loc[:, "InvoiceDate"] = np.NAN
            case _:
                raise ValueError(f"{mode} is not a valid mode. Use 'raise', 'warn' or 'default' instead.")

    return df

def configure():
    load_dotenv()