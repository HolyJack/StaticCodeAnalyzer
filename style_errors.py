class StyleError:
    #   TODO    Wooden leg with line number should be fixed. Error message should be move to arg or method.
    def __init__(self, line, path):
        self.path = path
        self.line = line + 1
        self.error_number = "000"
        self.message = ""

    def __str__(self):
        return f"{self.path}: Line {self.line}: S{self.error_number} {self.message}"


class LineTooLong(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "001"
        self.message = "Too long line"


class WrongIndentation(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "002"
        self.message = "Indentation is not a multiple of four"


class UnnecessarySemicolon(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "003"
        self.message = "Unnecessary semicolon"


class NotEnoughSpacesBeforeComment(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "004"
        self.message = "At least two spaces required before inline comments"


class Todo(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "005"
        self.message = "TODO found"


class TooManyLines(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "006"
        self.message = "More than two blank lines used before this line"


class TooManySpaces(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "007"
        self.message = "Too many spaces after construction_name (def or class)"


class ClassNameNotCamelCase(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "008"
        self.message = "Class name class_name should be written in CamelCase"


class FunctionNameNotSnakeCase(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.error_number = "009"
        self.message = "Function name function_name should be written in snake_case"


class ArgumentNameNotSnakeCase(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.line = line
        self.error_number = "010"
        self.message = "Argument name should " \
                       "be written in snake_case"


class VarNameNotSnakeCase(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.line = line
        self.error_number = "011"
        self.message = "Variable name should be written in snake_case"


class DefaultArgMutable(StyleError):

    def __init__(self, line, path):
        super().__init__(line, path)
        self.line = line
        self.error_number = "012"
        self.message = "Default argument value is mutable"
