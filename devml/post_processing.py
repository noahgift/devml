"""
Post processing utilities for dealing with git repos

#All file's changed with counts
git log --name-only --pretty=format: | sort | uniq -c | sort -nr

See this:
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/icse05churn.pdf

"""
import os
from pathlib import Path
from subprocess import (Popen, PIPE)
from collections import Counter
import re

import pandas as pd
from pandas import DataFrame
import numpy as np

from sensible.loginit import logger
log = logger(__name__)

from .mkdata import subdirs

#Git Globals
CHURN_GIT_CMD = "git log --name-only --pretty=format:"
AUTHOR_CHURN_CMD =\
 'git log --follow --no-merges --pretty=format:"Commit Hash: %H, Author: %aN, Date: %aD"'

FILES_DELETED_CMD=\
    'git log --diff-filter=D --summary | grep delete'

def files_deleted_match(output):
    """Retrieves files from output from subprocess
    
    i.e: 
    wcase/templates/hello.html\n delete mode 100644 
    Throws away everything but path to file
    """

    files = []
    integers_match_pattern = '^[-+]?[0-9]+$'
    for line in output.split():
        if line == b"delete":
            continue
        elif line == b"mode":
            continue
        elif re.match(integers_match_pattern, line.decode("utf-8")):
            continue
        else:
            files.append(line)
    return files

def git_deleted_files(path):
    """Finds deleted files"""

    os.chdir(path) #change directory to process git log
    del_msg = "Running del cmd: [%s] at path [%s]" % (FILES_DELETED_CMD, path)
    log.info(del_msg)
    p = Popen(FILES_DELETED_CMD, shell=True, stdout=PIPE)
    (git_deleted, _) = p.communicate()
    files = files_deleted_match(git_deleted)
    df = pd.DataFrame(files, columns=["files"])
    df["ext"] = df['files'].apply(file_ext)
    return df

def file_decode(file, decode_type="utf-8"):
    """decode binary files"""

    file = file.decode(decode_type)
    return file

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
        with open(fname, 'rb') as f:
            i = 1
            for i, _ in enumerate(f):
                pass
        return i + 1
    return np.nan

def file_ext(fname):
    """Gets file extension"""

    ext = Path(str(fname)).suffix.strip("'")
    return ext

def retrieve_churn_by_authors(fname):
    """Author churn counts by file"""

    fname = fname.decode("ASCII") #ensure not binary
    fname_cmd = "{AUTHOR_CHURN_CMD} {fname}".format(AUTHOR_CHURN_CMD=AUTHOR_CHURN_CMD,
                                                    fname=fname)    
    churn_msg = "Running churn cmd: [%s] at path [%s]" % (fname_cmd, os.getcwd())
    log.info(churn_msg)
    p = Popen(fname_cmd, shell=True, stdout=PIPE)
    (git_churn, _) = p.communicate()
    git_log = git_churn.decode('utf8').strip('\n\x1e').split("\x1e")
    git_log = [row.strip().split("\x1f") for row in git_log]
    git_log = git_log[0][0].split(",")
    cnt = Counter()
    for line in git_log:
        if "Author" in line:
            _,name = line.split(":")
            name = name.strip()
            cnt[name] += 1 
    return dict(cnt)

def author_churn_df(df):
    """Creates churn for all files by authors"""

    files = []
    data = []
    df_metadata = git_populate_file_metatdata(df)
    for file in df_metadata['files']:
        files.append(file.decode("ASCII"))
        data.append(retrieve_churn_by_authors(file))
        df = DataFrame.from_dict(data, orient='columns', dtype=None)    
        df['files'] = files
    return df

def git_populate_file_metatdata(df):
    """For all of the files found in git metadata, generate data about them"""

    df['line_count'] = df['files'].apply(file_len)
    df['extension'] = df['files'].apply(file_ext)
    df['relative_churn'] = round(df['churn_count']/df['line_count'],2)
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
