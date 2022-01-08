from flask import Flask

import logging
import sys
import mariadb

from typing import Optional


class SQLOperation:

    def __init__(self):
        self.db: Optional[mariadb.connection] = None
        self.cursor: Optional[mariadb.connection.cursor] = None

    def init_app(self, app: Flask):
        try:
            self.db = mariadb.connect(
                user=app.config['DATABASE_USER'],
                password=app.config['DATABASE_PASSWORD'],
                host=app.config['DATABASE_HOST'],
                port=app.config['DATABASE_PORT'],
                database=app.config["DATABASE_NAME"]
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
