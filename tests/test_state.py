from subprocess import call
import os
from devml.state import read_config


#Not worth it for now
# def test_valid_json():
#     """Ensure there is proper JSON"""
#     fname = os.path.join(os.path.dirname(__file__), 'validate-json.sh')
#     print fname
#     out = call(fname, shell=True)
#     assert out == 0
    
def test_read_config():
    fname = os.path.join(os.path.dirname(__file__), 'config.json')
    print(fname)
    actual = read_config(fname)
    assert "project" in list(actual.keys())