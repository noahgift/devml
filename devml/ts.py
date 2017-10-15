"""Time Series based methods"""

import pandas as pd

def convert_datetime(df):
    """Converts Git Timestamps to Pandas Datetime"""

    df['date'] = pd.to_datetime(df['date'],format="%a %b %d %X %Y")
    return df

def date_index(df):
    """Create date index for dataframe,
    Also initially seed dataframe with default 1 for commits column

    This gets us the following:
    http://chrisalbon.com/python/pandas_time_series_basics.html

    'View all observations that occured in 2014'
    df['2014']

    'in May 2016'

    """

    df.index = df['date']
    del df['date']
    #adds commits so numerical methods will work on timeseries
    df['commits']=1
    #fill in zeros for dates with NaaN
    #http://stackoverflow.com/questions/13295735/how-can-i-replace-all-the-nan-values-with-zeros-in-a-column-of-a-pandas-datafra
    df.fillna(0)
    return df

def date_range(df):
    """Takes the dataframe returns date range.

    Example here:
    http://pandas.pydata.org/pandas-docs/stable/timeseries.html  
    Returns as Days

    """

    start_date = df.tail(1)['date']
    start = pd.Timestamp.date(list(start_date.to_dict().values())[0])
    end_date = df.head(1)['date']
    end = pd.Timestamp.date(list(end_date.to_dict().values())[0])
    rng = pd.date_range(start, end)
    return rng

def unique_days(df):
    """Determines Unique/Active Days

    Returns a numpy.ndarray
    """

    ud = df.index.map(pd.Timestamp.date).unique()
    return ud

def unique_days_count(nda):
    """Generates a count of the active or unique days in a project

    Returns a numpy.ndarray
    """

    ud = unique_days(nda)
    return len(ud)

def first_day(nda):
    """Returns the First Day"""

    fd = nda[-1]
    return fd

def last_day(nda):
    """Returns the last Day"""

    ld = nda[0]
    return ld

