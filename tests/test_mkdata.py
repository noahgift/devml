import zipfile
import os
import shutil

import pytest
from devml import mkdata


@pytest.fixture
def data():
    checkout_folder = "temp_checkout"
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    os.mkdir(checkout_folder)
    zip_ref.extractall(directory_to_extract_to)
    abs_path = os.path.abspath(checkout_folder)
    yield abs_path
    shutil.rmtree(checkout_folder)

