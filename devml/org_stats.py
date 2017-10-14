"""
Organizational Stats, more information here:  https://github.com/noahgift/meta_machine_intelligence/blob/master/docs/stats.md
"""
import json

import pandas as pd

from .util import zipped_csv_to_df

from sensible.loginit import logger
log = logger(__name__)

#use default Dataframe if one isn't passed in
DF=zipped_csv_to_df()

def org_commits_by_day(df_raw=DF):
    """Returns all commits with a count and a date index by day"""

    odf_day = df_raw.resample('D').sum()
    return odf_day

def org_inactive_days(odf_day):
    """Returns all inactive days in org history"""

    odf_null = odf_day[odf_day.commits.isnull()]
    return odf_null

def count_org_inactive_days(odf_day):
    """Return count of inactive days in org history"""

    odf_null = org_inactive_days(odf_day)
    return len(odf_null)

def org_active_days(odf_day):
    """Returns all active days in org history"""

    odf_not_null = odf_day[odf_day.commits.notnull()]
    return odf_not_null

def count_org_active_days(odf_day):
    """Return count of active days in org history"""

    odf_not_null = org_active_days(odf_day)
    return len(odf_not_null)

def org_days_since_last_commit(df):
    """Returns the length in days since last commit"""

    today = pd.datetime.today()
    duration = abs((df.index[1]-today).days)
    return duration

def org_duration_from_today(df):
    """Returns the length in days of organization"""

    today = pd.datetime.today()
    duration = abs((df.index[-1]-today).days)
    return duration

def org_active_period(df):
    """Total number of days 'active, i.e. first commit to last commit'"""

    duration = abs((df.index[-1]-df.index[1]).days)
    return duration

def org_cumsum(odf_day):
    """Returns each active day as cumsum formated dict.
    To do create helper function to avoid duplication
    """

    formatted_dict = {}
    active_days = org_active_days(odf_day)
    active_cumsum = active_days.cumsum()
    ac_dict = active_cumsum.to_dict()
    for key,value in list(ac_dict['commits'].items()):
        new_key = key.to_pydatetime().strftime("%Y-%m-%d")
        formatted_dict[new_key] = value
    return formatted_dict

def org_active_days_series(odf_day):
    """Returns each active day as formatted dict
    To do create helper function to avoid duplication
    """

    formatted_dict = {}
    active_days = org_active_days(odf_day).to_dict()
    for key,value in list(active_days['commits'].items()):
        new_key = key.to_pydatetime().strftime("%Y-%m-%d")
        formatted_dict[new_key] = value
    return formatted_dict

def org_inactive_days_series(odf_day):
    """Returns each inactive day as formatted dict
    To do create helper function to avoid duplication
    """

    formatted_dict = {}
    inactive_days = org_inactive_days(odf_day).to_dict()
    for key,_ in list(inactive_days['commits'].items()):
        new_key = key.to_pydatetime().strftime("%Y-%m-%d")
        formatted_dict[new_key] = 0
    return formatted_dict

def org_descriptive_stats_commits(odf_day):
    """Create descriptive stats of active days"""

    active_days = org_active_days(odf_day)
    stats = active_days.describe().to_dict()
    stats['median_per_day'] = float(active_days.median())
    return stats

def make_org_report(df_raw=DF):
    """Create Report for organization"""
    
    odf_day = org_commits_by_day(df_raw)    
    report = {
        "inactive_days_count_days":count_org_inactive_days(odf_day),
        "active_days_count_days": count_org_active_days(odf_day),
        "org_active_period_count_days": org_active_period(odf_day),
        "org_active_days_series": org_active_days_series(odf_day),
        "org_inactive_days_series":org_inactive_days_series(odf_day),
        "commits_cumsum_series": org_cumsum(odf_day),
        "commits_descriptive_stats": org_descriptive_stats_commits(odf_day)
        }
    make_report_msg = "Created Org Report: %s" % report
    log.info(make_report_msg)
    return report

def make_org_report_json(df_raw=DF):
    """Create Report For Organization output as JSON"""

    report = make_org_report(df_raw)
    json_report = json.dumps(report)
    return json_report


def write_org_stats_json_to_disk(report_json, path):
    
    full_path = '%s/org_stats.json' % path
    log_msg = "Writing JSON Org Stats to: %s" % full_path
    log.info(log_msg)
    with open(full_path, 'w') as outfile:
        json.dump(report_json, outfile)









