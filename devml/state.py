"""Loads Initial State and manages project structure"""

import json
import subprocess
import os

from sensible.loginit import logger
log = logger(__name__)

def read_config(path):
    """Reads in Config File for a Project"""

    with open(path) as data_file:
        data = json.loads(data_file.read())
    return data

def project_metadata(data):
    """Returns project metadata"""

    project = data["project"]
    checkout_dir = project["checkout_dir"]
    oath_token = project["oath"]
    org = project["org"]
    return checkout_dir, oath_token, org

def get_project_metadata(path="project/config.json"):
    """Get metadata from project by selecting path"""

    data = read_config(path)
    checkout_dir, oath_token, org = project_metadata(data)
    return checkout_dir, oath_token, org

def create_project_folders(org):
    """Create the structure for the project on disk """

    project_folders = ["org", "author", "cluster", 
            "metadata", "archive", "logs"]

    root_path = "/mmi/data/projects"
    for folder in project_folders:
        folder_path = os.path.join(root_path, org, folder)
        mkdir_cmd = "mkdir -p %s" % folder_path
        res = subprocess.call([mkdir_cmd], shell=True)
        mkdir_log_msg = "Ran %s with exit status [%s]" % (mkdir_cmd, res)
        log.info(mkdir_log_msg)
    return True
