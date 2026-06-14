from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from async_db import UserService, UserBlocked, UserDoesNotExist, UserLoggedOut, \
    PermissionsService
from token_manager import JWTManager
from async_db.database_manager import manager

from Models import UserSchema

security = HTTPBearer()


async def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(security)) -> UserSchema:
    token = creds.credentials
    try:
        payload = JWTManager.decode_token(token)
        user_data = await UserService(manager).check_user(payload['sub'],
                                                          payload['ver'])

    except ValueError as e:
        raise HTTPException(401, str(e))
    except UserDoesNotExist as e:
        raise HTTPException(400, str(e))
    except (UserBlocked, UserLoggedOut) as e:
        raise HTTPException(403, str(e))
    else:
        return user_data


def require_permission(object_type: str, action: str):
    async def checker(user_data=Depends(get_current_user)):
        flag = await PermissionsService(manager).check_permissions(user_data.id,
                                                                   object_type,
                                                                   action)
        if flag:
            return user_data
        raise HTTPException(403, "Permission denied")

    return checker
