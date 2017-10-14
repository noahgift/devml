"""
Fetch Repositories From Github
"""

import os

from github import Github
import git
from git import GitCommandError

from sensible.loginit import logger
log = logger("devml")

def auth_github(oath_token):
    
    ghub = Github(oath_token)
    return ghub

def get_org(oath_token, org):

    ghub = auth_github(oath_token)
    org = ghub.get_organization(org)
    return org

def org_repo_names(oath_token, org):
    """"Get Repos for a Github Organization"""
    
    repos = {}
    ghub = get_org(oath_token, org)
    github_repos = ghub.get_repos()
    count = 0
    for repo in github_repos:
        count += 1
        repo_name = repo.name
        repo_path = "git@github.com:%s/%s.git" % (org, repo.name)
        log_msg = "Found Repo # %s REPO NAME: %s , URL: %s " %\
                         (count, repo_name, repo_path)
        log.info(log_msg)
        repos[repo_name] = repo_path  
    return repos

def clone_remote_repo(name, url, dest, branch="master"):

    path = os.path.join(dest, name) #create fully qualified path
    repo = git.Repo.clone_from(url, path, branch=branch)
    return repo

def validate_checkout_root(path):
    """Checks to see if checkout path has been created"""

    if os.path.exists(path):
        log_msg_warning = "Checkout Root Path Already Exists:  %s" % path
        log.warning(log_msg_warning)
        return False
    log_msg_success = "Creating Checkout Root:  %s" % path
    log.info(log_msg_success)
    return True


def clone_org_repos(oath_token, org, dest, branch="master"):
    """Clone All Organizations Repositories and Return Instances of Repos.
    """
    
    if not validate_checkout_root(dest):
        return False

    repo_instances = []
    repos = org_repo_names(oath_token, org)
    count = 0
    for name, url in list(repos.items()):
        count += 1
        log_msg = "Cloning Repo # %s REPO NAME: %s , URL: %s " %\
                         (count, name, url)
        log.info(log_msg)
        try:
            repo = clone_remote_repo(name, url, dest, branch=branch)
            repo_instances.append(repo)
        except GitCommandError:
            log.exception("NO MASTER BRANCH...SKIPPING")
    return repo_instances




