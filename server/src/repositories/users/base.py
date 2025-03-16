from abc import ABC, abstractmethod
from src.models.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_users(
        self,
    ) -> list[User]: ...

    @abstractmethod
    async def get_user_by_id(
        self,
        id: str,
    ) -> User | None: ...

    @abstractmethod
    async def get_user_avatar(
        self,
        id: str,
    ) -> tuple[bytes, str]: ...

    @abstractmethod
    async def verify_basic_credentials(
        self,
        username: str,
        password: str,
    ) -> User | None: ...

    @abstractmethod
    async def verify_token(
        self,
        token: str,
    ) -> User | None: ...
