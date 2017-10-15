#!/usr/bin/env python
import os

import click

from devml import state
from devml import fetch_repo
from devml import __version__
from devml import mkdata
from devml import stats
from devml import org_stats
from devml import post_processing

#Creates Defaults From JSON Config
try:
    CHECKOUT_DIR, OATH_TOKEN, ORG = state.get_project_metadata()
except FileNotFoundError:
    click.echo("No project directory with config.json:  project/config.json\n")
    CHECKOUT_DIR = "."
    OATH_TOKEN = "N/A"
    ORG = "N/A"

def create_csv_helper(path, org, csv_dest=None):
    """Helper function for creating csv reports"""

    #If there isn't a destination root, put the csv in the repo
    if csv_dest == None:
        csv_dest = path

    logs = mkdata.create_org_logs(path)
    filename = "%s.csv" % org
    filename_full_path = os.path.join(csv_dest, filename)
    click.echo("Created CSV file Of Github Commits: %s" % filename_full_path)
    mkdata.log_to_csv(filename_full_path, logs)

def org_stats_report_helper(path, json_report_path=None):
    """Organization reports"""

    if json_report_path is None:
        json_report_path = path

    org_df = mkdata.create_org_df(path)
    json_report = org_stats.make_org_report_json(org_df)
    org_stats.write_org_stats_json_to_disk(json_report, json_report_path)

def init_helper(token,org,dest, branch):
    """Helper method for init"""

    #Make folder structure for project on disk
    click.echo("Initializing Project First Time")
    state.create_project_folders(org=org)
    click.echo("Checking out Repo")
    
    #Checkout organization into archive location, i.e. "/mmi/data/projects/pallets/archive"
    if dest == None:
        dest = "/mmi/data/projects/%s/archive/checkout" % org
    
    fetch_repo.clone_org_repos(token, org, 
        dest, branch=branch)

    #Generate Combined CSV File
    click.echo("Creating Combined CSV Log")
    csv_file_root_path = "/mmi/data/projects/%s/logs" % org
    csv_log_msg = "Creating CSV logs in %s" % csv_file_root_path
    click.echo(csv_log_msg)
    create_csv_helper(dest, org, csv_dest=csv_file_root_path)

    #Create Organizational Report
    click.echo("Creating Organizational JSON Report")
    org_report_root_path = "/mmi/data/projects/%s/org" % org
    org_log_msg = "Creating ORG Report %s" % org_report_root_path
    click.echo(org_log_msg)
    org_stats_report_helper(path=dest, json_report_path=org_report_root_path)

    #Create Metadata Report
    click.echo("Creating Metadata JSON Report")
    metadata_report_root_path = "/mmi/data/projects/%s/metadata" % org
    metadata_log_msg = "Creating Metadata Report %s" % org_report_root_path
    click.echo(metadata_log_msg)
    post_processing.write_json_metata_to_disk(path=dest, 
        json_metadata_report_path=metadata_report_root_path)

@click.group()
@click.version_option(__version__)
def cli():
    """Github Machine Learning Tool
    """

@cli.group()
def github():
    """Downloads Repositories From Github"""

@github.command("download")
@click.option("--org", default=ORG, help="Github Organization")
@click.option("--token", default=OATH_TOKEN, help="Github Oath Token")
@click.option("--dest", default=CHECKOUT_DIR, help="Location For Org Checkouts")
@click.option("--branch", default="master", help="Git Branch To Checkout")
def download(token,org,dest, branch):
    """Downloads Github Repositories"""
        
    fetch_repo.clone_org_repos(token, org, 
        dest, branch=branch)

@cli.group()
def csv():
    """CSV Operations"""

@csv.command("create")
@click.option("--path", default=CHECKOUT_DIR, help="Create CSV")
@click.option("--csvname", default=ORG, help="Create CSV Name")
def create(path, csvname):
    """Creates CSV file"""

    create_csv_helper(path, org=csvname)

@cli.group()
def gstats():
    """Generate Stats"""

@gstats.command("author")
@click.option("--path", default=CHECKOUT_DIR, help="path to org")
def author(path):
    """Creates Author Stats

    Example is run after checkout:
    python dml.py gstats author --path /Users/noah/src/wulio/checkout
    """

    org_df = mkdata.create_org_df(path)
    author_counts = stats.author_commit_count(org_df)
    click.echo("Top Commits By Author: %s " % author_counts)

@gstats.command("activity")
@click.option("--path", default=CHECKOUT_DIR, help="path to org")
@click.option("--sort", default="active_days", help="can sorty by:  active_days, active_ratio, active_duration")
def activity(path, sort):
    """Creates Activity Stats

    Example is run after checkout:
    python dml.py gstats activity --path /Users/noah/src/wulio/checkout
    """

    org_df = mkdata.create_org_df(path)
    activity_counts = stats.author_unique_active_days(org_df, sort_by=sort)
    click.echo("Top Unique Active Days: %s " % activity_counts)

@gstats.command("org")
@click.option("--path", default=CHECKOUT_DIR, help="path to org")
def org_stats_report(path):
    """Creates Org Stats and Outputs JSON

    Example is run after checkout:
    python dml.py gstats org --path /Users/noah/src/wulio/checkout
    """
    org_stats_report_helper(path)


@gstats.command("metadata")
@click.option("--path", default=CHECKOUT_DIR, help="path to org")
def metadata_stats_report(path):
    """Creates Metadata Stats and Outputs JSON

    Example is run after checkout:
    python dml.py gstats metadata --path /Users/noah/src/wulio/checkout
    """


    post_processing.write_json_metata_to_disk(path, 
        json_metadata_report_path=path)


if __name__ == '__main__':
    cli()