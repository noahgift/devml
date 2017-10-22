"""Generate statistics about repos

#TO DO LIST:

http://stackoverflow.com/questions/26489134/whats-the-inverse-of-the-quantile-function-on-a-pandas-series
* Look into T-Score as ranking or Z-Score
* Create large columnar structure something like:
    ** active days, inactivate days, commits total, inserts total, inserts per active day etc.


"""

from pandas import DataFrame
import scipy

from .ts import (unique_days)


def commits_per_day_authors(df):
    """TO..in progress"""

    #group by author_name
    authors = df.groupby("author_name")
    #sum up commits each day
    commits_per_day = authors.resample('D').count()
    return commits_per_day

def author_commit_count(df):

    """
    Returns a Pandas Series sorted by counts of commits

    In [55]: out
    Out[55]: 
    author_name
    Armin Ronacher          5061
    Markus Unterwaditzer    1054
    
    

    """
    author_count = DataFrame({'commits' : df.groupby("author_name"
        ).size().sort_values(ascending=False)}).reset_index()
    return author_count

def author_descriptive_stats_commits(author):
    """Takes a data frame with commit counts"""

    describe = author.commits.describe().to_dict()
    author_commit_median = author.commits.median()
    describe["median"] = author_commit_median
    return describe

def author_percentile_commits(df):
    """Finds the Quantiles For Each Author

    """
    percent = []
    for row in df["commits"]:
        percent.append(
            scipy.stats.percentileofscore(df['commits'],row))
    df['percentile'] = percent
    return df

def author_percentile_of_total(df):
    """Generates % of total commits by author name

    """

    total = df['commits']/df['commits'].sum()
    df['percentage_total'] = total.values.round(2)
    return df


def author_active_days(df):
    """Active Days (Days in which there was a commit)

    This dataframe is return as index such that each column is a date
    in which a commit was created.
    
    Example of how to query this:
    ad = author_active_days(df)
    active_days = ad.loc["Armin Ronacher"].count()
    Out[98]: 960

    """

    active_days = {}
    for name, group in df.groupby("author_name"):
        uday = unique_days(group)
        active_days[name] = uday
    df = DataFrame.from_dict(active_days, orient='index')
    df.index.name = "author_name"
    return df

def author_unique_active_days(df, sort_by="active_days"):
    """DataFrame of Unique Active Days by Author With Descending Order
    
    author_name	unique_days
    46	Armin Ronacher	271
    260	Markus Unterwaditzer	145
    """

    author_list = []
    count_list = []
    duration_active_list = []
    ad = author_active_days(df)
    for author in ad.index:
        author_list.append(author) 
        vals = ad.loc[author]
        vals.dropna(inplace=True)
        vals.drop_duplicates(inplace=True)
        vals.sort_values(axis=0,inplace=True)
        vals.reset_index(drop=True, inplace=True)
        count_list.append(vals.count())
        duration_active_list.append(vals[len(vals)-1]-vals[0])
    df_author_ud = DataFrame()   
    df_author_ud["author_name"] = author_list
    df_author_ud["active_days"] = count_list
    df_author_ud["active_duration"] = duration_active_list
    df_author_ud["active_ratio"] = \
        round(df_author_ud["active_days"]/df_author_ud["active_duration"].dt.days, 2)
    df_author_ud = df_author_ud.iloc[1:] #first row is =
    df_author_ud = df_author_ud.sort_values(by=sort_by, ascending=False)
    return df_author_ud





