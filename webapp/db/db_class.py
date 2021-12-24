import logging
import sys
import mariadb
from typing import Optional


class SQLOperation:

    def __init__(self):
        self.db: Optional[mariadb.connection] = None
        self.cursor: Optional[mariadb.connection.cursor] = None

    def init_app(self, user: str, password: str, host: str, port: int, database: str):
        try:
            self.db = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database
            )
        except mariadb.Error as e:
            logging.warning(e)
            sys.exit(1)

        self.db.autocommit = True

    def connect(self) -> None:
        if self.cursor is None:
            self.cursor = self.db.cursor(named_tuple=True)

    def close(self) -> None:
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
