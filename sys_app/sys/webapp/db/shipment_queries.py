from enum import Enum
import datetime
import mariadb

from webapp.db.user_queries import increment_user_request_count
from webapp.utilities.decorators import get_db

from typing import List, Union, NamedTuple


class ShipmentQuery(str, Enum):
    SELECT_ALL_SHIPMENTS_BY_MAIL = "SELECT * FROM shipments WHERE trucker_mail = '{}';"
    SELECT_ALL_SHIPMENTS_BY_PLATE = "SELECT * FROM shipments WHERE license_plate = '{}';"
    GET_GPS_LOG_BY_ID = "SELECT GPS_log from shipments WHERE id = {};"
    EDIT_SHIPMENT = "UPDATE shipments SET status = {} WHERE id = {};"
    CREATE_SHIPMENT = "INSERT INTO " \
                      "shipments(trucker_mail, license_plate, start_date, end_date," \
                      "start_location, end_location, goods_type, goods_weight) " \
                      "VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', {});"


@get_db
def get_shipments_of_user(cursor: mariadb.connection.cursor, mail: str) -> List[Union[None, NamedTuple]]:
    cursor.execute(ShipmentQuery.SELECT_ALL_SHIPMENTS_BY_MAIL.format(mail))
    shipments = cursor.fetchall()
    return shipments


@get_db
def get_gps_log_by_id(cursor: mariadb.connection.cursor, shipment_id: int) -> Union[None, str]:
    cursor.execute(ShipmentQuery.SELECT_ALL_SHIPMENTS_BY_PLATE.format(shipment_id))
    gps_log = cursor.fetchone()
    return gps_log.GPS_log


@get_db
def get_shipments_by_plate(cursor: mariadb.connection.cursor, plate: str) -> List[Union[None, NamedTuple]]:
    cursor.execute(ShipmentQuery.SELECT_ALL_SHIPMENTS_BY_PLATE.format(plate))
    shipments = cursor.fetchall()
    return shipments


@get_db
def edit_shipment(cursor: mariadb.connection.cursor, shipment_id: int, shipment_status: int) -> None:
    cursor.execute(ShipmentQuery.EDIT_SHIPMENT.format(shipment_status + 1, shipment_id))


@get_db
def create_shipment(
        cursor: mariadb.connection.cursor,
        mail: str,
        plate: str,
        start_date: datetime.date,
        end_date: datetime.date,
        start_location: str,
        end_location: str,
        goods_type: str,
        goods_weight: int
) -> None:
    cursor.execute(ShipmentQuery.CREATE_SHIPMENT.format(
        mail,
        plate,
        start_date,
        end_date,
        start_location,
        end_location,
        goods_type,
        goods_weight
    ))
    increment_user_request_count(cursor, mail)
