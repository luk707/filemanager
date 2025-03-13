import logging
from contextlib import contextmanager

from ldap3 import Server, Connection
from src.models.user import User
from src.repositories.users.base import UserRepository
from src.configuration import LDAPIdentityBackendConfiguration


class LDAPUserRepository(UserRepository):
    def __init__(
        self,
        configuration: LDAPIdentityBackendConfiguration,
        logger: logging.Logger,
    ):
        self.ldap_server = Server(
            host=configuration.host,
            port=configuration.port,
            get_info="ALL",
        )
        self.configuration = configuration
        self.logger = logger

    @contextmanager
    def get_bind_connection(self):
        connection = Connection(
            self.ldap_server,
            user=self.configuration.bind_dn,
            password=self.configuration.bind_password.get_secret_value(),
            auto_bind=True,
        )
        try:
            yield connection
        finally:
            connection.unbind()

    async def get_users(self) -> list[User]:
        search_attributes = {
            key: attr
            for key, attr in self.configuration.attribute_map.items()
            if key != "avatar"
        }

        with self.get_bind_connection() as connection:
            connection.search(
                self.configuration.base_dn,
                self.configuration.user_filter,
                "SUBTREE",
                attributes=[attr for attr in self.configuration.attribute_map.values()],
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
                    avatar_url=f"http://localhost:8000/users/{entry[self.configuration.attribute_map['id']].values[0]}/avatar"
                    if "avatar" in self.configuration.attribute_map
                    and len(entry[self.configuration.attribute_map["avatar"]].values)
                    > 0
                    else None,
                )
                for entry in connection.entries
            ]

    async def get_user_avatar(self, id: str) -> tuple[bytes, str]:
        """Fetches a user's avatar from LDAP."""
        if "avatar" not in self.configuration.attribute_map:
            self.logger.warning("Avatar attribute not mapped in LDAP")
            return None, ""

        avatar_attribute = self.configuration.attribute_map["avatar"]

        with self.get_bind_connection() as connection:
            connection.search(
                self.configuration.base_dn,
                f"({self.configuration.attribute_map['id']}={id})",
                "SUBTREE",
                attributes=[avatar_attribute],
            )

            if not connection.entries:
                self.logger.warning(f"User {id} not found in LDAP")
                return None, ""

            entry = connection.entries[0]
            avatar_data = (
                entry[avatar_attribute].value if entry[avatar_attribute] else None
            )

            if not avatar_data:
                self.logger.info(f"No avatar found for user {id}")
                return None, ""

            return avatar_data, "image/jpeg"  # Adjust MIME type if necessary
