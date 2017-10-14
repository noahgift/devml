"""Author level stats"""

from .util import zipped_csv_to_df

#use default Dataframe if one isn't passed in
DF=zipped_csv_to_df()
        
def author_daily_commits(df_raw=DF):
    """Takes a data indexed dataframe
    creates a author groupby commit counts per day

    """

    dfa = df_raw.groupby("author_name").resample('D').sum()
    dfa = dfa.fillna(0)
    return dfa