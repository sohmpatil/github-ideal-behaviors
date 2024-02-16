import os
import re


def getuncommentedLines(file_name, code):
    file_extension = os.path.splitext(file_name)[1]
    file_type = file_extension.split('.')[1]
    if file_type == 'java':
        return getJavaUncommentedLines(code)
    elif file_type == 'py':
        return getPythonUncommentedLines(code)
    elif file_type == 'js':
        return getJavaScriptUncommentedLines(code)
    elif file_type == 'html':
        return getHTMLUncommentedLines(code)
    elif file_type == 'c':
        return getCUncommentedLines(code)
    return 0


def getJavaUncommentedLines(code):
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*\n?', '', code)
    lines = code.splitlines()
    return len(lines)


def getPythonUncommentedLines(code):
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
    lines = code.splitlines()
    return len(lines)


def getJavaScriptUncommentedLines(code):
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*\n?', '', code)
    lines = code.splitlines()
    return len(lines)


def getHTMLUncommentedLines(code):
    code = re.sub(r'<!--.*?-->\n?', '', code, flags=re.DOTALL)
    lines = code.splitlines()
    return len(lines)


def getCUncommentedLines(code):
    code = re.sub(r'/\*.*?\*/\n?', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*\n?', '', code)
    lines = code.splitlines()
    return len(lines)
