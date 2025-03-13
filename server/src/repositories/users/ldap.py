import logging
from contextlib import contextmanager

from ldap3 import Server, Connection
from src.models.user import User
from src.repositories.users.base import UserRepository


class LDAPUserRepository(UserRepository):
    def __init__(
        self,
        ldap_server: Server,
        attribute_map: dict[str, str],
        logger: logging.Logger,
    ):
        self.ldap_server = ldap_server
        self.attribute_map = attribute_map
        self.logger = logger

    @contextmanager
    def get_connection(self):
        connection = Connection(
            self.ldap_server,
            user="uid=admin,ou=people,dc=example,dc=com",
            password="password",
            auto_bind=True,
        )
        try:
            yield connection
        finally:
            connection.unbind()

    async def get_users(self) -> list[User]:
        search_base = "ou=people,dc=example,dc=com"
        search_filter = "(objectClass=person)"

        search_attributes = {
            key: attr for key, attr in self.attribute_map.items() if key != "avatar"
        }

        with self.get_connection() as connection:
            connection.search(
                search_base,
                search_filter,
                "SUBTREE",
                attributes=[attr for attr in self.attribute_map.values()],
            )

            return [
                User(
                    **{
                        user_field: entry[ldap_field].values[0]
                        if entry[ldap_field]
                        else None
                        for user_field, ldap_field in search_attributes.items()
                    },
                    # TODO: Remove hard coded API url
                    avatar_url=f"http://localhost:8000/users/{entry[self.attribute_map['id']].values[0]}/avatar"
                    if "avatar" in self.attribute_map
                    and len(entry[self.attribute_map["avatar"]].values) > 0
                    else None,
                )
                for entry in connection.entries
            ]

    async def get_user_avatar(self, id: str) -> tuple[bytes, str]:
        """Fetches a user's avatar from LDAP."""
        if "avatar" not in self.attribute_map:
            self.logger.warning("Avatar attribute not mapped in LDAP")
            return None, ""

        search_base = "ou=people,dc=example,dc=com"
        search_filter = f"({self.attribute_map['id']}={id})"
        avatar_field = self.attribute_map["avatar"]

        with self.get_connection() as connection:
            connection.search(
                search_base,
                search_filter,
                "SUBTREE",
                attributes=[avatar_field],
            )

            if not connection.entries:
                self.logger.warning(f"User {id} not found in LDAP")
                return None, ""

            entry = connection.entries[0]
            avatar_data = entry[avatar_field].value if entry[avatar_field] else None

            if not avatar_data:
                self.logger.info(f"No avatar found for user {id}")
                return None, ""

            return avatar_data, "image/jpeg"  # Adjust MIME type if necessary
