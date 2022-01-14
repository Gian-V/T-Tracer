import mariadb
import sys

from .config import settings

from typing import Optional


class Database:
    def __init__(self):
        self.db: Optional[mariadb.connection] = None

    def load(self) -> None:
        try:
            self.db = mariadb.connect(
                user=settings.database_user,
                password=settings.database_password,
                host=settings.database_host,
                port=settings.database_port,
                database=settings.database_name

            )
        except mariadb.Error as e:
            logging.warning(e)
            sys.exit(1)

        self.db.autocommit = True
        self.db.auto_reconnect = True

    def cursor(self) -> mariadb.connection.cursor:
        return self.db.cursor()

    def close(self):
        self.db.close()
        self.db = None
