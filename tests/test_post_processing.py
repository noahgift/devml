import pytest

from devml.post_processing import (files_deleted_match, 
                                        file_ext)

@pytest.fixture
def output():
   res = b'delete mode 100644 tests/test_deprecations.py\n delete mode 100644 scripts/flask-07-upgrade.py\n delete mode 100644 flask/ext/__init__.py\n delete mode 100644 flask/exthook.py\n delete mode 100644 script'
   expected = [b'tests/test_deprecations.py',
            b'scripts/flask-07-upgrade.py',
            b'flask/ext/__init__.py',
            b'flask/exthook.py',
            b'script'] 
   yield res, expected

def test_deleted_match(output):
    res, expected = output
    result = files_deleted_match(res)
    assert result == expected

def test_file_ext(output):
   _, expected = output
   res = []
   expected_extensions = ['.py', '.py', '.py', '.py', '']
   for line in expected:
       res.append(file_ext(line))
   assert res == expected_extensions