from utils import comments_utils

def test_get_uncommented_lines_python():
    """
    Tests the get_uncommented_lines utility function with Python code.

    This function asserts that the utility correctly identifies the number of uncommented lines
    in a Python code snippet.
    """
    file_name = "test.py"
    code = """
    # This is a Python comment
    x = 5 # This is also a comment
    y = 10
    """
    expected = 2
    assert comments_utils.get_uncommented_lines(file_name, code) == expected

def test_get_uncommented_lines_java():
    """
    Tests the get_uncommented_lines utility function with Java code.

    This function asserts that the utility correctly identifies the number of uncommented lines
    in a Java code snippet.
    """
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
    """
    Tests the get_uncommented_lines utility function with JavaScript code.

    This function asserts that the utility correctly identifies the number of uncommented lines
    in a JavaScript code snippet.
    """
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
    """
    Tests the get_uncommented_lines utility function with C code.

    This function asserts that the utility correctly identifies the number of uncommented lines
    in a C code snippet.
    """
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
    """
    Tests the get_uncommented_lines utility function with HTML code.

    This function asserts that the utility correctly identifies the number of uncommented lines
    in an HTML code snippet.
    """
    code = """
    <!-- This is an HTML comment -->
    <p>Hello, world!</p>
    """
    assert comments_utils.get_uncommented_lines("test.html", code) == 1


def test_invalid_file_extension():
    """
    Tests the get_uncommented_lines utility function with an invalid file extension.

    This function asserts that the utility returns 0 when given a file with an unsupported extension.
    """
    code = "dummy code"
    assert comments_utils.get_uncommented_lines("test.txt", code) == 0

def test_empty_file_extension():
    """
    Tests the get_uncommented_lines utility function with an empty file extension.

    This function asserts that the utility returns 0 when given a file with an empty extension.
    """
    code = "dummy code"
    assert comments_utils.get_uncommented_lines("test", code) == 0

def test_empty_code():
    """
    Tests the get_uncommented_lines utility function with an empty code snippet.

    This function asserts that the utility returns 0 when given an empty code snippet.
    """
    code = ""
    assert comments_utils.get_uncommented_lines("test.py", code) == 0
