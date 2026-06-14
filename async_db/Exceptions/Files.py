class FileNotFound(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(f'File named {name} not found')


class FileAlreadyExists(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(f'File named {name} already exists')
