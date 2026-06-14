class ObjectActionAlreadyExists(Exception):
    def __init__(self, obj_type: str, action_name: str):
        self.obj_type = obj_type
        self.action_name = action_name
        super().__init__(
            f'Action [{action_name}] for object [{obj_type}] already exists')

class NoPermission(Exception):
    def __init__(self):
        super().__init__(
            'You do not have permission to perform this action'
        )
