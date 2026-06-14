from typing import Literal, List

from pydantic import BaseModel


class PermissionsSchema(BaseModel):
    object_type: Literal['file', 'role']
    actions: List[Literal[
        # Да, область пока тут, но про это ничего не говорилось в задании
        'create', 'create_all', 'give', 'read', 'update', 'delete', 'read_all', 'update_all', 'delete_all']]
