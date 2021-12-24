from enum import Enum
from webapp.decorators.decorators import get_db
import mariadb
from typing import List, Union, NamedTuple


class ShipmentQuery(str, Enum):
    SELECT_ALL_SHIPMENT_BY_USERNAME = "SELECT * FROM shipments WHERE username = '{}';"


@get_db
def get_shipment_of_user(cursor: mariadb.connection.cursor, username: str) -> List[Union[None, NamedTuple]]:
    cursor.execute(ShipmentQuery.SELECT_ALL_SHIPMENT_BY_USERNAME.format(username))
    shipments = cursor.fetchall()
    return shipments


@get_db
def create_shipment(cursor: mariadb.connection.cursor, username: str) -> bool:
    pass
