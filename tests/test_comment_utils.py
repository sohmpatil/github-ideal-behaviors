from utils import comments_utils

def test_get_uncommented_lines_python():
    file_name = "test.py"
    code = """
    # This is a Python comment
    x = 5 # This is also a comment
    y = 10
    """
    expected = 2
    assert comments_utils.get_uncommented_lines(file_name, code) == expected

def test_get_uncommented_lines_java():
    file_name = "test.java"
    code = """
    // This is a Java comment
    /*
    Multiline comment
    */
    int x = 5; // This is also a comment
    int y = 10;
    """
    expected = 2
    assert comments_utils.get_uncommented_lines(file_name, code) == expected

def test_get_uncommented_lines_javascript():
    file_name = "test.js"
    code = """
    // This is a Java  Script comment
    /* Multiline comment
    */
    var x = 5; // This is also a comment
    var y = 10;
    """
    expected = 2
    assert comments_utils.get_uncommented_lines(file_name, code) == expected

def test_get_uncommented_lines_c():
    file_name = "test.c"
    code = """
    // This is a Java  Script comment
    /* Multiline comment
    */
    int x = 5; /* Comment */
    float y = 10.0;
    """
    expected = 2
    assert comments_utils.get_uncommented_lines(file_name, code) == expected

def test_get_uncommented_lines_html():
    code = """
    <!-- This is an HTML comment -->
    <p>Hello, world!</p>
    """
    assert comments_utils.get_uncommented_lines("test.html", code) == 1


def test_invalid_file_extension():
    code = "dummy code"
    assert comments_utils.get_uncommented_lines("test.txt", code) == 0

def test_empty_file_extension():
    code = "dummy code"
    assert comments_utils.get_uncommented_lines("test", code) == 0

def test_empty_code():
    code = ""
    assert comments_utils.get_uncommented_lines("test.py", code) == 0