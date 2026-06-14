from ..database_manager import DBManager


class BaseService:
    def __init__(self, db_manager: DBManager):
        self._db = db_manager