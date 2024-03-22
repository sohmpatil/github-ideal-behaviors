import os
import re


def get_uncommented_lines(file_name, code):
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
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    uncommented_lines = 0
    lines = code.splitlines()
    for line in lines:
        line = re.sub(r'//.*', '', line)
        if not line.isspace() and not len(line) == 0:
            uncommented_lines += 1
    return uncommented_lines


def get_python_uncommented_lines(code):
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    lines = code.splitlines()
    return len(list(filter(lambda l: not l.isspace() and not len(l) == 0, lines)))


def get_javascript_uncommented_lines(code):
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    uncommented_lines = 0
    lines = code.splitlines()
    for line in lines:
        line = re.sub(r'//.*', '', line)
        if not line.isspace() and not len(line) == 0:
            uncommented_lines += 1
    return uncommented_lines


def get_html_uncommented_lines(code):
    code = re.sub(r'<!--.*?-->\n?', '', code, flags=re.DOTALL)
    lines = code.splitlines()
    return len(list(filter(lambda l: not l.isspace() and not len(l) == 0, lines)))


def get_c_uncommented_lines(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    uncommented_lines = 0
    lines = code.splitlines()
    for line in lines:
        line = re.sub(r'//.*', '', line)
        if not line.isspace() and not len(line) == 0:
            uncommented_lines += 1
    return uncommented_lines
