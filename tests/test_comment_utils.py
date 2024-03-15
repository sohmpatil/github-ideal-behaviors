import pytest
from utils import comments_utils

@pytest.mark.parametrize("file_name, code, expected", [
    ("test.py", 
    """
    # This is a Python comment
    x = 5 # This is also a comment
    y = 10
    """, 2),
])
def test_get_uncommented_lines(file_name, code, expected):
    assert comments_utils.get_uncommented_lines(file_name, code) == expected