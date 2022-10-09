import re
import sys
import ast
from path_parser import PathParser
from style_errors import *


def is_function(line):
    regex = " *def +"

    if re.match(regex, line) is not None:
        return True
    return False


def is_class(line):
    regex = " *class +"

    if re.match(regex, line) is not None:
        return True
    return False


def find_comment_pos(line):
    quote, ignore, skip = None, False, False

    for i, c in enumerate(line):
        if skip:
            skip = False
            continue

        if c == '\\':
            skip = True
            continue

        if not ignore and (c == '"' or c == "'"):
            quote, ignore = c, True
        elif not ignore and c == '#':
            return i
        elif ignore and c == quote:
            quote, ignore = None, False

    return -1


def style_error_001(line):
    if len(line) > 79:
        return True

    return False


def style_error_002(line):
    for i, c in enumerate(line):
        if c != ' ' and i % 4 != 0:
            return True
        elif c != ' ':
            break

    return False


def style_error_003(line):
    pos = find_comment_pos(line)

    if pos != -1:
        line = line[:pos]
    line = line[::-1]

    for c in line:
        if c == ';':
            return True
        elif c != ' ':
            return False

    return False


def style_error_004(line):
    pos = find_comment_pos(line)

    if pos != -1:
        line = line[:pos]
        line = line[::-1]

        for i, c in enumerate(line):
            if c != ' ' and i < 2:
                return True
            elif c != ' ':
                return False

    return False


def style_error_005(line):
    pos = find_comment_pos(line)

    if pos != -1:
        line = line[pos+1:]
        words = line.lower().split(' ')

        for word in words:
            if word == 'todo':
                return True
    return False


def style_error_007(line):
    regex_class = " *class \\S"
    regex_function = " *def \\S"

    if is_class(line) and re.match(regex_class, line) is None:
        return True
    if is_function(line) and re.match(regex_function, line) is None:
        return True

    return False


def style_error_008(line):
    #   TODO    Should be rewritten with ast.
    regex = " *class +(?:[A-Z][a-z]*)+"

    if is_class(line) and re.match(regex, line) is None:
        return True
    return False


def style_error_009(line):
    #   TODO    Should be rewritten with ast.
    regex = " *def +(_*)(?:[a-z]+_?)+"

    if is_function(line) and re.match(regex, line) is None:
        return True
    return False


def style_error_010(line, path):
    #   TODO    Argument name arg_name should be written in snake_case;
    regex = "(?:_*?[a-z]+_*?)+"
    style_errors = list()

    tree = ast.parse(line)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            arguments, line_number = node.args.args, node.lineno
            arguments = [a.arg for a in arguments]
            for i, argument in enumerate(arguments):
                if re.match(regex, argument) is None:
                    style_errors.append(ArgumentNameNotSnakeCase(i, path))

    return style_errors


def style_error_011(line, path):
    #   TODO    There is pattern between function 011 - 012. Function can be united base on sat.walk loop. (also 009,0010)
    snake_case = "(?:_*?[a-z]+_*?)+"
    vars_wrong_names = set()
    style_errors = list()
    tree = ast.parse(line)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets, line_number = node.targets, node.lineno

            try:
                targets = [a.id for a in targets]
            except AttributeError:
                targets = [a.attr for a in targets]

            for target in targets:
                if target not in vars_wrong_names and re.match(snake_case, target) is None:
                    vars_wrong_names.add(target)
                    style_errors.append(VarNameNotSnakeCase(line_number, path))

    return style_errors


def style_error_012(line, path):
    #   TODO    The default argument value is mutable;
    style_errors = list()
    tree = ast.parse(line)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defaults, line_number = node.args.defaults, node.lineno

            for default in defaults:
                if not isinstance(default, ast.Constant):
                    style_errors.append(DefaultArgMutable(line_number, path))

    return style_errors


def static_code_analyze(code, file_path) -> list:
    #   TODO Function should be cut into smaller ones. Structure should be redesigned.
    style_errors_list = list()
    blanklines = 0

    for line_number, line in enumerate(code.split('\n')):

        if style_error_001(line):
            style_errors_list.append(LineTooLong(line_number, file_path))
        if style_error_002(line):
            style_errors_list.append(WrongIndentation(line_number, file_path))
        if style_error_003(line):
            style_errors_list.append(UnnecessarySemicolon(line_number, file_path))
        if style_error_004(line):
            style_errors_list.append(NotEnoughSpacesBeforeComment(line_number, file_path))
        if style_error_005(line):
            style_errors_list.append(Todo(line_number, file_path))
        if line.isspace() or not line:
            blanklines += 1
        else:
            if blanklines > 2:
                style_errors_list.append(TooManyLines(line_number, file_path))
            blanklines = 0
        if style_error_007(line):
            style_errors_list.append(TooManySpaces(line_number, file_path))
        if style_error_008(line):
            style_errors_list.append(ClassNameNotCamelCase(line_number, file_path))
        if style_error_009(line):
            style_errors_list.append(FunctionNameNotSnakeCase(line_number, file_path))

    style_errors_list.extend(style_error_010(code, file_path))
    style_errors_list.extend(style_error_011(code, file_path))
    style_errors_list.extend(style_error_012(code, file_path))

    #   TODO style_error_list contains members of class StyleError and cannot be sorted that way. Should be fixed.
    return style_errors_list


def analyze_files(python_files):
    errors_list = list()

    for python_file in python_files:
        file = open(python_file)
        code = file.read()
        errors_list.extend(static_code_analyze(code, python_file))

    for error in errors_list:
        print(error)


def main():
    args = sys.argv[1:]
    python_files = sorted(PathParser().path_parser(args))
    analyze_files(python_files)


if __name__ == '__main__':
    main()
