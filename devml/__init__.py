"""
API Example:

from devml import stats, mkdata

path = "/Users/noah/src/wulio/checkout/"
org_df = mkdata.create_org_df(path)
author_counts = stats.author_commit_count(org_df)

"""
__version__ = "0.5"
