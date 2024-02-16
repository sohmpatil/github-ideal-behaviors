import os
import re


def getuncommentedLines(file_name, code):
    file_extension = os.path.splitext(file_name)[1]
    file_type = file_extension.split('.')[1]
    if file_type == 'java':
        return getJavaUncommentedLines(code)
    return 0


def getJavaUncommentedLines(code):
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*\n?', '', code)
    lines = code.splitlines()
    return len(lines)
