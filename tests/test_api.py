"""
Integration testing for the api

"""
import zipfile
import shutil
import os

import pytest

from devml import (mkdata, stats)

@pytest.fixture
def setup():
    source = "checkout.zip"
    dest = "/tmp/"
    zip_ref = zipfile.ZipFile(os.path.join(os.path.dirname(__file__),source), 'r')
    zip_ref.extractall(dest)
    path_to_checkout = os.path.join(dest, "checkout")
    yield path_to_checkout
    #delete checkout
    shutil.rmtree(path_to_checkout)

def test_org_df(setup):
    
    path_to_checkout = setup
    org_df = mkdata.create_org_df(path_to_checkout)
    expected_keys = ['author_email', 'commits', 'author_name', 'repo', 'message', 'id']
    actual_keys = list(org_df.to_dict().keys())
    for key in actual_keys:
        assert key in expected_keys

def test_author_commit_count(setup):

    path_to_checkout = setup
    org_df = mkdata.create_org_df(path_to_checkout)
    author_counts = stats.author_commit_count(org_df)
    author_dict = author_counts.to_dict()
    print(author_dict)
    assert 'Armin Ronacher' in list(author_dict["author_name"].values())