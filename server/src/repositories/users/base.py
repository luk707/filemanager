from abc import ABC, abstractmethod
from src.models.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_users() -> list[User]: ...

    @abstractmethod
    async def get_user_avatar(id: str) -> tuple[bytes, str]: ...

    @abstractmethod
    async def verify_basic_credentials(username: str, password: str) -> bool: ...
