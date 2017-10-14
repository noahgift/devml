"""Common Utilities for Use Within DEVML"""
import pandas as pd

from .ts import (convert_datetime, date_index)

def zipped_csv_to_df(path='ext/data/pallets.csv.zip'):
    """Imports a compressed CSV to DF.
    
    Additionally, preps it for regular usage by adding date index
    """
    

    df = pd.read_csv(path, compression='zip', 
        header=0, sep=',', quotechar='"')
    #convert date to datetime format
    datetime_converted_df = convert_datetime(df)
    #Add A Date Index
    converted_df = date_index(datetime_converted_df)
    return converted_df

def csv_to_df(path):
    """Imports a CSV File to DF"""

    df = pd.read_csv(path,  header=0, sep=',', quotechar='"')
        #convert date to datetime format
    datetime_converted_df = convert_datetime(df)
    #Add A Date Index
    converted_df = date_index(datetime_converted_df)
    return converted_df