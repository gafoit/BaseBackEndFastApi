import logging
import os

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=[os.getenv('CryptContext')],
    deprecated="auto"
)
logger = logging.getLogger(__name__)


class PasswordManager:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str) -> bool:
        return pwd_context.verify(plain_password, stored_hash)

