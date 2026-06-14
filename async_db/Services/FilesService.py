from Models import FileCreateRequest, FileRequest
from .BaseService import BaseService
from ..Exceptions import *
from ..Repos import UsersRepo
from ..Repos.FilesRepo import FilesRepo


class FilesService(BaseService):
    async def create(self, request: FileCreateRequest):
        async with self._db.session() as s:
            files_repo = FilesRepo(s)
            user_repo = UsersRepo(s)
            if user_repo.get(request.user_id) is None:
                raise UserDoesNotExist()
            file = await files_repo.get_by_user_name(request.user_id,
                                                     request.name)
            if file is not None:
                raise FileAlreadyExists(request.name)
            file = await files_repo.create(**request.model_dump())
            await s.flush()
            return {'status': 'success', 'msg': f'Created new file {file.name}'}

    async def read(self, request: FileRequest):
        async with self._db.session() as s:
            files_repo = FilesRepo(s)
            user_repo = UsersRepo(s)
            if user_repo.get(request.user_id) is None:
                raise UserDoesNotExist()
            file = await files_repo.get_by_user_name(**request.model_dump())
            if file is None:
                raise FileNotFound(request.name)
            return {'status': 'success',
                    'content': f'{file.name}:{file.content}'}

    async def update(self, request: FileCreateRequest):
        async with self._db.session() as s:
            files_repo = FilesRepo(s)
            user_repo = UsersRepo(s)
            if user_repo.get(request.user_id) is None:
                raise UserDoesNotExist()
            file = await files_repo.get_by_user_name(**request.model_dump())
            if file is None:
                raise FileNotFound(request.name)
            file.content = request.content
            await s.flush()
            return {'status': 'success',
                    'msg': f'File {file.name} updated successfully'}

    async def delete(self, request: FileRequest):
        async with self._db.session() as s:
            files_repo = FilesRepo(s)
            user_repo = UsersRepo(s)
            if user_repo.get(request.user_id) is None:
                raise UserDoesNotExist()
            file = await files_repo.get_by_user_name(**request.model_dump())
            if file is None:
                raise FileNotFound(request.name)
            await files_repo.delete(file)
            await s.flush()
            return {'status': 'success',
                    'msg': f'File {file.name} deleted successfully'}

    async def list(self, user_id):
        async with self._db.session() as s:
            files_repo = FilesRepo(s)
            user_repo = UsersRepo(s)
            if user_repo.get(user_id) is None:
                raise UserDoesNotExist()
            return {
                file.name: file.content
                for file in await files_repo.list_by_user(user_id)
            }
