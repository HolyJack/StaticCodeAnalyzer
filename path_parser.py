import os


class PathParser:

    @staticmethod
    def is_python(filepath):
        if filepath[-3:] == ".py":
            return True
        return False

    @staticmethod
    def files_in_dir(directory):
        files = os.listdir(directory)
        for i, file in enumerate(files):
            files[i] = os.path.join(directory, file)

        return files

    def path_parser(self, args) -> list:
        python_files = list()

        for arg in args:
            if not os.path.exists(arg):
                continue
            elif os.path.isdir(arg):
                python_files.extend(self.path_parser(self.files_in_dir(arg)))
            elif os.path.isfile(arg) and self.is_python(arg):
                python_files.append(arg)

        return python_files
