"""
Post processing utilities for dealing with git repos

#All file's changed with counts
git log --name-only --pretty=format: | sort | uniq -c | sort -nr

See this:
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/icse05churn.pdf

"""
import os

from subprocess import (Popen, PIPE)
from collections import Counter

import pandas as pd
import numpy as np

from sensible.loginit import logger
log = logger(__name__)

from .mkdata import subdirs

#Git Globals
CHURN_GIT_CMD = "git log --name-only --pretty=format:"

def git_churn_df(path):
    """Returns a dataframe of churned files in a git repository"""
    
    os.chdir(path) #change directory to process git log
    churn_msg = "Running churn cmd: [%s] at path [%s]" % (CHURN_GIT_CMD, path)
    log.info(churn_msg)
    p = Popen(CHURN_GIT_CMD, shell=True, stdout=PIPE)
    (git_churn, _) = p.communicate()
    #Use fancy counter, but convert back to a dict
    churn_count = dict(Counter(git_churn.split()))
    df = pd.DataFrame(list(churn_count.items()),columns=["files", "churn_count"])
    return df

def file_len(fname):
    """Count lines in file else return np.nan if file doesn't exist"""

    if os.path.isfile(fname):
        with open(fname) as f:
            i = 1
            for i, _ in enumerate(f):
                pass
        return i + 1
    return np.nan

def git_populate_file_metatdata(df):
    """For all of the files found in git metadata, generate data about them"""


    df['line_count'] = df['files'].apply(file_len)
    df['relative_churn'] = df['churn_count']/df['line_count']
    #finally, sort and create new index
    df_sorted = df.sort_values(["churn_count", "relative_churn"], ascending=[False, False])
    df_sorted.index = list(range(1,len(df_sorted) + 1))
    return df_sorted

def write_json_metata_to_disk(path, json_metadata_report_path):
    """Writes metadata to disk"""

    for sdir in subdirs(path):
        repo_msg = "Processing Repo: %s" % sdir
        log.info(repo_msg)
        df = git_churn_df(sdir)
        df_metadata = git_populate_file_metatdata(df)
        json_report = df_metadata.to_json()
        repo_name = sdir.split("/")[-1]
        json_path = "%s/%s_metadata.json" % (json_metadata_report_path, repo_name)
        log_msg = "JSON Report Path: %s" % json_path
        log.info(log_msg)
        with open(json_path, 'w') as outfile:
            outfile.write(json_report)
