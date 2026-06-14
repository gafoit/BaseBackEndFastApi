from typing import List

from pydantic import BaseModel


class RolePermissionsSchema(BaseModel):
    role_id: int
    permission_ids: List[int]

