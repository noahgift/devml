import os
from subprocess import (Popen, PIPE)

import pandas as pd
from sensible.loginit import logger
log = logger(__name__)

LINES_COUNT="""git ls-files | grep py | while read f; do git blame -w -M -C -C --line-porcelain "$f" | grep \'^author \'; done | sort -f | uniq -ic | sort -n"""

def subdirs(path):
    """Yields a list of subdirectories for a given path"""

    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path,name)):
            full_path = os.path.abspath(os.path.join(path, name))
            sdir_msg = "Found repo: %s" % full_path
            log.info(sdir_msg)
            yield full_path

def line_python(path):
    """Returns a dataframe of churned files in a git repository"""
    
    os.chdir(path) #change directory to process git log
    count_msg = "Running lines/python cmd: [%s] at path [%s]" % (LINES_COUNT, path)
    log.info(count_msg)
    p = Popen(LINES_COUNT, shell=True, stdout=PIPE)
    (line_count, _) = p.communicate()
    return line_count

def clean_line_count_output(out):
    """Clean shell output into list based records"""

    record = []
    count_lines = out.split(b"\n") 
    #import ipdb;ipdb.set_trace()
    for line in count_lines:
        if line:
            line = line.split()
            log.debug(len(line))
            if len(line) == 4:
                count, _, first, last = line
                count = int(count)
                first = first.decode("utf-8")
                last = last.decode("utf-8")
                full_name = f"{first} {last}"
                record.append([count, full_name])
                log.debug(full_name)
            elif len(line) == 3:
                count, _, full_name = line
                count = int(count)
                full_name = full_name.decode("utf-8")
                record.append([count, full_name])
            else:
                log.debug("skipping")
                log.debug(line)
    return record

def output_to_df(record):
    """Converts list of records to DataFrame"""

    df = pd.DataFrame(record, columns=["line_count_python", "author_name"])
    return df

def create_org_df(path):
    """Returns a Pandas Dataframe of an Org"""

    original_cwd = os.getcwd()
    log.info(f"original cwd {original_cwd}")
    all_records = []
    for checkout_dir in subdirs(path):
        log.info(f"Processing path")        
        out = line_python(checkout_dir)
        clean_out = clean_line_count_output(out)
        all_records += clean_out
        new_cwd = os.getcwd()
        cd_msg = "Changing back to original cwd: %s from %s" % (original_cwd, new_cwd)
        log.info(cd_msg)
        os.chdir(original_cwd)
    df = output_to_df(all_records) 
    return df

if __name__ == "__main__":
    test_df = create_org_df("test_dir")
    print(test_df)
