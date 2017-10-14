import sys;sys.path.append("..")
from devml import fetch_repo

def test_api():
    ghub = fetch_repo.auth_github("123")
    api = ghub.get_api_status()
    assert api.status == "good"
