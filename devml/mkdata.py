from subprocess import (Popen, PIPE)
import os
import csv
import json

from .ts import (convert_datetime, date_index)

import pandas as pd

from sensible.loginit import logger
log = logger(__name__)

#Git Globals
GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'
GIT_LOG_CMD = 'git log --no-merges --date=local --format="%s"' % GIT_LOG_FORMAT
GIT_UNIQUE_CMD = "git remote -v"
GIT_REPO_NAME =  """basename `git rev-parse --show-toplevel`"""
GIT_CSV_COLUMN_NAMES = ["date","author_email", "author_name",  
                                        "id", "message", "repo"]

def df_from_csv(path):
    df = pd.read_csv(path)
    return df

def df_from_logs(logs):
    df = pd.DataFrame.from_dict(logs)
    return df

def generate_repo_name():
    """Returns short name of git repo"""

    p = Popen(GIT_REPO_NAME, shell=True, stdout=PIPE)
    repo_name = p.stdout.read().strip() 
    log_msg = "Repo Name: %s" % repo_name
    log.info(log_msg)
    return repo_name

def log_to_dict(path, repo_id=None):
    """Converts Git Log To A Python Dict"""
    
    #don't process the same repo twice
    guid = get_git_uid()
    if guid == repo_id:
        guid_true_msg = "guid: %s | repo_id: %s are equal:  SKIP" % (guid, repo_id)
        log.info(guid_true_msg)
        return False, False
    else:
        not_true_msg = "guid: %s" % guid
        log.info(not_true_msg)

    os.chdir(path) #change directory to process git log
    repo_name = generate_repo_name()
    p = Popen(GIT_LOG_CMD, shell=True, stdout=PIPE)
    (git_log, _) = p.communicate()
    try:
        git_log = git_log.decode('utf8').strip('\n\x1e').split("\x1e")
    except UnicodeDecodeError:
        log.exception("utf8 encoding is incorrect, trying ISO-8859-1")
        git_log = git_log.decode('ISO-8859-1').strip('\n\x1e').split("\x1e")
        
    git_log = [row.strip().split("\x1f") for row in git_log]
    git_log = [dict(list(zip(GIT_COMMIT_FIELDS, row))) for row in git_log]
    for dictionary in git_log:
        dictionary["repo"]=repo_name
    repo_msg = "Found %s Messages For Repo: %s" % (len(git_log), repo_name)
    log.info(repo_msg)
    return git_log, guid

def log_df(path):
    """Returns a Pandas DataFrame of git log history"""

    git_log = log_to_dict(path)
    df = pd.DataFrame.from_dict(git_log)
    return df

def log_to_csv(filename, git_log, column_headers=None):
    """Writes python dict of git log to csv file"""
    
    if column_headers is None:
        column_headers = GIT_CSV_COLUMN_NAMES

    with open(filename, mode='w') as outfile:
        fname_msg = "Creating Git Log File: %s" % filename
        log.info(fname_msg)
        writer = csv.writer(outfile)
        writer.writerow(column_headers)
        for row in git_log:
            try:
                writer.writerow([row["date"],row["author_email"], 
                    row["author_name"], row["id"], row["message"], 
                    row["repo"]])
            except KeyError:
                except_msg = "Skipping row: %s" % row
                log.exception(except_msg)
    return filename 

def subdirs(path):
    """Yields a list of subdirectories for a given path"""

    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path,name)):
            full_path = os.path.abspath(os.path.join(path, name))
            sdir_msg = "Found repo: %s" % full_path
            log.info(sdir_msg)
            yield full_path

def create_org_df(path):
    """Returns a Pandas Dataframe of an Org"""

    original_cwd = os.getcwd()
    logs = create_org_logs(path)
    org_df = pd.DataFrame.from_dict(logs)
    #convert date to datetime format
    datetime_converted_df = convert_datetime(org_df)
    #Add A Date Index
    converted_df = date_index(datetime_converted_df)
    new_cwd = os.getcwd()
    cd_msg = "Changing back to original cwd: %s from %s" % (original_cwd, new_cwd)
    log.info(cd_msg)
    os.chdir(original_cwd)
    return converted_df

def create_projectarea_df(ccmServer, projectArea, userId, password):
    """Returns a Pandas DataFrome of change sets delivered to components in a project area"""
    # Get all the users managed by this server, we need this to get the author_email
    columns = ['date', 'id', 'author_name', 'author_email', 'message', 'repo', 'commits']
    # login to EWM CCM
    p = Popen(f'lscm login -r {ccmServer} -u {userId} -P {password}', shell=True, stdout=PIPE)
    resp = p.stdout.read().decode('utf-8')
    if not resp.startswith('Logged in'):
        log.error(f'Cannot login to {ccmServer}')
        return None
    df = pd.DataFrame(columns=columns)
    p = Popen(f'lscm list users  -r {ccmServer} -j', shell=True, stdout=PIPE)
    ewmUsers = json.load(p.stdout)
    users = {user['name']: user['mail'] for user in ewmUsers}
    # get the components in the project area
    p = Popen(f'lscm list components  -r {ccmServer} -j', shell=True, stdout=PIPE)
    components = json.load(p.stdout)
    components = pd.DataFrame.from_dict(components['components']) if components != None else None
    if components is None or len(components) == 0:
        log.info(f'Could not get components in project area: "{projectArea}"')
        return df
    for component in components.name:
        # get all the completed change sets delivered to this component
        p = Popen(f'lscm list changesets  -r {ccmServer} -C "{component}" -j', shell=True, stdout=PIPE)
        changes = None
        try:
            changes = json.load(p.stdout)
            changes = changes['changes'] if changes != None else None
        except:
            continue
        changesDicts = [dict(list(zip(columns, [change['modified'],change['uuid'],change['author'],None,change['comment'],component,None]))) for change in changes]
        df = pd.concat([df, pd.DataFrame.from_dict(changesDicts)])
    df['date'] = pd.to_datetime(df['date'])
    pd.DataFrame.set_index(df, keys='date', drop=True, inplace=True)
    df['author_email'] = df['author_name'].apply(lambda author_name: users[author_name] if author_name in users else None)
    df['commits']=1
    p = Popen(f'lscm logout -r {ccmServer}', shell=True, stdout=PIPE)
    return df



def get_git_uid():
    """
    Uniquely identify git repo:

    https://stackoverflow.com/questions/34874343/
        how-can-i-uniquely-identify-a-git-repository

    This isn't great, used git remote instead
    """
    
    
    p = Popen(GIT_UNIQUE_CMD, shell=True, stdout=PIPE)
    (guid, _) = p.communicate()
    return guid

def create_org_logs(path):
    """Iterate through all paths in current working directory,
    make log dict"""

    combined_log = []
    guid = False
    for sdir in subdirs(path):
        repo_msg = "Processing Repo: %s" % sdir
        log.info(repo_msg)
        git_log, guid2 = log_to_dict(sdir, guid)
        #Only set guid if it isn't False
        if guid2:
            guid = guid2 
        if not git_log:
            msg = "repo already processed: git_log value == [%s]" % git_log
            log.info(msg)
            continue
        else:
            combined_log += git_log
    log_entry_msg = "Found a total log entries: %s" % len(combined_log)
    log.info(log_entry_msg)
    return combined_log
