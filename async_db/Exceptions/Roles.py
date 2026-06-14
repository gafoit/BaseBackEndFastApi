class RoleAlreadyExists(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Role: '{self.name}' already exists")


class RoleDoesNotExist(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Role '{name}' does not exist")
