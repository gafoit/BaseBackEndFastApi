import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError


class JWTManager:
    SECRET_KEY = os.getenv('JWT_SECRET')
    ALGORITHM = os.getenv('JWT_ALGORITHM')

    @classmethod
    def create_token(cls, user_id: int, token_ver: int):
        payload = {
            "sub": str(user_id),
            'ver': token_ver,
            "exp": datetime.now(timezone.utc) + timedelta(days=1)
        }
        token = jwt.encode(
            payload,
            cls.SECRET_KEY,
            algorithm=cls.ALGORITHM
        )
        return token

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                cls.SECRET_KEY,
                algorithms=[cls.ALGORITHM]
            )
            return payload

        except ExpiredSignatureError:
            raise ValueError("Token expired")

        except InvalidTokenError:
            raise ValueError("Invalid token")
