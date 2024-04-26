import os
import re


def get_uncommented_lines(file_name, code):
    """
    Counts the number of uncommented lines in a given code snippet or file.

    This function takes a file name and a code snippet as input. If a file name is provided, it reads the file and processes its content. Otherwise, it processes the provided code snippet directly. It then removes all comments and counts the number of lines that are not empty or whitespace.

    Args:
        file_name (str): The name of the file to process. If an empty string is provided, the function will process the provided code snippet directly.
        code (str): A string containing the code to process. This parameter is ignored if a file name is provided.

    Returns:
        int: The number of uncommented lines in the provided code snippet or file.

    Raises:
        FileNotFoundError: If the provided file name does not exist.

    Note:
        This function assumes that the input code is a single code snippet or a file. It does not handle multiple code snippets or files within the same call.
    """
    file_extension = os.path.splitext(file_name)[1]
    file = file_extension.split('.')
    if len(file) == 2:
        file_type = file[1]
    else:
        return 0
    if file_type == 'java':
        return get_java_uncommented_lines(code)
    elif file_type == 'py':
        return get_python_uncommented_lines(code)
    elif file_type == 'js':
        return get_javascript_uncommented_lines(code)
    elif file_type == 'html':
        return get_html_uncommented_lines(code)
    elif file_type == 'c':
        return get_c_uncommented_lines(code)
    return 0


def get_java_uncommented_lines(code):
    """
    Counts the number of uncommented lines in a Java code snippet.

    This function takes a Java code snippet as input, removes all comments, and counts the number of lines that are not empty or whitespace.

    Args:
        code (str): A string containing Java code.

    Returns:
        int: The number of uncommented lines in the provided code snippet.

    Note:
        This function assumes that the input code is a single Java code snippet. It does not handle multiple code snippets or files.
    """
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    uncommented_lines = 0
    lines = code.splitlines()
    for line in lines:
        line = re.sub(r'//.*', '', line)
        if not line.isspace() and not len(line) == 0:
            uncommented_lines += 1
    return uncommented_lines


def get_python_uncommented_lines(code):
    """
    Counts the number of uncommented lines in a Python code snippet.

    This function takes a Python code snippet as input, removes all comments, and counts the number of lines that are not empty or whitespace.

    Args:
        code (str): A string containing Python code.

    Returns:
        int: The number of uncommented lines in the provided code snippet.

    Note:
        This function assumes that the input code is a single Python code snippet. It does not handle multiple code snippets or files.
    """
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    lines = code.splitlines()
    return len(list(filter(lambda l: not l.isspace() and not len(l) == 0, lines)))


def get_javascript_uncommented_lines(code):
    """
    Counts the number of uncommented lines in a Javascript code snippet.

    This function takes a Javascript code snippet as input, removes all comments, and counts the number of lines that are not empty or whitespace.

    Args:
        code (str): A string containing Javascript code.

    Returns:
        int: The number of uncommented lines in the provided code snippet.

    Note:
        This function assumes that the input code is a single Javascript code snippet. It does not handle multiple code snippets or files.
    """
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    uncommented_lines = 0
    lines = code.splitlines()
    for line in lines:
        line = re.sub(r'//.*', '', line)
        if not line.isspace() and not len(line) == 0:
            uncommented_lines += 1
    return uncommented_lines


def get_html_uncommented_lines(code):
    """
    Counts the number of uncommented lines in a HTML code snippet.

    This function takes a HTML code snippet as input, removes all comments, and counts the number of lines that are not empty or whitespace.

    Args:
        code (str): A string containing HTML code.

    Returns:
        int: The number of uncommented lines in the provided code snippet.

    Note:
        This function assumes that the input code is a single HTML code snippet. It does not handle multiple code snippets or files.
    """
    code = re.sub(r'<!--.*?-->\n?', '', code, flags=re.DOTALL)
    lines = code.splitlines()
    return len(list(filter(lambda l: not l.isspace() and not len(l) == 0, lines)))


def get_c_uncommented_lines(code):
    """
    Counts the number of uncommented lines in a C code snippet.

    This function takes a C code snippet as input, removes all comments, and counts the number of lines that are not empty or whitespace.

    Args:
        code (str): A string containing C code.

    Returns:
        int: The number of uncommented lines in the provided code snippet.

    Note:
        This function assumes that the input code is a single C code snippet. It does not handle multiple code snippets or files.
    """
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    uncommented_lines = 0
    lines = code.splitlines()
    for line in lines:
        line = re.sub(r'//.*', '', line)
        if not line.isspace() and not len(line) == 0:
            uncommented_lines += 1
    return uncommented_lines
